from decimal import Decimal

from models import db
from models.user_setting import UserSetting
from utils.subscription_utils import quantize_money


ALLOWED_SPENDING_CAP_MODES = {"none", "soft", "hard"}


def get_or_create_user_settings(user):
    """Return the user's settings row, creating defaults when missing."""
    settings = user.settings

    if settings:
        return settings

    settings = UserSetting(user_id=user.user_id)
    db.session.add(settings)
    db.session.flush()
    return settings


def serialize_user_settings(settings):
    return settings.to_dict()


def build_cap_status(settings, current_monthly_total):
    """Return current cap state for the settings UI and warning logic."""
    mode = settings.spending_cap_mode if settings else "none"
    cap_amount = quantize_money(getattr(settings, "spending_cap_amount", 0) or 0)
    overage_percent = Decimal(
        str(getattr(settings, "soft_cap_overage_percent", 0) or 0)
    )
    current_total = quantize_money(current_monthly_total or 0)
    enabled = mode in {"soft", "hard"} and cap_amount > 0
    soft_cap_limit = (
        quantize_money(cap_amount * (Decimal("1") + (overage_percent / Decimal("100"))))
        if mode == "soft" and enabled
        else None
    )

    is_at_cap = enabled and current_total == cap_amount
    is_over_cap = enabled and current_total > cap_amount
    is_over_soft_limit = bool(
        mode == "soft"
        and soft_cap_limit is not None
        and current_total > soft_cap_limit
    )

    warning_message = None

    if enabled and mode == "hard":
        if is_at_cap:
            warning_message = "You have reached your hard cap."
        elif is_over_cap:
            warning_message = "Your active subscriptions are above the hard cap."
    elif enabled and mode == "soft":
        if is_over_soft_limit:
            warning_message = "Your active subscriptions are above the soft cap limit."
        elif is_over_cap:
            warning_message = "Your active subscriptions are above the base soft cap."

    return {
        "mode": mode,
        "enabled": enabled,
        "cap_amount": float(cap_amount),
        "soft_cap_overage_percent": float(overage_percent),
        "soft_cap_limit": float(soft_cap_limit) if soft_cap_limit is not None else None,
        "current_monthly_total": float(current_total),
        "is_at_cap": is_at_cap,
        "is_over_cap": is_over_cap,
        "is_over_soft_limit": is_over_soft_limit,
        "warning_message": warning_message,
    }


def evaluate_cap_limit(settings, current_monthly_total, projected_monthly_total):
    """Evaluate whether a projected monthly total is allowed for the user."""
    cap_status = build_cap_status(settings, current_monthly_total)
    mode = cap_status["mode"]
    enabled = cap_status["enabled"]
    projected_total = quantize_money(projected_monthly_total)

    if not enabled:
        return {
            "allowed": True,
            "cap_warning": None,
        }

    cap_amount = quantize_money(settings.spending_cap_amount)
    overage_percent = Decimal(str(settings.soft_cap_overage_percent or 0))
    soft_cap_limit = (
        quantize_money(cap_amount * (Decimal("1") + (overage_percent / Decimal("100"))))
        if mode == "soft"
        else None
    )

    if mode == "hard":
        if projected_total > cap_amount:
            return {
                "allowed": False,
                "cap_warning": {
                    "mode": "hard",
                    "cap_amount": float(cap_amount),
                    "projected_monthly_total": float(projected_total),
                    "message": "Adding this subscription would exceed your hard cap.",
                },
            }

        if projected_total == cap_amount:
            return {
                "allowed": True,
                "cap_warning": {
                    "mode": "hard",
                    "cap_amount": float(cap_amount),
                    "projected_monthly_total": float(projected_total),
                    "message": "This subscription reaches your hard cap.",
                },
            }

        return {
            "allowed": True,
            "cap_warning": None,
        }

    if projected_total > soft_cap_limit:
        return {
            "allowed": False,
            "cap_warning": {
                "mode": "soft",
                "cap_amount": float(cap_amount),
                "soft_cap_overage_percent": float(overage_percent),
                "soft_cap_limit": float(soft_cap_limit),
                "projected_monthly_total": float(projected_total),
                "message": "Adding this subscription would exceed your soft cap limit.",
            },
        }

    if projected_total > cap_amount:
        return {
            "allowed": True,
            "cap_warning": {
                "mode": "soft",
                "cap_amount": float(cap_amount),
                "soft_cap_overage_percent": float(overage_percent),
                "soft_cap_limit": float(soft_cap_limit),
                "projected_monthly_total": float(projected_total),
                "message": "This subscription goes above your base soft cap.",
            },
        }

    return {
        "allowed": True,
        "cap_warning": None,
    }

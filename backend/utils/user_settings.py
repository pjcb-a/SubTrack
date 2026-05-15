from decimal import Decimal, ROUND_HALF_UP

from models import db
from models.subscription import Subscription
from models.user_setting import UserSetting
from utils.subscription_utils import calculate_monthly_cost_from_recurrence


CAP_MODES = {"none", "soft", "hard"}


def get_or_create_user_settings(user):
    settings = UserSetting.query.filter_by(user_id=user.user_id).first()

    if settings:
        return settings

    settings = UserSetting(user_id=user.user_id)
    settings.spending_cap_amount = Decimal("0.00")
    settings.soft_cap_overage_percent = Decimal("0.00")
    user.settings = settings
    db.session.add(settings)
    db.session.flush()
    return settings


def quantize_money(value):
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def get_current_monthly_total(user, exclude_subscription_id=None):
    active_subscriptions = Subscription.query.filter_by(
        user_id=user.user_id,
        is_active=True,
    ).all()

    total = Decimal("0.00")

    for subscription in active_subscriptions:
        if exclude_subscription_id and subscription.subscription_id == exclude_subscription_id:
            continue

        total += Decimal(
            str(calculate_monthly_cost_from_recurrence(
                subscription.amount,
                subscription.recurrence_unit,
                subscription.recurrence_interval,
            ))
        )

    return quantize_money(total)


def build_cap_status(user, projected_monthly_total=None):
    settings = get_or_create_user_settings(user)
    current_total = get_current_monthly_total(user)
    cap_amount = (
        quantize_money(settings.spending_cap_amount)
        if settings.spending_cap_amount is not None
        else None
    )
    overage_percent = (
        Decimal(str(settings.soft_cap_overage_percent))
        if settings.soft_cap_overage_percent is not None
        else Decimal("0")
    )
    soft_limit = None

    if cap_amount is not None and settings.spending_cap_mode == "soft":
        soft_limit = quantize_money(
            cap_amount * (Decimal("1") + (overage_percent / Decimal("100")))
        )

    target_total = (
        quantize_money(projected_monthly_total)
        if projected_monthly_total is not None
        else current_total
    )

    warning_message = None
    is_at_cap = False
    is_over_cap = False
    is_over_soft_limit = False

    if settings.spending_cap_mode == "hard" and cap_amount is not None:
        is_at_cap = target_total == cap_amount
        is_over_cap = target_total > cap_amount
        if is_over_cap:
            warning_message = "This subscription would exceed your hard monthly cap."
        elif is_at_cap:
            warning_message = "You have reached your hard monthly cap."
    elif settings.spending_cap_mode == "soft" and cap_amount is not None:
        is_over_cap = target_total > cap_amount
        is_over_soft_limit = soft_limit is not None and target_total > soft_limit
        if is_over_soft_limit:
            warning_message = "This subscription would exceed your soft cap allowance."
        elif is_over_cap:
            warning_message = "This subscription goes beyond your soft cap allowance warning threshold."

    return {
        "mode": settings.spending_cap_mode,
        "enabled": settings.spending_cap_mode != "none",
        "cap_amount": float(cap_amount) if cap_amount is not None else None,
        "soft_cap_overage_percent": float(overage_percent),
        "soft_cap_limit": float(soft_limit) if soft_limit is not None else None,
        "current_monthly_total": float(current_total),
        "projected_monthly_total": float(target_total),
        "is_at_cap": is_at_cap,
        "is_over_cap": is_over_cap,
        "is_over_soft_limit": is_over_soft_limit,
        "warning_message": warning_message,
    }


def evaluate_cap_change(user, projected_monthly_total):
    cap_status = build_cap_status(user, projected_monthly_total=projected_monthly_total)
    mode = cap_status["mode"]

    if mode == "none" or cap_status["cap_amount"] is None:
        return None

    if mode == "hard":
        if cap_status["is_over_cap"]:
            return {
                "allowed": False,
                "status": 409,
                "message": cap_status["warning_message"],
                "cap_status": cap_status,
            }

        if cap_status["is_at_cap"]:
            return {
                "allowed": True,
                "warning": cap_status["warning_message"],
                "cap_status": cap_status,
            }

        return None

    if mode == "soft":
        if cap_status["is_over_soft_limit"]:
            return {
                "allowed": False,
                "status": 409,
                "message": cap_status["warning_message"],
                "cap_status": cap_status,
            }

        if cap_status["is_over_cap"]:
            return {
                "allowed": True,
                "warning": cap_status["warning_message"],
                "cap_status": cap_status,
            }

    return None

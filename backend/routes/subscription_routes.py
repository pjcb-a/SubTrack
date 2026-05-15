"""
Subscription CRUD and dashboard support endpoints.

These routes are intended to back the dashboard cards, calendar, upcoming list,
and summary values in the frontend once the mock store is replaced with API
requests.
"""

from datetime import date, datetime, timedelta
from decimal import Decimal

from flask import Blueprint, jsonify, request, g

from models import db
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from utils.auth import login_required
from utils.subscription_utils import (
    calculate_monthly_cost,
    calculate_monthly_cost_from_recurrence,
    get_next_due_date,
    iter_occurrences_in_range,
    parse_date,
)
from utils.user_settings import evaluate_cap_change, get_current_monthly_total
from utils.validators import validate_subscription_payload


subscription_bp = Blueprint("subscriptions", __name__, url_prefix="/api/subscriptions")


def get_user_subscription_or_404(subscription_id, user_id):
    """Load a subscription only if it belongs to the logged-in user.

    This prevents users from reading or editing another user's subscription by
    guessing an ID in the URL.
    """
    subscription = Subscription.query.filter_by(
        subscription_id=subscription_id,
        user_id=user_id,
    ).first()

    if not subscription:
        return None, (jsonify({"error": "Subscription not found"}), 404)

    return subscription, None


@subscription_bp.get("")
@login_required
def list_subscriptions():
    """Return every subscription owned by the logged-in user.

    Expected frontend use:
    Dashboard tables, cards, or calendar views can call this to populate the
    user's full subscription list.
    """
    subscriptions = (
        Subscription.query.filter_by(
            user_id=g.current_user.user_id,
            is_active=True,
        )
        .order_by(Subscription.subscription_id.desc())
        .all()
    )

    return jsonify(
        {
            "subscriptions": [subscription.to_dict() for subscription in subscriptions],
        }
    )


@subscription_bp.get("/history")
@login_required
def list_subscription_history():
    """Return deleted subscriptions so the history view survives refreshes."""
    subscriptions = (
        Subscription.query.filter_by(user_id=g.current_user.user_id)
        .filter(Subscription.deleted_at.isnot(None))
        .order_by(Subscription.deleted_at.desc(), Subscription.subscription_id.desc())
        .all()
    )

    return jsonify(
        {
            "subscriptions": [subscription.to_dict() for subscription in subscriptions],
        }
    )


@subscription_bp.post("")
@login_required
def create_subscription():
    """Validate input, create a subscription row, and create its reminder row.

    Expected frontend use:
    The add-subscription modal should eventually POST its form data here.
    """
    data = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_subscription_payload(data, partial=False)

    if errors:
        return jsonify({"errors": errors}), 400

    notification_data = cleaned_data.pop("notification_setting", {})

    projected_total = get_current_monthly_total(g.current_user) + Decimal(
        str(calculate_monthly_cost_from_recurrence(
            cleaned_data["amount"],
            cleaned_data.get("recurrence_unit"),
            cleaned_data.get("recurrence_interval"),
        ))
    )
    cap_result = evaluate_cap_change(g.current_user, projected_total)

    if cap_result and not cap_result["allowed"]:
        return jsonify(
            {
                "error": cap_result["message"],
                "cap_status": cap_result["cap_status"],
            }
        ), cap_result["status"]

    subscription = Subscription(
        user_id=g.current_user.user_id,
        **cleaned_data,
    )
    subscription.notification_setting = NotificationSetting(
        notify_days_before=notification_data.get("notify_days_before", 3),
        notification_enabled=notification_data.get("notification_enabled", True),
    )

    db.session.add(subscription)
    db.session.commit()

    response_payload = {
        "message": "Subscription created successfully",
        "subscription": subscription.to_dict(),
    }
    if cap_result and cap_result.get("warning"):
        response_payload["cap_warning"] = cap_result["cap_status"]

    return (
        jsonify(response_payload),
        201,
    )


@subscription_bp.get("/upcoming")
@login_required
def get_upcoming_subscriptions():
    """Return only active subscriptions due in the next 7 days.

    Expected frontend use:
    This can drive an "upcoming renewals" card without the frontend having to
    calculate due dates by itself.
    """
    today = date.today()
    end_date = today + timedelta(days=7)

    subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()

    upcoming_items = []

    for subscription in subscriptions:
        next_due_date = get_next_due_date(subscription, today)

        if next_due_date and today <= next_due_date <= end_date:
            subscription_data = subscription.to_dict()
            subscription_data["next_due_date"] = next_due_date.isoformat()
            subscription_data["days_until_due"] = (next_due_date - today).days
            upcoming_items.append(subscription_data)

    upcoming_items.sort(key=lambda item: item["next_due_date"])

    return jsonify(
        {
            "upcoming_subscriptions": upcoming_items,
        }
    )


@subscription_bp.get("/summary")
@login_required
def get_subscription_summary():
    """Return summary numbers for high-level dashboard widgets.

    This endpoint centralizes the billing-cycle math so the frontend does not
    need to duplicate monthly/quarterly/yearly conversion rules.
    """
    active_subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()

    total_monthly_cost = sum(
        calculate_monthly_cost_from_recurrence(
            subscription.amount,
            subscription.recurrence_unit,
            subscription.recurrence_interval,
        )
        for subscription in active_subscriptions
    )

    return jsonify(
        {
            "summary": {
                "active_subscriptions": len(active_subscriptions),
                "total_monthly_cost": round(total_monthly_cost, 2),
            }
        }
    )


@subscription_bp.get("/calendar")
@login_required
def get_subscription_calendar():
    from_value = request.args.get("from", "")
    to_value = request.args.get("to", "")
    range_start = parse_date(from_value)
    range_end = parse_date(to_value)

    if not range_start or not range_end:
        return jsonify({"error": "from and to must use YYYY-MM-DD format."}), 400

    if range_start > range_end:
        return jsonify({"error": "from cannot be later than to."}), 400

    if (range_end - range_start).days > 366:
        return jsonify({"error": "Calendar range cannot exceed 366 days."}), 400

    subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()

    occurrences = []
    for subscription in subscriptions:
        for occurrence_date in iter_occurrences_in_range(subscription, range_start, range_end):
            subscription_data = subscription.to_dict()
            occurrences.append(
                {
                    "subscription_id": subscription.subscription_id,
                    "subscription_name": subscription.subscription_name,
                    "amount": float(subscription.amount),
                    "category_id": subscription.category_id,
                    "category_name": subscription_data["category_name"],
                    "occurrence_date": occurrence_date.isoformat(),
                    "recurrence_unit": subscription_data["recurrence_unit"],
                    "recurrence_interval": subscription_data["recurrence_interval"],
                    "is_active": subscription.is_active,
                }
            )

    occurrences.sort(key=lambda item: (item["occurrence_date"], item["subscription_name"]))
    return jsonify({"occurrences": occurrences})


@subscription_bp.get("/<int:subscription_id>")
@login_required
def get_subscription(subscription_id):
    """Return a single subscription for details or edit screens."""
    subscription, error_response = get_user_subscription_or_404(
        subscription_id,
        g.current_user.user_id,
    )

    if error_response:
        return error_response

    return jsonify({"subscription": subscription.to_dict()})


@subscription_bp.put("/<int:subscription_id>")
@login_required
def update_subscription(subscription_id):
    """Apply partial or full subscription updates for the current user.

    Expected frontend use:
    The update modal can send only changed fields or the full form payload.
    """
    subscription, error_response = get_user_subscription_or_404(
        subscription_id,
        g.current_user.user_id,
    )

    if error_response:
        return error_response

    data = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_subscription_payload(data, partial=True)

    if errors:
        return jsonify({"errors": errors}), 400

    notification_data = cleaned_data.pop("notification_setting", None)

    next_amount = cleaned_data.get("amount", subscription.amount)
    next_recurrence_unit = cleaned_data.get(
        "recurrence_unit",
        subscription.recurrence_unit,
    )
    next_recurrence_interval = cleaned_data.get(
        "recurrence_interval",
        subscription.recurrence_interval,
    )
    current_total = get_current_monthly_total(
        g.current_user,
        exclude_subscription_id=subscription.subscription_id,
    )
    projected_total = current_total + Decimal(
        str(calculate_monthly_cost_from_recurrence(
            next_amount,
            next_recurrence_unit,
            next_recurrence_interval,
        ))
    )
    cap_result = evaluate_cap_change(g.current_user, projected_total)

    if cap_result and not cap_result["allowed"]:
        return jsonify(
            {
                "error": cap_result["message"],
                "cap_status": cap_result["cap_status"],
            }
        ), cap_result["status"]

    for field_name, value in cleaned_data.items():
        setattr(subscription, field_name, value)

    if notification_data is not None:
        if not subscription.notification_setting:
            subscription.notification_setting = NotificationSetting()

        if "notify_days_before" in notification_data:
            subscription.notification_setting.notify_days_before = notification_data[
                "notify_days_before"
            ]

        if "notification_enabled" in notification_data:
            subscription.notification_setting.notification_enabled = notification_data[
                "notification_enabled"
            ]

    if "is_active" in cleaned_data and cleaned_data["is_active"]:
        subscription.deleted_at = None

    db.session.commit()

    response_payload = {
        "message": "Subscription updated successfully",
        "subscription": subscription.to_dict(),
    }
    if cap_result and cap_result.get("warning"):
        response_payload["cap_warning"] = cap_result["cap_status"]

    return jsonify(response_payload)


@subscription_bp.delete("/<int:subscription_id>")
@login_required
def delete_subscription(subscription_id):
    """Move one subscription into history instead of hard-deleting it."""
    subscription, error_response = get_user_subscription_or_404(
        subscription_id,
        g.current_user.user_id,
    )

    if error_response:
        return error_response

    subscription.is_active = False
    subscription.deleted_at = datetime.utcnow()
    db.session.commit()

    return jsonify(
        {
            "message": "Subscription moved to history successfully",
            "subscription": subscription.to_dict(),
        }
    )


@subscription_bp.delete("/history")
@login_required
def clear_subscription_history():
    """Permanently remove deleted subscriptions from the history view."""
    deleted_subscriptions = (
        Subscription.query.filter_by(
            user_id=g.current_user.user_id,
            is_active=False,
        )
        .filter(Subscription.deleted_at.isnot(None))
        .all()
    )

    for subscription in deleted_subscriptions:
        db.session.delete(subscription)

    db.session.commit()

    return jsonify({"message": "Subscription history cleared successfully"})

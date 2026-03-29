"""
Subscription CRUD and dashboard support endpoints.

These routes are intended to back the dashboard cards, calendar, upcoming list,
and summary values in the frontend once the mock store is replaced with API
requests.
"""

from datetime import date, timedelta

from flask import Blueprint, jsonify, request, g

from models import db
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from utils.auth import login_required
from utils.subscription_utils import calculate_monthly_cost, get_next_due_date
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
        Subscription.query.filter_by(user_id=g.current_user.user_id)
        .order_by(Subscription.subscription_id.desc())
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

    return (
        jsonify(
            {
                "message": "Subscription created successfully",
                "subscription": subscription.to_dict(),
            }
        ),
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
        calculate_monthly_cost(subscription.amount, subscription.billing_cycle)
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

    db.session.commit()

    return jsonify(
        {
            "message": "Subscription updated successfully",
            "subscription": subscription.to_dict(),
        }
    )


@subscription_bp.delete("/<int:subscription_id>")
@login_required
def delete_subscription(subscription_id):
    """Delete one subscription belonging to the logged-in user."""
    subscription, error_response = get_user_subscription_or_404(
        subscription_id,
        g.current_user.user_id,
    )

    if error_response:
        return error_response

    db.session.delete(subscription)
    db.session.commit()

    return jsonify({"message": "Subscription deleted successfully"})

"""
Subscription CRUD, recurrence, history, and dashboard support endpoints.
"""

from datetime import date, datetime, timedelta
from types import SimpleNamespace

from flask import Blueprint, g, jsonify, request

from models import db
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from utils.auth import login_required
from utils.subscription_utils import (
    calculate_active_monthly_total,
    calculate_monthly_cost,
    get_occurrences_in_range,
    get_next_due_date,
    get_subscription_monthly_equivalent,
    parse_date,
)
from utils.user_settings import evaluate_cap_limit, get_or_create_user_settings
from utils.validators import validate_subscription_payload


subscription_bp = Blueprint(
    "subscriptions",
    __name__,
    url_prefix="/api/subscriptions",
)


def get_user_subscription_or_404(subscription_id, user_id):
    subscription = Subscription.query.filter_by(
        subscription_id=subscription_id,
        user_id=user_id,
    ).first()

    if not subscription:
        return None, (jsonify({"error": "Subscription not found"}), 404)

    return subscription, None


def get_active_user_subscriptions(user_id):
    return Subscription.query.filter_by(user_id=user_id, is_active=True).all()


def validate_calendar_window(start_date, end_date):
    if not start_date or not end_date:
        return {"error": "Both from and to dates are required."}, 400

    if start_date > end_date:
        return {"error": "The from date must be before or equal to the to date."}, 400

    if (end_date - start_date).days > 366:
        return {"error": "Calendar requests cannot exceed 366 days."}, 400

    return None, None


def build_cap_evaluation(user, candidate_subscription, exclude_subscription_id=None):
    settings = get_or_create_user_settings(user)
    current_total = calculate_active_monthly_total(
        get_active_user_subscriptions(user.user_id),
        exclude_subscription_id=exclude_subscription_id,
    )

    if candidate_subscription.is_active is False:
        return current_total, {"allowed": True, "cap_warning": None}

    projected_total = (
        current_total + get_subscription_monthly_equivalent(candidate_subscription)
    )
    evaluation = evaluate_cap_limit(settings, current_total, projected_total)
    return current_total, evaluation


def build_candidate_subscription(subscription, cleaned_data):
    candidate = SimpleNamespace(
        subscription_id=subscription.subscription_id,
        amount=cleaned_data.get("amount", subscription.amount),
        recurrence_unit=cleaned_data.get(
            "recurrence_unit",
            subscription.recurrence_unit,
        ),
        recurrence_interval=cleaned_data.get(
            "recurrence_interval",
            subscription.recurrence_interval,
        ),
        anchor_date=cleaned_data.get("anchor_date", subscription.anchor_date),
        start_date=cleaned_data.get("start_date", subscription.start_date),
        billing_cycle=subscription.billing_cycle,
        is_active=cleaned_data.get("is_active", subscription.is_active),
    )

    if not candidate.anchor_date:
        candidate.anchor_date = candidate.start_date

    if not candidate.start_date:
        candidate.start_date = candidate.anchor_date

    return candidate


@subscription_bp.get("")
@login_required
def list_subscriptions():
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


@subscription_bp.get("/calendar")
@login_required
def get_subscription_calendar():
    start_date = parse_date(request.args.get("from"))
    end_date = parse_date(request.args.get("to"))
    error_payload, error_status = validate_calendar_window(start_date, end_date)

    if error_payload:
        return jsonify(error_payload), error_status

    subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()
    occurrences = []

    for subscription in subscriptions:
        for occurrence_date in get_occurrences_in_range(
            subscription,
            start_date,
            end_date,
        ):
            occurrences.append(
                {
                    "subscription_id": subscription.subscription_id,
                    "subscription_name": subscription.subscription_name,
                    "amount": float(subscription.amount),
                    "category_id": subscription.category_id,
                    "category_name": (
                        subscription.category.category_name
                        if subscription.category
                        else None
                    ),
                    "occurrence_date": occurrence_date.isoformat(),
                    "recurrence_unit": subscription.recurrence_unit,
                    "recurrence_interval": subscription.recurrence_interval,
                }
            )

    occurrences.sort(
        key=lambda occurrence: (
            occurrence["occurrence_date"],
            occurrence["subscription_id"],
        )
    )

    return jsonify({"occurrences": occurrences})


@subscription_bp.post("")
@login_required
def create_subscription():
    data = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_subscription_payload(data, partial=False)

    if errors:
        return jsonify({"error": "Validation failed.", "errors": errors}), 400

    notification_data = cleaned_data.pop("notification_setting", {})
    subscription = Subscription(
        user_id=g.current_user.user_id,
        **cleaned_data,
    )
    if subscription.is_active is None:
        subscription.is_active = True
    subscription.sync_legacy_schedule_fields()

    current_total, evaluation = build_cap_evaluation(g.current_user, subscription)

    if not evaluation["allowed"]:
        return jsonify(
            {
                "error": evaluation["cap_warning"]["message"],
                "cap_warning": evaluation["cap_warning"],
            }
        ), 409

    subscription.notification_setting = NotificationSetting(
        notify_days_before=notification_data.get("notify_days_before", 3),
        notification_enabled=notification_data.get("notification_enabled", True),
    )
    db.session.add(subscription)
    db.session.commit()

    response_body = {
        "message": "Subscription created successfully.",
        "subscription": subscription.to_dict(),
    }

    if evaluation["cap_warning"]:
        response_body["cap_warning"] = evaluation["cap_warning"]

    return jsonify(response_body), 201


@subscription_bp.get("/upcoming")
@login_required
def get_upcoming_subscriptions():
    today = date.today()
    end_date = today + timedelta(days=7)
    subscriptions = get_active_user_subscriptions(g.current_user.user_id)
    upcoming_items = []

    for subscription in subscriptions:
        next_due_date = get_next_due_date(subscription, today)

        if next_due_date and today <= next_due_date <= end_date:
            subscription_data = subscription.to_dict()
            subscription_data["next_due_date"] = next_due_date.isoformat()
            subscription_data["days_until_due"] = (next_due_date - today).days
            upcoming_items.append(subscription_data)

    upcoming_items.sort(key=lambda item: item["next_due_date"])

    return jsonify({"upcoming_subscriptions": upcoming_items})


@subscription_bp.get("/summary")
@login_required
def get_subscription_summary():
    active_subscriptions = get_active_user_subscriptions(g.current_user.user_id)
    total_monthly_cost = sum(
        calculate_monthly_cost(
            subscription.amount,
            subscription.recurrence_unit,
            subscription.recurrence_interval,
            subscription.billing_cycle,
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


@subscription_bp.get("/<int:subscription_id>")
@login_required
def get_subscription(subscription_id):
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
    subscription, error_response = get_user_subscription_or_404(
        subscription_id,
        g.current_user.user_id,
    )

    if error_response:
        return error_response

    data = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_subscription_payload(data, partial=True)

    if errors:
        return jsonify({"error": "Validation failed.", "errors": errors}), 400

    notification_data = cleaned_data.pop("notification_setting", None)
    candidate_subscription = build_candidate_subscription(subscription, cleaned_data)
    current_total, evaluation = build_cap_evaluation(
        g.current_user,
        candidate_subscription,
        exclude_subscription_id=subscription.subscription_id,
    )

    if not evaluation["allowed"]:
        return jsonify(
            {
                "error": evaluation["cap_warning"]["message"],
                "cap_warning": evaluation["cap_warning"],
            }
        ), 409

    for field_name, value in cleaned_data.items():
        setattr(subscription, field_name, value)

    if any(
        field_name in cleaned_data
        for field_name in (
            "recurrence_unit",
            "recurrence_interval",
            "anchor_date",
            "start_date",
        )
    ):
        subscription.sync_legacy_schedule_fields()

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

    if "is_active" in cleaned_data:
        if cleaned_data["is_active"]:
            subscription.deleted_at = None
        elif not subscription.deleted_at:
            subscription.deleted_at = datetime.utcnow()

    db.session.commit()

    response_body = {
        "message": "Subscription updated successfully.",
        "subscription": subscription.to_dict(),
    }

    if evaluation["cap_warning"]:
        response_body["cap_warning"] = evaluation["cap_warning"]

    return jsonify(response_body)


@subscription_bp.delete("/<int:subscription_id>")
@login_required
def delete_subscription(subscription_id):
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
            "message": "Subscription moved to history successfully.",
            "subscription": subscription.to_dict(),
        }
    )


@subscription_bp.delete("/history")
@login_required
def clear_subscription_history():
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

    return jsonify({"message": "Subscription history cleared successfully."})

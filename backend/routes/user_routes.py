"""
User profile, settings, and data transfer endpoints.
"""

from datetime import datetime
from io import BytesIO

from flask import Blueprint, Response, g, jsonify, request, session
from sqlalchemy import func
from sqlalchemy.orm import selectinload
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.category import Category
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from models.user import User
from utils.auth import login_required
from utils.subscription_csv import (
    build_csv_payload,
    build_duplicate_fingerprint,
    read_import_rows,
    validate_import_row,
)
from utils.subscription_utils import (
    calculate_active_monthly_total,
    get_legacy_billing_cycle,
    get_subscription_monthly_equivalent,
    parse_datetime,
    quantize_money,
)
from utils.user_settings import (
    build_cap_status,
    evaluate_cap_limit,
    get_or_create_user_settings,
    serialize_user_settings,
)
from utils.validators import (
    is_valid_email,
    validate_user_settings_payload,
)


user_bp = Blueprint("user", __name__, url_prefix="/api/user")


def get_case_insensitive_category_map():
    categories = Category.query.order_by(Category.category_name.asc()).all()
    return {
        category.category_name.strip().lower(): category for category in categories
    }


def build_import_response(created_ids, row_results):
    warning_count = sum(
        1 for row_result in row_results if row_result["status"] == "warning"
    )
    skipped_count = sum(
        1 for row_result in row_results if row_result["status"] == "skipped"
    )

    return {
        "created_count": len(created_ids),
        "skipped_count": skipped_count,
        "warning_count": warning_count,
        "created_ids": created_ids,
        "row_results": row_results,
    }


@user_bp.get("")
def get_current_user():
    """Return session state for the current browser."""
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"authenticated": False, "user": None})

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return jsonify({"authenticated": False, "user": None})

    return jsonify({"authenticated": True, "user": user.to_dict()})


@user_bp.get("/settings")
@login_required
def get_user_settings():
    settings = get_or_create_user_settings(g.current_user)
    active_subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()
    current_total = calculate_active_monthly_total(active_subscriptions)

    return jsonify(
        {
            "user": g.current_user.to_dict(),
            "settings": serialize_user_settings(settings),
            "cap_status": build_cap_status(settings, current_total),
        }
    )


@user_bp.patch("/profile")
@login_required
def update_user_profile():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()

    if not username:
        return jsonify({"error": "Username is required."}), 400

    existing_user = User.query.filter(
        func.lower(User.username) == username.lower(),
        User.user_id != g.current_user.user_id,
    ).first()

    if existing_user:
        return jsonify({"error": "Username is already taken."}), 409

    g.current_user.username = username
    db.session.commit()

    return jsonify(
        {
            "message": "Profile updated successfully.",
            "user": g.current_user.to_dict(),
        }
    )


@user_bp.post("/change-password")
@login_required
def change_password():
    data = request.get_json(silent=True) or {}
    current_password = str(data.get("current_password", ""))
    new_password = str(data.get("new_password", ""))

    if not current_password or not new_password:
        return jsonify(
            {"error": "Current password and new password are required."}
        ), 400

    if not check_password_hash(g.current_user.password_hash, current_password):
        return jsonify({"error": "Current password is incorrect."}), 400

    g.current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()

    return jsonify({"message": "Password updated successfully."})


@user_bp.patch("/settings")
@login_required
def update_user_settings():
    data = request.get_json(silent=True) or {}
    errors, cleaned_data = validate_user_settings_payload(data)

    if errors:
        return jsonify({"error": "Validation failed.", "errors": errors}), 400

    settings = get_or_create_user_settings(g.current_user)

    for field_name, value in cleaned_data.items():
        setattr(settings, field_name, value)

    active_subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()
    current_total = calculate_active_monthly_total(active_subscriptions)
    cap_status = build_cap_status(settings, current_total)
    db.session.commit()

    return jsonify(
        {
            "message": "Settings updated successfully.",
            "settings": serialize_user_settings(settings),
            "cap_status": cap_status,
        }
    )


@user_bp.get("/export")
@login_required
def export_user_data():
    subscriptions = (
        Subscription.query.options(
            selectinload(Subscription.category),
            selectinload(Subscription.notification_setting),
        )
        .filter_by(user_id=g.current_user.user_id)
        .order_by(Subscription.subscription_id.asc())
        .all()
    )
    csv_payload = build_csv_payload(subscriptions)
    filename = f"subtrack-subscriptions-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}.csv"

    return Response(
        csv_payload,
        mimetype="text/csv; charset=utf-8",
        headers={
            "Content-Disposition": f'attachment; filename="{filename}"',
        },
    )


@user_bp.post("/import")
@login_required
def import_user_data():
    uploaded_file = request.files.get("file")

    if not uploaded_file:
        return jsonify({"error": "A CSV file is required."}), 400

    rows, import_error = read_import_rows(uploaded_file)

    if import_error:
        return jsonify({"error": import_error}), 400

    if not rows:
        return jsonify({"error": "The CSV file does not contain any data rows."}), 400

    settings = get_or_create_user_settings(g.current_user)
    active_subscriptions = Subscription.query.filter_by(
        user_id=g.current_user.user_id,
        is_active=True,
    ).all()
    current_total = calculate_active_monthly_total(active_subscriptions)
    categories_by_name = get_case_insensitive_category_map()
    existing_subscriptions = (
        Subscription.query.options(
            selectinload(Subscription.category),
            selectinload(Subscription.notification_setting),
        )
        .filter_by(user_id=g.current_user.user_id)
        .all()
    )
    import_started_at = datetime.utcnow()
    existing_fingerprints = set()

    for existing_subscription in existing_subscriptions:
        existing_fingerprints.add(
            build_duplicate_fingerprint(
                {
                    "subscription_name": existing_subscription.subscription_name,
                    "category_name": (
                        existing_subscription.category.category_name
                        if existing_subscription.category
                        else ""
                    ),
                    "amount": quantize_money(existing_subscription.amount),
                    "recurrence_unit": existing_subscription.recurrence_unit,
                    "recurrence_interval": existing_subscription.recurrence_interval,
                    "anchor_date": existing_subscription.anchor_date,
                    "is_active": existing_subscription.is_active,
                    "deleted_at": existing_subscription.deleted_at,
                }
            )
        )

    created_ids = []
    row_results = []

    for row_number, raw_row in enumerate(rows, start=1):
        cleaned_row, row_errors = validate_import_row(raw_row)

        if row_errors:
            row_results.append(
                {
                    "row": row_number,
                    "status": "skipped",
                    "reason": " ".join(row_errors),
                }
            )
            continue

        category = categories_by_name.get(
            cleaned_row["category_name"].strip().lower()
        )

        if not category:
            row_results.append(
                {
                    "row": row_number,
                    "status": "skipped",
                    "reason": "Category does not exist in this environment.",
                }
            )
            continue

        if cleaned_row["is_active"]:
            cleaned_row["deleted_at"] = None
        elif not cleaned_row["deleted_at"]:
            cleaned_row["deleted_at"] = import_started_at

        fingerprint = build_duplicate_fingerprint(cleaned_row)

        if fingerprint in existing_fingerprints:
            row_results.append(
                {
                    "row": row_number,
                    "status": "skipped",
                    "reason": "Duplicate subscription row skipped.",
                }
            )
            continue

        subscription = Subscription(
            user_id=g.current_user.user_id,
            category_id=category.category_id,
            subscription_name=cleaned_row["subscription_name"],
            amount=cleaned_row["amount"],
            recurrence_unit=cleaned_row["recurrence_unit"],
            recurrence_interval=cleaned_row["recurrence_interval"],
            anchor_date=cleaned_row["anchor_date"],
            is_active=cleaned_row["is_active"],
            deleted_at=cleaned_row["deleted_at"],
        )
        subscription.sync_legacy_schedule_fields()

        cap_warning = None
        if subscription.is_active:
            projected_total = (
                current_total + get_subscription_monthly_equivalent(subscription)
            )
            evaluation = evaluate_cap_limit(
                settings,
                current_total,
                projected_total,
            )

            if not evaluation["allowed"]:
                row_results.append(
                    {
                        "row": row_number,
                        "status": "skipped",
                        "reason": evaluation["cap_warning"]["message"],
                    }
                )
                continue

            cap_warning = evaluation["cap_warning"]
            current_total = projected_total

        subscription.notification_setting = NotificationSetting(
            notify_days_before=cleaned_row["notify_days_before"],
            notification_enabled=cleaned_row["notification_enabled"],
        )
        db.session.add(subscription)
        db.session.flush()
        created_ids.append(subscription.subscription_id)
        existing_fingerprints.add(fingerprint)

        row_result = {
            "row": row_number,
            "status": "warning" if cap_warning else "created",
            "reason": (
                cap_warning["message"]
                if cap_warning
                else "Subscription imported successfully."
            ),
        }

        if cap_warning:
            row_result["cap_warning"] = cap_warning

        row_results.append(row_result)

    db.session.commit()

    return jsonify(
        {
            "message": "Import completed.",
            "result": build_import_response(created_ids, row_results),
        }
    )


@user_bp.delete("/account")
@login_required
def delete_user_account():
    user = g.current_user
    session.clear()
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully."})

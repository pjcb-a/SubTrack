"""
User session, settings, account, and data-transfer endpoints.
"""

import csv
import io
from decimal import Decimal, InvalidOperation

from flask import Blueprint, jsonify, request, session, send_file, g
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.subscription import Subscription
from models.user import User
from utils.auth import login_required
from utils.subscription_csv import (
    build_import_duplicate_query,
    build_subscription_csv,
    parse_import_row,
)
from utils.subscription_utils import calculate_monthly_cost
from utils.user_settings import (
    CAP_MODES,
    build_cap_status,
    evaluate_cap_change,
    get_current_monthly_total,
    get_or_create_user_settings,
    quantize_money,
)


user_bp = Blueprint("user", __name__, url_prefix="/api/user")


def get_session_user():
    user_id = session.get("user_id")

    if not user_id:
        return None

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return None

    return user


def build_settings_response(user):
    settings = get_or_create_user_settings(user)
    db.session.flush()

    return {
        "user": user.to_dict(),
        "settings": settings.to_dict(),
        "cap_status": build_cap_status(user),
    }


@user_bp.get("")
def get_current_user():
    user = get_session_user()

    if not user:
        return jsonify({"authenticated": False, "user": None})

    return jsonify({"authenticated": True, "user": user.to_dict()})


@user_bp.get("/settings")
@login_required
def get_user_settings():
    return jsonify(build_settings_response(g.current_user))


@user_bp.patch("/profile")
@login_required
def update_profile():
    data = request.get_json(silent=True) or {}
    username = str(data.get("username", "")).strip()

    if not username:
        return jsonify({"error": "Username is required."}), 400

    existing_user = User.query.filter(
        User.username == username,
        User.user_id != g.current_user.user_id,
    ).first()
    if existing_user:
        return jsonify({"error": "Username is already taken."}), 409

    g.current_user.username = username
    db.session.commit()

    return jsonify({"message": "Profile updated successfully.", "user": g.current_user.to_dict()})


@user_bp.post("/change-password")
@login_required
def change_password():
    data = request.get_json(silent=True) or {}
    current_password = str(data.get("current_password", ""))
    new_password = str(data.get("new_password", ""))

    if not current_password or not new_password:
        return jsonify({"error": "Current password and new password are required."}), 400

    if not check_password_hash(g.current_user.password_hash, current_password):
        return jsonify({"error": "Current password is incorrect."}), 400

    if len(new_password) < 6:
        return jsonify({"error": "New password must be at least 6 characters."}), 400

    g.current_user.password_hash = generate_password_hash(new_password)
    db.session.commit()
    return jsonify({"message": "Password changed successfully."})


@user_bp.patch("/settings")
@login_required
def update_settings():
    data = request.get_json(silent=True) or {}
    settings = get_or_create_user_settings(g.current_user)
    errors = {}

    if "renewal_reminders_enabled" in data:
        settings.renewal_reminders_enabled = bool(data["renewal_reminders_enabled"])

    if "monthly_reports_enabled" in data:
        settings.monthly_reports_enabled = bool(data["monthly_reports_enabled"])

    if "spending_cap_mode" in data:
        mode = str(data.get("spending_cap_mode", "none")).strip().lower()
        if mode not in CAP_MODES:
            errors["spending_cap_mode"] = "Cap mode must be none, soft, or hard."
        else:
            settings.spending_cap_mode = mode

    if "spending_cap_amount" in data:
        raw_amount = data.get("spending_cap_amount")
        if raw_amount in (None, ""):
            settings.spending_cap_amount = None
        else:
            try:
                amount = Decimal(str(raw_amount))
                if amount <= 0:
                    raise InvalidOperation
                settings.spending_cap_amount = quantize_money(amount)
            except (InvalidOperation, ValueError):
                errors["spending_cap_amount"] = "Cap amount must be greater than 0."

    if "soft_cap_overage_percent" in data:
        raw_percent = data.get("soft_cap_overage_percent")
        if raw_percent in (None, ""):
            settings.soft_cap_overage_percent = None
        else:
            try:
                percent = Decimal(str(raw_percent))
                if percent < 0:
                    raise InvalidOperation
                settings.soft_cap_overage_percent = quantize_money(percent)
            except (InvalidOperation, ValueError):
                errors["soft_cap_overage_percent"] = (
                    "Soft cap overage percent must be 0 or greater."
                )

    if errors:
        return jsonify({"errors": errors}), 400

    if settings.spending_cap_mode == "soft" and settings.soft_cap_overage_percent is None:
        settings.soft_cap_overage_percent = Decimal("10.00")

    if settings.spending_cap_mode == "none":
        settings.spending_cap_amount = Decimal("0.00")
        settings.soft_cap_overage_percent = Decimal("0.00")
    elif settings.spending_cap_mode == "hard":
        settings.soft_cap_overage_percent = Decimal("0.00")

    db.session.commit()
    return jsonify(build_settings_response(g.current_user))


@user_bp.get("/export")
@login_required
def export_subscriptions():
    subscriptions = (
        Subscription.query.filter_by(user_id=g.current_user.user_id)
        .order_by(Subscription.subscription_id.asc())
        .all()
    )

    csv_content = build_subscription_csv(subscriptions)
    buffer = io.BytesIO(csv_content.encode("utf-8"))

    return send_file(
        buffer,
        mimetype="text/csv",
        as_attachment=True,
        download_name="subtrack-subscriptions.csv",
    )


@user_bp.post("/import")
@login_required
def import_subscriptions():
    uploaded_file = request.files.get("file")
    if not uploaded_file:
        return jsonify({"error": "Please choose a CSV file to import."}), 400

    try:
        content = uploaded_file.read().decode("utf-8-sig")
    except UnicodeDecodeError:
        return jsonify({"error": "CSV file must be UTF-8 encoded."}), 400

    reader = csv.DictReader(io.StringIO(content))
    row_results = []
    created_ids = []
    created_count = 0
    skipped_count = 0
    warning_count = 0
    current_total = get_current_monthly_total(g.current_user)

    for row_number, row in enumerate(reader, start=1):
        errors, row_data = parse_import_row(row)
        if errors:
            skipped_count += 1
            row_results.append(
                {
                    "row": row_number,
                    "status": "skipped",
                    "reason": "; ".join(errors),
                }
            )
            continue

        if not row_data["is_active"] and row_data["deleted_at"] is None:
            row_data["deleted_at"] = g.current_user.created_at

        duplicate_query = build_import_duplicate_query(g.current_user.user_id, row_data)
        duplicate = duplicate_query.first()

        if duplicate:
            skipped_count += 1
            row_results.append(
                {
                    "row": row_number,
                    "status": "skipped",
                    "reason": "Duplicate subscription skipped.",
                }
            )
            continue

        cap_warning = None
        if row_data["is_active"]:
            projected_total = current_total + Decimal(
                str(calculate_monthly_cost(row_data["amount"], row_data["billing_cycle"]))
            )
            cap_result = evaluate_cap_change(g.current_user, projected_total)

            if cap_result and not cap_result["allowed"]:
                skipped_count += 1
                row_results.append(
                    {
                        "row": row_number,
                        "status": "skipped",
                        "reason": cap_result["message"],
                    }
                )
                continue

            if cap_result and cap_result.get("warning"):
                warning_count += 1
                cap_warning = cap_result["cap_status"]

        subscription = Subscription(
            user_id=g.current_user.user_id,
            category_id=row_data["category"].category_id,
            subscription_name=row_data["subscription_name"],
            amount=row_data["amount"].quantize(Decimal("0.01")),
            billing_cycle=row_data["billing_cycle"],
            start_date=row_data["start_date"],
            due_day=row_data["due_day"],
            is_active=row_data["is_active"],
            deleted_at=row_data["deleted_at"],
        )
        db.session.add(subscription)
        db.session.flush()

        from models.notification_setting import NotificationSetting

        subscription.notification_setting = NotificationSetting(
            subscription_id=subscription.subscription_id,
            notify_days_before=row_data["notify_days_before"],
            notification_enabled=row_data["notification_enabled"],
        )

        db.session.flush()
        created_ids.append(subscription.subscription_id)
        created_count += 1

        if row_data["is_active"]:
            current_total = current_total + Decimal(
                str(calculate_monthly_cost(subscription.amount, subscription.billing_cycle))
            )

        row_results.append(
            {
                "row": row_number,
                "status": "warning" if cap_warning else "created",
                "reason": (
                    cap_warning["warning_message"]
                    if cap_warning and cap_warning.get("warning_message")
                    else "Imported successfully."
                ),
                **({"cap_warning": cap_warning} if cap_warning else {}),
            }
        )

    db.session.commit()

    return jsonify(
        {
            "message": "Import complete.",
            "result": {
                "created_count": created_count,
                "skipped_count": skipped_count,
                "warning_count": warning_count,
                "created_ids": created_ids,
                "row_results": row_results,
            },
        }
    )


@user_bp.delete("/account")
@login_required
def delete_account():
    db.session.delete(g.current_user)
    db.session.commit()
    session.clear()
    return jsonify({"message": "Account deleted successfully."})

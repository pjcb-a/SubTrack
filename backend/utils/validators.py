"""
Validation helpers for incoming API payloads.
"""

import re
from decimal import Decimal, InvalidOperation

from models import db
from models.category import Category
from utils.subscription_utils import (
    ALLOWED_RECURRENCE_UNITS,
    LEGACY_BILLING_CYCLE_MAP,
    parse_date,
)
from utils.user_settings import ALLOWED_SPENDING_CAP_MODES


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    return bool(EMAIL_PATTERN.match(email))


def parse_boolean(value):
    if isinstance(value, bool):
        return value, None

    if isinstance(value, int) and value in (0, 1):
        return bool(value), None

    if isinstance(value, str):
        lowered = value.strip().lower()

        if lowered in {"true", "1", "yes"}:
            return True, None

        if lowered in {"false", "0", "no"}:
            return False, None

    return None, "Must be a boolean value."


def resolve_recurrence_fields(data):
    recurrence_unit = str(data.get("recurrence_unit", "")).strip().lower()

    if not recurrence_unit:
        billing_cycle = str(data.get("billing_cycle", "")).strip().lower()
        recurrence_unit = LEGACY_BILLING_CYCLE_MAP.get(billing_cycle, "")

    recurrence_interval = data.get("recurrence_interval", 1)

    if recurrence_interval in (None, ""):
        recurrence_interval = 1

    anchor_date = data.get("anchor_date")

    if not anchor_date:
        anchor_date = data.get("start_date")

    return recurrence_unit, recurrence_interval, anchor_date


def validate_subscription_payload(data, partial=False):
    """Validate subscription JSON for create and update routes."""
    errors = {}
    cleaned_data = {}

    recurrence_unit, recurrence_interval, anchor_date = resolve_recurrence_fields(data)
    required_fields = [
        "category_id",
        "subscription_name",
        "amount",
        "anchor_date",
    ]

    if not partial:
        for field_name in required_fields:
            if data.get(field_name) in (None, "") and not (
                field_name == "anchor_date" and anchor_date
            ):
                errors[field_name] = "This field is required."

        if not recurrence_unit:
            errors["recurrence_unit"] = "Recurrence unit is required."

    if "category_id" in data:
        try:
            category_id = int(data["category_id"])
        except (TypeError, ValueError):
            errors["category_id"] = "Category ID must be a number."
        else:
            category = db.session.get(Category, category_id)

            if not category:
                errors["category_id"] = "Category not found."
            else:
                cleaned_data["category_id"] = category_id

    if "subscription_name" in data:
        subscription_name = str(data.get("subscription_name", "")).strip()

        if not subscription_name:
            errors["subscription_name"] = "Subscription name cannot be empty."
        else:
            cleaned_data["subscription_name"] = subscription_name

    if "amount" in data:
        try:
            amount = Decimal(str(data["amount"]))
        except (InvalidOperation, ValueError):
            errors["amount"] = "Amount must be a valid number."
        else:
            if amount <= 0:
                errors["amount"] = "Amount must be greater than 0."
            else:
                cleaned_data["amount"] = amount.quantize(Decimal("0.01"))

    if recurrence_unit:
        if recurrence_unit not in ALLOWED_RECURRENCE_UNITS:
            errors["recurrence_unit"] = (
                "Recurrence unit must be day, week, month, or year."
            )
        else:
            cleaned_data["recurrence_unit"] = recurrence_unit

    if recurrence_interval not in (None, ""):
        try:
            recurrence_interval = int(recurrence_interval)
        except (TypeError, ValueError):
            errors["recurrence_interval"] = (
                "Recurrence interval must be a number."
            )
        else:
            if recurrence_interval < 1:
                errors["recurrence_interval"] = (
                    "Recurrence interval must be at least 1."
                )
            else:
                cleaned_data["recurrence_interval"] = recurrence_interval

    if anchor_date:
        parsed_anchor_date = parse_date(anchor_date)

        if not parsed_anchor_date:
            errors["anchor_date"] = "Anchor date must use YYYY-MM-DD format."
        else:
            cleaned_data["anchor_date"] = parsed_anchor_date

    if "is_active" in data:
        is_active, error_message = parse_boolean(data["is_active"])

        if error_message:
            errors["is_active"] = error_message
        else:
            cleaned_data["is_active"] = is_active

    if "notification_setting" in data:
        notification_setting = data["notification_setting"]

        if not isinstance(notification_setting, dict):
            errors["notification_setting"] = "Notification setting must be an object."
        else:
            cleaned_notification_data = {}

            if "notify_days_before" in notification_setting:
                try:
                    notify_days_before = int(
                        notification_setting["notify_days_before"]
                    )
                except (TypeError, ValueError):
                    errors["notify_days_before"] = (
                        "notify_days_before must be a number."
                    )
                else:
                    if notify_days_before < 0:
                        errors["notify_days_before"] = (
                            "notify_days_before cannot be negative."
                        )
                    else:
                        cleaned_notification_data["notify_days_before"] = (
                            notify_days_before
                        )

            if "notification_enabled" in notification_setting:
                notification_enabled, error_message = parse_boolean(
                    notification_setting["notification_enabled"]
                )

                if error_message:
                    errors["notification_enabled"] = error_message
                else:
                    cleaned_notification_data["notification_enabled"] = (
                        notification_enabled
                    )

            cleaned_data["notification_setting"] = cleaned_notification_data

    if errors:
        return errors, {}

    if "anchor_date" in cleaned_data:
        cleaned_data["start_date"] = cleaned_data["anchor_date"]
        cleaned_data["due_day"] = cleaned_data["anchor_date"].day

    if "recurrence_unit" in cleaned_data and "recurrence_interval" not in cleaned_data:
        cleaned_data["recurrence_interval"] = 1

    return errors, cleaned_data


def validate_user_settings_payload(data):
    errors = {}
    cleaned_data = {}

    if "renewal_reminders_enabled" in data:
        renewal_reminders_enabled, error_message = parse_boolean(
            data["renewal_reminders_enabled"]
        )

        if error_message:
            errors["renewal_reminders_enabled"] = error_message
        else:
            cleaned_data["renewal_reminders_enabled"] = renewal_reminders_enabled

    if "monthly_reports_enabled" in data:
        monthly_reports_enabled, error_message = parse_boolean(
            data["monthly_reports_enabled"]
        )

        if error_message:
            errors["monthly_reports_enabled"] = error_message
        else:
            cleaned_data["monthly_reports_enabled"] = monthly_reports_enabled

    if "spending_cap_mode" in data:
        spending_cap_mode = str(data.get("spending_cap_mode", "")).strip().lower()

        if spending_cap_mode not in ALLOWED_SPENDING_CAP_MODES:
            errors["spending_cap_mode"] = (
                "Spending cap mode must be none, soft, or hard."
            )
        else:
            cleaned_data["spending_cap_mode"] = spending_cap_mode

    if "spending_cap_amount" in data:
        try:
            spending_cap_amount = Decimal(str(data["spending_cap_amount"]))
        except (InvalidOperation, ValueError):
            errors["spending_cap_amount"] = "Cap amount must be a valid number."
        else:
            if spending_cap_amount < 0:
                errors["spending_cap_amount"] = "Cap amount cannot be negative."
            else:
                cleaned_data["spending_cap_amount"] = spending_cap_amount.quantize(
                    Decimal("0.01")
                )

    if "soft_cap_overage_percent" in data:
        try:
            soft_cap_overage_percent = Decimal(str(data["soft_cap_overage_percent"]))
        except (InvalidOperation, ValueError):
            errors["soft_cap_overage_percent"] = (
                "Soft cap overage percent must be a valid number."
            )
        else:
            if soft_cap_overage_percent < 0:
                errors["soft_cap_overage_percent"] = (
                    "Soft cap overage percent cannot be negative."
                )
            else:
                cleaned_data["soft_cap_overage_percent"] = (
                    soft_cap_overage_percent.quantize(Decimal("0.01"))
                )

    effective_mode = cleaned_data.get(
        "spending_cap_mode",
        str(data.get("spending_cap_mode", "")).strip().lower() or None,
    )
    effective_cap_amount = cleaned_data.get("spending_cap_amount")
    if effective_cap_amount is None and "spending_cap_amount" in data:
        try:
            effective_cap_amount = Decimal(str(data["spending_cap_amount"]))
        except (InvalidOperation, ValueError):
            effective_cap_amount = None

    if effective_mode in {"soft", "hard"}:
        if effective_cap_amount is None:
            errors["spending_cap_amount"] = (
                "Cap amount is required when a cap mode is enabled."
            )
        elif effective_cap_amount <= 0:
            errors["spending_cap_amount"] = (
                "Cap amount must be greater than 0 when enabled."
            )

        if effective_mode == "soft":
            effective_soft_percent = cleaned_data.get("soft_cap_overage_percent")
            if effective_soft_percent is None and "soft_cap_overage_percent" in data:
                try:
                    effective_soft_percent = Decimal(
                        str(data["soft_cap_overage_percent"])
                    )
                except (InvalidOperation, ValueError):
                    effective_soft_percent = None

            if effective_soft_percent is None:
                errors["soft_cap_overage_percent"] = (
                    "Soft cap overage percent is required for soft cap mode."
                )

    return errors, cleaned_data

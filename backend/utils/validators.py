"""
Validation helpers for incoming API payloads.

These functions protect the database layer by normalizing and validating JSON
before route handlers create or update rows.
"""

import re
from decimal import Decimal, InvalidOperation

from models import db
from models.category import Category
from utils.subscription_utils import (
    ALLOWED_BILLING_CYCLES,
    ALLOWED_RECURRENCE_UNITS,
    parse_date,
)


EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


def is_valid_email(email):
    """Simple format check used by the registration endpoint."""
    return bool(EMAIL_PATTERN.match(email))


def parse_boolean(value):
    """Normalize common boolean-like inputs from JSON into Python booleans."""
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


def validate_subscription_payload(data, partial=False):
    """Validate subscription JSON for create and update routes.

    Route usage:
    - `POST /api/subscriptions` calls this with `partial=False`
    - `PUT /api/subscriptions/<id>` calls this with `partial=True`

    Frontend effect:
    The returned `errors` object is designed to map cleanly back to form fields
    when the dashboard is switched from mock state to real API requests.
    """
    errors = {}
    cleaned_data = {}
    required_fields = [
        "category_id",
        "subscription_name",
        "amount",
        "start_date",
    ]

    if not partial:
        for field_name in required_fields:
            if data.get(field_name) in (None, ""):
                errors[field_name] = "This field is required."

    recurrence_unit = None
    recurrence_interval = None

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

    if "billing_cycle" in data:
        billing_cycle = str(data.get("billing_cycle", "")).strip().lower()

        if billing_cycle not in ALLOWED_BILLING_CYCLES:
            errors["billing_cycle"] = (
                "Billing cycle must be daily, weekly, monthly, annual, or custom."
            )
        else:
            cleaned_data["billing_cycle"] = billing_cycle

    if "recurrence_unit" in data:
        recurrence_unit = str(data.get("recurrence_unit", "")).strip().lower()

        if recurrence_unit not in ALLOWED_RECURRENCE_UNITS:
            errors["recurrence_unit"] = "Recurrence unit must be day, week, month, or year."
        else:
            cleaned_data["recurrence_unit"] = recurrence_unit

    if "recurrence_interval" in data:
        try:
            recurrence_interval = int(data["recurrence_interval"])
        except (TypeError, ValueError):
            errors["recurrence_interval"] = "Recurrence interval must be a number."
        else:
            if recurrence_interval < 1:
                errors["recurrence_interval"] = "Recurrence interval must be at least 1."
            else:
                cleaned_data["recurrence_interval"] = recurrence_interval

    if "start_date" in data:
        start_date = parse_date(data.get("start_date"))

        if not start_date:
            errors["start_date"] = "Start date must use YYYY-MM-DD format."
        else:
            cleaned_data["start_date"] = start_date

    if "due_day" in data:
        try:
            due_day = int(data["due_day"])
        except (TypeError, ValueError):
            errors["due_day"] = "Due day must be a number."
        else:
            if due_day < 1 or due_day > 31:
                errors["due_day"] = "Due day must be between 1 and 31."
            else:
                cleaned_data["due_day"] = due_day
    elif "start_date" in cleaned_data:
        cleaned_data["due_day"] = cleaned_data["start_date"].day

    if "recurrence_end_mode" in data:
        recurrence_end_mode = str(data.get("recurrence_end_mode", "")).strip().lower()
        if recurrence_end_mode not in {"forever", "until"}:
            errors["recurrence_end_mode"] = "Recurrence end mode must be forever or until."
        else:
            cleaned_data["recurrence_end_mode"] = recurrence_end_mode

    if "recurrence_end_date" in data:
        raw_end_date = data.get("recurrence_end_date")
        if raw_end_date in (None, ""):
            cleaned_data["recurrence_end_date"] = None
        else:
            recurrence_end_date = parse_date(raw_end_date)
            if not recurrence_end_date:
                errors["recurrence_end_date"] = "Recurrence end date must use YYYY-MM-DD format."
            else:
                cleaned_data["recurrence_end_date"] = recurrence_end_date

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

    if not partial:
        billing_cycle = cleaned_data.get("billing_cycle")
        if billing_cycle in (None, ""):
            errors["billing_cycle"] = "This field is required."

        if billing_cycle == "custom":
            if "recurrence_unit" not in cleaned_data:
                errors["recurrence_unit"] = "Recurrence unit is required for custom schedules."
            if "recurrence_interval" not in cleaned_data:
                errors["recurrence_interval"] = "Recurrence interval is required for custom schedules."

    billing_cycle = cleaned_data.get("billing_cycle", data.get("billing_cycle"))
    if billing_cycle and billing_cycle != "custom":
        preset_unit_map = {
            "daily": "day",
            "weekly": "week",
            "monthly": "month",
            "annual": "year",
        }
        cleaned_data["recurrence_unit"] = preset_unit_map.get(str(billing_cycle).lower(), "month")
        cleaned_data["recurrence_interval"] = 1

    if cleaned_data.get("recurrence_end_mode") == "until":
        if cleaned_data.get("recurrence_end_date") is None:
            errors["recurrence_end_date"] = "Recurrence end date is required when using an until date."
        elif cleaned_data.get("start_date") and cleaned_data["recurrence_end_date"] < cleaned_data["start_date"]:
            errors["recurrence_end_date"] = "Recurrence end date cannot be earlier than start date."

    if cleaned_data.get("recurrence_end_mode") != "until" and "recurrence_end_mode" in cleaned_data:
        cleaned_data["recurrence_end_date"] = None

    return errors, cleaned_data

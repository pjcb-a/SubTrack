import csv
from decimal import Decimal, InvalidOperation
from io import StringIO, TextIOWrapper

from utils.subscription_utils import parse_date, parse_datetime, quantize_money


CSV_COLUMNS = [
    "subscription_name",
    "category_name",
    "amount",
    "recurrence_unit",
    "recurrence_interval",
    "anchor_date",
    "is_active",
    "deleted_at",
    "notify_days_before",
    "notification_enabled",
]


def build_csv_payload(subscriptions):
    """Serialize subscriptions into a UTF-8 CSV string."""
    output = StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
    writer.writeheader()

    for subscription in subscriptions:
        writer.writerow(
            {
                "subscription_name": subscription.subscription_name,
                "category_name": (
                    subscription.category.category_name if subscription.category else ""
                ),
                "amount": f"{float(subscription.amount):.2f}",
                "recurrence_unit": subscription.recurrence_unit,
                "recurrence_interval": subscription.recurrence_interval,
                "anchor_date": (
                    subscription.anchor_date.isoformat()
                    if subscription.anchor_date
                    else ""
                ),
                "is_active": "true" if subscription.is_active else "false",
                "deleted_at": (
                    subscription.deleted_at.isoformat()
                    if subscription.deleted_at
                    else ""
                ),
                "notify_days_before": (
                    subscription.notification_setting.notify_days_before
                    if subscription.notification_setting
                    else 3
                ),
                "notification_enabled": (
                    "true"
                    if (
                        subscription.notification_setting
                        and subscription.notification_setting.notification_enabled
                    )
                    else "false"
                ),
            }
        )

    return output.getvalue()


def read_import_rows(file_storage):
    """Parse an uploaded CSV file into row dictionaries."""
    text_wrapper = TextIOWrapper(
        file_storage.stream,
        encoding="utf-8",
        newline="",
    )

    try:
        reader = csv.DictReader(text_wrapper)

        if reader.fieldnames != CSV_COLUMNS:
            return None, (
                "CSV header does not match the expected export format."
            )

        return list(reader), None
    finally:
        text_wrapper.detach()
        file_storage.stream.seek(0)


def normalize_boolean(value):
    if isinstance(value, bool):
        return value, None

    lowered_value = str(value or "").strip().lower()

    if lowered_value in {"true", "1", "yes"}:
        return True, None

    if lowered_value in {"false", "0", "no"}:
        return False, None

    return None, "Must be true or false."


def validate_import_row(row):
    """Validate one import row against the supported CSV schema."""
    cleaned_row = {}
    errors = []

    subscription_name = str(row.get("subscription_name", "")).strip()

    if not subscription_name:
        errors.append("subscription_name is required.")
    else:
        cleaned_row["subscription_name"] = subscription_name

    category_name = str(row.get("category_name", "")).strip()

    if not category_name:
        errors.append("category_name is required.")
    else:
        cleaned_row["category_name"] = category_name

    try:
        amount = quantize_money(Decimal(str(row.get("amount", ""))))
    except (InvalidOperation, ValueError):
        errors.append("amount must be a valid number.")
    else:
        if amount <= 0:
            errors.append("amount must be greater than 0.")
        else:
            cleaned_row["amount"] = amount

    recurrence_unit = str(row.get("recurrence_unit", "")).strip().lower()

    if recurrence_unit not in {"day", "week", "month", "year"}:
        errors.append("recurrence_unit must be day, week, month, or year.")
    else:
        cleaned_row["recurrence_unit"] = recurrence_unit

    try:
        recurrence_interval = int(row.get("recurrence_interval", ""))
    except (TypeError, ValueError):
        errors.append("recurrence_interval must be a valid number.")
    else:
        if recurrence_interval < 1:
            errors.append("recurrence_interval must be at least 1.")
        else:
            cleaned_row["recurrence_interval"] = recurrence_interval

    anchor_date = parse_date(row.get("anchor_date"))

    if not anchor_date:
        errors.append("anchor_date must use YYYY-MM-DD format.")
    else:
        cleaned_row["anchor_date"] = anchor_date

    is_active, active_error = normalize_boolean(row.get("is_active"))

    if active_error:
        errors.append("is_active must be true or false.")
    else:
        cleaned_row["is_active"] = is_active

    deleted_at = parse_datetime(row.get("deleted_at"))
    if row.get("deleted_at") and not deleted_at:
        errors.append("deleted_at must be a valid ISO datetime when provided.")
    else:
        cleaned_row["deleted_at"] = deleted_at

    try:
        notify_days_before = int(row.get("notify_days_before", ""))
    except (TypeError, ValueError):
        errors.append("notify_days_before must be a valid number.")
    else:
        if notify_days_before < 0:
            errors.append("notify_days_before cannot be negative.")
        else:
            cleaned_row["notify_days_before"] = notify_days_before

    notification_enabled, notification_error = normalize_boolean(
        row.get("notification_enabled")
    )
    if notification_error:
        errors.append("notification_enabled must be true or false.")
    else:
        cleaned_row["notification_enabled"] = notification_enabled

    return cleaned_row, errors


def build_duplicate_fingerprint(row_data):
    normalized_deleted_at = row_data.get("deleted_at")

    if normalized_deleted_at:
        normalized_deleted_at = normalized_deleted_at.isoformat()
    else:
        normalized_deleted_at = ""

    return (
        row_data["subscription_name"].strip().lower(),
        row_data["category_name"].strip().lower(),
        f"{row_data['amount']:.2f}",
        row_data["recurrence_unit"],
        int(row_data["recurrence_interval"]),
        row_data["anchor_date"].isoformat(),
        bool(row_data["is_active"]),
        normalized_deleted_at,
    )

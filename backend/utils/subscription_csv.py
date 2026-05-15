import csv
import io
from datetime import datetime
from decimal import Decimal, InvalidOperation

from models.category import Category
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from utils.subscription_utils import ALLOWED_BILLING_CYCLES, parse_date


CSV_COLUMNS = [
    "subscription_name",
    "category_name",
    "amount",
    "billing_cycle",
    "start_date",
    "due_day",
    "is_active",
    "deleted_at",
    "notify_days_before",
    "notification_enabled",
]


def build_subscription_csv(subscriptions):
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=CSV_COLUMNS)
    writer.writeheader()

    for subscription in subscriptions:
        writer.writerow(
            {
                "subscription_name": subscription.subscription_name,
                "category_name": (
                    subscription.category.category_name
                    if subscription.category
                    else ""
                ),
                "amount": float(subscription.amount),
                "billing_cycle": subscription.billing_cycle,
                "start_date": subscription.start_date.isoformat(),
                "due_day": subscription.due_day,
                "is_active": str(subscription.is_active).lower(),
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
                "notification_enabled": str(
                    subscription.notification_setting.notification_enabled
                    if subscription.notification_setting
                    else True
                ).lower(),
            }
        )

    return output.getvalue()


def normalize_bool(value, default=False):
    if value is None or value == "":
        return default

    lowered = str(value).strip().lower()
    if lowered in {"true", "1", "yes"}:
        return True
    if lowered in {"false", "0", "no"}:
        return False
    raise ValueError("Must be a boolean value.")


def parse_import_row(row):
    errors = []
    subscription_name = str(row.get("subscription_name", "")).strip()
    category_name = str(row.get("category_name", "")).strip()
    amount_raw = str(row.get("amount", "")).strip()
    billing_cycle = str(row.get("billing_cycle", "")).strip().lower()
    start_date = parse_date(row.get("start_date"))
    deleted_at_raw = str(row.get("deleted_at", "")).strip()

    if not subscription_name:
        errors.append("subscription_name is required")

    if not category_name:
        errors.append("category_name is required")

    category = None
    if category_name:
        category = Category.query.filter(
            Category.category_name.ilike(category_name)
        ).first()
        if not category:
            errors.append("category_name not found")

    try:
        amount = Decimal(amount_raw)
        if amount <= 0:
            raise ValueError
    except (InvalidOperation, ValueError):
        errors.append("amount must be greater than 0")
        amount = None

    if billing_cycle not in ALLOWED_BILLING_CYCLES:
        errors.append("billing_cycle must be weekly, monthly, or annual")

    if not start_date:
        errors.append("start_date must use YYYY-MM-DD format")

    try:
        due_day = int(row.get("due_day", ""))
        if due_day < 1 or due_day > 31:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("due_day must be between 1 and 31")
        due_day = None

    try:
        is_active = normalize_bool(row.get("is_active"), default=True)
    except ValueError:
        errors.append("is_active must be a boolean value")
        is_active = True

    try:
        notify_days_before = int(row.get("notify_days_before", 3))
        if notify_days_before < 0:
            raise ValueError
    except (TypeError, ValueError):
        errors.append("notify_days_before must be 0 or greater")
        notify_days_before = 3

    try:
        notification_enabled = normalize_bool(
            row.get("notification_enabled"),
            default=True,
        )
    except ValueError:
        errors.append("notification_enabled must be a boolean value")
        notification_enabled = True

    deleted_at = None
    if deleted_at_raw:
        try:
            deleted_at = datetime.fromisoformat(deleted_at_raw)
        except ValueError:
            errors.append("deleted_at must use ISO datetime format")

    return errors, {
        "subscription_name": subscription_name,
        "category": category,
        "amount": amount,
        "billing_cycle": billing_cycle,
        "start_date": start_date,
        "due_day": due_day,
        "is_active": is_active,
        "deleted_at": deleted_at,
        "notify_days_before": notify_days_before,
        "notification_enabled": notification_enabled,
    }


def build_import_duplicate_query(user_id, row_data):
    return Subscription.query.filter_by(
        user_id=user_id,
        category_id=row_data["category"].category_id,
        subscription_name=row_data["subscription_name"],
        amount=row_data["amount"].quantize(Decimal("0.01")),
        billing_cycle=row_data["billing_cycle"],
        start_date=row_data["start_date"],
        due_day=row_data["due_day"],
        is_active=row_data["is_active"],
    )


def attach_notification_setting(subscription, notify_days_before, notification_enabled):
    subscription.notification_setting = NotificationSetting(
        notify_days_before=notify_days_before,
        notification_enabled=notification_enabled,
    )

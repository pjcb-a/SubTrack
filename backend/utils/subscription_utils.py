"""
Helpers for recurrence math, monthly-equivalent spend, and cap evaluation.
"""

from calendar import monthrange
from datetime import date, datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP


ALLOWED_RECURRENCE_UNITS = {"day", "week", "month", "year"}
LEGACY_BILLING_CYCLE_MAP = {
    "daily": "day",
    "weekly": "week",
    "monthly": "month",
    "annual": "year",
    "yearly": "year",
}
LEGACY_UNIT_LABELS = {
    "day": "daily",
    "week": "weekly",
    "month": "monthly",
    "year": "annual",
}
MONEY_PRECISION = Decimal("0.01")
YEAR_DAYS = Decimal("365.25")
MONTHS_PER_YEAR = Decimal("12")
WEEK_DAYS = Decimal("7")


def parse_date(date_string):
    """Parse the YYYY-MM-DD format used by JSON payloads from the frontend."""
    if isinstance(date_string, date):
        return date_string

    try:
        return datetime.strptime(str(date_string), "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def parse_datetime(datetime_string):
    """Parse ISO-like datetimes used by import/export endpoints."""
    if not datetime_string:
        return None

    if isinstance(datetime_string, datetime):
        return datetime_string

    normalized_value = str(datetime_string).strip().replace("Z", "+00:00")

    try:
        return datetime.fromisoformat(normalized_value)
    except ValueError:
        return None


def quantize_money(value):
    return Decimal(value).quantize(MONEY_PRECISION, rounding=ROUND_HALF_UP)


def normalize_decimal(value, default="0"):
    if value in (None, ""):
        return Decimal(default)

    return Decimal(str(value))


def build_due_date(year, month, due_day):
    """Clamp the due day to the last valid day of the target month."""
    last_day_of_month = monthrange(year, month)[1]
    safe_due_day = min(due_day, last_day_of_month)
    return date(year, month, safe_due_day)


def add_months(current_date, months_to_add, due_day):
    """Advance a date by a month interval while honoring an anchor day."""
    month_index = current_date.month - 1 + months_to_add
    new_year = current_date.year + month_index // 12
    new_month = month_index % 12 + 1
    return build_due_date(new_year, new_month, due_day)


def shift_occurrence(anchor_date, recurrence_unit, interval_multiplier):
    """Return the occurrence that is N intervals away from the anchor date."""
    if recurrence_unit == "day":
        return anchor_date + timedelta(days=interval_multiplier)

    if recurrence_unit == "week":
        return anchor_date + timedelta(days=interval_multiplier * 7)

    if recurrence_unit == "month":
        return add_months(anchor_date, interval_multiplier, anchor_date.day)

    return add_months(anchor_date, interval_multiplier * 12, anchor_date.day)


def advance_occurrence(current_date, recurrence_unit, recurrence_interval, anchor_date):
    """Move a generated occurrence to the next recurrence slot."""
    if recurrence_unit == "day":
        return current_date + timedelta(days=recurrence_interval)

    if recurrence_unit == "week":
        return current_date + timedelta(days=recurrence_interval * 7)

    if recurrence_unit == "month":
        return add_months(current_date, recurrence_interval, anchor_date.day)

    return add_months(current_date, recurrence_interval * 12, anchor_date.day)


def get_subscription_recurrence_unit(subscription):
    """Return the canonical recurrence unit for a subscription record."""
    if getattr(subscription, "recurrence_unit", None) in ALLOWED_RECURRENCE_UNITS:
        return subscription.recurrence_unit

    return LEGACY_BILLING_CYCLE_MAP.get(
        getattr(subscription, "billing_cycle", ""),
        "month",
    )


def get_subscription_recurrence_interval(subscription):
    """Return the canonical recurrence interval for a subscription record."""
    recurrence_interval = getattr(subscription, "recurrence_interval", None)

    if isinstance(recurrence_interval, int) and recurrence_interval >= 1:
        return recurrence_interval

    return 1


def get_subscription_anchor_date(subscription):
    """Return the anchor date used to build recurring occurrences."""
    if getattr(subscription, "anchor_date", None):
        return subscription.anchor_date

    return getattr(subscription, "start_date", None)


def get_legacy_billing_cycle(recurrence_unit, recurrence_interval):
    """Return a legacy billing-cycle string for transitional compatibility."""
    if recurrence_interval == 1:
        return LEGACY_UNIT_LABELS.get(recurrence_unit, "custom")

    return "custom"


def get_occurrences_in_range(subscription, start_date, end_date):
    """Generate every active occurrence for a subscription in a date window."""
    if not subscription.is_active:
        return []

    anchor_date = get_subscription_anchor_date(subscription)

    if not anchor_date:
        return []

    recurrence_unit = get_subscription_recurrence_unit(subscription)
    recurrence_interval = get_subscription_recurrence_interval(subscription)
    current_date = anchor_date

    if recurrence_unit == "day":
        step_days = recurrence_interval
        if current_date < start_date:
            days_diff = (start_date - current_date).days
            skipped_steps = days_diff // step_days
            current_date = current_date + timedelta(days=skipped_steps * step_days)
            while current_date < start_date:
                current_date = current_date + timedelta(days=step_days)
    elif recurrence_unit == "week":
        step_days = recurrence_interval * 7
        if current_date < start_date:
            days_diff = (start_date - current_date).days
            skipped_steps = days_diff // step_days
            current_date = current_date + timedelta(days=skipped_steps * step_days)
            while current_date < start_date:
                current_date = current_date + timedelta(days=step_days)
    else:
        while current_date < start_date:
            current_date = advance_occurrence(
                current_date,
                recurrence_unit,
                recurrence_interval,
                anchor_date,
            )

    occurrences = []

    while current_date <= end_date:
        if current_date >= start_date:
            occurrences.append(current_date)

        current_date = advance_occurrence(
            current_date,
            recurrence_unit,
            recurrence_interval,
            anchor_date,
        )

    return occurrences


def get_next_due_date(subscription, today=None):
    """Compute the next upcoming occurrence for one subscription record."""
    if not subscription.is_active:
        return None

    anchor_date = get_subscription_anchor_date(subscription)

    if not anchor_date:
        return None

    today = today or date.today()
    occurrences = get_occurrences_in_range(subscription, today, today + timedelta(days=366))
    return occurrences[0] if occurrences else None


def calculate_monthly_equivalent(amount, recurrence_unit, recurrence_interval):
    """Normalize a recurring amount into its monthly-equivalent cost."""
    amount_decimal = quantize_money(normalize_decimal(amount))
    interval_decimal = Decimal(recurrence_interval or 1)

    if recurrence_unit == "day":
        monthly_amount = amount_decimal * (YEAR_DAYS / MONTHS_PER_YEAR) / interval_decimal
    elif recurrence_unit == "week":
        monthly_amount = amount_decimal * (YEAR_DAYS / WEEK_DAYS / MONTHS_PER_YEAR) / interval_decimal
    elif recurrence_unit == "month":
        monthly_amount = amount_decimal / interval_decimal
    else:
        monthly_amount = amount_decimal / (MONTHS_PER_YEAR * interval_decimal)

    return quantize_money(monthly_amount)


def calculate_monthly_cost(amount, recurrence_unit=None, recurrence_interval=1, billing_cycle=None):
    """Backward-compatible wrapper for monthly-equivalent cost."""
    effective_unit = recurrence_unit

    if not effective_unit and billing_cycle:
        effective_unit = LEGACY_BILLING_CYCLE_MAP.get(str(billing_cycle).lower(), "month")

    return float(
        calculate_monthly_equivalent(
            amount,
            effective_unit or "month",
            recurrence_interval or 1,
        )
    )


def get_subscription_monthly_equivalent(subscription):
    return calculate_monthly_equivalent(
        subscription.amount,
        get_subscription_recurrence_unit(subscription),
        get_subscription_recurrence_interval(subscription),
    )


def calculate_active_monthly_total(subscriptions, exclude_subscription_id=None):
    total = Decimal("0")

    for subscription in subscriptions:
        if not subscription.is_active:
            continue

        if (
            exclude_subscription_id is not None
            and subscription.subscription_id == exclude_subscription_id
        ):
            continue

        total += get_subscription_monthly_equivalent(subscription)

    return quantize_money(total)

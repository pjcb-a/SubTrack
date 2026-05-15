"""
Helpers for date and billing-cycle calculations.

These functions keep subscription math in one place so route files can stay
focused on request/response flow instead of calendar logic.
"""

from calendar import monthrange
from datetime import date, datetime, timedelta


ALLOWED_BILLING_CYCLES = {"daily", "weekly", "monthly", "annual", "custom"}
ALLOWED_RECURRENCE_UNITS = {"day", "week", "month", "year"}


def parse_date(date_string):
    """Parse the YYYY-MM-DD format used by JSON payloads from the frontend."""
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


def build_due_date(year, month, due_day):
    """Clamp the due day to the last valid day of the target month."""
    last_day_of_month = monthrange(year, month)[1]
    safe_due_day = min(due_day, last_day_of_month)
    return date(year, month, safe_due_day)


def add_months(current_date, months_to_add, due_day):
    """Advance a due date by the billing interval while keeping a valid day."""
    month_index = current_date.month - 1 + months_to_add
    new_year = current_date.year + month_index // 12
    new_month = month_index % 12 + 1
    return build_due_date(new_year, new_month, due_day)


def add_years(current_date, years_to_add, due_day):
    """Advance a date by whole years while clamping the day-of-month."""
    new_year = current_date.year + years_to_add
    return build_due_date(new_year, current_date.month, due_day)


def get_first_due_date(start_date, due_day, cycle_months):
    """Find the first bill date that should count for a subscription."""
    first_due_date = build_due_date(start_date.year, start_date.month, due_day)

    if first_due_date < start_date:
        first_due_date = add_months(first_due_date, cycle_months, due_day)

    return first_due_date


def get_next_due_date(subscription, today=None):
    """Compute the next upcoming due date for one subscription record.

    Route usage:
    `GET /api/subscriptions/upcoming` uses this to build the dashboard-ready
    upcoming list.
    """
    if not subscription.is_active:
        return None

    today = today or date.today()
    recurrence_unit = getattr(subscription, "recurrence_unit", None)
    recurrence_interval = getattr(subscription, "recurrence_interval", None) or 1

    if not recurrence_unit:
        if subscription.billing_cycle == "weekly":
            recurrence_unit = "week"
        elif subscription.billing_cycle == "annual":
            recurrence_unit = "year"
        elif subscription.billing_cycle == "daily":
            recurrence_unit = "day"
        else:
            recurrence_unit = "month"

    next_due_date = subscription.start_date

    while next_due_date < today:
        next_due_date = advance_occurrence(
            next_due_date,
            recurrence_unit,
            recurrence_interval,
            subscription.due_day,
        )

    recurrence_end_date = getattr(subscription, "recurrence_end_date", None)
    if recurrence_end_date and next_due_date > recurrence_end_date:
        return None

    return next_due_date


def calculate_monthly_cost(amount, billing_cycle):
    """Normalize a subscription price into a monthly-equivalent amount.

    Route usage:
    `GET /api/subscriptions/summary` uses this to build the dashboard total.
    """
    if billing_cycle == "weekly":
        return round(float(amount) * 52 / 12, 2)

    if billing_cycle == "annual":
        return round(float(amount) / 12, 2)

    return round(float(amount), 2)


def calculate_monthly_cost_from_recurrence(amount, recurrence_unit, recurrence_interval):
    """Normalize any supported recurrence schedule into a monthly amount."""
    normalized_amount = float(amount)
    normalized_interval = max(int(recurrence_interval or 1), 1)

    if recurrence_unit == "day":
        return round(normalized_amount * (365.25 / 12) / normalized_interval, 2)

    if recurrence_unit == "week":
        return round(normalized_amount * (365.25 / 7 / 12) / normalized_interval, 2)

    if recurrence_unit == "year":
        return round(normalized_amount / (12 * normalized_interval), 2)

    return round(normalized_amount / normalized_interval, 2)


def advance_occurrence(current_date, recurrence_unit, recurrence_interval, due_day):
    """Advance one occurrence according to the recurrence rule."""
    normalized_interval = max(int(recurrence_interval or 1), 1)

    if recurrence_unit == "day":
        return current_date + timedelta(days=normalized_interval)

    if recurrence_unit == "week":
        return current_date + timedelta(days=7 * normalized_interval)

    if recurrence_unit == "year":
        return add_years(current_date, normalized_interval, due_day)

    return add_months(current_date, normalized_interval, due_day)


def iter_occurrences_in_range(subscription, range_start, range_end):
    """Yield every scheduled occurrence in the requested date window."""
    if not subscription.is_active:
        return []

    occurrences = []
    recurrence_unit = getattr(subscription, "recurrence_unit", None)
    recurrence_interval = getattr(subscription, "recurrence_interval", None) or 1
    recurrence_end_date = getattr(subscription, "recurrence_end_date", None)

    if not recurrence_unit:
        if subscription.billing_cycle == "weekly":
            recurrence_unit = "week"
        elif subscription.billing_cycle == "annual":
            recurrence_unit = "year"
        elif subscription.billing_cycle == "daily":
            recurrence_unit = "day"
        else:
            recurrence_unit = "month"

    next_due_date = subscription.start_date

    guard = 0
    while next_due_date < range_start and guard < 500:
        next_due_date = advance_occurrence(
            next_due_date,
            recurrence_unit,
            recurrence_interval,
            subscription.due_day,
        )
        guard += 1

    while next_due_date <= range_end and guard < 1000:
        if recurrence_end_date and next_due_date > recurrence_end_date:
            break
        occurrences.append(next_due_date)
        next_due_date = advance_occurrence(
            next_due_date,
            recurrence_unit,
            recurrence_interval,
            subscription.due_day,
        )
        guard += 1

    return occurrences

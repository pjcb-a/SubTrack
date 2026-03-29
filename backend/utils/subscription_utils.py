"""
Helpers for date and billing-cycle calculations.

These functions keep subscription math in one place so route files can stay
focused on request/response flow instead of calendar logic.
"""

from calendar import monthrange
from datetime import date, datetime, timedelta


ALLOWED_BILLING_CYCLES = {"weekly", "monthly", "annual"}


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
    if subscription.billing_cycle == "weekly":
        next_due_date = subscription.start_date

        while next_due_date < today:
            next_due_date = next_due_date + timedelta(days=7)

        return next_due_date

    cycle_months = 12 if subscription.billing_cycle == "annual" else 1
    next_due_date = get_first_due_date(subscription.start_date, subscription.due_day, cycle_months)

    while next_due_date < today:
        next_due_date = add_months(next_due_date, cycle_months, subscription.due_day)

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

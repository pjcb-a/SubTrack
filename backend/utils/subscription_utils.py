from calendar import monthrange
from datetime import date, datetime


ALLOWED_BILLING_CYCLES = {
    "monthly": 1,
    "quarterly": 3,
    "yearly": 12,
}


# FOR TURNING A DATE STRING INTO A PYTHON DATE
def parse_date(date_string):
    try:
        return datetime.strptime(date_string, "%Y-%m-%d").date()
    except (TypeError, ValueError):
        return None


# FOR BUILDING A SAFE DUE DATE INSIDE A VALID CALENDAR MONTH
def build_due_date(year, month, due_day):
    last_day_of_month = monthrange(year, month)[1]
    safe_due_day = min(due_day, last_day_of_month)
    return date(year, month, safe_due_day)


# FOR MOVING A DUE DATE FORWARD BY A NUMBER OF MONTHS
def add_months(current_date, months_to_add, due_day):
    month_index = current_date.month - 1 + months_to_add
    new_year = current_date.year + month_index // 12
    new_month = month_index % 12 + 1
    return build_due_date(new_year, new_month, due_day)


# FOR FINDING THE FIRST VALID DUE DATE AFTER THE START DATE
def get_first_due_date(start_date, due_day, cycle_months):
    first_due_date = build_due_date(start_date.year, start_date.month, due_day)

    if first_due_date < start_date:
        first_due_date = add_months(first_due_date, cycle_months, due_day)

    return first_due_date


# FOR CALCULATING THE NEXT UPCOMING DUE DATE OF A SUBSCRIPTION
def get_next_due_date(subscription, today=None):
    if not subscription.is_active:
        return None

    today = today or date.today()
    cycle_months = ALLOWED_BILLING_CYCLES[subscription.billing_cycle]
    next_due_date = get_first_due_date(
        subscription.start_date,
        subscription.due_day,
        cycle_months,
    )

    while next_due_date < today:
        next_due_date = add_months(
            next_due_date,
            cycle_months,
            subscription.due_day,
        )

    return next_due_date


# FOR CONVERTING ANY BILLING CYCLE INTO A MONTHLY COST
def calculate_monthly_cost(amount, billing_cycle):
    cycle_months = ALLOWED_BILLING_CYCLES[billing_cycle]
    return round(float(amount) / cycle_months, 2)

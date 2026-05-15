"""
Lightweight schema repair helpers for environments without formal migrations.
"""

from sqlalchemy import inspect, text

from models import db


SUBSCRIPTION_RECURRING_DEFAULTS_SQL = """
UPDATE subscriptions
SET
    recurrence_unit = CASE
        WHEN billing_cycle = 'weekly' THEN 'week'
        WHEN billing_cycle = 'annual' THEN 'year'
        ELSE 'month'
    END,
    recurrence_interval = COALESCE(recurrence_interval, 1),
    anchor_date = COALESCE(anchor_date, start_date)
WHERE recurrence_unit IS NULL
   OR recurrence_interval IS NULL
   OR anchor_date IS NULL
"""


def ensure_column(table_name, column_name, column_definition):
    inspector = inspect(db.engine)

    if table_name not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns(table_name)
    }

    if column_name in existing_columns:
        return

    db.session.execute(
        text(
            f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_definition}"
        )
    )
    db.session.commit()


def ensure_subscription_deleted_at_column():
    ensure_column("subscriptions", "deleted_at", "TIMESTAMP NULL")


def ensure_subscription_recurrence_columns():
    ensure_column("subscriptions", "recurrence_unit", "VARCHAR(16) NULL")
    ensure_column("subscriptions", "recurrence_interval", "INTEGER NULL")
    ensure_column("subscriptions", "anchor_date", "DATE NULL")


def backfill_subscription_recurrence_columns():
    inspector = inspect(db.engine)

    if "subscriptions" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns("subscriptions")
    }

    if not {"recurrence_unit", "recurrence_interval", "anchor_date"}.issubset(
        existing_columns
    ):
        return

    db.session.execute(text(SUBSCRIPTION_RECURRING_DEFAULTS_SQL))
    db.session.commit()


def sync_schema():
    ensure_subscription_deleted_at_column()
    ensure_subscription_recurrence_columns()
    backfill_subscription_recurrence_columns()

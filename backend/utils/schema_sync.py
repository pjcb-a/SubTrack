"""
Lightweight schema repair helpers for environments without formal migrations.

The current project still uses `db.create_all()` during startup, which creates
missing tables but does not add new columns to existing tables. These helpers
patch the small schema differences needed by newer backend features when an old
local database is reused.
"""

from sqlalchemy import inspect, text

from models import db


def ensure_subscription_deleted_at_column():
    """Add `subscriptions.deleted_at` when older local databases do not have it.

    Frontend impact:
    The history page relies on this timestamp to persist deleted subscriptions
    across page refreshes instead of keeping them only in browser memory.
    """
    inspector = inspect(db.engine)

    if "subscriptions" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns("subscriptions")
    }

    if "deleted_at" in existing_columns:
        return

    db.session.execute(
        text("ALTER TABLE subscriptions ADD COLUMN deleted_at TIMESTAMP NULL")
    )
    db.session.commit()


def ensure_subscription_recurrence_columns():
    """Add recurrence columns for older local databases."""
    inspector = inspect(db.engine)

    if "subscriptions" not in inspector.get_table_names():
        return

    existing_columns = {
        column["name"] for column in inspector.get_columns("subscriptions")
    }
    statements = []

    if "recurrence_unit" not in existing_columns:
        statements.append(
            "ALTER TABLE subscriptions ADD COLUMN recurrence_unit VARCHAR(20) NULL"
        )

    if "recurrence_interval" not in existing_columns:
        statements.append(
            "ALTER TABLE subscriptions ADD COLUMN recurrence_interval INTEGER NULL"
        )

    if "recurrence_end_mode" not in existing_columns:
        statements.append(
            "ALTER TABLE subscriptions ADD COLUMN recurrence_end_mode VARCHAR(20) NULL"
        )

    if "recurrence_end_date" not in existing_columns:
        statements.append(
            "ALTER TABLE subscriptions ADD COLUMN recurrence_end_date DATE NULL"
        )

    for statement in statements:
        db.session.execute(text(statement))

    if statements:
        db.session.commit()

    db.session.execute(
        text(
            """
            UPDATE subscriptions
            SET recurrence_unit = CASE
                WHEN billing_cycle = 'daily' THEN 'day'
                WHEN billing_cycle = 'weekly' THEN 'week'
                WHEN billing_cycle = 'annual' THEN 'year'
                ELSE 'month'
            END
            WHERE recurrence_unit IS NULL
            """
        )
    )
    db.session.execute(
        text(
            """
            UPDATE subscriptions
            SET recurrence_interval = 1
            WHERE recurrence_interval IS NULL
            """
        )
    )
    db.session.execute(
        text(
            """
            UPDATE subscriptions
            SET recurrence_end_mode = 'forever'
            WHERE recurrence_end_mode IS NULL
            """
        )
    )
    db.session.commit()

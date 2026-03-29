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

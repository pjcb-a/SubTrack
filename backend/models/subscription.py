from models import db
from utils.subscription_utils import (
    get_legacy_billing_cycle,
    get_next_due_date,
    get_subscription_anchor_date,
    get_subscription_recurrence_interval,
    get_subscription_recurrence_unit,
)


class Subscription(db.Model):
    """Main business record for a tracked subscription.

    System role:
    This table powers the dashboard, summaries, due-date calculations, and
    CRUD routes.

    Frontend role:
    When the frontend is connected, the dashboard cards, calendar, and edit
    forms will be driven by the JSON returned from `to_dict()`.
    """
    __tablename__ = "subscriptions"

    subscription_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"), nullable=False)
    category_id = db.Column(
        db.Integer,
        db.ForeignKey("categories.category_id"),
        nullable=False,
    )
    subscription_name = db.Column(db.String(120), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    billing_cycle = db.Column(db.String(20), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    due_day = db.Column(db.Integer, nullable=False)
    recurrence_unit = db.Column(db.String(16), nullable=True)
    recurrence_interval = db.Column(db.Integer, nullable=True)
    anchor_date = db.Column(db.Date, nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    deleted_at = db.Column(db.DateTime, nullable=True)

    user = db.relationship("User", back_populates="subscriptions")
    category = db.relationship("Category", back_populates="subscriptions")
    notification_setting = db.relationship(
        "NotificationSetting",
        back_populates="subscription",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """Return a frontend-friendly JSON version of a subscription.

        This flattens related data such as category name and notification
        settings so the UI can render one object without making extra requests.
        """
        next_due_date = get_next_due_date(self)
        recurrence_unit = get_subscription_recurrence_unit(self)
        recurrence_interval = get_subscription_recurrence_interval(self)
        anchor_date = get_subscription_anchor_date(self)

        return {
            "subscription_id": self.subscription_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "category_name": self.category.category_name if self.category else None,
            "subscription_name": self.subscription_name,
            "amount": float(self.amount),
            "billing_cycle": get_legacy_billing_cycle(
                recurrence_unit,
                recurrence_interval,
            ),
            "start_date": self.start_date.isoformat(),
            "next_due_date": next_due_date.isoformat() if next_due_date else None,
            "due_day": self.due_day,
            "recurrence_unit": recurrence_unit,
            "recurrence_interval": recurrence_interval,
            "anchor_date": anchor_date.isoformat() if anchor_date else None,
            "is_active": self.is_active,
            "deleted_at": self.deleted_at.isoformat() if self.deleted_at else None,
            "notification_setting": (
                self.notification_setting.to_dict()
                if self.notification_setting
                else None
            ),
        }

    def sync_legacy_schedule_fields(self):
        """Keep transitional legacy columns aligned with recurrence fields."""
        anchor_date = get_subscription_anchor_date(self)

        if not anchor_date:
            return

        self.start_date = anchor_date
        self.due_day = anchor_date.day
        self.billing_cycle = get_legacy_billing_cycle(
            get_subscription_recurrence_unit(self),
            get_subscription_recurrence_interval(self),
        )

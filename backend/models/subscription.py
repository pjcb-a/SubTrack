from models import db
from utils.subscription_utils import get_next_due_date


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
    is_active = db.Column(db.Boolean, default=True, nullable=False)

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

        return {
            "subscription_id": self.subscription_id,
            "user_id": self.user_id,
            "category_id": self.category_id,
            "category_name": self.category.category_name if self.category else None,
            "subscription_name": self.subscription_name,
            "amount": float(self.amount),
            "billing_cycle": self.billing_cycle,
            "start_date": self.start_date.isoformat(),
            "next_due_date": next_due_date.isoformat() if next_due_date else None,
            "due_day": self.due_day,
            "is_active": self.is_active,
            "notification_setting": (
                self.notification_setting.to_dict()
                if self.notification_setting
                else None
            ),
        }

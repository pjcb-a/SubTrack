from models import db


class NotificationSetting(db.Model):
    """Stores reminder preferences attached to exactly one subscription.

    System role:
    This model lets the backend keep notification rules separate from the main
    subscription row while still returning them together in API responses.
    """
    __tablename__ = "notification_settings"

    notification_id = db.Column(db.Integer, primary_key=True)
    subscription_id = db.Column(
        db.Integer,
        db.ForeignKey("subscriptions.subscription_id"),
        nullable=False,
        unique=True,
    )
    notify_days_before = db.Column(db.Integer, default=3, nullable=False)
    notification_enabled = db.Column(db.Boolean, default=True, nullable=False)

    subscription = db.relationship(
        "Subscription",
        back_populates="notification_setting",
    )

    def to_dict(self):
        """Serialize reminder settings for subscription API responses."""
        return {
            "notification_id": self.notification_id,
            "subscription_id": self.subscription_id,
            "notify_days_before": self.notify_days_before,
            "notification_enabled": self.notification_enabled,
        }

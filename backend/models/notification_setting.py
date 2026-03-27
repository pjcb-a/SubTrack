from models import db


# FOR STORING REMINDER SETTINGS FOR ONE SUBSCRIPTION
class NotificationSetting(db.Model):
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

    # FOR SENDING NOTIFICATION SETTING DATA BACK AS JSON
    def to_dict(self):
        return {
            "notification_id": self.notification_id,
            "subscription_id": self.subscription_id,
            "notify_days_before": self.notify_days_before,
            "notification_enabled": self.notification_enabled,
        }

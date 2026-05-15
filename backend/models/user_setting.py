from datetime import datetime

from models import db


class UserSetting(db.Model):
    """Stores one persisted settings row per user."""

    __tablename__ = "user_settings"

    user_setting_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.user_id"),
        nullable=False,
        unique=True,
    )
    renewal_reminders_enabled = db.Column(
        db.Boolean,
        default=True,
        nullable=False,
    )
    monthly_reports_enabled = db.Column(
        db.Boolean,
        default=False,
        nullable=False,
    )
    spending_cap_mode = db.Column(
        db.String(20),
        default="none",
        nullable=False,
    )
    spending_cap_amount = db.Column(
        db.Numeric(10, 2),
        default=0,
        nullable=False,
    )
    soft_cap_overage_percent = db.Column(
        db.Numeric(5, 2),
        default=0,
        nullable=False,
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False,
    )
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )

    user = db.relationship("User", back_populates="settings")

    def to_dict(self):
        return {
            "renewal_reminders_enabled": self.renewal_reminders_enabled,
            "monthly_reports_enabled": self.monthly_reports_enabled,
            "spending_cap_mode": self.spending_cap_mode,
            "spending_cap_amount": (
                float(self.spending_cap_amount)
                if self.spending_cap_amount is not None
                else None
            ),
            "soft_cap_overage_percent": (
                float(self.soft_cap_overage_percent)
                if self.soft_cap_overage_percent is not None
                else None
            ),
        }

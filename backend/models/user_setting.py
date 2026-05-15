from datetime import datetime

from models import db


class UserSetting(db.Model):
    """Stores global dashboard/account preferences for one user."""

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
        nullable=False,
        default=True,
    )
    monthly_reports_enabled = db.Column(
        db.Boolean,
        nullable=False,
        default=False,
    )
    spending_cap_mode = db.Column(
        db.String(16),
        nullable=False,
        default="none",
    )
    spending_cap_amount = db.Column(
        db.Numeric(10, 2),
        nullable=False,
        default=0,
    )
    soft_cap_overage_percent = db.Column(
        db.Numeric(5, 2),
        nullable=False,
        default=0,
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
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
            "spending_cap_amount": float(self.spending_cap_amount or 0),
            "soft_cap_overage_percent": float(
                self.soft_cap_overage_percent or 0
            ),
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }

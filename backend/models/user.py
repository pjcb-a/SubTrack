from datetime import datetime

from models import db


class User(db.Model):
    """Stores account data for authentication and ownership checks.

    System role:
    Routes use this table to register users, log them in, and scope
    subscriptions to the correct account.
    """
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    subscriptions = db.relationship(
        "Subscription",
        back_populates="user",
        cascade="all, delete-orphan",
    )
    settings = db.relationship(
        "UserSetting",
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        """Return only safe user fields for the API response.

        `password_hash` is intentionally excluded so it never leaks to the
        frontend or any API consumer.
        """
        return {
            "user_id": self.user_id,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat(),
        }

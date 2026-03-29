from models import db


class Category(db.Model):
    """Lookup table for subscription categories like Music or Education.

    Backend use:
    Subscription rows reference this table through `category_id`.

    Frontend use:
    Once the frontend is connected, category names from `to_dict()` can be
    shown in forms, lists, and filters without hardcoding them in the UI.
    """
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    subscriptions = db.relationship(
        "Subscription",
        back_populates="category",
    )

    def to_dict(self):
        """Serialize the category into API-safe JSON."""
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
        }

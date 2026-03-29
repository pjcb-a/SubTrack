from models import db


# FOR STORING SUBSCRIPTION CATEGORY NAMES
class Category(db.Model):
    __tablename__ = "categories"

    category_id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), unique=True, nullable=False)

    subscriptions = db.relationship(
        "Subscription",
        back_populates="category",
    )

    # FOR SENDING CATEGORY DATA BACK AS JSON
    def to_dict(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
        }

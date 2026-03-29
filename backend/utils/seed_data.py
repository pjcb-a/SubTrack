from models import db
from models.category import Category


DEFAULT_CATEGORIES = [
    {"category_id": 1, "category_name": "Entertainment"},
    {"category_id": 2, "category_name": "Productivity"},
    {"category_id": 3, "category_name": "Music"},
    {"category_id": 4, "category_name": "Cloud Storage"},
    {"category_id": 5, "category_name": "Education"},
]


# FOR ADDING DEFAULT CATEGORIES WHEN THE DATABASE IS EMPTY
def seed_default_categories():
    for category_data in DEFAULT_CATEGORIES:
        category = db.session.get(Category, category_data["category_id"])

        if not category:
            existing_with_same_name = Category.query.filter_by(
                category_name=category_data["category_name"]
            ).first()

            if not existing_with_same_name:
                db.session.add(Category(**category_data))

    db.session.commit()

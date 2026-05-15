from flask_sqlalchemy import SQLAlchemy


# Shared SQLAlchemy object used everywhere in the backend.
# `app.py` binds this object to the Flask app during startup.
db = SQLAlchemy()

# Importing the models here has two jobs:
# 1. it makes the classes easy to import from `models`
# 2. it registers every table definition before `db.create_all()` runs in app.py
from models.category import Category
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from models.user import User
from models.user_setting import UserSetting


__all__ = [
    "db",
    "User",
    "UserSetting",
    "Category",
    "Subscription",
    "NotificationSetting",
]

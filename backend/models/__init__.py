from flask_sqlalchemy import SQLAlchemy


# FOR CREATING THE SHARED DATABASE OBJECT
db = SQLAlchemy()

# FOR MAKING THE MODELS AVAILABLE ACROSS THE APP
from models.category import Category
from models.notification_setting import NotificationSetting
from models.subscription import Subscription
from models.user import User


__all__ = ["db", "User", "Category", "Subscription", "NotificationSetting"]

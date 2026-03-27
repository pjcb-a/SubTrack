from functools import wraps

from flask import g, jsonify, session

from models import db
from models.user import User


# FOR PROTECTING ROUTES THAT REQUIRE LOGIN
def login_required(route_function):
    @wraps(route_function)
    def wrapper(*args, **kwargs):
        user_id = session.get("user_id")

        if not user_id:
            return jsonify({"error": "Authentication required"}), 401

        user = db.session.get(User, user_id)

        if not user:
            session.clear()
            return jsonify({"error": "User session is no longer valid"}), 401

        g.current_user = user
        return route_function(*args, **kwargs)

    return wrapper

"""
Authentication helpers shared by route files.

The main piece here is `login_required`, which protects endpoints that should
only be accessible after the browser has logged in through `/api/auth/login`.
"""

from functools import wraps

from flask import g, jsonify, session

from models import db
from models.user import User


def login_required(route_function):
    """Reject requests that do not have a valid logged-in session.

    System effect:
    - reads `user_id` from the Flask session cookie
    - loads the corresponding user from the database
    - stores that user in `g.current_user` for the route handler

    Route usage:
    `subscription_routes.py` and `user_routes.py` use this decorator to scope
    every protected action to the authenticated user.
    """
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

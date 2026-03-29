"""
User profile endpoints.

This route group exposes lightweight user data for the current browser session.
Unlike the write endpoints, the session check route is intentionally soft: a
logged-out browser gets a normal JSON response instead of an error so the
frontend can load the login screen without treating "not logged in yet" as a
failure state.
"""

from flask import Blueprint, jsonify, session

from models import db
from models.user import User


user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.get("")
def get_current_user():
    """Return session state for the current browser.

    Expected frontend use:
    - app startup can check whether a session already exists
    - logged-in UIs can read the current user without another login call

    Response behavior:
    - authenticated browsers get `{"authenticated": true, "user": {...}}`
    - logged-out browsers get `{"authenticated": false, "user": null}`
    """
    user_id = session.get("user_id")

    if not user_id:
        return jsonify({"authenticated": False, "user": None})

    user = db.session.get(User, user_id)

    if not user:
        session.clear()
        return jsonify({"authenticated": False, "user": None})

    return jsonify({"authenticated": True, "user": user.to_dict()})

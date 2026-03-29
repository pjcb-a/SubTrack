"""
User profile endpoints.

This route group exposes lightweight user data for the currently logged-in
browser session.
"""

from flask import Blueprint, jsonify, g

from utils.auth import login_required


user_bp = Blueprint("user", __name__, url_prefix="/api/user")


@user_bp.get("")
@login_required
def get_current_user():
    """Return the authenticated user's safe profile fields.

    Expected frontend use:
    Header/profile widgets can call this after login to personalize the UI.
    """
    return jsonify({"user": g.current_user.to_dict()})

from flask import Blueprint, jsonify, g

from utils.auth import login_required


user_bp = Blueprint("user", __name__, url_prefix="/api/user")


# FOR RETURNING THE CURRENT LOGGED-IN USER
@user_bp.get("")
@login_required
def get_current_user():
    return jsonify({"user": g.current_user.to_dict()})

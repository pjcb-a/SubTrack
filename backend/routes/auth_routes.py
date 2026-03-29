"""
Authentication endpoints used for registration, login, and logout.

These routes are the future bridge between the login/register frontend forms
and the Flask session system. Right now the frontend is not calling them yet.
"""

from flask import Blueprint, jsonify, request, session
from sqlalchemy import or_
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.user import User
from utils.validators import is_valid_email


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@auth_bp.post("/register")
def register():
    """Create a new user account and store a hashed password.

    Expected frontend caller:
    A registration form should POST `username`, `email`, and `password` here.
    """
    data = request.get_json(silent=True) or {}

    username = str(data.get("username", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not username or not email or not password:
        return jsonify({"error": "username, email, and password are required"}), 400

    if not is_valid_email(email):
        return jsonify({"error": "Please provide a valid email address"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username is already taken"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email is already registered"}), 409

    user = User(
        username=username,
        email=email,
        password_hash=generate_password_hash(password),
    )

    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {
                "message": "User registered successfully",
                "user": user.to_dict(),
            }
        ),
        201,
    )


@auth_bp.post("/login")
def login():
    """Authenticate a user and persist their ID in the Flask session.

    System effect:
    After this succeeds, protected routes can find the user through the session
    cookie sent by the browser.
    """
    data = request.get_json(silent=True) or {}

    identifier = str(
        data.get("email")
        or data.get("username")
        or data.get("identifier")
        or ""
    ).strip()
    password = str(data.get("password", ""))

    if not identifier or not password:
        return jsonify({"error": "username/email and password are required"}), 400

    lowered_identifier = identifier.lower()
    user = User.query.filter(
        or_(
            User.email == lowered_identifier,
            User.username == identifier,
        )
    ).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid username/email or password"}), 401

    session.clear()
    session["user_id"] = user.user_id

    return jsonify(
        {
            "message": "Login successful",
            "user": user.to_dict(),
        }
    )


@auth_bp.post("/logout")
def logout():
    """Clear the current browser session."""
    session.clear()
    return jsonify({"message": "Logout successful"})

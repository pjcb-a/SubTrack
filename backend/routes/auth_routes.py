from flask import Blueprint, jsonify, request, session
from werkzeug.security import check_password_hash, generate_password_hash

from models import db
from models.user import User
from utils.validators import is_valid_email


auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# FOR REGISTERING A NEW USER
@auth_bp.post("/register")
def register():
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


# FOR LOGGING IN A USER
@auth_bp.post("/login")
def login():
    data = request.get_json(silent=True) or {}

    email = str(data.get("email", "")).strip().lower()
    password = str(data.get("password", ""))

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    session.clear()
    session["user_id"] = user.user_id

    return jsonify(
        {
            "message": "Login successful",
            "user": user.to_dict(),
        }
    )


# FOR LOGGING OUT THE CURRENT USER
@auth_bp.post("/logout")
def logout():
    session.clear()
    return jsonify({"message": "Logout successful"})

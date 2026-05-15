"""
Application entry point for the Flask API.

This file creates the Flask app instance, loads shared config, attaches the
database, enables cross-origin requests from the frontend, and registers the
route groups that expose the API consumed by the UI.
"""

import os

from flask import Flask, jsonify
from flask_cors import CORS

from config import Config
from models import db
from routes.auth_routes import auth_bp
from routes.subscription_routes import subscription_bp
from routes.user_routes import user_bp
from utils.schema_sync import ensure_subscription_deleted_at_column
from utils.seed_data import seed_default_categories


def create_app():
    """Build the Flask application used by both local dev and production.

    Main responsibilities:
    - load settings from `config.py`
    - connect SQLAlchemy so route files can query the database
    - allow browser requests from the frontend through CORS
    - register API blueprints for auth, user profile, and subscriptions
    - create tables and default categories on first startup

    Frontend impact:
    When the Vue frontend is later switched from mock data to real API calls,
    every request will eventually enter the system through this app instance.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # Makes the shared `db` object in models/__init__.py use this app's config.
    db.init_app(app)

    # Lets the frontend running on Vite/localhost call the Flask API and send
    # session cookies. Without this, browser requests from the frontend would be
    # blocked even if the backend is running correctly.
    CORS(
        app,
        supports_credentials=True,
        origins=app.config["CORS_ORIGINS"],
        methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],                                                                                                           
        allow_headers=["Content-Type", "Authorization"],
    )

    # Each blueprint groups related endpoints.
    # These routes are the backend surface that the frontend will eventually call.
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(subscription_bp)

    @app.errorhandler(404)
    def not_found(_error):
        """Return JSON instead of HTML for missing API routes."""
        return jsonify({"error": "Route not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(_error):
        """Return JSON when a route exists but the HTTP method is wrong."""
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(500)
    def internal_server_error(_error):
        """Rollback failed DB work so one broken request does not poison later ones."""
        db.session.rollback()
        return jsonify({"error": "Internal server error"}), 500

    # Initializes the database on startup so the backend can boot on a clean
    # machine without a manual migration step. The seeded categories are later
    # referenced by subscription creation and editing flows.
    # Only run DB init locally. 
    # For Production (Vercel), handle migrations/seeding manually or via a script.
    # if not os.getenv("VERCEL"):
    #     with app.app_context():
    #         db.create_all()
            # ensure_subscription_deleted_at_column()
            # seed_default_categories()

    return app


# Exposes the ready-to-run Flask app object used by `python app.py`.
app = create_app()


if __name__ == "__main__":
    # Local development server entrypoint.
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5001"))
    app.run(debug=True, host=host, port=port)

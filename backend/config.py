"""
Centralized runtime settings for the backend.

`app.py` imports `Config` from here so the whole backend reads environment
values from one place. The CORS settings in this file directly affect whether
the frontend browser can call the API.
"""

import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

if os.path.exists(os.path.join(BASE_DIR, ".env")):
    load_dotenv(os.path.join(BASE_DIR, ".env"))

LOCAL_DEV_CORS_ORIGINS = [
    "http://127.0.0.1:5173", 
    "http://localhost:5173",
]


def get_bool_env(name, default=False):
    """Parse a boolean env flag using common truthy string values."""
    raw_value = os.getenv(name)

    if raw_value is None:
        return default

    return raw_value.strip().lower() in {"1", "true", "yes", "on"}


def get_cors_origins():
    """Return the list of frontend URLs allowed to access the API.

    This is consumed by Flask-CORS in `app.py`. If the frontend runs on a URL
    that is not listed here, browser requests from the UI will fail even when
    the endpoint itself works.
    """
    cors_value = os.getenv("CORS_ORIGINS", "")
    configured_origins = [
        origin.strip() for origin in cors_value.split(",") if origin.strip()
    ]

    if configured_origins:
        return configured_origins

    # Defaults to common local-development hosts so a freshly cloned project
    # can run from localhost, loopback, or a machine's private LAN address
    # without editing environment files first.
    return LOCAL_DEV_CORS_ORIGINS


class Config:
    """Flask config object loaded by `app.config.from_object(Config)`.

    System effect:
    - `SECRET_KEY` secures the Flask session cookie used after login
    - `SQLALCHEMY_DATABASE_URI` chooses which database stores app data
    - `CORS_ORIGINS` controls which frontend hosts can talk to the backend
    """
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        SECRET_KEY = "subtrack-dev-secret"  # Fallback for local dev only
    
    _database_url = os.getenv("DATABASE_URL")
    
    # Check if we are on Vercel/Production and fix the prefix
    if _database_url and _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)
    
    SQLALCHEMY_DATABASE_URI = _database_url or f"sqlite:///{os.path.join(BASE_DIR, 'subtrack.db')}"

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    # Logic for cross-domain cookies (Vercel)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "None" if os.getenv("FLASK_ENV") == "production" else "Lax"
    SESSION_COOKIE_SECURE = True if os.getenv("FLASK_ENV") == "production" else False
    # Keep local HTTP development usable by default. Production deployments
    # should opt in explicitly through `SESSION_COOKIE_SECURE=true`.
    CORS_ORIGINS = get_cors_origins()

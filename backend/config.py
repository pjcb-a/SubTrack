"""
Centralized runtime settings for the backend.

`app.py` imports `Config` from here so the whole backend reads environment
values from one place. The CORS settings in this file directly affect whether
the frontend browser can call the API.
"""

import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))

env_path = os.path.join(BASE_DIR, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

LOCAL_DEV_CORS_ORIGINS = [
    r"^https?://localhost(?::\d+)?$",
    r"^https?://127\.0\.0\.1(?::\d+)?$",
    r"^https?://192\.168\.\d{1,3}\.\d{1,3}(?::\d+)?$",
    r"^https?://10\.\d{1,3}\.\d{1,3}\.\d{1,3}(?::\d+)?$",
    r"^https?://172\.(1[6-9]|2\d|3[0-1])\.\d{1,3}\.\d{1,3}(?::\d+)?$",
]


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
    SECRET_KEY = os.getenv("SECRET_KEY", "subtrack-dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'subtrack.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"
    CORS_ORIGINS = get_cors_origins()

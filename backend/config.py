import os

from dotenv import load_dotenv


BASE_DIR = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(BASE_DIR, ".env"))


# FOR READING ALLOWED FRONTEND ORIGINS FROM THE ENVIRONMENT
def get_cors_origins():
    cors_value = os.getenv(
        "CORS_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://127.0.0.1:3000",
    )
    return [origin.strip() for origin in cors_value.split(",") if origin.strip()]


# FOR STORING THE MAIN FLASK SETTINGS
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "subtrack-dev-secret")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, 'subtrack.db')}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = False
    CORS_ORIGINS = get_cors_origins()

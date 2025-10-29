import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        # Default to SQLite for local development/testing
        "sqlite:///todo.db",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False



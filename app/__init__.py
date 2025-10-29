import logging
import os
from datetime import timedelta

from flask import Flask, redirect, session, url_for
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")

    # Configuration
    app.config.from_object("config.Config")

    # Session config
    app.permanent_session_lifetime = timedelta(days=7)

    # Initialize extensions
    db.init_app(app)

    # Logging
    configure_logging(app)

    # Register blueprints
    from .auth import auth_bp
    from .todos import todos_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(todos_bp)

    # Create tables if not exist (for simplicity; in production use migrations)
    with app.app_context():
        from . import models  # noqa: F401 ensure models are registered
        db.create_all()

    # Root route → redirect based on auth status
    @app.route("/")
    def root():
        if session.get("user_id"):
            return redirect(url_for("todos.index"))
        return redirect(url_for("auth.login"))

    return app


def configure_logging(app: Flask) -> None:
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )
    handler.setFormatter(formatter)
    app.logger.setLevel(log_level)
    app.logger.addHandler(handler)



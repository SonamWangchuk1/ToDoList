import os
import tempfile
import pytest

from app import create_app, db
from app.models import User
from werkzeug.security import generate_password_hash


@pytest.fixture()
def app():
    db_fd, db_path = tempfile.mkstemp()
    os.close(db_fd)

    # Ensure the app uses the temp database before initialization
    os.environ["DATABASE_URL"] = f"sqlite:///{db_path}"
    os.environ["SECRET_KEY"] = "test-secret"

    test_app = create_app()
    test_app.config.update(
        TESTING=True,
    )

    with test_app.app_context():
        db.drop_all()
        db.create_all()

    yield test_app

    # Cleanup
    try:
        os.unlink(db_path)
    finally:
        os.environ.pop("DATABASE_URL", None)
        os.environ.pop("SECRET_KEY", None)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()


def create_user(email="user@example.com", password="secret123"):
    user = User(email=email, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return user


def login(client, email="user@example.com", password="secret123"):
    return client.post("/auth/login", data={"email": email, "password": password}, follow_redirects=True)



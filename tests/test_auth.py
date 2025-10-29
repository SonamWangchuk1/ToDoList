from app import db
from app.models import User


def test_signup_validation(client):
    # Missing fields
    resp = client.post("/auth/signup", data={"email": "", "password": "a", "confirm_password": "b"}, follow_redirects=True)
    assert b"All fields are required" in resp.data

    # Password mismatch
    resp = client.post("/auth/signup", data={"email": "new@example.com", "password": "secret123", "confirm_password": "mismatch"}, follow_redirects=True)
    assert b"Passwords do not match" in resp.data

    # Too short
    resp = client.post("/auth/signup", data={"email": "new@example.com", "password": "123", "confirm_password": "123"}, follow_redirects=True)
    assert b"at least 6 characters" in resp.data


def test_signup_and_login_flow(client):
    resp = client.post("/auth/signup", data={"email": "user@example.com", "password": "secret123", "confirm_password": "secret123"}, follow_redirects=True)
    assert b"Signup successful" in resp.data

    resp = client.post("/auth/login", data={"email": "user@example.com", "password": "secret123"}, follow_redirects=True)
    assert b"My Todos" in resp.data


def test_invalid_login(client):
    resp = client.post("/auth/login", data={"email": "nouser@example.com", "password": "nope"}, follow_redirects=True)
    assert b"Invalid email or password" in resp.data



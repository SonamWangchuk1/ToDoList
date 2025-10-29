from typing import Optional

from flask import Blueprint, flash, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from . import db
from .models import User


auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


def get_current_user_id() -> Optional[int]:
    return session.get("user_id")


def login_required(view_func):
    def wrapped(*args, **kwargs):
        if not get_current_user_id():
            return redirect(url_for("auth.login"))
        return view_func(*args, **kwargs)

    # Preserve function identity for Flask debug
    wrapped.__name__ = view_func.__name__
    return wrapped


@auth_bp.route("/signup", methods=["GET", "POST"]) 
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm_password", "")

        error = None
        if not email or not password or not confirm:
            error = "All fields are required."
        elif "@" not in email:
            error = "Please enter a valid email."
        elif password != confirm:
            error = "Passwords do not match."
        elif len(password) < 6:
            error = "Password must be at least 6 characters."
        elif User.query.filter_by(email=email).first() is not None:
            error = "Email already registered."

        if error:
            flash(error, "error")
        else:
            user = User(email=email, password_hash=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            flash("Signup successful. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("signup.html")


@auth_bp.route("/login", methods=["GET", "POST"]) 
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            session.permanent = True
            session["user_id"] = user.id
            return redirect(url_for("todos.index"))
        flash("Invalid email or password.", "error")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("auth.login"))



from flask import Blueprint, abort, flash, redirect, render_template, request, url_for

from . import db
from .auth import get_current_user_id, login_required
from .models import Todo


todos_bp = Blueprint("todos", __name__, url_prefix="/todos")


@todos_bp.route("/", methods=["GET", "POST"]) 
@login_required
def index():
    user_id = get_current_user_id()

    if request.method == "POST":
        task = request.form.get("task", "").strip()
        if not task:
            flash("Task cannot be empty.", "error")
        else:
            todo = Todo(user_id=user_id, task=task)
            db.session.add(todo)
            db.session.commit()
            flash("Task added.", "success")
        return redirect(url_for("todos.index"))

    items = Todo.query.filter_by(user_id=user_id).order_by(Todo.created_at.desc()).all()
    return render_template("todos.html", todos=items)


@todos_bp.route("/edit/<int:todo_id>", methods=["POST"]) 
@login_required
def edit(todo_id: int):
    user_id = get_current_user_id()
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != user_id:
        abort(403)
    new_task = request.form.get("task", "").strip()
    if not new_task:
        flash("Task cannot be empty.", "error")
    else:
        todo.task = new_task
        db.session.commit()
        flash("Task updated.", "success")
    return redirect(url_for("todos.index"))


@todos_bp.route("/delete/<int:todo_id>", methods=["POST"]) 
@login_required
def delete(todo_id: int):
    user_id = get_current_user_id()
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != user_id:
        abort(403)
    db.session.delete(todo)
    db.session.commit()
    flash("Task deleted.", "success")
    return redirect(url_for("todos.index"))


@todos_bp.route("/toggle/<int:todo_id>", methods=["POST"]) 
@login_required
def toggle(todo_id: int):
    user_id = get_current_user_id()
    todo = Todo.query.get_or_404(todo_id)
    if todo.user_id != user_id:
        abort(403)
    todo.completed = not todo.completed
    db.session.commit()
    return redirect(url_for("todos.index"))



from app import db
from app.models import Todo
from tests.conftest import create_user, login


def test_requires_login(client):
    resp = client.get("/todos/", follow_redirects=False)
    assert resp.status_code == 302
    assert "/auth/login" in resp.location


def test_add_edit_toggle_delete_todo(client, app):
    with app.app_context():
        user = create_user()

    login(client)

    # Add
    resp = client.post("/todos/", data={"task": "Write tests"}, follow_redirects=True)
    assert b"Task added" in resp.data
    with app.app_context():
        todo = Todo.query.first()
        assert todo and todo.task == "Write tests"

    # Edit
    with app.app_context():
        todo_id = Todo.query.first().id
    resp = client.post(f"/todos/edit/{todo_id}", data={"task": "Write more tests"}, follow_redirects=True)
    assert b"Task updated" in resp.data
    with app.app_context():
        assert Todo.query.first().task == "Write more tests"

    # Toggle
    resp = client.post(f"/todos/toggle/{todo_id}", follow_redirects=True)
    with app.app_context():
        assert Todo.query.get(todo_id).completed is True

    # Delete
    resp = client.post(f"/todos/delete/{todo_id}", follow_redirects=True)
    assert b"Task deleted" in resp.data
    with app.app_context():
        assert Todo.query.get(todo_id) is None


def test_authorization_is_enforced(client, app):
    # Create two users and a todo for user1
    with app.app_context():
        user1 = create_user(email="u1@example.com")
        user2 = create_user(email="u2@example.com")
        t = Todo(user_id=user1.id, task="Private task")
        db.session.add(t)
        db.session.commit()
        todo_id = t.id

    # Login as user2 and try to edit/delete user1's todo
    login(client, email="u2@example.com")

    resp = client.post(f"/todos/edit/{todo_id}", data={"task": "Hack"})
    assert resp.status_code == 403

    resp = client.post(f"/todos/delete/{todo_id}")
    assert resp.status_code == 403



# Todo List Web Application

Simple multi-user todo app built with Flask, PostgreSQL, Docker, and GitHub Actions CI.

## Features
- User signup/login with secure password hashing
- User-specific todos: add, edit, delete, toggle completed
- Session-based authentication and protected routes
- PostgreSQL support (via SQLAlchemy) with SQLite fallback for local/dev
- Dockerfile and docker-compose for app + Postgres
- GitHub Actions workflow to run tests and build Docker image

## Project Structure
```
app/
  __init__.py
  models.py
  auth.py
  todos.py
  templates/
    base.html
    login.html
    signup.html
    todos.html
  static/
    styles.css
config.py
wsgi.py
requirements.txt
Dockerfile
docker-compose.yml
.github/workflows/ci.yml
tests/
  conftest.py
  test_auth.py
  test_todos.py
```

## Local Setup
1. Python 3.12+ recommended
2. Create a virtual environment and install dependencies
```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```
3. Run the app (SQLite by default)
```bash
export SECRET_KEY=dev-secret
python wsgi.py
```
App listens on http://localhost:5000

## Run with Docker Compose (PostgreSQL)
```bash
docker compose up --build
```
App: http://localhost:5000

## Configuration
- `SECRET_KEY`: Flask secret key
- `DATABASE_URL`: SQLAlchemy URL. Examples:
  - SQLite: `sqlite:///todo.db`
  - Postgres (local): `postgresql+psycopg2://todo:todo@localhost:5432/todo`

## Testing
```bash
pytest -q
```
Tests use an isolated SQLite database.

## GitHub Actions CI
Workflow: `.github/workflows/ci.yml`
- Runs unit tests
- Builds Docker image
- Optionally pushes to Docker Hub when `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set

## Security Notes
- Change `SECRET_KEY` in production
- Use a managed Postgres with strong credentials
- Consider adding CSRF protection and HTTPS in production


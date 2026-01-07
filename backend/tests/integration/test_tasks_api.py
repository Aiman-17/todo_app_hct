"""
Integration tests for tasks API endpoints.

Tests CRUD operations, completion toggling, and user isolation with FastAPI TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models.user import User
from src.services.task_service import create_task


def get_auth_headers(client: TestClient, email: str, password: str) -> dict:
    """Helper function to get authentication headers."""
    response = client.post("/api/auth/login", json={
        "email": email,
        "password": password
    })
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_get_tasks_authenticated(client: TestClient, test_user: User, db_session: Session):
    """Test retrieving tasks for authenticated user."""
    # Create some tasks for test_user
    create_task(db_session, test_user.id, "Task 1", "Description 1")
    create_task(db_session, test_user.id, "Task 2", "Description 2")

    # Get auth headers
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Get tasks
    response = client.get("/api/tasks", headers=headers)

    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "Task 2"  # Newest first (created_at DESC)
    assert tasks[1]["title"] == "Task 1"


def test_get_tasks_unauthenticated(client: TestClient):
    """Test that tasks endpoint requires authentication."""
    response = client.get("/api/tasks")
    assert response.status_code == 401


def test_create_task(client: TestClient, test_user: User):
    """Test creating a new task."""
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    response = client.post("/api/tasks", headers=headers, json={
        "title": "Buy groceries",
        "description": "Milk, eggs, bread"
    })

    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert data["description"] == "Milk, eggs, bread"
    assert data["completed"] is False
    assert "id" in data
    assert "created_at" in data


def test_create_task_invalid_title(client: TestClient, test_user: User):
    """Test that task creation fails with invalid title."""
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Empty title
    response = client.post("/api/tasks", headers=headers, json={
        "title": "",
        "description": "Description"
    })
    assert response.status_code == 422

    # Title too long (>200 chars)
    response = client.post("/api/tasks", headers=headers, json={
        "title": "x" * 201,
        "description": "Description"
    })
    assert response.status_code == 422


def test_update_task(client: TestClient, test_user: User, db_session: Session):
    """Test updating a task."""
    # Create task
    task = create_task(db_session, test_user.id, "Original title", "Original description")
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Update task
    response = client.put(f"/api/tasks/{task.id}", headers=headers, json={
        "title": "Updated title",
        "description": "Updated description"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task.id
    assert data["title"] == "Updated title"
    assert data["description"] == "Updated description"


def test_update_task_partial(client: TestClient, test_user: User, db_session: Session):
    """Test partial update (only some fields)."""
    # Create task
    task = create_task(db_session, test_user.id, "Original title", "Original description")
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Update only title
    response = client.put(f"/api/tasks/{task.id}", headers=headers, json={
        "title": "Updated title"
    })

    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated title"
    assert data["description"] == "Original description"  # Unchanged


def test_delete_task(client: TestClient, test_user: User, db_session: Session):
    """Test deleting a task."""
    # Create task
    task = create_task(db_session, test_user.id, "Task to delete")
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Delete task
    response = client.delete(f"/api/tasks/{task.id}", headers=headers)
    assert response.status_code == 204

    # Verify task is deleted
    response = client.get("/api/tasks", headers=headers)
    tasks = response.json()
    assert len(tasks) == 0


def test_toggle_completion(client: TestClient, test_user: User, db_session: Session):
    """Test toggling task completion status."""
    # Create incomplete task
    task = create_task(db_session, test_user.id, "Task to complete")
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Toggle to complete
    response = client.patch(f"/api/tasks/{task.id}/toggle", headers=headers)
    assert response.status_code == 200
    assert response.json()["completed"] is True

    # Toggle back to incomplete
    response = client.patch(f"/api/tasks/{task.id}/toggle", headers=headers)
    assert response.status_code == 200
    assert response.json()["completed"] is False


def test_user_isolation_get_tasks(client: TestClient, test_user: User, db_session: Session):
    """Test that users can only see their own tasks."""
    # Create another user
    other_user = User(
        email="other@example.com",
        name="Other User",
        password_hash="$2b$12$hash"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Create tasks for both users
    create_task(db_session, test_user.id, "Test user task")
    create_task(db_session, other_user.id, "Other user task")

    # Login as test_user
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Get tasks - should only see test_user's task
    response = client.get("/api/tasks", headers=headers)
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "Test user task"


def test_user_isolation_update_task(client: TestClient, test_user: User, db_session: Session):
    """Test that users cannot update other users' tasks."""
    # Create another user and their task
    from src.services.user_service import create_user
    other_user = create_user(db_session, "other@example.com", "Other User", "OtherPass123")
    other_task = create_task(db_session, other_user.id, "Other user's task")

    # Login as test_user
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Try to update other user's task (should fail)
    response = client.put(f"/api/tasks/{other_task.id}", headers=headers, json={
        "title": "Hacked title"
    })
    assert response.status_code == 404  # Not found (user isolation)


def test_user_isolation_delete_task(client: TestClient, test_user: User, db_session: Session):
    """Test that users cannot delete other users' tasks."""
    # Create another user and their task
    from src.services.user_service import create_user
    other_user = create_user(db_session, "other@example.com", "Other User", "OtherPass123")
    other_task = create_task(db_session, other_user.id, "Other user's task")

    # Login as test_user
    headers = get_auth_headers(client, "test@example.com", "TestPass123")

    # Try to delete other user's task (should fail)
    response = client.delete(f"/api/tasks/{other_task.id}", headers=headers)
    assert response.status_code == 404  # Not found (user isolation)

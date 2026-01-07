"""
Unit tests for task service functions.

Tests CRUD operations and user isolation for tasks.
"""
import pytest
from sqlmodel import Session
from uuid import uuid4

from src.models.user import User
from src.models.task import Task
from src.services.task_service import (
    get_tasks,
    create_task,
    update_task,
    delete_task,
    toggle_completion,
    get_task_by_id
)


def test_create_task(db_session: Session, test_user: User):
    """Test creating a new task."""
    task = create_task(
        db=db_session,
        user_id=test_user.id,
        title="Buy groceries",
        description="Milk, eggs, bread"
    )

    assert task.id is not None
    assert task.user_id == test_user.id
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False


def test_get_tasks(db_session: Session, test_user: User):
    """Test retrieving all tasks for a user."""
    # Create multiple tasks
    task1 = create_task(db_session, test_user.id, "Task 1")
    task2 = create_task(db_session, test_user.id, "Task 2")
    task3 = create_task(db_session, test_user.id, "Task 3")

    # Get all tasks
    tasks = get_tasks(db_session, test_user.id)

    assert len(tasks) == 3
    assert all(task.user_id == test_user.id for task in tasks)


def test_get_tasks_user_isolation(db_session: Session, test_user: User):
    """Test that get_tasks only returns tasks for the specified user."""
    # Create another user
    other_user = User(
        email="other@example.com",
        name="Other User",
        password_hash="hash"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Create tasks for both users
    task1 = create_task(db_session, test_user.id, "Test user task 1")
    task2 = create_task(db_session, test_user.id, "Test user task 2")
    task3 = create_task(db_session, other_user.id, "Other user task")

    # Get tasks for test_user
    test_user_tasks = get_tasks(db_session, test_user.id)
    assert len(test_user_tasks) == 2
    assert all(task.user_id == test_user.id for task in test_user_tasks)

    # Get tasks for other_user
    other_user_tasks = get_tasks(db_session, other_user.id)
    assert len(other_user_tasks) == 1
    assert other_user_tasks[0].user_id == other_user.id


def test_update_task(db_session: Session, test_user: User):
    """Test updating task fields."""
    # Create task
    task = create_task(db_session, test_user.id, "Original title", "Original description")

    # Update task
    updated_task = update_task(
        db=db_session,
        task_id=task.id,
        user_id=test_user.id,
        title="Updated title",
        description="Updated description"
    )

    assert updated_task is not None
    assert updated_task.id == task.id
    assert updated_task.title == "Updated title"
    assert updated_task.description == "Updated description"


def test_update_task_user_isolation(db_session: Session, test_user: User):
    """Test that users cannot update other users' tasks."""
    # Create another user
    other_user = User(
        email="other@example.com",
        name="Other User",
        password_hash="hash"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Create task for other_user
    task = create_task(db_session, other_user.id, "Other user's task")

    # Try to update as test_user (should fail/return None)
    updated_task = update_task(
        db=db_session,
        task_id=task.id,
        user_id=test_user.id,  # Different user
        title="Hacked title"
    )

    assert updated_task is None  # Update should fail


def test_delete_task(db_session: Session, test_user: User):
    """Test deleting a task."""
    # Create task
    task = create_task(db_session, test_user.id, "Task to delete")
    task_id = task.id

    # Delete task
    result = delete_task(db_session, task_id, test_user.id)
    assert result is True

    # Verify task is deleted
    deleted_task = get_task_by_id(db_session, task_id, test_user.id)
    assert deleted_task is None


def test_delete_task_user_isolation(db_session: Session, test_user: User):
    """Test that users cannot delete other users' tasks."""
    # Create another user
    other_user = User(
        email="other@example.com",
        name="Other User",
        password_hash="hash"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Create task for other_user
    task = create_task(db_session, other_user.id, "Other user's task")

    # Try to delete as test_user (should fail)
    result = delete_task(db_session, task.id, test_user.id)
    assert result is False

    # Verify task still exists for other_user
    existing_task = get_task_by_id(db_session, task.id, other_user.id)
    assert existing_task is not None


def test_toggle_completion(db_session: Session, test_user: User):
    """Test toggling task completion status."""
    # Create incomplete task
    task = create_task(db_session, test_user.id, "Task to complete")
    assert task.completed is False

    # Toggle to complete
    updated_task = toggle_completion(db_session, task.id, test_user.id)
    assert updated_task is not None
    assert updated_task.completed is True

    # Toggle back to incomplete
    updated_task = toggle_completion(db_session, task.id, test_user.id)
    assert updated_task is not None
    assert updated_task.completed is False


def test_toggle_completion_user_isolation(db_session: Session, test_user: User):
    """Test that users cannot toggle other users' task completion."""
    # Create another user
    other_user = User(
        email="other@example.com",
        name="Other User",
        password_hash="hash"
    )
    db_session.add(other_user)
    db_session.commit()
    db_session.refresh(other_user)

    # Create task for other_user
    task = create_task(db_session, other_user.id, "Other user's task")

    # Try to toggle as test_user (should fail)
    updated_task = toggle_completion(db_session, task.id, test_user.id)
    assert updated_task is None  # Toggle should fail

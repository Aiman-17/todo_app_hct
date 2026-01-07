"""
Unit tests for Task model.

Tests task creation, updates, completion status changes, and field validation.
"""
import pytest
from sqlmodel import Session
from datetime import datetime, timezone

from src.models.user import User
from src.models.task import Task


def test_task_creation(db_session: Session, test_user: User):
    """Test creating a task with all fields."""
    task = Task(
        user_id=test_user.id,
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Verify auto-generated fields
    assert task.id is not None
    assert isinstance(task.id, int)
    assert task.created_at is not None
    assert task.updated_at is not None

    # Verify provided fields
    assert task.user_id == test_user.id
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False


def test_task_update(db_session: Session, test_user: User):
    """Test updating task fields (title, description)."""
    # Create initial task
    task = Task(
        user_id=test_user.id,
        title="Original title",
        description="Original description"
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    original_created_at = task.created_at
    original_updated_at = task.updated_at

    # Update task fields
    task.title = "Updated title"
    task.description = "Updated description"
    task.updated_at = datetime.now(timezone.utc)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    # Verify updates
    assert task.title == "Updated title"
    assert task.description == "Updated description"
    assert task.created_at == original_created_at  # Created timestamp unchanged
    assert task.updated_at > original_updated_at  # Updated timestamp changed


def test_task_completion(db_session: Session, test_user: User):
    """Test toggling task completion status."""
    # Create incomplete task
    task = Task(
        user_id=test_user.id,
        title="Task to complete",
        completed=False
    )
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.completed is False

    # Mark as complete
    task.completed = True
    task.updated_at = datetime.now(timezone.utc)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.completed is True

    # Mark as incomplete again
    task.completed = False
    task.updated_at = datetime.now(timezone.utc)
    db_session.add(task)
    db_session.commit()
    db_session.refresh(task)

    assert task.completed is False

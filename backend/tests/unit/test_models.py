"""
Unit tests for SQLModel models (User and Task).

Tests model creation, field validation, constraints, and relationships.
"""
import pytest
from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from uuid import UUID

from src.models.user import User
from src.models.task import Task


def test_user_model_creation(db_session: Session):
    """Test creating a user with all required fields."""
    user = User(
        email="alice@example.com",
        name="Alice Smith",
        password_hash="$2b$12$KIXxLhFz7xFGVwPq7Z8ZYeQ5X..."
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Verify auto-generated fields
    assert user.id is not None
    assert isinstance(user.id, UUID)
    assert user.created_at is not None
    assert user.updated_at is not None

    # Verify provided fields
    assert user.email == "alice@example.com"
    assert user.name == "Alice Smith"
    assert user.password_hash == "$2b$12$KIXxLhFz7xFGVwPq7Z8ZYeQ5X..."


def test_user_unique_email_constraint(db_session: Session):
    """Test that duplicate email addresses are rejected."""
    # Create first user
    user1 = User(
        email="alice@example.com",
        name="Alice Smith",
        password_hash="hash1"
    )
    db_session.add(user1)
    db_session.commit()

    # Attempt to create second user with same email
    user2 = User(
        email="alice@example.com",  # Duplicate email
        name="Alice Duplicate",
        password_hash="hash2"
    )
    db_session.add(user2)

    # Should raise IntegrityError due to unique constraint
    with pytest.raises(IntegrityError):
        db_session.commit()


def test_task_model_creation(db_session: Session):
    """Test creating a task with all required fields."""
    # Create a user first (foreign key requirement)
    user = User(
        email="alice@example.com",
        name="Alice Smith",
        password_hash="hash"
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)

    # Create task
    task = Task(
        user_id=user.id,
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
    assert task.user_id == user.id
    assert task.title == "Buy groceries"
    assert task.description == "Milk, eggs, bread"
    assert task.completed is False


def test_task_user_relationship(db_session: Session):
    """Test that tasks are correctly associated with users via foreign key."""
    # Create two users
    user1 = User(email="alice@example.com", name="Alice", password_hash="hash1")
    user2 = User(email="bob@example.com", name="Bob", password_hash="hash2")
    db_session.add(user1)
    db_session.add(user2)
    db_session.commit()
    db_session.refresh(user1)
    db_session.refresh(user2)

    # Create tasks for each user
    task1 = Task(user_id=user1.id, title="Alice's task 1")
    task2 = Task(user_id=user1.id, title="Alice's task 2")
    task3 = Task(user_id=user2.id, title="Bob's task 1")
    db_session.add(task1)
    db_session.add(task2)
    db_session.add(task3)
    db_session.commit()

    # Query tasks for user1
    user1_tasks = db_session.exec(
        select(Task).where(Task.user_id == user1.id)
    ).all()
    assert len(user1_tasks) == 2
    assert all(task.user_id == user1.id for task in user1_tasks)

    # Query tasks for user2
    user2_tasks = db_session.exec(
        select(Task).where(Task.user_id == user2.id)
    ).all()
    assert len(user2_tasks) == 1
    assert user2_tasks[0].user_id == user2.id

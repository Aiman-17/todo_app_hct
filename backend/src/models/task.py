"""
Task SQLModel for todo items with user isolation.

Defines the tasks table schema with integer primary key, foreign key to users,
and composite index for optimized default sort query.
"""
from sqlmodel import SQLModel, Field, Index, Column
from pydantic import ConfigDict
from sqlalchemy import JSON
from datetime import datetime, timezone
from uuid import UUID
from typing import Optional, List, Dict, Any
from enum import Enum


class TaskPriority(str, Enum):
    """Task priority levels."""
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Task(SQLModel, table=True):
    """
    Task model representing a todo item owned by a user.

    Attributes:
        id: Unique integer identifier (auto-increment)
        user_id: UUID of the owning user (foreign key to users.id, indexed)
        title: Task title (max 200 characters)
        description: Optional task description (max 2000 characters)
        completed: Completion status (default False)
        priority: Task priority level (high/medium/low, default medium)
        due_date: Optional due date (nullable datetime)
        tags: Optional list of tags (JSON array)
        recurrence_rule: Optional recurrence configuration (JSON object)
        created_at: Task creation timestamp (UTC)
        updated_at: Last modification timestamp (UTC)
        deleted_at: Soft delete timestamp (NULL if not deleted, UTC datetime if deleted)

    Indexes:
        - Primary key on id
        - Foreign key index on user_id
        - Composite index on (user_id, completed, created_at DESC)
          for optimized default sort query (incomplete first, newest first)

    Example:
        task = Task(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            title="Buy groceries",
            description="Milk, eggs, bread",
            completed=False,
            priority=TaskPriority.HIGH,
            due_date=datetime(2025, 12, 31, 23, 59, 59),
            tags=["shopping", "urgent"]
        )
    """

    __tablename__ = "tasks"
    __table_args__ = (
        Index(
            "ix_tasks_user_completed_created",
            "user_id",
            "completed",
            "created_at",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    title: str = Field(max_length=200, nullable=False)
    description: Optional[str] = Field(default="", max_length=2000)
    completed: bool = Field(default=False, nullable=False)
    priority: TaskPriority = Field(default=TaskPriority.MEDIUM, nullable=False)
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    tags: Optional[List[str]] = Field(default=None, sa_column=Column(JSON))
    recurrence_rule: Optional[Dict[str, Any]] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": "550e8400-e29b-41d4-a716-446655440000",
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "priority": "high",
                "due_date": "2025-12-31T23:59:59Z",
                "tags": ["shopping", "urgent"],
                "recurrence_rule": {"frequency": "weekly", "interval": 1},
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
    )

"""
Pydantic schemas for task API requests and responses.

Provides validation for task creation, updates, and response payloads.
"""
from pydantic import BaseModel, field_validator, ConfigDict
from datetime import datetime
from typing import Optional, List, Dict, Any
from src.models.task import TaskPriority


class TaskCreate(BaseModel):
    """
    Schema for task creation request.

    Validates title (required, max 200), description (optional, max 2000),
    priority (default: medium), due_date (optional), tags (optional),
    and recurrence_rule (optional).
    """

    title: str
    description: str = ""
    priority: TaskPriority = TaskPriority.MEDIUM
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    recurrence_rule: Optional[Dict[str, Any]] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title is non-empty and within length limits."""
        v = v.strip()
        if not v:
            raise ValueError("Title cannot be empty")
        if len(v) > 200:
            raise ValueError("Title too long (max 200 characters)")
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: str) -> str:
        """Validate description is within length limits."""
        if len(v) > 2000:
            raise ValueError("Description too long (max 2000 characters)")
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate tags list (max 10 tags, each max 50 characters)."""
        if v is not None:
            if len(v) > 10:
                raise ValueError("Maximum 10 tags allowed")
            for tag in v:
                if len(tag) > 50:
                    raise ValueError("Tag too long (max 50 characters)")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "priority": "high",
                "due_date": "2025-12-31T23:59:59Z",
                "tags": ["shopping", "urgent"],
                "recurrence_rule": {"frequency": "weekly", "interval": 1}
            }
        }
    )


class TaskUpdate(BaseModel):
    """
    Schema for task update request.

    All fields are optional (only update provided fields).
    """

    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[TaskPriority] = None
    due_date: Optional[datetime] = None
    tags: Optional[List[str]] = None
    recurrence_rule: Optional[Dict[str, Any]] = None

    @field_validator('title')
    @classmethod
    def validate_title(cls, v: Optional[str]) -> Optional[str]:
        """Validate title if provided."""
        if v is not None:
            v = v.strip()
            if not v:
                raise ValueError("Title cannot be empty")
            if len(v) > 200:
                raise ValueError("Title too long (max 200 characters)")
        return v

    @field_validator('description')
    @classmethod
    def validate_description(cls, v: Optional[str]) -> Optional[str]:
        """Validate description if provided."""
        if v is not None and len(v) > 2000:
            raise ValueError("Description too long (max 2000 characters)")
        return v

    @field_validator('tags')
    @classmethod
    def validate_tags(cls, v: Optional[List[str]]) -> Optional[List[str]]:
        """Validate tags list if provided."""
        if v is not None:
            if len(v) > 10:
                raise ValueError("Maximum 10 tags allowed")
            for tag in v:
                if len(tag) > 50:
                    raise ValueError("Tag too long (max 50 characters)")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "Buy groceries and snacks",
                "description": "Milk, eggs, bread, chips",
                "priority": "medium",
                "due_date": "2025-12-31T23:59:59Z",
                "tags": ["shopping"]
            }
        }
    )


class TaskResponse(BaseModel):
    """
    Schema for task response.

    Returns complete task information including timestamps and extended fields.
    """

    id: int
    title: str
    description: str
    completed: bool
    priority: TaskPriority
    due_date: Optional[datetime]
    tags: Optional[List[str]]
    recurrence_rule: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode for SQLModel → Pydantic conversion
        json_schema_extra={
            "example": {
                "id": 1,
                "title": "Buy groceries",
                "description": "Milk, eggs, bread",
                "completed": False,
                "priority": "high",
                "due_date": "2025-12-31T23:59:59Z",
                "tags": ["shopping", "urgent"],
                "recurrence_rule": {"frequency": "weekly", "interval": 1},
                "created_at": "2025-12-30T10:05:00Z",
                "updated_at": "2025-12-30T10:05:00Z"
            }
        }
    )

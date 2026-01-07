"""
User SQLModel for authentication and task ownership.

Defines the users table schema with UUID primary key, unique email index,
and bcrypt password hashing.
"""
from sqlmodel import SQLModel, Field
from pydantic import ConfigDict
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional


class User(SQLModel, table=True):
    """
    User model representing an authenticated user account.

    Attributes:
        id: Unique UUID identifier (auto-generated)
        email: Unique email address (used for login, indexed for fast lookup)
        name: User display name
        password_hash: bcrypt hashed password (NEVER store plaintext passwords)
        created_at: Account creation timestamp (UTC)
        updated_at: Last modification timestamp (UTC)

    Example:
        user = User(
            email="alice@example.com",
            name="Alice Smith",
            password_hash="$2b$12$KIXxLhFz7xFGVwPq7Z8ZYeQ5X..."
        )
    """

    __tablename__ = "users"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(max_length=255, unique=True, index=True, nullable=False)
    name: str = Field(max_length=255, nullable=False)
    password_hash: str = Field(max_length=255, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "alice@example.com",
                "name": "Alice Smith",
                "created_at": "2025-12-30T10:00:00Z",
                "updated_at": "2025-12-30T10:00:00Z"
            }
        }
    )

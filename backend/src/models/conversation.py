"""
Phase III: Conversation and Message SQLModels for AI chatbot persistence.

Defines conversation and message tables for storing chat history between
users and the AI assistant. Follows the same patterns as existing Phase II models.
"""
from sqlmodel import SQLModel, Field, Index
from pydantic import ConfigDict
from datetime import datetime, timezone
from uuid import UUID, uuid4
from typing import Optional
from enum import Enum


class MessageRole(str, Enum):
    """Message sender role (user or AI assistant)."""
    USER = "user"
    ASSISTANT = "assistant"


class Conversation(SQLModel, table=True):
    """
    Conversation model representing a chat thread between user and AI assistant.

    Attributes:
        id: Unique UUID identifier (auto-generated)
        user_id: UUID of the conversation owner (foreign key to users.id, indexed)
        created_at: Conversation creation timestamp (UTC)
        updated_at: Last message timestamp (UTC, updated on each new message)
        deleted_at: Soft delete timestamp (NULL if active, UTC datetime if deleted)

    Indexes:
        - Primary key on id
        - Composite index on (user_id, created_at DESC) for listing user conversations
        - Partial index on (user_id) WHERE deleted_at IS NULL for active conversations

    Example:
        conversation = Conversation(
            user_id=UUID("550e8400-e29b-41d4-a716-446655440000")
        )
    """

    __tablename__ = "conversations"
    __table_args__ = (
        Index(
            "ix_conversations_user_created",
            "user_id",
            "created_at",
        ),
        # Partial index for active (non-deleted) conversations
        Index(
            "idx_active_conversations",
            "user_id",
            postgresql_where="deleted_at IS NULL",
        ),
    )

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
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
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "created_at": "2026-01-13T10:30:00Z",
                "updated_at": "2026-01-13T10:35:00Z",
                "deleted_at": None
            }
        }
    )


class Message(SQLModel, table=True):
    """
    Message model representing individual chat messages within a conversation.

    Messages are append-only for audit trail purposes. Once created, messages
    should not be updated or deleted (soft delete only for exceptional cases).

    Attributes:
        id: Unique auto-incrementing message ID (bigserial)
        conversation_id: UUID of parent conversation (foreign key to conversations.id)
        user_id: UUID of message owner (foreign key to users.id, for isolation)
        role: Message sender role ('user' or 'assistant')
        content: Message text content (max 10,000 characters)
        created_at: Message creation timestamp (UTC)
        deleted_at: Soft delete timestamp (NULL if active, UTC datetime if deleted)

    Indexes:
        - Primary key on id
        - Composite index on (conversation_id, created_at ASC) for message ordering
        - Partial index on (conversation_id) WHERE deleted_at IS NULL for active messages

    Validation:
        - role must be 'user' or 'assistant'
        - content cannot be empty
        - content max length: 10,000 characters
        - user_id must match conversation's user_id (enforced in application layer)

    Example:
        message = Message(
            conversation_id=UUID("550e8400-e29b-41d4-a716-446655440000"),
            user_id=UUID("7c9e6679-7425-40de-944b-e07fc1f90ae7"),
            role=MessageRole.USER,
            content="Add a task to buy groceries"
        )
    """

    __tablename__ = "messages"
    __table_args__ = (
        Index(
            "ix_messages_conversation_created",
            "conversation_id",
            "created_at",
        ),
        # Partial index for active (non-deleted) messages
        Index(
            "idx_active_messages",
            "conversation_id",
            postgresql_where="deleted_at IS NULL",
        ),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", nullable=False, index=True)
    user_id: UUID = Field(foreign_key="users.id", nullable=False, index=True)
    role: str = Field(nullable=False, max_length=20)  # 'user' or 'assistant' - validated by DB check constraint
    content: str = Field(max_length=10000, nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    deleted_at: Optional[datetime] = Field(default=None, nullable=True)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "user_id": "7c9e6679-7425-40de-944b-e07fc1f90ae7",
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-01-13T10:30:00Z",
                "deleted_at": None
            }
        }
    )

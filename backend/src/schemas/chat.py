"""
Phase III: Pydantic schemas for chat API requests and responses.

Defines request/response models for chatbot endpoints with validation.
"""
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from uuid import UUID
from datetime import datetime


class ChatRequest(BaseModel):
    """
    Request schema for POST /api/chat endpoint.

    Attributes:
        message: User's natural language message (max 10,000 characters)
        conversation_id: Optional UUID of existing conversation (None = new conversation)

    Example:
        {
            "message": "remind me to call mom tomorrow",
            "conversation_id": null
        }
    """

    message: str = Field(
        ...,
        min_length=1,
        max_length=10000,
        description="User's natural language message",
        examples=["remind me to call mom tomorrow", "show my tasks", "mark task 5 as done"]
    )
    conversation_id: Optional[UUID] = Field(
        default=None,
        description="UUID of existing conversation (null for new conversation)",
        examples=[None, "550e8400-e29b-41d4-a716-446655440000"]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "message": "add a high priority task to buy groceries",
                "conversation_id": None
            }
        }
    )


class ChatResponse(BaseModel):
    """
    Response schema for POST /api/chat endpoint.

    Attributes:
        response: Assistant's natural language response
        conversation_id: UUID of the conversation
        intent: Classified intent (for debugging/metrics)
        success: Whether the operation succeeded
        correlation_id: Correlation ID for distributed tracing

    Example:
        {
            "response": "✓ Created task: 'Buy groceries' (ID: 42).",
            "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
            "intent": "create_task",
            "success": true,
            "correlation_id": "abc123"
        }
    """

    response: str = Field(
        ...,
        description="Assistant's natural language response",
        examples=["✓ Created task: 'Buy groceries' (ID: 42). I've added it to your list!"]
    )
    conversation_id: UUID = Field(
        ...,
        description="UUID of the conversation",
        examples=["550e8400-e29b-41d4-a716-446655440000"]
    )
    intent: str = Field(
        ...,
        description="Classified intent (create_task, list_tasks, etc.)",
        examples=["create_task", "list_tasks", "complete_task", "unclear"]
    )
    success: bool = Field(
        ...,
        description="Whether the operation succeeded",
        examples=[True, False]
    )
    correlation_id: str = Field(
        ...,
        description="Correlation ID for request tracing",
        examples=["abc123-def456-ghi789"]
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "response": "✓ Created task: 'Buy groceries' (ID: 42). Marked as high priority.",
                "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
                "intent": "create_task",
                "success": True,
                "correlation_id": "abc123-def456"
            }
        }
    )


class ConversationResponse(BaseModel):
    """
    Response schema for GET /api/conversations endpoint.

    Attributes:
        id: Conversation UUID
        created_at: Conversation creation timestamp
        updated_at: Last message timestamp
        message_count: Number of messages in conversation

    Example:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2026-01-14T10:30:00Z",
            "updated_at": "2026-01-14T10:35:00Z",
            "message_count": 4
        }
    """

    id: UUID
    created_at: datetime
    updated_at: datetime
    message_count: int = Field(ge=0, description="Number of messages in conversation")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "created_at": "2026-01-14T10:30:00.000Z",
                "updated_at": "2026-01-14T10:35:00.000Z",
                "message_count": 4
            }
        }
    )


class MessageResponse(BaseModel):
    """
    Response schema for messages in GET /api/conversations/{id}/messages endpoint.

    Attributes:
        id: Message ID
        role: Message sender role (user or assistant)
        content: Message text content
        created_at: Message creation timestamp

    Example:
        {
            "id": 1,
            "role": "user",
            "content": "Add a task to buy groceries",
            "created_at": "2026-01-14T10:30:00Z"
        }
    """

    id: int
    role: str = Field(..., pattern="^(user|assistant)$", description="Message sender role")
    content: str = Field(..., description="Message text content")
    created_at: datetime

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "id": 1,
                "role": "user",
                "content": "Add a task to buy groceries",
                "created_at": "2026-01-14T10:30:00.000Z"
            }
        }
    )

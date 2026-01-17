"""
Phase III: Conversation API routes for managing chat history.

Provides endpoints to list conversations and retrieve message history.
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select, func
from uuid import UUID
from typing import List
import logging

from src.schemas.chat import ConversationResponse, MessageResponse
from src.dependencies import get_db_session, get_current_user
from src.models.user import User
from src.models.conversation import Conversation, Message

logger = logging.getLogger("mcp_tools")

# Create router with /api prefix and conversations tag
router = APIRouter(prefix="/api", tags=["conversations"])


@router.get("/conversations", response_model=List[ConversationResponse], status_code=status.HTTP_200_OK)
async def list_conversations(
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    limit: int = 50
) -> List[ConversationResponse]:
    """
    List all conversations for the authenticated user (most recent first).

    **Authentication**: Requires valid JWT token in Authorization header.

    **Query Parameters**:
    - limit: Maximum number of conversations to return (default: 50, max: 200)

    **Example Response**:
    ```json
    [
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "created_at": "2026-01-14T10:30:00Z",
            "updated_at": "2026-01-14T10:35:00Z",
            "message_count": 4
        }
    ]
    ```

    **Error Responses**:
    - 401: Invalid or missing JWT token
    - 500: Internal server error
    """
    try:
        # Enforce limit cap
        limit = min(limit, 200)

        # Query conversations for user (exclude soft-deleted)
        statement = select(Conversation).where(
            Conversation.user_id == current_user.id,
            Conversation.deleted_at.is_(None)
        ).order_by(Conversation.updated_at.desc()).limit(limit)

        conversations = db.exec(statement).all()

        # Count messages for each conversation
        results = []
        for conversation in conversations:
            # Count messages (exclude soft-deleted)
            message_count_stmt = select(func.count(Message.id)).where(
                Message.conversation_id == conversation.id,
                Message.deleted_at.is_(None)
            )
            message_count = db.exec(message_count_stmt).first() or 0

            results.append(
                ConversationResponse(
                    id=conversation.id,
                    created_at=conversation.created_at,
                    updated_at=conversation.updated_at,
                    message_count=message_count
                )
            )

        logger.info(
            "Conversations endpoint: listed conversations",
            extra={
                "user_id": str(current_user.id),
                "count": len(results)
            }
        )

        return results

    except Exception as e:
        logger.error(
            "Conversations endpoint: failed to list conversations",
            extra={"user_id": str(current_user.id), "error": str(e)},
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve conversations"
        )


@router.get("/conversations/{conversation_id}/messages", response_model=List[MessageResponse], status_code=status.HTTP_200_OK)
async def get_conversation_messages(
    conversation_id: UUID,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    limit: int = 100
) -> List[MessageResponse]:
    """
    Retrieve all messages in a conversation (chronological order).

    **Authentication**: Requires valid JWT token in Authorization header.

    **Path Parameters**:
    - conversation_id: UUID of the conversation

    **Query Parameters**:
    - limit: Maximum number of messages to return (default: 100, max: 1000)

    **Example Response**:
    ```json
    [
        {
            "id": 1,
            "role": "user",
            "content": "Add a task to buy groceries",
            "created_at": "2026-01-14T10:30:00Z"
        },
        {
            "id": 2,
            "role": "assistant",
            "content": "✓ Created task: 'Buy groceries' (ID: 42).",
            "created_at": "2026-01-14T10:30:02Z"
        }
    ]
    ```

    **Error Responses**:
    - 401: Invalid or missing JWT token
    - 404: Conversation not found or does not belong to user
    - 500: Internal server error
    """
    try:
        # Enforce limit cap
        limit = min(limit, 1000)

        # Verify conversation exists and belongs to user
        conversation_stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user.id,
            Conversation.deleted_at.is_(None)
        )
        conversation = db.exec(conversation_stmt).first()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )

        # Query messages (exclude soft-deleted)
        messages_stmt = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.deleted_at.is_(None)
        ).order_by(Message.created_at.asc()).limit(limit)

        messages = db.exec(messages_stmt).all()

        # Convert to response schema
        results = [
            MessageResponse(
                id=msg.id,
                role=msg.role.value,
                content=msg.content,
                created_at=msg.created_at
            )
            for msg in messages
        ]

        logger.info(
            "Messages endpoint: retrieved messages",
            extra={
                "user_id": str(current_user.id),
                "conversation_id": str(conversation_id),
                "count": len(results)
            }
        )

        return results

    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            "Messages endpoint: failed to retrieve messages",
            extra={
                "user_id": str(current_user.id),
                "conversation_id": str(conversation_id),
                "error": str(e)
            },
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve messages"
        )

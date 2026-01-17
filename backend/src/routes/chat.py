"""
Phase III: Chat API route for POST /api/chat endpoint.

Handles chatbot interactions with JWT authentication and conversation management.
"""
from fastapi import APIRouter, Depends, HTTPException, status, Header
from sqlmodel import Session
from uuid import uuid4
from typing import Optional
import logging
import time

from src.schemas.chat import ChatRequest, ChatResponse
from src.dependencies import get_db_session, get_current_user
from src.models.user import User
from src.services.chatbot_service import ChatbotService
from src.middleware.rate_limiter import check_rate_limit

logger = logging.getLogger("mcp_tools")

# Create router with /api prefix and chat tag
router = APIRouter(prefix="/api", tags=["chat"])

# Initialize chatbot service (singleton)
chatbot_service = ChatbotService()


@router.post("/chat", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(
    request: ChatRequest,
    db: Session = Depends(get_db_session),
    current_user: User = Depends(get_current_user)
) -> ChatResponse:
    """
    Process natural language chat message and return AI assistant response.

    **Authentication**: Requires valid JWT token in Authorization header.

    **Flow**:
    1. Extract user_id from JWT token
    2. Generate correlation ID for distributed tracing
    3. Process message through agent pipeline (Intent → Resolution → Action → Format)
    4. Save conversation to database
    5. Return natural language response

    **Example Request**:
    ```json
    {
        "message": "remind me to call mom tomorrow",
        "conversation_id": null
    }
    ```

    **Example Response**:
    ```json
    {
        "response": "✓ Created task: 'call mom' (ID: 42). Due: 2026-01-15.",
        "conversation_id": "550e8400-e29b-41d4-a716-446655440000",
        "intent": "create_task",
        "success": true,
        "correlation_id": "abc123-def456"
    }
    ```

    **Supported Commands**:
    - Create task: "add a task to [name]", "remind me to [name]"
    - List tasks: "show my tasks", "what do I need to do", "list tasks"
    - Complete task: "mark task [id] as done", "complete task [id]"
    - Delete task: "delete task [id]", "remove task [id]"
    - Update task: "update task [id] to [new title]"

    **Error Responses**:
    - 401: Invalid or missing JWT token
    - 500: Internal server error
    """
    start_time = time.time()

    # Generate correlation ID for request tracing
    correlation_id = str(uuid4())

    # Check rate limit (100 requests per hour per user)
    from fastapi import Request
    # Note: In real implementation, inject Request dependency
    # For now, pass user_id directly
    user_id_str = str(current_user.id)
    from src.middleware.rate_limiter import chat_rate_limiter
    if not chat_rate_limiter.is_allowed(user_id_str):
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": "You have exceeded the rate limit of 100 requests per hour. Please try again later.",
                "limit": 100,
                "remaining": chat_rate_limiter.get_remaining(user_id_str)
            }
        )

    try:
        # Log incoming request
        logger.info(
            "Chat endpoint: received request",
            extra={
                "user_id": str(current_user.id),
                "conversation_id": str(request.conversation_id) if request.conversation_id else "new",
                "message_length": len(request.message),
                "correlation_id": correlation_id
            }
        )

        # Process message through chatbot service
        result = chatbot_service.process_message(
            db=db,
            user_id=str(current_user.id),
            message=request.message,
            conversation_id=str(request.conversation_id) if request.conversation_id else None,
            correlation_id=correlation_id
        )

        # Calculate request latency
        latency_ms = (time.time() - start_time) * 1000

        logger.info(
            "Chat endpoint: request completed",
            extra={
                "user_id": str(current_user.id),
                "conversation_id": result["conversation_id"],
                "intent": result["intent"],
                "success": result["success"],
                "latency_ms": latency_ms,
                "correlation_id": correlation_id
            }
        )

        # Return response
        return ChatResponse(
            response=result["response"],
            conversation_id=result["conversation_id"],
            intent=result["intent"],
            success=result["success"],
            correlation_id=correlation_id
        )

    except Exception as e:
        logger.error(
            "Chat endpoint: request failed",
            extra={
                "user_id": str(current_user.id),
                "error": str(e),
                "correlation_id": correlation_id
            },
            exc_info=True
        )
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat message. Please try again."
        )

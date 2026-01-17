"""
Phase III: Chatbot Service for orchestrating AI agents and conversation management.

Coordinates the 4-agent pipeline: Intent → Resolution → Action → Formatter.
Manages conversation state persistence in database.
"""
from typing import Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone
import logging
from sqlmodel import Session, select

from src.models.conversation import Conversation, Message, MessageRole
from src.agents.intent_classifier import IntentClassifierAgent
from src.agents.task_resolution import TaskResolutionAgent
from src.agents.action_agent import ActionAgent
from src.agents.response_formatter import ResponseFormatterAgent

logger = logging.getLogger("mcp_tools")


class ChatbotService:
    """
    Service that orchestrates the chatbot conversation flow.

    Architecture (Stateless):
    1. Load conversation context from DB (if conversation_id provided)
    2. IntentClassifierAgent: Parse user message → intent + entities
    3. TaskResolutionAgent: Resolve task references (if needed)
    4. ActionAgent: Execute MCP tool operation
    5. ResponseFormatterAgent: Format response → natural language
    6. Save user message + assistant response to DB
    7. Return response + conversation_id to frontend

    Example:
        >>> service = ChatbotService()
        >>> result = service.process_message(
        ...     db, user_id="user-123",
        ...     message="remind me to call mom",
        ...     conversation_id=None
        ... )
        >>> result["response"]
        "✓ Created task: 'call mom' (ID: 42). I've added it to your list!"
    """

    def __init__(self):
        """Initialize chatbot service with all 4 agents."""
        self.intent_agent = IntentClassifierAgent()
        self.resolution_agent = TaskResolutionAgent()
        self.action_agent = ActionAgent()
        self.formatter_agent = ResponseFormatterAgent()

    def process_message(
        self,
        db: Session,
        user_id: str,
        message: str,
        conversation_id: Optional[str] = None,
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process user message through agent pipeline and return response.

        Args:
            db: Database session
            user_id: User ID (from JWT - UUID string)
            message: User's natural language message
            conversation_id: Optional conversation ID (UUID string, None = new conversation)
            correlation_id: Optional correlation ID for distributed tracing

        Returns:
            dict: {
                "response": str,  # Natural language response
                "conversation_id": str,  # UUID string
                "intent": str,  # Classified intent
                "success": bool  # Whether operation succeeded
            }

        Example:
            >>> result = service.process_message(db, "user-123", "show my tasks")
            >>> result["response"]
            "You have 5 task(s):..."
            >>> result["success"]
            True
        """
        try:
            # Generate correlation ID if not provided
            if not correlation_id:
                correlation_id = str(uuid4())

            # Convert user_id to UUID
            user_uuid = UUID(user_id)

            # Step 1: Load or create conversation
            conversation = self._get_or_create_conversation(
                db, user_uuid, conversation_id, correlation_id
            )

            logger.info(
                "ChatbotService: processing message",
                extra={
                    "user_id": user_id,
                    "conversation_id": str(conversation.id),
                    "message_length": len(message),
                    "correlation_id": correlation_id
                }
            )

            # Step 2: Classify intent
            classification = self.intent_agent.classify(message, user_id, correlation_id)
            intent = classification.get("intent", "unclear")
            confidence = classification.get("confidence", 0.0)
            entities = classification.get("entities", {})

            logger.info(
                "ChatbotService: intent classified",
                extra={
                    "user_id": user_id,
                    "intent": intent,
                    "confidence": confidence,
                    "correlation_id": correlation_id
                }
            )

            # Handle low-confidence intents
            if confidence < 0.7:
                response_text = self._handle_low_confidence(message)
                self._save_messages(db, conversation, user_id, message, response_text, correlation_id)
                return {
                    "response": response_text,
                    "conversation_id": str(conversation.id),
                    "intent": "unclear",
                    "success": False
                }

            # Step 3: Resolve task references (if intent requires task ID)
            if intent in ["complete_task", "delete_task", "update_task"] and "task_id" not in entities:
                resolution = self.resolution_agent.resolve(db, user_id, entities, correlation_id)

                if resolution.get("confirmation_needed"):
                    # Multiple matches - ask user for clarification
                    response_text = self._format_confirmation_request(resolution.get("matches", []))
                    self._save_messages(db, conversation, user_id, message, response_text, correlation_id)
                    return {
                        "response": response_text,
                        "conversation_id": str(conversation.id),
                        "intent": intent,
                        "success": False,
                        "needs_confirmation": True
                    }

                if resolution.get("task_ids"):
                    # Single match found - use it
                    entities["task_id"] = resolution["task_ids"][0]
                elif resolution.get("error"):
                    # No match found
                    response_text = resolution["error"]
                    self._save_messages(db, conversation, user_id, message, response_text, correlation_id)
                    return {
                        "response": response_text,
                        "conversation_id": str(conversation.id),
                        "intent": intent,
                        "success": False
                    }

            # Step 4: Execute action via MCP tools
            tool_result = self.action_agent.execute(
                db, intent, entities, user_id, correlation_id
            )

            # Step 5: Format response
            response_text = self.formatter_agent.format(
                intent, tool_result, user_id, correlation_id
            )

            # Step 6: Save conversation messages
            self._save_messages(db, conversation, user_id, message, response_text, correlation_id)

            logger.info(
                "ChatbotService: message processed successfully",
                extra={
                    "user_id": user_id,
                    "conversation_id": str(conversation.id),
                    "intent": intent,
                    "tool_success": tool_result.get("success", False),
                    "correlation_id": correlation_id
                }
            )

            return {
                "response": response_text,
                "conversation_id": str(conversation.id),
                "intent": intent,
                "success": tool_result.get("success", False)
            }

        except Exception as e:
            logger.error(
                "ChatbotService: message processing failed",
                extra={"user_id": user_id, "error": str(e), "correlation_id": correlation_id or "none"},
                exc_info=True
            )
            return {
                "response": "I encountered an error while processing your message. Please try again.",
                "conversation_id": conversation_id or "error",
                "intent": "error",
                "success": False,
                "error": str(e)
            }

    def _get_or_create_conversation(
        self,
        db: Session,
        user_uuid: UUID,
        conversation_id: Optional[str],
        correlation_id: str
    ) -> Conversation:
        """Load existing conversation or create new one."""
        if conversation_id:
            # Load existing conversation
            conversation_uuid = UUID(conversation_id)
            statement = select(Conversation).where(
                Conversation.id == conversation_uuid,
                Conversation.user_id == user_uuid,
                Conversation.deleted_at.is_(None)
            )
            conversation = db.exec(statement).first()

            if conversation:
                # Update conversation timestamp
                conversation.updated_at = datetime.now(timezone.utc)
                db.add(conversation)
                db.commit()
                db.refresh(conversation)
                return conversation

            logger.warning(
                "ChatbotService: conversation not found, creating new",
                extra={"user_id": str(user_uuid), "conversation_id": conversation_id, "correlation_id": correlation_id}
            )

        # Create new conversation
        conversation = Conversation(user_id=user_uuid)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)

        logger.info(
            "ChatbotService: new conversation created",
            extra={"user_id": str(user_uuid), "conversation_id": str(conversation.id), "correlation_id": correlation_id}
        )

        return conversation

    def _save_messages(
        self,
        db: Session,
        conversation: Conversation,
        user_id: str,
        user_message: str,
        assistant_response: str,
        correlation_id: str
    ):
        """Save user message and assistant response to database."""
        user_uuid = UUID(user_id)

        # Save user message
        user_msg = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role=MessageRole.USER,
            content=user_message
        )
        db.add(user_msg)

        # Save assistant response
        assistant_msg = Message(
            conversation_id=conversation.id,
            user_id=user_uuid,
            role=MessageRole.ASSISTANT,
            content=assistant_response
        )
        db.add(assistant_msg)

        # Update conversation timestamp
        conversation.updated_at = datetime.now(timezone.utc)
        db.add(conversation)

        db.commit()

        logger.info(
            "ChatbotService: messages saved",
            extra={
                "user_id": user_id,
                "conversation_id": str(conversation.id),
                "correlation_id": correlation_id
            }
        )

    def _handle_low_confidence(self, message: str) -> str:
        """Generate response for low-confidence intent classification."""
        return (
            "I'm not sure what you want to do. Here are some things you can try:\n"
            "- 'add a task to [task name]' - Create a new task\n"
            "- 'show my tasks' - View all your tasks\n"
            "- 'mark task [number] as done' - Complete a task\n"
            "- 'delete task [number]' - Remove a task\n"
            "\nPlease rephrase your request."
        )

    def _format_confirmation_request(self, matches: list) -> str:
        """Format multiple task matches as confirmation request."""
        response_lines = ["I found multiple tasks matching your request. Which one did you mean?"]

        for i, match in enumerate(matches[:5], 1):  # Limit to 5 matches
            title = match.get("title", "Untitled")
            task_id = match.get("id", "?")
            response_lines.append(f"{i}. {title} (ID: {task_id})")

        response_lines.append("\nPlease specify the task ID (e.g., 'mark task 5 as done').")

        return "\n".join(response_lines)

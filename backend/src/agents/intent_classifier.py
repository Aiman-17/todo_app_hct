"""
Phase III: IntentClassifierAgent for natural language intent classification.

Parses user messages to extract intent and entities using OpenAI's API.
"""
from typing import Dict, Any
import json
import logging
import time
from openai import OpenAI
from openai import OpenAIError, RateLimitError, APIError

from src.config import settings

logger = logging.getLogger("mcp_tools")


class IntentClassifierAgent:
    """
    Agent that classifies user messages into intents and extracts entities.

    Responsibilities:
    - Parse user message into structured intent
    - Extract relevant entities (task title, due date, priority, etc.)
    - Return confidence score for intent classification
    - Handle low-confidence scenarios (< 0.7 threshold)

    Intents:
    - create_task: User wants to create a new task
    - list_tasks: User wants to view their tasks
    - update_task: User wants to modify an existing task
    - delete_task: User wants to delete a task
    - complete_task: User wants to mark a task as complete
    - unclear: Intent cannot be determined with confidence

    Example:
        >>> agent = IntentClassifierAgent()
        >>> result = agent.classify("remind me to call mom tomorrow")
        >>> result["intent"]
        'create_task'
        >>> result["entities"]["title"]
        'call mom'
    """

    def __init__(self):
        """Initialize OpenAI client with API key."""
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = "gpt-4o-mini"  # Use GPT-4o-mini for cost-effective intent classification
        self.confidence_threshold = 0.7

    def classify(self, message: str, user_id: str = None, correlation_id: str = None) -> Dict[str, Any]:
        """
        Classify user message into intent and extract entities.

        Args:
            message: User's natural language message
            user_id: Optional user ID for logging
            correlation_id: Optional correlation ID for tracing

        Returns:
            dict: {
                "intent": str,  # create_task, list_tasks, update_task, delete_task, complete_task, unclear
                "confidence": float,  # 0.0 to 1.0
                "entities": dict  # Extracted entities (title, priority, due_date, task_id, etc.)
            }

        Example:
            >>> result = agent.classify("add a high priority task to buy groceries")
            >>> result
            {
                "intent": "create_task",
                "confidence": 0.95,
                "entities": {
                    "title": "buy groceries",
                    "priority": "high"
                }
            }
        """
        # Retry configuration (as per spec: 1 retry with 500ms delay)
        max_retries = 1
        retry_delay = 0.5  # 500ms
        last_error = None

        for attempt in range(max_retries + 1):
            try:
                # System prompt defining intent classification task
                system_prompt = """You are an intent classification assistant for a todo application.

Classify user messages into one of these intents:
- create_task: User wants to create a new task
- list_tasks: User wants to view their tasks (show, list, display)
- update_task: User wants to modify an existing task
- delete_task: User wants to delete/remove a task
- complete_task: User wants to mark a task as done/complete
- unclear: Intent cannot be determined

Extract relevant entities:
- title: Task title/description
- priority: high, medium, or low
- due_date: Date/time mentioned (in ISO format if possible)
- task_id: Numeric task ID if mentioned (e.g., "task 5", "number 3")
- task_reference: Text reference to a task (e.g., "the grocery one", "first task")
- completed: true/false for completion status
- tags: List of tags mentioned

Return JSON only:
{
    "intent": "intent_name",
    "confidence": 0.0-1.0,
    "entities": {}
}

Confidence scoring:
- 1.0: Extremely clear intent with explicit keywords
- 0.7-0.9: Clear intent, may need minor clarification
- 0.4-0.6: Ambiguous, needs user confirmation
- 0.0-0.3: Unclear, cannot determine intent

Examples:
"remind me to call mom" -> {"intent": "create_task", "confidence": 0.95, "entities": {"title": "call mom"}}
"show my tasks" -> {"intent": "list_tasks", "confidence": 1.0, "entities": {}}
"mark task 5 as done" -> {"intent": "complete_task", "confidence": 0.98, "entities": {"task_id": 5}}
"do the thing" -> {"intent": "unclear", "confidence": 0.2, "entities": {}}"""

                # Call OpenAI API
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": message}
                    ],
                    temperature=0.3,  # Lower temperature for consistent classification
                    max_tokens=300,
                    response_format={"type": "json_object"}  # Ensure JSON response
                )

                # Parse response
                result_text = response.choices[0].message.content
                result = json.loads(result_text)

                # Log classification
                logger.info(
                    "IntentClassifierAgent: classified message",
                    extra={
                        "user_id": user_id or "unknown",
                        "correlation_id": correlation_id or "none",
                        "intent": result.get("intent"),
                        "confidence": result.get("confidence"),
                        "message_length": len(message)
                    }
                )

                # Validate confidence threshold
                if result.get("confidence", 0) < self.confidence_threshold:
                    logger.warning(
                        "IntentClassifierAgent: low confidence",
                        extra={
                            "user_id": user_id or "unknown",
                            "correlation_id": correlation_id or "none",
                            "confidence": result.get("confidence"),
                            "threshold": self.confidence_threshold
                        }
                    )

                return result

            except (RateLimitError, APIError, OpenAIError) as e:
                last_error = e
                if attempt < max_retries:
                    logger.warning(
                        f"IntentClassifierAgent: OpenAI API error (attempt {attempt + 1}/{max_retries + 1}), retrying in {retry_delay}s",
                        extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none", "error": str(e)}
                    )
                    time.sleep(retry_delay)
                    continue
                else:
                    logger.error(
                        "IntentClassifierAgent: OpenAI API failed after retries",
                        extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none", "error": str(e)},
                        exc_info=True
                    )
                    return {
                        "intent": "unclear",
                        "confidence": 0.0,
                        "entities": {},
                        "error": f"OpenAI API unavailable: {str(e)}"
                    }

            except json.JSONDecodeError as e:
                logger.error(
                    "IntentClassifierAgent: JSON parse error",
                    extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none", "error": str(e)},
                    exc_info=True
                )
                return {
                    "intent": "unclear",
                    "confidence": 0.0,
                    "entities": {},
                    "error": "Failed to parse classification response"
                }

            except Exception as e:
                logger.error(
                    "IntentClassifierAgent: classification failed",
                    extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none", "error": str(e)},
                    exc_info=True
                )
                return {
                    "intent": "unclear",
                    "confidence": 0.0,
                    "entities": {},
                    "error": str(e)
                }

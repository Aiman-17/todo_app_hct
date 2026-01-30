"""
Phase III: IntentClassifierAgent for natural language intent classification.

Parses user messages to extract intent and entities using Google Gemini API.
"""
from typing import Dict, Any, List, Optional
import json
import logging
import time
import google.generativeai as genai

from src.config import settings
from src.agents.rule_based_classifier import RuleBasedClassifier

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
        """Initialize Gemini client with API key and rule-based fallback."""
        genai.configure(api_key=settings.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-2.0-flash-lite')  # Use Gemini 2.0 Flash Lite (higher free tier quota)
        self.confidence_threshold = 0.7
        self.fallback_classifier = RuleBasedClassifier()  # Fallback when Gemini fails

    def classify(self, message: str, user_id: str = None, correlation_id: str = None, conversation_history: Optional[List] = None) -> Dict[str, Any]:
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
                system_prompt = """You are a friendly, understanding AI assistant for todo management.

PERSONALITY:
- Be conversational and helpful
- Understand typos and informal language
- Users make mistakes - interpret intent, not exact spelling

TYPO EXAMPLES:
- "mkr tsk 5 complet" → mark task 5 complete
- "shw my tsks" → show my tasks
- "ad tsk buy milk" → add task buy milk
- "dlete teh first one" → delete the first task

Classify user messages into one of these intents:
- create_task: User wants to create a new task
- list_tasks: User wants to view their tasks (show, list, display, view)
- update_task: User wants to modify an existing task
- delete_task: User wants to delete/remove a task (single or batch)
- complete_task: User wants to mark a task as done/complete
- unclear: Intent cannot be determined

Extract relevant entities:
- title: Task title/description
- priority: high, medium, or low
- due_date: Date/time mentioned (in ISO format if possible)
- task_id: Numeric task ID if mentioned in ANY format:
  * "task 5" → 5
  * "id 20" → 20
  * "task id20" → 20
  * "number 3" → 3
  * "#42" → 42
  * "id20" → 20
- task_reference: Text reference to a task (e.g., "the grocery one", "first task", "it", "that")
- completed: true/false for completion status (use for filtering in list_tasks or batch delete)
- tags: List of tags mentioned
- filter_completed: true if user wants to filter by completed status (e.g., "completed tasks", "done tasks")

CONTEXT AWARENESS:
If conversation_history is provided and user says "it", "that", "the one", etc.,
check recent messages for task references.

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
"view tasks" -> {"intent": "list_tasks", "confidence": 1.0, "entities": {}}
"mark task 5 as done" -> {"intent": "complete_task", "confidence": 0.98, "entities": {"task_id": 5}}
"mark id 20" -> {"intent": "complete_task", "confidence": 0.95, "entities": {"task_id": 20}}
"mark task id20" -> {"intent": "complete_task", "confidence": 0.95, "entities": {"task_id": 20}}
"marks id 20 tasks as completed" -> {"intent": "complete_task", "confidence": 0.95, "entities": {"task_id": 20}}
"delete completed tasks" -> {"intent": "list_tasks", "confidence": 0.9, "entities": {"filter_completed": true}, "note": "User wants completed tasks, likely to delete them - show list first"}
"delete all done tasks" -> {"intent": "list_tasks", "confidence": 0.9, "entities": {"filter_completed": true}}
"delete id4" -> {"intent": "delete_task", "confidence": 0.98, "entities": {"task_id": 4}}
"delete aaa" -> {"intent": "delete_task", "confidence": 0.95, "entities": {"task_reference": "aaa"}}
"what you updated in do chat page update task?" -> {"intent": "list_tasks", "confidence": 0.8, "entities": {"task_reference": "do chat page update"}, "note": "User wants to see task details"}
"update do chat page update task" -> {"intent": "update_task", "confidence": 0.85, "entities": {"task_reference": "do chat page update"}}
"hey" -> {"intent": "unclear", "confidence": 0.1, "entities": {}}
"h" -> {"intent": "unclear", "confidence": 0.1, "entities": {}}
"mark it complete" (after creating task) -> {"intent": "complete_task", "confidence": 0.85, "entities": {"task_reference": "it"}}"""

                # Build conversation context for Gemini
                conversation_content = system_prompt + "\n\n"

                # Add conversation history for context
                if conversation_history:
                    conversation_content += "RECENT CONVERSATION:\n"
                    for msg in conversation_history[-10:]:  # Last 10 messages for context
                        role = "User" if msg.role == "user" else "Assistant"
                        conversation_content += f"{role}: {msg.content}\n"
                    conversation_content += "\n"

                conversation_content += f"CURRENT USER MESSAGE: {message}\n\nRespond with JSON only."

                # Call Gemini API
                response = self.model.generate_content(
                    conversation_content,
                    generation_config=genai.types.GenerationConfig(
                        temperature=0.3,  # Lower temperature for consistent classification
                        max_output_tokens=300,
                    )
                )

                # Parse response
                result_text = response.text

                # Clean up response (Gemini sometimes adds markdown)
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()

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

            except Exception as api_error:
                # Catch Gemini API errors (rate limits, network issues, etc.)
                if "ResourceExhausted" in str(api_error) or "429" in str(api_error) or "quota" in str(api_error).lower():
                    last_error = api_error
                    if attempt < max_retries:
                        logger.warning(
                            f"IntentClassifierAgent: Gemini API rate limit (attempt {attempt + 1}/{max_retries + 1}), retrying in {retry_delay}s",
                            extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none", "error": str(api_error)}
                        )
                        time.sleep(retry_delay)
                        continue
                    else:
                        # Quota exceeded - use rule-based fallback
                        logger.warning(
                            "IntentClassifierAgent: Gemini API quota exceeded, using rule-based fallback",
                            extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none"}
                        )
                        return self.fallback_classifier.classify(message, user_id, correlation_id, conversation_history)
                else:
                    # Other API errors - use rule-based fallback
                    logger.error(
                        "IntentClassifierAgent: Gemini API error, using rule-based fallback",
                        extra={"user_id": user_id or "unknown", "correlation_id": correlation_id or "none", "error": str(api_error)},
                        exc_info=True
                    )
                    return self.fallback_classifier.classify(message, user_id, correlation_id, conversation_history)

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

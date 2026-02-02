"""
Phase III: ResponseFormatterAgent for converting tool outputs to natural language.

Formats MCP tool execution results into user-friendly conversational responses.
"""
from typing import Dict, Any
import logging

logger = logging.getLogger("mcp_tools")


class ResponseFormatterAgent:
    """
    Agent that formats MCP tool outputs into natural language responses.

    Responsibilities:
    - Convert tool output JSON to conversational text
    - Handle success and error cases gracefully
    - Format task lists as readable bullet points
    - Be concise and user-friendly

    Example:
        >>> agent = ResponseFormatterAgent()
        >>> tool_result = {"success": True, "task": {"id": 42, "title": "Buy milk"}}
        >>> response = agent.format("create_task", tool_result)
        >>> response
        "✓ Created task: 'Buy milk' (ID: 42). I've added it to your list!"
    """

    def __init__(self):
        """Initialize response formatter agent."""
        self.urdu_templates = self._get_urdu_templates()

    def _get_urdu_templates(self) -> Dict[str, Dict[str, str]]:
        """Get Urdu response templates."""
        return {
            "create_task": {
                "success": "✓ کام بن گیا: '{title}' (آئی ڈی: {task_id})۔",
                "high_priority": " اہم کام کے طور پر نشان زد کیا۔",
                "due_date": " مقررہ تاریخ: {due_date}۔"
            },
            "list_tasks": {
                "header": "آپ کے پاس {count} کام ہیں:",
                "no_tasks": "ابھی آپ کے پاس کوئی کام نہیں ہے۔ 'کام شامل کریں' کہہ کر نیا کام بنائیں۔",
                "more_tasks": "...اور {count} مزید کام۔"
            },
            "complete_task": {
                "completed": "✓ '{title}' مکمل کے طور پر نشان زد کیا۔ بہت خوب! 🎉",
                "uncompleted": "○ '{title}' نامکمل کے طور پر نشان زد کیا۔"
            },
            "delete_task": {
                "success": "✓ کام کامیابی سے حذف ہو گیا۔ آپ کی فہرست سے ہٹا دیا گیا۔",
                "batch_success": "✓ کامیابی سے {count} مکمل کام حذف کیے۔",
                "no_completed": "حذف کرنے کے لیے کوئی مکمل کام نہیں ملا۔ آپ کی فہرست صاف ہے!"
            },
            "update_task": {
                "success": "✓ کام '{title}' کامیابی سے اپ ڈیٹ ہوا۔"
            },
            "errors": {
                "not_found": "میں وہ کام نہیں ڈھونڈ سکا۔ 'میرے کام دکھائیں' کہہ کر اپنی فہرست دیکھیں۔",
                "title_required": "کام کا عنوان ضروری ہے۔ کوشش کریں: 'کام شامل کریں [کام کا نام]'۔",
                "generic": "ایک مسئلہ پیش آیا: {error}۔ براہ کرم دوبارہ کوشش کریں۔"
            }
        }

    def format(
        self,
        intent: str,
        tool_result: Dict[str, Any],
        user_id: str = None,
        correlation_id: str = None,
        language: str = "en"
    ) -> str:
        """
        Format tool execution result into natural language response.

        Args:
            intent: The intent that was executed
            tool_result: MCP tool execution result
            user_id: Optional user ID for logging
            correlation_id: Optional correlation ID for tracing

        Returns:
            str: Natural language response to user

        Example:
            >>> agent.format("create_task", {"success": True, "task": {"id": 5, "title": "Call mom"}})
            "✓ Created task: 'Call mom' (ID: 5). I've added it to your list!"
        """
        try:
            # Handle tool failures
            if not tool_result.get("success"):
                error_msg = tool_result.get("error", "An unknown error occurred")
                logger.warning(
                    "ResponseFormatterAgent: formatting error response",
                    extra={"user_id": user_id or "unknown", "intent": intent, "error": error_msg, "correlation_id": correlation_id or "none"}
                )
                return self._format_error(intent, error_msg, language)

            # Route to intent-specific formatter
            if intent == "create_task":
                return self._format_create_task(tool_result, language)

            elif intent == "list_tasks":
                return self._format_list_tasks(tool_result, language)

            elif intent == "complete_task":
                return self._format_complete_task(tool_result, language)

            elif intent == "delete_task":
                return self._format_delete_task(tool_result, language)

            elif intent == "update_task":
                return self._format_update_task(tool_result, language)

            else:
                logger.warning(
                    "ResponseFormatterAgent: unknown intent for formatting",
                    extra={"user_id": user_id or "unknown", "intent": intent, "correlation_id": correlation_id or "none"}
                )
                return "I processed your request, but I'm not sure how to describe what happened."

        except Exception as e:
            logger.error(
                "ResponseFormatterAgent: formatting failed",
                extra={"user_id": user_id or "unknown", "intent": intent, "error": str(e), "correlation_id": correlation_id or "none"},
                exc_info=True
            )
            return f"Something went wrong while processing your request: {str(e)}"

    def _format_create_task(self, result: Dict, language: str = "en") -> str:
        """Format create_task result."""
        task = result.get("task", {})
        title = task.get("title", "Untitled")
        task_id = task.get("id", "?")
        priority = task.get("priority", "medium")

        if language == "ur":
            templates = self.urdu_templates["create_task"]
            response = templates["success"].format(title=title, task_id=task_id)

            if priority == "high":
                response += templates["high_priority"]

            if task.get("due_date"):
                due_date = task['due_date'].split('T')[0]
                response += templates["due_date"].format(due_date=due_date)
        else:
            response = f"✓ Created task: '{title}' (ID: {task_id})."

            if priority == "high":
                response += " Marked as high priority."

            if task.get("due_date"):
                response += f" Due: {task['due_date'].split('T')[0]}."

        return response

    def _format_list_tasks(self, result: Dict, language: str = "en") -> str:
        """Format list_tasks result."""
        tasks = result.get("tasks", [])

        if not tasks:
            if language == "ur":
                return self.urdu_templates["list_tasks"]["no_tasks"]
            return "You don't have any tasks yet. Try creating one by saying 'add a task to...'."

        # Format as bullet list
        if language == "ur":
            templates = self.urdu_templates["list_tasks"]
            response_lines = [templates["header"].format(count=len(tasks))]
        else:
            response_lines = [f"You have {len(tasks)} task(s):"]

        for i, task in enumerate(tasks[:10], 1):  # Limit to 10 tasks in chat
            title = task.get("title", "Untitled")
            task_id = task.get("id", "?")
            completed = task.get("completed", False)
            status_icon = "✓" if completed else "○"

            line = f"{i}. [{status_icon}] {title} (ID: {task_id})"

            # Add priority indicator
            priority = task.get("priority")
            if priority == "high":
                line += " 🔴"
            elif priority == "low":
                line += " 🟢"

            response_lines.append(line)

        if len(tasks) > 10:
            if language == "ur":
                templates = self.urdu_templates["list_tasks"]
                response_lines.append(templates["more_tasks"].format(count=len(tasks) - 10))
            else:
                response_lines.append(f"...and {len(tasks) - 10} more tasks.")

        return "\n".join(response_lines)

    def _format_complete_task(self, result: Dict, language: str = "en") -> str:
        """Format complete_task result."""
        task = result.get("task", {})
        title = task.get("title", "Untitled")
        completed = task.get("completed", False)

        if language == "ur":
            templates = self.urdu_templates["complete_task"]
            if completed:
                return templates["completed"].format(title=title)
            else:
                return templates["uncompleted"].format(title=title)
        else:
            if completed:
                return f"✓ Marked '{title}' as complete. Great job! 🎉"
            else:
                return f"○ Unmarked '{title}' as complete."

    def _format_delete_task(self, result: Dict, language: str = "en") -> str:
        """Format delete_task result (single or batch)."""
        # Check if this is a batch delete
        if "deleted_count" in result:
            deleted_count = result.get("deleted_count", 0)
            failed_count = result.get("failed_count", 0)

            if language == "ur":
                templates = self.urdu_templates["delete_task"]
                if deleted_count == 0:
                    return templates["no_completed"]
                return templates["batch_success"].format(count=deleted_count)
            else:
                if deleted_count == 0:
                    return "No completed tasks found to delete. Your task list is clean!"

                response = f"✓ Successfully deleted {deleted_count} completed task(s)."
                if failed_count > 0:
                    response += f" ({failed_count} task(s) failed to delete)"

                return response

        # Single task deletion
        if language == "ur":
            return self.urdu_templates["delete_task"]["success"]
        return "✓ Task deleted successfully. It's been removed from your list."

    def _format_update_task(self, result: Dict, language: str = "en") -> str:
        """Format update_task result."""
        task = result.get("task", {})
        title = task.get("title", "Untitled")

        if language == "ur":
            return self.urdu_templates["update_task"]["success"].format(title=title)
        return f"✓ Updated task '{title}' successfully."

    def _format_error(self, intent: str, error: str, language: str = "en") -> str:
        """Format error messages in user-friendly way."""
        if language == "ur":
            templates = self.urdu_templates["errors"]

            # Task not found errors
            if "not found" in error.lower() or "does not belong" in error.lower():
                return templates["not_found"]

            # Validation errors
            if "required" in error.lower() or "cannot be empty" in error.lower():
                if intent == "create_task":
                    return templates["title_required"]
                return templates["generic"].format(error=error)

            # Generic error
            return templates["generic"].format(error=error)
        else:
            # Task not found errors
            if "not found" in error.lower() or "does not belong" in error.lower():
                return f"I couldn't find that task. Try 'show my tasks' to see your task list."

            # Validation errors
            if "required" in error.lower() or "cannot be empty" in error.lower():
                if intent == "create_task":
                    return "Task title is required. Try: 'add a task to [task name]'."
                return f"Missing required information. {error}"

            # Generic error
            return f"I ran into an issue: {error}. Please try again or rephrase your request."

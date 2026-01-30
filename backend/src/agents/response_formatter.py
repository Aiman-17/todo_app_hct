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
        pass

    def format(
        self,
        intent: str,
        tool_result: Dict[str, Any],
        user_id: str = None,
        correlation_id: str = None
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
                return self._format_error(intent, error_msg)

            # Route to intent-specific formatter
            if intent == "create_task":
                return self._format_create_task(tool_result)

            elif intent == "list_tasks":
                return self._format_list_tasks(tool_result)

            elif intent == "complete_task":
                return self._format_complete_task(tool_result)

            elif intent == "delete_task":
                return self._format_delete_task(tool_result)

            elif intent == "update_task":
                return self._format_update_task(tool_result)

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

    def _format_create_task(self, result: Dict) -> str:
        """Format create_task result."""
        task = result.get("task", {})
        title = task.get("title", "Untitled")
        task_id = task.get("id", "?")
        priority = task.get("priority", "medium")

        response = f"✓ Created task: '{title}' (ID: {task_id})."

        if priority == "high":
            response += " Marked as high priority."

        if task.get("due_date"):
            response += f" Due: {task['due_date'].split('T')[0]}."

        return response

    def _format_list_tasks(self, result: Dict) -> str:
        """Format list_tasks result."""
        tasks = result.get("tasks", [])

        if not tasks:
            return "You don't have any tasks yet. Try creating one by saying 'add a task to...'."

        # Format as bullet list
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
            response_lines.append(f"...and {len(tasks) - 10} more tasks.")

        return "\n".join(response_lines)

    def _format_complete_task(self, result: Dict) -> str:
        """Format complete_task result."""
        task = result.get("task", {})
        title = task.get("title", "Untitled")
        completed = task.get("completed", False)

        if completed:
            return f"✓ Marked '{title}' as complete. Great job! 🎉"
        else:
            return f"○ Unmarked '{title}' as complete."

    def _format_delete_task(self, result: Dict) -> str:
        """Format delete_task result (single or batch)."""
        # Check if this is a batch delete
        if "deleted_count" in result:
            deleted_count = result.get("deleted_count", 0)
            failed_count = result.get("failed_count", 0)

            if deleted_count == 0:
                return "No completed tasks found to delete. Your task list is clean!"

            response = f"✓ Successfully deleted {deleted_count} completed task(s)."
            if failed_count > 0:
                response += f" ({failed_count} task(s) failed to delete)"

            return response

        # Single task deletion
        return "✓ Task deleted successfully. It's been removed from your list."

    def _format_update_task(self, result: Dict) -> str:
        """Format update_task result."""
        task = result.get("task", {})
        title = task.get("title", "Untitled")
        return f"✓ Updated task '{title}' successfully."

    def _format_error(self, intent: str, error: str) -> str:
        """Format error messages in user-friendly way."""
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

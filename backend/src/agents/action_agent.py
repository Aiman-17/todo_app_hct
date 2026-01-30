"""
Phase III: ActionAgent for executing MCP tool operations.

Maps classified intents to appropriate MCP tool calls and handles execution.
"""
from typing import Dict, Any
import logging
from sqlmodel import Session

from src.mcp.task_tools import (
    add_task,
    list_tasks,
    complete_task,
    delete_task,
    update_task
)
from src.agents.task_resolution import TaskResolutionAgent

logger = logging.getLogger("mcp_tools")


class ActionAgent:
    """
    Agent that executes MCP tool operations based on classified intent.

    Responsibilities:
    - Map intent to appropriate MCP tool
    - Validate parameters before execution
    - Execute MCP tool with user isolation
    - Return tool execution result
    - Handle tool failures gracefully

    Example:
        >>> agent = ActionAgent()
        >>> result = agent.execute(
        ...     db, "create_task",
        ...     {"title": "Buy milk", "priority": "high"},
        ...     "user-123"
        ... )
        >>> result["success"]
        True
    """

    def __init__(self):
        """Initialize action agent with task resolution."""
        self.task_resolver = TaskResolutionAgent()

    def execute(
        self,
        db: Session,
        intent: str,
        parameters: Dict[str, Any],
        user_id: str,
        correlation_id: str = None
    ) -> Dict[str, Any]:
        """
        Execute MCP tool based on intent and parameters.

        Args:
            db: Database session
            intent: Classified intent (from IntentClassifierAgent)
            parameters: Extracted entities/parameters
            user_id: User ID (from JWT)
            correlation_id: Optional correlation ID for tracing

        Returns:
            dict: MCP tool execution result {success: bool, ...}

        Example:
            >>> agent.execute(db, "create_task", {"title": "Buy milk"}, "user-123")
            {"success": True, "task": {...}}
        """
        try:
            # Route to appropriate MCP tool based on intent
            if intent == "create_task":
                return self._execute_create_task(db, parameters, user_id, correlation_id)

            elif intent == "list_tasks":
                return self._execute_list_tasks(db, parameters, user_id, correlation_id)

            elif intent == "complete_task":
                return self._execute_complete_task(db, parameters, user_id, correlation_id)

            elif intent == "delete_task":
                return self._execute_delete_task(db, parameters, user_id, correlation_id)

            elif intent == "update_task":
                return self._execute_update_task(db, parameters, user_id, correlation_id)

            elif intent == "unclear":
                logger.warning(
                    "ActionAgent: unclear intent, no action taken",
                    extra={"user_id": user_id, "correlation_id": correlation_id or "none"}
                )
                return {
                    "success": False,
                    "error": "Could not determine what action to take. Please rephrase your request."
                }

            else:
                logger.warning(
                    "ActionAgent: unknown intent",
                    extra={"user_id": user_id, "intent": intent, "correlation_id": correlation_id or "none"}
                )
                return {
                    "success": False,
                    "error": f"Unknown intent: {intent}"
                }

        except Exception as e:
            logger.error(
                "ActionAgent: execution failed",
                extra={"user_id": user_id, "intent": intent, "error": str(e), "correlation_id": correlation_id or "none"},
                exc_info=True
            )
            return {
                "success": False,
                "error": f"Failed to execute action: {str(e)}"
            }

    def _execute_create_task(self, db: Session, params: Dict, user_id: str, correlation_id: str) -> Dict:
        """Execute add_task MCP tool."""
        # Validate required parameters
        if "title" not in params or not params["title"]:
            return {"success": False, "error": "Task title is required"}

        return add_task(
            db=db,
            user_id=user_id,
            title=params["title"],
            description=params.get("description", ""),
            priority=params.get("priority", "medium"),
            due_date=params.get("due_date"),
            tags=params.get("tags"),
            correlation_id=correlation_id
        )

    def _execute_list_tasks(self, db: Session, params: Dict, user_id: str, correlation_id: str) -> Dict:
        """Execute list_tasks MCP tool."""
        # Parse status filter (check both 'completed' and 'filter_completed' for compatibility)
        status = "all"
        completed_filter = params.get("completed") or params.get("filter_completed")

        if completed_filter is True:
            status = "completed"
        elif completed_filter is False:
            status = "pending"

        return list_tasks(
            db=db,
            user_id=user_id,
            status=status,
            priority=params.get("priority"),
            tags=params.get("tags"),
            limit=params.get("limit", 50),
            correlation_id=correlation_id
        )

    def _execute_complete_task(self, db: Session, params: Dict, user_id: str, correlation_id: str) -> Dict:
        """Execute complete_task MCP tool."""
        # Try to get task_id directly
        task_id = params.get("task_id")

        # If no task_id, try to resolve task reference
        if not task_id and params.get("task_reference"):
            resolution = self.task_resolver.resolve(db, user_id, params, correlation_id)

            if resolution.get("error"):
                return {"success": False, "error": resolution["error"]}

            if resolution.get("confirmation_needed"):
                matches = resolution.get("matches", [])
                task_list = "\n".join([f"{i+1}. {t['title']} (ID: {t['id']})" for i, t in enumerate(matches)])
                return {
                    "success": False,
                    "error": f"Multiple tasks found. Please specify which one:\n{task_list}"
                }

            task_ids = resolution.get("task_ids", [])
            if task_ids:
                task_id = task_ids[0]

        if not task_id:
            return {"success": False, "error": "Task ID is required to mark as complete"}

        return complete_task(
            db=db,
            user_id=user_id,
            task_id=int(task_id),
            completed=params.get("completed", True),
            correlation_id=correlation_id
        )

    def _execute_delete_task(self, db: Session, params: Dict, user_id: str, correlation_id: str) -> Dict:
        """Execute delete_task MCP tool (single or batch)."""
        # Check if this is a batch delete operation
        if params.get("batch_delete") and params.get("filter_completed"):
            # Batch delete all completed tasks
            logger.info(
                "ActionAgent: executing batch delete of completed tasks",
                extra={"user_id": user_id, "correlation_id": correlation_id}
            )

            # Get all completed tasks
            list_result = list_tasks(
                db=db,
                user_id=user_id,
                completed=True,
                correlation_id=correlation_id
            )

            if not list_result.get("success"):
                return {"success": False, "error": "Failed to fetch completed tasks"}

            completed_tasks = list_result.get("tasks", [])

            if not completed_tasks:
                return {
                    "success": True,
                    "deleted_count": 0,
                    "message": "No completed tasks found to delete"
                }

            # Delete each completed task
            deleted_count = 0
            failed_count = 0
            for task in completed_tasks:
                try:
                    delete_result = delete_task(
                        db=db,
                        user_id=user_id,
                        task_id=task["id"],
                        correlation_id=correlation_id
                    )
                    if delete_result.get("success"):
                        deleted_count += 1
                    else:
                        failed_count += 1
                except Exception as e:
                    logger.error(
                        f"ActionAgent: failed to delete task {task['id']} during batch delete",
                        extra={"user_id": user_id, "error": str(e), "correlation_id": correlation_id}
                    )
                    failed_count += 1

            return {
                "success": True,
                "deleted_count": deleted_count,
                "failed_count": failed_count,
                "message": f"Deleted {deleted_count} completed task(s)" +
                          (f" ({failed_count} failed)" if failed_count > 0 else "")
            }

        # Single task deletion
        task_id = params.get("task_id")

        # If no task_id, try to resolve task reference
        if not task_id and params.get("task_reference"):
            resolution = self.task_resolver.resolve(db, user_id, params, correlation_id)

            if resolution.get("error"):
                return {"success": False, "error": resolution["error"]}

            if resolution.get("confirmation_needed"):
                matches = resolution.get("matches", [])
                task_list = "\n".join([f"{i+1}. {t['title']} (ID: {t['id']})" for i, t in enumerate(matches)])
                return {
                    "success": False,
                    "error": f"Multiple tasks found. Please specify which one:\n{task_list}"
                }

            task_ids = resolution.get("task_ids", [])
            if task_ids:
                task_id = task_ids[0]

        if not task_id:
            return {"success": False, "error": "Task ID is required to delete"}

        return delete_task(
            db=db,
            user_id=user_id,
            task_id=int(task_id),
            correlation_id=correlation_id
        )

    def _execute_update_task(self, db: Session, params: Dict, user_id: str, correlation_id: str) -> Dict:
        """Execute update_task MCP tool."""
        # Validate task_id
        task_id = params.get("task_id")
        if not task_id:
            return {"success": False, "error": "Task ID is required to update"}

        return update_task(
            db=db,
            user_id=user_id,
            task_id=int(task_id),
            title=params.get("title"),
            description=params.get("description"),
            priority=params.get("priority"),
            due_date=params.get("due_date"),
            tags=params.get("tags"),
            correlation_id=correlation_id
        )

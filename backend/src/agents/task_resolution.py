"""
Phase III: TaskResolutionAgent for resolving ambiguous task references.

Resolves natural language task references (e.g., "the grocery one", "first task")
to specific task IDs using semantic matching and MCP tools.
"""
from typing import Dict, Any, List, Optional
import logging
from sqlmodel import Session

from src.mcp.task_tools import list_tasks

logger = logging.getLogger("mcp_tools")


class TaskResolutionAgent:
    """
    Agent that resolves ambiguous task references to specific task IDs.

    Responsibilities:
    - Resolve fuzzy task references ("the grocery one", "my first task")
    - Use semantic matching to find best task match
    - Request user confirmation if multiple matches found
    - Use list_tasks MCP tool (read-only access)

    Example:
        >>> agent = TaskResolutionAgent()
        >>> result = agent.resolve(db, "user-123", {"reference": "the grocery one"})
        >>> result["task_ids"]
        [5]
        >>> result["confirmation_needed"]
        False
    """

    def __init__(self):
        """Initialize task resolution agent."""
        self.confidence_threshold = 0.7

    def resolve(
        self,
        db: Session,
        user_id: str,
        entities: Dict[str, Any],
        correlation_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Resolve task reference to specific task ID(s).

        Args:
            db: Database session
            user_id: User ID (from JWT)
            entities: Entities dict from IntentClassifierAgent
            correlation_id: Optional correlation ID for tracing

        Returns:
            dict: {
                "task_ids": list[int],  # Resolved task IDs
                "confirmation_needed": bool,  # True if multiple matches
                "matches": list[dict]  # Matched tasks for confirmation
            }

        Example:
            >>> # Single clear match
            >>> agent.resolve(db, "user-123", {"task_id": 5})
            {"task_ids": [5], "confirmation_needed": False, "matches": []}

            >>> # Fuzzy match needing confirmation
            >>> agent.resolve(db, "user-123", {"task_reference": "grocery"})
            {
                "task_ids": [5, 12],
                "confirmation_needed": True,
                "matches": [{"id": 5, "title": "Buy groceries"}, {"id": 12, "title": "Grocery shopping"}]
            }
        """
        try:
            # Case 1: Explicit task ID provided
            if "task_id" in entities and entities["task_id"]:
                task_id = int(entities["task_id"])
                logger.info(
                    "TaskResolutionAgent: explicit task_id",
                    extra={"user_id": user_id, "task_id": task_id, "correlation_id": correlation_id or "none"}
                )
                return {
                    "task_ids": [task_id],
                    "confirmation_needed": False,
                    "matches": []
                }

            # Case 2: Task reference (fuzzy text matching)
            if "task_reference" in entities and entities["task_reference"]:
                reference = entities["task_reference"].lower().strip()

                # Get all user's tasks via MCP tool (READ-ONLY)
                tasks_result = list_tasks(
                    db=db,
                    user_id=user_id,
                    status="all",
                    correlation_id=correlation_id
                )

                if not tasks_result.get("success"):
                    logger.error(
                        "TaskResolutionAgent: list_tasks failed",
                        extra={"user_id": user_id, "error": tasks_result.get("error"), "correlation_id": correlation_id or "none"}
                    )
                    return {
                        "task_ids": [],
                        "confirmation_needed": False,
                        "matches": [],
                        "error": "Failed to retrieve tasks"
                    }

                tasks = tasks_result.get("tasks", [])

                # Fuzzy match task titles
                matches = []
                for task in tasks:
                    title_lower = task["title"].lower()
                    # Simple substring matching (can be enhanced with fuzzy matching library)
                    if reference in title_lower or title_lower in reference:
                        matches.append({
                            "id": task["id"],
                            "title": task["title"],
                            "completed": task["completed"]
                        })

                logger.info(
                    "TaskResolutionAgent: fuzzy match",
                    extra={
                        "user_id": user_id,
                        "reference": reference,
                        "match_count": len(matches),
                        "correlation_id": correlation_id or "none"
                    }
                )

                # Single match - no confirmation needed
                if len(matches) == 1:
                    return {
                        "task_ids": [matches[0]["id"]],
                        "confirmation_needed": False,
                        "matches": matches
                    }

                # Multiple matches - need confirmation
                if len(matches) > 1:
                    return {
                        "task_ids": [m["id"] for m in matches],
                        "confirmation_needed": True,
                        "matches": matches
                    }

                # No matches found
                return {
                    "task_ids": [],
                    "confirmation_needed": False,
                    "matches": [],
                    "error": f"No tasks found matching '{reference}'"
                }

            # Case 3: Positional reference ("first task", "second one")
            # Extract ordinal numbers (first=0, second=1, etc.) - simplified
            if "task_reference" in entities:
                reference = entities["task_reference"].lower()
                ordinal_map = {
                    "first": 0, "1st": 0,
                    "second": 1, "2nd": 1,
                    "third": 2, "3rd": 2,
                    "fourth": 3, "4th": 3,
                    "fifth": 4, "5th": 4,
                    "last": -1
                }

                for word, index in ordinal_map.items():
                    if word in reference:
                        # Get tasks via MCP tool
                        tasks_result = list_tasks(
                            db=db,
                            user_id=user_id,
                            status="pending",  # Usually refers to active tasks
                            correlation_id=correlation_id
                        )

                        if tasks_result.get("success"):
                            tasks = tasks_result.get("tasks", [])
                            if 0 <= index < len(tasks) or (index == -1 and tasks):
                                task_id = tasks[index]["id"]
                                logger.info(
                                    "TaskResolutionAgent: positional reference",
                                    extra={"user_id": user_id, "position": word, "task_id": task_id, "correlation_id": correlation_id or "none"}
                                )
                                return {
                                    "task_ids": [task_id],
                                    "confirmation_needed": False,
                                    "matches": [tasks[index]]
                                }

            # No task reference found
            logger.warning(
                "TaskResolutionAgent: no resolvable task reference",
                extra={"user_id": user_id, "entities": entities, "correlation_id": correlation_id or "none"}
            )
            return {
                "task_ids": [],
                "confirmation_needed": False,
                "matches": [],
                "error": "No task reference found in message"
            }

        except Exception as e:
            logger.error(
                "TaskResolutionAgent: resolution failed",
                extra={"user_id": user_id, "error": str(e), "correlation_id": correlation_id or "none"},
                exc_info=True
            )
            return {
                "task_ids": [],
                "confirmation_needed": False,
                "matches": [],
                "error": str(e)
            }

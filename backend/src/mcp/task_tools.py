"""
Phase III: MCP Tool implementations for task operations.

This module provides Model Context Protocol (MCP) tools that expose Phase II
task CRUD operations to AI agents. All tools import Phase II service functions
(READ-ONLY) and enforce user isolation.

Tools:
- add_task: Create new task
- list_tasks: Retrieve tasks with filtering
- complete_task: Toggle task completion status
- delete_task: Soft delete a task
- update_task: Modify task fields

Architecture:
- All tools accept user_id as first parameter (extracted from JWT by agents)
- All tools use Phase II service layer functions (no direct database access)
- All tools return standardized {success: bool, ...} responses
- All tool calls are logged for audit trail
"""
import logging
from uuid import UUID
from typing import Dict, List, Any, Optional
from datetime import datetime
from sqlmodel import Session

# READ-ONLY imports from Phase II service layer
from src.services.task_service import (
    get_tasks as phase2_get_tasks,
    create_task as phase2_create_task,
    update_task as phase2_update_task,
    delete_task as phase2_delete_task,
    toggle_completion as phase2_toggle_completion
)
from src.models.task import TaskPriority
from src.config import settings

# Initialize MCP tools logging (creates file handler, rotation, correlation ID support)
from src.mcp.logging_config import setup_mcp_logging
logger = setup_mcp_logging()


def add_task(
    db: Session,
    user_id: str,
    title: str,
    description: str = "",
    priority: str = "medium",
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Create a new task for the authenticated user.

    Args:
        db: Database session
        user_id: UUID string of the user (from JWT)
        title: Task title (max 200 characters)
        description: Optional task description (max 2000 characters)
        priority: Task priority ('high', 'medium', 'low') - default 'medium'
        due_date: Optional due date in ISO format (e.g., "2026-01-15T10:30:00Z")
        tags: Optional list of tags (max 10 tags, each max 50 chars)
        correlation_id: Optional correlation ID for request tracing

    Returns:
        dict: {success: bool, task: dict} on success, {success: false, error: str} on failure

    Example:
        >>> result = add_task(db, "user-123", "Buy groceries", priority="high")
        >>> result["success"]
        True
        >>> result["task"]["title"]
        'Buy groceries'
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError as e:
                logger.warning(
                    "Invalid due_date format",
                    extra={"user_id": user_id, "due_date": due_date, "error": str(e), "correlation_id": correlation_id}
                )
                return {"success": False, "error": f"Invalid due_date format: {due_date}. Use ISO format (e.g., '2026-01-15T10:30:00Z')"}

        # Convert priority string to TaskPriority enum
        try:
            priority_enum = TaskPriority(priority.lower())
        except ValueError:
            return {"success": False, "error": f"Invalid priority '{priority}'. Must be 'high', 'medium', or 'low'"}

        # Validate title
        if not title or not title.strip():
            return {"success": False, "error": "Task title cannot be empty"}

        # Call Phase II service layer (READ-ONLY import)
        task = phase2_create_task(
            db=db,
            user_id=user_uuid,
            title=title.strip(),
            description=description.strip() if description else "",
            priority=priority_enum,
            due_date=due_date_obj,
            tags=tags
        )

        # Log successful operation
        logger.info(
            "MCP Tool: add_task",
            extra={
                "user_id": user_id,
                "task_id": task.id,
                "title": task.title,
                "correlation_id": correlation_id
            }
        )

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }

    except Exception as e:
        logger.error(
            "MCP Tool: add_task failed",
            extra={"user_id": user_id, "error": str(e), "correlation_id": correlation_id},
            exc_info=True
        )
        return {"success": False, "error": f"Failed to create task: {str(e)}"}


def list_tasks(
    db: Session,
    user_id: str,
    status: str = "all",
    priority: Optional[str] = None,
    tags: Optional[List[str]] = None,
    limit: int = 50,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Retrieve tasks for the authenticated user with optional filtering.

    Args:
        db: Database session
        user_id: UUID string of the user (from JWT)
        status: Filter by status ('all', 'pending', 'completed') - default 'all'
        priority: Filter by priority ('high', 'medium', 'low') - optional
        tags: Filter by tags (tasks must have ALL specified tags) - optional
        limit: Maximum number of tasks to return (default 50, max 200)
        correlation_id: Optional correlation ID for request tracing

    Returns:
        dict: {success: bool, tasks: list} on success, {success: false, error: str} on failure

    Example:
        >>> result = list_tasks(db, "user-123", status="pending", priority="high")
        >>> result["success"]
        True
        >>> len(result["tasks"])
        5
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Parse status filter
        completed_filter = None
        if status == "pending":
            completed_filter = False
        elif status == "completed":
            completed_filter = True
        elif status != "all":
            return {"success": False, "error": f"Invalid status '{status}'. Must be 'all', 'pending', or 'completed'"}

        # Parse priority filter
        priority_enum = None
        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
            except ValueError:
                return {"success": False, "error": f"Invalid priority '{priority}'. Must be 'high', 'medium', or 'low'"}

        # Enforce limit cap
        limit = min(limit, 200)

        # Call Phase II service layer (READ-ONLY import)
        tasks = phase2_get_tasks(
            db=db,
            user_id=user_uuid,
            priority=priority_enum,
            tags=tags,
            completed=completed_filter,
            sort_by="created_at",
            order="desc"
        )

        # Apply limit
        tasks = tasks[:limit]

        # Log successful operation
        logger.info(
            "MCP Tool: list_tasks",
            extra={
                "user_id": user_id,
                "task_count": len(tasks),
                "filters": {"status": status, "priority": priority, "tags": tags},
                "correlation_id": correlation_id
            }
        )

        return {
            "success": True,
            "tasks": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "priority": task.priority.value,
                    "due_date": task.due_date.isoformat() if task.due_date else None,
                    "tags": task.tags,
                    "created_at": task.created_at.isoformat(),
                    "updated_at": task.updated_at.isoformat()
                }
                for task in tasks
            ]
        }

    except Exception as e:
        logger.error(
            "MCP Tool: list_tasks failed",
            extra={"user_id": user_id, "error": str(e), "correlation_id": correlation_id},
            exc_info=True
        )
        return {"success": False, "error": f"Failed to list tasks: {str(e)}"}


def complete_task(
    db: Session,
    user_id: str,
    task_id: int,
    completed: bool = True,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Toggle task completion status.

    Args:
        db: Database session
        user_id: UUID string of the user (from JWT)
        task_id: Task ID to toggle
        completed: Target completion status (default True)
        correlation_id: Optional correlation ID for request tracing

    Returns:
        dict: {success: bool, task: dict} on success, {success: false, error: str} on failure

    Example:
        >>> result = complete_task(db, "user-123", task_id=42, completed=True)
        >>> result["success"]
        True
        >>> result["task"]["completed"]
        True
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Call Phase II service layer (READ-ONLY import)
        task = phase2_toggle_completion(db=db, task_id=task_id, user_id=user_uuid)

        if not task:
            logger.warning(
                "MCP Tool: complete_task - task not found",
                extra={"user_id": user_id, "task_id": task_id, "correlation_id": correlation_id}
            )
            return {"success": False, "error": f"Task {task_id} not found or does not belong to user"}

        # Check if we need to toggle again to match desired state
        if task.completed != completed:
            task = phase2_toggle_completion(db=db, task_id=task_id, user_id=user_uuid)

        # Log successful operation
        logger.info(
            "MCP Tool: complete_task",
            extra={
                "user_id": user_id,
                "task_id": task_id,
                "completed": task.completed,
                "correlation_id": correlation_id
            }
        )

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }

    except Exception as e:
        logger.error(
            "MCP Tool: complete_task failed",
            extra={"user_id": user_id, "task_id": task_id, "error": str(e), "correlation_id": correlation_id},
            exc_info=True
        )
        return {"success": False, "error": f"Failed to toggle task completion: {str(e)}"}


def delete_task(
    db: Session,
    user_id: str,
    task_id: int,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Soft delete a task.

    Sets deleted_at timestamp instead of permanently removing the task.

    Args:
        db: Database session
        user_id: UUID string of the user (from JWT)
        task_id: Task ID to delete
        correlation_id: Optional correlation ID for request tracing

    Returns:
        dict: {success: bool} on success, {success: false, error: str} on failure

    Example:
        >>> result = delete_task(db, "user-123", task_id=42)
        >>> result["success"]
        True
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Call Phase II service layer (READ-ONLY import)
        success = phase2_delete_task(db=db, task_id=task_id, user_id=user_uuid)

        if not success:
            logger.warning(
                "MCP Tool: delete_task - task not found",
                extra={"user_id": user_id, "task_id": task_id, "correlation_id": correlation_id}
            )
            return {"success": False, "error": f"Task {task_id} not found or does not belong to user"}

        # Log successful operation
        logger.info(
            "MCP Tool: delete_task",
            extra={"user_id": user_id, "task_id": task_id, "correlation_id": correlation_id}
        )

        return {"success": True}

    except Exception as e:
        logger.error(
            "MCP Tool: delete_task failed",
            extra={"user_id": user_id, "task_id": task_id, "error": str(e), "correlation_id": correlation_id},
            exc_info=True
        )
        return {"success": False, "error": f"Failed to delete task: {str(e)}"}


def update_task(
    db: Session,
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    due_date: Optional[str] = None,
    tags: Optional[List[str]] = None,
    correlation_id: Optional[str] = None
) -> Dict[str, Any]:
    """
    MCP Tool: Update task fields.

    Only provided fields are updated; None values are ignored.

    Args:
        db: Database session
        user_id: UUID string of the user (from JWT)
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority ('high', 'medium', 'low') - optional
        due_date: New due date in ISO format (optional)
        tags: New tags list (optional)
        correlation_id: Optional correlation ID for request tracing

    Returns:
        dict: {success: bool, task: dict} on success, {success: false, error: str} on failure

    Example:
        >>> result = update_task(db, "user-123", task_id=42, title="Updated title", priority="high")
        >>> result["success"]
        True
        >>> result["task"]["title"]
        'Updated title'
    """
    try:
        # Convert user_id string to UUID
        user_uuid = UUID(user_id)

        # Parse priority if provided
        priority_enum = None
        if priority:
            try:
                priority_enum = TaskPriority(priority.lower())
            except ValueError:
                return {"success": False, "error": f"Invalid priority '{priority}'. Must be 'high', 'medium', or 'low'"}

        # Parse due_date if provided
        due_date_obj = None
        if due_date:
            try:
                due_date_obj = datetime.fromisoformat(due_date.replace("Z", "+00:00"))
            except ValueError as e:
                logger.warning(
                    "Invalid due_date format",
                    extra={"user_id": user_id, "due_date": due_date, "error": str(e), "correlation_id": correlation_id}
                )
                return {"success": False, "error": f"Invalid due_date format: {due_date}. Use ISO format"}

        # Call Phase II service layer (READ-ONLY import)
        task = phase2_update_task(
            db=db,
            task_id=task_id,
            user_id=user_uuid,
            title=title.strip() if title else None,
            description=description.strip() if description else None,
            priority=priority_enum,
            due_date=due_date_obj,
            tags=tags
        )

        if not task:
            logger.warning(
                "MCP Tool: update_task - task not found",
                extra={"user_id": user_id, "task_id": task_id, "correlation_id": correlation_id}
            )
            return {"success": False, "error": f"Task {task_id} not found or does not belong to user"}

        # Log successful operation
        logger.info(
            "MCP Tool: update_task",
            extra={
                "user_id": user_id,
                "task_id": task_id,
                "updated_fields": {k: v for k, v in {"title": title, "priority": priority, "due_date": due_date, "tags": tags}.items() if v is not None},
                "correlation_id": correlation_id
            }
        )

        return {
            "success": True,
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "tags": task.tags,
                "created_at": task.created_at.isoformat(),
                "updated_at": task.updated_at.isoformat()
            }
        }

    except Exception as e:
        logger.error(
            "MCP Tool: update_task failed",
            extra={"user_id": user_id, "task_id": task_id, "error": str(e), "correlation_id": correlation_id},
            exc_info=True
        )
        return {"success": False, "error": f"Failed to update task: {str(e)}"}

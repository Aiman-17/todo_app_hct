"""
Tasks API router with CRUD endpoints for task management.

Provides REST API endpoints for:
- List user's tasks (GET /api/tasks)
- Create task (POST /api/tasks)
- Update task (PUT /api/tasks/{task_id})
- Delete task (DELETE /api/tasks/{task_id})
- Toggle completion (PATCH /api/tasks/{task_id}/toggle)

All endpoints require authentication and enforce user isolation.
"""
import logging
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlmodel import Session
from typing import List, Optional

from src.dependencies import get_db_session, get_current_user
from src.models.user import User
from src.models.task import TaskPriority
from src.schemas.task import TaskCreate, TaskUpdate, TaskResponse
from src.services.task_service import (
    get_tasks,
    get_task_by_id,
    create_task,
    update_task,
    delete_task,
    restore_task,
    toggle_completion,
    get_upcoming_recurring_tasks
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.get(
    "",
    response_model=List[TaskResponse],
    summary="List tasks with optional filtering and sorting",
    response_description="List of filtered and sorted tasks"
)
async def list_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
    priority: Optional[TaskPriority] = Query(None, description="Filter by priority (high, medium, low)"),
    tags: Optional[str] = Query(None, description="Filter by tags (comma-separated, e.g., 'work,urgent')"),
    completed: Optional[bool] = Query(None, description="Filter by completion status (true/false)"),
    sort_by: str = Query("created_at", description="Sort by field (created_at, due_date, priority, updated_at)"),
    order: str = Query("desc", description="Sort order (asc or desc)")
):
    """
    List tasks for the authenticated user with optional filtering and sorting.

    Query Parameters:
        - priority: Filter by priority (high, medium, low)
        - tags: Comma-separated tags (tasks must have ALL specified tags)
        - completed: Filter by completion status (true/false)
        - sort_by: Field to sort by (created_at, due_date, priority, updated_at)
        - order: Sort order (asc or desc)

    Args:
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)
        priority: Priority filter (optional)
        tags: Comma-separated tags filter (optional)
        completed: Completion status filter (optional)
        sort_by: Field to sort by
        order: Sort order

    Returns:
        List[TaskResponse]: Filtered and sorted tasks

    Example Requests:
        GET /api/tasks?priority=high&completed=false
        GET /api/tasks?tags=work,urgent&sort_by=due_date&order=asc
        GET /api/tasks?sort_by=priority&order=desc
    """
    # Parse tags from comma-separated string
    tag_list = [tag.strip() for tag in tags.split(",")] if tags else None

    # Validate sort_by and order
    valid_sort_fields = ["created_at", "due_date", "priority", "updated_at"]
    valid_orders = ["asc", "desc"]

    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid sort_by field. Must be one of: {', '.join(valid_sort_fields)}"
        )

    if order not in valid_orders:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid order. Must be 'asc' or 'desc'"
        )

    # Get tasks with filters
    tasks = get_tasks(
        db=db,
        user_id=current_user.id,
        priority=priority,
        tags=tag_list,
        completed=completed,
        sort_by=sort_by,
        order=order
    )

    logger.info(
        f"Retrieved {len(tasks)} tasks for user: {current_user.email} "
        f"(filters: priority={priority}, tags={tags}, completed={completed}, "
        f"sort_by={sort_by}, order={order})"
    )
    return [TaskResponse.model_validate(task) for task in tasks]


@router.post(
    "",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create a new task",
    response_description="The created task with generated ID and timestamps"
)
async def create_new_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Create a new task for the authenticated user.

    Args:
        task_data: TaskCreate schema with title and optional description
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)

    Returns:
        TaskResponse: The created task

    Example Request:
        POST /api/tasks
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        {
            "title": "Buy groceries",
            "description": "Milk, eggs, bread"
        }

    Example Response:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "created_at": "2025-12-30T10:00:00Z",
            "updated_at": "2025-12-30T10:00:00Z"
        }
    """
    task = create_task(
        db=db,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        tags=task_data.tags,
        recurrence_rule=task_data.recurrence_rule
    )
    logger.info(f"Task created (ID: {task.id}) by user: {current_user.email}")
    return TaskResponse.model_validate(task)


@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    summary="Update a task's title and/or description",
    response_description="The updated task with new data and updated timestamp"
)
async def update_existing_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Update a task's title and/or description.

    User can only update their own tasks (user isolation enforced).

    Args:
        task_id: ID of the task to update
        task_data: TaskUpdate schema with optional title and description
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)

    Returns:
        TaskResponse: The updated task

    Raises:
        404 Not Found: If task doesn't exist or doesn't belong to user

    Example Request:
        PUT /api/tasks/1
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
        {
            "title": "Updated title",
            "description": "Updated description"
        }

    Example Response:
        {
            "id": 1,
            "title": "Updated title",
            "description": "Updated description",
            "completed": false,
            "created_at": "2025-12-30T10:00:00Z",
            "updated_at": "2025-12-30T10:05:00Z"
        }
    """
    task = update_task(
        db=db,
        task_id=task_id,
        user_id=current_user.id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        due_date=task_data.due_date,
        tags=task_data.tags,
        recurrence_rule=task_data.recurrence_rule
    )

    if not task:
        logger.warning(f"Task update failed - not found (ID: {task_id}) for user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task updated (ID: {task_id}) by user: {current_user.email}")
    return TaskResponse.model_validate(task)


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
    response_description="No content (task successfully deleted)"
)
async def delete_existing_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Delete a task.

    User can only delete their own tasks (user isolation enforced).

    Args:
        task_id: ID of the task to delete
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)

    Returns:
        None (204 No Content on success)

    Raises:
        404 Not Found: If task doesn't exist or doesn't belong to user

    Example Request:
        DELETE /api/tasks/1
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
    """
    success = delete_task(db, task_id, current_user.id)

    if not success:
        logger.warning(f"Task delete failed - not found (ID: {task_id}) for user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task deleted (ID: {task_id}) by user: {current_user.email}")


@router.post(
    "/{task_id}/restore",
    response_model=TaskResponse,
    summary="Restore a soft-deleted task (undo delete)",
    response_description="The restored task"
)
async def restore_deleted_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Restore a soft-deleted task (undo delete operation).

    User can only restore their own tasks (user isolation enforced).
    Task must have been soft-deleted (deleted_at IS NOT NULL).

    Args:
        task_id: ID of the task to restore
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)

    Returns:
        TaskResponse: The restored task

    Raises:
        404 Not Found: If task doesn't exist, doesn't belong to user, or wasn't deleted

    Example Request:
        POST /api/tasks/1/restore
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": false,
            "priority": "high",
            "due_date": "2025-01-05T10:00:00Z",
            "tags": ["shopping"],
            "recurrence_rule": null,
            "created_at": "2025-01-01T10:00:00Z",
            "updated_at": "2025-01-04T10:05:00Z"
        }
    """
    task = restore_task(db, task_id, current_user.id)

    if not task:
        logger.warning(f"Task restore failed - not found or not deleted (ID: {task_id}) for user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found or not deleted"
        )

    logger.info(f"Task restored (ID: {task_id}) by user: {current_user.email}")
    return TaskResponse.model_validate(task)


@router.patch(
    "/{task_id}/toggle",
    response_model=TaskResponse,
    summary="Toggle task completion status",
    response_description="The task with toggled completion status"
)
async def toggle_task_completion(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session)
):
    """
    Toggle task completion status (complete ↔ incomplete).

    User can only toggle their own tasks (user isolation enforced).

    Args:
        task_id: ID of the task to toggle
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)

    Returns:
        TaskResponse: The task with updated completion status

    Raises:
        404 Not Found: If task doesn't exist or doesn't belong to user

    Example Request:
        PATCH /api/tasks/1/toggle
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response:
        {
            "id": 1,
            "title": "Buy groceries",
            "description": "Milk, eggs, bread",
            "completed": true,
            "created_at": "2025-12-30T10:00:00Z",
            "updated_at": "2025-12-30T10:05:00Z"
        }
    """
    task = toggle_completion(db, task_id, current_user.id)

    if not task:
        logger.warning(f"Task toggle failed - not found (ID: {task_id}) for user: {current_user.email}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    logger.info(f"Task completion toggled (ID: {task_id}, completed: {task.completed}) by user: {current_user.email}")
    return TaskResponse.model_validate(task)


@router.get(
    "/upcoming",
    response_model=List[TaskResponse],
    summary="Get upcoming recurring task occurrences",
    response_description="List of upcoming recurring task previews"
)
async def get_upcoming_tasks(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db_session),
    limit: int = Query(10, ge=1, le=50, description="Maximum number of upcoming tasks to return")
):
    """
    Get upcoming recurring task occurrences for preview.

    Returns a preview of the next occurrences for all recurring tasks.
    Useful for showing users what recurring tasks are coming up.

    Args:
        current_user: Authenticated user (injected dependency)
        db: Database session (injected dependency)
        limit: Maximum number of upcoming tasks to return (default: 10, max: 50)

    Returns:
        List[TaskResponse]: Upcoming recurring task occurrences

    Example Request:
        GET /api/tasks/upcoming?limit=20
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response:
        [
            {
                "id": 1,
                "title": "Daily standup",
                "description": "Team sync meeting",
                "completed": false,
                "priority": "medium",
                "due_date": "2025-01-05T10:00:00Z",
                "tags": ["work", "meeting"],
                "recurrence_rule": {"frequency": "daily", "interval": 1},
                "created_at": "2025-01-01T10:00:00Z",
                "updated_at": "2025-01-01T10:00:00Z"
            }
        ]
    """
    upcoming_tasks = get_upcoming_recurring_tasks(
        db=db,
        user_id=current_user.id,
        limit=limit
    )

    logger.info(f"Retrieved {len(upcoming_tasks)} upcoming recurring tasks for user: {current_user.email}")
    return [TaskResponse.model_validate(task) for task in upcoming_tasks]

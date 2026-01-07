"""
Task service for CRUD operations on Task model with user isolation.

Provides functions for creating, reading, updating, deleting tasks,
and toggling completion status. All operations enforce user isolation
to ensure users can only access their own tasks.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import List, Optional, Dict, Any
from datetime import datetime, timezone

from src.models.task import Task, TaskPriority


def get_tasks(
    db: Session,
    user_id: UUID,
    priority: Optional[TaskPriority] = None,
    tags: Optional[List[str]] = None,
    completed: Optional[bool] = None,
    sort_by: str = "created_at",
    order: str = "desc"
) -> List[Task]:
    """
    Retrieve tasks for a specific user with optional filtering and sorting.

    Excludes soft-deleted tasks (deleted_at IS NOT NULL).

    Args:
        db: Database session
        user_id: UUID of the user whose tasks to retrieve
        priority: Filter by priority (high, medium, low) - optional
        tags: Filter by tags (tasks must have ALL specified tags) - optional
        completed: Filter by completion status (True/False) - optional
        sort_by: Field to sort by (created_at, due_date, priority, updated_at)
        order: Sort order (asc or desc)

    Returns:
        List[Task]: Filtered and sorted tasks for the user (excluding deleted)

    Example:
        >>> tasks = get_tasks(db, user_id, priority=TaskPriority.HIGH, completed=False)
        >>> tasks = get_tasks(db, user_id, tags=["work", "urgent"], sort_by="due_date")
    """
    # Build base query with user isolation and exclude soft-deleted tasks
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.deleted_at.is_(None)
    )

    # Apply filters
    if priority is not None:
        statement = statement.where(Task.priority == priority)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    # Execute query to get tasks (for tags filtering in Python)
    tasks = db.exec(statement).all()

    # Filter by tags if provided (check if task has ALL specified tags)
    if tags:
        filtered_tasks = []
        for task in tasks:
            if task.tags and all(tag in task.tags for tag in tags):
                filtered_tasks.append(task)
        tasks = filtered_tasks

    # Sort tasks
    reverse = (order == "desc")

    if sort_by == "priority":
        # Sort by priority: high > medium > low
        priority_order = {"high": 3, "medium": 2, "low": 1}
        tasks = sorted(tasks, key=lambda t: priority_order.get(t.priority, 0), reverse=reverse)
    elif sort_by == "due_date":
        # Sort by due_date, None values go to end
        tasks = sorted(
            tasks,
            key=lambda t: (t.due_date is None, t.due_date if t.due_date else datetime.max.replace(tzinfo=timezone.utc)),
            reverse=reverse
        )
    elif sort_by == "updated_at":
        tasks = sorted(tasks, key=lambda t: t.updated_at, reverse=reverse)
    else:  # Default: created_at
        tasks = sorted(tasks, key=lambda t: t.created_at, reverse=reverse)

    return tasks


def get_task_by_id(db: Session, task_id: int, user_id: UUID) -> Optional[Task]:
    """
    Retrieve a single task by ID with user isolation.

    Excludes soft-deleted tasks (deleted_at IS NOT NULL).

    Args:
        db: Database session
        task_id: Task ID to retrieve
        user_id: UUID of the user (for authorization)

    Returns:
        Task if found and belongs to user (and not deleted), None otherwise

    Example:
        >>> task = get_task_by_id(db, 1, user_id)
        >>> if task:
        ...     print(task.title)
    """
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id,
        Task.deleted_at.is_(None)
    )
    task = db.exec(statement).first()
    return task


def create_task(
    db: Session,
    user_id: UUID,
    title: str,
    description: str = "",
    priority: TaskPriority = TaskPriority.MEDIUM,
    due_date: Optional[datetime] = None,
    tags: Optional[List[str]] = None,
    recurrence_rule: Optional[Dict[str, Any]] = None
) -> Task:
    """
    Create a new task for a user with all Phase 3 fields.

    Args:
        db: Database session
        user_id: UUID of the user creating the task
        title: Task title (max 200 characters)
        description: Optional task description (max 2000 characters)
        priority: Task priority (high, medium, low) - default medium
        due_date: Optional due date for the task
        tags: Optional list of tags (max 10 tags, each max 50 chars)
        recurrence_rule: Optional recurrence rule dictionary

    Returns:
        Task: The created task with id populated

    Example:
        >>> task = create_task(
        ...     db, user_id, "Buy groceries", "Milk, eggs, bread",
        ...     priority=TaskPriority.HIGH, tags=["shopping", "urgent"]
        ... )
    """
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=False,
        priority=priority,
        due_date=due_date,
        tags=tags,
        recurrence_rule=recurrence_rule
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def update_task(
    db: Session,
    task_id: int,
    user_id: UUID,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[TaskPriority] = None,
    due_date: Optional[datetime] = None,
    tags: Optional[List[str]] = None,
    recurrence_rule: Optional[Dict[str, Any]] = None
) -> Optional[Task]:
    """
    Update task fields with user isolation.

    Args:
        db: Database session
        task_id: Task ID to update
        user_id: UUID of the user (for authorization)
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)
        due_date: New due date (optional)
        tags: New tags list (optional)
        recurrence_rule: New recurrence rule (optional)

    Returns:
        Task: Updated task if found and belongs to user, None otherwise

    Example:
        >>> task = update_task(
        ...     db, 1, user_id,
        ...     title="Updated title",
        ...     priority=TaskPriority.HIGH,
        ...     tags=["urgent", "work"]
        ... )
    """
    # Find task with user isolation
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return None

    # Update fields if provided
    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if priority is not None:
        task.priority = priority
    if due_date is not None:
        task.due_date = due_date
    if tags is not None:
        task.tags = tags
    if recurrence_rule is not None:
        task.recurrence_rule = recurrence_rule

    # Update timestamp
    task.updated_at = datetime.now(timezone.utc)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def delete_task(db: Session, task_id: int, user_id: UUID) -> bool:
    """
    Soft delete a task with user isolation.

    Sets deleted_at timestamp instead of permanently removing the task.
    This allows for undo functionality.

    Args:
        db: Database session
        task_id: Task ID to delete
        user_id: UUID of the user (for authorization)

    Returns:
        bool: True if task was soft deleted, False if not found or unauthorized

    Example:
        >>> success = delete_task(db, 1, user_id)
        >>> if success:
        ...     print("Task soft deleted")
    """
    # Find task with user isolation
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return False

    # Soft delete by setting deleted_at timestamp
    task.deleted_at = datetime.now(timezone.utc)
    task.updated_at = datetime.now(timezone.utc)

    db.add(task)
    db.commit()
    db.refresh(task)
    return True


def restore_task(db: Session, task_id: int, user_id: UUID) -> Optional[Task]:
    """
    Restore a soft-deleted task (undo delete).

    Clears the deleted_at timestamp to restore the task.

    Args:
        db: Database session
        task_id: Task ID to restore
        user_id: UUID of the user (for authorization)

    Returns:
        Task: Restored task if found and belongs to user, None otherwise

    Example:
        >>> task = restore_task(db, 1, user_id)
        >>> if task:
        ...     print(f"Task '{task.title}' restored")
    """
    # Find task (including soft-deleted ones)
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db.exec(statement).first()

    if not task or task.deleted_at is None:
        return None

    # Restore by clearing deleted_at
    task.deleted_at = None
    task.updated_at = datetime.now(timezone.utc)

    db.add(task)
    db.commit()
    db.refresh(task)
    return task


def permanently_delete_task(db: Session, task_id: int, user_id: UUID) -> bool:
    """
    Permanently delete a task (hard delete).

    This is irreversible and should only be used for cleanup of old soft-deleted tasks.

    Args:
        db: Database session
        task_id: Task ID to permanently delete
        user_id: UUID of the user (for authorization)

    Returns:
        bool: True if task was permanently deleted, False if not found

    Example:
        >>> success = permanently_delete_task(db, 1, user_id)
        >>> if success:
        ...     print("Task permanently deleted")
    """
    # Find task (including soft-deleted ones)
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    task = db.exec(statement).first()

    if not task:
        return False

    db.delete(task)
    db.commit()
    return True


def toggle_completion(db: Session, task_id: int, user_id: UUID) -> Optional[Task]:
    """
    Toggle task completion status with user isolation.

    For recurring tasks: when marking as complete, creates a new task instance
    with the next occurrence date calculated from the recurrence rule.

    Args:
        db: Database session
        task_id: Task ID to toggle
        user_id: UUID of the user (for authorization)

    Returns:
        Task: Updated task if found and belongs to user, None otherwise

    Example:
        >>> task = toggle_completion(db, 1, user_id)
        >>> if task:
        ...     print(f"Completed: {task.completed}")
    """
    # Find task with user isolation
    task = get_task_by_id(db, task_id, user_id)
    if not task:
        return None

    # Check if task is being marked as complete and has recurrence
    is_completing = not task.completed
    has_recurrence = task.recurrence_rule is not None and "frequency" in task.recurrence_rule

    # Toggle completion status
    task.completed = not task.completed

    # Update timestamp
    task.updated_at = datetime.now(timezone.utc)

    db.add(task)
    db.commit()
    db.refresh(task)

    # Create next occurrence for recurring tasks
    if is_completing and has_recurrence:
        _create_next_occurrence(db, task)

    return task


def _create_next_occurrence(db: Session, completed_task: Task) -> Optional[Task]:
    """
    Create the next occurrence of a recurring task.

    Calculates next due date based on recurrence rule and creates a new task
    with the same properties (title, description, priority, tags, recurrence_rule).

    Args:
        db: Database session
        completed_task: The task that was just completed

    Returns:
        Task: New task instance for next occurrence, or None if no due_date
    """
    if not completed_task.due_date or not completed_task.recurrence_rule:
        return None

    # Calculate next due date
    next_due_date = _calculate_next_occurrence(
        completed_task.due_date,
        completed_task.recurrence_rule
    )

    # Create new task for next occurrence
    next_task = Task(
        user_id=completed_task.user_id,
        title=completed_task.title,
        description=completed_task.description,
        completed=False,
        priority=completed_task.priority,
        due_date=next_due_date,
        tags=completed_task.tags,
        recurrence_rule=completed_task.recurrence_rule
    )

    db.add(next_task)
    db.commit()
    db.refresh(next_task)
    return next_task


def _calculate_next_occurrence(
    from_date: datetime,
    recurrence_rule: Dict[str, Any]
) -> datetime:
    """
    Calculate next occurrence date based on recurrence rule.

    Args:
        from_date: Starting date (current due_date)
        recurrence_rule: Dictionary with 'frequency' and 'interval' keys

    Returns:
        datetime: Next occurrence date

    Example:
        >>> rule = {"frequency": "weekly", "interval": 2}
        >>> next_date = _calculate_next_occurrence(datetime(2025, 1, 1), rule)
        >>> # Returns: 2025-01-15 (2 weeks later)
    """
    from dateutil.relativedelta import relativedelta

    frequency = recurrence_rule.get("frequency", "daily")
    interval = recurrence_rule.get("interval", 1)

    if frequency == "daily":
        return from_date + relativedelta(days=interval)
    elif frequency == "weekly":
        return from_date + relativedelta(weeks=interval)
    elif frequency == "monthly":
        return from_date + relativedelta(months=interval)
    elif frequency == "yearly":
        return from_date + relativedelta(years=interval)
    else:
        # Default to daily if unknown frequency
        return from_date + relativedelta(days=interval)


def get_upcoming_recurring_tasks(
    db: Session,
    user_id: UUID,
    limit: int = 10
) -> List[Task]:
    """
    Get upcoming recurring task occurrences for preview.

    Returns incomplete recurring tasks sorted by next due date.
    Useful for showing users what recurring tasks are coming up.

    Args:
        db: Database session
        user_id: UUID of the user
        limit: Maximum number of tasks to return

    Returns:
        List[Task]: Upcoming recurring tasks sorted by due date

    Example:
        >>> upcoming = get_upcoming_recurring_tasks(db, user_id, limit=20)
        >>> for task in upcoming:
        ...     print(f"{task.title}: {task.due_date}")
    """
    # Get all incomplete tasks with recurrence rules (excluding soft-deleted)
    statement = select(Task).where(
        Task.user_id == user_id,
        Task.completed == False,
        Task.recurrence_rule.isnot(None),
        Task.due_date.isnot(None),
        Task.deleted_at.is_(None)
    )

    tasks = db.exec(statement).all()

    # Sort by due_date (soonest first)
    tasks = sorted(tasks, key=lambda t: t.due_date if t.due_date else datetime.max.replace(tzinfo=timezone.utc))

    # Return limited results
    return tasks[:limit]

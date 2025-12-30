"""Task service layer for managing todo operations.

This module provides the TaskService class that handles all CRUD operations
for tasks using in-memory storage.
"""

from typing import Dict, List, Optional
from models.task import Task


class TaskService:
    """Service layer for task management.

    Attributes:
        _tasks: Dictionary mapping task IDs to Task objects
        _next_id: Counter for generating unique task IDs
    """

    def __init__(self):
        """Initialize TaskService with empty storage."""
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    def _validate_title(self, title: str) -> str:
        """Validate and normalize task title.

        Args:
            title: The title string to validate

        Returns:
            Stripped title string

        Raises:
            ValueError: If title is empty or whitespace-only after stripping
        """
        stripped_title = title.strip()
        if not stripped_title:
            raise ValueError("Title cannot be empty")
        return stripped_title

    def add_task(self, title: str, description: str = "") -> Task:
        """Add a new task to the task list.

        Args:
            title: Task title (required, non-empty)
            description: Optional task description (default: empty string)

        Returns:
            The newly created Task object

        Raises:
            ValueError: If title is empty or whitespace-only
        """
        validated_title = self._validate_title(title)
        task = Task(
            id=self._next_id,
            title=validated_title,
            description=description,
            completed=False
        )
        self._tasks[self._next_id] = task
        self._next_id += 1
        return task

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks sorted by ID.

        Returns:
            List of all tasks sorted by task ID (ascending)
        """
        return sorted(self._tasks.values(), key=lambda task: task.id)

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID.

        Args:
            task_id: The ID of the task to retrieve

        Returns:
            Task object if found, None otherwise
        """
        return self._tasks.get(task_id)

    def update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Update a task's title and/or description.

        Args:
            task_id: The ID of the task to update
            title: New title (if provided, must be non-empty)
            description: New description (if provided)

        Returns:
            True if update was successful

        Raises:
            ValueError: If task_id not found or title is empty/whitespace
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task #{task_id} not found")

        if title is not None:
            validated_title = self._validate_title(title)
            task.title = validated_title

        if description is not None:
            task.description = description

        return True

    def toggle_complete(self, task_id: int) -> bool:
        """Toggle a task's completion status.

        Args:
            task_id: The ID of the task to toggle

        Returns:
            New completion status (True if now complete, False if now incomplete)

        Raises:
            ValueError: If task_id not found
        """
        task = self.get_task(task_id)
        if not task:
            raise ValueError(f"Task #{task_id} not found")

        task.completed = not task.completed
        return task.completed

    def delete_task(self, task_id: int) -> bool:
        """Delete a task by ID.

        Args:
            task_id: The ID of the task to delete

        Returns:
            True if deletion was successful

        Raises:
            ValueError: If task_id not found
        """
        if task_id not in self._tasks:
            raise ValueError(f"Task #{task_id} not found")

        del self._tasks[task_id]
        return True

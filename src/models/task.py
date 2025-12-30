"""Task data model for the Todo Console Application.

This module defines the Task dataclass representing a single todo item.
"""

from dataclasses import dataclass


@dataclass
class Task:
    """Represents a single todo item.

    Attributes:
        id: Unique identifier (auto-generated, sequential)
        title: Task title (required, non-empty)
        description: Optional task description
        completed: Completion status (default: False)
    """

    id: int
    title: str
    description: str = ""
    completed: bool = False

    def __str__(self) -> str:
        """Return user-friendly string representation.

        Format: [{status}] {id}. {title}{ - description}
        where status is ✓ for completed, space for incomplete
        """
        status = "✓" if self.completed else " "
        desc_preview = f" - {self.description}" if self.description else ""
        return f"[{status}] {self.id}. {self.title}{desc_preview}"

    def __repr__(self) -> str:
        """Return developer-friendly representation."""
        return f"Task(id={self.id}, title='{self.title}', completed={self.completed})"

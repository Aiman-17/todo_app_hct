"""Main entry point for the Todo Console Application.

This module initializes the application and starts the CLI menu loop.
"""

from services.task_service import TaskService
from cli.menu import run_menu


def main():
    """Initialize and run the Todo Console Application."""
    service = TaskService()
    run_menu(service)


if __name__ == "__main__":
    main()

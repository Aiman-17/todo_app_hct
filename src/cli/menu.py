"""CLI menu and user interaction handlers for the Todo Console Application.

This module provides all CLI interface functions including menu display
and operation handlers.
"""

from services.task_service import TaskService


def handle_add_task(service: TaskService) -> None:
    """Handle the add task operation.

    Prompts user for title and description, creates the task,
    and displays success or error message.

    Args:
        service: TaskService instance to perform the operation
    """
    title = input("Enter title: ")
    description = input("Enter description (optional): ")

    try:
        task = service.add_task(title, description)
        print(f"✓ Task #{task.id} created: {task.title}")
    except ValueError as e:
        print(f"✗ Error: {e}")
    except Exception as e:
        print(f"✗ Unexpected error: {e}")


def handle_view_tasks(service: TaskService) -> None:
    """Handle the view all tasks operation.

    Displays all tasks with their ID, title, description, and completion status.
    Shows "No tasks found." if the list is empty.

    Args:
        service: TaskService instance to perform the operation
    """
    tasks = service.get_all_tasks()

    if not tasks:
        print("\nNo tasks found.")
    else:
        print("\nYour Tasks:")
        print()
        for task in tasks:
            print(str(task))
        print()
        print("Legend:")
        print("[ ] = Incomplete")
        print("[✓] = Complete")


def handle_update_task(service: TaskService) -> None:
    """Handle the update task operation.

    Prompts user for task ID, displays current task, then prompts for new values.
    Empty inputs keep current values.

    Args:
        service: TaskService instance to perform the operation
    """
    try:
        task_id_input = input("\nEnter task ID: ")
        task_id = int(task_id_input)
    except ValueError:
        print("✗ Error: Invalid task ID")
        return

    task = service.get_task(task_id)
    if not task:
        print(f"✗ Error: Task #{task_id} not found")
        return

    # Display current task
    desc_part = f" - {task.description}" if task.description else ""
    print(f"Current task: {task.title}{desc_part}")
    print()

    # Prompt for new values
    new_title = input("Enter new title (press Enter to keep current): ")
    new_description = input("Enter new description (press Enter to keep current): ")

    # Only pass non-empty values
    title_to_update = new_title if new_title.strip() else None
    desc_to_update = new_description if new_description else None

    try:
        service.update_task(task_id, title=title_to_update, description=desc_to_update)
        print(f"\n✓ Task #{task_id} updated")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def display_menu() -> None:
    """Display the main menu."""
    print("\n=== Todo Application ===")
    print("1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")
    print()


def get_menu_choice() -> str:
    """Get menu choice from user.

    Returns:
        User's menu choice as string
    """
    return input("Enter choice (1-6): ")


def handle_exit() -> bool:
    """Handle exit confirmation.

    Prompts user to confirm exit and warns about data loss.

    Returns:
        True if user confirms exit, False if cancelled
    """
    while True:
        confirmation = input("\nExit? All tasks will be lost. [Y/N]: ")
        if confirmation.upper() == "Y":
            print("\nGoodbye!")
            return True
        elif confirmation.upper() == "N":
            return False
        else:
            print("✗ Invalid input. Please enter Y or N.")


def run_menu(service: TaskService) -> None:
    """Run the main menu loop.

    Displays menu, gets user choice, and dispatches to appropriate handler.
    Loops until user chooses to exit.

    Args:
        service: TaskService instance for all operations
    """
    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            handle_add_task(service)
        elif choice == "2":
            handle_view_tasks(service)
        elif choice == "3":
            handle_update_task(service)
        elif choice == "4":
            handle_delete_task(service)
        elif choice == "5":
            handle_toggle_complete(service)
        elif choice == "6":
            if handle_exit():
                break
        else:
            print("\n✗ Invalid choice. Please enter a number between 1 and 6.")


def handle_toggle_complete(service: TaskService) -> None:
    """Handle the toggle completion status operation.

    Prompts user for task ID and toggles its completion status.

    Args:
        service: TaskService instance to perform the operation
    """
    try:
        task_id_input = input("\nEnter task ID: ")
        task_id = int(task_id_input)
    except ValueError:
        print("✗ Error: Invalid task ID")
        return

    try:
        is_complete = service.toggle_complete(task_id)
        status_msg = "complete" if is_complete else "incomplete"
        print(f"\n✓ Task #{task_id} marked as {status_msg}")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def handle_delete_task(service: TaskService) -> None:
    """Handle the delete task operation.

    Prompts user for task ID and deletes the task.

    Args:
        service: TaskService instance to perform the operation
    """
    try:
        task_id_input = input("\nEnter task ID: ")
        task_id = int(task_id_input)
    except ValueError:
        print("✗ Error: Invalid task ID")
        return

    try:
        service.delete_task(task_id)
        print(f"\n✓ Task #{task_id} deleted")
    except ValueError as e:
        print(f"\n✗ Error: {e}")

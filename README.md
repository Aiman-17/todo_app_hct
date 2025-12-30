# Todo Console Application - Phase I

A simple, in-memory Python console application for managing todo tasks.

## Features

- ✅ Add tasks with title and optional description
- ✅ View all tasks with completion status
- ✅ Update task title and description
- ✅ Delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Exit confirmation to prevent accidental data loss

## Requirements

- Python 3.13 or higher
- No external dependencies (standard library only)

## Installation

```bash
# Clone the repository
git clone <repository-url>
cd todo_app_hct

# Verify Python version
python --version  # Should show Python 3.13.x or higher
```

## Running the Application

```bash
# Navigate to the src directory
cd src

# Run the application
python main.py
```

## Usage

The application presents a numbered menu with 6 options:

```
=== Todo Application ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6):
```

### Example Session

```bash
$ cd src
$ python main.py

=== Todo Application ===
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter choice (1-6): 1
Enter title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task #1 created: Buy groceries

Enter choice (1-6): 2

Your Tasks:
[ ] 1. Buy groceries - Milk, eggs, bread

Legend:
[ ] = Incomplete
[✓] = Complete

Enter choice (1-6): 5
Enter task ID: 1

✓ Task #1 marked as complete

Enter choice (1-6): 6

Exit? All tasks will be lost. [Y/N]: Y

Goodbye!
```

## Important Notes

⚠️ **Data is not persisted!** All tasks are stored in memory and will be lost when you exit the application. This is intentional for Phase I.

## Project Structure

```
todo_app_hct/
├── src/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py          # Task data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── task_service.py  # Business logic & CRUD operations
│   └── cli/
│       ├── __init__.py
│       └── menu.py           # CLI interface handlers
├── specs/                    # Specifications and planning docs
├── tests/                    # Test directory (future use)
└── README.md
```

## Development

This project follows spec-driven development principles. See `specs/001-phase1-console/` for:
- `spec.md` - Feature specification
- `plan.md` - Implementation plan
- `tasks.md` - Task breakdown
- `data-model.md` - Data structures
- `contracts/cli-interface.md` - CLI specifications

## Future Phases

- **Phase II**: Web interface (Next.js + FastAPI) with PostgreSQL persistence
- **Phase III**: AI chatbot interface (OpenAI Agents + MCP)
- **Phase IV**: Local Kubernetes deployment (Minikube)
- **Phase V**: Cloud deployment (DOKS/GKE/AKS with Kafka and Dapr)

## License

[Add your license here]

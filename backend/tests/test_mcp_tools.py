"""
Phase III: Unit tests for MCP tools (Model Context Protocol).

Critical tests for user isolation, data validation, and proper error handling.
"""
import pytest
from uuid import uuid4
from datetime import datetime, timezone
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.models.task import Task
from src.models.user import User
from src.mcp.task_tools import (
    add_task,
    list_tasks,
    update_task,
    complete_task,
    delete_task
)


@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="test_users")
def test_users_fixture(session: Session):
    """Create test users for isolation testing."""
    user1 = User(
        id=uuid4(),
        email="user1@test.com",
        name="User One",
        password_hash="hashed_password_1"
    )
    user2 = User(
        id=uuid4(),
        email="user2@test.com",
        name="User Two",
        password_hash="hashed_password_2"
    )
    session.add(user1)
    session.add(user2)
    session.commit()
    session.refresh(user1)
    session.refresh(user2)
    return {"user1": user1, "user2": user2}


class TestAddTask:
    """Tests for add_task MCP tool."""

    def test_add_task_success(self, session: Session, test_users):
        """Test successful task creation."""
        user_id = str(test_users["user1"].id)

        result = add_task(
            db=session,
            user_id=user_id,
            title="Buy groceries",
            description="Milk, bread, eggs"
        )

        assert result["success"] is True
        assert result["task"]["title"] == "Buy groceries"
        assert result["task"]["description"] == "Milk, bread, eggs"
        assert result["task"]["completed"] is False
        assert "id" in result["task"]

    def test_add_task_minimal_fields(self, session: Session, test_users):
        """Test task creation with only required fields."""
        user_id = str(test_users["user1"].id)

        result = add_task(
            db=session,
            user_id=user_id,
            title="Simple task"
        )

        assert result["success"] is True
        assert result["task"]["title"] == "Simple task"
        assert result["task"]["description"] == ""

    def test_add_task_empty_title_fails(self, session: Session, test_users):
        """Test that empty title is rejected."""
        user_id = str(test_users["user1"].id)

        result = add_task(
            db=session,
            user_id=user_id,
            title=""
        )

        assert result["success"] is False
        assert "error" in result
        assert "title" in result["error"].lower()


class TestListTasks:
    """Tests for list_tasks MCP tool - CRITICAL for user isolation."""

    def test_list_tasks_user_isolation(self, session: Session, test_users):
        """
        CRITICAL SECURITY TEST: Verify users can only see their own tasks.

        This test ensures user isolation is enforced at the MCP tool level.
        Failure of this test indicates a critical security vulnerability.
        """
        user1_id = str(test_users["user1"].id)
        user2_id = str(test_users["user2"].id)

        # User 1 creates tasks
        add_task(session, user1_id, "User 1 Task 1")
        add_task(session, user1_id, "User 1 Task 2")

        # User 2 creates tasks
        add_task(session, user2_id, "User 2 Task 1")
        add_task(session, user2_id, "User 2 Task 2")

        # User 1 lists tasks
        user1_result = list_tasks(session, user1_id)
        assert user1_result["success"] is True
        assert len(user1_result["tasks"]) == 2
        for task in user1_result["tasks"]:
            assert "User 1" in task["title"]

        # User 2 lists tasks
        user2_result = list_tasks(session, user2_id)
        assert user2_result["success"] is True
        assert len(user2_result["tasks"]) == 2
        for task in user2_result["tasks"]:
            assert "User 2" in task["title"]

    def test_list_tasks_empty(self, session: Session, test_users):
        """Test listing tasks when user has no tasks."""
        user_id = str(test_users["user1"].id)

        result = list_tasks(session, user_id)

        assert result["success"] is True
        assert result["tasks"] == []

    def test_list_tasks_filter_by_status(self, session: Session, test_users):
        """Test filtering tasks by completion status."""
        user_id = str(test_users["user1"].id)

        # Create tasks
        task1 = add_task(session, user_id, "Pending task")
        task2 = add_task(session, user_id, "Completed task")
        complete_task(session, user_id, task2["task"]["id"])

        # List pending only
        pending_result = list_tasks(session, user_id, status="pending")
        assert len(pending_result["tasks"]) == 1
        assert pending_result["tasks"][0]["completed"] is False

        # List completed only
        completed_result = list_tasks(session, user_id, status="completed")
        assert len(completed_result["tasks"]) == 1
        assert completed_result["tasks"][0]["completed"] is True


class TestCompleteTask:
    """Tests for complete_task MCP tool."""

    def test_complete_task_success(self, session: Session, test_users):
        """Test successfully marking task as complete."""
        user_id = str(test_users["user1"].id)

        # Create task
        task_result = add_task(session, user_id, "Task to complete")
        task_id = task_result["task"]["id"]

        # Complete it
        result = complete_task(session, user_id, task_id)

        assert result["success"] is True
        assert result["task"]["completed"] is True

    def test_complete_task_cross_user_forbidden(self, session: Session, test_users):
        """
        CRITICAL SECURITY TEST: Verify users cannot complete other users' tasks.
        """
        user1_id = str(test_users["user1"].id)
        user2_id = str(test_users["user2"].id)

        # User 1 creates task
        task_result = add_task(session, user1_id, "User 1 task")
        task_id = task_result["task"]["id"]

        # User 2 tries to complete User 1's task
        result = complete_task(session, user2_id, task_id)

        assert result["success"] is False
        assert "not found" in result["error"].lower()

    def test_complete_task_not_found(self, session: Session, test_users):
        """Test completing non-existent task."""
        user_id = str(test_users["user1"].id)

        result = complete_task(session, user_id, task_id=99999)

        assert result["success"] is False
        assert "not found" in result["error"].lower()


class TestUpdateTask:
    """Tests for update_task MCP tool."""

    def test_update_task_title_and_description(self, session: Session, test_users):
        """Test updating task title and description."""
        user_id = str(test_users["user1"].id)

        # Create task
        task_result = add_task(session, user_id, "Original title", "Original description")
        task_id = task_result["task"]["id"]

        # Update it
        result = update_task(
            session, user_id, task_id,
            title="Updated title",
            description="Updated description"
        )

        assert result["success"] is True
        assert result["task"]["title"] == "Updated title"
        assert result["task"]["description"] == "Updated description"

    def test_update_task_cross_user_forbidden(self, session: Session, test_users):
        """
        CRITICAL SECURITY TEST: Verify users cannot update other users' tasks.
        """
        user1_id = str(test_users["user1"].id)
        user2_id = str(test_users["user2"].id)

        # User 1 creates task
        task_result = add_task(session, user1_id, "User 1 task")
        task_id = task_result["task"]["id"]

        # User 2 tries to update User 1's task
        result = update_task(session, user2_id, task_id, title="Malicious update")

        assert result["success"] is False
        assert "not found" in result["error"].lower()


class TestDeleteTask:
    """Tests for delete_task MCP tool."""

    def test_delete_task_success(self, session: Session, test_users):
        """Test successfully deleting a task."""
        user_id = str(test_users["user1"].id)

        # Create task
        task_result = add_task(session, user_id, "Task to delete")
        task_id = task_result["task"]["id"]

        # Delete it
        result = delete_task(session, user_id, task_id)

        assert result["success"] is True

        # Verify it's gone
        list_result = list_tasks(session, user_id)
        assert len(list_result["tasks"]) == 0

    def test_delete_task_cross_user_forbidden(self, session: Session, test_users):
        """
        CRITICAL SECURITY TEST: Verify users cannot delete other users' tasks.
        """
        user1_id = str(test_users["user1"].id)
        user2_id = str(test_users["user2"].id)

        # User 1 creates task
        task_result = add_task(session, user1_id, "User 1 task")
        task_id = task_result["task"]["id"]

        # User 2 tries to delete User 1's task
        result = delete_task(session, user2_id, task_id)

        assert result["success"] is False
        assert "not found" in result["error"].lower()

        # Verify User 1's task still exists
        list_result = list_tasks(session, user1_id)
        assert len(list_result["tasks"]) == 1


class TestUserIsolationComprehensive:
    """Comprehensive user isolation test suite."""

    def test_complete_user_isolation_scenario(self, session: Session, test_users):
        """
        End-to-end user isolation test covering all MCP operations.

        This test simulates two users performing various operations
        and verifies complete isolation at every step.
        """
        user1_id = str(test_users["user1"].id)
        user2_id = str(test_users["user2"].id)

        # User 1: Create 3 tasks
        user1_tasks = []
        for i in range(3):
            result = add_task(session, user1_id, f"User 1 Task {i+1}")
            user1_tasks.append(result["task"]["id"])

        # User 2: Create 2 tasks
        user2_tasks = []
        for i in range(2):
            result = add_task(session, user2_id, f"User 2 Task {i+1}")
            user2_tasks.append(result["task"]["id"])

        # User 1: List tasks (should see only their 3)
        result = list_tasks(session, user1_id)
        assert len(result["tasks"]) == 3

        # User 2: List tasks (should see only their 2)
        result = list_tasks(session, user2_id)
        assert len(result["tasks"]) == 2

        # User 1: Try to complete User 2's task (should fail)
        result = complete_task(session, user1_id, user2_tasks[0])
        assert result["success"] is False

        # User 2: Try to delete User 1's task (should fail)
        result = delete_task(session, user2_id, user1_tasks[0])
        assert result["success"] is False

        # User 1: Complete their own task (should succeed)
        result = complete_task(session, user1_id, user1_tasks[0])
        assert result["success"] is True

        # User 2: Update their own task (should succeed)
        result = update_task(session, user2_id, user2_tasks[0], title="Updated by User 2")
        assert result["success"] is True
        assert result["task"]["title"] == "Updated by User 2"

        # Final verification: Each user still has only their tasks
        user1_final = list_tasks(session, user1_id)
        user2_final = list_tasks(session, user2_id)
        assert len(user1_final["tasks"]) == 3
        assert len(user2_final["tasks"]) == 2

"""
Pytest configuration and fixtures for backend testing.

Provides reusable fixtures for:
- In-memory SQLite database sessions
- FastAPI TestClient with database override
- Test user creation with known credentials
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from typing import Generator

from src.main import app
from src.dependencies import get_db_session
from src.models.user import User
from src.services.auth_service import hash_password


# In-memory SQLite database for testing (isolated, no persistence)
SQLITE_TEST_DATABASE_URL = "sqlite:///:memory:"

# Create test engine with SQLite in-memory
test_engine = create_engine(
    SQLITE_TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},  # SQLite specific
    poolclass=StaticPool,  # Single connection pool for in-memory DB
)


@pytest.fixture(name="db_session", scope="function")
def db_session_fixture() -> Generator[Session, None, None]:
    """
    Pytest fixture providing an in-memory SQLite database session.

    Creates all tables before each test and drops them after.
    Ensures test isolation (each test gets a fresh database).

    Yields:
        Session: SQLModel database session for testing

    Example:
        def test_create_user(db_session: Session):
            user = User(email="test@example.com", name="Test", password_hash="...")
            db_session.add(user)
            db_session.commit()
            assert user.id is not None
    """
    # Create all tables
    SQLModel.metadata.create_all(test_engine)

    # Create session
    with Session(test_engine) as session:
        yield session

    # Drop all tables after test
    SQLModel.metadata.drop_all(test_engine)


@pytest.fixture(name="client", scope="function")
def client_fixture(db_session: Session) -> Generator[TestClient, None, None]:
    """
    Pytest fixture providing a FastAPI TestClient with database override.

    Overrides the get_session dependency to use the in-memory test database
    instead of the production Neon database.

    Args:
        db_session: In-memory database session from db_session_fixture

    Returns:
        TestClient: FastAPI test client for making API requests

    Example:
        def test_health_check(client: TestClient):
            response = client.get("/api/health")
            assert response.status_code == 200
            assert response.json()["status"] == "healthy"
    """
    def get_db_session_override():
        """Override get_db_session to use test database."""
        try:
            yield db_session
        finally:
            pass  # Don't close session here, let db_session fixture handle it

    # Override dependency
    app.dependency_overrides[get_db_session] = get_db_session_override

    # Create test client
    client = TestClient(app)
    yield client

    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture(name="test_user", scope="function")
def test_user_fixture(db_session: Session) -> User:
    """
    Pytest fixture providing a pre-created test user with known credentials.

    Creates a user in the test database with:
    - Email: test@example.com
    - Name: Test User
    - Password: TestPass123 (hashed with bcrypt)

    Args:
        db_session: In-memory database session from db_session_fixture

    Returns:
        User: The created user model (with id populated)

    Example:
        def test_login(client: TestClient, test_user: User):
            response = client.post("/api/auth/login", json={
                "email": "test@example.com",
                "password": "TestPass123"
            })
            assert response.status_code == 200
    """
    user = User(
        email="test@example.com",
        name="Test User",
        password_hash=hash_password("TestPass123")
    )
    db_session.add(user)
    db_session.commit()
    db_session.refresh(user)
    return user

"""
Integration tests for authentication API endpoints.

Tests signup, login, and profile retrieval with FastAPI TestClient.
"""
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from src.models.user import User


def test_signup_success(client: TestClient, db_session: Session):
    """Test successful user signup with valid credentials."""
    response = client.post("/api/auth/signup", json={
        "email": "alice@example.com",
        "name": "Alice Smith",
        "password": "SecurePass123"
    })

    assert response.status_code == 201
    data = response.json()

    # Verify user data in response
    assert "user" in data
    assert data["user"]["email"] == "alice@example.com"
    assert data["user"]["name"] == "Alice Smith"
    assert "id" in data["user"]
    assert "created_at" in data["user"]

    # Verify tokens in response
    assert "tokens" in data
    assert "access_token" in data["tokens"]
    assert "refresh_token" in data["tokens"]
    assert data["tokens"]["token_type"] == "bearer"
    assert data["tokens"]["expires_in"] == 3600  # 1 hour (changed from 900/15 minutes)

    # Verify user was created in database
    from sqlmodel import select
    user = db_session.exec(
        select(User).where(User.email == "alice@example.com")
    ).first()
    assert user is not None
    assert user.name == "Alice Smith"


def test_signup_duplicate_email(client: TestClient, test_user: User):
    """Test that signup fails with duplicate email address."""
    # test_user fixture already created test@example.com
    response = client.post("/api/auth/signup", json={
        "email": "test@example.com",  # Duplicate email
        "name": "Another User",
        "password": "SecurePass123"
    })

    assert response.status_code == 400
    assert "already registered" in response.json()["detail"].lower()


def test_signup_invalid_password(client: TestClient):
    """Test that signup fails with invalid password (missing requirements)."""
    # Missing uppercase letter
    response = client.post("/api/auth/signup", json={
        "email": "alice@example.com",
        "name": "Alice Smith",
        "password": "securepass123"
    })
    assert response.status_code == 422
    assert "uppercase" in str(response.json()).lower()

    # Too short
    response = client.post("/api/auth/signup", json={
        "email": "alice@example.com",
        "name": "Alice Smith",
        "password": "Short1"
    })
    assert response.status_code == 422
    assert "8 characters" in str(response.json()).lower()

    # Missing number
    response = client.post("/api/auth/signup", json={
        "email": "alice@example.com",
        "name": "Alice Smith",
        "password": "SecurePass"
    })
    assert response.status_code == 422
    assert "number" in str(response.json()).lower()


def test_login_success(client: TestClient, test_user: User):
    """Test successful login with valid credentials."""
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123"
    })

    assert response.status_code == 200
    data = response.json()

    # Verify tokens in response
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"
    assert data["expires_in"] == 3600  # 1 hour (changed from 900/15 minutes)


def test_login_invalid_credentials(client: TestClient, test_user: User):
    """Test that login fails with incorrect password or non-existent email."""
    # Wrong password
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "WrongPass123"
    })
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()

    # Non-existent email
    response = client.post("/api/auth/login", json={
        "email": "nonexistent@example.com",
        "password": "TestPass123"
    })
    assert response.status_code == 401
    assert "invalid" in response.json()["detail"].lower()


def test_get_profile_authenticated(client: TestClient, test_user: User):
    """Test getting user profile with valid authentication token."""
    # First login to get token
    login_response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123"
    })
    access_token = login_response.json()["access_token"]

    # Get profile with token
    response = client.get(
        "/api/auth/profile",
        headers={"Authorization": f"Bearer {access_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data
    assert "created_at" in data


def test_get_profile_unauthenticated(client: TestClient):
    """Test that profile endpoint rejects requests without authentication."""
    # No Authorization header
    response = client.get("/api/auth/profile")
    assert response.status_code == 401

    # Invalid token
    response = client.get(
        "/api/auth/profile",
        headers={"Authorization": "Bearer invalid.token.here"}
    )
    assert response.status_code == 401

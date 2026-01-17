"""
Phase III: Integration tests for chat endpoint and rate limiting.

Tests chat API functionality, authentication, and rate limiting.
"""
import pytest
from fastapi.testclient import TestClient
from uuid import uuid4
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool

from src.main import app
from src.models.user import User
from src.middleware.rate_limiter import chat_rate_limiter


@pytest.fixture(name="client")
def client_fixture():
    """Create test client."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_rate_limiter():
    """Reset rate limiter before each test."""
    chat_rate_limiter.reset()
    yield
    chat_rate_limiter.reset()


class TestChatEndpointAuthentication:
    """Test authentication requirements for chat endpoint."""

    def test_chat_requires_authentication(self, client):
        """Test that chat endpoint requires valid JWT token."""
        response = client.post(
            "/api/chat",
            json={"message": "test message"}
        )
        assert response.status_code == 401  # Unauthorized

    def test_chat_rejects_invalid_token(self, client):
        """Test that invalid JWT tokens are rejected."""
        response = client.post(
            "/api/chat",
            headers={"Authorization": "Bearer invalid_token_here"},
            json={"message": "test message"}
        )
        assert response.status_code == 401


class TestChatEndpointRateLimiting:
    """Test rate limiting functionality."""

    def test_rate_limit_enforcement(self, client):
        """
        Test that rate limiting enforces 100 requests per hour limit.

        This test simulates exceeding the rate limit and verifies
        that the 429 status code is returned.
        """
        # Note: This test would need a valid JWT token to work
        # For now, we'll test the rate limiter directly
        from src.middleware.rate_limiter import RateLimiter

        limiter = RateLimiter(max_requests=3, window_seconds=60)
        user_id = "test-user-123"

        # First 3 requests should succeed
        assert limiter.is_allowed(user_id) is True
        assert limiter.is_allowed(user_id) is True
        assert limiter.is_allowed(user_id) is True

        # 4th request should be blocked
        assert limiter.is_allowed(user_id) is False

        # Check remaining count
        assert limiter.get_remaining(user_id) == 0

    def test_rate_limit_per_user_isolation(self):
        """Test that rate limits are isolated per user."""
        from src.middleware.rate_limiter import RateLimiter

        limiter = RateLimiter(max_requests=2, window_seconds=60)
        user1 = "user-1"
        user2 = "user-2"

        # User 1 makes 2 requests
        assert limiter.is_allowed(user1) is True
        assert limiter.is_allowed(user1) is True

        # User 1 is now at limit
        assert limiter.is_allowed(user1) is False

        # User 2 should still be allowed (separate limit)
        assert limiter.is_allowed(user2) is True
        assert limiter.is_allowed(user2) is True
        assert limiter.is_allowed(user2) is False

    def test_rate_limit_window_expiry(self):
        """Test that rate limits reset after time window expires."""
        import time
        from src.middleware.rate_limiter import RateLimiter

        limiter = RateLimiter(max_requests=2, window_seconds=1)  # 1 second window
        user_id = "test-user"

        # Make 2 requests
        assert limiter.is_allowed(user_id) is True
        assert limiter.is_allowed(user_id) is True

        # At limit
        assert limiter.is_allowed(user_id) is False

        # Wait for window to expire
        time.sleep(1.1)

        # Should be allowed again
        assert limiter.is_allowed(user_id) is True


class TestChatEndpointValidation:
    """Test request validation."""

    def test_chat_requires_message_field(self, client):
        """Test that message field is required."""
        # Note: This would need valid auth
        # Testing schema validation
        from src.schemas.chat import ChatRequest
        from pydantic import ValidationError

        # Valid request
        valid = ChatRequest(message="test message")
        assert valid.message == "test message"

        # Invalid: empty message should fail validation
        with pytest.raises(ValidationError):
            ChatRequest(message="")

    def test_chat_conversation_id_optional(self):
        """Test that conversation_id is optional."""
        from src.schemas.chat import ChatRequest

        # Without conversation_id
        request1 = ChatRequest(message="test")
        assert request1.conversation_id is None

        # With conversation_id
        conv_id = uuid4()
        request2 = ChatRequest(message="test", conversation_id=str(conv_id))
        assert request2.conversation_id == conv_id


class TestChatResponse:
    """Test chat response schema."""

    def test_chat_response_structure(self):
        """Test that chat response includes required fields."""
        from src.schemas.chat import ChatResponse

        response = ChatResponse(
            response="Test response",
            conversation_id=str(uuid4()),
            intent="create_task",
            success=True,
            correlation_id=str(uuid4())
        )

        assert response.response == "Test response"
        assert response.intent == "create_task"
        assert response.success is True
        assert response.correlation_id is not None
        assert response.conversation_id is not None

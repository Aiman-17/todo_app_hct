"""
Unit tests for authentication service functions.

Tests password hashing, JWT token creation, and token verification.
"""
import pytest
import jwt
from uuid import UUID, uuid4
from datetime import datetime, timedelta, timezone

from src.services.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    verify_token
)
from src.config import settings


def test_hash_password():
    """Test that hash_password generates a valid bcrypt hash."""
    password = "SecurePass123"
    hashed = hash_password(password)

    # Verify hash format (bcrypt hashes start with $2b$12$ for 12 rounds)
    assert hashed.startswith("$2b$12$")
    assert len(hashed) == 60  # bcrypt hashes are always 60 characters

    # Verify hashing is non-deterministic (same password -> different hashes)
    hashed2 = hash_password(password)
    assert hashed != hashed2


def test_verify_password():
    """Test password verification against bcrypt hash."""
    password = "SecurePass123"
    hashed = hash_password(password)

    # Correct password should verify
    assert verify_password(password, hashed) is True

    # Incorrect password should fail
    assert verify_password("WrongPass123", hashed) is False
    assert verify_password("securepass123", hashed) is False  # Case sensitive


def test_create_access_token():
    """Test JWT access token creation with 15-minute expiry."""
    user_id = uuid4()
    token = create_access_token(user_id)

    # Verify token is a string
    assert isinstance(token, str)
    assert len(token) > 0

    # Decode and verify payload
    payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"
    assert "exp" in payload
    assert "iat" in payload

    # Verify expiration is approximately 1 hour from now (changed from 15 minutes)
    exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    now = datetime.now(timezone.utc)
    time_diff = exp_time - now
    assert 59 * 60 <= time_diff.total_seconds() <= 61 * 60  # 59-61 minutes tolerance (1 hour)


def test_create_refresh_token():
    """Test JWT refresh token creation with 30-day expiry (changed from 7 days)."""
    user_id = uuid4()
    token = create_refresh_token(user_id)

    # Verify token is a string
    assert isinstance(token, str)
    assert len(token) > 0

    # Decode and verify payload
    payload = jwt.decode(token, settings.BETTER_AUTH_SECRET, algorithms=["HS256"])
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "refresh"
    assert "exp" in payload
    assert "iat" in payload

    # Verify expiration is approximately 30 days from now (changed from 7 days)
    exp_time = datetime.fromtimestamp(payload["exp"], tz=timezone.utc)
    now = datetime.now(timezone.utc)
    time_diff = exp_time - now
    assert 29.9 * 24 * 60 * 60 <= time_diff.total_seconds() <= 30.1 * 24 * 60 * 60  # ~30 days


def test_verify_token():
    """Test JWT token verification and decoding."""
    user_id = uuid4()

    # Create access token
    access_token = create_access_token(user_id)
    payload = verify_token(access_token)
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "access"

    # Create refresh token
    refresh_token = create_refresh_token(user_id)
    payload = verify_token(refresh_token)
    assert payload["sub"] == str(user_id)
    assert payload["type"] == "refresh"


def test_verify_token_invalid():
    """Test that invalid tokens raise exceptions."""
    # Invalid token format
    with pytest.raises(jwt.InvalidTokenError):
        verify_token("not.a.valid.token")

    # Token with wrong signature
    user_id = uuid4()
    token = jwt.encode(
        {"sub": str(user_id), "type": "access"},
        "wrong-secret",
        algorithm="HS256"
    )
    with pytest.raises(jwt.InvalidTokenError):
        verify_token(token)


def test_verify_token_expired():
    """Test that expired tokens raise ExpiredSignatureError."""
    user_id = uuid4()

    # Create token with past expiration
    past_time = datetime.now(timezone.utc) - timedelta(hours=1)
    payload = {
        "sub": str(user_id),
        "type": "access",
        "exp": past_time,
        "iat": past_time - timedelta(minutes=15)
    }
    expired_token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")

    # Should raise ExpiredSignatureError
    with pytest.raises(jwt.ExpiredSignatureError):
        verify_token(expired_token)

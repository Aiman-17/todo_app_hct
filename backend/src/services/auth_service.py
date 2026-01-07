"""
Authentication service for password hashing and JWT token management.

Provides bcrypt password hashing with 12 salt rounds and JWT token generation
with configurable expiration times (15-min access, 7-day refresh).
"""
import bcrypt
import jwt
from datetime import datetime, timedelta, timezone
from uuid import UUID
from typing import Dict, Any

from src.config import settings


def hash_password(password: str) -> str:
    """
    Hash a plaintext password using bcrypt with 12 salt rounds.

    Args:
        password: The plaintext password to hash

    Returns:
        The bcrypt hashed password as a string

    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> hashed.startswith("$2b$12$")
        True
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(password: str, hashed: str) -> bool:
    """
    Verify a plaintext password against a bcrypt hash.

    Args:
        password: The plaintext password to verify
        hashed: The bcrypt hashed password

    Returns:
        True if password matches hash, False otherwise

    Example:
        >>> hashed = hash_password("SecurePass123")
        >>> verify_password("SecurePass123", hashed)
        True
        >>> verify_password("WrongPass123", hashed)
        False
    """
    password_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(user_id: UUID) -> str:
    """
    Create a JWT access token with 1-hour expiration.

    Args:
        user_id: The UUID of the user

    Returns:
        JWT access token as a string

    Token Payload:
        - sub: user_id (string)
        - type: "access"
        - exp: expiration timestamp (1 hour from now)
        - iat: issued at timestamp

    Example:
        >>> from uuid import UUID
        >>> user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        >>> token = create_access_token(user_id)
        >>> isinstance(token, str)
        True
    """
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(hours=1)  # Changed from 15 minutes to 1 hour

    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "access",
        "exp": expiration,
        "iat": now
    }

    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return token


def create_refresh_token(user_id: UUID) -> str:
    """
    Create a JWT refresh token with 30-day expiration.

    Args:
        user_id: The UUID of the user

    Returns:
        JWT refresh token as a string

    Token Payload:
        - sub: user_id (string)
        - type: "refresh"
        - exp: expiration timestamp (30 days from now)
        - iat: issued at timestamp

    Example:
        >>> from uuid import UUID
        >>> user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        >>> token = create_refresh_token(user_id)
        >>> isinstance(token, str)
        True
    """
    now = datetime.now(timezone.utc)
    expiration = now + timedelta(days=30)  # Changed from 7 days to 30 days

    payload: Dict[str, Any] = {
        "sub": str(user_id),
        "type": "refresh",
        "exp": expiration,
        "iat": now
    }

    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm="HS256")
    return token


def verify_token(token: str) -> Dict[str, Any]:
    """
    Verify and decode a JWT token.

    Args:
        token: The JWT token to verify

    Returns:
        Decoded token payload as a dictionary

    Raises:
        jwt.ExpiredSignatureError: If token has expired
        jwt.InvalidTokenError: If token is invalid or signature verification fails

    Example:
        >>> from uuid import UUID
        >>> user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        >>> token = create_access_token(user_id)
        >>> payload = verify_token(token)
        >>> payload["sub"] == str(user_id)
        True
        >>> payload["type"] == "access"
        True
    """
    payload = jwt.decode(
        token,
        settings.BETTER_AUTH_SECRET,
        algorithms=["HS256"]
    )
    return payload

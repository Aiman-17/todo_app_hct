"""
Pydantic schemas for authentication API requests and responses.

Provides validation for user signup, login, and response payloads.
"""
from pydantic import BaseModel, EmailStr, field_validator, ConfigDict
from uuid import UUID
from datetime import datetime
import re


class UserCreate(BaseModel):
    """
    Schema for user registration (signup) request.

    Validates email format, name, and password requirements.
    """

    email: EmailStr
    name: str
    password: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v: str) -> str:
        """Validate name is non-empty and within length limits."""
        v = v.strip()
        if not v:
            raise ValueError("Name cannot be empty")
        if len(v) > 255:
            raise ValueError("Name too long (max 255 characters)")
        return v

    @field_validator('password')
    @classmethod
    def validate_password(cls, v: str) -> str:
        """
        Validate password meets security requirements.

        Requirements:
            - Minimum 8 characters
            - At least one uppercase letter (A-Z)
            - At least one lowercase letter (a-z)
            - At least one number (0-9)
        """
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        if not re.search(r'[A-Z]', v):
            raise ValueError("Password must include an uppercase letter")
        if not re.search(r'[a-z]', v):
            raise ValueError("Password must include a lowercase letter")
        if not re.search(r'[0-9]', v):
            raise ValueError("Password must include a number")
        return v

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "alice@example.com",
                "name": "Alice Smith",
                "password": "SecurePass123"
            }
        }
    )


class UserLogin(BaseModel):
    """Schema for user login request."""

    email: EmailStr
    password: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "email": "alice@example.com",
                "password": "SecurePass123"
            }
        }
    )


class RefreshTokenRequest(BaseModel):
    """Schema for token refresh request."""

    refresh_token: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
            }
        }
    )


class UserResponse(BaseModel):
    """
    Schema for user profile response (no password).

    Returns user information after successful signup or profile retrieval.
    """

    id: UUID
    email: str
    name: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True,  # Enable ORM mode for SQLModel → Pydantic conversion
        json_schema_extra={
            "example": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "alice@example.com",
                "name": "Alice Smith",
                "created_at": "2025-12-30T10:00:00Z"
            }
        }
    )


class TokenResponse(BaseModel):
    """
    Schema for JWT token response after successful login.

    Returns access token (1-hour expiry) and refresh token (30-day expiry).
    """

    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int = 3600  # 1 hour in seconds (changed from 900/15 minutes)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 3600
            }
        }
    )

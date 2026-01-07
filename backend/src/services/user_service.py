"""
User service for database operations on User model.

Provides functions for creating users, querying by email or ID,
and managing user authentication data.
"""
from sqlmodel import Session, select
from uuid import UUID
from typing import Optional

from src.models.user import User
from src.services.auth_service import hash_password


def create_user(db: Session, email: str, name: str, password: str) -> User:
    """
    Create a new user with hashed password.

    Args:
        db: Database session
        email: User email address (must be unique)
        name: User display name
        password: Plaintext password (will be hashed with bcrypt)

    Returns:
        User: The created user model with id populated

    Raises:
        IntegrityError: If email already exists (unique constraint)

    Example:
        >>> user = create_user(db, "alice@example.com", "Alice Smith", "SecurePass123")
        >>> user.id  # UUID generated
        >>> user.password_hash  # bcrypt hash, not plaintext
    """
    # Hash password with bcrypt (12 rounds)
    password_hash = hash_password(password)

    # Create user model
    user = User(
        email=email,
        name=name,
        password_hash=password_hash
    )

    # Add to database
    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """
    Retrieve a user by email address.

    Args:
        db: Database session
        email: User email address to search for

    Returns:
        User if found, None otherwise

    Example:
        >>> user = get_user_by_email(db, "alice@example.com")
        >>> if user:
        ...     print(user.name)
    """
    statement = select(User).where(User.email == email)
    user = db.exec(statement).first()
    return user


def get_user_by_id(db: Session, user_id: UUID) -> Optional[User]:
    """
    Retrieve a user by UUID.

    Args:
        db: Database session
        user_id: User UUID to search for

    Returns:
        User if found, None otherwise

    Example:
        >>> from uuid import UUID
        >>> user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
        >>> user = get_user_by_id(db, user_id)
        >>> if user:
        ...     print(user.email)
    """
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    return user

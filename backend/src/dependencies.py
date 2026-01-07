"""
FastAPI dependency injection for database sessions and authentication.

Provides reusable dependencies for:
- Database session management (auto-cleanup)
- Current user extraction from JWT tokens (OAuth2 Bearer)
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session, select
from typing import Generator
from uuid import UUID
import jwt

from src.database import get_session
from src.models.user import User
from src.services.auth_service import verify_token


# OAuth2 token extraction from Authorization header
# tokenUrl points to the login endpoint (will be created in T031)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_db_session() -> Generator[Session, None, None]:
    """
    FastAPI dependency for database session injection.

    Yields a SQLModel session and ensures cleanup after request completion.

    Yields:
        Session: SQLModel database session

    Example:
        @app.get("/api/users")
        async def get_users(db: Session = Depends(get_db_session)):
            users = db.exec(select(User)).all()
            return users
    """
    yield from get_session()


async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db_session)
) -> User:
    """
    FastAPI dependency for authenticated user extraction from JWT token.

    Extracts JWT from Authorization header, verifies signature and expiration,
    fetches user from database, and returns User model.

    Args:
        token: JWT token extracted from Authorization header by oauth2_scheme
        db: Database session injected by get_db_session dependency

    Returns:
        User: The authenticated user model

    Raises:
        HTTPException 401: If token is invalid, expired, or user not found

    Example:
        @app.get("/api/profile")
        async def get_profile(current_user: User = Depends(get_current_user)):
            return UserResponse.model_validate(current_user)
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Verify and decode JWT token
        payload = verify_token(token)

        # Extract user_id from token payload
        user_id_str: str | None = payload.get("sub")
        if user_id_str is None:
            raise credentials_exception

        # Convert string UUID to UUID object
        try:
            user_id = UUID(user_id_str)
        except ValueError:
            raise credentials_exception

        # Verify token type is "access" (not refresh token)
        token_type: str | None = payload.get("type")
        if token_type != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
                headers={"WWW-Authenticate": "Bearer"},
            )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise credentials_exception

    # Fetch user from database
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()

    if user is None:
        raise credentials_exception

    return user

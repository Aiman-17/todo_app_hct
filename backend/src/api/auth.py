"""
Authentication API router with signup, login, profile, and token refresh endpoints.

Provides REST API endpoints for:
- User signup (POST /api/auth/signup)
- User login (POST /api/auth/login)
- Token refresh (POST /api/auth/refresh)
- Profile retrieval (GET /api/auth/profile)
"""
import logging
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from sqlalchemy.exc import IntegrityError

from src.dependencies import get_db_session, get_current_user
from src.models.user import User
from src.schemas.auth import UserCreate, UserLogin, RefreshTokenRequest, UserResponse, TokenResponse
from src.services.user_service import create_user, get_user_by_email, get_user_by_id
from src.services.auth_service import verify_password, create_access_token, create_refresh_token, verify_token

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post(
    "/signup",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    response_description="User profile and authentication tokens"
)
async def signup(
    user_data: UserCreate,
    db: Session = Depends(get_db_session)
):
    """
    Register a new user account.

    Creates a new user with email, name, and hashed password. Returns user
    profile and authentication tokens (access + refresh).

    Args:
        user_data: UserCreate schema with email, name, password
        db: Database session (injected dependency)

    Returns:
        dict with "user" (UserResponse) and "tokens" (TokenResponse)

    Raises:
        400 Bad Request: If email is already registered
        422 Unprocessable Entity: If password validation fails

    Example Request:
        POST /api/auth/signup
        {
            "email": "alice@example.com",
            "name": "Alice Smith",
            "password": "SecurePass123"
        }

    Example Response:
        {
            "user": {
                "id": "550e8400-e29b-41d4-a716-446655440000",
                "email": "alice@example.com",
                "name": "Alice Smith",
                "created_at": "2025-12-30T10:00:00Z"
            },
            "tokens": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "expires_in": 900
            }
        }
    """
    # Check if email already exists
    existing_user = get_user_by_email(db, user_data.email)
    if existing_user:
        logger.warning(f"Signup attempt with existing email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user (password will be hashed in user_service)
    try:
        user = create_user(
            db=db,
            email=user_data.email,
            name=user_data.name,
            password=user_data.password
        )
        logger.info(f"New user registered: {user.email} (ID: {user.id})")
    except IntegrityError:
        # Race condition: another request created user with same email
        db.rollback()
        logger.error(f"Signup race condition for email: {user_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Generate JWT tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    logger.info(f"JWT tokens generated for user: {user.email}")

    # Return user profile + tokens
    return {
        "user": UserResponse.model_validate(user),
        "tokens": TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token
        )
    }


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="Authenticate user and return JWT tokens",
    response_description="JWT access and refresh tokens"
)
async def login(
    credentials: UserLogin,
    db: Session = Depends(get_db_session)
):
    """
    Authenticate user and return JWT tokens.

    Verifies email and password, then returns access and refresh tokens.

    Args:
        credentials: UserLogin schema with email and password
        db: Database session (injected dependency)

    Returns:
        TokenResponse with access_token, refresh_token, token_type, expires_in

    Raises:
        401 Unauthorized: If email not found or password incorrect

    Example Request:
        POST /api/auth/login
        {
            "email": "alice@example.com",
            "password": "SecurePass123"
        }

    Example Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 900
        }
    """
    # Find user by email
    user = get_user_by_email(db, credentials.email)
    if not user:
        logger.warning(f"Login attempt with non-existent email: {credentials.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Verify password
    if not verify_password(credentials.password, user.password_hash):
        logger.warning(f"Failed login attempt for user: {user.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # Generate JWT tokens
    access_token = create_access_token(user.id)
    refresh_token = create_refresh_token(user.id)

    logger.info(f"User logged in successfully: {user.email}")

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post(
    "/refresh",
    response_model=TokenResponse,
    summary="Refresh access token using refresh token",
    response_description="New JWT access and refresh tokens"
)
async def refresh_token_endpoint(
    request: RefreshTokenRequest,
    db: Session = Depends(get_db_session)
):
    """
    Refresh access token using a valid refresh token.

    This endpoint allows clients to obtain a new access token without requiring
    the user to log in again. Use this to maintain user sessions and prevent
    work loss due to token expiration.

    Args:
        refresh_token: Valid JWT refresh token (from login/signup response)
        db: Database session (injected dependency)

    Returns:
        TokenResponse with new access_token, refresh_token, token_type, expires_in

    Raises:
        401 Unauthorized: If refresh token is missing, invalid, expired, or wrong type

    Example Request:
        POST /api/auth/refresh
        {
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
        }

    Example Response:
        {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
            "expires_in": 900
        }
    """
    try:
        # Verify and decode refresh token
        payload = verify_token(request.refresh_token)

        # Ensure it's a refresh token (not an access token)
        if payload.get("type") != "refresh":
            logger.warning("Attempted to use access token for refresh")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type. Refresh token required."
            )

        # Extract user_id from token
        user_id = payload.get("sub")
        if not user_id:
            logger.error("Refresh token missing 'sub' claim")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token payload"
            )

        # Verify user still exists in database
        from uuid import UUID
        user = get_user_by_id(db, UUID(user_id))
        if not user:
            logger.warning(f"Refresh attempt for non-existent user: {user_id}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="User not found"
            )

        # Generate new tokens
        new_access_token = create_access_token(user.id)
        new_refresh_token = create_refresh_token(user.id)

        logger.info(f"Tokens refreshed for user: {user.email}")

        return TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token
        )

    except jwt.ExpiredSignatureError:
        logger.warning("Expired refresh token used")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token has expired. Please log in again."
        )
    except jwt.InvalidTokenError as e:
        logger.warning(f"Invalid refresh token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )


@router.get(
    "/profile",
    response_model=UserResponse,
    summary="Get authenticated user's profile",
    response_description="User profile data"
)
async def get_profile(
    current_user: User = Depends(get_current_user)
):
    """
    Get authenticated user's profile.

    Requires valid JWT access token in Authorization header.

    Args:
        current_user: Authenticated user (injected dependency)

    Returns:
        UserResponse with id, email, name, created_at

    Raises:
        401 Unauthorized: If token is missing, invalid, or expired

    Example Request:
        GET /api/auth/profile
        Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...

    Example Response:
        {
            "id": "550e8400-e29b-41d4-a716-446655440000",
            "email": "alice@example.com",
            "name": "Alice Smith",
            "created_at": "2025-12-30T10:00:00Z"
        }
    """
    logger.info(f"Profile accessed by user: {current_user.email}")
    return UserResponse.model_validate(current_user)

"""
Phase III: Simple in-memory rate limiter for chat endpoint.

Implements per-user rate limiting (100 requests per hour) to prevent abuse.
"""
from datetime import datetime, timedelta, timezone
from typing import Dict, List
from fastapi import HTTPException, Request
from collections import defaultdict
import logging

logger = logging.getLogger(__name__)


class RateLimiter:
    """
    Simple in-memory rate limiter for API endpoints.

    Tracks requests per user within a sliding time window.
    Not production-ready (doesn't scale across multiple servers),
    but sufficient for MVP/hackathon deployment.

    For production, use Redis-backed rate limiting (e.g., slowapi + Redis).
    """

    def __init__(self, max_requests: int = 100, window_seconds: int = 3600):
        """
        Initialize rate limiter.

        Args:
            max_requests: Maximum requests allowed per window
            window_seconds: Time window in seconds (default: 3600 = 1 hour)
        """
        self.max_requests = max_requests
        self.window = timedelta(seconds=window_seconds)
        # user_id -> list of request timestamps
        self.requests: Dict[str, List[datetime]] = defaultdict(list)

    def is_allowed(self, user_id: str) -> bool:
        """
        Check if user is allowed to make a request.

        Args:
            user_id: User identifier

        Returns:
            True if request allowed, False if rate limit exceeded
        """
        now = datetime.now(timezone.utc)
        cutoff = now - self.window

        # Clean up old requests outside the window
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if timestamp > cutoff
        ]

        # Check if under limit
        if len(self.requests[user_id]) >= self.max_requests:
            logger.warning(
                f"Rate limit exceeded for user {user_id}: "
                f"{len(self.requests[user_id])} requests in last hour"
            )
            return False

        # Record this request
        self.requests[user_id].append(now)
        return True

    def get_remaining(self, user_id: str) -> int:
        """Get remaining requests for user in current window."""
        now = datetime.now(timezone.utc)
        cutoff = now - self.window

        # Clean up old requests
        self.requests[user_id] = [
            timestamp for timestamp in self.requests[user_id]
            if timestamp > cutoff
        ]

        return max(0, self.max_requests - len(self.requests[user_id]))

    def reset(self, user_id: str = None):
        """Reset rate limit for user (for testing)."""
        if user_id:
            self.requests[user_id] = []
        else:
            self.requests.clear()


# Global rate limiter instance for chat endpoint
# 100 requests per hour per user (as per spec)
chat_rate_limiter = RateLimiter(max_requests=100, window_seconds=3600)


async def check_rate_limit(request: Request, user_id: str):
    """
    Middleware to check rate limit for authenticated requests.

    Args:
        request: FastAPI request object
        user_id: Authenticated user ID from JWT

    Raises:
        HTTPException: 429 Too Many Requests if limit exceeded
    """
    if not chat_rate_limiter.is_allowed(user_id):
        remaining = chat_rate_limiter.get_remaining(user_id)
        logger.warning(
            f"Rate limit exceeded for user {user_id} on {request.url.path}"
        )
        raise HTTPException(
            status_code=429,
            detail={
                "error": "Rate limit exceeded",
                "message": "You have exceeded the rate limit of 100 requests per hour. Please try again later.",
                "limit": chat_rate_limiter.max_requests,
                "remaining": remaining,
                "window_seconds": chat_rate_limiter.window.total_seconds()
            }
        )

    # Log successful rate limit check
    remaining = chat_rate_limiter.get_remaining(user_id)
    logger.debug(
        f"Rate limit check passed for user {user_id}: "
        f"{remaining}/{chat_rate_limiter.max_requests} remaining"
    )

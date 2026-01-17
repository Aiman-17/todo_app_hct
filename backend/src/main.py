"""
Main FastAPI application entry point for Phase II Todo Backend.

Initializes FastAPI app, configures CORS middleware, registers API routers,
and handles application lifecycle events (startup/shutdown).
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import time

from src.config import settings
from src.database import create_db_and_tables

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Application lifespan context manager.

    Handles startup and shutdown events for the FastAPI application.
    Called once when the application starts and once when it shuts down.
    """
    # Startup
    logger.info("🚀 Starting Todo Application API...")
    logger.info(f"📊 Database: {settings.DATABASE_URL.split('@')[1] if '@' in settings.DATABASE_URL else 'configured'}")
    logger.info(f"🌐 CORS Origins: {', '.join(settings.CORS_ORIGINS)}")

    # Create database tables (safe to call multiple times)
    create_db_and_tables()
    logger.info("✅ Database tables initialized")

    yield

    # Shutdown
    logger.info("👋 Shutting down Todo Application API...")


# Create FastAPI application instance with comprehensive OpenAPI metadata
app = FastAPI(
    lifespan=lifespan,
    title="Todo Application API",
    description="""
## Full-Stack Todo Application Backend

RESTful API for a modern todo application with JWT authentication and user isolation.

### Features

- **JWT Authentication**: Secure access with 15-minute access tokens and 7-day refresh tokens
- **User Isolation**: Users can only access their own tasks
- **SQLModel ORM**: Type-safe database operations with Pydantic validation
- **PostgreSQL/SQLite**: Supports both production and development databases
- **CORS Support**: Configurable cross-origin resource sharing for frontend integration
- **Password Security**: bcrypt hashing with 12 rounds
- **API Documentation**: Auto-generated OpenAPI/Swagger docs

### Authentication

Include the JWT access token in the `Authorization` header:

```
Authorization: Bearer <access_token>
```

Access tokens expire after 15 minutes. Use refresh tokens to obtain new access tokens.

### Error Responses

All endpoints return consistent error responses:

```json
{
  "detail": "Error message here"
}
```

Common HTTP status codes:
- `400`: Bad Request (validation error)
- `401`: Unauthorized (missing or invalid token)
- `403`: Forbidden (insufficient permissions)
- `404`: Not Found (resource doesn't exist)
- `500`: Internal Server Error (server-side error)
    """,
    version="1.0.0",
    contact={
        "name": "Todo Application Support",
        "email": "support@todo-app.example.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    openapi_tags=[
        {
            "name": "health",
            "description": "Health check endpoint for monitoring API availability",
        },
        {
            "name": "auth",
            "description": "Authentication endpoints for user signup, login, and profile management",
        },
        {
            "name": "tasks",
            "description": "Task management endpoints for creating, reading, updating, and deleting tasks",
        },
        {
            "name": "chat",
            "description": "Phase III: AI chatbot endpoint for natural language task management",
        },
        {
            "name": "conversations",
            "description": "Phase III: Conversation history management endpoints",
        },
    ],
)

# Configure CORS middleware
# Allows frontend (Next.js) to make API requests from different origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # e.g., ["http://localhost:3000"]
    allow_credentials=True,  # Allow cookies and authorization headers
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, PATCH)
    allow_headers=["*"],  # Allow all headers (including Authorization)
)


# Security headers middleware
@app.middleware("http")
async def add_security_headers(request: Request, call_next):
    """
    Add security headers to all HTTP responses.

    Security headers protect against common web vulnerabilities:
    - X-Frame-Options: Prevents clickjacking attacks
    - X-Content-Type-Options: Prevents MIME type sniffing
    - X-XSS-Protection: Enables browser XSS protection
    - Strict-Transport-Security: Enforces HTTPS connections
    - Content-Security-Policy: Controls resource loading
    """
    response = await call_next(request)

    # Prevent clickjacking by disallowing framing
    response.headers["X-Frame-Options"] = "DENY"

    # Prevent MIME type sniffing
    response.headers["X-Content-Type-Options"] = "nosniff"

    # Enable browser XSS protection (legacy, but still useful for older browsers)
    response.headers["X-XSS-Protection"] = "1; mode=block"

    # Enforce HTTPS for all future requests (1 year)
    # Only add this header if you're serving over HTTPS in production
    # For development (HTTP), this can be skipped
    # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"

    # Content Security Policy (CSP) - restrictive policy for API
    # Since this is an API backend, we don't load scripts or styles
    response.headers["Content-Security-Policy"] = "default-src 'none'; frame-ancestors 'none'"

    return response


# Request logging middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """
    Log incoming HTTP requests and response times.

    Logs method, path, status code, and processing time for each request.
    """
    start_time = time.time()

    # Log request
    logger.info(f"→ {request.method} {request.url.path}")

    # Process request
    response = await call_next(request)

    # Calculate processing time
    process_time = (time.time() - start_time) * 1000  # Convert to milliseconds

    # Log response
    logger.info(f"← {request.method} {request.url.path} - {response.status_code} ({process_time:.2f}ms)")

    return response


@app.get("/", tags=["health"])
async def root():
    """
    Root endpoint for platform health checks and API info.

    Provides API status and navigation links for Hugging Face Spaces
    container health checks and developer discovery.

    Returns:
        dict: Service status with navigation metadata

    Example response:
        {
            "status": "healthy",
            "service": "Todo Application API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/api/health"
        }
    """
    return {
        "status": "healthy",
        "service": "Todo Application API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }


@app.get("/api/health", tags=["health"])
async def health_check():
    """
    Health check endpoint (no authentication required).

    Returns API health status and current timestamp.

    Returns:
        dict: Health status object with "status" and "timestamp" fields

    Example response:
        {
            "status": "healthy",
            "timestamp": "2025-12-30T10:00:00Z"
        }
    """
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }


# Import and register API routers
from src.api.auth import router as auth_router
from src.api.tasks import router as tasks_router

# Phase III: AI Chatbot routers
from src.routes.chat import router as chat_router
from src.routes.conversations import router as conversations_router

app.include_router(auth_router)
app.include_router(tasks_router)

# Phase III: Register chat endpoints
app.include_router(chat_router)
app.include_router(conversations_router)

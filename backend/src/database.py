"""
Database configuration and session management for Phase II.

Handles SQLModel engine creation, Neon PostgreSQL connection pooling,
and session lifecycle management.
"""
from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set. Check backend/.env file.")

# Create SQLModel engine with Neon-optimized connection pooling
# pool_size=5: Maximum 5 connections in pool
# max_overflow=10: Allow up to 10 additional connections beyond pool_size
# pool_pre_ping=True: Verify connection before use (handles Neon serverless cold starts)
# pool_recycle=3600: Recycle connections after 1 hour (3600 seconds)
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Log SQL queries in development (set to False in production)
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
    pool_recycle=3600,
)


def create_db_and_tables():
    """
    Create all database tables defined in SQLModel models.

    This function should be called during application startup to ensure
    all tables exist. Safe to call multiple times (CREATE TABLE IF NOT EXISTS).
    """
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency injection function for FastAPI routes.

    Yields a SQLModel Session that is automatically committed and closed
    after request processing completes.

    Usage in FastAPI:
        @app.get("/endpoint")
        def my_route(session: Session = Depends(get_session)):
            # Use session here
            pass

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session

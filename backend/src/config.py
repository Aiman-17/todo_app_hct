"""
Configuration module for loading environment variables.

Loads and validates all required environment variables for the backend application.
"""
import os
from dotenv import load_dotenv
from typing import List

# Load .env file from backend directory
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "")

    # Authentication
    BETTER_AUTH_SECRET: str = os.getenv("BETTER_AUTH_SECRET", "")

    # CORS
    CORS_ORIGINS_STR: str = os.getenv("CORS_ORIGINS", "http://localhost:3000")

    @property
    def CORS_ORIGINS(self) -> List[str]:
        """Parse CORS_ORIGINS from comma-separated string to list."""
        return [origin.strip() for origin in self.CORS_ORIGINS_STR.split(",")]

    def validate(self) -> None:
        """
        Validate that all required environment variables are set.

        Raises:
            ValueError: If any required environment variable is missing or invalid
        """
        if not self.DATABASE_URL:
            raise ValueError("DATABASE_URL environment variable not set. Check backend/.env file.")

        if not self.BETTER_AUTH_SECRET:
            raise ValueError("BETTER_AUTH_SECRET environment variable not set. Check backend/.env file.")

        if len(self.BETTER_AUTH_SECRET) < 32:
            raise ValueError("BETTER_AUTH_SECRET must be at least 32 characters long for security.")

        if not self.CORS_ORIGINS:
            raise ValueError("CORS_ORIGINS environment variable not set. Check backend/.env file.")


# Global settings instance
settings = Settings()

# Validate on module import
settings.validate()

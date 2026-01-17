"""
Phase III: MCP Tools logging configuration with correlation ID support.

Sets up structured logging for all MCP tool operations with file handler,
correlation ID tracking, and configurable log levels.
"""
import logging
import logging.handlers
import os
from pathlib import Path

from src.config import settings


def setup_mcp_logging():
    """
    Configure MCP tools logger with file handler and structured formatting.

    Creates logs/mcp_tools.log file with rotation support (max 10MB, keep 5 backups).
    Includes correlation IDs in log output for distributed tracing.

    Log Format:
        TIMESTAMP - LEVEL - USER_ID - CORRELATION_ID - MESSAGE
        2026-01-14 10:30:00,123 - INFO - user-123 - corr-456 - MCP Tool: add_task

    Example:
        >>> setup_mcp_logging()
        >>> logger = logging.getLogger("mcp_tools")
        >>> logger.info("Tool called", extra={"user_id": "user-123", "correlation_id": "corr-456"})
    """
    # Get or create MCP tools logger
    logger = logging.getLogger("mcp_tools")

    # Set log level from configuration
    log_level = getattr(logging, settings.MCP_TOOLS_LOG_LEVEL, logging.INFO)
    logger.setLevel(log_level)

    # Prevent duplicate handlers
    if logger.hasHandlers():
        logger.handlers.clear()

    # Create logs directory if it doesn't exist
    log_dir = Path(__file__).parent.parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)

    log_file = log_dir / "mcp_tools.log"

    # Create rotating file handler (10MB max, keep 5 backups)
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,
        encoding="utf-8"
    )

    # Create console handler for development
    console_handler = logging.StreamHandler()

    # Create formatter with correlation ID support
    formatter = MCPToolsFormatter(
        fmt='%(asctime)s - %(levelname)s - %(user_id)s - %(correlation_id)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    # Add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Prevent propagation to root logger (avoid duplicate logs)
    logger.propagate = False

    logger.info(
        "MCP Tools logging initialized",
        extra={
            "user_id": "system",
            "correlation_id": "init",
            "log_level": settings.MCP_TOOLS_LOG_LEVEL,
            "log_file": str(log_file)
        }
    )

    return logger


class MCPToolsFormatter(logging.Formatter):
    """
    Custom formatter for MCP tools logs with correlation ID support.

    Ensures user_id and correlation_id are always present in log records,
    defaulting to 'unknown' if not provided in extra data.
    """

    def format(self, record):
        """
        Format log record with user_id and correlation_id defaults.

        Args:
            record: LogRecord instance

        Returns:
            str: Formatted log message
        """
        # Set defaults for structured logging fields
        if not hasattr(record, 'user_id'):
            record.user_id = 'unknown'
        if not hasattr(record, 'correlation_id'):
            record.correlation_id = 'none'

        return super().format(record)


# Initialize logging on module import
setup_mcp_logging()

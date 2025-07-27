"""
Logging configuration for the C2S-DSPy project.

This module provides centralized logging configuration with different levels,
formatters, and handlers for console and file output.
"""

import logging
import logging.handlers
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


class ColoredFormatter(logging.Formatter):
    """Custom formatter that adds colors to log levels for console output."""

    # ANSI color codes
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Green
        'WARNING': '\033[33m',  # Yellow
        'ERROR': '\033[31m',    # Red
        'CRITICAL': '\033[35m', # Magenta
        'RESET': '\033[0m'      # Reset
    }

    def format(self, record):
        # Add color to levelname
        levelname = record.levelname
        if levelname in self.COLORS:
            record.levelname = f"{self.COLORS[levelname]}{levelname}{self.COLORS['RESET']}"

        # Format the message
        formatted = super().format(record)

        # Reset levelname to original (in case record is reused)
        record.levelname = levelname

        return formatted


def setup_logging(
    name: str = "c2s-dspy",
    level: str = "DEBUG",
    log_dir: Optional[str] = None,
    console_output: bool = True,
    file_output: bool = True,
    max_file_size: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 5
) -> logging.Logger:
    """
    Set up logging configuration for the application.

    Args:
        name: Logger name
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_dir: Directory for log files (defaults to ./logs)
        console_output: Whether to output to console
        file_output: Whether to output to file
        max_file_size: Maximum size of log file before rotation
        backup_count: Number of backup files to keep

    Returns:
        Configured logger instance
    """

    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, level.upper()))

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatters
    console_formatter = ColoredFormatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%H:%M:%S'
    )

    file_formatter = logging.Formatter(
        fmt='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Console handler
    if console_output:
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

    # File handler
    if file_output:
        # Create logs directory if it doesn't exist
        if log_dir is None:
            log_dir = Path(__file__).parent / "logs"
        else:
            log_dir = Path(log_dir)

        log_dir.mkdir(exist_ok=True)

        # Create rotating file handler
        log_file = log_dir / f"{name}.log"
        file_handler = logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_file_size,
            backupCount=backup_count,
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    # Prevent propagation to avoid duplicate messages
    logger.propagate = False

    return logger


def get_logger(name: str = None) -> logging.Logger:
    """
    Get a logger instance. If no name provided, returns the main application logger.

    Args:
        name: Logger name (optional)

    Returns:
        Logger instance
    """
    if name is None:
        name = "c2s-dspy"

    logger = logging.getLogger(name)

    # If logger doesn't have handlers, set it up with default configuration
    if not logger.handlers:
        return setup_logging(name)

    return logger


def set_log_level(level: str):
    """
    Set the logging level for all existing loggers.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    """
    log_level = getattr(logging, level.upper())

    # Update all existing loggers
    for logger_name in logging.Logger.manager.loggerDict:
        if logger_name.startswith("c2s-dspy"):
            logger = logging.getLogger(logger_name)
            logger.setLevel(log_level)

            # Update handler levels
            for handler in logger.handlers:
                if isinstance(handler, logging.StreamHandler):
                    handler.setLevel(log_level)


def log_function_call(func):
    """
    Decorator to automatically log function entry and exit.

    Usage:
        @log_function_call
        def my_function():
            pass
    """
    def wrapper(*args, **kwargs):
        logger = get_logger()
        logger.debug(f"Entering function: {func.__name__}")
        try:
            result = func(*args, **kwargs)
            logger.debug(f"Exiting function: {func.__name__}")
            return result
        except Exception as e:
            logger.error(f"Exception in function {func.__name__}: {e}")
            raise

    return wrapper


# Environment variable configuration
def configure_from_env():
    """Configure logging based on environment variables."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    log_to_file = os.getenv("LOG_TO_FILE", "true").lower() == "true"
    log_to_console = os.getenv("LOG_TO_CONSOLE", "true").lower() == "true"
    log_dir = os.getenv("LOG_DIR", None)

    return setup_logging(
        level=log_level,
        log_dir=log_dir,
        console_output=log_to_console,
        file_output=log_to_file
    )


# Default logger setup
def get_default_logger() -> logging.Logger:
    """Get the default application logger with standard configuration."""
    log_level = os.getenv("LOG_LEVEL", "INFO")
    return setup_logging(
        name="c2s-dspy",
        level=log_level,
        console_output=True,
        file_output=True
    )


# Context manager for temporary log level changes
class TemporaryLogLevel:
    """Context manager to temporarily change log level."""

    def __init__(self, level: str, logger_name: str = "c2s-dspy"):
        self.level = level
        self.logger_name = logger_name
        self.original_level = None

    def __enter__(self):
        logger = logging.getLogger(self.logger_name)
        self.original_level = logger.level
        logger.setLevel(getattr(logging, self.level.upper()))
        return logger

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger = logging.getLogger(self.logger_name)
        logger.setLevel(self.original_level)


# Performance logging helper
class PerformanceLogger:
    """Helper class for logging performance metrics."""

    def __init__(self, logger_name: str = "c2s-dspy.performance"):
        self.logger = get_logger(logger_name)
        self.start_time = None

    def start(self, operation: str):
        """Start timing an operation."""
        self.operation = operation
        self.start_time = datetime.now()
        self.logger.debug(f"Starting operation: {operation}")

    def end(self):
        """End timing and log the duration."""
        if self.start_time:
            duration = datetime.now() - self.start_time
            self.logger.info(f"Operation '{self.operation}' completed in {duration.total_seconds():.3f} seconds")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.end()


# Example usage and testing
if __name__ == "__main__":
    # Test the logging configuration
    logger = setup_logging(level="DEBUG")

    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    # Test performance logging
    with PerformanceLogger() as perf:
        perf.start("test_operation")
        import time
        time.sleep(0.1)

    print("Logging configuration test completed!")

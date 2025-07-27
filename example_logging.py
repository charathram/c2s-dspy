#!/usr/bin/env python3
"""
Example script demonstrating logging usage and configuration for C2S-DSPy.

This script shows how to use the logging system with different levels,
performance monitoring, and various logging features.
"""

import time
import os
from logging_config import (
    get_default_logger,
    get_logger,
    set_log_level,
    PerformanceLogger,
    TemporaryLogLevel,
    log_function_call,
    configure_from_env
)


# Initialize different loggers
main_logger = get_default_logger()
utils_logger = get_logger("c2s-dspy.utils")
analysis_logger = get_logger("c2s-dspy.analysis")


@log_function_call
def example_function_with_logging():
    """Example function that demonstrates automatic function logging."""
    logger = get_logger("c2s-dspy.example")
    logger.info("This function has automatic entry/exit logging")
    time.sleep(0.1)  # Simulate some work
    return "Function completed successfully"


def demonstrate_log_levels():
    """Demonstrate different log levels."""
    logger = get_logger("c2s-dspy.demo")

    logger.debug("This is a DEBUG message - detailed information for debugging")
    logger.info("This is an INFO message - general information about program execution")
    logger.warning("This is a WARNING message - something unexpected happened")
    logger.error("This is an ERROR message - a serious problem occurred")
    logger.critical("This is a CRITICAL message - the program may not be able to continue")


def demonstrate_performance_logging():
    """Demonstrate performance monitoring."""
    perf_logger = PerformanceLogger("c2s-dspy.performance")

    # Method 1: Manual start/end
    perf_logger.start("manual_operation")
    time.sleep(0.2)
    perf_logger.end()

    # Method 2: Context manager
    with PerformanceLogger() as perf:
        perf.start("context_manager_operation")
        time.sleep(0.15)


def demonstrate_temporary_log_level():
    """Demonstrate temporary log level changes."""
    logger = get_logger("c2s-dspy.temp")

    logger.info("Normal log level - this should appear")
    logger.debug("Normal log level - this might not appear depending on configuration")

    # Temporarily change to DEBUG level
    with TemporaryLogLevel("DEBUG", "c2s-dspy.temp"):
        logger.info("Inside temporary DEBUG level")
        logger.debug("This DEBUG message should now appear")

    logger.debug("Back to normal log level - this might not appear again")


def simulate_file_processing():
    """Simulate processing files with detailed logging."""
    logger = get_logger("c2s-dspy.file_processor")

    files = ["sample1.py", "sample2.js", "sample3.java", "error_file.txt"]

    logger.info(f"Starting to process {len(files)} files")

    for i, filename in enumerate(files, 1):
        logger.debug(f"Processing file {i}/{len(files)}: {filename}")

        # Simulate different processing outcomes
        if "error" in filename:
            logger.error(f"Failed to process {filename}: Simulated error")
        elif filename.endswith(".py"):
            logger.info(f"Successfully processed Python file: {filename}")
        elif filename.endswith(".js"):
            logger.info(f"Successfully processed JavaScript file: {filename}")
        else:
            logger.warning(f"Unknown file type, but processed anyway: {filename}")

        time.sleep(0.05)  # Simulate processing time

    logger.info("File processing completed")


def demonstrate_error_handling():
    """Demonstrate error logging."""
    logger = get_logger("c2s-dspy.error_handler")

    try:
        logger.debug("Attempting risky operation")
        # Simulate an error
        result = 10 / 0
    except ZeroDivisionError as e:
        logger.error(f"Division by zero error occurred: {e}")
        logger.debug("Error details", exc_info=True)  # This includes full traceback in debug mode
    except Exception as e:
        logger.critical(f"Unexpected error: {e}", exc_info=True)


def demonstrate_structured_logging():
    """Demonstrate structured logging with additional context."""
    logger = get_logger("c2s-dspy.structured")

    # Simulate analyzing a code file
    file_info = {
        "filename": "sample_code.py",
        "size_bytes": 1024,
        "language": "python",
        "lines": 45
    }

    logger.info(f"Analyzing file: {file_info['filename']}")
    logger.debug(f"File details: {file_info}")

    # Simulate analysis results
    analysis_results = {
        "functions_found": 5,
        "classes_found": 2,
        "complexity_score": 7.5,
        "confidence": 0.92
    }

    logger.info(f"Analysis completed for {file_info['filename']}")
    logger.info(f"Results: {analysis_results['functions_found']} functions, "
               f"{analysis_results['classes_found']} classes, "
               f"complexity: {analysis_results['complexity_score']}")
    logger.debug(f"Full analysis results: {analysis_results}")


def main():
    """Main function demonstrating various logging features."""

    print("=" * 60)
    print("C2S-DSPy Logging Examples")
    print("=" * 60)

    # Set up environment-based configuration if desired
    # Uncomment the next line to use environment variables for configuration
    # logger = configure_from_env()

    main_logger.info("Starting logging demonstration")

    print("\n1. Basic Log Levels:")
    demonstrate_log_levels()

    print("\n2. Performance Logging:")
    demonstrate_performance_logging()

    print("\n3. Function Logging Decorator:")
    result = example_function_with_logging()
    main_logger.debug(f"Function returned: {result}")

    print("\n4. Temporary Log Level Changes:")
    demonstrate_temporary_log_level()

    print("\n5. File Processing Simulation:")
    simulate_file_processing()

    print("\n6. Error Handling:")
    demonstrate_error_handling()

    print("\n7. Structured Logging:")
    demonstrate_structured_logging()

    print("\n8. Dynamic Log Level Changes:")
    main_logger.info("Current log level messages")
    main_logger.debug("This debug message might not appear")

    print("   Changing to DEBUG level...")
    set_log_level("DEBUG")
    main_logger.debug("This debug message should now appear")

    print("   Changing back to INFO level...")
    set_log_level("INFO")
    main_logger.debug("This debug message should not appear again")

    main_logger.info("Logging demonstration completed")

    print("\n" + "=" * 60)
    print("Check the logs/ directory for log files!")
    print("You can also set environment variables to control logging:")
    print("  LOG_LEVEL=DEBUG uv run example_logging.py")
    print("  LOG_TO_FILE=false uv run example_logging.py")
    print("  LOG_TO_CONSOLE=false uv run example_logging.py")
    print("=" * 60)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Test script to demonstrate debug logging behavior in C2S-DSPy.

This script shows why debug messages might not appear and how to fix it.
"""

import os
from logging_config import get_default_logger, setup_logging

def test_logging_levels():
    """Test different logging levels and configurations."""
    print("=" * 60)
    print("DEBUG LOGGING TEST")
    print("=" * 60)

    print("\n1. Testing default logger (should be INFO level):")
    logger1 = get_default_logger()
    print(f"   Logger level: {logger1.level} (10=DEBUG, 20=INFO)")
    logger1.debug("This DEBUG message should NOT appear with default config")
    logger1.info("This INFO message SHOULD appear with default config")

    print("\n2. Testing with LOG_LEVEL=DEBUG environment variable:")
    os.environ["LOG_LEVEL"] = "DEBUG"
    logger2 = get_default_logger()
    print(f"   Logger level: {logger2.level}")
    logger2.debug("This DEBUG message SHOULD appear with DEBUG config")
    logger2.info("This INFO message SHOULD appear with DEBUG config")

    print("\n3. Testing explicit DEBUG level setup:")
    logger3 = setup_logging(name="test-debug", level="DEBUG")
    print(f"   Logger level: {logger3.level}")
    logger3.debug("This DEBUG message SHOULD appear with explicit DEBUG")
    logger3.info("This INFO message SHOULD appear with explicit DEBUG")

    print("\n4. Testing why line 88 in c2s.py might not show debug messages:")
    print("   - If LOG_LEVEL environment variable is not set to DEBUG")
    print("   - The default logger uses INFO level (20)")
    print("   - DEBUG messages (level 10) are filtered out")
    print("   - Only INFO (20) and higher levels are shown")

def demonstrate_c2s_issue():
    """Simulate the specific issue in c2s.py line 88."""
    print("\n" + "=" * 60)
    print("SIMULATING C2S.PY LINE 88 ISSUE")
    print("=" * 60)

    # Simulate the logger setup in c2s.py
    from c2s import logger

    print(f"\nCurrent logger level in c2s.py: {logger.level}")

    # Simulate the problematic line 88
    fake_daos = ["DAO1", "DAO2", "DAO3"]

    print("\nSimulating the problematic debug line:")
    print("logger.debug(f'DAOs type: {type(fake_daos)}')")

    # This might not appear if logger level is INFO
    logger.debug(f"DAOs type: {type(fake_daos)}")

    # This should always appear
    logger.info(f"Found DAOs: {fake_daos}")

    print(f"\nIf you don't see the debug message above, run:")
    print("LOG_LEVEL=DEBUG uv run test_debug_logging.py")

def show_solutions():
    """Show different ways to solve the debug logging issue."""
    print("\n" + "=" * 60)
    print("SOLUTIONS TO FIX DEBUG LOGGING")
    print("=" * 60)

    print("\nSolution 1: Use LOG_LEVEL environment variable")
    print("   LOG_LEVEL=DEBUG uv run c2s.py")

    print("\nSolution 2: Temporarily change log level in code")
    print("   from logging_config import set_log_level")
    print("   set_log_level('DEBUG')")

    print("\nSolution 3: Use TemporaryLogLevel context manager")
    print("   from logging_config import TemporaryLogLevel")
    print("   with TemporaryLogLevel('DEBUG'):")
    print("       logger.debug('This will appear')")

    print("\nSolution 4: Check if debug is enabled before logging")
    print("   if logger.isEnabledFor(logging.DEBUG):")
    print("       logger.debug('Expensive debug operation')")

def test_environment_variables():
    """Test different environment variable configurations."""
    print("\n" + "=" * 60)
    print("ENVIRONMENT VARIABLE TESTING")
    print("=" * 60)

    # Test different LOG_LEVEL values
    test_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]

    for level in test_levels:
        print(f"\nTesting LOG_LEVEL={level}:")
        os.environ["LOG_LEVEL"] = level

        # Create a new logger to pick up the environment change
        test_logger = setup_logging(name=f"test-{level.lower()}", level=level)
        print(f"   Logger level: {test_logger.level}")

        # Test all message types
        test_logger.debug(f"   DEBUG message with {level} level")
        test_logger.info(f"   INFO message with {level} level")
        test_logger.warning(f"   WARNING message with {level} level")

def main():
    """Main function to run all tests."""
    print("Testing debug logging behavior in C2S-DSPy")
    print("This script helps diagnose why debug messages might not appear")

    test_logging_levels()
    demonstrate_c2s_issue()
    show_solutions()
    test_environment_variables()

    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print("Debug messages in c2s.py line 88 don't appear because:")
    print("1. The default logger level is INFO (20)")
    print("2. DEBUG messages have level 10 (lower than INFO)")
    print("3. The logger filters out messages below its level")
    print("")
    print("To see debug messages, run:")
    print("LOG_LEVEL=DEBUG uv run c2s.py")
    print("")
    print("Or set the environment variable permanently:")
    print("export LOG_LEVEL=DEBUG  # Linux/macOS")
    print("set LOG_LEVEL=DEBUG     # Windows")

if __name__ == "__main__":
    main()

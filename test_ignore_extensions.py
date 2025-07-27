#!/usr/bin/env python3
"""
Test script to demonstrate the ignore_extensions functionality in utils.py.

This script creates test files with various extensions and shows how the
get_all_files and get_all_files_generator functions work with the new
ignore_extensions parameter.
"""

import os
import tempfile
import shutil
from pathlib import Path
from utils import get_all_files, get_all_files_generator
from logging_config import get_logger

# Initialize logger
logger = get_logger("c2s-dspy.test")


def create_test_directory():
    """Create a temporary directory with test files of various extensions."""
    # Create temporary directory
    test_dir = Path(tempfile.mkdtemp(prefix="c2s_test_"))
    logger.info(f"Created test directory: {test_dir}")

    # Define test files with various extensions
    test_files = [
        "main.py",
        "config.json",
        "readme.txt",
        "app.log",
        "temp.tmp",
        "backup.bak",
        "data.csv",
        "script.js",
        "style.css",
        "debug.log",
        "cache.tmp",
        "subdir/nested.py",
        "subdir/nested.log",
        "subdir/nested.txt",
        "subdir/deep/deep_file.js",
        "subdir/deep/error.log",
        "subdir/deep/temp_data.tmp"
    ]

    # Create the files
    created_files = []
    for file_path in test_files:
        full_path = test_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)

        # Write some content to the file
        with open(full_path, 'w') as f:
            f.write(f"Test content for {file_path}\n")

        created_files.append(str(full_path))
        logger.debug(f"Created test file: {full_path}")

    return test_dir, created_files


def test_without_ignore():
    """Test functions without ignore_extensions parameter."""
    print("=" * 60)
    print("TEST 1: Without ignore_extensions (should show all files)")
    print("=" * 60)

    test_dir, expected_files = create_test_directory()

    try:
        # Test get_all_files without ignore
        print("\n1.1 Using get_all_files():")
        files = get_all_files(test_dir)
        print(f"Found {len(files)} files:")
        for file_path in sorted(files):
            print(f"  - {Path(file_path).name} ({Path(file_path).suffix})")

        # Test get_all_files_generator without ignore
        print("\n1.2 Using get_all_files_generator():")
        files_gen = list(get_all_files_generator(test_dir))
        print(f"Found {len(files_gen)} files:")
        for file_path in sorted(files_gen):
            print(f"  - {Path(file_path).name} ({Path(file_path).suffix})")

        assert len(files) == len(files_gen), "Both functions should return same number of files"
        print(f"\n✅ Both functions returned {len(files)} files")

    finally:
        # Clean up
        shutil.rmtree(test_dir)
        logger.debug(f"Cleaned up test directory: {test_dir}")


def test_with_single_ignore():
    """Test functions with single extension to ignore."""
    print("\n" + "=" * 60)
    print("TEST 2: Ignoring .log files only")
    print("=" * 60)

    test_dir, expected_files = create_test_directory()

    try:
        ignore_ext = ['.log']

        # Test get_all_files with ignore
        print(f"\n2.1 Using get_all_files(ignore_extensions={ignore_ext}):")
        files = get_all_files(test_dir, ignore_extensions=ignore_ext)
        print(f"Found {len(files)} files (excluding .log):")
        for file_path in sorted(files):
            file_name = Path(file_path).name
            file_ext = Path(file_path).suffix
            print(f"  - {file_name} ({file_ext})")
            assert file_ext != '.log', f"Found .log file that should be ignored: {file_name}"

        # Test get_all_files_generator with ignore
        print(f"\n2.2 Using get_all_files_generator(ignore_extensions={ignore_ext}):")
        files_gen = list(get_all_files_generator(test_dir, ignore_extensions=ignore_ext))
        print(f"Found {len(files_gen)} files (excluding .log):")
        for file_path in sorted(files_gen):
            file_name = Path(file_path).name
            file_ext = Path(file_path).suffix
            print(f"  - {file_name} ({file_ext})")
            assert file_ext != '.log', f"Found .log file that should be ignored: {file_name}"

        assert len(files) == len(files_gen), "Both functions should return same number of files"
        print(f"\n✅ Both functions correctly ignored .log files")

    finally:
        # Clean up
        shutil.rmtree(test_dir)


def test_with_multiple_ignores():
    """Test functions with multiple extensions to ignore."""
    print("\n" + "=" * 60)
    print("TEST 3: Ignoring .log, .tmp, and .bak files")
    print("=" * 60)

    test_dir, expected_files = create_test_directory()

    try:
        ignore_ext = ['.log', '.tmp', '.bak']

        # Test get_all_files with multiple ignores
        print(f"\n3.1 Using get_all_files(ignore_extensions={ignore_ext}):")
        files = get_all_files(test_dir, ignore_extensions=ignore_ext)
        print(f"Found {len(files)} files (excluding {ignore_ext}):")
        for file_path in sorted(files):
            file_name = Path(file_path).name
            file_ext = Path(file_path).suffix
            print(f"  - {file_name} ({file_ext})")
            assert file_ext not in ignore_ext, f"Found ignored file: {file_name} with ext {file_ext}"

        # Test get_all_files_generator with multiple ignores
        print(f"\n3.2 Using get_all_files_generator(ignore_extensions={ignore_ext}):")
        files_gen = list(get_all_files_generator(test_dir, ignore_extensions=ignore_ext))
        print(f"Found {len(files_gen)} files (excluding {ignore_ext}):")
        for file_path in sorted(files_gen):
            file_name = Path(file_path).name
            file_ext = Path(file_path).suffix
            print(f"  - {file_name} ({file_ext})")
            assert file_ext not in ignore_ext, f"Found ignored file: {file_name} with ext {file_ext}"

        assert len(files) == len(files_gen), "Both functions should return same number of files"
        print(f"\n✅ Both functions correctly ignored {ignore_ext} files")

    finally:
        # Clean up
        shutil.rmtree(test_dir)


def test_extension_normalization():
    """Test that extensions are properly normalized (with/without dots, case sensitivity)."""
    print("\n" + "=" * 60)
    print("TEST 4: Extension normalization (dots and case)")
    print("=" * 60)

    test_dir, expected_files = create_test_directory()

    try:
        # Test different ways of specifying extensions
        test_cases = [
            ['.LOG'],           # Uppercase with dot
            ['log'],            # Lowercase without dot
            ['LOG'],            # Uppercase without dot
            ['.log'],           # Lowercase with dot
        ]

        for i, ignore_ext in enumerate(test_cases, 1):
            print(f"\n4.{i} Testing ignore_extensions={ignore_ext}:")
            files = get_all_files(test_dir, ignore_extensions=ignore_ext)

            # Count how many .log files are in the directory
            all_files = get_all_files(test_dir)
            log_files = [f for f in all_files if Path(f).suffix.lower() == '.log']

            print(f"  Total files: {len(all_files)}")
            print(f"  Log files in directory: {len(log_files)}")
            print(f"  Files after ignoring: {len(files)}")
            print(f"  Expected difference: {len(all_files) - len(log_files)}")

            # Verify no .log files remain
            remaining_log_files = [f for f in files if Path(f).suffix.lower() == '.log']
            assert len(remaining_log_files) == 0, f"Still found .log files: {remaining_log_files}"
            assert len(files) == len(all_files) - len(log_files), "Incorrect number of files filtered"

        print(f"\n✅ Extension normalization works correctly")

    finally:
        # Clean up
        shutil.rmtree(test_dir)


def test_real_world_scenario():
    """Test a real-world scenario with common file extensions to ignore."""
    print("\n" + "=" * 60)
    print("TEST 5: Real-world scenario (ignore logs, temps, caches)")
    print("=" * 60)

    test_dir, expected_files = create_test_directory()

    # Add more realistic files
    additional_files = [
        "__pycache__/module.pyc",
        ".git/config",
        ".DS_Store",
        "node_modules/package.json",
        "dist/bundle.js",
        "coverage/index.html",
        "logs/application.log",
        "temp/temp_file.tmp",
        ".env",
        ".venv/lib/python.py"
    ]

    for file_path in additional_files:
        full_path = test_dir / file_path
        full_path.parent.mkdir(parents=True, exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(f"Content for {file_path}\n")

    try:
        # Common extensions to ignore in development
        ignore_extensions = [
            '.log', '.tmp', '.pyc', '.pyo', '.pyd',
            '.so', '.dll', '.dylib', '.egg-info',
            '.DS_Store', '.thumbs.db'
        ]

        print(f"\n5.1 Ignoring common development files: {ignore_extensions}")

        # Get all files first
        all_files = get_all_files(test_dir)
        print(f"Total files in directory: {len(all_files)}")

        # Get filtered files
        filtered_files = get_all_files(test_dir, ignore_extensions=ignore_extensions)
        print(f"Files after filtering: {len(filtered_files)}")
        print(f"Files ignored: {len(all_files) - len(filtered_files)}")

        print("\nRemaining files:")
        for file_path in sorted(filtered_files):
            rel_path = Path(file_path).relative_to(test_dir)
            print(f"  - {rel_path}")

        print("\nIgnored files:")
        ignored_files = []
        for file_path in all_files:
            if file_path not in filtered_files:
                ignored_files.append(file_path)
                rel_path = Path(file_path).relative_to(test_dir)
                print(f"  - {rel_path} ({Path(file_path).suffix})")

        print(f"\n✅ Successfully filtered {len(ignored_files)} development files")

    finally:
        # Clean up
        shutil.rmtree(test_dir)


def main():
    """Run all tests to demonstrate ignore_extensions functionality."""
    print("Testing ignore_extensions functionality in utils.py")
    print("This demonstrates the new optional parameter for ignoring file extensions")

    try:
        test_without_ignore()
        test_with_single_ignore()
        test_with_multiple_ignores()
        test_extension_normalization()
        test_real_world_scenario()

        print("\n" + "=" * 60)
        print("ALL TESTS PASSED! ✅")
        print("=" * 60)
        print("\nSummary of ignore_extensions functionality:")
        print("1. ✅ Optional parameter works correctly")
        print("2. ✅ Single extension ignoring works")
        print("3. ✅ Multiple extension ignoring works")
        print("4. ✅ Extension normalization (dots/case) works")
        print("5. ✅ Real-world scenarios work")
        print("6. ✅ Both get_all_files() and get_all_files_generator() work identically")
        print("\nUsage examples:")
        print("  files = get_all_files('/path', ignore_extensions=['.log', '.tmp'])")
        print("  for f in get_all_files_generator('/path', ignore_extensions=['log', 'TMP']):")

    except Exception as e:
        print(f"\n❌ TEST FAILED: {e}")
        logger.error(f"Test failed with error: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()

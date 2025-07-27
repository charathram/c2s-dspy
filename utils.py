import os
from pathlib import Path
from typing import List, Iterator, Union, Optional
from logging_config import get_logger

# Initialize logger for utils module
logger = get_logger("c2s-dspy.utils")


def get_all_files(directory_path: Union[str, Path], ignore_extensions: Optional[List[str]] = None) -> List[str]:
    """
    Get all files in a directory and its subdirectories recursively.

    Args:
        directory_path (Union[str, Path]): The path to the directory to search
        ignore_extensions (Optional[List[str]]): File extensions to ignore (e.g., ['.log', '.tmp'])

    Returns:
        List[str]: A list containing the full path to each file found

    Raises:
        FileNotFoundError: If the directory does not exist
        PermissionError: If access to the directory is denied

    Examples:
        >>> files = get_all_files("/path/to/directory")
        >>> for file_path in files:
        ...     print(file_path)
        /path/to/directory/file1.txt
        /path/to/directory/subdir/file2.py

        >>> files = get_all_files("/path/to/directory", ignore_extensions=['.log', '.tmp'])
        >>> # Will exclude any .log and .tmp files
    """
    directory_path = Path(directory_path)

    # Normalize ignore_extensions to ensure they start with a dot and are lowercase
    if ignore_extensions:
        ignore_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in ignore_extensions]
        ignore_extensions = [ext.lower() for ext in ignore_extensions]
        logger.debug(f"Ignoring file extensions: {ignore_extensions}")

    logger.debug(f"Scanning directory: {directory_path}")

    if not directory_path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist")

    if not directory_path.is_dir():
        logger.error(f"Path is not a directory: {directory_path}")
        raise ValueError(f"'{directory_path}' is not a directory")

    files = []

    try:
        for root, dirs, filenames in os.walk(directory_path):
            logger.debug(f"Processing directory: {root} with {len(filenames)} files")
            for filename in filenames:
                full_path = os.path.join(root, filename)

                # Check if file should be ignored based on extension
                if ignore_extensions:
                    file_extension = Path(filename).suffix.lower()
                    if file_extension in ignore_extensions:
                        logger.debug(f"Ignoring file due to extension: {full_path}")
                        continue

                files.append(full_path)
    except PermissionError as e:
        logger.error(f"Permission denied accessing directory: {directory_path} - {e}")
        raise PermissionError(f"Permission denied accessing directory: {e}")

    logger.info(f"Found {len(files)} files in {directory_path}")
    return files


def get_all_files_generator(directory_path: Union[str, Path], ignore_extensions: Optional[List[str]] = None) -> Iterator[str]:
    """
    Generator version that yields file paths one at a time.
    More memory-efficient for large directories.

    Args:
        directory_path (Union[str, Path]): The path to the directory to search
        ignore_extensions (Optional[List[str]]): File extensions to ignore (e.g., ['.log', '.tmp'])

    Yields:
        str: Full path to each file found

    Raises:
        FileNotFoundError: If the directory does not exist
        PermissionError: If access to the directory is denied

    Examples:
        >>> for file_path in get_all_files_generator("/path/to/directory"):
        ...     print(file_path)
        /path/to/directory/file1.txt
        /path/to/directory/subdir/file2.py

        >>> for file_path in get_all_files_generator("/path/to/directory", ignore_extensions=['.log', '.tmp']):
        ...     print(file_path)
        # Will exclude any .log and .tmp files
    """
    directory_path = Path(directory_path)

    # Normalize ignore_extensions to ensure they start with a dot and are lowercase
    if ignore_extensions:
        ignore_extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in ignore_extensions]
        ignore_extensions = [ext.lower() for ext in ignore_extensions]
        logger.debug(f"Ignoring file extensions: {ignore_extensions}")

    logger.debug(f"Starting generator scan of directory: {directory_path}")

    if not directory_path.exists():
        logger.error(f"Directory does not exist: {directory_path}")
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist")

    if not directory_path.is_dir():
        logger.error(f"Path is not a directory: {directory_path}")
        raise ValueError(f"'{directory_path}' is not a directory")

    file_count = 0
    try:
        for root, dirs, filenames in os.walk(directory_path):
            logger.debug(f"Processing directory: {root} with {len(filenames)} files")
            for filename in filenames:
                full_path = os.path.join(root, filename)

                # Check if file should be ignored based on extension
                if ignore_extensions:
                    file_extension = Path(filename).suffix.lower()
                    if file_extension in ignore_extensions:
                        logger.debug(f"Ignoring file due to extension: {full_path}")
                        continue

                file_count += 1
                yield full_path
    except PermissionError as e:
        logger.error(f"Permission denied accessing directory: {directory_path} - {e}")
        raise PermissionError(f"Permission denied accessing directory: {e}")

    logger.debug(f"Generator completed, yielded {file_count} files")


def get_files_by_extension(directory_path: Union[str, Path],
                          extensions: Union[str, List[str]],
                          ignore_extensions: Optional[List[str]] = None) -> List[str]:
    """
    Get all files with specific extensions in a directory and its subdirectories.

    Args:
        directory_path (Union[str, Path]): The path to the directory to search
        extensions (Union[str, List[str]]): File extension(s) to filter by (e.g., '.py' or ['.py', '.txt'])
        ignore_extensions (Optional[List[str]]): File extensions to ignore (e.g., ['.log', '.tmp'])

    Returns:
        List[str]: A list containing the full path to each matching file

    Examples:
        >>> python_files = get_files_by_extension("/path/to/project", ".py")
        >>> code_files = get_files_by_extension("/path/to/project", [".py", ".js", ".java"])
        >>> py_files = get_files_by_extension("/path", ".py", ignore_extensions=[".pyc", ".pyo"])
    """
    if isinstance(extensions, str):
        extensions = [extensions]

    # Normalize extensions to ensure they start with a dot
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]
    logger.debug(f"Filtering files by extensions: {extensions} in directory: {directory_path}")

    all_files = get_all_files(directory_path, ignore_extensions=ignore_extensions)
    filtered_files = []

    for file_path in all_files:
        file_extension = Path(file_path).suffix.lower()
        if file_extension in [ext.lower() for ext in extensions]:
            filtered_files.append(file_path)
            logger.debug(f"Matched file: {file_path}")

    logger.info(f"Filtered {len(filtered_files)} files from {len(all_files)} total files using extensions {extensions}")
    return filtered_files


def read_code_file(file_path: Union[str, Path] = "sample_code.cbl") -> str:
    """
    Read code from filesystem and return its contents.

    Args:
        file_path (Union[str, Path]): Path to the code file to read

    Returns:
        str: Contents of the file, or None if file cannot be read

    Raises:
        FileNotFoundError: If the file does not exist
        IOError: If there's an error reading the file

    Examples:
        >>> content = read_code_file("sample_inputs/COACTUPC.cbl")
        >>> if content:
        ...     print(f"File loaded, length: {len(content)}")
    """
    file_path = Path(file_path)
    logger.debug(f"Attempting to read file: {file_path}")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()
            logger.info(f"Successfully read file: {file_path} ({len(content)} characters)")
            return content
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}. Please ensure the file exists in the current directory.")
        return None
    except IOError as e:
        logger.error(f"Error reading file {file_path}: {e}")
        return None

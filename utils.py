import os
from pathlib import Path
from typing import List, Iterator, Union


def get_all_files(directory_path: Union[str, Path]) -> List[str]:
    """
    Get all files in a directory and its subdirectories recursively.

    Args:
        directory_path (Union[str, Path]): The path to the directory to search

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
    """
    directory_path = Path(directory_path)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist")

    if not directory_path.is_dir():
        raise ValueError(f"'{directory_path}' is not a directory")

    files = []

    try:
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                files.append(full_path)
    except PermissionError as e:
        raise PermissionError(f"Permission denied accessing directory: {e}")

    return files


def get_all_files_generator(directory_path: Union[str, Path]) -> Iterator[str]:
    """
    Generator version that yields file paths one at a time.
    More memory-efficient for large directories.

    Args:
        directory_path (Union[str, Path]): The path to the directory to search

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
    """
    directory_path = Path(directory_path)

    if not directory_path.exists():
        raise FileNotFoundError(f"Directory '{directory_path}' does not exist")

    if not directory_path.is_dir():
        raise ValueError(f"'{directory_path}' is not a directory")

    try:
        for root, dirs, filenames in os.walk(directory_path):
            for filename in filenames:
                full_path = os.path.join(root, filename)
                yield full_path
    except PermissionError as e:
        raise PermissionError(f"Permission denied accessing directory: {e}")


def get_files_by_extension(directory_path: Union[str, Path],
                          extensions: Union[str, List[str]]) -> List[str]:
    """
    Get all files with specific extensions in a directory and its subdirectories.

    Args:
        directory_path (Union[str, Path]): The path to the directory to search
        extensions (Union[str, List[str]]): File extension(s) to filter by (e.g., '.py' or ['.py', '.txt'])

    Returns:
        List[str]: A list containing the full path to each matching file

    Examples:
        >>> python_files = get_files_by_extension("/path/to/project", ".py")
        >>> code_files = get_files_by_extension("/path/to/project", [".py", ".js", ".java"])
    """
    if isinstance(extensions, str):
        extensions = [extensions]

    # Normalize extensions to ensure they start with a dot
    extensions = [ext if ext.startswith('.') else f'.{ext}' for ext in extensions]

    all_files = get_all_files(directory_path)
    filtered_files = []

    for file_path in all_files:
        file_extension = Path(file_path).suffix.lower()
        if file_extension in [ext.lower() for ext in extensions]:
            filtered_files.append(file_path)

    return filtered_files

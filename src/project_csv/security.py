from pathlib import Path


def safe_file_path(file_name: str, base_dir: str = "data") -> Path:
    """
    Returns a safe, absolute path to a file within the base_dir,
    preventing path traversal.

    Args:
        file_name: The file name provided by the user (may include subdirectories)
        base_dir: The base directory to which access is restricted

    Returns:
        Path: A safe absolute path within base_dir

    Raises:
        OSError: If file_name resolves outside of base_dir
    """
    base_path = Path(base_dir).resolve()
    target_path = (base_path / file_name).resolve()

    if not target_path.is_relative_to(base_path):
        raise OSError(f"Unsafe file path: {file_name}")
        
    return target_path

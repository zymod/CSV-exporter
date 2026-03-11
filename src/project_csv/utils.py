import uuid
import random
import string
import csv
from pathlib import Path

from project_csv.security import safe_file_path


def generate_data(num_rows: int) -> list[dict[str, int | str | float]]:
    """Generate a list of sample data rows.

    Each row is a dictionary with the following keys:
    - 'id'   (int): sequential index starting from 1.
    - 'code' (str): random string of 3–12 uppercase letters
      and digits (A–Z, 0–9).
    - 'cost' (float): random value in the range [0.0, 1000.0].

    Args:
        num_rows: Number of rows to generate.
            Should be positive. A value of 0 returns an
            empty list.

    Returns:
        list[dict[str, int | str | float]]: List of
            dictionaries of length `num_rows`.
    """
    data = []
    for i in range(1, num_rows + 1):
        row = {
            "id": i,
            "code": ''.join(
                random.choices(
                    string.ascii_uppercase + string.digits,
                    k=random.randint(3, 12)
                )
            ),
            "cost": random.uniform(0, 1000)
        }
        data.append(row)
    return data


def export_to_csv(
    data: list[dict[str, str | float]],
    file_name: str | None = None
) -> str | None:
    """Export data to a CSV file in the `data/` directory.

    Column headers are taken from the keys of the first
    dictionary in the list. If `data` is empty, the file
    is not created, but the function returns the path where
    the file *would* have been created.

    Args:
        data: List of dictionaries to save. All dictionaries
            should have identical keys — the keys of the
            first element determine the CSV headers.
        file_name: Output file name (with or without the
            .csv extension). Spaces are replaced with
            underscores, and a missing .csv extension is
            added automatically. If None or an empty string,
            a random UUID4 name is generated.

    Returns:
        str | None: Absolute path to the generated CSV file,
            or None if `data` is empty and no file was created.

    Raises:
        OSError: If the directory cannot be created or the
            file cannot be written (e.g. insufficient
            permissions, full disk).
    """
    file_name = _normalize_file_name(file_name)
    file_path = None

    if data:
        try:
            file_path = get_or_create_file_path(file_name)
            with open(
                file_path, mode="w", newline="", encoding="utf-8"
            ) as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        except OSError as e:
            raise OSError(f"Failed to write file: {e}") from e

    return file_path


def get_or_create_file_path(file_name: str) -> str:
    """Return the absolute path to a CSV file in `data/` directory.

    If the `data/` directory (relative to the current working directory)
    does not exist, it is created automatically. The file itself is not
    created by this function.

    Args:
        file_name: Name of the file (e.g., "report.csv").
        Can include subdirectories relative to `data/`
        (e.g., "2024/report.csv").

    Returns:
        Absolute path to the file as a string, e.g.
        `/home/user/project/data/file_name.csv`.
    """
    file_path = safe_file_path(file_name)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    return str(file_path)


def _normalize_file_name(file_name: str | None = None) -> str:
    """Normalize a CSV file name.

    Performs the following steps in order:
    1. If `file_name` is None or an empty string —
       generates a UUID4 name.
    2. Replaces spaces with underscores (`replace_spaces`).
    3. Appends `.csv` if missing (`add_csv_suffix`).

    Args:
        file_name: Raw file name provided by the user,
            or None.

    Returns:
        str: Normalized file name ending with `.csv`.
    """
    if not file_name:
        file_name = str(uuid.uuid4())
    if not file_name.endswith(".csv"):
        file_name += ".csv"
    return file_name.replace(" ", "_")

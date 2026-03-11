from pathlib import Path

import pytest

from project_csv.security import safe_file_path
from .fixtures import VALID_PATHS, INVALID_PATHS


@pytest.mark.parametrize("case, expected", VALID_PATHS)
def test_safe_file_path_valid_cases(
    case: str,
    expected: str
) -> None:
    """Verify that safe_file_path() returns correct paths for valid inputs.

    Test cases:
        - "file.csv" → "data/file.csv"
        - "subdir/file.csv" → "data/subdir/file.csv"
        - "subdir/../file.csv" → "data/file.csv"
    """
    assert safe_file_path(case) == Path(expected)


@pytest.mark.parametrize("case, expected", INVALID_PATHS)
def test_safe_file_path_invalid_cases(
    case: str,
    expected: type(OSError)
) -> None:
    """Verify that safe_file_path() raises OSError for invalid inputs.

    Test cases:
        - "../file.csv" → OSError
        - "subdir/../../file.csv" → OSError
        - "/absolute/path/file.csv" → OSError
    """
    with pytest.raises(expected):
        safe_file_path(case)

from pathlib import Path

import pytest
from _pytest.monkeypatch import MonkeyPatch
from unittest.mock import patch

from project_csv.utils import export_to_csv, generate_data, _normalize_file_name
from fixtures import (
    GENERATE_DATA_LENGTHS,
    GENERATE_DATA_IDS,
    NORMALIZE_FILE_NAME_INPUTS,
    NORMALIZE_FILE_NAME_EMPTY_INPUTS,
)


@pytest.mark.parametrize("num_rows, expected", GENERATE_DATA_LENGTHS)
def test_generate_data_returns_correct_length(
    num_rows: int,
    expected: int
) -> None:
    """Verify that generate_data() returns a list of the correct length.

    Test cases (from fixtures.GENERATE_DATA_LENGTHS):
        - 0 rows → empty list,
        - 1 row,
        - small number of rows (5),
        - large number of rows (1000).
    """
    assert len(generate_data(num_rows)) == expected


@pytest.mark.parametrize("num_rows, expected", GENERATE_DATA_IDS)
def test_generate_data_ids_are_sequential_from_one(
    num_rows: int,
    expected: list[int]
) -> None:
    """Verify that generate_data() assigns sequential ids from 1.

    Test cases (from fixtures.GENERATE_DATA_IDS):
        - 1 row → ids: [1],
        - 5 rows → ids: [1, 2, 3, 4, 5].
    """
    ids = [row["id"] for row in generate_data(num_rows)]
    assert ids == expected


@pytest.mark.parametrize("case, expected", NORMALIZE_FILE_NAME_INPUTS)
def test_normalize_file_name_returns_normalized_name(
    case: str,
    expected: str
) -> None:
    """Verify that _normalize_file_name() normalizes the file name.

    Test cases (from fixtures.NORMALIZE_FILE_NAME_INPUTS):
        - no .csv suffix → .csv is appended,
        - name already has .csv → unchanged,
        - spaces in name → replaced with underscores,
        - .CSV suffix → gets an additional .csv appended.
    """
    assert _normalize_file_name(case) == expected


@pytest.mark.parametrize("case", NORMALIZE_FILE_NAME_EMPTY_INPUTS)
def test_normalize_file_name_generates_uuid_for_empty_input(
    case: str | None
) -> None:
    """Verify that _normalize_file_name() generates a UUID4 name
    for empty or missing input.

    Test cases (from fixtures.NORMALIZE_FILE_NAME_EMPTY_INPUTS):
        - None → UUID4-formatted name with .csv suffix,
        - empty string → UUID4-formatted name with .csv suffix.
    """
    fixed_uuid = "12345678-1234-4234-8234-123456789abc"
    with patch("project_csv.utils.uuid.uuid4", return_value=fixed_uuid):
        result = _normalize_file_name(case)
    assert result == f"{fixed_uuid}.csv"


def test_export_csv_creates_file(
    tmp_path: Path,
    monkeypatch: MonkeyPatch
    ) -> None:
    """Verify that export_to_csv() creates a CSV file in data/.

    Test cases:
        - input: `[{"a": 1}]`, file name: `"test.csv"` →
          file `data/test.csv` exists.
    """
    monkeypatch.chdir(tmp_path)
    export_to_csv([{"a": 1}], "test.csv")
    assert (tmp_path / "data/test.csv").exists()


def test_export_csv_does_not_create_file_for_empty_data(
    tmp_path: Path,
    monkeypatch: MonkeyPatch
) -> None:
    """Verify that export_to_csv() does not create a file for empty data.

    Test cases:
        - input: `[]`, file name: `"test.csv"` →
          file `data/test.csv` does not exist.
    """
    monkeypatch.chdir(tmp_path)
    export_to_csv([], "test.csv")
    assert not (tmp_path / "data/test.csv").exists()


def test_export_to_csv_raises_oserror() -> None:
    """Verify that export_to_csv() propagates an OSError on write failure.

    Test cases:
        - `builtins.open` raises OSError with message
          `"Write error"` → function raises OSError
          containing the original message.
    """
    data = [{"id": 1, "cost": 100}]

    with patch("builtins.open", side_effect=OSError("Write error")):
        with pytest.raises(OSError) as exc_info:
            export_to_csv(data, "test.csv")

    assert "Write error" in str(exc_info.value)

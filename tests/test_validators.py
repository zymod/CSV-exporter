import pytest
from _pytest.monkeypatch import MonkeyPatch

from project_csv.validators import parse_num_rows, _get_num_rows_default
from fixtures import VALID_INPUTS, INVALID_INPUTS, PARSE_NUM_ROWS_FALLBACK_INPUTS


@pytest.mark.parametrize("case, expected", VALID_INPUTS)
def test_valid_input_returns_expected(case: str, expected: int) -> None:
    """Verify that parse_num_rows() correctly converts valid input.

    Test cases (from fixtures.VALID_INPUTS):
        - positive integer as string (e.g. `"5"` → `5`)
        - large integer (e.g. `"346342"` → `346342`)
        - integer with leading spaces (e.g. `"   12"` → `12`)
    """
    assert parse_num_rows(case) == expected


def test_missing_env_variable_raises_exception(
    monkeypatch: MonkeyPatch
) -> None:
    """Verify that _get_num_rows_default() raises ValueError
    when NUM_ROWS_DEFAULT is not set.

    The variable is removed from the environment before the
    function is called using `monkeypatch.delenv(...,
    raising=False)` — the `raising=False` flag prevents an
    error if the variable did not exist beforehand.
    """
    monkeypatch.delenv("NUM_ROWS_DEFAULT", raising=False)
    with pytest.raises(ValueError):
        _get_num_rows_default()


@pytest.mark.parametrize("case, expected", INVALID_INPUTS)
def test_invalid_env_value_raises_exception(
    monkeypatch: MonkeyPatch,
    case: str,
    expected: type[ValueError]
) -> None:
    """Verify that _get_num_rows_default() raises ValueError
    for invalid NUM_ROWS_DEFAULT values.

    The environment variable is set via monkeypatch before
    each call.

    Test cases (from fixtures.INVALID_INPUTS):
        - non-numeric value (e.g. `"abc"`, `"!#$["`),
        - negative integer (e.g. `"-2"`),
        - invalid format (e.g. `"10-"`, `"10.5"`),
        - zero (e.g. `"0"`),
        - empty string (`""`).
    """
    monkeypatch.setenv("NUM_ROWS_DEFAULT", case)
    with pytest.raises(expected):
        _get_num_rows_default()


@pytest.mark.parametrize("case", PARSE_NUM_ROWS_FALLBACK_INPUTS)
def test_invalid_input_falls_back_to_env_default(
    monkeypatch: MonkeyPatch,
    case: str,
) -> None:
    """Verify that parse_num_rows() returns NUM_ROWS_DEFAULT
    for invalid input.

    Test cases (from fixtures.PARSE_NUM_ROWS_FALLBACK_INPUTS):
        - non-numeric value (e.g. `"abc"`, `"!#$["`),
        - negative integer (e.g. `"-2"`),
        - invalid format (e.g. `"10-"`, `"10.5"`),
        - zero (`"0"`),
        - empty string (`""`).
    """
    monkeypatch.setenv("NUM_ROWS_DEFAULT", "10")
    assert parse_num_rows(case) == 10


@pytest.mark.parametrize("case, expected", VALID_INPUTS)
def test_valid_env_value_returns_expected(
    monkeypatch: MonkeyPatch,
    case: str,
    expected: int
) -> None:
    """Verify that parse_num_rows() returns the expected value
    when both the input and NUM_ROWS_DEFAULT are valid.

    NUM_ROWS_DEFAULT is set to `str(expected)`, so even via
    the fallback path the result should be identical. This
    verifies consistency between the main path and the
    fallback path for the same input.

    Test cases (from fixtures.GENERATE_DATA_IDS):
        - positive integer as string (e.g. `"5"` → `5`)
        - large integer (e.g. `"346342"` → `346342`)
        - integer with leading spaces (e.g. `"   12"` → `12`)
    """
    monkeypatch.setenv("NUM_ROWS_DEFAULT", str(expected))
    result = parse_num_rows(case)
    assert result == expected

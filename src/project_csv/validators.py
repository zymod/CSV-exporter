import os


def parse_num_rows(num_rows: str) -> int:
    """Parse and validate the number of rows provided by the user.

    Converts `num_rows` to `int`. If the value is invalid
    (non-numeric, negative, or zero), returns the default
    value from the `NUM_ROWS_DEFAULT` environment variable.

    Supports underscore-formatted numbers (e.g. `"10_000"`)
    via Python's built-in `int()` behaviour.

    Args:
        num_rows: String containing the number of rows
            provided by the user.

    Returns:
        int: Positive integer representing the requested
            number of rows.

    Raises:
        ValueError: If `num_rows` is invalid *and* the
            `NUM_ROWS_DEFAULT` variable is not set or
            contains an invalid value
            (delegated from `_get_num_rows_default`).
    """
    try:
        num_rows = int(num_rows)
        if num_rows <= 0:
            raise ValueError
    except ValueError:
        return _get_num_rows_default()
    return num_rows


def _get_num_rows_default() -> int:
    """Read the default row count from NUM_ROWS_DEFAULT.

    The variable should be set in the `.env` file and
    loaded by `python-dotenv` before this function is
    called.

    Returns:
        int: Value of `NUM_ROWS_DEFAULT`.

    Raises:
        ValueError: If the `NUM_ROWS_DEFAULT` variable
            is not set.
        ValueError: If the variable's value cannot be
            cast to `int` (e.g. `"abc"`, `"1.5"`).
    """
    num_rows_default = os.getenv('NUM_ROWS_DEFAULT')
    if num_rows_default is None:
        raise ValueError(
            "NUM_ROWS_DEFAULT variable is missing from .env"
        )
    try:
        num_rows = int(num_rows_default)
        if num_rows <= 0:
            raise ValueError
    except ValueError:
        msg = "Invalid NUM_ROWS_DEFAULT value in .env: {}"
        raise ValueError(msg.format(num_rows_default))
    return num_rows

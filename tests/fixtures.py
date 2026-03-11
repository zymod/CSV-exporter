import pytest

FILE_NAME = 'test.csv'

VALID_INPUTS = [
    pytest.param("5", 5, id="small_positive_integer"),
    pytest.param("1_000", 1_000, id="positive_integer_with_underscores"),
    pytest.param("346342", 346342, id="large_positive_integer"),
    pytest.param("   12", 12, id="positive_integer_with_spaces"),
]

INVALID_INPUTS = [
    pytest.param("abc", ValueError, id="letters"),
    pytest.param("!#$[", ValueError, id="special_characters"),
    pytest.param("-2", ValueError, id="negative_integer"),
    pytest.param("10-", ValueError, id="trailing_minus"),
    pytest.param("10.5", ValueError, id="decimal"),
    pytest.param("0", ValueError, id="zero"),
    pytest.param("", ValueError, id="empty_string"),
]

NORMALIZE_FILE_NAME_INPUTS = [
    pytest.param("report", "report.csv", id="no_csv_suffix"),
    pytest.param("report.csv", "report.csv", id="already_has_csv_suffix"),
    pytest.param("my report", "my_report.csv", id="spaces_replaced"),
    pytest.param("report.CSV", "report.CSV.csv", id="uppercase_csv_suffix"),
]

NORMALIZE_FILE_NAME_EMPTY_INPUTS = [
    pytest.param(None, id="none"),
    pytest.param("", id="empty_string"),
]

GENERATE_DATA_LENGTHS = [
    pytest.param(0, 0, id="zero_rows"),
    pytest.param(1, 1, id="single_row"),
    pytest.param(5, 5, id="small_number_of_rows"),
    pytest.param(1_000, 1_000, id="large_number_of_rows"),
]

PARSE_NUM_ROWS_FALLBACK_INPUTS = [
    pytest.param("abc", id="letters"),
    pytest.param("!#$[", id="special_characters"),
    pytest.param("-2", id="negative_integer"),
    pytest.param("10-", id="trailing_minus"),
    pytest.param("10.5", id="decimal"),
    pytest.param("0", id="zero"),
    pytest.param("", id="empty_string"),
]

GENERATE_DATA_IDS = [
    pytest.param(1, [1], id="single_row"),
    pytest.param(5, [1, 2, 3, 4, 5], id="small_number_of_rows"),
]
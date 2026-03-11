import time

from dotenv import load_dotenv

from project_csv.validators import parse_num_rows
from project_csv.utils import generate_data, export_to_csv


def main():
    """Run the interactive CSV sample-data exporter.

    Orchestrates the full workflow:
    1. Loads environment variables from `.env` (provides ``NUM_ROWS_DEFAULT``).
    2. Prompts the user for an output file name — spaces are replaced with
       underscores and the ``.csv`` extension is appended automatically;
       an empty input produces a random UUID4 file name.
    3. Prompts the user for the number of rows — accepts plain integers or
       underscore-formatted numbers (e.g. ``10_000``); a missing, non-numeric,
       negative, or zero value falls back to ``NUM_ROWS_DEFAULT`` from ``.env``.
    4. Generates the requested number of sample rows, each containing:
       ``id`` (sequential int), ``code`` (3–12 random uppercase letters/digits),
       and ``cost`` (random float in [0.0, 1000.0]).
    5. Writes the data to a CSV file inside the ``data/`` directory, creating
       it if it does not exist.
    6. Prints the total execution time (steps 4–5) in seconds.

    Raises:
        ValueError: If the row count cannot be resolved (invalid input *and*
            ``NUM_ROWS_DEFAULT`` is missing or non-numeric in ``.env``).
        OSError: If the ``data/`` directory or the CSV file cannot be created
            or written (e.g. insufficient permissions, full disk).
    """
    load_dotenv()
    file_name = input(
        "Enter the file name (or press Enter "
        "to generate a random name): "
    )
    num_rows = input(
        "Enter the number of rows for the .csv file "
        "(or press Enter to use the default row count): "
    )
    num_rows = parse_num_rows(num_rows)
    start_time = time.time()
    data = generate_data(num_rows)
    export_to_csv(data, file_name=file_name)
    end_time = time.time()
    delta_time = end_time - start_time
    print(f"Execution time: {delta_time:.4f} seconds")


if __name__ == "__main__":
    main()

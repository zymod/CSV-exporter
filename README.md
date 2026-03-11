# CSV Sample Data Exporter

A minimalist CLI tool for exporting sample data in CSV format.
The project is designed with a focus on:

- separation of concerns,
- testability,
- determinism,
- file operation safety,
- scalability.


## Table of Contents

- [Project Goal](#project-goal)
- [Architecture](#architecture)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Tests](#tests)
- [Design Decisions](#design-decisions)
- [Security](#security)
- [Roadmap](#roadmap)


## Project Goal

The goal of the project is to export a CSV file with sample test data
in a way that is:

- configurable,
- predictable,
- secure,
- easy to test.

The project can serve as:

- a test data exporter,
- an example of a well-structured small Python project.


## Architecture

The project separates responsibilities into layers:

- CLI / entrypoint – accepts input arguments
- Validation and parsing – processes input data
- Domain layer – exportes data
- I/O layer – writes data to disk

This approach:

- simplifies testing
- allows I/O to be mocked
- minimises coupling between modules


## Requirements

- Python ≥ 3.10
- pip


## Installation

### 1. Create a virtual environment (optional)

#### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

#### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
pip install -e .
```

Installing in editable mode (`-e`) enables:

- use of absolute imports
- consistency between the development and test environments


## Configuration

The project uses a `.env` file.

Supported environment variables:
- `NUM_ROWS_DEFAULT`


## Usage

```bash
python main.py
```

The program runs interactively — on startup it prompts for input:

```
Enter the file name (or press Enter to generate a random name): sample.csv
Enter the number of rows for the .csv file (or press Enter to use the default row count): 1000
Execution time: 0.0123 seconds
```

Skipping both values (Enter) — name and row count are generated automatically.


### Application Behaviour

**File name**

- No `file_name` → UUID is generated
- File saved in the `data/` directory

**num_rows validation**

- **CLI / interactive run**
  - No value → fallback to **NUM_ROWS_DEFAULT**
  - Negative values → fallback to **NUM_ROWS_DEFAULT**
  - Value 0 → fallback to **NUM_ROWS_DEFAULT**
  - Underscore-formatted numbers (`10_000`) → parsed correctly
  - Unparseable values (e.g. `"abc"`) → **ValueError** raised with a message

- **Configuration file (.env)**
  - No value → **ValueError** raised with error description
  - Negative values / 0 → fallback to **NUM_ROWS_DEFAULT**
  - Underscore-formatted numbers → parsed correctly

## Project Structure

```
├── main.py
├── pyproject.toml
├── README.md
├── requirements.txt
├── src
│   └── project_csv
│       ├── __init__.py
│       ├── utils.py
│       └── validators.py
└── tests
    ├── data
    ├── fixtures.py
    ├── __init__.py
    ├── test_utils.py
    └── test_validators.py
```


## Tests

### Philosophy

Tests focus on:

- business logic
- edge cases
- input/output contracts
- I/O isolation

### Test Scope

**1. Input validation**

- negative values
- zero
- numbers with underscores
- unparseable data
- missing argument

**2. File name generation**

- UUID generated when no name is provided
- format correctness
- no dependency on global state

**3. CSV generation**

- correct number of records
- correct headers
- data structure matches the contract

**4. I/O tests**

- writing to a temporary directory (`tmp_path`)
- no modification of the development environment
- isolation of file operations

### Running Tests

```bash
pytest
```


### Test Coverage

```bash
pytest --cov=project_csv --cov-report=term-missing
```

The project has **100% test coverage** for core modules:

- `utils.py` – 100%
- `validators.py` – 100%


## Design Decisions

### 1. Fallback instead of exception for negative values

Negative `num_rows` is treated as invalid but non-critical input.
A fallback to `NUM_ROWS_DEFAULT` is applied.

Reason:

- a CLI tool should be resilient to erroneous user input.

### 2. Support for `10_000`

Improves CLI ergonomics and aligns with Python conventions.

### 3. Absolute imports

All imports are absolute relative to the package:

```python
from project_csv.utils import ...
```

Reason:

- compatibility with editable installation
- no dependency on the current working directory

### 4. Separation of logic from I/O

Data export logic does not depend on the file system.
This enables:

- testing without mocking the entire environment


## Security

Planned:

- path traversal protection
- safe file writing (no overwriting)


## Roadmap

- [x] Sample data export
- [x] Fallback for values ≤ 0
- [x] CSV writing
- [ ] Safe Save (suffix on conflict)
- [ ] Streaming generation (memory-efficient)
- [ ] Input path validation

### Future Development

- JSON export
- streaming generator support
- typing and input validation using Pydantic models
- CLI based on typer or click


## License

MIT


## Author

A demonstration project showcasing approaches to:

- small project structure
- testability
- deliberate design decisions
- clear technical documentation

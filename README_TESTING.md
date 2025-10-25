# Testing Guide

This document explains how to set up and run tests for the Web_page_Screenshot_Segmentation project.

## Prerequisites

- Python 3.9 or higher
- `uv` package manager (recommended)

## Setup

### 1. Create a Virtual Environment

```bash
uv venv
```

Activate it:
- **Linux/macOS**: `source .venv/bin/activate`
- **Windows (PowerShell)**: `.venv\Scripts\activate`
- **Windows (CMD)**: `.venv\Scripts\activate.bat`

### 2. Install Dependencies with Dev Tools

```bash
uv pip install -e ".[dev]"
```

This installs:
- The package in editable mode (changes to source reflect immediately)
- All runtime dependencies (opencv-python, numpy, Pillow)
- Dev dependencies (pytest, pytest-cov)

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Verbose Output

```bash
pytest -v
```

### Run Specific Test File

```bash
pytest test/test_master.py -v
```

### Run Specific Test Class

```bash
pytest test/test_master.py::TestSplitHeights -v
```

### Run Specific Test Function

```bash
pytest test/test_master.py::TestSplitHeights::test_split_heights_with_unicode_filename -v
```

### Run Tests with Coverage Report

```bash
pytest --cov=Web_page_Screenshot_Segmentation --cov-report=term-missing
```

### Generate HTML Coverage Report

```bash
pytest --cov=Web_page_Screenshot_Segmentation --cov-report=html
```

Then open `htmlcov/index.html` in your browser.

## Test Organization

Tests are organized in the `test/` directory:

- **`test_master.py`** — Tests for image loading and split height detection
  - `TestRemoveCloseValues` — Tests for the helper function
  - `TestSplitHeights` — Tests for main splitting function with Unicode file path support

- **`test_blank_spliter.py`** — Tests for blank region detection
  - `TestBlankSpliter` — Tests for low variation region detection

- **`test_color_spliter.py`** — Tests for color-based splitting
  - `TestColorSpliter` — Tests for color height detection

- **`conftest.py`** — Pytest configuration and shared fixtures
  - `test_images_dir` — Path to test images
  - `sample_image_path` — Fixture providing a test image
  - `unicode_image_path` — Fixture for testing Unicode filename support

## Test Markers

Tests are marked with markers for easy filtering:

- `@pytest.mark.unit` — Unit tests (fast)
- `@pytest.mark.integration` — Integration tests
- `@pytest.mark.slow` — Slow running tests

Run only unit tests:

```bash
pytest -m unit
```

Exclude slow tests:

```bash
pytest -m "not slow"
```

## Current Coverage

Current test coverage:

| Module | Coverage |
|--------|----------|
| blank_spliter.py | 100% |
| color_spliter.py | 100% |
| master.py | 74% |
| __init__.py | 100% |
| drawer.py | 27% |
| spliter.py | 23% |
| **Overall** | **57%** |

## Adding New Tests

1. Create test functions in appropriate test file (or create new file)
2. Use naming convention: `test_*.py` for files, `test_*` for functions
3. Use pytest assertions and fixtures
4. Mark with appropriate markers if needed

Example:

```python
@pytest.mark.unit
def test_my_feature(sample_image_path):
    """Test description."""
    result = my_function(sample_image_path)
    assert result is not None
```

## Notes

- Tests use real image files from the `images/` directory
- Unicode filename support is tested with the file `16、奈氏图绘制.png`
- Temporary test outputs are created in system temp directory and cleaned up automatically
- If image files are missing, some tests will be skipped with a message

## Continuous Integration

To add CI/CD, create a `.github/workflows/tests.yml` file:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
      - uses: astral-sh/setup-uv@v1
      - run: uv venv
      - run: uv pip install -e ".[dev]"
      - run: pytest --cov
```

"""
ASCII Diagram Enforcer - Test Suite

Test package initialization with common fixtures and utilities.

Implements: Test infrastructure for comprehensive validation coverage
Requirements: pytest >=7.0.0

Author: DDR System Integration Team
Version: 1.0.0
"""

from pathlib import Path


# Test data directories
TESTS_DIR = Path(__file__).parent
FIXTURES_DIR = TESTS_DIR / "fixtures"
TEST_DATA_DIR = TESTS_DIR / "test_data"


def get_fixture_content(fixture_name: str) -> str:
    """
    Load fixture file content.

    Parameters
    ----------
    fixture_name : str
        Name of fixture file (without path).

    Returns
    -------
    str
        Fixture file content.

    Examples
    --------
    >>> content = get_fixture_content("valid_sad_section.rst")
    >>> ".. sad::" in content
    True
    """
    fixture_path = FIXTURES_DIR / fixture_name

    if not fixture_path.exists():
        raise FileNotFoundError(f"Fixture not found: {fixture_name}")

    return fixture_path.read_text(encoding='utf-8')


def get_test_data(data_file: str) -> str:
    """
    Load test data file content.

    Parameters
    ----------
    data_file : str
        Name of test data file.

    Returns
    -------
    str
        Test data content.

    Examples
    --------
    >>> diagrams = get_test_data("sample_diagrams.txt")
    >>> len(diagrams) > 0
    True
    """
    data_path = TEST_DATA_DIR / data_file

    if not data_path.exists():
        raise FileNotFoundError(f"Test data not found: {data_file}")

    return data_path.read_text(encoding='utf-8')


# Common test constants
VALID_SAD_TAG_IDS = [
    "SAD-1",
    "SAD-10",
    "SAD-1.1",
    "SAD-1.10",
    "SAD-99.99"
]

INVALID_SAD_TAG_IDS = [
    "sad-1",      # Lowercase
    "SAD_1",      # Wrong separator
    "BRD-1",      # Wrong tier
    "SAD-",       # Missing number
    "SAD-1.",     # Trailing dot
]

MINIMAL_VALID_DIAGRAM = """
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
"""

TOO_SHORT_DIAGRAM = """
Core --> UI
"""


__all__ = [
    "TESTS_DIR",
    "FIXTURES_DIR",
    "TEST_DATA_DIR",
    "get_fixture_content",
    "get_test_data",
    "VALID_SAD_TAG_IDS",
    "INVALID_SAD_TAG_IDS",
    "MINIMAL_VALID_DIAGRAM",
    "TOO_SHORT_DIAGRAM",
]

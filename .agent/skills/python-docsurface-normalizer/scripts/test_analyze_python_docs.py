"""
Provide semantic validation of the Python documentation analyzer.

role: unit-test-suite
entrypoints: pytest compatible
reads: temporary python files
writes: temporary python files (lifecycle managed)
external_io: fs (read/write/delete)
state_model: stateless
failure_surface: fs-io, assertion-errors
coupling: analyze_python_docs
determinism: deterministic
concurrency: thread-safe
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from analyze_python_docs import analyze_targets  # noqa: E402

def write_file(path: Path, content: str) -> None:
    """
    Create a file with de-indented multi-line content for testing purposes.

    purpose: test-fixture generation
    preconditions: path parent is writable
    postconditions: file exists at path with dedented content
    mutates: filesystem
    reads: none
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe (fs write)
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        target file path
    content : str
        raw multi-line content to dedent and write
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(dedent(content).lstrip(), encoding="utf-8")

def test_analyzer_marks_existing_docstrings_and_non_directive_comments() -> None:
    """
    Verify that the analyzer correctly identifies docstrings and semantic comments.

    purpose: documentation-surface identification validation
    preconditions: none
    postconditions: assertions pass
    mutates: filesystem (temporary file)
    reads: filesystem
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe (fs write)
    ordering: none
    aliasing: none
    security: none
    coupling: analyze_python_docs
    """
    path = SCRIPT_DIR / "_tmp_test_analyze_sample.py"
    try:
        write_file(
            path,
            '''
            """Module summary."""

            # semantic comment
            VALUE = 1  # noqa: F401

            class Example:
                """Class summary."""

                def run(self) -> int:
                    """Return the current value."""
                    return VALUE
            ''',
        )

        result = analyze_targets([path])[0]
        assert result.eligible is True
        assert result.parse_ok is True
        assert result.module_docstring_present is True
        assert result.public_class_count == 1
        assert result.public_function_count == 0
        assert result.docstring_count == 3
        assert result.comment_count == 2
        assert result.directive_comment_count == 1
        assert result.preserve_sensitive is True
        assert "3 existing docstring(s)" in result.preserve_reasons
        assert "1 non-directive comment(s)" in result.preserve_reasons
    finally:
        path.unlink(missing_ok=True)

def test_analyzer_rejects_schema_mirror_paths(tmp_path: Path) -> None:
    """
    Verify that the analyzer correctly excludes schema mirror paths.

    purpose: eligibility-exclusion validation
    preconditions: none
    postconditions: assertions pass
    mutates: filesystem (temporary file)
    reads: filesystem
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe (fs write)
    ordering: none
    aliasing: none
    security: none
    coupling: analyze_python_docs

    Parameters
    ----------
    tmp_path : Path
        pytest fixture providing a temporary directory
    """
    path = tmp_path / "resources" / "schema" / "example.py"
    write_file(path, "VALUE = 1\n")

    result = analyze_targets([path])[0]
    assert result.eligible is False
    assert "schema_mirror_target" in result.hard_exclusions

def test_analyzer_reports_parse_failures_without_hiding_comments(tmp_path: Path) -> None:
    """
    Verify that comment scanning works even if the AST cannot be parsed.

    purpose: robust analysis validation
    preconditions: none
    postconditions: assertions pass
    mutates: filesystem (temporary file)
    reads: filesystem
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe (fs write)
    ordering: none
    aliasing: none
    security: none
    coupling: analyze_python_docs

    Parameters
    ----------
    tmp_path : Path
        pytest fixture providing a temporary directory
    """
    path = tmp_path / "broken.py"
    write_file(
        path,
        """
        def broken(
            # semantic note
            return 1
        """,
    )

    result = analyze_targets([path])[0]
    assert result.eligible is True
    assert result.parse_ok is False
    assert result.comment_count == 1
    assert result.directive_comment_count == 0
    assert result.preserve_sensitive is True


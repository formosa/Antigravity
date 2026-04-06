"""
Provide semantic validation of the documentation and comment stripper.

role: unit-test-suite
entrypoints: pytest compatible
reads: temporary python files
writes: temporary python files (lifecycle managed)
external_io: fs (read/write)
state_model: stateless
failure_surface: assertion-errors, value-errors
coupling: strip_comments
determinism: deterministic
concurrency: thread-safe
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

import pytest

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from strip_comments import process_file  # noqa: E402

def write_file(path: Path, content: str) -> None:
    """
    Write de-indented source code to a file for testing.

    purpose: test-fixture generation
    preconditions: path parent directory exists
    postconditions: file exists at path with content
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
        destination file path
    content : str
        raw multi-line string to write
    """
    path.write_text(dedent(content).lstrip(), encoding="utf-8")

def test_strip_comments_preserves_directives_and_removes_non_directive_docs(tmp_path: Path) -> None:
    """
    Verify that the stripper preserves tooling pragmas and removes and non-directive text.

    purpose: stripping-precision validation
    preconditions: none
    postconditions: assertions pass
    mutates: filesystem
    reads: filesystem
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: strip_comments

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory fixture
    """
    path = tmp_path / "sample.py"
    write_file(
        path,
        '''
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        """Module docstring."""

        VALUE = 1  # noqa: F401
        # semantic comment
        # pylint: disable=unused-variable

        def run() -> int:
            """Return the current value."""
            current = VALUE  # type: ignore[assignment]
            # semantic branch note
            return current
        ''',
    )

    result = process_file(path, write=False)
    assert result.removed_docstrings == 2
    assert result.removed_comments == 2
    assert result.preserved_directive_comments == 5
    assert "#!/usr/bin/env python3" in result.rewritten_source
    assert "# -*- coding: utf-8 -*-" in result.rewritten_source
    assert "# noqa: F401" in result.rewritten_source
    assert "# pylint: disable=unused-variable" in result.rewritten_source
    assert "# type: ignore[assignment]" in result.rewritten_source
    assert "Module docstring" not in result.rewritten_source
    assert "Return the current value." not in result.rewritten_source
    assert "semantic comment" not in result.rewritten_source
    assert "semantic branch note" not in result.rewritten_source

def test_strip_comments_writes_in_place_when_requested(tmp_path: Path) -> None:
    """
    Verify that changes are correctly persisted to disk when requested.

    purpose: side-effect validation (disk write)
    preconditions: none
    postconditions: assertions pass
    mutates: filesystem
    reads: filesystem
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: strip_comments

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory fixture
    """
    path = tmp_path / "write_test.py"
    write_file(
        path,
        '''
        """Module docstring."""

        VALUE = 1
        # remove me
        ''',
    )

    result = process_file(path, write=True)
    assert result.write_applied is True
    updated = path.read_text(encoding="utf-8")
    assert "Module docstring" not in updated
    assert "remove me" not in updated

def test_strip_comments_rejects_syntax_invalid_input(tmp_path: Path) -> None:
    """
    Verify that the stripper rejects malformed Python source code.

    purpose: error-handling validation
    preconditions: none
    postconditions: assertions pass
    mutates: filesystem
    reads: filesystem
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: strip_comments

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory fixture
    """
    path = tmp_path / "broken.py"
    write_file(
        path,
        """
        def broken(
            return 1
        """,
    )

    with pytest.raises(ValueError):
        process_file(path, write=False)


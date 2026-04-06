"""
Provide semantic validation of the AST structural comparator.

role: unit-test-suite
entrypoints: pytest compatible
reads: temporary python files
writes: temporary python files (lifecycle managed)
external_io: fs (read/write)
state_model: stateless
failure_surface: assertion-errors
coupling: compare_ast
determinism: deterministic
concurrency: thread-safe
"""

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from compare_ast import compare_files  # noqa: E402

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

def test_compare_ast_ignores_docstring_differences(tmp_path: Path) -> None:
    """
    Prove that docstring text changes do not trigger AST mismatches.

    purpose: structural-equivalence validation (docstrings)
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
    coupling: compare_ast

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory fixture
    """
    before = tmp_path / "before.py"
    after = tmp_path / "after.py"
    write_file(
        before,
        '''
        def run() -> int:
            """Return one."""
            return 1
        ''',
    )
    write_file(
        after,
        '''
        def run() -> int:
            """Return the canonical integer constant."""
            return 1
        ''',
    )

    success, message = compare_files(before, after)
    assert success is True
    assert message.startswith("AST VERIFIED:")

def test_compare_ast_ignores_comment_only_differences(tmp_path: Path) -> None:
    """
    Prove that comment differences do not trigger AST mismatches.

    purpose: structural-equivalence validation (comments)
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
    coupling: compare_ast

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory fixture
    """
    before = tmp_path / "before.py"
    after = tmp_path / "after.py"
    write_file(
        before,
        """
        VALUE = 1
        # semantic note
        """,
    )
    write_file(
        after,
        """
        VALUE = 1
        # updated semantic note
        """,
    )

    success, _ = compare_files(before, after)
    assert success is True

def test_compare_ast_detects_logic_changes(tmp_path: Path) -> None:
    """
    Prove that actual code logic changes are correctly detected as AST mismatches.

    purpose: mismatch detection validation
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
    coupling: compare_ast

    Parameters
    ----------
    tmp_path : Path
        pytest temporary directory fixture
    """
    before = tmp_path / "before.py"
    after = tmp_path / "after.py"
    write_file(before, "VALUE = 1\n")
    write_file(after, "VALUE = 2\n")

    success, message = compare_files(before, after)
    assert success is False
    assert message.startswith("AST MISMATCH:")


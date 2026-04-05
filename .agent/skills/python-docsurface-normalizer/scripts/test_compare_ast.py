from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from compare_ast import compare_files  # noqa: E402


def write_file(path: Path, content: str) -> None:
    path.write_text(dedent(content).lstrip(), encoding="utf-8")


def test_compare_ast_ignores_docstring_differences(tmp_path: Path) -> None:
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
    before = tmp_path / "before.py"
    after = tmp_path / "after.py"
    write_file(before, "VALUE = 1\n")
    write_file(after, "VALUE = 2\n")

    success, message = compare_files(before, after)
    assert success is False
    assert message.startswith("AST MISMATCH:")

from __future__ import annotations

import sys
from pathlib import Path
from textwrap import dedent

import pytest


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from strip_comments import process_file  # noqa: E402


def write_file(path: Path, content: str) -> None:
    path.write_text(dedent(content).lstrip(), encoding="utf-8")


def test_strip_comments_preserves_directives_and_removes_non_directive_docs(tmp_path: Path) -> None:
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

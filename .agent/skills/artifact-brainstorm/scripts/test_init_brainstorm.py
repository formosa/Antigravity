from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from init_brainstorm import DEFAULT_SOURCE_REFERENCE, render_seed  # noqa: E402


REPO_ROOT = SCRIPT_DIR.parents[3]
SEED_PATH = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"
EXPECTED_REFERENCE = ".agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml"


def test_default_source_reference_points_to_xhtml() -> None:
    assert DEFAULT_SOURCE_REFERENCE.name == "DDR_AppFramework_Brainstorm.xhtml"
    assert DEFAULT_SOURCE_REFERENCE.as_posix().endswith(EXPECTED_REFERENCE)


def test_render_seed_records_xhtml_reference() -> None:
    rendered = render_seed(SEED_PATH.read_text(encoding="utf-8"), DEFAULT_SOURCE_REFERENCE)

    assert "{{SOURCE_REFERENCE_PATH}}" not in rendered
    assert EXPECTED_REFERENCE in rendered

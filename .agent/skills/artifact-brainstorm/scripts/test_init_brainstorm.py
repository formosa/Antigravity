"""
Unit tests for init_brainstorm.py.

role: unit test suite for brainstorm initialization logic
entrypoints: pytest
reads: init_brainstorm.py, brainstorm seed
writes: none
external_io: fs (read-only)
state_model: stateless
failure_surface: none
coupling: highly coupled to init_brainstorm.py
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# INVARIANT: local import after path injection
from init_brainstorm import DEFAULT_SOURCE_REFERENCE, render_seed  # noqa: E402


REPO_ROOT = SCRIPT_DIR.parents[3]
SEED_PATH = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"
EXPECTED_REFERENCE = ".agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml"


def test_default_source_reference_points_to_xhtml() -> None:
    """
    Verify the default source reference path and filename.

    purpose: integration/config validation
    """
    assert DEFAULT_SOURCE_REFERENCE.name == "DDR_AppFramework_Brainstorm.xhtml"
    assert DEFAULT_SOURCE_REFERENCE.as_posix().endswith(EXPECTED_REFERENCE)


def test_render_seed_records_xhtml_reference() -> None:
    """
    Verify that rendering correctly replaces template placeholders with the reference path.

    purpose: functionality test for template rendering
    """
    rendered = render_seed(SEED_PATH.read_text(encoding="utf-8"), DEFAULT_SOURCE_REFERENCE)

    assert "{{SOURCE_REFERENCE_PATH}}" not in rendered
    assert EXPECTED_REFERENCE in rendered

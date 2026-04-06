"""
Unit tests for validate_brainstorm.py.

role: unit test suite for brainstorm validation logic
entrypoints: pytest
reads: validate_brainstorm.py, brainstorm seed
writes: none (uses tmp_path)
external_io: fs
state_model: stateless
failure_surface: none
coupling: highly coupled to validate_brainstorm.py and brainstorm schema
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

# INVARIANT: local import after path injection
from validate_brainstorm import audit_brainstorm, validate_brainstorm  # noqa: E402


REPO_ROOT = SCRIPT_DIR.parents[3]
SEED_PATH = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"


def initialized_seed_text() -> str:
    """
    Generate valid brainstorm text based on the seed template.

    purpose: test fixture generation
    """
    return (
        SEED_PATH.read_text(encoding="utf-8")
        .replace("{{CREATED_DATE}}", "2026-03-30")
        .replace("{{LAST_REVISED_DATE}}", "2026-03-30")
        .replace("{{SOURCE_REFERENCE_PATH}}", ".agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml")
    )


def test_initialized_seed_validates(tmp_path: Path) -> None:
    """
    Verify that an correctly initialized seed file passes validation.

    purpose: success path validation
    """
    path = tmp_path / "brainstorm.md"
    path.write_text(initialized_seed_text(), encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert errors == []


def test_audit_runs_on_initialized_seed(tmp_path: Path) -> None:
    """
    Verify that the audit function returns a list on valid input.

    purpose: basic audit functionality check
    """
    path = tmp_path / "brainstorm.md"
    path.write_text(initialized_seed_text(), encoding="utf-8")

    warnings = audit_brainstorm(path)
    assert isinstance(warnings, list)


def test_unknown_brain_class_fails(tmp_path: Path) -> None:
    """
    Verify that invalid CSS classes in the markdown trigger validation errors.

    purpose: schema enforcement test
    """
    text = initialized_seed_text()
    mutated = text.replace("brain-risk", "brain-unknown", 1)
    path = tmp_path / "brainstorm.md"
    path.write_text(mutated, encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert any("Unknown brain-* class" in error for error in errors)


def test_missing_citation_ids_fail(tmp_path: Path) -> None:
    """
    Verify that missing required frontmatter fields trigger validation errors.

    purpose: mandatory field validation
    """
    text = initialized_seed_text()
    mutated = re.sub(r"\ncitation_ids:\n(?:- .+\n)+", "\n", text, count=1)
    path = tmp_path / "brainstorm.md"
    path.write_text(mutated, encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert any("missing common field(s): citation_ids" in error for error in errors)


def test_current_citation_staleness_fails(tmp_path: Path) -> None:
    """
    Verify that stale citations trigger validation errors.

    purpose: semantic validation (staleness check)
    """
    text = initialized_seed_text()
    mutated = text.replace("published_date: '2026-03-04'", "published_date: '2025-03-04'", 1)
    path = tmp_path / "brainstorm.md"
    path.write_text(mutated, encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert any("is more than 183 days" in error for error in errors)

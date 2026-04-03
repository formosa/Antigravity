from __future__ import annotations

import re
import sys
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SCRIPT_DIR))

from validate_brainstorm import audit_brainstorm, validate_brainstorm  # noqa: E402


REPO_ROOT = SCRIPT_DIR.parents[3]
SEED_PATH = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"


def initialized_seed_text() -> str:
    return (
        SEED_PATH.read_text(encoding="utf-8")
        .replace("{{CREATED_DATE}}", "2026-03-30")
        .replace("{{LAST_REVISED_DATE}}", "2026-03-30")
        .replace("{{SOURCE_REFERENCE_PATH}}", ".agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.docx")
    )


def test_initialized_seed_validates(tmp_path: Path) -> None:
    path = tmp_path / "brainstorm.md"
    path.write_text(initialized_seed_text(), encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert errors == []


def test_audit_runs_on_initialized_seed(tmp_path: Path) -> None:
    path = tmp_path / "brainstorm.md"
    path.write_text(initialized_seed_text(), encoding="utf-8")

    warnings = audit_brainstorm(path)
    assert isinstance(warnings, list)


def test_unknown_brain_class_fails(tmp_path: Path) -> None:
    text = initialized_seed_text()
    mutated = text.replace("brain-risk", "brain-unknown", 1)
    path = tmp_path / "brainstorm.md"
    path.write_text(mutated, encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert any("Unknown brain-* class" in error for error in errors)


def test_missing_citation_ids_fail(tmp_path: Path) -> None:
    text = initialized_seed_text()
    mutated = re.sub(r"\ncitation_ids:\n(?:- .+\n)+", "\n", text, count=1)
    path = tmp_path / "brainstorm.md"
    path.write_text(mutated, encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert any("missing common field(s): citation_ids" in error for error in errors)


def test_current_citation_staleness_fails(tmp_path: Path) -> None:
    text = initialized_seed_text()
    mutated = text.replace("published_date: '2026-03-04'", "published_date: '2025-03-04'", 1)
    path = tmp_path / "brainstorm.md"
    path.write_text(mutated, encoding="utf-8")

    errors = validate_brainstorm(path, SEED_PATH)
    assert any("is more than 183 days" in error for error in errors)

"""
Unit tests for validate_issue_report.py.

role: unit test suite for issue report validation logic
entrypoints: pytest
reads: validate_issue_report.py, issue report examples
writes: none
external_io: fs (read-only)
state_model: stateless
failure_surface: none
coupling: highly coupled to validate_issue_report.py and issue report schema
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("validate_issue_report.py")
REPO_ROOT = Path(__file__).resolve().parents[4]
CANONICAL_EXAMPLE_PATH = REPO_ROOT / ".agent" / "schemas" / "issue" / "example.md"
LEGACY_EXAMPLE_PATH = REPO_ROOT / ".agent" / "schemas" / "issue" / "example-legacy-v4.md"

spec = importlib.util.spec_from_file_location("validate_issue_report", SCRIPT_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def test_canonical_example_is_valid() -> None:
    """
    Verify that the canonical example issue report passes validation.

    purpose: success path validation for canonical reports
    """
    label, errors, notes = module.validate_path(CANONICAL_EXAMPLE_PATH, mode="canonical")
    assert label == "canonical"
    assert errors == []
    assert notes == []


def test_legacy_example_is_valid() -> None:
    """
    Verify that the legacy v4 example issue report passes validation in auto-detection mode.

    purpose: success path validation for legacy reports
    """
    label, errors, notes = module.validate_path(LEGACY_EXAMPLE_PATH, mode="auto")
    assert label == "legacy:v4-like"
    assert errors == []
    assert notes == []


def test_missing_updated_fails() -> None:
    """
    Verify that missing required frontmatter fields trigger validation errors.

    purpose: mandatory field validation
    """
    text = CANONICAL_EXAMPLE_PATH.read_text(encoding="utf-8").replace('  updated:         "2026-04-04"\n', "", 1)
    label, errors, _ = module.validate_content(text, mode="canonical")
    assert label == "canonical"
    assert "Frontmatter is missing required keys: updated" in errors


def test_option_c_in_canonical_fails() -> None:
    """
    Verify that forbidden legacy options in canonical reports trigger errors.

    purpose: schema restriction validation
    """
    text = CANONICAL_EXAMPLE_PATH.read_text(encoding="utf-8")
    text = text.replace(
        "### 3. Comparative Analysis and Recommended Strategy",
        "#### Option C: Add an extension-only audit path\n\nThis legacy-only option should not be present in canonical reports.\n\n"
        "* **Supporting Insights:** Canonical issue reports do not allow a third option.\n"
        "* **Citations:** No authoritative external reference identified for this specific claim.\n\n"
        "### 3. Comparative Analysis and Recommended Strategy",
        1,
    )
    _, errors, _ = module.validate_content(text, mode="canonical")
    assert "Canonical reports must not contain Option C" in errors


def test_missing_implementation_note_fails() -> None:
    """
    Verify that missing required markers (headings) trigger validation errors.

    purpose: structural marker validation
    """
    text = CANONICAL_EXAMPLE_PATH.read_text(encoding="utf-8")
    text = text.replace(
        "\n### 4. Implementation Note\n\nImplementation remains pending. This canonical example illustrates the report contract only and did not apply a repository patch.\n",
        "\n",
        1,
    )
    _, errors, _ = module.validate_content(text, mode="canonical")
    assert "Missing required heading or marker: ### 4. Implementation Note" in errors
    assert "Missing section: ### 4. Implementation Note" in errors


def test_resolved_missing_resolved_fails() -> None:
    """
    Verify that reports with 'RESOLVED' status must contain specific fields.

    purpose: conditional field validation
    """
    text = CANONICAL_EXAMPLE_PATH.read_text(encoding="utf-8")
    text = text.replace('  status:          "OPEN"', '  status:          "RESOLVED"', 1)
    text = text.replace("status:      OPEN", "status:      RESOLVED", 1)
    text = text.replace(
        "Implementation remains pending. This canonical example illustrates the report contract only and did not apply a repository patch.",
        "Implemented a discriminator-based validation branch and confirmed the report remains aligned with the updated contract.",
        1,
    )
    _, errors, _ = module.validate_content(text, mode="canonical")
    assert "Canonical resolved reports must include document.resolved" in errors
    assert "Resolved canonical reports must include Agent Context resolved" in errors

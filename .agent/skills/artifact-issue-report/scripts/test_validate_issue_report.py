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
    label, errors, notes = module.validate_path(CANONICAL_EXAMPLE_PATH, mode="canonical")
    assert label == "canonical"
    assert errors == []
    assert notes == []


def test_legacy_example_is_valid() -> None:
    label, errors, notes = module.validate_path(LEGACY_EXAMPLE_PATH, mode="auto")
    assert label == "legacy:v4-like"
    assert errors == []
    assert notes == []


def test_missing_updated_fails() -> None:
    text = CANONICAL_EXAMPLE_PATH.read_text(encoding="utf-8").replace('  updated:         "2026-04-04"\n', "", 1)
    label, errors, _ = module.validate_content(text, mode="canonical")
    assert label == "canonical"
    assert "Frontmatter is missing required keys: updated" in errors


def test_option_c_in_canonical_fails() -> None:
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

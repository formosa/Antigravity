#!/usr/bin/env python3
"""
Regression tests for validate_updated_issues_tracker.py.
"""

from __future__ import annotations

import importlib.util
import re
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).with_name("validate_updated_issues_tracker.py")
REPO_ROOT = Path(__file__).resolve().parents[4]
EXAMPLE_PATH = REPO_ROOT / ".agent" / "schemas" / "issues-tracker" / "example-it-1.1.md"
REAL_TRACKER_PATH = (
    REPO_ROOT
    / ".agent"
    / "assets"
    / "proposals"
    / "active"
    / "v6.3"
    / "DDR_v6.2_Issues_Tracker.md"
)

spec = importlib.util.spec_from_file_location("validate_updated_issues_tracker", SCRIPT_PATH)
module = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(module)


def replace_section(content: str, heading: str, new_body: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    replacement = f"## {heading}\n\n{new_body.strip()}\n\n"
    return re.sub(pattern, replacement, content, count=1, flags=re.MULTILINE | re.DOTALL)


def extract_section(content: str, heading: str) -> str:
    match = re.search(
        rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group("body").strip()


def migrate_real_tracker_fixture(content: str) -> str:
    example_text = EXAMPLE_PATH.read_text(encoding="utf-8")
    issue_schema = extract_section(example_text, "ISSUE SCHEMA")
    workflow = extract_section(example_text, "RESOLUTION WORKFLOW")

    content = content.replace('format_version:  "IT-1.0"', 'format_version:  "IT-1.1"', 1)
    content = content.replace("Issues Tracker — IT-1.0*", "Issues Tracker — IT-1.1*", 1)
    content = replace_section(content, "ISSUE SCHEMA", issue_schema)
    content = replace_section(content, "RESOLUTION WORKFLOW", workflow)

    for issue_number in range(1, 12):
        suffix = f"{issue_number:03d}"
        insertion = (
            f"\n#### Resolution-{suffix}: Option C - Consolidate authority closure at the root profile boundary\n"
            "Move the fix to the narrowest shared authority boundary so the tracker can exercise a third, structurally "
            "distinct resolution path without changing the repository source files in this test fixture. This keeps the "
            "fixture realistic while remaining validator-focused.\n\n"
            f"#### Comparative Analysis-{suffix}\n"
            "Option A targets the smallest local repair, Option B raises the concern into a broader architectural change, "
            "and Option C consolidates adjacent contract edges at the root profile boundary. Option C is intentionally "
            "distinct because it changes the authority location and compatibility posture rather than just restating an "
            "existing patch.\n\n"
            f"#### Recommendation-{suffix}\n"
            "**Endorsed Option:** `Option A`\n"
            "Option A is endorsed in this migration fixture because it usually delivers the cleanest machine-readable "
            "repair with the lowest compatibility blast radius, which is enough to test the `IT-1.1` recommendation shape.\n\n"
            f"#### Supporting Citations-{suffix}\n"
            "- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance on encoding profile-specific obligations with conditional schema logic.\n"
            "- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance on closing object contracts and constraining structural authority surfaces.\n"
        )
        content = content.replace(
            f"\n#### Notes-{suffix}\n",
            f"{insertion}\n#### Notes-{suffix}\n",
            1,
        )

    return content


class ValidateUpdatedIssuesTrackerTests(unittest.TestCase):
    def validate_text(self, text: str) -> list[str]:
        return module.validate_tracker_content(text)

    def test_example_it11_is_valid(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8")
        self.assertEqual([], self.validate_text(text))

    def test_missing_citations_fails(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8")
        text = text.replace(
            "- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance on encoding profile-specific required fields with `if`/`then`.\n"
            "- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance on closing object contracts with explicit properties and `additionalProperties`.\n",
            "",
            1,
        )
        self.assertIn(
            "ISSUE-001 Supporting Citations-001 must contain at least one citation bullet",
            self.validate_text(text),
        )

    def test_duplicate_option_c_fails(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8")
        option_a_match = re.search(
            r"#### Resolution-001: Option A - (?P<label>[^\n]+)\n(?P<body>.*?)(?=^#### )",
            text,
            re.MULTILINE | re.DOTALL,
        )
        assert option_a_match is not None
        replacement = (
            "#### Resolution-001: Option C - Add `webhook_profile` Enum\n"
            f"{option_a_match.group('body')}"
        )
        text = re.sub(
            r"#### Resolution-001: Option C - [^\n]+\n.*?(?=^#### Comparative Analysis-001)",
            replacement,
            text,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIn(
            "ISSUE-001 Option C is not materially distinct from Option A or Option B",
            self.validate_text(text),
        )

    def test_unsorted_registry_fails(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8")
        unsorted = (
            "| [ISSUE-002](#issue-002-normalize-cursor-pagination-error-semantics) | `MODERATE` | `LOGICAL_CONFLICT` | `OPEN` | `Pagination surface` | Normalize cursor pagination error semantics |\n"
            "| [ISSUE-001](#issue-001-require-an-explicit-webhook-profile-discriminator) | `CRITICAL` | `SCHEMA_DEFECT` | `OPEN` | `Webhook schema` | Require an explicit webhook profile discriminator |\n"
        )
        text = re.sub(
            r"\| \[ISSUE-001\].*?\n\| \[ISSUE-002\].*?\n",
            unsorted,
            text,
            count=1,
            flags=re.MULTILINE | re.DOTALL,
        )
        self.assertIn("Issue registry rows must be sorted by severity then issue number", self.validate_text(text))

    def test_stale_counts_fail(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8").replace("open_issues:     2", "open_issues:     1", 1)
        self.assertIn(
            "document.open_issues (1) does not match OPEN+IN_REVIEW count (2)",
            self.validate_text(text),
        )

    def test_missing_recommendation_block_fails(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8")
        text = text.replace("#### Recommendation-001", "#### Recommendation-XXX", 1)
        self.assertIn("ISSUE-001 is missing subsection: Recommendation-001", self.validate_text(text))

    def test_placeholders_fail(self) -> None:
        text = EXAMPLE_PATH.read_text(encoding="utf-8").replace(
            "Option C is endorsed because the discriminator keeps the shape additive, localizes the validation branch, and avoids duplicating every common webhook property across multiple object definitions. It delivers the strongest machine-readable closure with a smaller migration surface than a full object split.",
            "{{TODO}}",
            1,
        )
        self.assertIn("Tracker contains unresolved placeholders", self.validate_text(text))

    def test_real_tracker_migration_fixture_validates_and_does_not_mutate_sources(self) -> None:
        if not REAL_TRACKER_PATH.exists():
            self.skipTest(f"Real tracker fixture is not present: {REAL_TRACKER_PATH}")

        original_bytes = REAL_TRACKER_PATH.read_bytes()
        migrated_text = migrate_real_tracker_fixture(REAL_TRACKER_PATH.read_text(encoding="utf-8"))

        with tempfile.TemporaryDirectory() as temp_dir:
            temp_path = Path(temp_dir) / "DDR_v6.2_Issues_Tracker_IT11.md"
            temp_path.write_text(migrated_text, encoding="utf-8")
            self.assertEqual([], module.validate_path(temp_path))

        self.assertEqual(original_bytes, REAL_TRACKER_PATH.read_bytes())


if __name__ == "__main__":
    unittest.main()

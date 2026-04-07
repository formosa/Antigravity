#!/usr/bin/env python3
"""
Regression tests for asset-rule tooling.

role: unit test suite for rule owner tooling
entrypoints: main
reads: local rule tooling scripts via dynamic import
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: coupled to asset-rule tooling
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent


def load_module(module_name: str, filename: str):
    """
    Load a sibling script as an importable module for testing.
    """
    script_path = SCRIPT_DIR / filename
    spec = importlib.util.spec_from_file_location(module_name, script_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


INIT_RULE = load_module("asset_rule_init_rule_test_module", "init_rule.py")
QUICK_VALIDATE = load_module("asset_rule_quick_validate_test_module", "quick_validate.py")
UPDATE_INDEX = load_module("asset_rule_update_index_test_module", "update_index.py")


class TestAssetRuleTooling(unittest.TestCase):
    """
    Test suite for the asset-rule owner tooling.
    """

    def test_build_content_replaces_name_and_description(self) -> None:
        """
        Verify rule scaffolding rewrites the expected frontmatter fields.
        """
        template = (
            "---\n"
            "name: example-rule\n"
            "description: Example description.\n"
            "priority: medium\n"
            "trigger: manual\n"
            "version: 1.0.0\n"
            "---\n"
            "\n"
            "<constraints>\n- Example.\n</constraints>\n"
        )

        content = INIT_RULE.build_content("fresh-rule", template)

        self.assertIn("name: fresh-rule", content)
        self.assertIn("TODO: Describe the rule outcome", content)

    def test_validate_rule_file_rejects_missing_constraints(self) -> None:
        """
        Verify malformed rule fixtures fail validation.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            rule_path = Path(tmpdir) / "bad-rule.md"
            rule_path.write_text(
                "---\n"
                'name: bad-rule\n'
                'description: "Rule missing its required constraints block."\n'
                "priority: high\n"
                "trigger: manual\n"
                "version: 1.0.0\n"
                "---\n",
                encoding="utf-8",
            )

            result = QUICK_VALIDATE.validate_rule_file(rule_path)

            self.assertFalse(result.valid)
            self.assertTrue(any("Missing required `<constraints>` block." in error for error in result.errors))

    def test_rule_index_generation_is_deterministic(self) -> None:
        """
        Verify discovered rule records are ordered by trigger precedence and rendered into the index.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            rules_dir = Path(tmpdir)
            (rules_dir / "zeta-rule.md").write_text(
                "---\n"
                'name: zeta-rule\n'
                'description: "Manual rule."\n'
                "trigger: manual\n"
                "priority: low\n"
                "version: 1.0.0\n"
                "---\n"
                "\n<constraints>\n- Manual.\n</constraints>\n",
                encoding="utf-8",
            )
            (rules_dir / "alpha-rule.md").write_text(
                "---\n"
                'name: alpha-rule\n'
                'description: "Always-on rule."\n'
                "trigger: always_on\n"
                "priority: critical\n"
                "version: 1.0.0\n"
                "---\n"
                "\n<constraints>\n- Always on.\n</constraints>\n",
                encoding="utf-8",
            )

            records = UPDATE_INDEX.rule_records(rules_dir)
            index_content = UPDATE_INDEX.build_index(records)

            self.assertEqual([record.rule_id for record in records], ["alpha-rule", "zeta-rule"])
            self.assertIn("## Selection Map", index_content)
            self.assertIn("alpha-rule", index_content)
            self.assertIn("zeta-rule", index_content)


if __name__ == "__main__":
    unittest.main()

#!/usr/bin/env python3
"""
Regression tests for asset-workflow tooling.

role: unit test suite for workflow owner tooling
entrypoints: main
reads: local workflow tooling scripts via dynamic import
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: coupled to asset-workflow tooling
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


INIT_WORKFLOW = load_module("asset_workflow_init_workflow_test_module", "init_workflow.py")
QUICK_VALIDATE = load_module("asset_workflow_quick_validate_test_module", "quick_validate.py")
UPDATE_INDEX = load_module("asset_workflow_update_index_test_module", "update_index.py")


class TestAssetWorkflowTooling(unittest.TestCase):
    """
    Test suite for the asset-workflow owner tooling.
    """

    def test_build_content_replaces_name_and_description(self) -> None:
        """
        Verify workflow scaffolding rewrites the expected frontmatter fields.
        """
        template = (
            "---\n"
            "name: strict-integration-deploy\n"
            "version: 1.0.0\n"
            "description: Example workflow.\n"
            "---\n"
            "\n### steps\n\n1. Example.\n"
        )

        content = INIT_WORKFLOW.build_content("agent-asset-hygiene-review", template)

        self.assertIn("name: agent-asset-hygiene-review", content)
        self.assertIn("TODO: Describe the repeatable workflow outcome", content)

    def test_validate_workflow_rejects_missing_steps(self) -> None:
        """
        Verify malformed workflow fixtures fail validation.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            workflow_path = Path(tmpdir) / "bad-workflow.md"
            workflow_path.write_text(
                "---\n"
                "name: bad-workflow\n"
                "version: 1.0.0\n"
                'description: "Workflow missing numbered steps."\n'
                "---\n"
                "\n### verification_plan\n\n- Nothing.\n",
                encoding="utf-8",
            )

            result = QUICK_VALIDATE.validate_workflow(workflow_path)

            self.assertFalse(result.valid)
            self.assertTrue(any("Missing required `### steps` section." in error for error in result.errors))

    def test_workflow_index_generation_is_deterministic(self) -> None:
        """
        Verify workflow discovery and index rendering include live workflow assets only.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            workflows_dir = Path(tmpdir)
            (workflows_dir / "index.md").write_text("ignore me\n", encoding="utf-8")
            (workflows_dir / "agent-asset-hygiene-review.md").write_text(
                "---\n"
                "name: agent-asset-hygiene-review\n"
                "version: 1.0.0\n"
                'description: "Review changed .agent assets and run the correct validators."\n'
                "---\n"
                "\n### steps\n\n1. Review.\n",
                encoding="utf-8",
            )

            records = UPDATE_INDEX.workflow_records(workflows_dir)
            index_content = UPDATE_INDEX.build_index(records)

            self.assertEqual([record.workflow_id for record in records], ["agent-asset-hygiene-review"])
            self.assertIn("## Selection Map", index_content)
            self.assertIn("agent-asset-hygiene-review", index_content)


if __name__ == "__main__":
    unittest.main()

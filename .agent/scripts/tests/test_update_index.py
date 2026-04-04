#!/usr/bin/env python3
"""Unit tests for update_index.py."""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "update_index.py"
SPEC = importlib.util.spec_from_file_location("update_index", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["update_index"] = MODULE
SPEC.loader.exec_module(MODULE)

ScriptRecord = MODULE.ScriptRecord
build_root_index = MODULE.build_root_index
build_tests_index = MODULE.build_tests_index
collect_root_script_records = MODULE.collect_root_script_records
collect_test_script_records = MODULE.collect_test_script_records
detect_tool_links = MODULE.detect_tool_links
extract_docstring_summary = MODULE.extract_docstring_summary


class TestUpdateIndex(unittest.TestCase):
    def test_extract_docstring_summary_skips_filename_banner(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            script_path = Path(tmpdir) / "validate_env.py"
            script_path.write_text(
                '"""\nvalidate_env.py\n===============\nValidation gate for the environment.\n"""\n',
                encoding="utf-8",
            )

            summary = extract_docstring_summary(script_path)

            self.assertEqual(summary, "Validation gate for the environment.")

    def test_collect_root_script_records_excludes_init_and_links_tools(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            scripts_dir = Path(tmpdir) / ".agent" / "scripts"
            tools_dir = Path(tmpdir) / ".agent" / "tools"
            scripts_dir.mkdir(parents=True)
            tools_dir.mkdir(parents=True)

            (scripts_dir / "__init__.py").write_text("", encoding="utf-8")
            (scripts_dir / "cleanup_temp_assets.py").write_text(
                '"""Cleanup temp assets."""\n',
                encoding="utf-8",
            )
            (scripts_dir / "directory_tree.py").write_text(
                '"""Generate a directory tree with reporting."""\n',
                encoding="utf-8",
            )
            (scripts_dir / "update_index.py").write_text(
                '"""Regenerate indexes."""\n',
                encoding="utf-8",
            )
            (tools_dir / "cleanup_temp_assets.md").write_text(
                "---\ncommand: '& \"${workspaceFolder}/.venv/Scripts/python.exe\" \"${workspaceFolder}/.agent/scripts/cleanup_temp_assets.py\"'\n---\n",
                encoding="utf-8",
            )

            tool_links = detect_tool_links(tools_dir)
            records = collect_root_script_records(scripts_dir, tool_links)

            self.assertEqual([record.filename for record in records], ["cleanup_temp_assets.py", "directory_tree.py", "update_index.py"])
            self.assertEqual(records[0].tool_definition, ".agent/tools/cleanup_temp_assets.md")
            self.assertEqual(records[0].category, "utility_and_infrastructure")
            self.assertEqual(records[1].category, "analysis_and_reporting")
            self.assertEqual(records[2].category, "governance_and_inventory")

    def test_collect_test_script_records_categorizes_scripts(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            tests_dir = Path(tmpdir) / ".agent" / "scripts" / "tests"
            tests_dir.mkdir(parents=True)
            (tests_dir / "test_cleanup_temp_assets.py").write_text(
                '"""Unit tests for cleanup_temp_assets.py."""\n',
                encoding="utf-8",
            )
            (tests_dir / "validate_env.py").write_text(
                '"""validate_env.py\n====\nValidation gate for the shell baseline.\n"""\n',
                encoding="utf-8",
            )
            (tests_dir / "chaos_script.py").write_text("print('chaos')\n", encoding="utf-8")

            records = collect_test_script_records(tests_dir)

            categories = {record.filename: record.category for record in records}
            self.assertEqual(categories["test_cleanup_temp_assets.py"], "unit_tests")
            self.assertEqual(categories["validate_env.py"], "diagnostics_and_validation")
            self.assertEqual(categories["chaos_script.py"], "fixtures_and_chaos")

    def test_build_indexes_emit_required_sections(self) -> None:
        root_records = [
            ScriptRecord(
                script_id="cleanup_temp_assets",
                filename="cleanup_temp_assets.py",
                relative_path=".agent/scripts/cleanup_temp_assets.py",
                category="utility_and_infrastructure",
                description="Cleanup temp assets.",
                tool_definition=".agent/tools/cleanup_temp_assets.md",
            )
        ]
        test_records = [
            ScriptRecord(
                script_id="test_cleanup_temp_assets",
                filename="test_cleanup_temp_assets.py",
                relative_path=".agent/scripts/tests/test_cleanup_temp_assets.py",
                category="unit_tests",
                description="Unit tests for cleanup_temp_assets.py.",
            )
        ]

        root_index = build_root_index(root_records)
        tests_index = build_tests_index(test_records)

        self.assertIn("## Use This Index", root_index)
        self.assertIn("## Manifest", root_index)
        self.assertIn("## Script Records", root_index)
        self.assertIn("cleanup_temp_assets.md", root_index)
        self.assertIn("## Use This Index", tests_index)
        self.assertIn("## Manifest", tests_index)
        self.assertIn("## Test Script Records", tests_index)


if __name__ == "__main__":
    unittest.main()

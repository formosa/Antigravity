#!/usr/bin/env python3
"""
Regression tests for core-schema tooling.

role: unit test suite for core schema tooling
entrypoints: main
reads: local core-schema scripts via copied temp repo layouts
writes: nothing durable (uses tempfile)
external_io: fs, subprocess
state_model: stateless
failure_surface: none
coupling: coupled to core-schema tooling
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_DIR = SCRIPT_DIR.parent


class TestCoreSchemaTooling(unittest.TestCase):
    """
    Test suite for the core-schema owner tooling.
    """

    def _prepare_temp_repo(self, tmpdir: str) -> tuple[Path, Path]:
        """
        Create a temp repo layout matching the scripts' path expectations.
        """
        root = Path(tmpdir)
        temp_skill_dir = root / ".agent" / "skills" / "core-schema"
        temp_scripts_dir = temp_skill_dir / "scripts"
        temp_scripts_dir.mkdir(parents=True, exist_ok=True)

        for filename in ("scaffold_schema.py", "validate_schema.py", "update_index.py"):
            shutil.copy2(SCRIPT_DIR / filename, temp_scripts_dir / filename)
        shutil.copy2(SKILL_DIR / "config.json", temp_skill_dir / "config.json")
        return root, temp_scripts_dir

    def test_scaffold_schema_copies_example_into_target_dir(self) -> None:
        """
        Verify schema scaffolding copies the source example into the new schema directory.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            root, temp_scripts_dir = self._prepare_temp_repo(tmpdir)
            source_example = root / "seed.md"
            source_example.write_text("# Example\n", encoding="utf-8")

            result = subprocess.run(
                [
                    sys.executable,
                    str(temp_scripts_dir / "scaffold_schema.py"),
                    "--target-file",
                    str(source_example),
                    "--name",
                    "demo-schema",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 0)
            self.assertTrue((root / ".agent" / "schemas" / "demo-schema" / "example.md").exists())

    def test_validate_schema_rolls_back_from_backup_on_failure(self) -> None:
        """
        Verify failed schema validation restores the last backup file.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            root, temp_scripts_dir = self._prepare_temp_repo(tmpdir)
            schema_dir = root / ".agent" / "schemas" / "demo"
            schema_dir.mkdir(parents=True, exist_ok=True)
            dts_path = schema_dir / "demo.d.ts"
            backup_path = schema_dir / "demo.d.ts.bak"
            dts_path.write_text("current\n", encoding="utf-8")
            backup_path.write_text("backup\n", encoding="utf-8")

            tsc_dir = root / ".nodeenv" / "Scripts"
            tsc_dir.mkdir(parents=True, exist_ok=True)
            (tsc_dir / "tsc.cmd").write_text(
                "@echo off\n"
                "echo simulated TypeScript failure 1>&2\n"
                "exit /b 1\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [
                    sys.executable,
                    str(temp_scripts_dir / "validate_schema.py"),
                    "--name",
                    "demo",
                ],
                cwd=root,
                capture_output=True,
                text=True,
            )

            self.assertEqual(result.returncode, 1)
            self.assertEqual(dts_path.read_text(encoding="utf-8"), "backup\n")

    def test_update_index_writes_schema_table_from_readmes(self) -> None:
        """
        Verify schema index regeneration reads README metadata into the canonical table.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            root, temp_scripts_dir = self._prepare_temp_repo(tmpdir)
            schema_dir = root / ".agent" / "schemas" / "alpha"
            schema_dir.mkdir(parents=True, exist_ok=True)
            (schema_dir / "README.md").write_text(
                "<document_purpose>\nAlpha schema purpose.\n</document_purpose>\n\n"
                "<modification_history>\n"
                "| Date | Version | Classification | Description |\n"
                "| :--- | :--- | :--- | :--- |\n"
                "| 2026-04-06 | v1.2.3 | Governance | Example row. |\n"
                "</modification_history>\n\n"
                "<schema_governance>\n```yaml\nprimary_owner_skill: core-schema\ndistribution_model: canonical-plus-vendored-mirror\n```\n</schema_governance>\n",
                encoding="utf-8",
            )

            result = subprocess.run(
                [sys.executable, str(temp_scripts_dir / "update_index.py")],
                cwd=root,
                capture_output=True,
                text=True,
            )

            index_path = root / ".agent" / "schemas" / "index.md"
            self.assertEqual(result.returncode, 0)
            self.assertTrue(index_path.exists())
            self.assertIn("| alpha | v1.2.3 | core-schema | Alpha schema purpose. |", index_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

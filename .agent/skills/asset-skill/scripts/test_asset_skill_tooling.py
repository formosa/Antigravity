#!/usr/bin/env python3
"""
Regression tests for asset-skill tooling.

role: unit test suite for skill owner tooling
entrypoints: main
reads: local skill tooling scripts via dynamic import
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: coupled to asset-skill tooling
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
import zipfile
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


INIT_SKILL = load_module("asset_skill_init_skill_test_module", "init_skill.py")
QUICK_VALIDATE = load_module("quick_validate", "quick_validate.py")
SYNC_MIRRORS = load_module("sync_schema_mirrors", "sync_schema_mirrors.py")
PACKAGE_SKILL = load_module("asset_skill_package_skill_test_module", "package_skill.py")


class TestAssetSkillTooling(unittest.TestCase):
    """
    Test suite for the asset-skill owner tooling.
    """

    def test_init_skill_creates_readme_and_schema_mirror(self) -> None:
        """
        Verify skill scaffolding creates the expected durable surfaces.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = INIT_SKILL.init_skill(
                "sample-skill",
                tmpdir,
                resource_dirs={"scripts", "resources"},
                include_examples=True,
            )

            self.assertIsNotNone(skill_dir)
            assert skill_dir is not None
            self.assertTrue((skill_dir / "SKILL.md").exists())
            self.assertTrue((skill_dir / "README.md").exists())
            self.assertTrue((skill_dir / "resources" / "schema" / "skill" / "skill.d.ts").exists())
            self.assertTrue((skill_dir / "scripts" / "example.py").exists())
            self.assertTrue((skill_dir / "resources" / "reference.md").exists())

    def test_validate_skill_rejects_missing_root_readme(self) -> None:
        """
        Verify malformed skill fixtures fail validation.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = INIT_SKILL.init_skill("broken-skill", tmpdir)
            assert skill_dir is not None
            (skill_dir / "README.md").unlink()

            result = QUICK_VALIDATE.validate_skill(skill_dir)

            self.assertFalse(result.valid)
            self.assertTrue(any("README.md not found at skill root." in error for error in result.errors))

    def test_sync_skill_removes_unexpected_schema_dir(self) -> None:
        """
        Verify schema mirror synchronization removes stale schema directories.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = INIT_SKILL.init_skill("synced-skill", tmpdir)
            assert skill_dir is not None
            stale_dir = skill_dir / "resources" / "schema" / "unexpected"
            stale_dir.mkdir(parents=True)
            (stale_dir / "junk.txt").write_text("stale", encoding="utf-8")

            synced_ids = SYNC_MIRRORS.sync_skill(skill_dir)

            self.assertIn("skill", synced_ids)
            self.assertFalse(stale_dir.exists())

    def test_package_skill_excludes_cache_artifacts(self) -> None:
        """
        Verify packaged skills omit cache directories and compiled artifacts.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            skill_dir = INIT_SKILL.init_skill(
                "packaged-skill",
                tmpdir,
                resource_dirs={"scripts"},
                include_examples=True,
            )
            assert skill_dir is not None
            (skill_dir / ".pytest_cache").mkdir()
            (skill_dir / ".pytest_cache" / "state").write_text("cache", encoding="utf-8")
            (skill_dir / "scripts" / "__pycache__").mkdir()
            (skill_dir / "scripts" / "__pycache__" / "junk.pyc").write_bytes(b"compiled")
            (skill_dir / "scripts" / "compiled.pyc").write_bytes(b"compiled")

            output_dir = Path(tmpdir) / "dist"
            package_path = PACKAGE_SKILL.package_skill(skill_dir, output_dir)

            self.assertIsNotNone(package_path)
            assert package_path is not None
            with zipfile.ZipFile(package_path, "r") as archive:
                names = archive.namelist()
            self.assertTrue(all("__pycache__" not in name for name in names))
            self.assertTrue(all(not name.endswith(".pyc") for name in names))


if __name__ == "__main__":
    unittest.main()

"""
Unit tests for managed_temp.py.

role: unit test suite for managed temp helpers
entrypoints: main
reads: managed_temp.py (via dynamic import)
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: coupled to managed_temp.py
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

from datetime import datetime
import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "managed_temp.py"
SPEC = importlib.util.spec_from_file_location("managed_temp_test_module", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["managed_temp_test_module"] = MODULE
SPEC.loader.exec_module(MODULE)


class TestManagedTemp(unittest.TestCase):
    """
    Test suite for managed temp directory helpers.
    """

    def test_create_run_dir_uses_collision_suffix(self) -> None:
        """
        Verify same-second collisions receive a numeric suffix.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            now = datetime(2026, 4, 6, 12, 30, 45)
            first = MODULE.create_run_dir("rebuild-docs", temp_root=tmpdir, now=now)
            second = MODULE.create_run_dir("rebuild-docs", temp_root=tmpdir, now=now)

            self.assertEqual(first.name, "20260406-123045-rebuild-docs")
            self.assertEqual(second.name, "20260406-123045-rebuild-docs-01")

    def test_retain_failure_writes_marker_and_cleanup_removes_run_dir(self) -> None:
        """
        Verify failure retention markers and success cleanup stay within the temp root.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = MODULE.create_run_dir("test-task", temp_root=tmpdir)
            marker = MODULE.retain_failure(run_dir, "intentional failure", temp_root=tmpdir)

            self.assertTrue(marker.exists())
            self.assertEqual(marker.read_text(encoding="utf-8").strip(), "intentional failure")

            MODULE.cleanup_run_dir(run_dir, temp_root=tmpdir)
            self.assertFalse(run_dir.exists())


if __name__ == "__main__":
    unittest.main()

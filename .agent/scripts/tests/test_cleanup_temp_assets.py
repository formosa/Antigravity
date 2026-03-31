#!/usr/bin/env python3
"""Unit tests for cleanup_temp_assets.py."""

from __future__ import annotations

import importlib.util
import os
import sys
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "cleanup_temp_assets.py"
SPEC = importlib.util.spec_from_file_location("cleanup_temp_assets", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["cleanup_temp_assets"] = MODULE
SPEC.loader.exec_module(MODULE)

AuditReport = MODULE.AuditReport
RunDirectory = MODULE.RunDirectory
RETAINED_MARKER_NAME = MODULE.RETAINED_MARKER_NAME
classify_directories = MODULE.classify_directories
delete_run_directories = MODULE.delete_run_directories


def age_path(path: Path, *, days: int) -> None:
    timestamp = (datetime.now(timezone.utc) - timedelta(days=days)).timestamp()
    os.utime(path, (timestamp, timestamp))


class TestCleanupTempAssets(unittest.TestCase):
    def test_classify_directories_groups_expected_run_dirs(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)

            empty_dir = root / "20260331-103500-deadbeef-empty-run"
            empty_dir.mkdir()

            retained_dir = root / "20260330-113000-abcdef12-failed-run"
            retained_dir.mkdir()
            (retained_dir / RETAINED_MARKER_NAME).write_text(
                "Schema mismatch retained for debugging.",
                encoding="utf-8",
            )

            stale_dir = root / "20260321-101500-feedface-stale-run"
            stale_dir.mkdir()
            (stale_dir / "debug.log").write_text("stale", encoding="utf-8")
            age_path(stale_dir, days=10)

            active_dir = root / "20260331-114500-ba5eba11-active-run"
            active_dir.mkdir()
            (active_dir / "script.py").write_text("print('ok')", encoding="utf-8")

            invalid_dir = root / "rebuild-docs"
            invalid_dir.mkdir()

            report: AuditReport = classify_directories(root, stale_days=7)

            self.assertEqual([entry.path.name for entry in report.empty_run_dirs], [empty_dir.name])
            self.assertEqual(
                [entry.path.name for entry in report.retained_failure_dirs],
                [retained_dir.name],
            )
            self.assertEqual([entry.path.name for entry in report.stale_run_dirs], [stale_dir.name])
            self.assertEqual([entry.path.name for entry in report.active_run_dirs], [active_dir.name])
            self.assertEqual([entry.path.name for entry in report.invalid_dirs], [invalid_dir.name])

    def test_delete_run_directories_removes_valid_descendants(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            run_dir = root / "20260331-103500-deadbeef-empty-run"
            run_dir.mkdir()
            report = classify_directories(root)

            deleted = delete_run_directories(report.empty_run_dirs, root)

            self.assertEqual(deleted, [run_dir])
            self.assertFalse(run_dir.exists())

    def test_delete_run_directories_rejects_outside_paths(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir, tempfile.TemporaryDirectory() as other_tmpdir:
            root = Path(tmpdir)
            outside = Path(other_tmpdir)

            outside_run = RunDirectory(
                path=outside,
                age_days=0,
                modified_at=datetime.now(timezone.utc),
                is_empty=True,
                is_retained_failure=False,
                retention_reason=None,
                is_valid_name=True,
            )

            with self.assertRaises(ValueError):
                delete_run_directories([outside_run], root)


if __name__ == "__main__":
    unittest.main()

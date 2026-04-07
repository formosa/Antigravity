"""
Unit tests for rebuild_docs.py.

role: unit test suite for docs rebuild workflow
entrypoints: main
reads: rebuild_docs.py (via dynamic import)
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: coupled to rebuild_docs.py
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock


SCRIPTS_DIR = Path(__file__).resolve().parents[1]
MANAGED_TEMP_PATH = SCRIPTS_DIR / "managed_temp.py"
MANAGED_TEMP_SPEC = importlib.util.spec_from_file_location("managed_temp", MANAGED_TEMP_PATH)
MANAGED_TEMP_MODULE = importlib.util.module_from_spec(MANAGED_TEMP_SPEC)
sys.modules["managed_temp"] = MANAGED_TEMP_MODULE
MANAGED_TEMP_SPEC.loader.exec_module(MANAGED_TEMP_MODULE)

SCRIPT_PATH = SCRIPTS_DIR / "rebuild_docs.py"
SPEC = importlib.util.spec_from_file_location("rebuild_docs_test_module", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
sys.modules["rebuild_docs_test_module"] = MODULE
SPEC.loader.exec_module(MODULE)


class TestRebuildDocs(unittest.TestCase):
    """
    Test suite for rebuild docs workflow behavior.
    """

    def _make_repo_root(self, tmpdir: str) -> Path:
        root = Path(tmpdir)
        (root / "docs").mkdir(parents=True)
        return root

    def test_run_rebuild_cleans_managed_temp_on_success(self) -> None:
        """
        Verify successful rebuilds validate outputs and remove temp logs.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_repo_root(tmpdir)
            temp_root = root / ".agent" / ".temp"

            def fake_run(_root: Path, _python: str, spec: MODULE.BuildSpec):
                spec.log_path.parent.mkdir(parents=True, exist_ok=True)
                spec.log_path.write_text("WARNING: sample\n", encoding="utf-8")
                spec.output_dir.mkdir(parents=True, exist_ok=True)
                if spec.builder == "needs":
                    (spec.output_dir / "needs.json").write_text('{"ok": true}', encoding="utf-8")
                else:
                    (spec.output_dir / "index.html").write_text("<html></html>", encoding="utf-8")
                return MODULE.subprocess.CompletedProcess(args=["sphinx"], returncode=0, stdout="", stderr="")

            with mock.patch.object(MODULE, "run_sphinx_build", side_effect=fake_run):
                exit_code = MODULE.run_rebuild(root, python_executable="python", temp_root=temp_root)

            self.assertEqual(exit_code, 0)
            self.assertTrue((root / "docs" / "_build" / "json" / "needs.json").exists())
            self.assertTrue((root / "docs" / "_build" / "html" / "index.html").exists())
            self.assertEqual(list(temp_root.glob("*")), [])

    def test_run_rebuild_retains_failure_logs_with_marker(self) -> None:
        """
        Verify failed builds retain the temp run directory with a marker file.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            root = self._make_repo_root(tmpdir)
            temp_root = root / ".agent" / ".temp"

            def fake_run(_root: Path, _python: str, spec: MODULE.BuildSpec):
                spec.log_path.parent.mkdir(parents=True, exist_ok=True)
                spec.log_path.write_text("WARNING: broken\n", encoding="utf-8")
                return MODULE.subprocess.CompletedProcess(
                    args=["sphinx"],
                    returncode=1,
                    stdout="build failed",
                    stderr="traceback",
                )

            with mock.patch.object(MODULE, "run_sphinx_build", side_effect=fake_run):
                exit_code = MODULE.run_rebuild(root, python_executable="python", temp_root=temp_root)

            self.assertEqual(exit_code, 1)
            run_dirs = list(temp_root.glob("*"))
            self.assertEqual(len(run_dirs), 1)
            marker = run_dirs[0] / MODULE.RETAINED_MARKER_NAME
            self.assertTrue(marker.exists())
            self.assertIn("Sphinx needs build failed", marker.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()

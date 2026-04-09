#!/usr/bin/env python3
"""
Regression tests for runtime-target loading and config-mode validation.

role: unit test suite for shared runtime-target tooling
entrypoints: main
reads: local runtime-target scripts and settings fixtures
writes: nothing durable (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: coupled to runtime-target and validate_env helpers
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

import importlib.util
import sys
import tempfile
import textwrap
import unittest
from pathlib import Path


SCRIPT_TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_TESTS_DIR.parent


def load_module(module_name: str, path: Path):
    """
    Load a script path as an importable module for testing.
    """
    spec = importlib.util.spec_from_file_location(module_name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


RUNTIME_TARGET = load_module("runtime_target_test_module", SCRIPTS_DIR / "runtime_target.py")
VALIDATE_ENV = load_module("validate_env_test_module", SCRIPT_TESTS_DIR / "validate_env.py")


class TestRuntimeTarget(unittest.TestCase):
    """
    Test suite for runtime-target manifest loading and config-mode validation.
    """

    def test_load_runtime_target_from_repo_manifest(self) -> None:
        """
        Verify the checked-in runtime-target manifest loads with the expected fields.
        """
        root = RUNTIME_TARGET.repo_root(__file__)
        manifest = RUNTIME_TARGET.load_runtime_target(root)

        self.assertEqual(manifest["target_platform"]["version"], "1.21.9")
        self.assertIn("gemini-3-pro-preview", manifest["approved_models"])
        self.assertEqual(manifest["rules_surfaces"]["local_workspace"], ".agent/rules/")

    def test_validate_runtime_target_rejects_missing_required_keys(self) -> None:
        """
        Verify malformed manifests fail with a useful contract error.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            manifest_path = Path(tmpdir) / "runtime-target.yaml"
            manifest_path.write_text("target_platform: {}\n", encoding="utf-8")

            with self.assertRaises(RUNTIME_TARGET.RuntimeTargetError):
                RUNTIME_TARGET.load_runtime_target(path=manifest_path)

    def test_collect_config_findings_accepts_valid_repo_shape(self) -> None:
        """
        Verify config-mode validation passes for a manifest-aligned temp repo.
        """
        with tempfile.TemporaryDirectory() as tmpdir:
            root = Path(tmpdir)
            (root / ".agent" / "config").mkdir(parents=True, exist_ok=True)
            (root / ".vscode").mkdir(parents=True, exist_ok=True)
            (root / ".venv" / "Scripts").mkdir(parents=True, exist_ok=True)
            (root / ".venv" / "Scripts" / "python.exe").write_text("", encoding="utf-8")

            manifest_text = (RUNTIME_TARGET.runtime_target_path(RUNTIME_TARGET.repo_root(__file__))).read_text(
                encoding="utf-8"
            )
            (root / ".agent" / "config" / "runtime-target.yaml").write_text(manifest_text, encoding="utf-8")

            settings_text = textwrap.dedent(
                """\
                {
                  "workbench.editorAssociations": {
                    "**/.agent/rules/**/*.md": "default",
                    "**/.agent/skills/**/*.md": "default",
                    "**/.agent/tools/**/*.md": "default",
                    "**/.agent/workflows/**/*.md": "default"
                  },
                  "terminal.integrated.defaultProfile.windows": "PowerShell 7",
                  "terminal.integrated.profiles.windows": {
                    "PowerShell 7": {
                      "path": "C:\\\\Program Files\\\\PowerShell\\\\7\\\\pwsh.exe",
                      "args": ["-NoLogo"]
                    }
                  },
                  "terminal.integrated.env.windows": {
                    "PYTHONUTF8": "1",
                    "PYTHONIOENCODING": "utf-8"
                  },
                  "python.defaultInterpreterPath": "${workspaceFolder}\\\\.venv\\\\Scripts\\\\python.exe"
                }
                """
            )
            (root / ".vscode" / "settings.json").write_text(settings_text, encoding="utf-8")
            (root / "Antigravity.code-workspace").write_text(
                textwrap.dedent(
                    """\
                    {
                      "folders": [{"path": "."}],
                      "settings": {
                        "workbench.editorAssociations": {
                          "**/.agent/rules/**/*.md": "default",
                          "**/.agent/skills/**/*.md": "default",
                          "**/.agent/tools/**/*.md": "default",
                          "**/.agent/workflows/**/*.md": "default"
                        },
                        "terminal.integrated.defaultProfile.windows": "PowerShell 7",
                        "terminal.integrated.profiles.windows": {
                          "PowerShell 7": {
                            "path": "C:\\\\Program Files\\\\PowerShell\\\\7\\\\pwsh.exe",
                            "args": ["-NoLogo"]
                          }
                        },
                        "terminal.integrated.env.windows": {
                          "PYTHONUTF8": "1",
                          "PYTHONIOENCODING": "utf-8"
                        },
                        "python.defaultInterpreterPath": "${workspaceFolder}\\\\.venv\\\\Scripts\\\\python.exe"
                      }
                    }
                    """
                ),
                encoding="utf-8",
            )

            manifest = RUNTIME_TARGET.load_runtime_target(root)
            failures, warnings = VALIDATE_ENV.collect_config_findings(root, manifest)

            self.assertEqual(failures, [])
            self.assertEqual(warnings, [])


if __name__ == "__main__":
    unittest.main()

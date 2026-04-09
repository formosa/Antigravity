"""
Validation gate for the Antigravity PowerShell execution baseline.

Supports two modes:
- `--config`: deterministic validation of repo-controlled settings against
  `.agent/config/runtime-target.yaml`
- `--runtime`: live-shell validation of the current interpreter, UTF-8 mode,
  PowerShell availability, and optional `rg` launchability

role: environment validation diagnostic
entrypoints: main
reads: repo settings files, os.environ, sys.flags, subprocess output
writes: stdout
external_io: fs, subprocess (pwsh, rg)
state_model: stateless
failure_surface: missing pwsh; encoding mismatches; repo configuration drift
coupling: coupled to runtime-target manifest and Windows execution settings
determinism: config mode deterministic; runtime mode external-state-dependent
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import argparse
import json
import os
import platform
import re
import subprocess
import sys
from pathlib import Path


SCRIPT_TESTS_DIR = Path(__file__).resolve().parent
SCRIPTS_DIR = SCRIPT_TESTS_DIR.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from runtime_target import load_runtime_target, repo_root, workspace_python_path


REQUIRED_EDITOR_ASSOCIATIONS = {
    "**/.agent/rules/**/*.md": "default",
    "**/.agent/skills/**/*.md": "default",
    "**/.agent/tools/**/*.md": "default",
    "**/.agent/workflows/**/*.md": "default",
}


def print_status(check_name: str, passed: bool, details: str = "") -> bool:
    """
    Output a pass or fail line for a validation check.

    purpose: diagnostic reporting
    """
    status = "[PASS]" if passed else "[FAIL]"
    print(f"{status} {check_name:<45} {details}")
    return passed


def print_warning(check_name: str, details: str = "") -> None:
    """
    Output a warning line for a non-fatal validation check.

    purpose: diagnostic reporting
    """
    print(f"[WARN] {check_name:<45} {details}")


def strip_jsonc_comments(content: str) -> str:
    """
    Remove line comments from simple JSONC files.

    purpose: JSONC normalization
    """
    return re.sub(r"(?m)^\s*//.*$", "", content)


def load_jsonc(path: Path) -> dict:
    """
    Parse a repo-controlled JSONC file into a mapping.

    purpose: settings loading
    """
    parsed = json.loads(strip_jsonc_comments(path.read_text(encoding="utf-8")))
    if not isinstance(parsed, dict):
        raise ValueError(f"JSONC root must be an object: {path}")
    return parsed


def load_repo_settings(root: Path) -> tuple[dict, dict]:
    """
    Load the VS Code settings and workspace settings documents.

    purpose: deterministic settings loading
    """
    vscode_settings = load_jsonc(root / ".vscode" / "settings.json")
    workspace_document = load_jsonc(root / "Antigravity.code-workspace")
    workspace_settings = workspace_document.get("settings", {})
    if not isinstance(workspace_settings, dict):
        raise ValueError("Antigravity.code-workspace must contain a `settings` mapping.")
    return vscode_settings, workspace_settings


def collect_config_findings(root: Path, target: dict | None = None) -> tuple[list[str], list[str]]:
    """
    Validate repo-controlled settings against the runtime-target manifest.

    purpose: deterministic config auditing
    """
    manifest = target or load_runtime_target(root)
    vscode_settings, workspace_settings = load_repo_settings(root)
    failures: list[str] = []
    warnings: list[str] = []

    preferred_shell = manifest["windows_execution"]["preferred_shell"]
    preferred_python = manifest["windows_execution"]["preferred_python"]
    utf8_env = manifest["windows_execution"]["utf8_env"]
    expected_interpreter_setting = preferred_python["workspace_setting"]
    expected_interpreter_path = workspace_python_path(root, manifest)

    def require_setting(settings: dict, label: str, key: str, expected: object) -> None:
        actual = settings.get(key)
        if actual != expected:
            failures.append(f"{label} must set `{key}` to `{expected}` (current: `{actual}`).")

    def require_mapping_value(settings: dict, label: str, key: str, nested_key: str, expected: object) -> None:
        mapping = settings.get(key)
        if not isinstance(mapping, dict):
            failures.append(f"{label} must define `{key}` as an object.")
            return
        actual = mapping.get(nested_key)
        if actual != expected:
            failures.append(
                f"{label} must set `{key}.{nested_key}` to `{expected}` (current: `{actual}`)."
            )

    require_setting(
        vscode_settings,
        ".vscode/settings.json",
        "terminal.integrated.defaultProfile.windows",
        preferred_shell["profile_name"],
    )
    require_setting(
        workspace_settings,
        "Antigravity.code-workspace",
        "terminal.integrated.defaultProfile.windows",
        preferred_shell["profile_name"],
    )
    require_setting(
        vscode_settings,
        ".vscode/settings.json",
        "python.defaultInterpreterPath",
        expected_interpreter_setting,
    )
    require_setting(
        workspace_settings,
        "Antigravity.code-workspace",
        "python.defaultInterpreterPath",
        expected_interpreter_setting,
    )
    require_mapping_value(
        vscode_settings,
        ".vscode/settings.json",
        "terminal.integrated.profiles.windows",
        preferred_shell["profile_name"],
        {
            "path": preferred_shell["executable"].replace("/", "\\"),
            "args": ["-NoLogo"],
        },
    )
    require_mapping_value(
        workspace_settings,
        "Antigravity.code-workspace",
        "terminal.integrated.profiles.windows",
        preferred_shell["profile_name"],
        {
            "path": preferred_shell["executable"].replace("/", "\\"),
            "args": ["-NoLogo"],
        },
    )

    for settings_label, settings in (
        (".vscode/settings.json", vscode_settings),
        ("Antigravity.code-workspace", workspace_settings),
    ):
        env_settings = settings.get("terminal.integrated.env.windows")
        if not isinstance(env_settings, dict):
            failures.append(f"{settings_label} must define `terminal.integrated.env.windows`.")
        else:
            for key, expected_value in utf8_env.items():
                actual_value = env_settings.get(key)
                if actual_value != expected_value:
                    failures.append(
                        f"{settings_label} must set `terminal.integrated.env.windows.{key}` to "
                        f"`{expected_value}` (current: `{actual_value}`)."
                    )

        editor_associations = settings.get("workbench.editorAssociations")
        if not isinstance(editor_associations, dict):
            failures.append(f"{settings_label} must define `workbench.editorAssociations`.")
        else:
            for key, expected_value in REQUIRED_EDITOR_ASSOCIATIONS.items():
                actual_value = editor_associations.get(key)
                if actual_value != expected_value:
                    failures.append(
                        f"{settings_label} must set `workbench.editorAssociations.{key}` to "
                        f"`{expected_value}` (current: `{actual_value}`)."
                    )

    if not expected_interpreter_path.exists():
        failures.append(f"Preferred workspace interpreter is missing: {expected_interpreter_path}")

    manifest_local_rules = manifest["rules_surfaces"]["local_workspace"]
    if manifest_local_rules != ".agent/rules/":
        warnings.append(
            "Config-mode validation currently expects `.agent/rules/` as the local rules surface."
        )

    return failures, warnings


def print_config_validation(root: Path, target: dict | None = None) -> int:
    """
    Execute deterministic repository configuration validation.

    purpose: config-mode reporting
    """
    manifest = target or load_runtime_target(root)
    print("=" * 75)
    print(" Antigravity - Repository Configuration Validation")
    print(f" Platform target : {manifest['target_platform']['product']} {manifest['target_platform']['version']}")
    print(f" Manifest path   : {root / '.agent' / 'config' / 'runtime-target.yaml'}")
    print("=" * 75)

    failures, warnings = collect_config_findings(root, manifest)
    passed = not failures
    print_status("Repo Config: runtime-target aligned", passed, f"({len(failures)} failure(s))")
    for warning in warnings:
        print_warning("Repo Config: advisory", warning)
    for failure in failures:
        print(f"  - {failure}")

    print("=" * 75)
    if passed:
        print(" [OK] Repository configuration validated.\n")
        return 0

    print(f" [ERR] {len(failures)} repository configuration failure(s) detected.\n")
    return 1


def print_runtime_validation(root: Path, target: dict | None = None) -> int:
    """
    Execute live-shell runtime validation checks.

    purpose: runtime-mode reporting
    """
    manifest = target or load_runtime_target(root)
    expected_interpreter = workspace_python_path(root, manifest).resolve()
    expected_utf8_env = manifest["windows_execution"]["utf8_env"]

    print("=" * 75)
    print(" Antigravity - PowerShell Execution Validation")
    print(f" Platform : {platform.system()} {platform.release()}")
    print(f" Runtime  : Python {sys.version.split()[0]}")
    print("=" * 75)

    failures = 0

    env_utf8 = os.environ.get("PYTHONUTF8") == expected_utf8_env["PYTHONUTF8"]
    if not print_status(
        "IDE Boundary: PYTHONUTF8=1",
        env_utf8,
        f"(Current: '{os.environ.get('PYTHONUTF8')}')",
    ):
        failures += 1

    env_io = str(os.environ.get("PYTHONIOENCODING")).lower() in ["utf-8", "utf8"]
    if not print_status(
        "IDE Boundary: PYTHONIOENCODING=utf-8",
        env_io,
        f"(Current: '{os.environ.get('PYTHONIOENCODING')}')",
    ):
        failures += 1

    utf8_mode = getattr(sys.flags, "utf8_mode", 0) == 1
    if not print_status("Python Runtime: sys.flags.utf8_mode active", utf8_mode):
        failures += 1

    stdout_encoding = (sys.stdout.encoding or "").lower()
    stdout_enc = stdout_encoding in ["utf-8", "utf-8-sig"]
    if not print_status(
        "Python Runtime: sys.stdout is UTF-8",
        stdout_enc,
        f"(Current: '{sys.stdout.encoding}')",
    ):
        failures += 1

    current_executable = Path(sys.executable).resolve()
    interpreter_ok = current_executable == expected_interpreter
    if not print_status(
        "Python Runtime: workspace interpreter active",
        interpreter_ok,
        f"(Current: '{current_executable}')",
    ):
        failures += 1

    try:
        ps_version_check = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", "$PSVersionTable.PSVersion.Major"],
            capture_output=True,
            text=True,
            check=True,
        )
        ps_version = int(ps_version_check.stdout.strip())
        ps_pass = ps_version >= 7
        if not print_status(
            "Shell Baseline: PowerShell >= 7 (pwsh)",
            ps_pass,
            f"(Detected: v{ps_version})",
        ):
            failures += 1
    except (FileNotFoundError, ValueError, subprocess.CalledProcessError):
        print_status(
            "Shell Baseline: PowerShell >= 7 (pwsh)",
            False,
            "(pwsh not found or execution failed)",
        )
        failures += 1

    test_glyph = "Architectural Validation: warning x check bullet"
    try:
        glyph_check = subprocess.run(
            ["pwsh", "-Command", f"Write-Output '{test_glyph}'"],
            capture_output=True,
            encoding="utf-8",
            errors="strict",
            check=True,
        )
        glyph_pass = test_glyph in glyph_check.stdout
        if not print_status(
            "Pipeline Encoding: Subprocess Round-Trip",
            glyph_pass,
            "(Data intact)",
        ):
            failures += 1
    except Exception as exc:  # pragma: no cover - diagnostic path
        print_status(
            "Pipeline Encoding: Subprocess Round-Trip",
            False,
            f"({type(exc).__name__})",
        )
        failures += 1

    try:
        rg_check = subprocess.run(
            ["pwsh", "-NoProfile", "-Command", "rg --version"],
            capture_output=True,
            text=True,
            check=True,
        )
        first_line = (rg_check.stdout or "").splitlines()[0] if rg_check.stdout else ""
        print_status("Optional Tooling: rg launchability", True, first_line)
    except Exception as exc:  # pragma: no cover - diagnostic path
        print_warning(
            "Optional Tooling: rg launchability",
            f"({type(exc).__name__}) fallback to Get-ChildItem + Select-String",
        )

    print("=" * 75)
    if failures == 0:
        print(" [OK] Core PowerShell execution baseline validated.\n")
        return 0

    print(f" [ERR] {failures} core validation failure(s) detected.\n")
    return 1


def parse_args() -> argparse.Namespace:
    """
    Parse the command-line mode flags.

    purpose: CLI configuration extraction
    """
    parser = argparse.ArgumentParser(description="Validate Antigravity repo config or live runtime state.")
    mode_group = parser.add_mutually_exclusive_group(required=True)
    mode_group.add_argument("--config", action="store_true", help="Validate repo-controlled settings.")
    mode_group.add_argument("--runtime", action="store_true", help="Validate the current live shell runtime.")
    return parser.parse_args()


def main() -> None:
    """
    Dispatch validation based on the selected mode.

    purpose: entrypoint
    """
    args = parse_args()
    root = repo_root(__file__)
    target = load_runtime_target(root)

    if args.config:
        sys.exit(print_config_validation(root, target))

    sys.exit(print_runtime_validation(root, target))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Validate a canonical schema `.d.ts` file and selected compatibility text surfaces.

role: core schema validator
entrypoints: main
reads: core schema files, config.json, runtime-target manifest
writes: stdout, backup file
external_io: fs, tsc subprocess
state_model: stateless
failure_surface: fs access errors; tsc missing; validation failure
coupling: coupled to TypeScript compiler, runtime-target manifest, and schema structure
determinism: input-dependent
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import shutil
import subprocess
import sys
from pathlib import Path
import re


REPO_ROOT = Path(__file__).resolve().parents[4]
SCRIPTS_DIR = REPO_ROOT / ".agent" / "scripts"
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from runtime_target import load_runtime_target


@dataclass(frozen=True)
class CompatibilityRule:
    """
    Represent compatibility expectations for one schema-adjacent file.
    """

    relative_path: str
    required_tokens: tuple[str, ...] = ()
    forbidden_tokens: tuple[str, ...] = ()
    strip_modification_history: bool = False


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments.

    purpose: CLI configuration extraction
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    return parser.parse_args()


def load_config() -> tuple[Path, bool]:
    """
    Load the core-schema config and resolve the schema root.

    purpose: config loading
    """
    config_path = Path(__file__).parent.parent / "config.json"
    schemas_dir = REPO_ROOT / ".agent" / "schemas"
    do_validation = True
    if config_path.exists():
        cfg = json.loads(config_path.read_text(encoding="utf-8"))
        rel = cfg.get("default_schema_location")
        if rel:
            schemas_dir = (REPO_ROOT / rel).resolve()
        do_validation = cfg.get("enable_auto_validation", True)
    return schemas_dir, do_validation


def strip_modification_history(content: str) -> str:
    """
    Remove the modification history block before compatibility scanning.

    purpose: false-positive reduction
    """
    return re.sub(
        r"(?ms)<modification_history>\s*.*?\s*</modification_history>",
        "",
        content,
    )


def build_compatibility_rules(schema_name: str, runtime_target: dict) -> list[CompatibilityRule]:
    """
    Build schema-specific compatibility text rules from the runtime-target manifest.

    purpose: compatibility rule derivation
    """
    runtime_version = runtime_target["target_platform"]["version"]
    local_rules = runtime_target["rules_surfaces"]["local_workspace"]
    optional_global = runtime_target["rules_surfaces"]["optional_global"]
    planner_model, executor_model = runtime_target["approved_models"]
    deprecated_models = tuple(runtime_target["deprecated_models"])

    schema_rules: dict[str, list[CompatibilityRule]] = {
        "gemini": [
            CompatibilityRule(
                "gemini.d.ts",
                required_tokens=(f"v{runtime_version}", planner_model, executor_model),
                forbidden_tokens=deprecated_models + ("AGENTS.md",),
            ),
            CompatibilityRule(
                "README.md",
                required_tokens=(f"v{runtime_version}", local_rules, optional_global, planner_model, executor_model),
                forbidden_tokens=deprecated_models + ("AGENTS.md",),
                strip_modification_history=True,
            ),
            CompatibilityRule(
                "example.md",
                required_tokens=(planner_model, executor_model, local_rules, optional_global),
                forbidden_tokens=deprecated_models + ("AGENTS.md",),
            ),
        ],
        "implementation-plan": [
            CompatibilityRule(
                "implementation-plan.d.ts",
                required_tokens=(f"v{runtime_version}", planner_model, executor_model),
                forbidden_tokens=deprecated_models,
            ),
            CompatibilityRule(
                "README.md",
                required_tokens=(f"v{runtime_version}", local_rules, optional_global, planner_model, executor_model),
                forbidden_tokens=deprecated_models + ("AGENTS.md",),
                strip_modification_history=True,
            ),
            CompatibilityRule(
                "example.md",
                required_tokens=(planner_model, executor_model),
                forbidden_tokens=deprecated_models,
            ),
        ],
        "security-policy": [
            CompatibilityRule("security-policy.d.ts", required_tokens=(f"v{runtime_version}",)),
            CompatibilityRule(
                "README.md",
                required_tokens=(f"v{runtime_version}",),
                strip_modification_history=True,
            ),
        ],
        "task": [
            CompatibilityRule(
                "task.d.ts",
                required_tokens=(f"v{runtime_version}", planner_model, executor_model),
                forbidden_tokens=deprecated_models,
            ),
            CompatibilityRule(
                "README.md",
                required_tokens=(f"v{runtime_version}", planner_model, executor_model),
                strip_modification_history=True,
            ),
            CompatibilityRule(
                "example.md",
                required_tokens=(executor_model,),
                forbidden_tokens=deprecated_models,
            ),
        ],
        "walkthrough": [
            CompatibilityRule("walkthrough.d.ts", required_tokens=(f"v{runtime_version}",)),
            CompatibilityRule(
                "README.md",
                required_tokens=(f"v{runtime_version}",),
                forbidden_tokens=("Wikipedia",),
                strip_modification_history=True,
            ),
        ],
        "schema": [
            CompatibilityRule("schema.d.ts", required_tokens=(f"v{runtime_version}",)),
            CompatibilityRule(
                "example.md",
                required_tokens=(
                    f"Google Antigravity {runtime_version}",
                    optional_global,
                    "Gemini 3 Pro Preview",
                ),
                forbidden_tokens=(">=1.18", ".antigravity/rules.md", "Gemini 3.1 Pro"),
            ),
        ],
        "issues-tracker": [
            CompatibilityRule(
                "template.md",
                required_tokens=(f"Google Antigravity {runtime_version}", "Gemini 3 Pro Preview"),
                forbidden_tokens=(">=1.18", "Gemini 3.1 Pro"),
            ),
            CompatibilityRule(
                "example.md",
                required_tokens=(f"Google Antigravity {runtime_version}", "Gemini 3 Pro Preview"),
                forbidden_tokens=(">=1.18", "Gemini 3.1 Pro"),
            ),
            CompatibilityRule(
                "example-it-1.1.md",
                required_tokens=(f"Google Antigravity {runtime_version}", "Gemini 3 Pro Preview"),
                forbidden_tokens=(">=1.18", "Gemini 3.1 Pro"),
            ),
        ],
    }
    return schema_rules.get(schema_name, [])


def validate_compatibility_text(target_dir: Path, schema_name: str, runtime_target: dict) -> list[str]:
    """
    Validate schema-adjacent compatibility text against runtime-target expectations.

    purpose: compatibility drift detection
    """
    failures: list[str] = []
    for rule in build_compatibility_rules(schema_name, runtime_target):
        file_path = target_dir / rule.relative_path
        if not file_path.exists():
            failures.append(f"Missing compatibility surface: {file_path}")
            continue

        content = file_path.read_text(encoding="utf-8")
        if rule.strip_modification_history:
            content = strip_modification_history(content)

        for token in rule.required_tokens:
            if token not in content:
                failures.append(f"`{file_path}` is missing required compatibility token: `{token}`")
        for token in rule.forbidden_tokens:
            if token and contains_forbidden_token(content, token):
                failures.append(f"`{file_path}` still contains stale compatibility token: `{token}`")
    return failures


def contains_forbidden_token(content: str, token: str) -> bool:
    """
    Detect stale compatibility tokens without false positives on preview suffixes.

    purpose: token matching
    """
    if token.startswith("gemini-"):
        pattern = re.escape(token)
        if token.endswith("-flash") or token.endswith("-pro"):
            return re.search(rf"(?<![A-Za-z0-9.-]){pattern}(?!-preview\b)", content) is not None
        return re.search(rf"(?<![A-Za-z0-9.-]){pattern}(?![A-Za-z0-9.-])", content) is not None
    return token in content


def resolve_tsc_command(project_root: Path) -> str:
    """
    Resolve the preferred TypeScript compiler command.

    purpose: tool path resolution
    """
    tsc_cmd = project_root / ".nodeenv" / "Scripts" / "tsc.cmd"
    return str(tsc_cmd) if tsc_cmd.exists() else "tsc"


def main() -> None:
    """
    Execute the core schema validation logic.

    purpose: entrypoint
    """
    args = parse_args()
    schemas_dir, do_validation = load_config()
    runtime_target = load_runtime_target(REPO_ROOT)

    target_dir = schemas_dir / args.name
    dts_path = target_dir / f"{args.name}.d.ts"
    backup_path = target_dir / f"{args.name}.d.ts.bak"

    if not dts_path.exists():
        print(f"[ERROR] Schema .d.ts not found at {dts_path}")
        sys.exit(1)

    if not do_validation:
        print("[OK] Auto-validation disabled.")
        sys.exit(0)

    print(f"Validating {dts_path}...")
    result = subprocess.run(
        [resolve_tsc_command(REPO_ROOT), "--noEmit", str(dts_path)],
        capture_output=True,
        text=True,
    )

    if result.returncode != 0:
        print("[ERROR] Validation failed. Outputting errors:")
        print(result.stderr or result.stdout)
        if backup_path.exists():
            print(f"[WARN] Rolling back {dts_path} to previous state...")
            shutil.copy(backup_path, dts_path)
        else:
            print("[WARN] No backup found (initial creation). File remains unchanged for manual correction.")
        sys.exit(1)

    compatibility_failures = validate_compatibility_text(target_dir, args.name, runtime_target)
    if compatibility_failures:
        print("[ERROR] Compatibility text validation failed:")
        for failure in compatibility_failures:
            print(f"- {failure}")
        sys.exit(1)

    print(f"[OK] Schema {args.name} validated successfully.")
    shutil.copy(dts_path, backup_path)


if __name__ == "__main__":
    main()

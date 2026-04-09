#!/usr/bin/env python3
"""
Shared loader and validator for the repository runtime target manifest.

role: runtime target manifest loader
entrypoints: none
reads: .agent/config/runtime-target.yaml
writes: none
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors; manifest contract violations
coupling: coupled to runtime-target manifest structure
determinism: deterministic
concurrency: thread-safe; process-local
"""

from __future__ import annotations

from pathlib import Path

import yaml


class RuntimeTargetError(ValueError):
    """
    Raised when the runtime-target manifest is missing or malformed.
    """


REQUIRED_TOP_LEVEL_KEYS = {
    "target_platform",
    "rules_surfaces",
    "approved_models",
    "deprecated_models",
    "windows_execution",
    "search_policy",
}

REQUIRED_NESTED_KEYS = {
    ("target_platform",): {"product", "version", "evidence_date", "source_urls"},
    ("rules_surfaces",): {"local_workspace", "optional_global"},
    ("windows_execution",): {"preferred_shell", "preferred_python", "utf8_env"},
    ("windows_execution", "preferred_shell"): {"profile_name", "executable"},
    ("windows_execution", "preferred_python"): {
        "relative_path",
        "workspace_setting",
        "prefer_explicit_path_invocation",
        "forbid_naked_python_when_workspace_interpreter_known",
    },
    ("windows_execution", "utf8_env"): {"PYTHONUTF8", "PYTHONIOENCODING"},
    ("search_policy",): {"preferred_tool", "rg_required", "first_failure_fallback"},
}


def repo_root(anchor: str | Path | None = None) -> Path:
    """
    Resolve the repository root by walking upward until `.agent/` is found.

    purpose: path resolution
    """
    start = Path(anchor).resolve() if anchor is not None else Path(__file__).resolve()
    if start.is_file():
        start = start.parent

    for candidate in [start, *start.parents]:
        if (candidate / ".agent").exists():
            return candidate

    raise RuntimeTargetError("Unable to resolve repository root from the provided anchor.")


def runtime_target_path(root: str | Path | None = None) -> Path:
    """
    Return the absolute path to the runtime-target manifest.

    purpose: manifest path resolution
    """
    return repo_root(root) / ".agent" / "config" / "runtime-target.yaml"


def _require_mapping(value: object, label: str) -> dict:
    """
    Ensure a manifest node is a mapping.

    purpose: structure validation
    """
    if not isinstance(value, dict):
        raise RuntimeTargetError(f"`{label}` must be a mapping.")
    return value


def _require_non_empty_string(value: object, label: str) -> None:
    """
    Ensure a manifest leaf is a non-empty string.

    purpose: scalar validation
    """
    if not isinstance(value, str) or not value.strip():
        raise RuntimeTargetError(f"`{label}` must be a non-empty string.")


def _require_string_list(value: object, label: str) -> None:
    """
    Ensure a manifest leaf is a non-empty list of strings.

    purpose: list validation
    """
    if not isinstance(value, list) or not value or not all(isinstance(item, str) and item.strip() for item in value):
        raise RuntimeTargetError(f"`{label}` must be a non-empty list of strings.")


def validate_runtime_target(data: object) -> dict:
    """
    Validate the manifest structure and return it as a mapping.

    purpose: manifest contract validation
    """
    root_mapping = _require_mapping(data, "runtime-target")
    missing_keys = REQUIRED_TOP_LEVEL_KEYS - set(root_mapping.keys())
    if missing_keys:
        raise RuntimeTargetError(
            "runtime-target manifest is missing required keys: " + ", ".join(sorted(missing_keys))
        )

    for path_segments, required_keys in REQUIRED_NESTED_KEYS.items():
        node = root_mapping
        for segment in path_segments:
            node = _require_mapping(node.get(segment), ".".join(path_segments))
        missing_nested = required_keys - set(node.keys())
        if missing_nested:
            raise RuntimeTargetError(
                f"`{'.'.join(path_segments)}` is missing required keys: {', '.join(sorted(missing_nested))}"
            )

    target_platform = _require_mapping(root_mapping["target_platform"], "target_platform")
    rules_surfaces = _require_mapping(root_mapping["rules_surfaces"], "rules_surfaces")
    preferred_shell = _require_mapping(
        _require_mapping(root_mapping["windows_execution"], "windows_execution")["preferred_shell"],
        "windows_execution.preferred_shell",
    )
    preferred_python = _require_mapping(
        _require_mapping(root_mapping["windows_execution"], "windows_execution")["preferred_python"],
        "windows_execution.preferred_python",
    )
    utf8_env = _require_mapping(
        _require_mapping(root_mapping["windows_execution"], "windows_execution")["utf8_env"],
        "windows_execution.utf8_env",
    )
    search_policy = _require_mapping(root_mapping["search_policy"], "search_policy")

    for key, value in target_platform.items():
        if key != "source_urls":
            _require_non_empty_string(value, f"target_platform.{key}")
    _require_string_list(target_platform["source_urls"], "target_platform.source_urls")
    _require_non_empty_string(rules_surfaces["local_workspace"], "rules_surfaces.local_workspace")
    _require_non_empty_string(rules_surfaces["optional_global"], "rules_surfaces.optional_global")
    _require_string_list(root_mapping["approved_models"], "approved_models")
    if not isinstance(root_mapping["deprecated_models"], list):
        raise RuntimeTargetError("`deprecated_models` must be a list.")
    _require_non_empty_string(preferred_shell["profile_name"], "windows_execution.preferred_shell.profile_name")
    _require_non_empty_string(preferred_shell["executable"], "windows_execution.preferred_shell.executable")
    _require_non_empty_string(preferred_python["relative_path"], "windows_execution.preferred_python.relative_path")
    _require_non_empty_string(
        preferred_python["workspace_setting"],
        "windows_execution.preferred_python.workspace_setting",
    )
    if not isinstance(preferred_python["prefer_explicit_path_invocation"], bool):
        raise RuntimeTargetError("`windows_execution.preferred_python.prefer_explicit_path_invocation` must be boolean.")
    if not isinstance(preferred_python["forbid_naked_python_when_workspace_interpreter_known"], bool):
        raise RuntimeTargetError(
            "`windows_execution.preferred_python.forbid_naked_python_when_workspace_interpreter_known` must be boolean."
        )
    for key, value in utf8_env.items():
        _require_non_empty_string(value, f"windows_execution.utf8_env.{key}")
    _require_non_empty_string(search_policy["preferred_tool"], "search_policy.preferred_tool")
    if not isinstance(search_policy["rg_required"], bool):
        raise RuntimeTargetError("`search_policy.rg_required` must be boolean.")
    _require_non_empty_string(search_policy["first_failure_fallback"], "search_policy.first_failure_fallback")

    return root_mapping


def load_runtime_target(root: str | Path | None = None, path: str | Path | None = None) -> dict:
    """
    Load and validate the runtime-target manifest.

    purpose: manifest loading
    """
    manifest_path = Path(path).resolve() if path is not None else runtime_target_path(root)
    if not manifest_path.exists():
        raise RuntimeTargetError(f"runtime-target manifest not found: {manifest_path}")

    try:
        parsed = yaml.safe_load(manifest_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:  # pragma: no cover - exercised via validation path
        raise RuntimeTargetError(f"Invalid YAML in runtime-target manifest: {exc}") from exc

    return validate_runtime_target(parsed)


def workspace_python_path(root: str | Path | None = None, target: dict | None = None) -> Path:
    """
    Resolve the preferred workspace interpreter path.

    purpose: interpreter path resolution
    """
    manifest = target or load_runtime_target(root)
    relative_path = manifest["windows_execution"]["preferred_python"]["relative_path"]
    return repo_root(root) / Path(relative_path)

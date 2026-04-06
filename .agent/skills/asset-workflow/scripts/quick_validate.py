#!/usr/bin/env python3
"""
Quick validation script for the current Antigravity workflow contract.

role: workflow asset validator
entrypoints: main
reads: workflow markdown files
writes: stdout
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors; schema violations
coupling: coupled to workflow asset schema
determinism: input-dependent
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import sys
from pathlib import Path

import yaml

REQUIRED_FRONTMATTER_KEYS = {"description", "version"}
OPTIONAL_FRONTMATTER_KEYS = {"name"}
WORKFLOW_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
STEP_PATTERN = re.compile(r"^\d+\.\s", re.MULTILINE)


@dataclass
class ValidationResult:
    """
    Represent the outcome of a workflow validation check.

    Attributes
    ----------
    errors : list[str]
        blocking violations
    warnings : list[str]
        non-blocking recommendations
    """
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        """True if no blocking errors exist."""
        return not self.errors

    def summary(self) -> str:
        """Return a human-readable summary of the validation state."""
        if not self.valid:
            return "Workflow validation failed."
        if self.warnings:
            return "Workflow is valid against the current contract, with warnings."
        return "Workflow is valid against the current contract."


def extract_frontmatter(content: str) -> tuple[dict | None, str | None]:
    """
    Extract and parse the YAML frontmatter block from markdown content.

    purpose: metadata extraction
    """
    if not content.startswith("---"):
        return None, "No YAML frontmatter found."

    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return None, "Invalid frontmatter format."

    try:
        frontmatter = yaml.safe_load(match.group(1))
    except yaml.YAMLError as exc:
        return None, f"Invalid YAML in frontmatter: {exc}"

    if not isinstance(frontmatter, dict):
        return None, "Frontmatter must parse to a key-value mapping."

    return frontmatter, None


def extract_section(content: str, heading: str) -> str | None:
    """
    Extract the text content of a specific level-3 section.

    purpose: structural extraction
    """
    pattern = rf"(?ms)^### {re.escape(heading)}\s*\n(.*?)(?=^### |\Z)"
    match = re.search(pattern, content)
    return match.group(1).strip() if match else None


def validate_workflow(path: str | Path) -> ValidationResult:
    """
    Perform structural and semantic validation of a single workflow file.

    purpose: single-workflow validation
    preconditions: path is a readable markdown file
    postconditions: returns populated ValidationResult
    mutates: none
    reads: filesystem
    writes: none
    external_io: fs
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: coupled to workflow asset schema
    """
    result = ValidationResult()
    workflow_path = Path(path)
    if not workflow_path.exists():
        result.errors.append(f"Workflow not found: {workflow_path}")
        return result

    content = workflow_path.read_text(encoding="utf-8")
    frontmatter, frontmatter_error = extract_frontmatter(content)
    if frontmatter_error:
        result.errors.append(frontmatter_error)
        return result

    assert frontmatter is not None
    keys = set(frontmatter.keys())
    missing = REQUIRED_FRONTMATTER_KEYS - keys
    unexpected = keys - (REQUIRED_FRONTMATTER_KEYS | OPTIONAL_FRONTMATTER_KEYS)
    if missing:
        result.errors.append(f"Missing required frontmatter key(s): {', '.join(sorted(missing))}.")
    if unexpected:
        result.errors.append(f"Unexpected key(s) in frontmatter: {', '.join(sorted(unexpected))}.")

    version = str(frontmatter.get("version", "")).strip()
    if version and not SEMVER_PATTERN.fullmatch(version):
        result.errors.append("`version` must use semantic versioning, e.g. `1.0.0`.")

    name = frontmatter.get("name")
    if name is not None and not WORKFLOW_NAME_PATTERN.fullmatch(str(name).strip()):
        result.errors.append("`name` must use lowercase letters, digits, and hyphens only.")

    description = str(frontmatter.get("description", "")).strip()
    if not description:
        result.errors.append("`description` must be non-empty.")

    steps = extract_section(content, "steps")
    verification = extract_section(content, "verification_plan")
    if steps is None:
        result.errors.append("Missing required `### steps` section.")
    elif not STEP_PATTERN.search(steps):
        result.errors.append("`### steps` must contain at least one numbered step.")

    if verification is not None and not verification.strip():
        result.errors.append("`### verification_plan` must not be empty when present.")

    if result.errors:
        return result

    if len(description.split()) < 8:
        result.warnings.append("`description` is short. Add clearer trigger and outcome context.")

    if "TODO" in content:
        result.warnings.append("Workflow still contains TODO placeholders.")

    return result


def print_validation_result(result: ValidationResult) -> None:
    """
    Print a summary of validation results to stdout.

    purpose: reporting
    """
    print(result.summary())

    if result.errors:
        print("\nErrors:")
        for error in result.errors:
            print(f"- {error}")

    if result.warnings:
        print("\nWarnings:")
        for warning in result.warnings:
            print(f"- {warning}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <workflow_path>")
        sys.exit(1)

    validation_result = validate_workflow(sys.argv[1])
    print_validation_result(validation_result)
    sys.exit(0 if validation_result.valid else 1)

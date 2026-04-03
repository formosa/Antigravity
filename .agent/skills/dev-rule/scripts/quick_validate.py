#!/usr/bin/env python3
"""
Quick validation script for the current Antigravity rule contract.
"""

from __future__ import annotations

from dataclasses import dataclass, field
import re
import sys
from pathlib import Path

import yaml

REQUIRED_FRONTMATTER_KEYS = {"description", "priority", "trigger", "version"}
OPTIONAL_FRONTMATTER_KEYS = {"execution_tier", "globs", "name"}
VALID_TRIGGERS = {"@mention", "always_on", "auto", "glob", "manual"}
VALID_PRIORITIES = {"critical", "high", "low", "medium"}
VALID_EXECUTION_TIERS = {"parallel_high_perf", "standard"}
SEMVER_PATTERN = re.compile(r"^\d+\.\d+\.\d+$")
PREFERRED_RULE_NAME_PATTERN = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
LEGACY_RULE_NAME_PATTERN = re.compile(r"^[A-Za-z0-9][A-Za-z0-9_-]{0,127}$")
TODO_PLACEHOLDER_PATTERN = re.compile(r"(?i)(?:\btodo\s*:|\[todo\b)")


@dataclass
class ValidationResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def valid(self) -> bool:
        return not self.errors

    def summary(self) -> str:
        if not self.valid:
            return "Rule validation failed."
        if self.warnings:
            return "Rule is valid against the current contract, with warnings."
        return "Rule is valid against the current contract."


@dataclass
class FileReport:
    path: Path
    result: ValidationResult


def extract_frontmatter(content: str) -> tuple[dict | None, str | None]:
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


def extract_tag_block(content: str, block_name: str) -> str | None:
    pattern = rf"(?ms)^[ \t]*<{block_name}>[ \t]*\r?\n(.*?)^[ \t]*</{block_name}>[ \t]*$"
    match = re.search(pattern, content, re.DOTALL)
    return match.group(1).strip() if match else None


def strip_known_blocks(content: str) -> str:
    body = re.sub(r"^---\n.*?\n---\s*", "", content, count=1, flags=re.DOTALL)
    body = re.sub(r"(?ms)^[ \t]*<constraints>[ \t]*\r?\n.*?^[ \t]*</constraints>[ \t]*\r?\n?", "", body)
    body = re.sub(r"(?ms)^[ \t]*<verification_step>[ \t]*\r?\n.*?^[ \t]*</verification_step>[ \t]*\r?\n?", "", body)
    return body.strip()


def iter_rule_files(target: Path) -> list[Path]:
    if target.is_file():
        if target.name.lower() == "index.md":
            return []
        return [target]

    if target.is_dir():
        return sorted(
            [path for path in target.glob("*.md") if path.name.lower() != "index.md"],
            key=lambda path: path.name.lower(),
        )

    return []


def validate_rule_file(path: Path) -> ValidationResult:
    result = ValidationResult()
    content = path.read_text(encoding="utf-8")
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

    description = str(frontmatter.get("description", "")).strip()
    if not description:
        result.errors.append("`description` must be non-empty.")

    trigger = str(frontmatter.get("trigger", "")).strip()
    if trigger and trigger not in VALID_TRIGGERS:
        result.errors.append(f"`trigger` must be one of: {', '.join(sorted(VALID_TRIGGERS))}.")

    priority = str(frontmatter.get("priority", "")).strip()
    if priority and priority not in VALID_PRIORITIES:
        result.errors.append(f"`priority` must be one of: {', '.join(sorted(VALID_PRIORITIES))}.")

    execution_tier = frontmatter.get("execution_tier")
    if execution_tier is not None and str(execution_tier).strip() not in VALID_EXECUTION_TIERS:
        result.errors.append(
            f"`execution_tier` must be one of: {', '.join(sorted(VALID_EXECUTION_TIERS))}."
        )

    globs = frontmatter.get("globs")
    globs_text = str(globs).strip() if globs is not None else ""
    if trigger == "glob" and not globs_text:
        result.errors.append("`globs` is required when `trigger` is `glob`.")
    if trigger != "glob" and globs is not None:
        result.errors.append("`globs` must be omitted unless `trigger` is `glob`.")

    name = frontmatter.get("name")
    if name is not None:
        name_text = str(name).strip()
        if not name_text:
            result.errors.append("`name` must be non-empty when present.")
        elif not LEGACY_RULE_NAME_PATTERN.fullmatch(name_text):
            result.errors.append(
                "`name` must use letters, digits, hyphens, or underscores only for rule-asset compatibility."
            )
        elif not PREFERRED_RULE_NAME_PATTERN.fullmatch(name_text):
            result.warnings.append("`name` is valid but not in the preferred lowercase hyphen-case format.")

    constraints = extract_tag_block(content, "constraints")
    verification = extract_tag_block(content, "verification_step")
    if constraints is None:
        result.errors.append("Missing required `<constraints>` block.")
    elif not constraints.strip():
        result.errors.append("`<constraints>` must not be empty.")

    if verification is not None and not verification.strip():
        result.errors.append("`<verification_step>` must not be empty when present.")

    stray_content = strip_known_blocks(content)
    if stray_content:
        result.warnings.append("Rule contains content outside the recognized XML blocks.")

    if result.errors:
        return result

    if len(description.split()) < 10:
        result.warnings.append("`description` is short. Add clearer trigger and outcome context.")

    if execution_tier is None:
        result.warnings.append("`execution_tier` is omitted. Prefer `standard` unless a stronger case exists.")

    if TODO_PLACEHOLDER_PATTERN.search(content):
        result.warnings.append("Rule still contains TODO placeholders.")

    if not PREFERRED_RULE_NAME_PATTERN.fullmatch(path.stem):
        result.warnings.append("Filename is legacy-compatible but not in the preferred lowercase hyphen-case format.")

    return result


def print_report(report: FileReport) -> None:
    print(f"\n[{report.path.as_posix()}]")
    print(report.result.summary())

    if report.result.errors:
        print("Errors:")
        for error in report.result.errors:
            print(f"- {error}")

    if report.result.warnings:
        print("Warnings:")
        for warning in report.result.warnings:
            print(f"- {warning}")


def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <rule_path_or_directory>")
        sys.exit(1)

    target = Path(sys.argv[1]).resolve()
    if not target.exists():
        print(f"Error: Path not found: {target}")
        sys.exit(1)

    rule_files = iter_rule_files(target)
    if target.is_file() and target.name.lower() == "index.md":
        print("Skipped index file: rule validation applies only to individual rule assets.")
        sys.exit(0)

    if not rule_files:
        print("No rule files found to validate.")
        sys.exit(1)

    reports = [FileReport(path=rule_path, result=validate_rule_file(rule_path)) for rule_path in rule_files]
    valid_count = sum(1 for report in reports if report.result.valid)
    error_count = sum(1 for report in reports if report.result.errors)
    warning_count = sum(1 for report in reports if report.result.warnings)

    print(
        f"Validated {len(reports)} rule file(s): {valid_count} valid, {error_count} with errors, "
        f"{warning_count} with warnings."
    )
    for report in reports:
        print_report(report)

    sys.exit(0 if error_count == 0 else 1)


if __name__ == "__main__":
    main()

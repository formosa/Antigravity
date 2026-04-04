#!/usr/bin/env python3
"""
Validator for issue-report artifacts used by artifact-issue-report.

Canonical mode validates the current v6.1-style output contract.
Legacy mode validates historical v4/v5 report artifacts without rewriting them.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}")
FRONTMATTER_RE = re.compile(r"^---\s*\n(?P<yaml>.*?)\n---\s*\n", re.DOTALL)
ABSOLUTE_WINDOWS_PATH_RE = re.compile(r"(?i)\b[a-z]:\\[^\s`]+")

CANONICAL_MARKERS = [
    '## Optimized Resolution Strategy for "',
    "### Agent Context",
    "### 1. Validation Audit of ",
    "### 2. Suggested Strategies for Optimal Resolution of ",
    "### 3. Comparative Analysis and Recommended Strategy",
    "#### Comparative Analysis",
    "#### Endorsement and Contextual Justification",
    "### 4. Implementation Note",
]

LEGACY_MARKERS = [
    '## Optimized Resolution Strategy for "',
    "### Agent Context",
    "### 1. Validation Audit of ",
    "### 2. Suggested Strategies for Optimal Resolution of ",
    "### 3. Comparative Analysis and Recommended Strategy",
    "#### Comparative Analysis",
    "#### Endorsement and Contextual Justification",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate issue-report artifacts.")
    parser.add_argument("path", help="Path to the issue-report markdown file.")
    parser.add_argument(
        "--mode",
        choices=("auto", "canonical", "legacy"),
        default="auto",
        help="Validation profile. Defaults to auto-detect.",
    )
    return parser.parse_args()


def detect_mode(content: str) -> str:
    if "### 4. Implementation Note" in content or re.search(r"^\s*updated:\s*", content, re.MULTILINE):
        return "canonical"
    return "legacy"


def detect_legacy_profile(content: str) -> str:
    if "#### Option C:" in content or "### 4. Independent Review Conclusion" in content:
        return "v4-like"
    return "v5-like"


def parse_frontmatter(content: str) -> dict:
    match = FRONTMATTER_RE.match(content)
    if not match:
        raise ValueError("Missing YAML frontmatter")
    parsed = yaml.safe_load(match.group("yaml"))
    if not isinstance(parsed, dict) or "document" not in parsed:
        raise ValueError("Frontmatter must contain a top-level 'document' object")
    document = parsed["document"]
    if not isinstance(document, dict):
        raise ValueError("'document' frontmatter must be a mapping")
    return document


def extract_agent_context(content: str) -> dict:
    match = re.search(
        r"^### Agent Context\s+```yaml\s*(?P<yaml>.*?)```",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("Missing Agent Context YAML block")
    parsed = yaml.safe_load(match.group("yaml"))
    if not isinstance(parsed, dict):
        raise ValueError("Agent Context block must parse to a mapping")
    return parsed


def extract_section(content: str, heading: str) -> str:
    pattern = rf"^{re.escape(heading)}\n(?P<body>.*?)(?=^### |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group("body").strip()


def extract_option_block(content: str, option: str) -> str:
    pattern = rf"^#### {re.escape(option)}: .*?\n(?P<body>.*?)(?=^#### Option [A-Z]: |^### |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing block for {option}")
    return match.group("body").strip()


def validate_heading_order(content: str, markers: list[str], errors: list[str]) -> None:
    last_index = -1
    for marker in markers:
        index = content.find(marker)
        if index == -1:
            errors.append(f"Missing required heading or marker: {marker}")
            continue
        if index < last_index:
            errors.append(f"Heading order is invalid around: {marker}")
        last_index = index


def validate_common_structure(content: str, errors: list[str]) -> None:
    if PLACEHOLDER_RE.search(content):
        errors.append("Report contains unresolved placeholders")
    if not re.search(r'^## Optimized Resolution Strategy for "ISSUE-\d{3}"', content, re.MULTILINE):
        errors.append("Missing or invalid report title heading")
    if content.count("#### Option A:") != 1:
        errors.append("Report must contain exactly one Option A section")
    if content.count("#### Option B:") != 1:
        errors.append("Report must contain exactly one Option B section")


def validate_frontmatter_keys(document: dict, required: set[str], errors: list[str]) -> None:
    missing = sorted(required - set(document.keys()))
    if missing:
        errors.append(f"Frontmatter is missing required keys: {', '.join(missing)}")


def validate_canonical(content: str) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    notes: list[str] = []

    validate_common_structure(content, errors)
    validate_heading_order(content, CANONICAL_MARKERS, errors)

    if "#### Option C:" in content:
        errors.append("Canonical reports must not contain Option C")
    if "### 4. Independent Review Conclusion" in content:
        errors.append("Canonical reports must not contain Independent Review Conclusion")

    try:
        document = parse_frontmatter(content)
    except ValueError as exc:
        return [str(exc)], notes

    validate_frontmatter_keys(
        document,
        {
            "id",
            "title",
            "format_version",
            "target_platform",
            "target_model",
            "subject",
            "created",
            "updated",
            "status",
            "severity",
            "type",
        },
        errors,
    )

    status = document.get("status")
    if status == "RESOLVED" and "resolved" not in document:
        errors.append("Canonical resolved reports must include document.resolved")
    if status != "RESOLVED" and "resolved" in document:
        errors.append("Canonical non-resolved reports must not include document.resolved")

    try:
        agent_context = extract_agent_context(content)
    except ValueError as exc:
        return errors + [str(exc)], notes

    for field in ("id", "status", "severity", "type", "tier_refs", "section_ref", "rule_refs", "updated"):
        if field not in agent_context:
            errors.append(f"Agent Context is missing required field: {field}")

    issue_match = re.search(r"(ISSUE-\d{3})", str(document.get("title", "")))
    if issue_match and agent_context.get("id") != issue_match.group(1):
        errors.append("Agent Context id does not match the issue id embedded in the document title")

    for field in ("status", "severity", "type"):
        if field in document and field in agent_context and document[field] != agent_context[field]:
            errors.append(f"Frontmatter and Agent Context disagree on {field}")

    if "updated" in document and "updated" in agent_context:
        if str(document["updated"]) != str(agent_context["updated"]):
            errors.append("Frontmatter and Agent Context disagree on updated")

    if status == "RESOLVED":
        if "resolved" not in agent_context:
            errors.append("Resolved canonical reports must include Agent Context resolved")
        elif str(document.get("resolved")) != str(agent_context.get("resolved")):
            errors.append("Frontmatter and Agent Context disagree on resolved")
    elif "resolved" in agent_context:
        errors.append("Non-resolved canonical reports must not include Agent Context resolved")

    for option_name in ("Option A", "Option B"):
        try:
            option_block = extract_option_block(content, option_name)
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if "* **Supporting Insights:**" not in option_block:
            errors.append(f"{option_name} is missing Supporting Insights")
        if "* **Citations:**" not in option_block:
            errors.append(f"{option_name} is missing Citations")

    try:
        implementation_note = extract_section(content, "### 4. Implementation Note")
    except ValueError as exc:
        errors.append(str(exc))
        implementation_note = ""

    if status == "RESOLVED":
        if implementation_note and re.search(r"\bpending\b", implementation_note, re.IGNORECASE):
            errors.append("Resolved canonical reports must not describe implementation as pending")
    else:
        if implementation_note and not re.search(
            r"\bpending\b|not yet implemented|did not apply a repository patch",
            implementation_note,
            re.IGNORECASE,
        ):
            errors.append(
                "Non-resolved canonical reports must state that implementation remains pending"
            )

    absolute_paths = ABSOLUTE_WINDOWS_PATH_RE.findall(content)
    if absolute_paths:
        notes.append(
            "Report uses absolute Windows paths. Historical canonical artifacts are accepted, but new reports should use repo-relative paths."
        )

    return errors, notes


def validate_legacy(content: str) -> tuple[list[str], str]:
    errors: list[str] = []

    validate_common_structure(content, errors)
    validate_heading_order(content, LEGACY_MARKERS, errors)

    try:
        document = parse_frontmatter(content)
    except ValueError as exc:
        return [str(exc)], "unknown"

    validate_frontmatter_keys(
        document,
        {
            "id",
            "title",
            "format_version",
            "target_platform",
            "target_model",
            "subject",
            "created",
            "status",
            "severity",
            "type",
        },
        errors,
    )

    if "### 4. Implementation Note" in content and "updated" not in document:
        errors.append("Legacy reports should not use the canonical Implementation Note section")

    profile = detect_legacy_profile(content)
    if profile == "v5-like" and "#### Option C:" in content:
        errors.append("v5-like legacy reports must not contain Option C")

    try:
        agent_context = extract_agent_context(content)
    except ValueError as exc:
        return errors + [str(exc)], profile

    if "id" not in agent_context:
        errors.append("Legacy Agent Context is missing required field: id")
    else:
        issue_match = re.search(r"(ISSUE-\d{3})", str(document.get("title", "")))
        if issue_match and agent_context.get("id") != issue_match.group(1):
            errors.append("Agent Context id does not match the issue id embedded in the document title")

    for field in ("status", "severity", "type"):
        if field not in agent_context:
            errors.append(f"Legacy Agent Context is missing required field: {field}")
        elif document.get(field) != agent_context.get(field):
            errors.append(f"Frontmatter and Agent Context disagree on {field}")

    return errors, profile


def validate_content(content: str, mode: str = "auto") -> tuple[str, list[str], list[str]]:
    resolved_mode = detect_mode(content) if mode == "auto" else mode

    if resolved_mode == "canonical":
        errors, notes = validate_canonical(content)
        label = "canonical"
    else:
        errors, profile = validate_legacy(content)
        notes = []
        label = f"legacy:{profile}"

    return label, errors, notes


def validate_path(path: str | Path, mode: str = "auto") -> tuple[str, list[str], list[str]]:
    resolved_path = Path(path)
    if not resolved_path.exists():
        return "missing", [f"file not found: {resolved_path}"], []

    content = resolved_path.read_text(encoding="utf-8")
    return validate_content(content, mode=mode)


def main() -> int:
    args = parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"INVALID: file not found: {path}")
        return 1

    label, errors, notes = validate_path(path, mode=args.mode)

    if errors:
        print(f"INVALID [{label}] {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID [{label}] {path}")
    for note in notes:
        print(f"! {note}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Validator for Issues Tracker artifacts used by artifact-issue-tracker.

Canonical mode validates the current blank-initialization contract.
Legacy mode validates historical v4/v5 tracker artifacts without rewriting them.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

REQUIRED_SECTIONS = [
    "DOCUMENT METADATA",
    "ISSUE SCHEMA",
    "ISSUE REGISTRY",
    "ISSUES",
    "RESOLUTION WORKFLOW",
    "APPENDIX: CROSS-ISSUE DEPENDENCY MAP",
]

PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}")
ISSUE_HEADING_RE = re.compile(r"^### ISSUE-\d{3}:", re.MULTILINE)
FOOTER_RE = re.compile(
    r"^\*(?P<total>\d+) issues identified \| (?P<resolved>\d+) resolved \| Last updated: "
    r"(?P<date>\d{4}-\d{2}-\d{2})\*$",
    re.MULTILINE,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate Issues Tracker artifacts.")
    parser.add_argument("path", help="Path to the Issues Tracker markdown file.")
    parser.add_argument(
        "--mode",
        choices=("auto", "canonical", "legacy"),
        default="auto",
        help="Validation profile. Defaults to auto-detect.",
    )
    return parser.parse_args()


def detect_mode(content: str) -> str:
    if "AGENT PARSING HEADER" in content or "<!-- AGENT_CONTEXT" in content:
        return "legacy"
    return "canonical"


def extract_section(content: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group("body").strip()


def extract_between_headings(content: str, start_heading: str, end_heading: str) -> str:
    pattern = (
        rf"^## {re.escape(start_heading)}\n(?P<body>.*?)(?=^## {re.escape(end_heading)}\n)"
    )
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Could not extract section between {start_heading} and {end_heading}")
    return match.group("body").strip()


def parse_metadata(content: str) -> dict:
    match = re.search(
        r"^## DOCUMENT METADATA\s+```yaml\s*(?P<yaml>.*?)```",
        content,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise ValueError("Missing DOCUMENT METADATA yaml block")
    parsed = yaml.safe_load(match.group("yaml"))
    if not isinstance(parsed, dict) or "document" not in parsed:
        raise ValueError("DOCUMENT METADATA must contain a top-level 'document' object")
    if not isinstance(parsed["document"], dict):
        raise ValueError("'document' metadata must be a mapping")
    return parsed["document"]


def parse_footer(content: str) -> tuple[int, int, str]:
    match = FOOTER_RE.search(content)
    if not match:
        raise ValueError("Missing footer summary line")
    return (
        int(match.group("total")),
        int(match.group("resolved")),
        match.group("date"),
    )


def parse_table_rows(section_body: str) -> list[list[str]]:
    lines = [line.strip() for line in section_body.splitlines() if line.strip().startswith("|")]
    if len(lines) < 3:
        raise ValueError("Issue registry table is incomplete")
    data_lines = lines[2:]
    rows: list[list[str]] = []
    for line in data_lines:
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def count_issue_statuses(issue_section: str) -> dict[str, int]:
    counts: dict[str, int] = {}
    for match in re.finditer(r"^\*\*Status:\*\* `(?P<status>[^`]+)`", issue_section, re.MULTILINE):
        status = match.group("status")
        counts[status] = counts.get(status, 0) + 1
    return counts


def validate_required_sections(content: str, errors: list[str]) -> None:
    for heading in REQUIRED_SECTIONS:
        if f"## {heading}" not in content:
            errors.append(f"Missing section heading: {heading}")


def validate_canonical(content: str) -> list[str]:
    errors: list[str] = []
    validate_required_sections(content, errors)

    if "AGENT PARSING HEADER" in content:
        errors.append("Canonical format must not contain an HTML parser header")
    if "<!-- AGENT_CONTEXT" in content:
        errors.append("Canonical format must not contain AGENT_CONTEXT blocks")
    if PLACEHOLDER_RE.search(content):
        errors.append("Canonical format contains unresolved placeholders")

    try:
        metadata = parse_metadata(content)
    except ValueError as exc:
        errors.append(str(exc))
        return errors

    required_keys = {
        "id",
        "title",
        "format_version",
        "target_platform",
        "target_model",
        "subject",
        "created",
        "last_modified",
        "author",
        "open_issues",
        "resolved_issues",
        "status_values",
        "severity_values",
        "type_values",
    }
    missing = sorted(required_keys - set(metadata.keys()))
    if missing:
        errors.append(f"DOCUMENT METADATA is missing required keys: {', '.join(missing)}")

    title = metadata.get("title")
    subject = metadata.get("subject")
    heading_match = re.search(r"^# (?P<title>.+)$", content, re.MULTILINE)
    if heading_match and subject and title:
        expected_heading = f"{subject} — Issues Tracker"
        if heading_match.group("title") != expected_heading:
            errors.append("Top-level heading does not match metadata subject")
        if title != expected_heading:
            errors.append("DOCUMENT METADATA title does not match metadata subject")

    issue_count = len(ISSUE_HEADING_RE.findall(content))
    if issue_count != 0:
        errors.append(f"Canonical blank initialization must contain 0 issue entries, found {issue_count}")

    if metadata.get("open_issues") != 0:
        errors.append("Canonical blank initialization must set open_issues to 0")
    if metadata.get("resolved_issues") != 0:
        errors.append("Canonical blank initialization must set resolved_issues to 0")

    try:
        rows = parse_table_rows(extract_section(content, "ISSUE REGISTRY"))
    except ValueError as exc:
        errors.append(str(exc))
        rows = []

    if rows:
        if len(rows) != 1:
            errors.append(f"Canonical blank initialization must contain exactly 1 registry row, found {len(rows)}")
        elif any(cell for cell in rows[0]):
            errors.append("Canonical blank initialization registry row must be empty")

    try:
        total_issues, resolved_issues, footer_date = parse_footer(content)
        if total_issues != 0:
            errors.append("Footer total issues must be 0 for a blank initialization")
        if resolved_issues != 0:
            errors.append("Footer resolved issues must be 0 for a blank initialization")
        if metadata.get("last_modified") != footer_date:
            errors.append("Footer date must match document.last_modified")
    except ValueError as exc:
        errors.append(str(exc))

    return errors


def parse_legacy_header_counts(content: str) -> tuple[int, int, int]:
    header_match = re.search(r"<!--(?P<header>.*?)-->", content, re.DOTALL)
    if not header_match:
        raise ValueError("Legacy format must contain an HTML parser header")
    header = header_match.group("header")
    values = []
    for key in ("total_issues", "open_issues", "resolved_issues"):
        match = re.search(rf"{key}:\s+(\d+)", header)
        if not match:
            raise ValueError(f"Legacy header is missing {key}")
        values.append(int(match.group(1)))
    return values[0], values[1], values[2]


def validate_legacy(content: str) -> list[str]:
    errors: list[str] = []
    validate_required_sections(content, errors)

    if "AGENT PARSING HEADER" not in content:
        errors.append("Legacy format must contain an AGENT PARSING HEADER")
    if "<!-- AGENT_CONTEXT" not in content:
        errors.append("Legacy format must contain AGENT_CONTEXT blocks")
    if PLACEHOLDER_RE.search(content):
        errors.append("Legacy format contains unresolved placeholders")

    try:
        issue_section = extract_between_headings(content, "ISSUES", "RESOLUTION WORKFLOW")
    except ValueError as exc:
        errors.append(str(exc))
        issue_section = ""

    issue_count = len(ISSUE_HEADING_RE.findall(issue_section))

    try:
        total_issues, open_issues, resolved_issues = parse_legacy_header_counts(content)
        if issue_count != total_issues:
            errors.append(
                f"Legacy header total_issues ({total_issues}) does not match issue entry count ({issue_count})"
            )
    except ValueError as exc:
        errors.append(str(exc))
        total_issues = open_issues = resolved_issues = 0

    status_counts = count_issue_statuses(issue_section)
    actual_total = sum(status_counts.values())

    if issue_section and actual_total != issue_count:
        errors.append("Could not reconcile issue status lines with issue headings in legacy tracker")

    return errors


def main() -> int:
    args = parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"INVALID: file not found: {path}")
        return 1

    content = path.read_text(encoding="utf-8")
    mode = detect_mode(content) if args.mode == "auto" else args.mode
    errors = validate_canonical(content) if mode == "canonical" else validate_legacy(content)

    if errors:
        print(f"INVALID [{mode}] {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID [{mode}] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

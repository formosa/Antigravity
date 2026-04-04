#!/usr/bin/env python3
"""
Validate populated IT-1.1 Issues Tracker artifacts used by artifact-issue-tracker.
"""

from __future__ import annotations

import argparse
import difflib
import re
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

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
FOOTER_SUMMARY_RE = re.compile(
    r"^\*(?P<total>\d+) issues identified \| (?P<resolved>\d+) resolved \| Last updated: "
    r"(?P<date>\d{4}-\d{2}-\d{2})\*$",
    re.MULTILINE,
)
FOOTER_BANNER_RE = re.compile(r"^\*(?P<label>.+) — IT-1\.1\*$", re.MULTILINE)
ISSUE_HEADING_RE = re.compile(r"^### ISSUE-(?P<num>\d{3}): (?P<title>.+)$", re.MULTILINE)
STATUS_LINE_RE = re.compile(
    r"^\*\*Status:\*\* `(?P<status>[^`]+)` \| \*\*Severity:\*\* `(?P<severity>[^`]+)` \| "
    r"\*\*Type:\*\* `(?P<issue_type>[^`]+)`$",
    re.MULTILINE,
)
META_LINE_RE = re.compile(
    r"^\*\*Tiers Affected:\*\* `(?P<tiers>[^`]+)` \| \*\*Spec Section:\*\* `(?P<section>[^`]+)`$",
    re.MULTILINE,
)
SUBSECTION_RE = re.compile(
    r"^#### (?P<heading>[^\n]+)\n(?P<body>.*?)(?=^#### |\Z)",
    re.MULTILINE | re.DOTALL,
)
RECOMMENDATION_RE = re.compile(r"\*\*Endorsed Option:\*\*\s*`Option (?P<option>[ABC])`")
CITATION_LINE_RE = re.compile(
    r"^- \[(?P<label>[^\]]+)\]\((?P<url>https?://[^)\s]+)\): (?P<note>.+)$"
)

EXPECTED_STATUS_VALUES = ["OPEN", "IN_REVIEW", "RESOLVED", "WONT_FIX", "DEFERRED"]
EXPECTED_SEVERITY_VALUES = ["CRITICAL", "MAJOR", "MODERATE", "MINOR"]
EXPECTED_TYPE_VALUES = [
    "LOGICAL_CONFLICT",
    "DESIGN_INADEQUACY",
    "UNNECESSARY_COMPLEXITY",
    "AXIOM_VIOLATION",
    "SCHEMA_DEFECT",
    "MIGRATION_GAP",
    "LIFECYCLE_GAP",
]
SEVERITY_ORDER = {name: index for index, name in enumerate(EXPECTED_SEVERITY_VALUES)}
OPEN_COUNT_STATUSES = {"OPEN", "IN_REVIEW"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate populated IT-1.1 Issues Tracker artifacts.")
    parser.add_argument("path", help="Path to the Issues Tracker markdown file.")
    return parser.parse_args()


def extract_section(content: str, heading: str) -> str:
    pattern = rf"^## {re.escape(heading)}\n(?P<body>.*?)(?=^## |\Z)"
    match = re.search(pattern, content, re.MULTILINE | re.DOTALL)
    if not match:
        raise ValueError(f"Missing section: {heading}")
    return match.group("body").strip()


def parse_metadata(content: str) -> dict[str, Any]:
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
    document = parsed["document"]
    if not isinstance(document, dict):
        raise ValueError("'document' metadata must be a mapping")
    return document


def parse_table_rows(section_body: str) -> list[list[str]]:
    lines = [line.strip() for line in section_body.splitlines() if line.strip().startswith("|")]
    if len(lines) < 2:
        raise ValueError("Issue registry table is incomplete")

    data_lines = lines[2:]
    rows: list[list[str]] = []
    for line in data_lines:
        rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def normalize_text(value: str) -> str:
    value = value.lower()
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def unwrap_code_cell(value: str) -> str:
    value = value.strip()
    if value.startswith("`") and value.endswith("`") and len(value) >= 2:
        return value[1:-1]
    return value


def parse_issue_blocks(content: str) -> list[dict[str, Any]]:
    issues_body = extract_section(content, "ISSUES")
    matches = list(ISSUE_HEADING_RE.finditer(issues_body))
    issues: list[dict[str, Any]] = []

    for index, match in enumerate(matches):
        start = match.start()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(issues_body)
        block = issues_body[start:end].strip()
        issue_number = match.group("num")

        status_match = STATUS_LINE_RE.search(block)
        if not status_match:
            raise ValueError(f"ISSUE-{issue_number} is missing the Status/Severity/Type metadata line")

        meta_match = META_LINE_RE.search(block)
        if not meta_match:
            raise ValueError(f"ISSUE-{issue_number} is missing the Tiers Affected/Spec Section metadata line")

        subsections = {
            subsection_match.group("heading"): subsection_match.group("body").strip()
            for subsection_match in SUBSECTION_RE.finditer(block)
        }

        issues.append(
            {
                "id": f"ISSUE-{issue_number}",
                "number": int(issue_number),
                "title": match.group("title").strip(),
                "status": status_match.group("status"),
                "severity": status_match.group("severity"),
                "type": status_match.group("issue_type"),
                "tiers": meta_match.group("tiers"),
                "section": meta_match.group("section"),
                "block": block,
                "subsections": subsections,
            }
        )

    return issues


def is_valid_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def validate_required_sections(content: str, errors: list[str]) -> None:
    for heading in REQUIRED_SECTIONS:
        if f"## {heading}" not in content:
            errors.append(f"Missing section heading: {heading}")


def validate_metadata(content: str, metadata: dict[str, Any], errors: list[str]) -> None:
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

    if metadata.get("format_version") != "IT-1.1":
        errors.append("document.format_version must be IT-1.1")

    if metadata.get("status_values") != EXPECTED_STATUS_VALUES:
        errors.append("document.status_values must match the IT-1.1 canonical status list")
    if metadata.get("severity_values") != EXPECTED_SEVERITY_VALUES:
        errors.append("document.severity_values must match the IT-1.1 canonical severity list")
    if metadata.get("type_values") != EXPECTED_TYPE_VALUES:
        errors.append("document.type_values must match the IT-1.1 canonical type list")

    heading_match = re.search(r"^# (?P<title>.+)$", content, re.MULTILINE)
    subject = metadata.get("subject")
    title = metadata.get("title")
    expected_title = f"{subject} — Issues Tracker" if subject else None
    if heading_match and expected_title and heading_match.group("title") != expected_title:
        errors.append("Top-level heading does not match metadata subject")
    if expected_title and title != expected_title:
        errors.append("DOCUMENT METADATA title does not match metadata subject")


def validate_it11_schema_and_workflow(content: str, errors: list[str]) -> None:
    try:
        issue_schema = extract_section(content, "ISSUE SCHEMA")
    except ValueError as exc:
        errors.append(str(exc))
        issue_schema = ""

    for marker in (
        "Resolution-[NNN]: Option C - [Short Label]",
        "Comparative Analysis-[NNN]",
        "Recommendation-[NNN]",
        "Supporting Citations-[NNN]",
    ):
        if marker not in issue_schema:
            errors.append(f"ISSUE SCHEMA is missing the IT-1.1 marker: {marker}")

    try:
        workflow = extract_section(content, "RESOLUTION WORKFLOW")
    except ValueError as exc:
        errors.append(str(exc))
        workflow = ""

    if "Option (A/B/C)" not in workflow:
        errors.append("RESOLUTION WORKFLOW must reference Option (A/B/C)")
    if 'Record resolution: "Option [A|B|C]:' not in workflow:
        errors.append("RESOLUTION WORKFLOW must allow recording Option [A|B|C]")


def validate_issue_subsections(issue: dict[str, Any], errors: list[str]) -> None:
    issue_id = issue["id"]
    number = issue["number"]
    suffix = f"{number:03d}"
    subsections = issue["subsections"]

    expected_plain = [
        f"Problem Statement-{suffix}",
        f"Evidence & Justification-{suffix}",
        f"Impact Assessment-{suffix}",
        f"Comparative Analysis-{suffix}",
        f"Recommendation-{suffix}",
        f"Supporting Citations-{suffix}",
        f"Notes-{suffix}",
    ]
    for heading in expected_plain:
        if heading not in subsections:
            errors.append(f"{issue_id} is missing subsection: {heading}")

    option_info: dict[str, tuple[str, str]] = {}
    for option in ("A", "B", "C"):
        prefix = f"Resolution-{suffix}: Option {option} - "
        heading = next((name for name in subsections if name.startswith(prefix)), None)
        if heading is None:
            errors.append(f"{issue_id} is missing Resolution-{suffix}: Option {option} - ...")
            continue
        option_info[option] = (heading[len(prefix) :].strip(), subsections[heading])

    if {"A", "B", "C"} <= option_info.keys():
        label_a, body_a = option_info["A"]
        label_b, body_b = option_info["B"]
        label_c, body_c = option_info["C"]
        if normalize_text(label_c) in {normalize_text(label_a), normalize_text(label_b)}:
            errors.append(f"{issue_id} Option C must use a distinct label")

        similarity_ac = difflib.SequenceMatcher(None, normalize_text(body_a), normalize_text(body_c)).ratio()
        similarity_bc = difflib.SequenceMatcher(None, normalize_text(body_b), normalize_text(body_c)).ratio()
        if normalize_text(body_c) in {normalize_text(body_a), normalize_text(body_b)} or similarity_ac >= 0.96 or similarity_bc >= 0.96:
            errors.append(f"{issue_id} Option C is not materially distinct from Option A or Option B")

    recommendation_heading = f"Recommendation-{suffix}"
    if recommendation_heading in subsections:
        recommendation = subsections[recommendation_heading]
        match = RECOMMENDATION_RE.search(recommendation)
        if not match:
            errors.append(f"{issue_id} Recommendation-{suffix} must declare **Endorsed Option:** `Option A|B|C`")
        elif match.group("option") not in option_info:
            errors.append(f"{issue_id} Recommendation-{suffix} endorses an option that is not defined")

    citations_heading = f"Supporting Citations-{suffix}"
    if citations_heading in subsections:
        citations = subsections[citations_heading]
        bullet_lines = [line.strip() for line in citations.splitlines() if line.strip().startswith("- ")]
        if not bullet_lines:
            errors.append(f"{issue_id} Supporting Citations-{suffix} must contain at least one citation bullet")
        for line in bullet_lines:
            match = CITATION_LINE_RE.match(line)
            if not match:
                errors.append(f"{issue_id} has a malformed citation bullet: {line}")
                continue
            if not is_valid_url(match.group("url")):
                errors.append(f"{issue_id} has an invalid citation URL: {match.group('url')}")


def validate_issue_registry(content: str, issues: list[dict[str, Any]], errors: list[str]) -> None:
    try:
        rows = parse_table_rows(extract_section(content, "ISSUE REGISTRY"))
    except ValueError as exc:
        errors.append(str(exc))
        return

    if not issues:
        non_empty_rows = [row for row in rows if any(cell.strip() for cell in row)]
        if len(non_empty_rows) > 1:
            errors.append("An empty IT-1.1 tracker must not contain more than one non-empty registry row")
        return

    if len(rows) != len(issues):
        errors.append(
            f"Issue registry row count ({len(rows)}) does not match issue entry count ({len(issues)})"
        )
        return

    issue_map = {issue["id"]: issue for issue in issues}
    parsed_rows: list[dict[str, Any]] = []
    for row in rows:
        if len(row) != 6:
            errors.append(f"Issue registry row must contain 6 cells, found {len(row)}")
            continue

        issue_id_match = re.search(r"ISSUE-\d{3}", row[0])
        if not issue_id_match:
            errors.append(f"Could not parse issue id from registry row: {row[0]}")
            continue

        issue_id = issue_id_match.group(0)
        severity = unwrap_code_cell(row[1])
        issue_type = unwrap_code_cell(row[2])
        status = unwrap_code_cell(row[3])
        tiers = unwrap_code_cell(row[4])
        title = row[5].strip()

        parsed_rows.append(
            {
                "id": issue_id,
                "severity": severity,
                "type": issue_type,
                "status": status,
                "tiers": tiers,
                "title": title,
            }
        )

        if issue_id not in issue_map:
            errors.append(f"Registry row references unknown issue id: {issue_id}")
            continue

        issue = issue_map[issue_id]
        if severity != issue["severity"]:
            errors.append(f"{issue_id} registry severity does not match issue body")
        if issue_type != issue["type"]:
            errors.append(f"{issue_id} registry type does not match issue body")
        if status != issue["status"]:
            errors.append(f"{issue_id} registry status does not match issue body")
        if tiers != issue["tiers"]:
            errors.append(f"{issue_id} registry tiers do not match issue body")
        if normalize_text(title) != normalize_text(issue["title"]):
            errors.append(f"{issue_id} registry title does not match issue heading")

    expected_order = sorted(
        parsed_rows,
        key=lambda row: (SEVERITY_ORDER.get(row["severity"], 999), int(row["id"].split("-")[1])),
    )
    if parsed_rows and parsed_rows != expected_order:
        errors.append("Issue registry rows must be sorted by severity then issue number")


def validate_footer(metadata: dict[str, Any], issues: list[dict[str, Any]], content: str, errors: list[str]) -> None:
    banner_match = FOOTER_BANNER_RE.search(content)
    if not banner_match:
        errors.append("Missing IT-1.1 footer banner line")

    summary_match = FOOTER_SUMMARY_RE.search(content)
    if not summary_match:
        errors.append("Missing footer summary line")
        return

    total_issues = len(issues)
    resolved_issues = sum(1 for issue in issues if issue["status"] == "RESOLVED")
    open_issues = sum(1 for issue in issues if issue["status"] in OPEN_COUNT_STATUSES)

    if metadata.get("open_issues") != open_issues:
        errors.append(
            f"document.open_issues ({metadata.get('open_issues')}) does not match OPEN+IN_REVIEW count ({open_issues})"
        )
    if metadata.get("resolved_issues") != resolved_issues:
        errors.append(
            f"document.resolved_issues ({metadata.get('resolved_issues')}) does not match RESOLVED count ({resolved_issues})"
        )

    if int(summary_match.group("total")) != total_issues:
        errors.append("Footer total issues does not match issue entry count")
    if int(summary_match.group("resolved")) != resolved_issues:
        errors.append("Footer resolved issues does not match RESOLVED issue count")
    if metadata.get("last_modified") != summary_match.group("date"):
        errors.append("Footer date must match document.last_modified")


def validate_tracker_content(content: str, source: str = "<memory>") -> list[str]:
    errors: list[str] = []
    validate_required_sections(content, errors)

    if PLACEHOLDER_RE.search(content):
        errors.append("Tracker contains unresolved placeholders")

    if errors:
        return errors

    try:
        metadata = parse_metadata(content)
    except ValueError as exc:
        return [str(exc)]

    validate_metadata(content, metadata, errors)
    validate_it11_schema_and_workflow(content, errors)

    try:
        issues = parse_issue_blocks(content)
    except ValueError as exc:
        return errors + [str(exc)]

    for issue in issues:
        validate_issue_subsections(issue, errors)

    validate_issue_registry(content, issues, errors)
    validate_footer(metadata, issues, content, errors)

    return errors


def validate_path(path: Path) -> list[str]:
    return validate_tracker_content(path.read_text(encoding="utf-8"), str(path))


def main() -> int:
    args = parse_args()
    path = Path(args.path)

    if not path.exists():
        print(f"INVALID: file not found: {path}")
        return 1

    errors = validate_path(path)
    if errors:
        print(f"INVALID [IT-1.1] {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID [IT-1.1] {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
"""
Validate brainstorm.md documents managed by codex-brainstorm.
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SEED = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"

REQUIRED_HEADINGS = [
    "## PART I — Document Manifest",
    "### §1 Document Purpose and Scope",
    "### §2 Document Structure and Navigation",
    "#### 2.1 Part Registry",
    "### §3 Entry Schema (BRAIN-ENTRY-1.0)",
    "#### 3.1 Common Fields (All Entry Types)",
    "#### 3.2 Idea Entry (TYPE: IDEA)",
    "#### 3.3 Library Candidate Entry (TYPE: LIB)",
    "#### 3.4 Category Taxonomy",
    "#### 3.5 Entry Status Vocabulary",
    "#### 3.6 Priority Vocabulary",
    "### §4 Rules for Adding New Sections",
    "### §5 Governance and Promotion Protocol",
    "## PART II — Application Design Concepts",
    "### Part II — Section Index",
    "### §II.1 Application Architecture Overview",
    "### §II.2 DAG Engine Design",
    "### §II.3 Node CRUD and Editing Surface",
    "### §II.4 Validation and Schema Enforcement",
    "### §II.5 Extension System Integration",
    "### §II.6 AI and Agentic Interface",
    "## PART III — Open-Source Library Candidates",
    "### Part III — Section Index",
    "### §III.1 DAG and Graph Engine Libraries",
    "### §III.2 Graph Visualization Libraries",
    "### §III.3 YAML / JSON Schema Validation",
    "### §III.4 Desktop GUI Frameworks",
    "### §III.5 File-System Watching and Event Handling",
    "### §III.6 Serialization and Data Modeling",
    "### §III.7 CLI Frameworks",
]

TABLE_HEADINGS = [
    "#### 2.1 Part Registry",
    "#### 3.1 Common Fields (All Entry Types)",
    "#### 3.2 Idea Entry (TYPE: IDEA)",
    "#### 3.3 Library Candidate Entry (TYPE: LIB)",
    "#### 3.4 Category Taxonomy",
    "#### 3.5 Entry Status Vocabulary",
    "#### 3.6 Priority Vocabulary",
    "### Part II — Section Index",
    "### Part III — Section Index",
]

PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}")
ENTRY_BLOCK_RE = re.compile(
    r"^#### \[(?P<id>BRAIN-(?P<part>II|III)-(?P<num>\d{3}))\] (?P<title>.+?)\n```yaml\n(?P<body>.*?)\n```",
    re.MULTILINE | re.DOTALL,
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

CATEGORIES = {
    "CAT-ARCH",
    "CAT-DAG",
    "CAT-VIZ",
    "CAT-CRUD",
    "CAT-VALID",
    "CAT-STORE",
    "CAT-LIFE",
    "CAT-EXT",
    "CAT-UX",
    "CAT-DIST",
    "CAT-AI",
    "CAT-TEST",
    "CAT-MISC",
}
STATUSES = {"SEED", "EXPLORING", "CANDIDATE", "PROMOTED", "REJECTED", "PARKED", "SUPERSEDED"}
PRIORITIES = {"HIGH", "MED", "LOW", "PARKED"}
TIERS = {"XPD", "SIL", "GPCL", "FCL", "CL", "SAL", "ICL", "CDL", "ISL"}
EXTENSIONS = {"E1", "E2", "E3", "E4", "E5", "E6", "E7", "E8", "E9"}
LANGUAGES = {"Python", "JavaScript", "Rust", "Go", "Other"}
LICENSES = {"MIT", "Apache-2.0", "BSD-2-Clause", "BSD-3-Clause", "ISC", "MPL-2.0", "LGPL", "Other"}
COMMERCIAL_USE = {"YES", "CONDITIONAL", "NO"}
MAINTENANCE = {"ACTIVE", "MAINTAINED", "SLOW", "ARCHIVED"}
MATURITY = {"EXPERIMENTAL", "STABLE", "MATURE", "LEGACY"}
VERDICTS = {"CANDIDATE", "UNDER_REVIEW", "ACCEPTED", "REJECTED", "PARKED"}

COMMON_FIELDS = {
    "entry_type",
    "entry_id",
    "title",
    "category",
    "priority",
    "status",
    "authored_by",
    "authored_date",
    "revised_date",
    "description",
    "detail",
    "open_questions",
    "tags",
    "ddr_relevance",
    "references",
}
IDEA_FIELDS = {"motivation", "prior_art", "ddr_constraints", "risks", "dependencies"}
LIB_FIELDS = {
    "repository",
    "language",
    "license",
    "commercial_use",
    "latest_release",
    "maintenance",
    "install_size_kb",
    "maturity",
    "verdict",
    "rejection_reason",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Validate a brainstorm markdown document.")
    parser.add_argument("path", help="Path to the brainstorm markdown file.")
    parser.add_argument(
        "--baseline",
        help="Optional baseline brainstorm file used to enforce append-only ID preservation.",
    )
    parser.add_argument(
        "--seed",
        default=str(DEFAULT_SEED),
        help="Canonical seed file used to enforce preservation of seeded entries.",
    )
    return parser.parse_args()


def read_text(path_str: str) -> tuple[Path, str]:
    path = (REPO_ROOT / path_str).resolve() if not Path(path_str).is_absolute() else Path(path_str)
    return path, path.read_text(encoding="utf-8")


def ensure_headings(content: str, errors: list[str]) -> None:
    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"Missing required heading: {heading}")


def ensure_tables(content: str, errors: list[str]) -> None:
    lines = content.splitlines()
    for heading in TABLE_HEADINGS:
        try:
            index = lines.index(heading)
        except ValueError:
            continue
        found = False
        for line in lines[index + 1 :]:
            if line.startswith("#"):
                break
            if line.strip().startswith("|"):
                found = True
                break
        if not found:
            errors.append(f"Missing markdown table below heading: {heading}")


def parse_entries(content: str) -> list[dict[str, Any]]:
    entries: list[dict[str, Any]] = []
    for match in ENTRY_BLOCK_RE.finditer(content):
        data = yaml.safe_load(match.group("body"))
        if not isinstance(data, dict):
            raise ValueError(f"{match.group('id')} YAML block must parse to a mapping")
        entries.append(
            {
                "id": match.group("id"),
                "part": match.group("part"),
                "number": int(match.group("num")),
                "title": match.group("title").strip(),
                "start": match.start(),
                "data": data,
            }
        )
    return entries


def validate_metadata_table(content: str, errors: list[str]) -> None:
    required_rows = [
        "| Document ID | DDR-BRAIN-001 |",
        "| Schema | BRAIN-ENTRY-1.0 |",
        "| Created |",
        "| Last Revised |",
        "| Reference Source |",
    ]
    for row in required_rows:
        if row not in content:
            errors.append(f"Missing metadata table row containing: {row}")


def validate_entry_common(entry: dict[str, Any], errors: list[str]) -> None:
    entry_id = entry["id"]
    data = entry["data"]
    missing = sorted(COMMON_FIELDS - set(data.keys()))
    if missing:
        errors.append(f"{entry_id} is missing common field(s): {', '.join(missing)}")
        return

    if data["entry_id"] != entry_id:
        errors.append(f"{entry_id} has mismatched entry_id field: {data['entry_id']}")
    if data["title"] != entry["title"]:
        errors.append(f"{entry_id} title field does not match heading title")
    if data["category"] not in CATEGORIES:
        errors.append(f"{entry_id} uses unknown category: {data['category']}")
    if data["priority"] not in PRIORITIES:
        errors.append(f"{entry_id} uses unknown priority: {data['priority']}")
    if data["status"] not in STATUSES:
        errors.append(f"{entry_id} uses unknown status: {data['status']}")
    for field in ("authored_date", "revised_date"):
        if not is_valid_date_value(data[field]):
            errors.append(f"{entry_id} field {field} must be YYYY-MM-DD")
    for field in ("description", "detail", "authored_by", "title"):
        if not isinstance(data[field], str) or not data[field].strip():
            errors.append(f"{entry_id} field {field} must be a non-empty string")
    for field in ("open_questions", "tags", "ddr_relevance", "references"):
        if not isinstance(data[field], list):
            errors.append(f"{entry_id} field {field} must be a list")
    if isinstance(data.get("ddr_relevance"), list):
        invalid = [item for item in data["ddr_relevance"] if item not in TIERS | EXTENSIONS]
        if invalid:
            errors.append(f"{entry_id} has invalid ddr_relevance item(s): {', '.join(invalid)}")


def validate_idea(entry: dict[str, Any], errors: list[str]) -> None:
    entry_id = entry["id"]
    data = entry["data"]
    missing = sorted(IDEA_FIELDS - set(data.keys()))
    if missing:
        errors.append(f"{entry_id} is missing IDEA field(s): {', '.join(missing)}")
        return
    if data.get("entry_type") != "IDEA":
        errors.append(f"{entry_id} must declare entry_type IDEA")
    if not isinstance(data.get("dependencies"), list):
        errors.append(f"{entry_id} field dependencies must be a list")


def validate_lib(entry: dict[str, Any], errors: list[str]) -> None:
    entry_id = entry["id"]
    data = entry["data"]
    missing = sorted(LIB_FIELDS - set(data.keys()))
    if missing:
        errors.append(f"{entry_id} is missing LIB field(s): {', '.join(missing)}")
        return
    if data.get("entry_type") != "LIB":
        errors.append(f"{entry_id} must declare entry_type LIB")
    if data.get("language") not in LANGUAGES:
        errors.append(f"{entry_id} uses unknown language: {data.get('language')}")
    if data.get("license") not in LICENSES:
        errors.append(f"{entry_id} uses unknown license: {data.get('license')}")
    commercial_use = normalize_commercial_use(data.get("commercial_use"))
    if commercial_use not in COMMERCIAL_USE:
        errors.append(f"{entry_id} uses unknown commercial_use: {data.get('commercial_use')}")
    if data.get("maintenance") not in MAINTENANCE:
        errors.append(f"{entry_id} uses unknown maintenance: {data.get('maintenance')}")
    if data.get("maturity") not in MATURITY:
        errors.append(f"{entry_id} uses unknown maturity: {data.get('maturity')}")
    if data.get("verdict") not in VERDICTS:
        errors.append(f"{entry_id} uses unknown verdict: {data.get('verdict')}")


def validate_part_placement(content: str, entries: list[dict[str, Any]], errors: list[str]) -> None:
    part_ii_start = content.find("## PART II — Application Design Concepts")
    part_iii_start = content.find("## PART III — Open-Source Library Candidates")
    if part_ii_start == -1 or part_iii_start == -1:
        return
    for entry in entries:
        position = entry["start"]
        if entry["part"] == "II":
            if not (part_ii_start < position < part_iii_start):
                errors.append(f"{entry['id']} is outside Part II")
        if entry["part"] == "III":
            if not (part_iii_start < position):
                errors.append(f"{entry['id']} is outside Part III")


def validate_sequence(entries: list[dict[str, Any]], errors: list[str]) -> None:
    for part in ("II", "III"):
        numbers = sorted(entry["number"] for entry in entries if entry["part"] == part)
        if not numbers:
            errors.append(f"No entries found for Part {part}")
            continue
        expected = list(range(1, numbers[-1] + 1))
        if numbers != expected:
            errors.append(f"Part {part} entry IDs must be sequential without gaps: found {numbers}")


def validate_duplicates(entries: list[dict[str, Any]], errors: list[str]) -> None:
    ids = [entry["id"] for entry in entries]
    duplicates = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
    if duplicates:
        errors.append(f"Duplicate entry IDs found: {', '.join(duplicates)}")


def parse_seed_ids(path: Path) -> set[str]:
    content = path.read_text(encoding="utf-8")
    return {match.group("id") for match in ENTRY_BLOCK_RE.finditer(content)}


def validate_append_only(entries: list[dict[str, Any]], seed_path: Path, baseline_path: Path | None, errors: list[str]) -> None:
    current_ids = {entry["id"] for entry in entries}
    seed_ids = parse_seed_ids(seed_path)
    missing_seed = sorted(seed_ids - current_ids)
    if missing_seed:
        errors.append(f"Missing canonical seeded entry IDs: {', '.join(missing_seed)}")
    if baseline_path is not None:
        baseline_ids = parse_seed_ids(baseline_path)
        missing_baseline = sorted(baseline_ids - current_ids)
        if missing_baseline:
            errors.append(f"Missing baseline entry IDs: {', '.join(missing_baseline)}")


def is_valid_date_value(value: Any) -> bool:
    if isinstance(value, str):
        return bool(DATE_RE.match(value))
    if isinstance(value, datetime):
        return bool(DATE_RE.match(value.date().isoformat()))
    if isinstance(value, date):
        return bool(DATE_RE.match(value.isoformat()))
    return False


def normalize_commercial_use(value: Any) -> Any:
    if value is True:
        return "YES"
    if value is False:
        return "NO"
    return value


def validate_brainstorm(path: Path, seed_path: Path, baseline_path: Path | None = None) -> list[str]:
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if PLACEHOLDER_RE.search(content):
        errors.append("Document contains unresolved placeholders")

    validate_metadata_table(content, errors)
    ensure_headings(content, errors)
    ensure_tables(content, errors)

    try:
        entries = parse_entries(content)
    except ValueError as exc:
        return errors + [str(exc)]

    validate_duplicates(entries, errors)
    validate_sequence(entries, errors)
    validate_part_placement(content, entries, errors)
    validate_append_only(entries, seed_path, baseline_path, errors)

    for entry in entries:
        validate_entry_common(entry, errors)
        if entry["part"] == "II":
            validate_idea(entry, errors)
        if entry["part"] == "III":
            validate_lib(entry, errors)

    return errors


def main() -> int:
    args = parse_args()
    path, _ = read_text(args.path)
    seed_path, _ = read_text(args.seed)
    baseline_path = None
    if args.baseline:
        baseline_path, _ = read_text(args.baseline)

    errors = validate_brainstorm(path, seed_path, baseline_path)
    if errors:
        print(f"INVALID {path}")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"VALID {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

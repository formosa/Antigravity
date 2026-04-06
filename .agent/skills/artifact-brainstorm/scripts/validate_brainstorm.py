#!/usr/bin/env python3
"""
Validate brainstorm.md documents managed by artifact-brainstorm.

role: brainstorm validation engine
entrypoints: main
reads: brainstorm.md, brainstorm seed
writes: stdout
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors; schema violations
coupling: coupled to brainstorm schema and seed structure
determinism: input-dependent
concurrency: not thread-safe; process-local
"""

from __future__ import annotations

import argparse
import re
from datetime import date, datetime
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml


REPO_ROOT = Path(__file__).resolve().parents[4]
DEFAULT_SEED = REPO_ROOT / ".agent" / "schemas" / "brainstorm" / "seed.md"

REQUIRED_HEADINGS = [
    "## PART I — Document Manifest",
    "### §1 Document Purpose and Scope",
    "### §2 Document Structure and Navigation",
    "#### 2.1 Part Registry",
    "### §3 Entry Schema (BRAIN-ENTRY-1.1)",
    "#### 3.1 Common Fields (All Entry Types)",
    "#### 3.2 Idea Entry (TYPE: IDEA)",
    "#### 3.3 Library Candidate Entry (TYPE: LIB)",
    "#### 3.4 Category Taxonomy",
    "#### 3.5 Entry Status Vocabulary",
    "#### 3.6 Priority Vocabulary",
    "### §4 Rules for Adding New Sections",
    "### §5 Governance and Promotion Protocol",
    "### §6 Visual Semantics and Font Color Index",
    "#### 6.1 Font Color Index",
    "### §7 Citation and Research Protocol",
    "#### 7.1 Source Hierarchy",
    "#### 7.2 Citation Freshness Rules",
    "#### 7.3 Citation Application Rules",
    "### §8 Mermaid Diagram Standards",
    "#### 8.1 Supported Mermaid Diagram Types",
    "#### 8.2 Accessibility and Stability Rules",
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
    "### §III.8 Full Target Subsystem Dependencies",
    "### §III.9 Desktop Runtime and IDE Workbench Libraries",
    "### §III.10 Embedded Store, Search, and Telemetry",
    "### §III.11 MCP, Browser, and Agent Automation Assets",
    "### §III.12 Citations and References",
]

TABLE_HEADINGS = [
    "#### 2.1 Part Registry",
    "#### 3.1 Common Fields (All Entry Types)",
    "#### 3.2 Idea Entry (TYPE: IDEA)",
    "#### 3.3 Library Candidate Entry (TYPE: LIB)",
    "#### 3.4 Category Taxonomy",
    "#### 3.5 Entry Status Vocabulary",
    "#### 3.6 Priority Vocabulary",
    "#### 6.1 Font Color Index",
    "#### 8.1 Supported Mermaid Diagram Types",
    "### Part II — Section Index",
    "### Part III — Section Index",
]

PLACEHOLDER_RE = re.compile(r"\{\{[^{}\n]+\}\}")
ENTRY_BLOCK_RE = re.compile(
    r"^#### \[(?P<id>BRAIN-(?P<part>II|III)-(?P<num>\d{3}))\] (?P<title>.+?)\n```yaml\n(?P<body>.*?)\n```",
    re.MULTILINE | re.DOTALL,
)
CITATION_BLOCK_RE = re.compile(
    r"^#### \[(?P<id>C(?P<num>\d+))\] (?P<title>.+?)\n```yaml\n(?P<body>.*?)\n```",
    re.MULTILINE | re.DOTALL,
)
MERMAID_BLOCK_RE = re.compile(r"```mermaid\n(?P<body>.*?)\n```", re.DOTALL)
STYLE_BLOCK_RE = re.compile(r"<style>\n(?P<body>.*?)\n</style>", re.DOTALL)
INLINE_CITATION_RE = re.compile(r"\[(C\d+)\]")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
BRAIN_SPAN_CLASS_RE = re.compile(r'class="([^"]*\bbrain-[^"]*)"')
BRAIN_SELECTOR_RE = re.compile(r"\.(brain-[a-z0-9-]+)")
URL_RE = re.compile(r"https?://")
BRAIN_ID_RE = re.compile(r"^BRAIN-(II|III)-\d{3}$")
ADR_RE = re.compile(r"^ADR[-\s:/#]?[A-Za-z0-9._-]+$")

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
AUTHORITY_TYPES = {
    "OFFICIAL_VENDOR",
    "OFFICIAL_PROJECT",
    "STANDARDS_BODY",
    "GOVERNMENT",
    "ACADEMIC",
    "REPUTABLE_SECONDARY",
}
RECENCY_CLASSES = {"CURRENT", "EVERGREEN", "HISTORICAL"}
SEMANTIC_CLASSES = {
    "brain-governance",
    "brain-evidence",
    "brain-hypothesis",
    "brain-recommendation",
    "brain-risk",
}
STYLE_CLASSES = SEMANTIC_CLASSES | {"brain-badge", "brain-label"}

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
    "citation_ids",
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
CITATION_FIELDS = {
    "citation_id",
    "publisher",
    "title",
    "url",
    "published_date",
    "accessed_date",
    "authority_type",
    "recency_class",
    "support_note",
    "related_entries",
}
IDEA_PROSE_FIELDS = ("description", "detail", "motivation", "prior_art", "ddr_constraints", "risks")
LIB_PROSE_FIELDS = ("description", "detail")


def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for brainstorm validation.

    purpose: CLI configuration extraction
    """
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
    parser.add_argument(
        "--audit",
        action="store_true",
        help="Emit non-fatal audit warnings for citation freshness, diagrams, and visual semantics.",
    )
    return parser.parse_args()


def read_text(path_str: str) -> tuple[Path, str]:
    """
    Read file content and return resolved path and text.

    purpose: file reading helper
    """
    path = (REPO_ROOT / path_str).resolve() if not Path(path_str).is_absolute() else Path(path_str)
    return path, path.read_text(encoding="utf-8")


def ensure_headings(content: str, errors: list[str]) -> None:
    """
    Verify that all required headings are present in the document.

    purpose: structural validation
    """
    for heading in REQUIRED_HEADINGS:
        if heading not in content:
            errors.append(f"Missing required heading: {heading}")


def ensure_tables(content: str, errors: list[str]) -> None:
    """
    Verify that specific headings are followed by markdown tables.

    purpose: structural validation
    """
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
    """
    Extract entries (BRAIN-II/III) from the markdown content.

    purpose: entry extraction
    """
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
                "body": match.group("body"),
                "data": data,
            }
        )
    return entries


def parse_citations(content: str) -> list[dict[str, Any]]:
    """
    Extract citations (C*) from the markdown content.

    purpose: citation extraction
    """
    citations: list[dict[str, Any]] = []
    for match in CITATION_BLOCK_RE.finditer(content):
        data = yaml.safe_load(match.group("body"))
        if not isinstance(data, dict):
            raise ValueError(f"{match.group('id')} YAML block must parse to a mapping")
        citations.append(
            {
                "id": match.group("id"),
                "number": int(match.group("num")),
                "title": match.group("title").strip(),
                "start": match.start(),
                "data": data,
            }
        )
    return citations


def validate_metadata_table(content: str, errors: list[str]) -> None:
    """
    Verify the contents of the document metadata table.

    purpose: manifest validation
    """
    required_pairs = [
        ("Document ID", "DDR-BRAIN-001"),
        ("Schema", "BRAIN-ENTRY-1.1"),
        ("Created", None),
        ("Last Revised", None),
        ("Reference Source", None),
    ]
    lines = [line.strip() for line in content.splitlines() if line.strip().startswith("|")]
    for key, required_value in required_pairs:
        matched = False
        for line in lines:
            if key not in line:
                continue
            if required_value is not None and required_value not in line:
                continue
            matched = True
            break
        if not matched:
            if required_value is None:
                errors.append(f"Missing metadata table row containing key: {key}")
            else:
                errors.append(f"Missing metadata table row containing key/value: {key} / {required_value}")


def validate_style_block(content: str, errors: list[str]) -> None:
    """
    Verify the document-level <style> block and its contents.

    purpose: visual semantics validation
    """
    match = STYLE_BLOCK_RE.search(content)
    if not match:
        errors.append("Missing required document-level <style> block")
        return

    part_i_pos = content.find("## PART I — Document Manifest")
    if part_i_pos != -1 and match.start() > part_i_pos:
        errors.append("Document-level <style> block must appear before Part I")

    style_body = match.group("body")
    required_selectors = {".brain-badge", ".brain-label"} | {f".{class_name}" for class_name in SEMANTIC_CLASSES}
    for selector in required_selectors:
        if selector not in style_body:
            errors.append(f"Missing required style selector: {selector}")

    unknown_classes = sorted({name for name in BRAIN_SELECTOR_RE.findall(style_body) if name not in STYLE_CLASSES})
    if unknown_classes:
        errors.append(f"Unknown brain-* class in style block: {', '.join(unknown_classes)}")


def validate_span_classes(content: str, errors: list[str]) -> None:
    """
    Verify all brain-* classes used in <span> elements within the document.

    purpose: visual semantics validation
    """
    unknown_classes: set[str] = set()
    for match in BRAIN_SPAN_CLASS_RE.finditer(content):
        for class_name in match.group(1).split():
            if class_name.startswith("brain-") and class_name not in STYLE_CLASSES:
                unknown_classes.add(class_name)
    if unknown_classes:
        errors.append(f"Unknown brain-* class used in document: {', '.join(sorted(unknown_classes))}")


def validate_entry_common(entry: dict[str, Any], citations: dict[str, dict[str, Any]], errors: list[str]) -> None:
    """
    Validate common fields and logic for all entry types (IDEA, LIB).

    purpose: common schema validation
    """
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

    for field in ("open_questions", "tags", "ddr_relevance", "citation_ids", "references"):
        if not isinstance(data[field], list):
            errors.append(f"{entry_id} field {field} must be a list")

    if isinstance(data.get("ddr_relevance"), list):
        invalid = [item for item in data["ddr_relevance"] if item not in TIERS | EXTENSIONS]
        if invalid:
            errors.append(f"{entry_id} has invalid ddr_relevance item(s): {', '.join(invalid)}")

    citation_ids = data.get("citation_ids", [])
    if isinstance(citation_ids, list):
        invalid_citation_ids = [item for item in citation_ids if not isinstance(item, str) or not re.fullmatch(r"C\d+", item)]
        if invalid_citation_ids:
            errors.append(f"{entry_id} has invalid citation_ids item(s): {', '.join(map(str, invalid_citation_ids))}")
        if len(set(citation_ids)) != len(citation_ids):
            errors.append(f"{entry_id} citation_ids must not contain duplicates")
        if not citation_ids:
            errors.append(f"{entry_id} must declare at least one citation_id")
        for citation_id in citation_ids:
            if citation_id not in citations:
                errors.append(f"{entry_id} references unknown citation_id: {citation_id}")

    if isinstance(data.get("references"), list):
        bad_refs = [ref for ref in data["references"] if is_external_or_citation_ref(ref)]
        if bad_refs:
            errors.append(f"{entry_id} references must not contain external URLs or citation IDs: {', '.join(map(str, bad_refs))}")
        invalid_refs = [ref for ref in data["references"] if not is_valid_internal_reference(ref)]
        if invalid_refs:
            errors.append(f"{entry_id} references contains invalid internal reference(s): {', '.join(map(str, invalid_refs))}")

    inline_markers = collect_entry_inline_citations(data)
    inline_set = set(inline_markers)
    citation_set = set(citation_ids) if isinstance(citation_ids, list) else set()
    if inline_set != citation_set:
        missing_inline = sorted(citation_set - inline_set)
        undeclared = sorted(inline_set - citation_set)
        details: list[str] = []
        if missing_inline:
            details.append(f"missing inline markers for {', '.join(missing_inline)}")
        if undeclared:
            details.append(f"undeclared inline markers {', '.join(undeclared)}")
        errors.append(f"{entry_id} citation_ids must exactly match inline citation markers ({'; '.join(details)})")

    if isinstance(citation_ids, list) and is_valid_date_value(data.get("revised_date")):
        revised_date = coerce_date(data["revised_date"])
        for citation_id in citation_ids:
            citation = citations.get(citation_id)
            if not citation:
                continue
            citation_data = citation["data"]
            if entry_id not in citation_data.get("related_entries", []):
                errors.append(f"{entry_id} is not listed in {citation_id} related_entries")
            if citation_data.get("recency_class") == "CURRENT":
                published_date = coerce_date(citation_data["published_date"])
                if abs((revised_date - published_date).days) > 183:
                    errors.append(
                        f"{entry_id} cites {citation_id} as CURRENT but {citation_id} is more than 183 days from the entry revised_date"
                    )


def validate_idea(entry: dict[str, Any], errors: list[str]) -> None:
    """
    Validate fields specific to IDEA type entries.

    purpose: IDEA schema validation
    """
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
    """
    Validate fields specific to LIB type entries.

    purpose: LIB schema validation
    """
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
    repository = data.get("repository")
    if not isinstance(repository, str) or not is_valid_url(repository):
        errors.append(f"{entry_id} repository must be a valid URL")


def validate_citations(citations: list[dict[str, Any]], entry_ids: set[str], errors: list[str]) -> dict[str, dict[str, Any]]:
    """
    Validate the citation catalog and return a map of valid citations.

    purpose: citation schema validation
    """
    if not citations:
        errors.append("No citations found in §III.12 Citations and References")
        return {}

    ids = [citation["id"] for citation in citations]
    duplicates = sorted({citation_id for citation_id in ids if ids.count(citation_id) > 1})
    if duplicates:
        errors.append(f"Duplicate citation IDs found: {', '.join(duplicates)}")

    citation_map: dict[str, dict[str, Any]] = {}
    for citation in citations:
        citation_id = citation["id"]
        data = citation["data"]
        citation_map[citation_id] = citation
        missing = sorted(CITATION_FIELDS - set(data.keys()))
        if missing:
            errors.append(f"{citation_id} is missing citation field(s): {', '.join(missing)}")
            continue
        if data["citation_id"] != citation_id:
            errors.append(f"{citation_id} has mismatched citation_id field: {data['citation_id']}")
        if data["title"] != citation["title"]:
            errors.append(f"{citation_id} title field does not match heading title")
        for field in ("publisher", "title", "url", "support_note"):
            if not isinstance(data[field], str) or not data[field].strip():
                errors.append(f"{citation_id} field {field} must be a non-empty string")
        for field in ("published_date", "accessed_date"):
            if not is_valid_date_value(data[field]):
                errors.append(f"{citation_id} field {field} must be YYYY-MM-DD")
        if not is_valid_url(data.get("url")):
            errors.append(f"{citation_id} field url must be a valid URL")
        if data.get("authority_type") not in AUTHORITY_TYPES:
            errors.append(f"{citation_id} uses unknown authority_type: {data.get('authority_type')}")
        if data.get("recency_class") not in RECENCY_CLASSES:
            errors.append(f"{citation_id} uses unknown recency_class: {data.get('recency_class')}")
        if not isinstance(data.get("related_entries"), list):
            errors.append(f"{citation_id} field related_entries must be a list")
        elif any(not isinstance(item, str) or not BRAIN_ID_RE.fullmatch(item) for item in data["related_entries"]):
            errors.append(f"{citation_id} related_entries must contain only brainstorm entry IDs")
        else:
            unknown_entries = sorted(set(data["related_entries"]) - entry_ids)
            if unknown_entries:
                errors.append(f"{citation_id} related_entries references unknown entry ID(s): {', '.join(unknown_entries)}")
    return citation_map


def validate_part_placement(content: str, entries: list[dict[str, Any]], errors: list[str]) -> None:
    """
    Verify that entries are located in the correct Markdown part sections.

    purpose: location validation
    """
    part_ii_start = content.find("## PART II — Application Design Concepts")
    part_iii_start = content.find("## PART III — Open-Source Library Candidates")
    citations_start = content.find("### §III.12 Citations and References")
    if part_ii_start == -1 or part_iii_start == -1 or citations_start == -1:
        return
    for entry in entries:
        position = entry["start"]
        if entry["part"] == "II" and not (part_ii_start < position < part_iii_start):
            errors.append(f"{entry['id']} is outside Part II")
        if entry["part"] == "III" and not (part_iii_start < position < citations_start):
            errors.append(f"{entry['id']} is outside Part III library sections")


def validate_sequence(entries: list[dict[str, Any]], errors: list[str]) -> None:
    """
    Verify that entry IDs are sequential without gaps within each part.

    purpose: identifier sequence validation
    """
    for part in ("II", "III"):
        numbers = sorted(entry["number"] for entry in entries if entry["part"] == part)
        if not numbers:
            errors.append(f"No entries found for Part {part}")
            continue
        expected = list(range(1, numbers[-1] + 1))
        if numbers != expected:
            errors.append(f"Part {part} entry IDs must be sequential without gaps: found {numbers}")


def validate_duplicates(entries: list[dict[str, Any]], errors: list[str]) -> None:
    """
    Verify that entry IDs are unique within the document.

    purpose: identifier uniqueness validation
    """
    ids = [entry["id"] for entry in entries]
    duplicates = sorted({entry_id for entry_id in ids if ids.count(entry_id) > 1})
    if duplicates:
        errors.append(f"Duplicate entry IDs found: {', '.join(duplicates)}")


def parse_seed_ids(path: Path) -> set[str]:
    """
    Parse entry IDs from a reference (seed or baseline) file.

    purpose: identifier collection
    """
    content = path.read_text(encoding="utf-8")
    return {match.group("id") for match in ENTRY_BLOCK_RE.finditer(content)}


def validate_append_only(entries: list[dict[str, Any]], seed_path: Path, baseline_path: Path | None, errors: list[str]) -> None:
    """
    Verify that no previously existing IDs have been removed.

    purpose: preservation validation
    """
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


def validate_mermaid(content: str, errors: list[str]) -> list[dict[str, Any]]:
    """
    Verify Mermaid diagram blocks for type support and accessibility metadata.

    purpose: diagram validation
    """
    blocks: list[dict[str, Any]] = []
    for index, match in enumerate(MERMAID_BLOCK_RE.finditer(content), start=1):
        body = match.group("body")
        blocks.append({"index": index, "body": body, "start": match.start()})
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        if not lines:
            errors.append(f"Mermaid block {index} is empty")
            continue
        diagram_type = lines[0]
        if not diagram_type.startswith(("flowchart", "sequenceDiagram", "stateDiagram-v2", "classDiagram", "erDiagram")):
            errors.append(f"Mermaid block {index} uses an unsupported diagram type: {diagram_type}")
        if not any(line.startswith("accTitle:") for line in lines):
            errors.append(f"Mermaid block {index} must include accTitle")
        if not any(line.startswith("accDescr:") for line in lines):
            errors.append(f"Mermaid block {index} must include accDescr")
        disallowed = [
            token
            for token in ("architecture-beta", "mindmap", "timeline", "journey", "sankey-beta", "xychart-beta", "gantt")
            if token in body
        ]
        if disallowed:
            errors.append(f"Mermaid block {index} uses disallowed Mermaid features: {', '.join(disallowed)}")
    return blocks


def validate_brainstorm(path: Path, seed_path: Path, baseline_path: Path | None = None) -> list[str]:
    """
    Perform a full validation of a brainstorm markdown document.

    purpose: full validation workflow
    """
    content = path.read_text(encoding="utf-8")
    errors: list[str] = []

    if PLACEHOLDER_RE.search(content):
        errors.append("Document contains unresolved placeholders")

    validate_metadata_table(content, errors)
    ensure_headings(content, errors)
    ensure_tables(content, errors)
    validate_style_block(content, errors)
    validate_span_classes(content, errors)
    validate_mermaid(content, errors)

    try:
        entries = parse_entries(content)
        citations = parse_citations(content)
    except ValueError as exc:
        return errors + [str(exc)]

    validate_duplicates(entries, errors)
    validate_sequence(entries, errors)
    validate_part_placement(content, entries, errors)
    validate_append_only(entries, seed_path, baseline_path, errors)

    entry_ids = {entry["id"] for entry in entries}
    citation_map = validate_citations(citations, entry_ids, errors)

    for entry in entries:
        validate_entry_common(entry, citation_map, errors)
        if entry["part"] == "II":
            validate_idea(entry, errors)
        if entry["part"] == "III":
            validate_lib(entry, errors)

    return errors


def audit_brainstorm(path: Path) -> list[str]:
    """
    Perform audit checks for non-fatal brainstorm quality issues.

    purpose: audit workflow
    """
    content = path.read_text(encoding="utf-8")
    warnings: list[str] = []
    entries = parse_entries(content)
    citations = parse_citations(content)
    citation_map = {citation["id"]: citation for citation in citations}
    mermaid_blocks = list(MERMAID_BLOCK_RE.finditer(content))

    for entry in entries:
        data = entry["data"]
        entry_id = entry["id"]
        citation_ids = [citation_id for citation_id in data.get("citation_ids", []) if citation_id in citation_map]
        if citation_ids:
            has_current = any(citation_map[citation_id]["data"].get("recency_class") == "CURRENT" for citation_id in citation_ids)
            if not has_current:
                warnings.append(f"{entry_id} has no CURRENT citation support")
        for field in prose_fields_for_entry(data):
            value = data.get(field)
            if isinstance(value, str) and len(value.split()) >= 18 and not INLINE_CITATION_RE.search(value):
                warnings.append(f"{entry_id} field {field} appears substantive but has no inline citation marker")

    used_citations = {
        citation_id
        for entry in entries
        for citation_id in set(data_id for data_id in entry["data"].get("citation_ids", []))
        if citation_id in citation_map
    }
    orphaned = sorted(set(citation_map) - used_citations)
    for citation_id in orphaned:
        warnings.append(f"{citation_id} is orphaned in the citation catalog")

    used_semantic_classes = {
        class_name
        for match in BRAIN_SPAN_CLASS_RE.finditer(content)
        for class_name in match.group(1).split()
        if class_name in SEMANTIC_CLASSES
    }
    unused_semantic = sorted(SEMANTIC_CLASSES - used_semantic_classes)
    for class_name in unused_semantic:
        warnings.append(f"Visual semantic class is defined but unused: {class_name}")

    if len(mermaid_blocks) < 2:
        warnings.append("Document has fewer than 2 Mermaid diagrams; add diagrams to high-complexity sections")

    return warnings


def prose_fields_for_entry(data: dict[str, Any]) -> tuple[str, ...]:
    """
    Return the names of substantive prose fields for the given entry type.

    purpose: metadata helper
    """
    entry_type = data.get("entry_type")
    if entry_type == "IDEA":
        return IDEA_PROSE_FIELDS
    if entry_type == "LIB":
        return LIB_PROSE_FIELDS
    return ()


def collect_entry_inline_citations(data: dict[str, Any]) -> list[str]:
    """
    Extract citation markers ([C1], [C2], ...) from entry prose.

    purpose: citation marker extraction
    """
    markers: set[str] = set()
    for field in prose_fields_for_entry(data):
        value = data.get(field)
        if isinstance(value, str):
            markers.update(INLINE_CITATION_RE.findall(value))
    return sorted(markers, key=citation_sort_key)


def is_valid_date_value(value: Any) -> bool:
    """
    Check if a value represents a valid ISO 8601 date.

    purpose: date format validation
    """
    if isinstance(value, str):
        return bool(DATE_RE.fullmatch(value))
    if isinstance(value, datetime):
        return bool(DATE_RE.fullmatch(value.date().isoformat()))
    if isinstance(value, date):
        return bool(DATE_RE.fullmatch(value.isoformat()))
    return False


def coerce_date(value: Any) -> date:
    """
    Safely convert string or datetime values to a date object.

    purpose: date coercion
    """
    if isinstance(value, datetime):
        return value.date()
    if isinstance(value, date):
        return value
    if isinstance(value, str) and DATE_RE.fullmatch(value):
        return date.fromisoformat(value)
    raise ValueError(f"Cannot coerce value to date: {value!r}")


def normalize_commercial_use(value: Any) -> Any:
    """
    Normalize boolean or string commercial_use values to the vocabulary.

    purpose: commercial use normalization
    """
    if value is True:
        return "YES"
    if value is False:
        return "NO"
    return value


def is_valid_url(value: Any) -> bool:
    """
    Verify that a value is a valid HTTP/HTTPS URL string.

    purpose: URL validation
    """
    if not isinstance(value, str) or not value.strip():
        return False
    parsed = urlparse(value)
    return parsed.scheme in {"http", "https"} and bool(parsed.netloc)


def is_external_or_citation_ref(value: Any) -> bool:
    """
    Check if a reference string is an external URL or a citation ID.

    purpose: reference classification
    """
    return isinstance(value, str) and (bool(URL_RE.search(value)) or bool(re.fullmatch(r"C\d+", value)))


def is_valid_internal_reference(value: Any) -> bool:
    """
    Verify that a reference string adheres to allowed internal patterns.

    purpose: project-internal reference validation
    """
    if not isinstance(value, str) or not value.strip():
        return False
    if BRAIN_ID_RE.fullmatch(value):
        return True
    if ADR_RE.fullmatch(value):
        return True
    if value.startswith("DDR System"):
        return True
    if value.endswith((".md", ".yaml", ".yml", ".json", ".txt", ".py", ".ts")):
        return True
    if "/" in value or "\\" in value:
        return True
    return False


def citation_sort_key(value: str) -> int:
    """
    Provide a numeric key for sorting citation IDs (C1, C10, C2).

    purpose: sorting helper
    """
    match = re.fullmatch(r"C(\d+)", value)
    return int(match.group(1)) if match else 10**9


def main() -> int:
    """
    Execute the brainstorm validation CLI.

    purpose: entrypoint
    """
    args = parse_args()
    path, _ = read_text(args.path)
    seed_path, _ = read_text(args.seed)
    baseline_path = None
    if args.baseline:
        baseline_path, _ = read_text(args.baseline)

    errors = validate_brainstorm(path, seed_path, baseline_path)
    warnings: list[str] = []
    if args.audit:
        warnings = audit_brainstorm(path)

    if errors:
        print(f"INVALID {path}")
        for error in errors:
            print(f"- {error}")
        if warnings:
            print(f"AUDIT {path}")
            for warning in warnings:
                print(f"- {warning}")
        return 1

    print(f"VALID {path}")
    if warnings:
        print(f"AUDIT {path}")
        for warning in warnings:
            print(f"- {warning}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

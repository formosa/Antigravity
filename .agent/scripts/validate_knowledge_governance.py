"""
Validate Knowledge Governance Tool.

Validates DDR knowledge files against the metadata schema and governance policies.
Scope: .agent/knowledge/sources/** and .agent/knowledge/context/**

Checks:
1. Frontmatter existence and validity (Simple Parser)
2. Required fields (archetype, status, version, created, updated)
3. Enum conformance (archetype, status)
4. Path prohibition (no `../` in metadata)
5. Source citation conformance (canonical format)
6. Index file policy

Usage:
    python validate_knowledge_governance.py
"""
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

# --- Configuration ---
ROOT_DIR = Path(__file__).parent.parent / "knowledge"
REQUIRED_FIELDS = ["archetype", "status", "version", "created", "updated"]
VALID_ARCHETYPES = [
    "concept", "protocol", "constraint", "pattern", "vocabulary", "context", "index"
]
VALID_STATUSES = ["draft", "review", "active", "deprecated"]

CANONICAL_SOURCE_REGEX = re.compile(
    r"^- Source: `?\.?\.agent/assets/documentation_system\.md`? §.*", re.MULTILINE
)

PATH_PROHIBITED = "../"

def parse_frontmatter(content: str) -> Dict[str, Any]:
    """Extracts and parses simple YAML frontmatter without PyYAML."""
    if not content.startswith("---\n"):
        return {}

    try:
        parts = content.split("---", 2)
        if len(parts) < 3:
            return {}

        fm_text = parts[1]
        data = {}
        current_list_key = None

        for line in fm_text.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            if line.startswith("- "):
                # List item
                if current_list_key:
                    val = line[2:].strip()
                    if current_list_key not in data:
                        data[current_list_key] = []
                    data[current_list_key].append(val)
                continue

            if ":" in line:
                key, val = line.split(":", 1)
                key = key.strip()
                val = val.strip()

                if val == "" or val == "[]":
                    current_list_key = key
                    data[key] = [] # Initialize empty list
                else:
                    current_list_key = None
                    # Handle basic types
                    if val.startswith("[") and val.endswith("]"):
                         # inline list
                         items = [x.strip() for x in val[1:-1].split(",")]
                         data[key] = [i for i in items if i]
                    else:
                        data[key] = val

        return data
    except Exception:
        return {}

def validate_file(path: Path) -> List[str]:
    errors = []
    try:
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()
    except Exception as e:
        return [f"Could not read file: {e}"]

    # 1. Frontmatter Check
    if path.name == "README.md":
        return errors

    fm = parse_frontmatter(content)
    # Minimal check: must have archetype if supposed to
    if not fm:
        if path.name == "_index.md" or path.suffix == ".md":
            errors.append("Missing or invalid YAML frontmatter")
        return errors

    # 2. Required Fields (skip strict required check for _index.md? Plan says: "Index Policy: all _index.md files... require minimal frontmatter".
    # But schema says specific fields for all.
    # Let's apply stricter check for now and see failures.

    # Special handling for _index.md: check minimal fields or archetype
    # But metadata_schema.md lists required fields for ALL.
    for field in REQUIRED_FIELDS:
        if field not in fm:
            errors.append(f"Missing required field: '{field}'")

    # 3. Enum Checks
    if "archetype" in fm and fm["archetype"] not in VALID_ARCHETYPES:
        errors.append(f"Invalid archetype: '{fm['archetype']}'")

    if "status" in fm and fm["status"] not in VALID_STATUSES:
        errors.append(f"Invalid status: '{fm['status']}'")

    # 4. Path Checks (requires/related)
    for list_field in ["requires", "related"]:
        if list_field in fm and isinstance(fm[list_field], list):
            for ref in fm[list_field]:
                if PATH_PROHIBITED in ref:
                    errors.append(f"Prohibited relative path '../' in '{list_field}': {ref}")

    # 5. Source Citation Check (Body)
    # Only check if "Source:" is present in body
    # Using regex search for flexible match

    # Exempt the style definition file itself
    if path.name == "source_citation_style.md":
        return errors

    body = content.split("---", 2)[-1] if len(content.split("---", 2)) >= 3 else content

    for line in body.splitlines():
        if line.strip().startswith("- Source:"):
            # Check for canonical path
            if ".agent/assets/documentation_system.md" not in line:
                 errors.append(f"Non-canonical Source citation: '{line.strip()}'")

    # 6. Index Policy
    if path.name == "_index.md":
        if fm.get("archetype") != "index":
            errors.append("Index file must have archetype 'index'")

    return errors


def main():
    script_dir = Path(__file__).parent
    knowledge_dir = script_dir.parent / "knowledge"
    report_file = script_dir.parent / "validation_report.txt"

    output_lines = []
    def log(msg):
        print(msg)
        output_lines.append(msg)

    log(f"Scanning knowledge repository: {knowledge_dir}")
    if not knowledge_dir.exists():
        log(f"Error: Directory not found: {knowledge_dir}")
        sys.exit(1)

    all_errors = {}
    files_scanned = 0

    # Walk sources and context
    for subdir in ["sources", "context"]:
        search_dir = knowledge_dir / subdir
        if not search_dir.exists():
            continue

        for root, _, files in os.walk(search_dir):
            for file in files:
                if not file.endswith(".md"):
                    continue

                full_path = Path(root) / file
                try:
                    rel_path = full_path.relative_to(knowledge_dir)
                except ValueError:
                    rel_path = full_path
                files_scanned += 1

                file_errors = validate_file(full_path)
                if file_errors:
                    all_errors[str(rel_path)] = file_errors

    # Also check root _index.md
    root_index = knowledge_dir / "_index.md"
    if root_index.exists():
        files_scanned += 1
        errs = validate_file(root_index)
        if errs:
            all_errors["_index.md"] = errs

    log(f"\nScanned {files_scanned} files.")

    if all_errors:
        log(f"Found violations in {len(all_errors)} files:")
        for fpath, errs in all_errors.items():
            log(f"\n[FAIL] {fpath}")
            for e in errs:
                log(f"  - {e}")

        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        sys.exit(1)
    else:
        log("\n[SUCCESS] All files conform to governance schema.")
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("\n".join(output_lines))
        sys.exit(0)

if __name__ == "__main__":
    main()

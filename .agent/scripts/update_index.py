"""
Regenerate governed root and tests script indexes in .agent/scripts/.

role: documentation and discovery maintenance script
entrypoints: main
reads: .agent/scripts/, .agent/scripts/tests/, .agent/tools/
writes: .agent/scripts/index.md, .agent/scripts/tests/index.md
external_io: fs
state_model: stateless
failure_surface: fs access errors; yaml parsing errors
coupling: coupled to .agent folder structure and tool definition schema
determinism: input-dependent (filesystem state)
concurrency: not thread-safe; process-local
"""

#!/usr/bin/env python3
from __future__ import annotations

import ast
import re
from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(frozen=True)
class ScriptRecord:
    """
    Data container for a script's metadata used in index generation.

    role: value object for script metadata
    lifecycle: transient; constructed during index build
    mutability: immutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal

    Attributes
    ----------
    script_id : str
        unique identifier derived from stem
    filename : str
        basename of the script
    relative_path : str
        repo-relative path
    category : str
        assigned classification
    description : str
        semantic summary
    tool_definition : str | None
        path to linked tool definition if any
    """
    script_id: str
    filename: str
    relative_path: str
    category: str
    description: str
    tool_definition: str | None = None


REPO_ROOT = Path(__file__).resolve().parents[2]
SCRIPTS_DIR = REPO_ROOT / ".agent" / "scripts"
TESTS_DIR = SCRIPTS_DIR / "tests"
TOOLS_DIR = REPO_ROOT / ".agent" / "tools"
ROOT_INDEX_PATH = SCRIPTS_DIR / "index.md"
TESTS_INDEX_PATH = TESTS_DIR / "index.md"
SKIP_FILENAMES = {"__init__.py", "index.md"}


def normalize_sentence(value: str) -> str:
    """
    Collapse internal whitespace and strip leading/trailing spaces.

    purpose: string normalization
    preconditions: none
    postconditions: space-normalized string
    mutates: none
    reads: input string
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    value : str
        input text

    Returns
    -------
    str
        normalized text
    """
    return " ".join(value.split())


def read_text(path: Path) -> str:
    """
    Read file content as UTF-8 string.

    purpose: file reading helper
    preconditions: path must exist and be readable
    postconditions: returns file content
    mutates: none
    reads: filesystem
    writes: none
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        target file path

    Returns
    -------
    str
        file content
    """
    return path.read_text(encoding="utf-8")


def extract_docstring_summary(path: Path) -> str | None:
    """
    Parse Python module and extract the first meaningful line of its docstring.

    purpose: metadata extraction
    preconditions: path should exist and be a valid Python file
    postconditions: returns summary string or None
    mutates: none
    reads: filesystem; AST structure
    writes: none
    external_io: fs
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: ast.parse execution
    coupling: minimal

    Parameters
    ----------
    path : Path
        Python script path

    Returns
    -------
    str | None
        extracted summary or None if extraction fails
    """
    try:
        module = ast.parse(read_text(path))
    except (SyntaxError, OSError, UnicodeDecodeError):
        return None

    docstring = ast.get_docstring(module)
    if not docstring:
        return None

    basename = path.name.lower()
    stem = path.stem.lower()
    for raw_line in docstring.splitlines():
        line = raw_line.strip()
        lowered = line.lower()
        if not line:
            continue
        if re.fullmatch(r"[=\-`~:#*]+", line):
            continue
        if lowered in {basename, stem}:
            continue
        return normalize_sentence(line)
    return None


def fallback_description(path: Path, *, is_test_index: bool) -> str:
    """
    Provide a default description based on filename and context.

    purpose: default description generation
    preconditions: none
    postconditions: returns descriptive string
    mutates: none
    reads: path property
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        script path
    is_test_index : bool
        true if script resides in tests subtree

    Returns
    -------
    str
        fallback description
    """
    name = path.name
    if not is_test_index and name == "cleanup_temp_assets.py":
        return "Audit and optionally clean up stale managed temp run directories."
    if not is_test_index and name == "directory_tree.py":
        return "Generate filtered directory trees with reporting-oriented labels."
    if not is_test_index and name == "generate_uuid.py":
        return "Generate a UUIDv4 string for workflow and temp-path capture."
    if not is_test_index and name == "update_index.py":
        return "Regenerate the governed root and tests script indexes."
    if name.startswith("test_"):
        return f"Unit tests for `{name.removeprefix('test_')}` behavior."
    if name.startswith("validate_"):
        subject = name.removeprefix("validate_").removesuffix(".py").replace("_", " ")
        return f"Validation utility for {subject}."
    if name.startswith("chaos_"):
        return "Chaos fixture script used for adversarial or low-quality test inputs."
    return f"Python script `{name}`."


def safe_description(path: Path, *, is_test_index: bool) -> str:
    """
    Resolve description by attempting extraction then falling back to defaults.

    purpose: stable description resolution
    preconditions: none
    postconditions: returns non-empty string
    mutates: none
    reads: file content if parseable
    writes: none
    external_io: none
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        script path
    is_test_index : bool
        true if script resides in tests subtree

    Returns
    -------
    str
        resolved description
    """
    summary = extract_docstring_summary(path)
    if path.name == "generate_uuid.py" and summary == "UUID Generation Tool.":
        return fallback_description(path, is_test_index=is_test_index)
    return summary or fallback_description(path, is_test_index=is_test_index)


def build_keywords(record: ScriptRecord) -> list[str]:
    """
    Derive a list of keywords from a script record.

    purpose: keyword extraction for manifest
    preconditions: none
    postconditions: returns unique keyword list
    mutates: none
    reads: record properties
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: stable order
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    record : ScriptRecord
        input record

    Returns
    -------
    list[str]
        deduplicated keywords
    """
    pieces = re.split(r"[-_]", record.script_id.lower())
    keywords = ["script", *[piece for piece in pieces if piece], record.category]
    if record.tool_definition:
        keywords.append("tool-linked")
    deduped: list[str] = []
    for keyword in keywords:
        if keyword not in deduped:
            deduped.append(keyword)
    return deduped


def extract_frontmatter(content: str) -> dict:
    """
    Extract and parse YAML frontmatter from Markdown content.

    purpose: frontmatter extraction
    preconditions: none
    postconditions: returns dict of frontmatter or empty dict
    mutates: none
    reads: content string
    writes: none
    external_io: none
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: yaml.safe_load
    coupling: minimal

    Parameters
    ----------
    content : str
        raw Markdown content

    Returns
    -------
    dict
        parsed frontmatter
    """
    match = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return {}
    try:
        parsed = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return parsed if isinstance(parsed, dict) else {}


def detect_tool_links(tools_dir: Path) -> dict[str, str]:
    """
    Map Python scripts to their corresponding tool definition files.

    purpose: tool-link discovery
    preconditions: tools_dir must exist
    postconditions: returns mapping of script name to tool path
    mutates: none
    reads: tools directory; individual tool files
    writes: none
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: sorted by tool name
    aliasing: none
    security: none
    coupling: coupled to tool-definition schema (command field)

    Parameters
    ----------
    tools_dir : Path
        directory containing tool definitions

    Returns
    -------
    dict[str, str]
        {script_name: tool_definition_path}
    """
    links: dict[str, str] = {}
    for tool_path in sorted(tools_dir.glob("*.md"), key=lambda item: item.name.lower()):
        if tool_path.name == "index.md":
            continue
        content = read_text(tool_path)
        frontmatter = extract_frontmatter(content)
        command = str(frontmatter.get("command", ""))
        for match in re.finditer(r"\.agent/scripts/([A-Za-z0-9_-]+\.py)", command):
            script_name = match.group(1)
            links[script_name] = f".agent/tools/{tool_path.name}"
    return links


def should_include(path: Path) -> bool:
    """
    Determine if a file should be included in the script index.

    purpose: file filtering logic
    preconditions: none
    postconditions: none
    mutates: none
    reads: path properties
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        target file path

    Returns
    -------
    bool
        true if file should be indexed
    """
    if path.name in SKIP_FILENAMES:
        return False
    if path.suffix != ".py":
        return False
    if "__pycache__" in path.parts:
        return False
    if any(part.startswith(".") and part != ".agent" for part in path.parts):
        return False
    return True


def categorize_root_script(path: Path, tool_links: dict[str, str]) -> str:
    """
    Assign a categorization label to a root-level script.

    purpose: category assignment
    preconditions: none
    postconditions: returns category string
    mutates: none
    reads: path property, tool_links
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        script path
    tool_links : dict[str, str]
        existing tool mappings

    Returns
    -------
    str
        assigned category
    """
    if path.name in tool_links:
        return "utility_and_infrastructure"
    if path.name == "directory_tree.py":
        return "analysis_and_reporting"
    if path.name == "update_index.py":
        return "governance_and_inventory"
    return "general_scripts"


def categorize_test_script(path: Path) -> str:
    """
    Assign a categorization label to a test-subtree script.

    purpose: category assignment
    preconditions: none
    postconditions: returns category string
    mutates: none
    reads: path property
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        script path

    Returns
    -------
    str
        assigned category
    """
    if path.name.startswith("test_"):
        return "unit_tests"
    if path.name.startswith("validate_"):
        return "diagnostics_and_validation"
    if path.name.startswith("chaos_"):
        return "fixtures_and_chaos"
    return "test_support"


def collect_root_script_records(scripts_dir: Path, tool_links: dict[str, str]) -> list[ScriptRecord]:
    """
    Crawl scripts directory and build records for root-level scripts.

    purpose: record collection
    preconditions: scripts_dir exists
    postconditions: returns list of ScriptRecord
    mutates: none
    reads: filesystem (glob)
    writes: none
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: sorted by filename
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    scripts_dir : Path
        source directory
    tool_links : dict[str, str]
        pre-detected tool mappings

    Returns
    -------
    list[ScriptRecord]
        populated records
    """
    records: list[ScriptRecord] = []
    for path in sorted(scripts_dir.glob("*.py"), key=lambda item: item.name.lower()):
        if not should_include(path):
            continue
        records.append(
            ScriptRecord(
                script_id=path.stem,
                filename=path.name,
                relative_path=f".agent/scripts/{path.name}",
                category=categorize_root_script(path, tool_links),
                description=safe_description(path, is_test_index=False),
                tool_definition=tool_links.get(path.name),
            )
        )
    return records


def collect_test_script_records(tests_dir: Path) -> list[ScriptRecord]:
    """
    Crawl tests directory and build records for test-subtree scripts.

    purpose: record collection
    preconditions: tests_dir exists
    postconditions: returns list of ScriptRecord
    mutates: none
    reads: filesystem (glob)
    writes: none
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: sorted by filename
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    tests_dir : Path
        source tests directory

    Returns
    -------
    list[ScriptRecord]
        populated records
    """
    records: list[ScriptRecord] = []
    for path in sorted(tests_dir.glob("*.py"), key=lambda item: item.name.lower()):
        if not should_include(path):
            continue
        records.append(
            ScriptRecord(
                script_id=path.stem,
                filename=path.name,
                relative_path=f".agent/scripts/tests/{path.name}",
                category=categorize_test_script(path),
                description=safe_description(path, is_test_index=True),
            )
        )
    return records


def render_selection_map(records: list[ScriptRecord]) -> list[str]:
    """
    Generate the 'Selection Map' section of the index.

    purpose: Markdown rendering
    preconditions: none
    postconditions: returns Markdown line list
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        input records

    Returns
    -------
    list[str]
        Markdown lines
    """
    if not records:
        return ["*No scripts are currently defined.*"]
    return [f"- `{record.script_id}`: {record.description}" for record in records]


def render_manifest(records: list[ScriptRecord], *, root_key: str) -> str:
    """
    Generate the YAML manifest section of the index.

    purpose: YAML rendering
    preconditions: none
    postconditions: returns YAML string
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        input records
    root_key : str
        top-level key for the manifest

    Returns
    -------
    str
        formatted YAML
    """
    manifest_records: list[dict[str, object]] = []
    for record in records:
        manifest_record: dict[str, object] = {
            "id": record.script_id,
            "definition": record.relative_path,
            "asset_structure": "flat-file",
            "category": record.category,
            "implementation": record.relative_path,
            "keywords": build_keywords(record),
            "use_when": [record.description],
        }
        if record.tool_definition:
            manifest_record["tool_definition"] = record.tool_definition
        manifest_records.append(manifest_record)
    return yaml.safe_dump({root_key: manifest_records}, sort_keys=False, allow_unicode=False).strip()


def render_category_totals(records: list[ScriptRecord], *, category_order: list[str]) -> list[str]:
    """
    Generate the 'Category Totals' summary section.

    purpose: count aggregation and rendering
    preconditions: none
    postconditions: returns Markdown line list
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: follows category_order
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        input records
    category_order : list[str]
        order in which categories should be displayed

    Returns
    -------
    list[str]
        Markdown lines
    """
    totals: list[str] = []
    for category in category_order:
        count = sum(1 for record in records if record.category == category)
        if count:
            totals.append(f"- `{category}`: `{count}`")
    totals.append(f"- `total`: `{len(records)}`")
    return totals


def render_root_records(records: list[ScriptRecord]) -> list[str]:
    """
    Generate detailed record blocks for root scripts.

    purpose: detailed Markdown rendering
    preconditions: none
    postconditions: returns Markdown line list
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        input records

    Returns
    -------
    list[str]
        Markdown lines
    """
    if not records:
        return ["*No root scripts are currently defined.*"]

    lines: list[str] = []
    for record in records:
        lines.extend(
            [
                f"### `{record.script_id}`",
                "",
                f"- Implementation: [`{record.filename}`]({record.filename})",
                f"- Best used for: {record.description}",
                f"- Category: `{record.category}`",
            ]
        )
        if record.tool_definition:
            tool_name = Path(record.tool_definition).name
            lines.append(f"- Tool Definition: [`{tool_name}`](../tools/{tool_name})")
            lines.append("- Open the linked tool definition before execution when exact flags, outputs, or safety boundaries matter.")
        else:
            lines.append("- Tool Definition: none")
            lines.append("- Open the script implementation when internal helper behavior or direct invocation details matter.")
        lines.append("")
    return lines[:-1]


def render_test_records(records: list[ScriptRecord]) -> list[str]:
    """
    Generate detailed record blocks for test-subtree scripts.

    purpose: detailed Markdown rendering
    preconditions: none
    postconditions: returns Markdown line list
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        input records

    Returns
    -------
    list[str]
        Markdown lines
    """
    if not records:
        return ["*No tests scripts are currently defined.*"]

    lines: list[str] = []
    for record in records:
        lines.extend(
            [
                f"### `{record.script_id}`",
                "",
                f"- Implementation: [`{record.filename}`]({record.filename})",
                f"- Best used for: {record.description}",
                f"- Category: `{record.category}`",
                "- Open the script implementation when exact assertions, fixture behavior, or validation protocol matter.",
                "",
            ]
        )
    return lines[:-1]


def build_root_index(records: list[ScriptRecord]) -> str:
    """
    Assemble the complete root script index document.

    purpose: index assembly
    preconditions: none
    postconditions: returns full Markdown content
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        root script records

    Returns
    -------
    str
        Markdown document content
    """
    lines = [
        "# Agent Scripts Index",
        "",
        "> Consolidated registry of root script implementations in `.agent/scripts/`.",
        ">",
        "> Scope: discovery, first-pass selection, and quick routing across durable script assets that live directly under the scripts root.",
        ">",
        f"> Total scripts: `{len(records)}`",
        ">",
        "> Parent: [`.agent/`](..)",
        ">",
        "> Authority rule: if this index conflicts with a linked script implementation or linked tool definition, the implementation and tool definition are authoritative.",
        "",
        "## Use This Index",
        "",
        "1. Use the selection map to identify the most likely root script by intent.",
        "2. Use the manifest to confirm the implementation path, category, and optional tool linkage.",
        "3. Open the linked tool definition before execution when invocation semantics, output handling, or safety boundaries matter.",
        "",
        "## Selection Map",
        "",
    ]
    lines.extend(render_selection_map(records))
    lines.extend(
        [
            "",
            "## Manifest",
            "",
            "```yaml",
            render_manifest(records, root_key="scripts"),
            "```",
            "",
            "## Script Records",
            "",
        ]
    )
    lines.extend(render_root_records(records))
    lines.extend(
        [
            "",
            "## Category Totals",
            "",
        ]
    )
    lines.extend(
        render_category_totals(
            records,
            category_order=[
                "utility_and_infrastructure",
                "analysis_and_reporting",
                "governance_and_inventory",
                "general_scripts",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Index Boundaries",
            "",
            "- This file is a discovery and selection aid, not the execution contract.",
            "- It inventories only root-level Python scripts under `.agent/scripts/` and excludes the governed `tests/` subtree.",
            "- When a task depends on exact CLI behavior, outputs, or deletion semantics, defer to the linked script implementation and any linked tool definition.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def build_tests_index(records: list[ScriptRecord]) -> str:
    """
    Assemble the complete test subtree script index document.

    purpose: index assembly
    preconditions: none
    postconditions: returns full Markdown content
    mutates: none
    reads: records
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    records : list[ScriptRecord]
        test script records

    Returns
    -------
    str
        Markdown document content
    """
    lines = [
        "# Agent Script Tests Index",
        "",
        "> Consolidated registry of governed test and validation scripts in `.agent/scripts/tests/`.",
        ">",
        "> Scope: discovery, first-pass selection, and quick routing across unit tests, diagnostics, and fixture helpers that support the scripts collection.",
        ">",
        f"> Total test scripts: `{len(records)}`",
        ">",
        "> Parent: [`.agent/scripts/`](..)",
        ">",
        "> Authority rule: if this index conflicts with a linked test implementation, the test script is authoritative.",
        "",
        "## Use This Index",
        "",
        "1. Use the selection map to identify the most relevant test, diagnostic, or fixture script.",
        "2. Use the manifest to confirm the implementation path and category before execution.",
        "3. Open the linked test implementation when exact assertions, environment assumptions, or fixture behavior matter.",
        "",
        "## Selection Map",
        "",
    ]
    lines.extend(render_selection_map(records))
    lines.extend(
        [
            "",
            "## Manifest",
            "",
            "```yaml",
            render_manifest(records, root_key="tests"),
            "```",
            "",
            "## Test Script Records",
            "",
        ]
    )
    lines.extend(render_test_records(records))
    lines.extend(
        [
            "",
            "## Category Totals",
            "",
        ]
    )
    lines.extend(
        render_category_totals(
            records,
            category_order=[
                "unit_tests",
                "diagnostics_and_validation",
                "fixtures_and_chaos",
                "test_support",
            ],
        )
    )
    lines.extend(
        [
            "",
            "## Index Boundaries",
            "",
            "- This file is a discovery and selection aid, not the execution contract.",
            "- It inventories only live Python files in `.agent/scripts/tests/` and excludes generated indexes, caches, and compiled artifacts.",
            "- When a task depends on exact assertions, subprocess expectations, or fixture semantics, defer to the linked test implementation.",
            "",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def write_file(path: Path, content: str) -> None:
    """
    Physically write index content to the filesystem with UTF-8 encoding.

    purpose: index persistence
    preconditions: path parent must exist
    postconditions: file written to disk
    mutates: none
    reads: none
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: not thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : Path
        target path
    content : str
        content to write
    """
    path.write_text(content, encoding="utf-8", newline="\n")


def main() -> None:
    """
    Execute the index regeneration workflow.

    purpose: entrypoint
    preconditions: filesystem access to .agent/scripts/ and .agent/tools/
    postconditions: script indexes updated
    mutates: .agent/scripts/index.md, .agent/scripts/tests/index.md
    reads: tools, scripts, tests
    writes: root and tests indexes
    external_io: fs
    determinism: state-dependent
    idempotency: yes
    concurrency: process-local
    ordering: sequential
    aliasing: none
    security: none
    coupling: coupled to project directory structure
    """
    tool_links = detect_tool_links(TOOLS_DIR)
    root_records = collect_root_script_records(SCRIPTS_DIR, tool_links)
    test_records = collect_test_script_records(TESTS_DIR)
    write_file(ROOT_INDEX_PATH, build_root_index(root_records))
    write_file(TESTS_INDEX_PATH, build_tests_index(test_records))
    print("[OK] scripts indexes updated successfully.")


if __name__ == "__main__":
    main()

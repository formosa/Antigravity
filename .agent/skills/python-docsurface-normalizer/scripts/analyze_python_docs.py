#!/usr/bin/env python3
"""
Provide deterministic analysis of Python files for documentation normalization eligibility.

role: deterministic-analyzer
entrypoints: main
reads: target python files
writes: stdout (json or text)
external_io: fs (read-only)
state_model: stateless
failure_surface: fs-io, syntax-errors, token-errors
coupling: minimal
determinism: deterministic
concurrency: thread-safe
"""

from __future__ import annotations

import argparse
import ast
import io
import json
import re
import tokenize
from dataclasses import dataclass, field
from pathlib import Path

ENCODING_PATTERN = re.compile(r"coding[:=]\s*[-\w.]+", re.IGNORECASE)
DIRECTIVE_PATTERNS = (
    re.compile(r"^noqa(?::.*)?$", re.IGNORECASE),
    re.compile(r"^type:\s*ignore(?:\[.*\])?.*$", re.IGNORECASE),
    re.compile(r"^pragma:\s*no\s*cover\b.*$", re.IGNORECASE),
    re.compile(r"^pyright:\s*.*$", re.IGNORECASE),
    re.compile(r"^pylint:\s*.*$", re.IGNORECASE),
    re.compile(r"^ruff:\s*.*$", re.IGNORECASE),
    re.compile(r"^fmt:\s*(?:on|off|skip)\b.*$", re.IGNORECASE),
    re.compile(r"^isort:\s*.*$", re.IGNORECASE),
)

@dataclass(slots=True)
class AnalysisResult:
    """
    Represent the documentation-readiness analysis of a single Python file.

    role: record-container
    lifecycle: transient
    mutability: mutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: dictionary-serializable
    coupling: minimal
    failure_surface: minimal

    Attributes
    ----------
    path : str
        filesystem path to target
    eligible : bool
        true if target meets selection criteria
    parse_ok : bool
        true if target is syntactically valid
    hard_exclusions : list[str]
        identified reasons for ineligibility
    module_docstring_present : bool
        true if module-level docstring exists
    public_class_count : int
        count of classes not prefixed with underscore
    public_function_count : int
        count of functions not prefixed with underscore
    docstring_count : int
        total count of identified docstrings
    comment_count : int
        total count of identified comments
    directive_comment_count : int
        total count of identified directive/tooling comments
    preserve_sensitive : bool
        true if target contains non-directive comments or docstrings
    preserve_reasons : list[str]
        semantic justification for preservation
    """
    path: str
    eligible: bool
    parse_ok: bool
    hard_exclusions: list[str] = field(default_factory=list)
    module_docstring_present: bool = False
    public_class_count: int = 0
    public_function_count: int = 0
    docstring_count: int = 0
    comment_count: int = 0
    directive_comment_count: int = 0
    preserve_sensitive: bool = False
    preserve_reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, object]:
        """
        Convert the analysis result to a JSON-stable dictionary.

        purpose: preparation for serialization
        preconditions: none
        postconditions: returns dictionary containing current field values
        mutates: none
        reads: self
        writes: none
        external_io: none
        determinism: deterministic
        idempotency: yes
        concurrency: thread-safe
        ordering: none
        aliasing: returns new dictionary object
        security: none
        coupling: minimal

        Returns
        -------
        dict[str, object]
            dictionary representation of AnalysisResult
        """
        return {
            "path": self.path,
            "eligible": self.eligible,
            "parse_ok": self.parse_ok,
            "hard_exclusions": self.hard_exclusions,
            "module_docstring_present": self.module_docstring_present,
            "public_class_count": self.public_class_count,
            "public_function_count": self.public_function_count,
            "docstring_count": self.docstring_count,
            "comment_count": self.comment_count,
            "directive_comment_count": self.directive_comment_count,
            "preserve_sensitive": self.preserve_sensitive,
            "preserve_reasons": self.preserve_reasons,
        }

def read_text(path: Path) -> str:
    """
    Read file content with fallback encoding detection.

    purpose: file-to-string extraction
    preconditions: path is readable
    postconditions: returns file content
    mutates: none
    reads: filesystem
    writes: none
    external_io: fs
    determinism: deterministic (based on file content)
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
        file content as string
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")

def contains_sequence(parts: tuple[str, ...], sequence: tuple[str, ...]) -> bool:
    """
    Determine if a tuple contains a specific subsequence regardless of casing.

    purpose: case-insensitive subsequence detection
    preconditions: none
    postconditions: returns true if sequence is present
    mutates: none
    reads: none
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: linear scan
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    parts : tuple[str, ...]
        container sequence
    sequence : tuple[str, ...]
        target subsequence

    Returns
    -------
    bool
        true if sequence found in parts
    """
    lowered_parts = tuple(part.lower() for part in parts)
    lowered_sequence = tuple(part.lower() for part in sequence)
    width = len(lowered_sequence)
    for index in range(0, len(lowered_parts) - width + 1):
        if lowered_parts[index : index + width] == lowered_sequence:
            return True
    return False

def is_directive_comment(comment_text: str, line_number: int) -> bool:
    """
    Classify a comment as a directive or tooling pragma.

    purpose: documentation-normalization exclusion check
    preconditions: none
    postconditions: returns true if comment is a shebang, encoding, or known pragma
    mutates: none
    reads: none
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: matches DIRECTIVE_PATTERNS

    Parameters
    ----------
    comment_text : str
        raw comment string including #
    line_number : int
        1-based line number for contextual classification

    Returns
    -------
    bool
        true if comment is a directive
    """
    # INVARIANT: shebang must be on line 1
    stripped = comment_text.strip()
    if line_number == 1 and stripped.startswith("#!"):
        return True
    # INVARIANT: encoding header must be in first 2 lines
    if line_number <= 2 and ENCODING_PATTERN.search(stripped):
        return True
    if not stripped.startswith("#"):
        return False

    body = stripped[1:].strip()
    return any(pattern.match(body) for pattern in DIRECTIVE_PATTERNS)

def collect_hard_exclusions(path: Path) -> list[str]:
    """
    Identify reasons why a path is ineligible for documentation normalization.

    purpose: eligibility filtering
    preconditions: none
    postconditions: returns list of identified exclusion codes
    mutates: none
    reads: filesystem (existence, directory check)
    writes: none
    external_io: fs
    determinism: deterministic (based on path and fs state)
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: path-structure coupling

    Parameters
    ----------
    path : Path
        target path to evaluate

    Returns
    -------
    list[str]
        identified exclusion reason codes
    """
    exclusions: list[str] = []
    parts = path.parts
    lowered_parts = {part.lower() for part in parts}

    if path.suffix.lower() != ".py":
        exclusions.append("non_python_target")
    if path.exists() and path.is_dir():
        exclusions.append("directory_targets_not_supported")
    if ".archive" in lowered_parts:
        exclusions.append("archive_target")
    if ".venv" in lowered_parts:
        exclusions.append("virtualenv_target")
    if "__pycache__" in lowered_parts:
        exclusions.append("pycache_target")
    if contains_sequence(parts, (".agent", ".temp")):
        exclusions.append("managed_temp_target")
    if contains_sequence(parts, ("resources", "schema")):
        exclusions.append("schema_mirror_target")
    if any(part.lower().endswith(".skill") for part in parts):
        exclusions.append("packaged_skill_surface")
    if not path.exists():
        exclusions.append("missing_target")

    return exclusions

def scan_comments(source: str) -> tuple[int, int]:
    """
    Analyze tokens in source code to count total and directive comments.

    purpose: comment-surface analysis
    preconditions: source is valid python
    postconditions: returns (total_comment_count, directive_comment_count)
    mutates: none
    reads: none
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
    source : str
        python source code string

    Returns
    -------
    tuple[int, int]
        (total_count, directive_count)
    """
    comment_count = 0
    directive_count = 0
    try:
        # SIDE-EFFECT: tokenize may raise TokenError on malformed source
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type != tokenize.COMMENT:
                continue
            comment_count += 1
            if is_directive_comment(token.string, token.start[0]):
                directive_count += 1
    except tokenize.TokenError:
        pass
    return comment_count, directive_count

def count_docstrings(tree: ast.Module) -> tuple[bool, int]:
    """
    Traverse an AST to count identified docstrings and check for module docstring.

    purpose: docstring-surface analysis
    preconditions: tree is a valid ast.Module
    postconditions: returns (module_docstring_present, total_docstring_count)
    mutates: none
    reads: none
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
    tree : ast.Module
        parsed module AST

    Returns
    -------
    tuple[bool, int]
        (has_module_docstring, total_count)
    """
    module_docstring_present = bool(ast.get_docstring(tree, clean=False))
    count = 1 if module_docstring_present else 0

    for node in ast.walk(tree):
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and ast.get_docstring(
            node, clean=False
        ):
            count += 1

    return module_docstring_present, count

def analyze_target(raw_target: str | Path) -> AnalysisResult:
    """
    Perform deep analysis of a single target path for normalization readiness.

    purpose: single-file eligibility and surface-density analysis
    preconditions: none
    postconditions: returns populated AnalysisResult
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
    coupling: minimal

    Parameters
    ----------
    raw_target : str | Path
        path to target file

    Returns
    -------
    AnalysisResult
        populated result object
    """
    path = Path(raw_target).resolve()
    hard_exclusions = collect_hard_exclusions(path)
    result = AnalysisResult(
        path=path.as_posix(),
        eligible=not hard_exclusions,
        parse_ok=False,
        hard_exclusions=hard_exclusions,
    )

    if not result.eligible:
        return result

    try:
        source = read_text(path)
    except OSError:
        result.hard_exclusions.append("unreadable_target")
        result.eligible = False
        return result

    result.comment_count, result.directive_comment_count = scan_comments(source)
    non_directive_comment_count = result.comment_count - result.directive_comment_count

    try:
        tree = ast.parse(source)
    except SyntaxError:
        result.parse_ok = False
    else:
        result.parse_ok = True
        result.module_docstring_present, result.docstring_count = count_docstrings(tree)
        result.public_class_count = sum(
            1 for node in tree.body if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
        )
        result.public_function_count = sum(
            1
            for node in tree.body
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and not node.name.startswith("_")
        )

    if result.docstring_count:
        result.preserve_reasons.append(f"{result.docstring_count} existing docstring(s)")
    if non_directive_comment_count:
        result.preserve_reasons.append(f"{non_directive_comment_count} non-directive comment(s)")

    result.preserve_sensitive = bool(result.preserve_reasons)
    return result

def analyze_targets(targets: list[str | Path]) -> list[AnalysisResult]:
    """
    Process multiple target paths in sequence for normalization analysis.

    purpose: bulk eligibility analysis
    preconditions: none
    postconditions: returns list of AnalysisResult objects
    mutates: none
    reads: filesystem
    writes: none
    external_io: fs
    determinism: input-dependent
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    targets : list[str | Path]
        list of candidate file paths

    Returns
    -------
    list[AnalysisResult]
        list of populated result objects
    """
    return [analyze_target(target) for target in targets]

def render_text(results: list[AnalysisResult]) -> str:
    """
    Prepare a human-readable text block summarizing analysis results.

    purpose: analysis result representation
    preconditions: none
    postconditions: returns formatted text block
    mutates: none
    reads: results
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
    results : list[AnalysisResult]
        list of completed analysis results

    Returns
    -------
    str
        formatted result text
    """
    rendered_blocks: list[str] = []
    for result in results:
        reasons = result.preserve_reasons or ["none"]
        rendered_blocks.extend(
            [
                f"path: {result.path}",
                f"eligible: {str(result.eligible).lower()}",
                f"parse_ok: {str(result.parse_ok).lower()}",
                f"hard_exclusions: {', '.join(result.hard_exclusions) if result.hard_exclusions else 'none'}",
                f"module_docstring_present: {str(result.module_docstring_present).lower()}",
                f"public_class_count: {result.public_class_count}",
                f"public_function_count: {result.public_function_count}",
                f"docstring_count: {result.docstring_count}",
                f"comment_count: {result.comment_count}",
                f"directive_comment_count: {result.directive_comment_count}",
                f"preserve_sensitive: {str(result.preserve_sensitive).lower()}",
                "preserve_reasons:",
                *[f"  - {reason}" for reason in reasons],
                "",
            ]
        )
    return "\n".join(rendered_blocks).rstrip() + "\n"

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the analyzer.

    purpose: CLI configuration extraction
    preconditions: none
    postconditions: returns parsed argument namespace
    mutates: none
    reads: sys.argv
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Returns
    -------
    argparse.Namespace
        parsed arguments
    """
    parser = argparse.ArgumentParser(description="Analyze explicit Python targets for documentation rewrite eligibility.")
    parser.add_argument("targets", nargs="+", help="Explicit Python file target(s).")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable text.")
    return parser.parse_args()

def main() -> int:
    """
    Execute the core analysis workflow from CLI.

    purpose: entrypoint for normalization analysis
    preconditions: none
    postconditions: outputs results to stdout
    mutates: none
    reads: filesystem
    writes: stdout
    external_io: fs, stdout
    determinism: input-dependent
    idempotency: yes
    concurrency: not thread-safe (stdout writes)
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Returns
    -------
    int
        exit code (0 for success)
    """
    args = parse_args()
    results = analyze_targets(args.targets)
    if args.json:
        print(json.dumps([result.to_dict() for result in results], indent=2, ensure_ascii=False))
    else:
        print(render_text(results), end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


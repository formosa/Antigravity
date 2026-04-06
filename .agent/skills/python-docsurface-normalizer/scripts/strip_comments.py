#!/usr/bin/env python3
"""
Provide deterministic removal of non-directive docstrings and comments from Python files.

role: documentation-stripper
entrypoints: main
reads: target python file
writes: modified python file (optional) or stdout
external_io: fs (read/write)
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
import re
import tokenize
from dataclasses import dataclass
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
class StripResult:
    """
    Represent the outcome of a documentation and comment stripping operation.

    role: record-container
    lifecycle: transient
    mutability: mutable
    ownership: none
    concurrency: thread-safe
    cache_behavior: none
    serialization: none
    coupling: minimal
    failure_surface: minimal

    Attributes
    ----------
    path : str
        filesystem path to target
    rewritten_source : str
        source code after stripping
    removed_docstrings : int
        count of docstrings removed
    removed_comments : int
        count of non-directive comments removed
    preserved_directive_comments : int
        count of directive/tooling comments preserved
    changed : bool
        true if output source differs from input
    write_applied : bool
        true if changes were persisted to disk
    """
    path: str
    rewritten_source: str
    removed_docstrings: int
    removed_comments: int
    preserved_directive_comments: int
    changed: bool
    write_applied: bool

def read_text(path: Path) -> tuple[str, str]:
    """
    Read file content and return text plus identified encoding.

    purpose: file-to-string extraction with encoding preservation
    preconditions: path is readable
    postconditions: returns (content, encoding_name)
    mutates: none
    reads: filesystem
    writes: none
    external_io: fs
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
    tuple[str, str]
        (file_content, encoding)
    """
    try:
        return path.read_text(encoding="utf-8"), "utf-8"
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1"), "latin-1"

def is_directive_comment(comment_text: str, line_number: int) -> bool:
    """
    Classify a comment as a directive or tooling pragma.

    purpose: documentation-stripping exclusion check
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
    stripped = comment_text.strip()
    if line_number == 1 and stripped.startswith("#!"):
        return True
    if line_number <= 2 and ENCODING_PATTERN.search(stripped):
        return True
    if not stripped.startswith("#"):
        return False

    body = stripped[1:].strip()
    return any(pattern.match(body) for pattern in DIRECTIVE_PATTERNS)

def get_offset(lines: list[str], lineno: int, col_offset: int) -> int:
    """
    Convert (line, column) coordinates into a linear byte offset.

    purpose: coordinate translation for string slicing
    preconditions: lineno and col_offset are valid for lines
    postconditions: returns absolute offset from start of string
    mutates: none
    reads: lines
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: linear sum of previous lines
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    lines : list[str]
        list of source lines with ends preserved
    lineno : int
        1-based line number
    col_offset : int
        0-based column offset

    Returns
    -------
    int
        linear index into the full source string
    """
    return sum(len(line) for line in lines[: lineno - 1]) + col_offset

def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
    """
    Merge overlapping or adjacent coordinate intervals into canonical disjoint sets.

    purpose: interval normalization before cutting
    preconditions: none
    postconditions: returns sorted list of minimal disjoint intervals
    mutates: none
    reads: intervals
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sorts by start index
    aliasing: returns new list
    security: none
    coupling: minimal

    Parameters
    ----------
    intervals : list[tuple[int, int]]
        list of (start, end) coordinate pairs

    Returns
    -------
    list[tuple[int, int]]
        normalized disjoint intervals
    """
    if not intervals:
        return []

    ordered = sorted(intervals, key=lambda item: item[0])
    merged = [ordered[0]]
    for start, end in ordered[1:]:
        current_start, current_end = merged[-1]
        if start <= current_end:
            merged[-1] = (current_start, max(current_end, end))
        else:
            merged.append((start, end))
    return merged

def is_docstring_expr(node: ast.Expr) -> bool:
    """
    Check if an AST expression represents a valid Python docstring.

    purpose: docstring identification
    preconditions: node is an ast.Expr
    postconditions: returns true if expression content is a string constant
    mutates: none
    reads: node
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
    node : ast.Expr
        AST expression node

    Returns
    -------
    bool
        true if node is a docstring candidate
    """
    value = node.value
    return isinstance(value, ast.Constant) and isinstance(value.value, str) or isinstance(value, ast.Str)

def get_docstring_ranges(tree: ast.AST, lines: list[str]) -> tuple[list[tuple[int, int]], int]:
    """
    Identify character ranges of all docstrings in an AST.

    purpose: docstring coordinate extraction
    preconditions: tree matches source code in lines
    postconditions: returns (coordinate_ranges, docstring_count)
    mutates: none
    reads: tree, lines
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: depth-first search
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    tree : ast.AST
        parsed AST
    lines : list[str]
        source lines used for coordinate resolution

    Returns
    -------
    tuple[list[tuple[int, int]], int]
        (intervals, count)
    """
    ranges: list[tuple[int, int]] = []
    removed = 0
    for node in ast.walk(tree):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not getattr(node, "body", None):
            continue
        first_statement = node.body[0]
        if not isinstance(first_statement, ast.Expr) or not is_docstring_expr(first_statement):
            continue
        if not hasattr(first_statement, "end_lineno") or not hasattr(first_statement, "end_col_offset"):
            continue
        start = get_offset(lines, first_statement.lineno, first_statement.col_offset)
        end = get_offset(lines, first_statement.end_lineno, first_statement.end_col_offset)
        ranges.append((start, end))
        removed += 1
    return ranges, removed

def get_comment_ranges(source: str, lines: list[str]) -> tuple[list[tuple[int, int]], int, int]:
    """
    Identify character ranges of all non-directive comments using token analysis.

    purpose: comment coordinate extraction
    preconditions: source matches lines
    postconditions: returns (intervals, removed_count, preserved_count)
    mutates: none
    reads: source, lines
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential token scan
    aliasing: none
    security: none
    coupling: matches DIRECTIVE_PATTERNS

    Parameters
    ----------
    source : str
        raw source code
    lines : list[str]
        source lines for coordinate resolution

    Returns
    -------
    tuple[list[tuple[int, int]], int, int]
        (intervals, removed_count, preserved_count)
    """
    ranges: list[tuple[int, int]] = []
    removed = 0
    preserved = 0
    try:
        tokens = tokenize.generate_tokens(io.StringIO(source).readline)
        for token in tokens:
            if token.type != tokenize.COMMENT:
                continue
            if is_directive_comment(token.string, token.start[0]):
                preserved += 1
                continue
            start = get_offset(lines, token.start[0], token.start[1])
            end = get_offset(lines, token.end[0], token.end[1])
            ranges.append((start, end))
            removed += 1
    except tokenize.TokenError as exc:
        raise ValueError(f"Tokenizer error while scanning comments: {exc}") from exc
    return ranges, removed, preserved

def apply_cuts(source: str, cuts: list[tuple[int, int]]) -> str:
    """
    Remove specified segments from a string.

    purpose: source code redaction
    preconditions: none
    postconditions: returns string with intervals removed
    mutates: none
    reads: source
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: processes intervals in reverse order to maintain index stability
    aliasing: returns new string
    security: none
    coupling: minimal

    Parameters
    ----------
    source : str
        input string
    cuts : list[tuple[int, int]]
        list of (start, end) byte offsets

    Returns
    -------
    str
        redacted string
    """
    rewritten = source
    for start, end in sorted(cuts, key=lambda item: item[0], reverse=True):
        rewritten = rewritten[:start] + rewritten[end:]
    return rewritten

def detect_newline(source: str) -> str:
    """
    Determine the prevailing newline character sequence in a string.

    purpose: newline preservation
    preconditions: none
    postconditions: returns "\\r\\n" or "\\n"
    mutates: none
    reads: source
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: search for CRLF first
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    source : str
        input source code

    Returns
    -------
    str
        detected newline sequence
    """
    return "\r\n" if "\r\n" in source else "\n"

def collapse_blank_lines(source: str, newline: str) -> str:
    """
    Reduce sequences of three or more consecutive newlines into two.

    purpose: blank line normalization
    preconditions: none
    postconditions: returns string with collapsed blank lines
    mutates: none
    reads: source
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: iterative replacement
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    source : str
        input source
    newline : str
        newline sequence to target

    Returns
    -------
    str
        normalized source
    """
    while newline * 3 in source:
        source = source.replace(newline * 3, newline * 2)
    return source

def strip_trailing_whitespace(source: str, newline: str) -> str:
    """
    Remove trailing whitespace from each line in a string.

    purpose: whitespace cleanup
    preconditions: none
    postconditions: returns cleaned string
    mutates: none
    reads: source
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: line-by-line processing
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    source : str
        input source
    newline : str
        newline sequence for joining

    Returns
    -------
    str
        cleaned source
    """
    has_final_newline = source.endswith(("\n", "\r"))
    lines = source.splitlines()
    cleaned = newline.join(line.rstrip() for line in lines)
    if has_final_newline:
        cleaned += newline
    return cleaned

def validate_syntax(source: str) -> None:
    """
    Prove that a source string is syntactically valid Python.

    purpose: post-modification safety check
    preconditions: none
    postconditions: raises ValueError if source is invalid
    mutates: none
    reads: source
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
        Python source code to validate
    """
    try:
        compile(source, "<string>", "exec")
    except SyntaxError as exc:
        raise ValueError(f"Rewritten source has syntax errors: {exc}") from exc

def rewrite_source(source: str) -> tuple[str, int, int, int]:
    """
    Execute the core stripping logic against a source code string.

    purpose: modular stripping workflow
    preconditions: source is valid Python
    postconditions: returns (rewritten_source, removed_docstrings, removed_comments, preserved_directives)
    mutates: none
    reads: source
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential steps: parse -> coordinate identification -> cut -> normalize -> validate
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    source : str
        input raw source code

    Returns
    -------
    tuple[str, int, int, int]
        stripping outcome payload
    """
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        raise ValueError(f"Input source has syntax errors: {exc}") from exc

    lines = source.splitlines(keepends=True)
    docstring_ranges, removed_docstrings = get_docstring_ranges(tree, lines)
    comment_ranges, removed_comments, preserved_directives = get_comment_ranges(source, lines)
    cuts = merge_intervals(docstring_ranges + comment_ranges)

    rewritten = apply_cuts(source, cuts)
    newline = detect_newline(source)
    rewritten = collapse_blank_lines(rewritten, newline)
    rewritten = strip_trailing_whitespace(rewritten, newline)
    validate_syntax(rewritten)
    return rewritten, removed_docstrings, removed_comments, preserved_directives

def process_file(path: str | Path, *, write: bool = False) -> StripResult:
    """
    Coordinate the end-to-end stripping process for a filesystem target.

    purpose: file-centric stripping workflow
    preconditions: path is readable and exists
    postconditions: returns StripResult, optionally writes to disk
    mutates: filesystem (if write is true)
    reads: filesystem
    writes: filesystem (if write is true)
    external_io: fs
    determinism: input-dependent
    idempotency: yes (idempotent result)
    concurrency: not thread-safe (file writes)
    ordering: sequential steps
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    path : str | Path
        path to target file
    write : bool
        if true, overwrite the original file with changes

    Returns
    -------
    StripResult
        outcome details
    """
    target_path = Path(path).resolve()
    source, encoding = read_text(target_path)
    rewritten, removed_docstrings, removed_comments, preserved_directives = rewrite_source(source)
    changed = rewritten != source

    if write:
        target_path.write_text(rewritten, encoding=encoding, newline="")

    return StripResult(
        path=target_path.as_posix(),
        rewritten_source=rewritten,
        removed_docstrings=removed_docstrings,
        removed_comments=removed_comments,
        preserved_directive_comments=preserved_directives,
        changed=changed,
        write_applied=write,
    )

def parse_args() -> argparse.Namespace:
    """
    Parse command-line arguments for the stripper.

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
    parser = argparse.ArgumentParser(description="Strip non-directive docstrings and comments from a Python file.")
    parser.add_argument("target", help="Explicit Python file target.")
    parser.add_argument("--write", action="store_true", help="Write the rewritten source back to the file.")
    return parser.parse_args()

def main() -> int:
    """
    Execute the stripper workflow from CLI.

    purpose: entrypoint for documentation stripping
    preconditions: none
    postconditions: outputs result status or source to stdout
    mutates: filesystem (if --write passed)
    reads: filesystem
    writes: filesystem, stdout
    external_io: fs, stdout
    determinism: input-dependent
    idempotency: yes
    concurrency: not thread-safe (stdout/file writes)
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Returns
    -------
    int
        exit code (0 for success, 1 for error)
    """
    args = parse_args()
    try:
        result = process_file(args.target, write=args.write)
    except (OSError, ValueError) as exc:
        print(f"ERROR: {exc}")
        return 1

    if args.write:
        print(
            f"Updated {result.path} (removed {result.removed_docstrings} docstring(s), "
            f"{result.removed_comments} comment(s); preserved {result.preserved_directive_comments} directive comment(s))."
        )
    else:
        print(result.rewritten_source, end="")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())


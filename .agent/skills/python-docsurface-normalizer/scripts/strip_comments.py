#!/usr/bin/env python3
"""
Strip non-directive docstrings and comments from a Python file.
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
    path: str
    rewritten_source: str
    removed_docstrings: int
    removed_comments: int
    preserved_directive_comments: int
    changed: bool
    write_applied: bool


def read_text(path: Path) -> tuple[str, str]:
    try:
        return path.read_text(encoding="utf-8"), "utf-8"
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1"), "latin-1"


def is_directive_comment(comment_text: str, line_number: int) -> bool:
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
    return sum(len(line) for line in lines[: lineno - 1]) + col_offset


def merge_intervals(intervals: list[tuple[int, int]]) -> list[tuple[int, int]]:
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
    value = node.value
    return isinstance(value, ast.Constant) and isinstance(value.value, str) or isinstance(value, ast.Str)


def get_docstring_ranges(tree: ast.AST, lines: list[str]) -> tuple[list[tuple[int, int]], int]:
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
    rewritten = source
    for start, end in sorted(cuts, key=lambda item: item[0], reverse=True):
        rewritten = rewritten[:start] + rewritten[end:]
    return rewritten


def detect_newline(source: str) -> str:
    return "\r\n" if "\r\n" in source else "\n"


def collapse_blank_lines(source: str, newline: str) -> str:
    while newline * 3 in source:
        source = source.replace(newline * 3, newline * 2)
    return source


def strip_trailing_whitespace(source: str, newline: str) -> str:
    has_final_newline = source.endswith(("\n", "\r"))
    lines = source.splitlines()
    cleaned = newline.join(line.rstrip() for line in lines)
    if has_final_newline:
        cleaned += newline
    return cleaned


def validate_syntax(source: str) -> None:
    try:
        compile(source, "<string>", "exec")
    except SyntaxError as exc:
        raise ValueError(f"Rewritten source has syntax errors: {exc}") from exc


def rewrite_source(source: str) -> tuple[str, int, int, int]:
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
    parser = argparse.ArgumentParser(description="Strip non-directive docstrings and comments from a Python file.")
    parser.add_argument("target", help="Explicit Python file target.")
    parser.add_argument("--write", action="store_true", help="Write the rewritten source back to the file.")
    return parser.parse_args()


def main() -> int:
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

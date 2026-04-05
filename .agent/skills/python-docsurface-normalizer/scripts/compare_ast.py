#!/usr/bin/env python3
"""
Compare two Python files while ignoring docstring differences.
"""

from __future__ import annotations

import argparse
import ast
import copy
from pathlib import Path


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")


def strip_docstrings(tree: ast.AST) -> ast.AST:
    stripped = copy.deepcopy(tree)
    for node in ast.walk(stripped):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not getattr(node, "body", None):
            continue
        first_statement = node.body[0]
        if (
            isinstance(first_statement, ast.Expr)
            and isinstance(first_statement.value, ast.Constant)
            and isinstance(first_statement.value.value, str)
        ) or (isinstance(first_statement, ast.Expr) and isinstance(first_statement.value, ast.Str)):
            node.body = node.body[1:]
    return stripped


def normalize_ast(tree: ast.AST) -> str:
    for node in ast.walk(tree):
        for attr in ("lineno", "col_offset", "end_lineno", "end_col_offset"):
            if hasattr(node, attr):
                setattr(node, attr, 0)
    return ast.dump(tree, annotate_fields=True, include_attributes=False)


def compare_files(before_path: str | Path, after_path: str | Path) -> tuple[bool, str]:
    original = Path(before_path).resolve()
    modified = Path(after_path).resolve()

    try:
        original_ast = ast.parse(read_text(original))
    except (OSError, SyntaxError) as exc:
        return False, f"ERROR: unable to parse original file: {exc}"

    try:
        modified_ast = ast.parse(read_text(modified))
    except (OSError, SyntaxError) as exc:
        return False, f"ERROR: unable to parse modified file: {exc}"

    normalized_original = normalize_ast(strip_docstrings(original_ast))
    normalized_modified = normalize_ast(strip_docstrings(modified_ast))
    if normalized_original == normalized_modified:
        return True, "AST VERIFIED: code structure matches when docstrings are ignored"
    return False, "AST MISMATCH: code structure changed beyond docstrings/comments"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Compare two Python files while ignoring docstring differences.")
    parser.add_argument("before_file", help="Original or snapshot Python file.")
    parser.add_argument("after_file", help="Modified Python file.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    success, message = compare_files(args.before_file, args.after_file)
    print(message)
    if message.startswith("ERROR:"):
        return 2
    return 0 if success else 1


if __name__ == "__main__":
    raise SystemExit(main())

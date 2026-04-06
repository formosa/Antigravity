#!/usr/bin/env python3
"""
Provide AST-level comparison of Python files to verify structural equivalence.

role: structural-validator
entrypoints: main
reads: two python files (snapshot and modified)
writes: stdout (verification status)
external_io: fs (read-only)
state_model: stateless
failure_surface: fs-io, syntax-errors
coupling: minimal
determinism: deterministic
concurrency: thread-safe
"""

from __future__ import annotations

import argparse
import ast
import copy
from pathlib import Path

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
    -------
    str
        file content as string
    """
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin-1")

def strip_docstrings(tree: ast.AST) -> ast.AST:
    """
    Remove docstrings from an AST module, class, or function definition.

    purpose: docstring-insensitive structural normalization
    preconditions: tree is a valid Python AST
    postconditions: returns deep-copied AST with docstrings removed from major nodes
    mutates: none (operates on deep copy)
    reads: tree
    writes: none
    external_io: none
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: depth-first search
    aliasing: returns new AST object (deep copy)
    security: none
    coupling: minimal

    Parameters
    ----------
    tree : ast.AST
        input AST to strip

    Returns
    -------
    ast.AST
        stripped AST copy
    """
    stripped = copy.deepcopy(tree)
    for node in ast.walk(stripped):
        if not isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)):
            continue
        if not getattr(node, "body", None):
            continue
        first_statement = node.body[0]
        # INVARIANT: docstring is the first statement in the body if it is an expression constant string
        if (
            isinstance(first_statement, ast.Expr)
            and isinstance(first_statement.value, ast.Constant)
            and isinstance(first_statement.value.value, str)
        ) or (isinstance(first_statement, ast.Expr) and isinstance(first_statement.value, ast.Str)):
            node.body = node.body[1:]
    return stripped

def normalize_ast(tree: ast.AST) -> str:
    """
    Normalize an AST by stripping location metadata and dumping to a string.

    purpose: location-insensitive AST comparison
    preconditions: tree is a valid Python AST
    postconditions: returns string representation of purged AST
    mutates: tree (resets line/column offsets)
    reads: tree
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
    tree : ast.AST
        AST to normalize

    Returns
    -------
    str
        normalized AST dump string
    """
    for node in ast.walk(tree):
        for attr in ("lineno", "col_offset", "end_lineno", "end_col_offset"):
            if hasattr(node, attr):
                setattr(node, attr, 0)
    return ast.dump(tree, annotate_fields=True, include_attributes=False)

def compare_files(before_path: str | Path, after_path: str | Path) -> tuple[bool, str]:
    """
    Parse two files and compare their ASTs while ignoring docstrings and location.

    purpose: validation of documentation-only changes
    preconditions: both paths exist and are readable
    postconditions: returns (success, message)
    mutates: none
    reads: filesystem
    writes: none
    external_io: fs
    determinism: deterministic
    idempotency: yes
    concurrency: thread-safe
    ordering: sequential parse and compare
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    before_path : str | Path
        path to baseline file
    after_path : str | Path
        path to modified file

    Returns
    -------
    tuple[bool, str]
        (is_structurally_equivalent, status_message)
    """
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
    """
    Parse command-line arguments for the AST comparator.

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
    parser = argparse.ArgumentParser(description="Compare two Python files while ignoring docstring differences.")
    parser.add_argument("before_file", help="Original or snapshot Python file.")
    parser.add_argument("after_file", help="Modified Python file.")
    return parser.parse_args()

def main() -> int:
    """
    Execute the AST comparison workflow from CLI.

    purpose: entrypoint for structural verification
    preconditions: none
    postconditions: outputs result to stdout
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
        exit code (0 for success, 1 for mismatch, 2 for error)
    """
    args = parse_args()
    success, message = compare_files(args.before_file, args.after_file)
    print(message)
    if message.startswith("ERROR:"):
        return 2
    return 0 if success else 1

if __name__ == "__main__":
    raise SystemExit(main())


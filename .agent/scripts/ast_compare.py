"""
AST Comparison Tool Python Script for Docstring Workflow.

Compares two Python files' Abstract Syntax Tree (AST) structures,
ignoring docstrings. Used to verify that docstring-only modifications
have not altered code logic.

Meta
----
Tool Definition : .agent/tools/ast_compare.mdt
Workflow Role   : Safety Gatekeeper / Logic Verifier
Architect       : Antigravity IDE (Adversarial Lead)

Usage
-----
    python ast_compare.py <original_file> <modified_file>

Exit Codes
----------
0 : AST structures match (success)
1 : AST structures differ (failure)
2 : File parsing error
"""

import ast
import copy
import sys
from typing import Tuple


def strip_docstrings(tree: ast.AST) -> ast.AST:
    """
    Remove docstrings from all nodes in an AST.

    Parameters
    ----------
    tree : ast.AST
        Parsed AST to process.

    Returns
    -------
    ast.AST
        Deep copy of AST with docstrings removed.

    Notes
    -----
    Creates a deep copy to preserve the original tree structure.
    Docstrings are the first statement in module/class/function bodies
    when that statement is a string literal (Expr containing Constant).
    Handles Module, ClassDef, FunctionDef, and AsyncFunctionDef nodes.

    Examples
    --------
    >>> source = 'def foo():\\n    ""Docstring""\\n    return 42'
    >>> tree = ast.parse(source)
    >>> stripped = strip_docstrings(tree)
    >>> # Original tree remains unchanged, stripped has no docstring
    """
    tree = copy.deepcopy(tree)

    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            if (node.body and
                isinstance(node.body[0], ast.Expr) and
                isinstance(node.body[0].value, ast.Constant) and
                isinstance(node.body[0].value.value, str)):
                node.body = node.body[1:]

    return tree


def normalize_ast(tree: ast.AST) -> str:
    """
    Convert AST to normalized string representation for comparison.

    Parameters
    ----------
    tree : ast.AST
        Parsed AST to normalize.

    Returns
    -------
    str
        Normalized string dump of the AST.

    Notes
    -----
    Uses ast.dump without line numbers or column offsets to allow
    comparison independent of formatting changes. Zeros out all
    positional attributes in a single traversal for optimal performance.

    Examples
    --------
    >>> source = "x = 1\\ny = 2"
    >>> tree = ast.parse(source)
    >>> normalized = normalize_ast(tree)
    >>> # Returns AST dump with all positional data zeroed
    """
    for node in ast.walk(tree):
        for attr in ('lineno', 'col_offset', 'end_lineno', 'end_col_offset'):
            if hasattr(node, attr):
                setattr(node, attr, 0)

    return ast.dump(tree, annotate_fields=True, include_attributes=False)


def compare_ast(original_path: str, modified_path: str) -> Tuple[bool, str]:
    """
    Compare two Python files' AST structures, ignoring docstrings.

    Parameters
    ----------
    original_path : str
        Path to the original Python file.
    modified_path : str
        Path to the modified Python file.

    Returns
    -------
    success : bool
        True if AST structures match, False otherwise.
    message : str
        Descriptive result message.

    Examples
    --------
    >>> success, msg = compare_ast("original.py", "documented.py")
    >>> print(msg)
    AST VERIFIED: Code structures match (docstrings excluded)
    """
    try:
        with open(original_path, 'r', encoding='utf-8') as f:
            original_source = f.read()
    except Exception as e:
        return False, f"ERROR: Cannot read original file: {e}"

    try:
        with open(modified_path, 'r', encoding='utf-8') as f:
            modified_source = f.read()
    except Exception as e:
        return False, f"ERROR: Cannot read modified file: {e}"

    try:
        original_ast = ast.parse(original_source)
    except SyntaxError as e:
        return False, f"ERROR: Original file has syntax error: {e}"

    try:
        modified_ast = ast.parse(modified_source)
    except SyntaxError as e:
        return False, f"ERROR: Modified file has syntax error: {e}"

    # Strip docstrings from both ASTs
    original_ast = strip_docstrings(original_ast)
    modified_ast = strip_docstrings(modified_ast)

    # Normalize and compare
    original_normalized = normalize_ast(original_ast)
    modified_normalized = normalize_ast(modified_ast)

    if original_normalized == modified_normalized:
        return True, "AST VERIFIED: Code structures match (docstrings excluded)"
    else:
        return False, "AST MISMATCH: Code logic has been altered"


def main() -> int:
    """
    CLI entry point for AST comparison.

    Returns
    -------
    int
        Exit code (0=match, 1=mismatch, 2=error).

    Examples
    --------
    Command line usage:
        $ python ast_compare.py original.py modified.py
        AST VERIFIED: Code structures match (docstrings excluded)
        $ echo $?
        0
    """
    if len(sys.argv) != 3:
        print("Usage: python ast_compare.py <original_file> <modified_file>")
        print("Exit codes: 0=match, 1=mismatch, 2=error")
        return 2

    original_path = sys.argv[1]
    modified_path = sys.argv[2]

    success, message = compare_ast(original_path, modified_path)
    print(message)

    if "ERROR:" in message:
        return 2
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())

"""
Source Code Sanitization Tool.

Surgically removes all docstrings and comments from a Python file while
strictly preserving the formatting, indentation, and layout of the
remaining code.

Features
--------
- Preservation: Keeps Shebangs (#!/...) and Encoding headers (PEP-263).
- Safety: Merges overlapping cut ranges to prevent file corruption.
- Validation: Post-clean syntax checking prevents corrupted output.
- Simulation: Supports --dry-run to preview changes.
- Compatibility: Supports modern and legacy AST string nodes.

Meta
----
Tool Definition : .agent/tools/clean_source.mdt
Workflow Role   : Code Sanitizer / Obfuscator
Architect       : Antigravity IDE (Adversarial Lead)

Usage
-----
    python clean_source.py <target_file> [--dry-run]

Exit Codes
----------
0 : Success (File modified or dry-run completed)
1 : Error (File access, encoding, or parse failure)
"""

import ast
import sys
import tokenize
import re
from io import BytesIO
from typing import List, Tuple


def get_offset(lines: List[str], lineno: int, col_offset: int) -> int:
    """
    Calculate the absolute character offset from (line, col) coordinates.

    Parameters
    ----------
    lines : List[str]
        List of source code lines with line endings preserved.
    lineno : int
        1-indexed line number from AST/tokenizer.
    col_offset : int
        0-indexed column offset within the line.

    Returns
    -------
    int
        Absolute character offset in the full source string.

    Examples
    --------
    >>> lines = ["hello\\n", "world\\n"]
    >>> get_offset(lines, 2, 0)
    6
    """
    offset = sum(len(line) for line in lines[:lineno - 1])
    return offset + col_offset


def merge_intervals(intervals: List[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Merge overlapping or adjacent intervals.

    Critical for safety: prevents double-slicing which corrupts files.

    Parameters
    ----------
    intervals : List[Tuple[int, int]]
        List of (start, end) offset tuples to merge.

    Returns
    -------
    List[Tuple[int, int]]
        Sorted, merged list of non-overlapping intervals.

    Examples
    --------
    >>> merge_intervals([(0, 5), (3, 8), (10, 15)])
    [(0, 8), (10, 15)]
    """
    if not intervals:
        return []

    intervals.sort(key=lambda x: x[0])
    merged = []
    current_start, current_end = intervals[0]

    for next_start, next_end in intervals[1:]:
        if next_start <= current_end:
            current_end = max(current_end, next_end)
        else:
            merged.append((current_start, current_end))
            current_start, current_end = next_start, next_end

    merged.append((current_start, current_end))
    return merged


def get_docstring_ranges(source: str, lines: List[str]) -> List[Tuple[int, int]]:
    """
    Identify start/end offsets for all docstrings using AST.

    Supports both ast.Constant (Py3.8+) and ast.Str (Legacy).

    Parameters
    ----------
    source : str
        Full source code content.
    lines : List[str]
        Source split into lines with endings preserved.

    Returns
    -------
    List[Tuple[int, int]]
        List of (start_offset, end_offset) for each docstring.

    Notes
    -----
    Does not detect PEP 224 attribute docstrings (rarely used).
    """
    cuts = []
    try:
        tree = ast.parse(source)
    except SyntaxError:
        print("WARNING: SyntaxError detected. Docstring removal may be partial.", file=sys.stderr)
        return []

    for node in ast.walk(tree):
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef,
                             ast.AsyncFunctionDef)):
            if (node.body and
                isinstance(node.body[0], ast.Expr)):

                val = node.body[0].value

                is_docstring = False
                if isinstance(val, ast.Constant) and isinstance(val.value, str):
                    is_docstring = True
                elif isinstance(val, ast.Str):
                    is_docstring = True

                if is_docstring:
                    doc_node = node.body[0]

                    if hasattr(doc_node, 'end_lineno') and hasattr(doc_node, 'end_col_offset'):
                        start = get_offset(lines, doc_node.lineno, doc_node.col_offset)
                        end = get_offset(lines, doc_node.end_lineno, doc_node.end_col_offset)
                        cuts.append((start, end))

    return cuts


def get_comment_ranges(source: str, lines: List[str]) -> List[Tuple[int, int]]:
    """
    Identify start/end offsets for all comments using Tokenizer.

    Preserves Shebangs (Line 1) and Encoding Headers (Line 1 or 2).

    Parameters
    ----------
    source : str
        Full source code content.
    lines : List[str]
        Source split into lines with endings preserved.

    Returns
    -------
    List[Tuple[int, int]]
        List of (start_offset, end_offset) for each comment.

    Notes
    -----
    Shebangs and PEP-263 encoding declarations are preserved.
    """
    cuts = []
    source_bytes = source.encode('utf-8')

    encoding_pattern = re.compile(r"coding[:=]\s*[-\w.]+")

    try:
        tokens = tokenize.tokenize(BytesIO(source_bytes).readline)
        for token in tokens:
            if token.type == tokenize.COMMENT:
                if token.start[0] == 1 and token.string.startswith("#!"):
                    continue
                if token.start[0] <= 2 and encoding_pattern.search(token.string):
                    continue

                start = get_offset(lines, token.start[0], token.start[1])
                end = get_offset(lines, token.end[0], token.end[1])
                cuts.append((start, end))
    except tokenize.TokenError:
        pass

    return cuts


def apply_cuts(source: str, cuts: List[Tuple[int, int]]) -> str:
    """
    Remove defined ranges from source string.

    Parameters
    ----------
    source : str
        Original source code.
    cuts : List[Tuple[int, int]]
        Merged intervals to remove.

    Returns
    -------
    str
        Source with specified ranges removed.
    """
    cuts.sort(key=lambda x: x[0], reverse=True)

    modified_source = source
    for start, end in cuts:
        assert start <= end, f"Logic Error: Invalid cut interval ({start}, {end})"
        modified_source = modified_source[:start] + modified_source[end:]

    return modified_source


def collapse_blank_lines(source: str) -> str:
    """
    Collapse consecutive blank lines into a single blank line.

    Parameters
    ----------
    source : str
        Source code with potential multiple consecutive blank lines.

    Returns
    -------
    str
        Source code with collapsed blank lines.

    Examples
    --------
    >>> collapse_blank_lines("x = 1\\n\\n\\n\\ny = 2")
    'x = 1\\n\\ny = 2'
    """
    return re.sub(r'\n\n\n+', '\n\n', source)


def strip_trailing_whitespace(source: str) -> str:
    """
    Remove trailing whitespace from each line.

    Parameters
    ----------
    source : str
        Source code potentially containing trailing whitespace.

    Returns
    -------
    str
        Source with trailing whitespace removed per line.

    Examples
    --------
    >>> strip_trailing_whitespace("x = 5  \\ny = 10  ")
    'x = 5\\ny = 10'
    """
    return '\n'.join(line.rstrip() for line in source.splitlines())


def validate_syntax(source: str) -> bool:
    """
    Verify cleaned source is syntactically valid Python.

    Parameters
    ----------
    source : str
        Cleaned source code to validate.

    Returns
    -------
    bool
        True if source compiles without SyntaxError, False otherwise.

    Examples
    --------
    >>> validate_syntax("x = 1\\ny = 2")
    True
    >>> validate_syntax("x = ")
    False
    """
    try:
        compile(source, '<string>', 'exec')
        return True
    except SyntaxError:
        return False


def main() -> int:
    """
    Main entry point for source code sanitization.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    if len(sys.argv) < 2:
        print("Usage: python clean_source.py <target_file> [--dry-run]", file=sys.stderr)
        return 1

    target_path = sys.argv[1]
    dry_run = "--dry-run" in sys.argv

    try:
        content = ""
        encoding = 'utf-8'
        try:
            with open(target_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            with open(target_path, 'r', encoding='latin-1') as f:
                content = f.read()
            encoding = 'latin-1'

        lines = content.splitlines(keepends=True)

        doc_cuts = get_docstring_ranges(content, lines)
        comment_cuts = get_comment_ranges(content, lines)

        all_cuts = doc_cuts + comment_cuts
        final_cuts = merge_intervals(all_cuts)

        clean_source = apply_cuts(content, final_cuts)
        clean_source = collapse_blank_lines(clean_source)
        clean_source = strip_trailing_whitespace(clean_source)

        if not validate_syntax(clean_source):
            print("ERROR: Cleaned source has syntax errors. Aborting write.", file=sys.stderr)
            print("--- CORRUPTED OUTPUT (NOT WRITTEN) ---", file=sys.stderr)
            print(clean_source, file=sys.stderr)
            print("--- END CORRUPTED OUTPUT ---", file=sys.stderr)
            return 1

        if dry_run:
            print("--- DRY RUN: PREVIEW OF OUTPUT ---")
            print(clean_source)
            print("--- END PREVIEW ---")
        else:
            with open(target_path, 'w', encoding=encoding) as f:
                f.write(clean_source)
            print(f"SUCCESS: Cleaned {target_path}")

        return 0

    except Exception as e:
        print(f"ERROR: Failed to clean source: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

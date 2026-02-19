"""
Structural entropy analysis for Python source code.

This module computes a set of deterministic, architecture-level entropy
metrics using Python's Abstract Syntax Tree (AST).

Entropy, in this context, is defined as the degree to which a codebase
exhibits:
- Non-linear control flow
- Implicit behavioral branching
- Excessive nesting
- Overloaded functional responsibility
- Poor locality of reasoning

The metrics produced by this module are intended to be:
- Stable across executions
- Comparable across refactors
- Resistant to superficial formatting changes
- Actionable for automated refactoring systems

No dynamic analysis is performed.
"""
from __future__ import annotations

import ast
from dataclasses import dataclass, asdict
from typing import Iterable

# ---------------------------------------------------------------------------
# Configuration constants for normalization
# ---------------------------------------------------------------------------
MAX_ALLOWED_COMPLEXITY = 50
MAX_ALLOWED_NESTING_DEPTH = 10
MAX_ALLOWED_BRANCH_DENSITY = 0.5
MAX_ALLOWED_FUNCTION_LENGTH = 50

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------
@dataclass(frozen=True)
class FunctionEntropyMetrics:
    """
    Entropy metrics for a single function.
    
    Attributes
    ----------
    function_name : str
        Name of the function.
    line_start : int
        Starting line number (1-indexed).
    line_end : int
        Ending line number (1-indexed).
    branch_count : int
        Number of branching constructs in this function.
    nesting_depth : int
        Maximum nesting depth within this function.
    boolean_op_count : int
        Number of boolean operators in this function.
    statement_count : int
        Number of statements in the function body.
    normalized_score : float
        Normalized entropy score for this function (0.0 to 1.0).
    """
    function_name: str
    line_start: int
    line_end: int
    branch_count: int
    nesting_depth: int
    boolean_op_count: int
    statement_count: int
    normalized_score: float
    
    def to_dict(self) -> dict:
        """Return JSON-serializable representation."""
        return asdict(self)
    
    def is_high_entropy(self, threshold: float = 0.4) -> bool:
        """Check if function entropy exceeds threshold."""
        return self.normalized_score > threshold


@dataclass(frozen=True)
class EntropyMetrics:
    """
    Immutable container for entropy metrics.

    Attributes
    ----------
    function_count : int
        Number of function definitions.
    class_count : int
        Number of class definitions.
    branch_count : int
        Number of explicit branching constructs (if/for/while/match).
    boolean_op_count : int
        Number of boolean operators (and/or).
    exception_handler_count : int
        Number of except blocks.
    max_nesting_depth : int
        Maximum AST nesting depth.
    total_nodes : int
        Total number of AST nodes.
    average_function_length : float
        Mean number of statements per function body.
    normalized_score : float
        Normalized entropy score from 0.0 (low entropy) to 1.0 (high entropy).
        As defined in entropy_reduction_doctrine.md.
    """

    function_count: int
    class_count: int
    branch_count: int
    boolean_op_count: int
    exception_handler_count: int
    max_nesting_depth: int
    total_nodes: int
    average_function_length: float
    normalized_score: float

    def to_dict(self) -> dict:
        """Return a JSON-serializable representation."""
        return asdict(self)

    def is_high_entropy(self, threshold: float = 0.4) -> bool:
        """
        Check if the normalized score exceeds the entropy threshold.

        Parameters
        ----------
        threshold : float
            Maximum acceptable entropy score (default: 0.4 per doctrine).

        Returns
        -------
        bool
            True if entropy exceeds threshold.
        """
        return self.normalized_score > threshold

# ---------------------------------------------------------------------------
# AST Visitor
# ---------------------------------------------------------------------------
class _EntropyVisitor(ast.NodeVisitor):
    """
    AST visitor that collects raw entropy signals.

    This class is intentionally private and stateful.
    Aggregation and interpretation occur elsewhere.
    """

    __slots__ = (
        "_function_lengths",
        "function_count",
        "class_count",
        "branch_count",
        "boolean_op_count",
        "exception_handler_count",
        "total_nodes",
        "max_nesting_depth",
        "current_depth",
    )

    def __init__(self) -> None:
        self._function_lengths: list[int] = []
        self.function_count = 0
        self.class_count = 0
        self.branch_count = 0
        self.boolean_op_count = 0
        self.exception_handler_count = 0
        self.total_nodes = 0
        self.max_nesting_depth = 0
        self.current_depth = 0

    # ---- Core traversal ----------------------------------------------------

    def generic_visit(self, node: ast.AST) -> None:
        self.total_nodes += 1
        self.max_nesting_depth = max(self.max_nesting_depth, self.current_depth)
        self.current_depth += 1
        for field, value in ast.iter_fields(node):
            if isinstance(value, list):
                for item in value:
                    if isinstance(item, ast.AST):
                        self.visit(item)
            elif isinstance(value, ast.AST):
                self.visit(value)
        self.current_depth -= 1

    # ---- Structural elements -----------------------------------------------

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        self.function_count += 1
        self._function_lengths.append(len(node.body))
        self.generic_visit(node)

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        self.function_count += 1
        self._function_lengths.append(len(node.body))
        self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        self.class_count += 1
        self.generic_visit(node)

    # ---- Control flow ------------------------------------------------------

    def visit_If(self, node: ast.If) -> None:
        self.branch_count += 1
        self.generic_visit(node)

    def visit_For(self, node: ast.For) -> None:
        self.branch_count += 1
        self.generic_visit(node)

    def visit_While(self, node: ast.While) -> None:
        self.branch_count += 1
        self.generic_visit(node)

    def visit_Match(self, node: ast.Match) -> None:
        # Python 3.10+ structural pattern matching
        self.branch_count += 1
        self.generic_visit(node)

    # ---- Logical complexity ------------------------------------------------

    def visit_BoolOp(self, node: ast.BoolOp) -> None:
        self.boolean_op_count += 1
        self.generic_visit(node)

    # ---- Error handling ----------------------------------------------------

    def visit_ExceptHandler(self, node: ast.ExceptHandler) -> None:
        self.exception_handler_count += 1
        self.generic_visit(node)

# ---------------------------------------------------------------------------
# Normalization logic
# ---------------------------------------------------------------------------
def _clamp(value: float, min_val: float = 0.0, max_val: float = 1.0) -> float:
    """Clamp a value to the specified range."""
    return max(min_val, min(max_val, value))

def _compute_normalized_score(
    branch_count: int,
    boolean_op_count: int,
    exception_handler_count: int,
    max_nesting_depth: int,
    total_nodes: int,
    average_function_length: float,
) -> float:
    """
    Compute a normalized entropy score from 0.0 to 1.0.

    The score is a weighted combination of multiple factors:
    - Complexity factor (30%): Combined branching and boolean complexity
    - Nesting factor (25%): Maximum nesting depth relative to threshold
    - Branch density factor (25%): Ratio of branches to total nodes
    - Function length factor (20%): Average function length relative to max

    Parameters
    ----------
    branch_count : int
        Number of branching constructs.
    boolean_op_count : int
        Number of boolean operators.
    exception_handler_count : int
        Number of exception handlers.
    max_nesting_depth : int
        Maximum AST nesting depth.
    total_nodes : int
        Total number of AST nodes.
    average_function_length : float
        Mean statements per function.

    Returns
    -------
    float
        Normalized score in range [0.0, 1.0].
    """
    # Complexity: combined count of branching elements
    raw_complexity = branch_count + boolean_op_count + exception_handler_count
    complexity_factor = _clamp(raw_complexity / MAX_ALLOWED_COMPLEXITY)

    # Nesting depth relative to maximum allowed
    nesting_factor = _clamp(max_nesting_depth / MAX_ALLOWED_NESTING_DEPTH)

    # Branch density: ratio of branches to total code volume
    if total_nodes > 0:
        branch_density = branch_count / total_nodes
        branch_density_factor = _clamp(branch_density / MAX_ALLOWED_BRANCH_DENSITY)
    else:
        branch_density_factor = 0.0

    # Function length relative to maximum allowed
    function_length_factor = _clamp(
        average_function_length / MAX_ALLOWED_FUNCTION_LENGTH
    )

    # Weighted combination
    normalized_score = (
        complexity_factor * 0.30
        + nesting_factor * 0.25
        + branch_density_factor * 0.25
        + function_length_factor * 0.20
    )

    return round(_clamp(normalized_score), 4)

# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------
def compute_entropy(tree: ast.AST) -> EntropyMetrics:
    """
    Compute structural entropy metrics for a Python AST.

    Parameters
    ----------
    tree : ast.AST
        Parsed Python abstract syntax tree.

    Returns
    -------
    EntropyMetrics
        Immutable entropy metrics snapshot with normalized score.
    """
    visitor = _EntropyVisitor()
    visitor.visit(tree)

    avg_func_len = (
        sum(visitor._function_lengths) / len(visitor._function_lengths)
        if visitor._function_lengths
        else 0.0
    )

    normalized_score = _compute_normalized_score(
        branch_count=visitor.branch_count,
        boolean_op_count=visitor.boolean_op_count,
        exception_handler_count=visitor.exception_handler_count,
        max_nesting_depth=visitor.max_nesting_depth,
        total_nodes=visitor.total_nodes,
        average_function_length=avg_func_len,
    )

    return EntropyMetrics(
        function_count=visitor.function_count,
        class_count=visitor.class_count,
        branch_count=visitor.branch_count,
        boolean_op_count=visitor.boolean_op_count,
        exception_handler_count=visitor.exception_handler_count,
        max_nesting_depth=visitor.max_nesting_depth,
        total_nodes=visitor.total_nodes,
        average_function_length=round(avg_func_len, 2),
        normalized_score=normalized_score,
    )

# ---------------------------------------------------------------------------
# Convenience helpers
# ---------------------------------------------------------------------------
def compute_entropy_from_source(source: str) -> EntropyMetrics:
    """
    Compute entropy metrics directly from source code.

    Parameters
    ----------
    source : str
        Python source code.

    Returns
    -------
    EntropyMetrics
    """
    tree = ast.parse(source)
    return compute_entropy(tree)

def compute_entropy_from_file(path: str) -> EntropyMetrics:
    """
    Compute entropy metrics from a Python file.

    Parameters
    ----------
    path : str
        Path to .py file.

    Returns
    -------
    EntropyMetrics
    """
    with open(path, "r", encoding="utf-8") as f:
        source = f.read()
    return compute_entropy_from_source(source)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------
def main(argv: list[str] | None = None) -> int:
    """
    Command-line interface for entropy analysis.

    Usage
    -----
    python analyze_entropy.py <file.py>

    Parameters
    ----------
    argv : list[str] | None
        Command-line arguments. Uses sys.argv[1:] if None.

    Returns
    -------
    int
        Exit code (0=success, 1=analysis error, 2=usage error).
    """
    import sys
    import json
    from pathlib import Path

    argv = argv or sys.argv[1:]
    if not argv:
        print(f"Usage: {Path(__file__).name} <file.py>", file=sys.stderr)
        return 2

    path = Path(argv[0])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        return 2

    if not path.suffix == ".py":
        print(f"Warning: {path} does not have .py extension", file=sys.stderr)

    try:
        metrics = compute_entropy_from_file(str(path))
        output = metrics.to_dict()
        output["file_path"] = str(path)
        print(json.dumps(output, indent=2))
        
        # Return non-zero if high entropy detected
        if metrics.is_high_entropy():
            print(f"\n[WARNING] High entropy detected: {metrics.normalized_score:.4f}", file=sys.stderr)
            return 1
        return 0
    except SyntaxError as e:
        print(f"Syntax error in {path}: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error analyzing {path}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())


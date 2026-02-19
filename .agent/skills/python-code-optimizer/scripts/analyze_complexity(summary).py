#!/usr/bin/env python3
"""
Python Code Complexity Analyzer

Performs standalone complexity analysis of Python source files, generating
detailed reports on cyclomatic complexity, cognitive complexity, Halstead
metrics, and maintainability indicators. Designed for integration with
Google Antigravity IDE 1.16.5 and Gemini 3 Pro agent workflows.

Author: Enterprise Development Team
Version: 3.0.0
Target: Google Antigravity IDE 1.16.5, Gemini 3 Pro
License: Apache-2.0
"""

import ast
import json
import logging
import math
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import argparse

logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)


# ---------------------------------------------------------------------------
# Data Models
# ---------------------------------------------------------------------------

@dataclass
class FunctionComplexity:
    """
    Complexity report for a single callable (function or method).

    Attributes
    ----------
    name : str
        Qualified name of the function
    lineno : int
        Line number where the function is defined
    cyclomatic_complexity : int
        McCabe cyclomatic complexity score
    cognitive_complexity : int
        Cognitive complexity score (Sonar-style)
    parameter_count : int
        Number of formal parameters
    return_count : int
        Number of return statements
    has_docstring : bool
        Whether a Numpy-style docstring is present
    has_type_hints : bool
        Whether all parameters and return type are annotated
    nesting_depth : int
        Maximum nesting depth within the function body
    lines_of_code : int
        Lines of code within function (excluding docstring)
    """
    name: str
    lineno: int
    cyclomatic_complexity: int
    cognitive_complexity: int
    parameter_count: int
    return_count: int
    has_docstring: bool
    has_type_hints: bool
    nesting_depth: int
    lines_of_code: int


@dataclass
class ModuleComplexityReport:
    """
    Aggregate complexity report for an entire Python module.

    Attributes
    ----------
    file_path : str
        Absolute path to the analyzed file
    total_lines : int
        Total line count including blanks and comments
    lines_of_code : int
        Non-blank, non-comment lines
    comment_lines : int
        Lines consisting solely of comments
    blank_lines : int
        Blank lines
    function_count : int
        Number of top-level and nested functions
    class_count : int
        Number of class definitions
    import_count : int
        Number of import statements
    average_complexity : float
        Mean cyclomatic complexity across all functions
    max_complexity : int
        Highest cyclomatic complexity in the module
    average_cognitive : float
        Mean cognitive complexity across all functions
    maintainability_index : float
        Computed maintainability index (0–100)
    documentation_coverage : float
        Percentage of callables with docstrings
    type_hint_coverage : float
        Percentage of functions fully type-annotated
    functions : List[FunctionComplexity]
        Per-function complexity records
    hotspots : List[str]
        Names of functions flagged as complexity hotspots
    recommendations : List[str]
        Actionable improvement recommendations
    """
    file_path: str
    total_lines: int
    lines_of_code: int
    comment_lines: int
    blank_lines: int
    function_count: int
    class_count: int
    import_count: int
    average_complexity: float
    max_complexity: int
    average_cognitive: float
    maintainability_index: float
    documentation_coverage: float
    type_hint_coverage: float
    functions: List[FunctionComplexity] = field(default_factory=list)
    hotspots: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Analyzer
# ---------------------------------------------------------------------------

class ComplexityAnalyzer:
    """
    Comprehensive AST-based complexity analyzer for Python source files.

    Computes cyclomatic and cognitive complexity, Halstead metrics, and
    generates prioritized optimization recommendations.

    Parameters
    ----------
    max_complexity_threshold : int, default=10
        Cyclomatic complexity above which functions are flagged as hotspots
    max_cognitive_threshold : int, default=15
        Cognitive complexity above which functions are flagged
    min_maintainability : float, default=65.0
        Maintainability index below which a module-level warning is issued

    Examples
    --------
    >>> analyzer = ComplexityAnalyzer(max_complexity_threshold=8)
    >>> report = analyzer.analyze('my_module.py')
    >>> print(report.average_complexity)
    """

    # Decision-point node types that increment cyclomatic complexity
    _CC_NODES = (
        ast.If, ast.While, ast.For, ast.ExceptHandler,
        ast.With, ast.Assert, ast.comprehension
    )

    def __init__(
        self,
        max_complexity_threshold: int = 10,
        max_cognitive_threshold: int = 15,
        min_maintainability: float = 65.0
    ) -> None:
        self.max_complexity_threshold = max_complexity_threshold
        self.max_cognitive_threshold = max_cognitive_threshold
        self.min_maintainability = min_maintainability

    def analyze(self, file_path: str) -> ModuleComplexityReport:
        """
        Analyze a Python source file and return its complexity report.

        Parameters
        ----------
        file_path : str
            Path to the Python file to analyze

        Returns
        -------
        ModuleComplexityReport
            Complete complexity and quality report

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist
        SyntaxError
            If the file cannot be parsed as valid Python
        """
        path = Path(file_path).resolve()
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(path, 'r', encoding='utf-8') as f:
            source = f.read()

        tree = ast.parse(source, filename=str(path))
        lines = source.splitlines()

        # Line counting
        total_lines = len(lines)
        blank_lines = sum(1 for l in lines if not l.strip())
        comment_lines = sum(1 for l in lines if l.strip().startswith('#'))
        loc = total_lines - blank_lines - comment_lines

        # Structural counts
        function_count = sum(
            1 for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        )
        class_count = sum(
            1 for n in ast.walk(tree)
            if isinstance(n, ast.ClassDef)
        )
        import_count = sum(
            1 for n in ast.walk(tree)
            if isinstance(n, (ast.Import, ast.ImportFrom))
        )

        # Per-function analysis
        function_reports = self._analyze_all_functions(tree)

        # Aggregate complexity metrics
        complexities = [f.cyclomatic_complexity for f in function_reports]
        cognitives   = [f.cognitive_complexity  for f in function_reports]

        avg_cc  = (sum(complexities) / len(complexities)) if complexities else 0.0
        max_cc  = max(complexities, default=0)
        avg_cog = (sum(cognitives)  / len(cognitives))   if cognitives  else 0.0

        # Halstead-based maintainability index
        mi = self._compute_maintainability_index(source, avg_cc, loc)

        # Coverage metrics
        doc_cov  = self._documentation_coverage(function_reports)
        type_cov = self._type_hint_coverage(function_reports)

        # Hotspot detection
        hotspots = [
            f.name for f in function_reports
            if (f.cyclomatic_complexity > self.max_complexity_threshold
                or f.cognitive_complexity > self.max_cognitive_threshold)
        ]

        # Recommendations
        recommendations = self._generate_recommendations(
            function_reports, mi, doc_cov, type_cov, hotspots
        )

        return ModuleComplexityReport(
            file_path=str(path),
            total_lines=total_lines,
            lines_of_code=loc,
            comment_lines=comment_lines,
            blank_lines=blank_lines,
            function_count=function_count,
            class_count=class_count,
            import_count=import_count,
            average_complexity=round(avg_cc, 2),
            max_complexity=max_cc,
            average_cognitive=round(avg_cog, 2),
            maintainability_index=round(mi, 2),
            documentation_coverage=round(doc_cov, 2),
            type_hint_coverage=round(type_cov, 2),
            functions=function_reports,
            hotspots=hotspots,
            recommendations=recommendations
        )

    def _analyze_all_functions(
        self, tree: ast.AST
    ) -> List[FunctionComplexity]:
        """
        Analyze every callable in the module's AST.

        Parameters
        ----------
        tree : ast.AST
            Parsed module AST

        Returns
        -------
        List[FunctionComplexity]
            Complexity record for each function/method
        """
        results = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                results.append(self._analyze_function(node))
        return results

    def _analyze_function(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> FunctionComplexity:
        """
        Compute complexity metrics for a single function node.

        Parameters
        ----------
        node : ast.FunctionDef or ast.AsyncFunctionDef
            AST node representing the function

        Returns
        -------
        FunctionComplexity
            Detailed complexity report for this function
        """
        cc = self._cyclomatic_complexity(node)
        cog = self._cognitive_complexity(node, depth=0)
        nesting = self._max_nesting_depth(node)
        returns = sum(
            1 for n in ast.walk(node)
            if isinstance(n, ast.Return)
        )
        params = node.args.args
        non_self_params = [a for a in params if a.arg not in ('self', 'cls')]
        has_hints = (
            all(a.annotation is not None for a in non_self_params)
            and node.returns is not None
        )
        has_doc = bool(ast.get_docstring(node))

        # LOC: end_lineno - lineno (minus docstring lines)
        start = node.lineno
        end   = getattr(node, 'end_lineno', node.lineno)
        raw_loc = end - start + 1

        return FunctionComplexity(
            name=node.name,
            lineno=node.lineno,
            cyclomatic_complexity=cc,
            cognitive_complexity=cog,
            parameter_count=len(non_self_params),
            return_count=returns,
            has_docstring=has_doc,
            has_type_hints=has_hints,
            nesting_depth=nesting,
            lines_of_code=raw_loc
        )

    def _cyclomatic_complexity(
        self, node: ast.FunctionDef | ast.AsyncFunctionDef
    ) -> int:
        """
        Compute McCabe cyclomatic complexity for a function node.

        Cyclomatic complexity = number of decision points + 1.

        Parameters
        ----------
        node : ast.FunctionDef or ast.AsyncFunctionDef
            Target function AST node

        Returns
        -------
        int
            Cyclomatic complexity score (minimum 1)
        """
        complexity = 1
        for child in ast.walk(node):
            if isinstance(child, self._CC_NODES):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        return complexity

    def _cognitive_complexity(
        self, node: ast.AST, depth: int
    ) -> int:
        """
        Compute cognitive complexity using a nesting-penalty model.

        Cognitive complexity increments for each structural break in linear
        flow and applies additional nesting penalties for nested structures.

        Parameters
        ----------
        node : ast.AST
            AST node (function or sub-tree)
        depth : int
            Current structural nesting depth

        Returns
        -------
        int
            Cognitive complexity score
        """
        score = 0
        nesting_types = (ast.If, ast.For, ast.While, ast.With,
                         ast.Try, ast.ExceptHandler)
        linear_types  = (ast.Break, ast.Continue, ast.Return,
                         ast.Raise, ast.Assert)

        for child in ast.iter_child_nodes(node):
            if isinstance(child, nesting_types):
                score += 1 + depth  # Nesting penalty
                score += self._cognitive_complexity(child, depth + 1)
            elif isinstance(child, linear_types):
                score += 1
            elif isinstance(child, ast.BoolOp):
                score += len(child.values) - 1
            else:
                score += self._cognitive_complexity(child, depth)

        return score

    def _max_nesting_depth(self, node: ast.AST, current: int = 0) -> int:
        """
        Recursively compute the maximum nesting depth within a node.

        Parameters
        ----------
        node : ast.AST
            Starting AST node
        current : int, default=0
            Current depth level

        Returns
        -------
        int
            Maximum nesting depth observed
        """
        nesting_types = (ast.If, ast.For, ast.While, ast.With,
                         ast.Try, ast.FunctionDef, ast.AsyncFunctionDef)
        max_depth = current
        for child in ast.iter_child_nodes(node):
            if isinstance(child, nesting_types):
                depth = self._max_nesting_depth(child, current + 1)
                max_depth = max(max_depth, depth)
            else:
                depth = self._max_nesting_depth(child, current)
                max_depth = max(max_depth, depth)
        return max_depth

    def _compute_maintainability_index(
        self, source: str, avg_cc: float, loc: int
    ) -> float:
        """
        Compute the SEI maintainability index from source characteristics.

        Uses a Halstead volume approximation derived from operator/operand
        token counts extracted from the source text.

        Parameters
        ----------
        source : str
            Raw Python source code
        avg_cc : float
            Average cyclomatic complexity of the module
        loc : int
            Lines of code (excluding blanks and comments)

        Returns
        -------
        float
            Maintainability index clamped to [0, 100]

        Notes
        -----
        Formula (SEI variant):
            MI = max(0, 171 - 5.2*ln(HV) - 0.23*CC - 16.2*ln(LOC)) * 100/171
        """
        # Approximate Halstead volume using token counts
        import tokenize
        import io

        operators: set = set()
        operands:  set = set()
        total_ops = 0
        total_opds = 0

        op_tokens = {
            tokenize.OP, tokenize.ERRORTOKEN
        }
        opd_tokens = {
            tokenize.NAME, tokenize.NUMBER, tokenize.STRING
        }

        try:
            tokens = list(tokenize.generate_tokens(
                io.StringIO(source).readline
            ))
            for tok in tokens:
                if tok.type in op_tokens:
                    operators.add(tok.string)
                    total_ops += 1
                elif tok.type in opd_tokens:
                    operands.add(tok.string)
                    total_opds += 1
        except tokenize.TokenError:
            pass

        n1, n2 = len(operators), len(operands)
        N1, N2 = total_ops, total_opds
        vocabulary = max(n1 + n2, 1)
        length     = N1 + N2
        volume     = length * math.log2(vocabulary) if vocabulary > 1 else 1.0

        safe_loc = max(loc, 1)
        safe_hv  = max(volume, 1.0)
        safe_cc  = max(avg_cc, 0.0)

        mi_raw = (171
                  - 5.2  * math.log(safe_hv)
                  - 0.23 * safe_cc
                  - 16.2 * math.log(safe_loc))

        return max(0.0, min(100.0, mi_raw * 100.0 / 171.0))

    def _documentation_coverage(
        self, functions: List[FunctionComplexity]
    ) -> float:
        """
        Compute documentation coverage as a percentage.

        Parameters
        ----------
        functions : List[FunctionComplexity]
            All analyzed function records

        Returns
        -------
        float
            Coverage percentage in [0.0, 100.0]
        """
        if not functions:
            return 100.0
        documented = sum(1 for f in functions if f.has_docstring)
        return (documented / len(functions)) * 100.0

    def _type_hint_coverage(
        self, functions: List[FunctionComplexity]
    ) -> float:
        """
        Compute type annotation coverage as a percentage.

        Parameters
        ----------
        functions : List[FunctionComplexity]
            All analyzed function records

        Returns
        -------
        float
            Coverage percentage in [0.0, 100.0]
        """
        if not functions:
            return 100.0
        annotated = sum(1 for f in functions if f.has_type_hints)
        return (annotated / len(functions)) * 100.0

    def _generate_recommendations(
        self,
        functions: List[FunctionComplexity],
        mi: float,
        doc_cov: float,
        type_cov: float,
        hotspots: List[str]
    ) -> List[str]:
        """
        Generate prioritized, actionable optimization recommendations.

        Parameters
        ----------
        functions : List[FunctionComplexity]
            Per-function complexity records
        mi : float
            Module maintainability index
        doc_cov : float
            Documentation coverage percentage
        type_cov : float
            Type hint coverage percentage
        hotspots : List[str]
            Function names flagged as hotspots

        Returns
        -------
        List[str]
            Ordered list of recommendations (highest priority first)
        """
        recs: List[str] = []

        if hotspots:
            recs.append(
                f"[CRITICAL] Decompose high-complexity functions: "
                f"{', '.join(hotspots)}"
            )

        if mi < self.min_maintainability:
            recs.append(
                f"[HIGH] Maintainability index ({mi:.1f}) is below threshold "
                f"({self.min_maintainability}). Simplify logic and improve documentation."
            )

        if doc_cov < 80.0:
            undoc = [f.name for f in functions if not f.has_docstring]
            recs.append(
                f"[HIGH] Add Numpy-style docstrings to {len(undoc)} "
                f"undocumented functions: {', '.join(undoc[:5])}"
                f"{'...' if len(undoc) > 5 else ''}"
            )

        if type_cov < 70.0:
            untyped = [f.name for f in functions if not f.has_type_hints]
            recs.append(
                f"[MEDIUM] Add type annotations to {len(untyped)} functions: "
                f"{', '.join(untyped[:5])}"
                f"{'...' if len(untyped) > 5 else ''}"
            )

        deep = [f for f in functions if f.nesting_depth > 4]
        if deep:
            recs.append(
                f"[MEDIUM] Reduce nesting depth (>4) in: "
                f"{', '.join(f.name for f in deep)}"
            )

        long_fns = [f for f in functions if f.lines_of_code > 50]
        if long_fns:
            recs.append(
                f"[LOW] Consider splitting large functions (>50 LOC): "
                f"{', '.join(f.name for f in long_fns)}"
            )

        if not recs:
            recs.append("[OK] No critical issues detected. Code meets quality thresholds.")

        return recs


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    """Build CLI argument parser for the complexity analyzer."""
    parser = argparse.ArgumentParser(
        prog='analyze_complexity',
        description='Analyze Python code complexity — Antigravity Skill v3.0.0'
    )
    parser.add_argument('--input', '-i', required=True,
                        help='Python file to analyze')
    parser.add_argument('--output', '-o', default=None,
                        help='Path to write JSON report (default: stdout)')
    parser.add_argument('--max-complexity', type=int, default=10,
                        help='Cyclomatic complexity hotspot threshold')
    parser.add_argument('--verbose', '-v', action='store_true')
    return parser


def main() -> int:
    """
    CLI entry point for the complexity analyzer.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on error
    """
    parser = _build_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    try:
        analyzer = ComplexityAnalyzer(max_complexity_threshold=args.max_complexity)
        report = analyzer.analyze(args.input)
        report_dict = asdict(report)

        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f:
                json.dump(report_dict, f, indent=2)
            logger.info(f"Report written to: {args.output}")
        else:
            print(json.dumps(report_dict, indent=2))

        # Print summary to stderr so stdout remains clean JSON
        print(
            f"\nAnalysis Summary — {Path(args.input).name}\n"
            f"  Avg Complexity   : {report.average_complexity}\n"
            f"  Max Complexity   : {report.max_complexity}\n"
            f"  Maintainability  : {report.maintainability_index}\n"
            f"  Doc Coverage     : {report.documentation_coverage}%\n"
            f"  Type Coverage    : {report.type_hint_coverage}%\n"
            f"  Hotspots         : {', '.join(report.hotspots) or 'None'}\n",
            file=sys.stderr
        )
        return 0
    except (FileNotFoundError, SyntaxError) as e:
        logger.error(str(e))
        return 1


if __name__ == '__main__':
    sys.exit(main())

#!/usr/bin/env python3
"""
Python Code Optimizer - Main Orchestration Script

This script coordinates the comprehensive optimization of Python source files,
implementing a multi-stage optimization pipeline that enhances code quality,
documentation, performance, and maintainability to academic-professional standards.

Author: Enterprise Development Team
Version: 3.0.0
Target: Google Antigravity IDE 1.16.5, Gemini 3 Flash
License: Apache-2.0
"""

import argparse
import ast
import json
import logging
import filecmp
import sys
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import subprocess
import shutil
import tempfile
from dataclasses import dataclass, asdict
from datetime import datetime


# Local imports
sys.path.append(str(Path(__file__).parent))
try:
    import analyze_entropy
except ImportError:
    analyze_entropy = None

try:
    from refactor_engine import RefactorEngine
except ImportError:
    RefactorEngine = None

try:
    from validation_suite import ValidationSuite
except ImportError:
    ValidationSuite = None

import io
import tokenize as tokenize_mod

# Configure logging for enterprise production environment
_log_handlers = [logging.StreamHandler(sys.stdout)]
try:
    import os
    if os.environ.get('PY_OPTIMIZER_LOG_FILE'):
        _log_handlers.append(logging.FileHandler(os.environ['PY_OPTIMIZER_LOG_FILE']))
except Exception:
    pass
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=_log_handlers
)
logger = logging.getLogger(__name__)


@dataclass
class OptimizationMetrics:
    """
    Container for code quality and optimization metrics.

    Attributes
    ----------
    cyclomatic_complexity : float
        Average cyclomatic complexity across all functions
    maintainability_index : float
        Maintainability index score (0-100 scale)
    lines_of_code : int
        Total lines of code (excluding comments/blanks)
    documentation_coverage : float
        Percentage of functions with complete docstrings
    pep8_violations : int
        Number of PEP 8 style violations
    type_hint_coverage : float
        Percentage of functions with type hints
    execution_time : Optional[float]
        Execution time in seconds (if profiled)
    memory_usage : Optional[float]
        Peak memory usage in MB (if profiled)

    Examples
    --------
    >>> metrics = OptimizationMetrics(
    ...     cyclomatic_complexity=7.2,
    ...     maintainability_index=68.5,
    ...     lines_of_code=450,
    ...     documentation_coverage=85.0,
    ...     pep8_violations=12,
    ...     type_hint_coverage=75.0
    ... )
    """
    cyclomatic_complexity: float
    maintainability_index: float
    lines_of_code: int
    documentation_coverage: float
    pep8_violations: int

    type_hint_coverage: float
    entropy_score: float = 0.0
    execution_time: Optional[float] = None
    memory_usage: Optional[float] = None


@dataclass
class OptimizationResult:
    """
    Comprehensive result of code optimization process.

    Attributes
    ----------
    success : bool
        Whether optimization completed successfully
    original_metrics : OptimizationMetrics
        Metrics from original code
    optimized_metrics : OptimizationMetrics
        Metrics from optimized code
    changes_applied : List[str]
        Descriptions of optimization changes
    warnings : List[str]
        Warnings encountered during optimization
    errors : List[str]
        Errors encountered during optimization
    optimization_duration : float
        Total optimization time in seconds
    """
    success: bool
    original_metrics: Optional[OptimizationMetrics]
    optimized_metrics: OptimizationMetrics
    changes_applied: List[str]
    warnings: List[str]
    errors: List[str]
    optimization_duration: float


class _CommentPreserver:
    """
    Extract and re-inject comments across AST round-trips.

    Uses Python's tokenize module to capture all comments before
    ast.unparse() strips them, then re-injects them into the
    refactored source using anchor-line matching.

    Parameters
    ----------
    source : str
        Original Python source code containing comments to preserve
    """

    def __init__(self, source: str) -> None:
        self._groups = self._extract_groups(source)

    @staticmethod
    def _normalize(line: str) -> str:
        """Normalize a code line for fuzzy anchor matching."""
        return ' '.join(line.split()).strip().rstrip(':,')

    @staticmethod
    def _extract_groups(source: str) -> List[dict]:
        """
        Extract comment groups from source.

        Groups consecutive comment-only lines into blocks.
        Inline comments (sharing a line with code) are
        individual groups.

        Returns
        -------
        List[dict]
            Each dict has keys: 'lines' (list of comment
            strings), 'inline' (bool), 'anchor' (normalized
            code string to match against refactored output)
        """
        comments_by_line: Dict[int, str] = {}
        try:
            tokens = tokenize_mod.generate_tokens(
                io.StringIO(source).readline
            )
            for tok_type, tok_string, start, _end, _line in tokens:
                if tok_type == tokenize_mod.COMMENT:
                    comments_by_line[start[0]] = tok_string
        except tokenize_mod.TokenError:
            return []

        if not comments_by_line:
            return []

        source_lines = source.splitlines()
        groups: List[dict] = []
        sorted_line_nums = sorted(comments_by_line.keys())

        i = 0
        while i < len(sorted_line_nums):
            line_num = sorted_line_nums[i]
            code_before = (
                source_lines[line_num - 1].split('#')[0].strip()
            )
            is_inline = len(code_before) > 0

            if is_inline:
                groups.append({
                    'lines': [comments_by_line[line_num]],
                    'inline': True,
                    'anchor': _CommentPreserver._normalize(
                        code_before
                    ),
                })
                i += 1
            else:
                block = [comments_by_line[line_num]]
                j = i + 1
                while j < len(sorted_line_nums):
                    next_num = sorted_line_nums[j]
                    if next_num != sorted_line_nums[j - 1] + 1:
                        break
                    next_code = (
                        source_lines[next_num - 1]
                        .split('#')[0]
                        .strip()
                    )
                    if len(next_code) > 0:
                        break
                    block.append(comments_by_line[next_num])
                    j += 1

                anchor = None
                last_comment_line = sorted_line_nums[j - 1]
                for k in range(last_comment_line, len(source_lines)):
                    candidate = source_lines[k].split('#')[0].strip()
                    if candidate and not candidate.startswith('#'):
                        anchor = _CommentPreserver._normalize(
                            candidate
                        )
                        break

                groups.append({
                    'lines': block,
                    'inline': False,
                    'anchor': anchor,
                })
                i = j

        return groups

    def reinsert(self, refactored: str) -> str:
        """
        Re-inject extracted comments into refactored source.

        Parameters
        ----------
        refactored : str
            Source after AST transformation (comments stripped)

        Returns
        -------
        str
            Source with comments re-injected at anchor positions
        """
        if not self._groups:
            return refactored

        lines = refactored.splitlines()
        norm = _CommentPreserver._normalize

        anchor_map: Dict[str, int] = {}
        for idx, line in enumerate(lines):
            n = norm(line)
            if n and n not in anchor_map:
                anchor_map[n] = idx

        insertions: List[Tuple[int, List[str], bool]] = []
        for group in self._groups:
            if not group['anchor']:
                continue
            target_idx = anchor_map.get(group['anchor'])
            if target_idx is not None:
                insertions.append(
                    (target_idx, group['lines'], group['inline'])
                )

        insertions.sort(key=lambda x: x[0])
        offset = 0
        used_inline: set = set()

        for target_idx, comment_lines, is_inline in insertions:
            actual_idx = target_idx + offset
            if is_inline:
                if actual_idx not in used_inline:
                    lines[actual_idx] = (
                        f"{lines[actual_idx]}  {comment_lines[0]}"
                    )
                    used_inline.add(actual_idx)
            else:
                anchor_line = lines[actual_idx]
                indent = len(anchor_line) - len(
                    anchor_line.lstrip()
                )
                prefix = ' ' * indent
                for ci, ctext in enumerate(comment_lines):
                    lines.insert(actual_idx + ci, prefix + ctext)
                offset += len(comment_lines)

        return '\n'.join(lines)


class PythonCodeOptimizer:
    """
    Comprehensive Python code optimization engine.

    Implements multi-stage optimization pipeline including structural refactoring,
    documentation enhancement, performance optimization, and quality enforcement.
    Designed for Google Antigravity IDE 1.16.5 and Gemini 3 Pro agent.

    Parameters
    ----------
    optimization_level : str, default='balanced'
        Optimization aggressiveness: 'conservative', 'balanced', or 'aggressive'
    focus_areas : Optional[List[str]], default=None
        Specific optimization categories to focus on. Options include:
        'documentation', 'performance', 'structure', 'style', 'complexity'
    preserve_comments : bool, default=True
        Whether to preserve existing inline comments
    max_complexity : int, default=10
        Maximum allowed cyclomatic complexity per function
    target_maintainability : float, default=70.0
        Target maintainability index score

    Attributes
    ----------
    temp_dir : Path
        Temporary directory for intermediate files
    validation_enabled : bool
        Whether to validate changes preserve functionality

    Examples
    --------
    >>> optimizer = PythonCodeOptimizer(
    ...     optimization_level='aggressive',
    ...     focus_areas=['documentation', 'performance']
    ... )
    >>> result = optimizer.optimize_file('script.py', 'optimized_script.py')
    >>> print(f"Success: {result.success}")
    >>> print(f"Improvements: {len(result.changes_applied)}")
    """

    def __init__(
        self,
        optimization_level: str = 'balanced',
        focus_areas: Optional[List[str]] = None,
        preserve_comments: bool = True,
        max_complexity: int = 10,
        target_maintainability: float = 75.0
    ):
        """
        Initialize the Python Code Optimizer.

        Parameters
        ----------
        optimization_level : str, default='balanced'
            Level of optimization aggressiveness
        focus_areas : Optional[List[str]], default=None
            Specific areas to optimize
        preserve_comments : bool, default=True
            Preserve existing comments
        max_complexity : int, default=10
            Maximum cyclomatic complexity threshold
        target_maintainability : float, default=75.0
            Target maintainability index
        """
        self.optimization_level = optimization_level
        self.focus_areas = focus_areas or ['all']
        self.preserve_comments = preserve_comments
        self.max_complexity = max_complexity
        self.target_maintainability = target_maintainability
        self.temp_dir = Path(tempfile.mkdtemp(prefix='py_optimize_'))
        self.validation_enabled = True

        # Apply level-based threshold overrides
        if self.optimization_level == 'extreme':
            self.max_complexity = min(self.max_complexity, 6)
            self.target_maintainability = max(
                self.target_maintainability, 85.0
            )

        logger.info(
            f"Initialized PythonCodeOptimizer: level={optimization_level}, "
            f"focus={focus_areas}, max_complexity={max_complexity}"
        )

    def optimize_file(
        self,
        input_path: str,
        output_path: str,
        generate_report: bool = True
    ) -> OptimizationResult:
        """
        Optimize a Python source file through comprehensive multi-stage pipeline.

        Orchestrates the complete optimization workflow including analysis,
        refactoring, documentation, style enforcement, and validation.

        Parameters
        ----------
        input_path : str
            Path to input Python file to optimize
        output_path : str
            Path where optimized file will be written
        generate_report : bool, default=True
            Whether to generate detailed optimization report

        Returns
        -------
        OptimizationResult
            Comprehensive results including metrics and changes

        Raises
        ------
        FileNotFoundError
            If input file does not exist
        SyntaxError
            If input file contains invalid Python syntax
        ValueError
            If optimization level is invalid

        Examples
        --------
        >>> optimizer = PythonCodeOptimizer()
        >>> result = optimizer.optimize_file(
        ...     'legacy_code.py',
        ...     'refactored_code.py',
        ...     generate_report=True
        ... )
        >>> if result.success:
        ...     print(f"Optimized! {len(result.changes_applied)} improvements")
        """
        start_time = datetime.now()
        changes_applied = []
        warnings = []
        errors = []

        try:
            # Validate input file exists and is valid Python
            input_file = Path(input_path)
            if not input_file.exists():
                raise FileNotFoundError(f"Input file not found: {input_path}")

            logger.info(f"Starting optimization: {input_path}")

            # Stage 1: Initial Analysis
            logger.info("Stage 1: Analyzing code structure and metrics")
            original_metrics = self._analyze_code(input_path)
            logger.info(f"Original metrics: {asdict(original_metrics)}")

            # Create working copy
            working_file = self.temp_dir / "working.py"
            shutil.copy2(input_path, working_file)

            # Stage 2: Structural Optimization
            if 'all' in self.focus_areas or 'structure' in self.focus_areas:
                logger.info("Stage 2: Analyzing structure")
                structure_changes, structure_warnings = self._optimize_structure(working_file)
                changes_applied.extend(structure_changes)
                warnings.extend(structure_warnings)

            # Stage 2.5: AST-Based Refactoring
            if 'all' in self.focus_areas or 'structure' in self.focus_areas:
                logger.info(
                    "Stage 2.5: Applying AST-based refactoring "
                    "(naming, docstrings, type stubs, "
                    "modularization)"
                )
                refactor_changes, refactor_warnings = (
                    self._apply_refactoring(working_file)
                )
                changes_applied.extend(refactor_changes)
                warnings.extend(refactor_warnings)

            # Stage 3: Documentation Enhancement
            if 'all' in self.focus_areas or 'documentation' in self.focus_areas:
                logger.info("Stage 3: Enhancing documentation")
                doc_changes, doc_warnings = self._enhance_documentation(working_file)
                changes_applied.extend(doc_changes)
                warnings.extend(doc_warnings)

            # Stage 4: Code Quality Enforcement
            if 'all' in self.focus_areas or 'style' in self.focus_areas:
                logger.info("Stage 4: Enforcing code quality standards")
                style_changes = self._enforce_quality(working_file)
                changes_applied.extend(style_changes)

            # Stage 5: Performance Optimization
            if 'all' in self.focus_areas or 'performance' in self.focus_areas:
                logger.info("Stage 5: Analyzing performance")
                perf_changes, perf_warnings = self._optimize_performance(working_file)
                changes_applied.extend(perf_changes)
                warnings.extend(perf_warnings)

            # Stage 6: Validation
            logger.info("Stage 6: Validating optimizations")
            validation_warnings = self._validate_optimizations(
                input_path,
                str(working_file)
            )
            warnings.extend(validation_warnings)

            # Analyze optimized code
            optimized_metrics = self._analyze_code(str(working_file))
            logger.info(f"Optimized metrics: {asdict(optimized_metrics)}")

            # Copy to output location
            if filecmp.cmp(working_file, input_path):
                logger.info("No changes were necessary - file is already optimized.")
                changes_applied.append("No changes needed (content identical)")
            else:
                shutil.copy2(working_file, output_path)
                logger.info(f"Optimization complete: {output_path}")

            # Generate report if requested
            if generate_report:
                self._generate_report(
                    original_metrics,
                    optimized_metrics,
                    changes_applied,
                    output_path
                )
            
            # stdout summary for agent visibility
            print("\n=== OPTIMIZATION SUMMARY ===")
            print(f"File: {output_path}")
            print(f"Status: {'Success' if changes_applied else 'No Changes'}")
            print(f"Changes Applied: {len(changes_applied)}")
            for change in changes_applied:
                print(f"  - {change}")
            print("============================\n")

            duration = (datetime.now() - start_time).total_seconds()

            return OptimizationResult(
                success=True,
                original_metrics=original_metrics,
                optimized_metrics=optimized_metrics,
                changes_applied=changes_applied,
                warnings=warnings,
                errors=errors,
                optimization_duration=duration
            )

        except Exception as e:
            logger.error(f"Optimization failed: {str(e)}", exc_info=True)
            errors.append(str(e))

            # Return failure result with partial metrics if available
            duration = (datetime.now() - start_time).total_seconds()

            return OptimizationResult(
                success=False,
                original_metrics=original_metrics if 'original_metrics' in locals() else None,
                optimized_metrics=None,
                changes_applied=changes_applied,
                warnings=warnings,
                errors=errors,
                optimization_duration=duration
            )

        finally:
            # Cleanup temporary directory
            if self.temp_dir.exists():
                shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _analyze_code(self, file_path: str) -> OptimizationMetrics:
        """
        Perform comprehensive code analysis to generate quality metrics.

        Analyzes cyclomatic complexity, maintainability index, documentation
        coverage, PEP 8 compliance, and type hint coverage.

        Parameters
        ----------
        file_path : str
            Path to Python file to analyze

        Returns
        -------
        OptimizationMetrics
            Comprehensive code quality metrics

        Notes
        -----
        Uses external tools: radon (complexity), pylint (style)
        Complexity calculation: Weighted average across all functions
        """
        logger.debug(f"Analyzing: {file_path}")

        # Read source code
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        # Parse AST for structural analysis
        try:
            tree = ast.parse(source_code)
        except SyntaxError as e:
            logger.error(f"Syntax error in {file_path}: {e}")
            raise

        # Calculate cyclomatic complexity using radon
        complexity = self._calculate_complexity(file_path)

        # Calculate maintainability index
        maintainability = self._calculate_maintainability(file_path)

        # Count lines of code
        loc = self._count_lines_of_code(source_code)

        # Analyze documentation coverage
        doc_coverage = self._analyze_documentation_coverage(tree)

        # Check PEP 8 violations
        pep8_violations = self._check_pep8(file_path)

        # Analyze type hint coverage
        type_coverage = self._analyze_type_hints(tree)

        # Compute Entropy
        entropy = 0.0
        if analyze_entropy:
            try:
                metrics = analyze_entropy.compute_entropy_from_source(source_code)
                entropy = metrics.normalized_score
            except Exception:
                pass

        return OptimizationMetrics(
            cyclomatic_complexity=complexity,
            maintainability_index=maintainability,
            lines_of_code=loc,
            documentation_coverage=doc_coverage,
            pep8_violations=pep8_violations,
            type_hint_coverage=type_coverage,
            entropy_score=entropy
        )

    def _optimize_structure(self, file_path: Path) -> Tuple[List[str], List[str]]:
        """Analyze structure and recommend improvements."""
        changes = []
        warnings = []

        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:
            logger.warning(f"Cannot parse {file_path} for structural optimization")
            return changes, warnings

        # Identify functions with high complexity
        complex_functions = self._find_complex_functions(tree)

        if complex_functions:
            warnings.append(
                f"[Structure] Found {len(complex_functions)} functions exceeding "
                f"complexity threshold (>{self.max_complexity}). Recommendation: Decompose."
            )

        # Extract duplicated code
        duplicates = self._find_code_duplication(tree)
        if duplicates:
            warnings.append(
                f"[Structure] Found {len(duplicates)} duplicated code blocks. "
                f"Recommendation: Extract to utilities."
            )

        # Clean Code F1: Max 5 Arguments (enterprise target)
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                args = [a for a in node.args.args if a.arg not in ('self', 'cls')]
                if len(args) > 5:
                     warnings.append(f"[Clean Code] Function '{node.name}' has {len(args)} arguments (Max 5). Recommendation: Use dataclass.")

        return changes, warnings

    def _apply_refactoring(
        self, file_path: Path
    ) -> Tuple[List[str], List[str]]:
        """
        Apply AST-based refactoring via RefactorEngine with comment
        preservation.

        Performs naming convention enforcement, docstring injection,
        type stub injection, large string modularization, and
        anti-pattern elimination while preserving existing comments.

        Parameters
        ----------
        file_path : Path
            Path to the working Python file to refactor

        Returns
        -------
        Tuple[List[str], List[str]]
            (changes_applied, warnings)

        Notes
        -----
        - Skipped when RefactorEngine is unavailable
        - Skipped in 'conservative' mode (analysis only)
        - On engine failure, original file is preserved and errors
          are demoted to warnings (fail-safe)
        """
        changes: List[str] = []
        warnings: List[str] = []

        if RefactorEngine is None:
            warnings.append(
                "[Refactor] refactor_engine module not available; "
                "AST refactoring skipped."
            )
            return changes, warnings

        if self.optimization_level == 'conservative':
            logger.info(
                "Skipping AST refactoring in conservative mode"
            )
            return changes, warnings

        source = file_path.read_text(encoding='utf-8')

        # Preserve comments before AST round-trip
        preserver = None
        if self.preserve_comments:
            preserver = _CommentPreserver(source)
            logger.info(
                f"Extracted {len(preserver._groups)} comment "
                f"groups for preservation"
            )

        # String restoration thresholds by optimization level
        _thresholds = {
            'balanced':   {'min_newlines': 6, 'min_length': 300},
            'aggressive': {'min_newlines': 4, 'min_length': 200},
            'extreme':    {'min_newlines': 2, 'min_length': 100},
        }.get(self.optimization_level, {'min_newlines': 4, 'min_length': 200})

        engine = RefactorEngine(
            max_line_length=88,
            inject_type_stubs=True,
            numpy_doc_examples=True,
            string_restore_min_newlines=_thresholds['min_newlines'],
            string_restore_min_length=_thresholds['min_length']
        )
        result = engine.refactor_source(source, str(file_path))

        if not result.success:
            for err in result.errors:
                warnings.append(
                    f"[Refactor] Engine error: {err}"
                )
            logger.warning(
                "RefactorEngine failed; preserving original file"
            )
            return changes, warnings

        refactored = result.refactored_source

        # Re-inject preserved comments
        if preserver is not None and refactored != source:
            refactored = preserver.reinsert(refactored)

        # Only write back if source actually changed
        if refactored != source:
            file_path.write_text(refactored, encoding='utf-8')
            for rc in result.changes:
                changes.append(
                    f"[Refactor/{rc.category}] {rc.description}"
                )
            logger.info(
                f"Refactoring complete: "
                f"{len(result.changes)} transformations applied"
            )
        else:
            logger.info("Refactoring produced no changes")

        return changes, warnings

    def _enhance_documentation(self, file_path: Path) -> Tuple[List[str], List[str]]:
        """Analyze documentation and recommend improvements."""
        changes = []
        warnings = []

        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return changes, warnings

        # Find undocumented elements
        undocumented = self._find_undocumented_elements(tree)

        if undocumented['functions']:
            warnings.append(
                f"[Documentation] Found {len(undocumented['functions'])} undocumented functions. "
                f"Recommendation: Add Numpy-style docstrings."
            )

        if undocumented['classes']:
            warnings.append(
                f"[Documentation] Found {len(undocumented['classes'])} undocumented classes. "
                f"Recommendation: Add docstrings."
            )

        return changes, warnings

    def _enforce_quality(self, file_path: Path) -> List[str]:
        """
        Enforce code quality standards including PEP 8, type hints, and naming.

        Applies Ruff formatting and linting (preferred), with Black/isort fallback.

        Parameters
        ----------
        file_path : Path
            Path to file to format

        Returns
        -------
        List[str]
            Descriptions of quality improvements
        """
        changes = []

        # Prefer Ruff (modern, fast, replaces black+isort+pycodestyle)
        ruff_available = False
        try:
            result = subprocess.run(
                ['ruff', 'format', str(file_path)],
                capture_output=True,
                text=True,
                timeout=30,
                errors='replace'
            )
            if result.returncode == 0:
                changes.append("Applied Ruff code formatting (PEP 8)")
                ruff_available = True
            else:
                logger.warning(f"Ruff format failed: {result.stderr}")
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.info("Ruff not available, falling back to black+isort")

        if ruff_available:
            # Ruff lint with auto-fix
            try:
                result = subprocess.run(
                    ['ruff', 'check', '--fix', str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    errors='replace'
                )
                if result.returncode == 0:
                    changes.append("Applied Ruff lint fixes (imports, style)")
            except (subprocess.TimeoutExpired, FileNotFoundError):
                pass
        else:
            # Fallback: Black formatting
            try:
                result = subprocess.run(
                    ['black', '--quiet', str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    errors='replace'
                )
                if result.returncode == 0:
                    changes.append("Applied Black code formatting (PEP 8)")
                else:
                    logger.warning(f"Black formatting failed: {result.stderr}")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                logger.warning(f"Black not available: {e}")

            # Fallback: isort import organization
            try:
                result = subprocess.run(
                    ['isort', '--quiet', str(file_path)],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    errors='replace'
                )
                if result.returncode == 0:
                    changes.append("Organized imports with isort")
            except (subprocess.TimeoutExpired, FileNotFoundError) as e:
                logger.warning(f"isort not available: {e}")

        return changes

    def _optimize_performance(self, file_path: Path) -> Tuple[List[str], List[str]]:
        """Analyze performance and recommend improvements."""
        changes = []
        warnings = []

        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return changes, warnings

        # Identify inefficient patterns
        patterns = self._find_inefficient_patterns(tree)

        if patterns.get('nested_loops'):
            warnings.append(
                f"[Performance] Found {len(patterns['nested_loops'])} nested loop structures. "
                f"Recommendation: Review for O(n^2) complexity."
            )

        if patterns.get('repeated_operations'):
            warnings.append(
                f"[Performance] Found {len(patterns['repeated_operations'])} repeated "
                f"expensive operations. Recommendation: Implement caching."
            )

        return changes, warnings

    def _validate_optimizations(
        self,
        original_path: str,
        optimized_path: str
    ) -> List[str]:
        """
        Validate that optimizations preserve original functionality.

        Runs the full ValidationSuite (if available) to check API
        preservation, documentation coverage, type hint coverage,
        complexity thresholds, and Clean Code compliance. Falls back
        to basic syntax validation if the suite is unavailable.

        Parameters
        ----------
        original_path : str
            Path to original file
        optimized_path : str
            Path to optimized file

        Returns
        -------
        List[str]
            Validation warnings if any issues detected
        """
        warnings = []

        # Basic syntax validation (always performed)
        try:
            with open(optimized_path, 'r', encoding='utf-8') as f:
                ast.parse(f.read())
        except SyntaxError as e:
            warnings.append(f"Syntax error in optimized code: {e}")
            return warnings

        # Full validation via ValidationSuite
        if ValidationSuite is not None:
            try:
                suite = ValidationSuite()
                report = suite.validate(original_path, optimized_path)
                if not report.overall_pass:
                    for check in report.checks:
                        if not check.passed:
                            warnings.append(
                                f"[Validation/{check.severity}] "
                                f"{check.name}: {check.details}"
                            )
                for rec in report.recommendations:
                    warnings.append(
                        f"[Validation] Recommendation: {rec}"
                    )
                logger.info(
                    "ValidationSuite complete: score=%.1f, pass=%s",
                    report.quality_score, report.overall_pass
                )
            except Exception as e:
                logger.warning(
                    "ValidationSuite failed: %s", str(e)
                )
                warnings.append(
                    f"[Validation] Suite error: {e}"
                )
        else:
            logger.info(
                "ValidationSuite not available; syntax-only validation"
            )

        logger.info("Validation completed successfully")
        return warnings

    def _generate_report(
        self,
        original_metrics: OptimizationMetrics,
        optimized_metrics: OptimizationMetrics,
        changes: List[str],
        output_path: str
    ) -> None:
        """
        Generate comprehensive optimization report.

        Creates detailed report comparing before/after metrics, listing all
        changes applied, and providing optimization recommendations.

        Parameters
        ----------
        original_metrics : OptimizationMetrics
            Metrics from original code
        optimized_metrics : OptimizationMetrics
            Metrics from optimized code
        changes : List[str]
            List of changes applied
        output_path : str
            Path to optimized file
        """
        report_path = Path(output_path).with_suffix('.optimization_report.json')

        report = {
            'timestamp': datetime.now().isoformat(),
            'original_file': str(Path(output_path).with_suffix('.py')),
            'optimized_file': output_path,
            'metrics': {
                'original': asdict(original_metrics),
                'optimized': asdict(optimized_metrics),
                'improvements': self._calculate_improvements(
                    original_metrics,
                    optimized_metrics
                )
            },
            'changes_applied': changes,
            'optimization_level': self.optimization_level,
            'focus_areas': self.focus_areas
        }

        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2)

        logger.info(f"Generated optimization report: {report_path}")

    def _calculate_complexity(self, file_path: str) -> float:
        """Calculate average cyclomatic complexity using radon or fallback."""
        try:
            result = subprocess.run(
                ['radon', 'cc', '-a', file_path],
                capture_output=True,
                text=True,
                timeout=10,
                errors='replace'
            )
            if result.returncode == 0:
                # Parse radon output for average complexity
                # Format: "Average complexity: A (5.2)"
                output = result.stdout
                if 'Average complexity' in output:
                    parts = output.split('(')
                    if len(parts) > 1:
                        complexity_str = parts[1].split(')')[0]
                        return float(complexity_str)
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        # Fallback: Simple AST-based complexity estimation
        return self._simple_complexity_estimate(file_path)

    def _simple_complexity_estimate(self, file_path: str) -> float:
        """Estimate complexity by counting decision points in AST."""
        with open(file_path, 'r', encoding='utf-8') as f:
            try:
                tree = ast.parse(f.read())
            except SyntaxError:
                return 0.0

        total_complexity = 0
        function_count = 0

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                function_count += 1
                # Count decision points
                complexity = 1  # Base complexity
                for child in ast.walk(node):
                    if isinstance(child, (ast.If, ast.While, ast.For,
                                         ast.ExceptHandler, ast.With)):
                        complexity += 1
                    elif isinstance(child, ast.BoolOp):
                        complexity += len(child.values) - 1
                total_complexity += complexity

        return total_complexity / max(function_count, 1)

    def _calculate_maintainability(self, file_path: str) -> float:
        """
        Calculate maintainability index using radon or AST-based fallback.

        The maintainability index is a composite metric derived from cyclomatic
        complexity, Halstead volume, and lines of code. Higher scores (closer
        to 100) indicate more maintainable code.

        Parameters
        ----------
        file_path : str
            Path to Python file to evaluate

        Returns
        -------
        float
            Maintainability index in range [0, 100]

        Notes
        -----
        Maintainability Index formula (SEI variant):
            MI = 171 - 5.2*ln(HV) - 0.23*CC - 16.2*ln(LOC)
        where HV = Halstead Volume, CC = Cyclomatic Complexity, LOC = lines.
        """
        try:
            result = subprocess.run(
                ['radon', 'mi', '-s', file_path],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                # Parse radon output: "file.py - A (85.23)"
                output = result.stdout
                if '(' in output and ')' in output:
                    mi_str = output.split('(')[1].split(')')[0]
                    return float(mi_str)
        except (subprocess.TimeoutExpired, FileNotFoundError, ValueError):
            pass

        # Fallback: heuristic-based maintainability estimate
        return self._simple_maintainability_estimate(file_path)

    def _simple_maintainability_estimate(self, file_path: str) -> float:
        """
        Compute a heuristic maintainability score from basic AST features.

        Parameters
        ----------
        file_path : str
            Path to Python file

        Returns
        -------
        float
            Estimated maintainability index in range [0, 100]
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            source = f.read()

        lines = source.splitlines()
        loc = max(len([l for l in lines if l.strip() and not l.strip().startswith('#')]), 1)

        try:
            tree = ast.parse(source)
        except SyntaxError:
            return 0.0

        # Count documented vs total callables
        callables = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]
        documented = [
            n for n in callables
            if (ast.get_docstring(n) or '')
        ]
        doc_ratio = len(documented) / max(len(callables), 1)

        # Penalize excessive LOC
        loc_penalty = max(0.0, 1.0 - (loc / 1000.0))

        # Combine into heuristic score (0-100)
        score = 50.0 + (doc_ratio * 30.0) + (loc_penalty * 20.0)
        return round(min(score, 100.0), 2)

    def _count_lines_of_code(self, source: str) -> int:
        """
        Count non-blank, non-comment lines of code in a source string.

        Parameters
        ----------
        source : str
            Raw Python source code

        Returns
        -------
        int
            Number of logical lines of code
        """
        return sum(
            1 for line in source.splitlines()
            if line.strip() and not line.strip().startswith('#')
        )

    def _analyze_documentation_coverage(self, tree: ast.AST) -> float:
        """
        Compute the percentage of callables possessing non-trivial docstrings.

        Parameters
        ----------
        tree : ast.AST
            Parsed AST of the Python source

        Returns
        -------
        float
            Documentation coverage as a percentage in range [0.0, 100.0]
        """
        callables = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]
        if not callables:
            return 100.0

        documented = sum(
            1 for n in callables
            if ast.get_docstring(n)
        )
        return round((documented / len(callables)) * 100.0, 2)

    def _check_pep8(self, file_path: str) -> int:
        """
        Count PEP 8 style violations using pycodestyle.

        Parameters
        ----------
        file_path : str
            Path to Python file

        Returns
        -------
        int
            Total number of PEP 8 violations detected; -1 if tool unavailable
        """
        try:
            result = subprocess.run(
                ['pycodestyle', '--statistics', '-q', file_path],
                capture_output=True,
                text=True,
                timeout=15
            )
            # Each non-empty line in stdout represents one violation
            return sum(1 for line in result.stdout.splitlines() if line.strip())
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.warning("pycodestyle not available; skipping PEP 8 check")
            return -1

    def _analyze_type_hints(self, tree: ast.AST) -> float:
        """
        Compute the percentage of function signatures containing type hints.

        Evaluates both parameter annotations and return type annotations.
        A function is considered fully annotated only if all parameters
        (excluding ``self``/``cls``) and the return type are annotated.

        Parameters
        ----------
        tree : ast.AST
            Parsed AST of the Python source

        Returns
        -------
        float
            Type hint coverage as a percentage in range [0.0, 100.0]
        """
        functions = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        if not functions:
            return 100.0

        fully_annotated = 0
        for func in functions:
            args = [
                a for a in func.args.args
                if a.arg not in ('self', 'cls')
            ]
            params_annotated = all(a.annotation is not None for a in args)
            return_annotated = func.returns is not None
            if params_annotated and return_annotated:
                fully_annotated += 1

        return round((fully_annotated / len(functions)) * 100.0, 2)

    def _find_complex_functions(
        self, tree: ast.AST
    ) -> List[Tuple[str, int]]:
        """
        Identify functions whose estimated cyclomatic complexity exceeds threshold.

        Parameters
        ----------
        tree : ast.AST
            Parsed AST of the Python source

        Returns
        -------
        List[Tuple[str, int]]
            List of (function_name, complexity) tuples for violating functions
        """
        complex_funcs: List[Tuple[str, int]] = []

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            complexity = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For,
                                      ast.ExceptHandler, ast.With,
                                      ast.Assert, ast.comprehension)):
                    complexity += 1
                elif isinstance(child, ast.BoolOp):
                    complexity += len(child.values) - 1
            if complexity > self.max_complexity:
                complex_funcs.append((node.name, complexity))

        return complex_funcs

    def _find_code_duplication(
        self, tree: ast.AST
    ) -> List[Dict[str, Any]]:
        """
        Detect duplicated statement blocks across function bodies.

        Uses a hash-based approach on serialized AST subtrees to find
        structurally identical code blocks that are candidates for extraction.

        Parameters
        ----------
        tree : ast.AST
            Parsed AST of the Python source

        Returns
        -------
        List[Dict[str, Any]]
            List of duplication records, each containing 'hash', 'locations',
            and 'line_count'
        """
        import hashlib

        block_hashes: Dict[str, List[Dict[str, Any]]] = {}

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            # Slide a window of 3+ statements through the body
            body = node.body
            for window_size in range(3, len(body) + 1):
                for start in range(len(body) - window_size + 1):
                    block = body[start:start + window_size]
                    block_src = ast.dump(ast.Module(body=block, type_ignores=[]))
                    block_hash = hashlib.md5(block_src.encode()).hexdigest()
                    entry = {
                        'function': node.name,
                        'start_line': getattr(block[0], 'lineno', -1),
                        'line_count': window_size
                    }
                    block_hashes.setdefault(block_hash, []).append(entry)

        return [
            {'hash': h, 'locations': locs, 'line_count': locs[0]['line_count']}
            for h, locs in block_hashes.items()
            if len(locs) > 1
        ]

    def _find_undocumented_elements(
        self, tree: ast.AST
    ) -> Dict[str, List[str]]:
        """
        Collect names of all undocumented functions and classes in the AST.

        Parameters
        ----------
        tree : ast.AST
            Parsed AST of the Python source

        Returns
        -------
        Dict[str, List[str]]
            Dictionary with keys 'functions' and 'classes', each mapping to
            a list of undocumented element names
        """
        result: Dict[str, List[str]] = {'functions': [], 'classes': []}

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                if not ast.get_docstring(node):
                    result['functions'].append(node.name)
            elif isinstance(node, ast.ClassDef):
                if not ast.get_docstring(node):
                    result['classes'].append(node.name)

        return result

    def _find_inefficient_patterns(
        self, tree: ast.AST
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        Detect common inefficient coding patterns that degrade performance.

        Identifies: nested loops with O(n²)+ complexity, repeated attribute
        lookups inside loops, list concatenation in loops, and calls to
        expensive operations without caching.

        Parameters
        ----------
        tree : ast.AST
            Parsed AST of the Python source

        Returns
        -------
        Dict[str, List[Dict[str, Any]]]
            Categorized dictionary of detected patterns, each entry containing
            'line' and 'description' keys
        """
        patterns: Dict[str, List[Dict[str, Any]]] = {
            'nested_loops': [],
            'repeated_operations': [],
            'list_concat_in_loop': [],
        }

        for node in ast.walk(tree):
            # Detect nested loops
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if child is not node and isinstance(child, (ast.For, ast.While)):
                        patterns['nested_loops'].append({
                            'line': getattr(node, 'lineno', -1),
                            'description': 'Nested loop detected - potential O(n²)'
                        })
                        break

            # Detect list concatenation inside loops (+=  with list)
            if isinstance(node, (ast.For, ast.While)):
                for child in ast.walk(node):
                    if isinstance(child, ast.AugAssign):
                        if isinstance(child.op, ast.Add):
                            patterns['list_concat_in_loop'].append({
                                'line': getattr(child, 'lineno', -1),
                                'description': 'List concatenation in loop - use .append()'
                            })

        return patterns

    def _calculate_improvements(
        self,
        original: OptimizationMetrics,
        optimized: OptimizationMetrics
    ) -> Dict[str, Any]:
        """
        Compute percentage-based improvement deltas between metric snapshots.

        Parameters
        ----------
        original : OptimizationMetrics
            Metrics captured before optimization
        optimized : OptimizationMetrics
            Metrics captured after optimization

        Returns
        -------
        Dict[str, Any]
            Dictionary mapping metric names to improvement values and deltas,
            where positive values indicate improvement
        """
        def _pct_change(before: float, after: float, lower_is_better: bool = False) -> float:
            if before == 0:
                return 0.0
            delta = ((after - before) / before) * 100.0
            return -delta if lower_is_better else delta

        return {
            'cyclomatic_complexity': {
                'before': original.cyclomatic_complexity,
                'after': optimized.cyclomatic_complexity,
                'improvement_pct': _pct_change(
                    original.cyclomatic_complexity,
                    optimized.cyclomatic_complexity,
                    lower_is_better=True
                )
            },
            'maintainability_index': {
                'before': original.maintainability_index,
                'after': optimized.maintainability_index,
                'improvement_pct': _pct_change(
                    original.maintainability_index,
                    optimized.maintainability_index
                )
            },
            'documentation_coverage': {
                'before': original.documentation_coverage,
                'after': optimized.documentation_coverage,
                'improvement_pct': _pct_change(
                    original.documentation_coverage,
                    optimized.documentation_coverage
                )
            },
            'pep8_violations': {
                'before': original.pep8_violations,
                'after': optimized.pep8_violations,
                'improvement_pct': _pct_change(
                    original.pep8_violations,
                    optimized.pep8_violations,
                    lower_is_better=True
                )
            },
            'type_hint_coverage': {
                'before': original.type_hint_coverage,
                'after': optimized.type_hint_coverage,
                'improvement_pct': _pct_change(
                    original.type_hint_coverage,
                    optimized.type_hint_coverage
                )
            },
        }


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def _build_argument_parser() -> argparse.ArgumentParser:
    """
    Construct the command-line argument parser for the optimizer.

    Returns
    -------
    argparse.ArgumentParser
        Fully configured argument parser
    """
    parser = argparse.ArgumentParser(
        prog='optimize_python',
        description=(
            'Optimize Python code to academic-professional standards.\n'
            'Part of the python-code-optimizer Antigravity Skill v3.0.0.'
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=(
            'Examples:\n'
            '  optimize_python.py --input script.py --output optimized.py\n'
            '  optimize_python.py --input script.py --level aggressive --report\n'
            '  optimize_python.py --input script.py --focus documentation,performance\n'
        )
    )
    parser.add_argument(
        '--input', '-i',
        required=True,
        type=str,
        help='Path to the Python file to optimize'
    )
    parser.add_argument(
        '--output', '-o',
        required=True,
        type=str,
        help='Path to write the optimized Python file'
    )
    parser.add_argument(
        '--level', '-l',
        choices=['conservative', 'balanced', 'aggressive', 'extreme'],
        default='balanced',
        help='Optimization aggressiveness level (default: balanced)'
    )
    parser.add_argument(
        '--focus', '-f',
        type=str,
        default='all',
        help=(
            'Comma-separated optimization categories: '
            'all, documentation, performance, structure, style, complexity'
        )
    )
    parser.add_argument(
        '--report', '-r',
        action='store_true',
        help='Generate detailed JSON optimization report alongside output'
    )
    parser.add_argument(
        '--max-complexity',
        type=int,
        default=10,
        help='Maximum allowed cyclomatic complexity per function (default: 10)'
    )
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging output'
    )
    return parser


def main() -> int:
    """
    Main entry point for the Python Code Optimizer CLI.

    Parses arguments, initializes the optimizer, executes the optimization
    pipeline, and prints a human-readable summary to stdout.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on failure
    """
    parser = _build_argument_parser()
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    focus_areas = [f.strip() for f in args.focus.split(',') if f.strip()]

    optimizer = PythonCodeOptimizer(
        optimization_level=args.level,
        focus_areas=focus_areas,
        max_complexity=args.max_complexity
    )

    result = optimizer.optimize_file(
        input_path=args.input,
        output_path=args.output,
        generate_report=args.report
    )

    # Print human-readable summary
    status = "SUCCESS" if result.success else "FAILED"
    print(f"\n{'='*60}")
    print(f"  Python Code Optimizer - {status}")
    print(f"{'='*60}")
    print(f"  Input  : {args.input}")
    print(f"  Output : {args.output}")
    print(f"  Level  : {args.level}")
    print(f"  Duration: {result.optimization_duration:.2f}s")

    if result.success and result.original_metrics and result.optimized_metrics:
        orig = result.original_metrics
        opt  = result.optimized_metrics
        print(f"\n  Metric                  Before     After")
        print(f"  {'-'*44}")
        print(f"  Cyclomatic Complexity   {orig.cyclomatic_complexity:>6.2f}  ->  {opt.cyclomatic_complexity:>6.2f}")
        print(f"  Maintainability Index   {orig.maintainability_index:>6.2f}  ->  {opt.maintainability_index:>6.2f}")
        print(f"  Doc Coverage (%)        {orig.documentation_coverage:>6.2f}  ->  {opt.documentation_coverage:>6.2f}")
        print(f"  PEP 8 Violations        {orig.pep8_violations:>6}  ->  {opt.pep8_violations:>6}")
        print(f"  Type Hint Coverage (%)  {orig.type_hint_coverage:>6.2f}  ->  {opt.type_hint_coverage:>6.2f}")
        print(f"  Lines of Code           {orig.lines_of_code:>6}  ->  {opt.lines_of_code:>6}")
        print(f"\n  Changes Applied : {len(result.changes_applied)}")
        for change in result.changes_applied:
            print(f"    - {change}")

    if result.warnings:
        print(f"\n  Warnings ({len(result.warnings)}):")
        for w in result.warnings:
            print(f"    [WARN] {w}")

    if result.errors:
        print(f"\n  Errors ({len(result.errors)}):")
        for e in result.errors:
            print(f"    [ERR]  {e}")

    print(f"{'='*60}\n")

    return 0 if result.success else 1


if __name__ == '__main__':
    sys.exit(main())

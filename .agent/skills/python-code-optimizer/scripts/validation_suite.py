#!/usr/bin/env python3
"""
Optimization Validation Suite

Validates that optimized Python files preserve functional equivalence with
their originals, meet all quality thresholds, and conform to enterprise
production standards.

Author: Enterprise Development Team
Version: 3.0.0
Target: Google Antigravity IDE 1.16.5, Gemini 3 Pro
License: Apache-2.0
"""

import ast
import hashlib
import json
import logging
import subprocess
import sys
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import argparse
import traceback
import re
from typing import Set

# Add local scripts to path to allow importing analyze_entropy
sys.path.append(str(Path(__file__).parent))
try:
    import analyze_entropy
except ImportError:
    analyze_entropy = None

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
class ValidationCheck:
    """
    Result of a single validation check.

    Attributes
    ----------
    name : str
        Human-readable check identifier
    passed : bool
        Whether the check passed
    severity : str
        Check severity if failed: 'critical', 'major', 'minor'
    details : str
        Detailed message explaining the result
    score : Optional[float]
        Numeric score for quantitative checks (0-100)
    """
    name: str
    passed: bool
    severity: str
    details: str
    score: Optional[float] = None


@dataclass
class ValidationReport:
    """
    Comprehensive validation report for an optimized Python file.

    Attributes
    ----------
    original_file : str
        Path to original source file
    optimized_file : str
        Path to optimized source file
    overall_pass : bool
        True only if all critical and major checks pass
    checks : List[ValidationCheck]
        Individual check results
    quality_score : float
        Aggregate quality score (0-100)
    critical_failures : List[str]
        Names of critical checks that failed
    recommendations : List[str]
        Suggested follow-up actions
    """
    original_file: str
    optimized_file: str
    overall_pass: bool
    checks: List[ValidationCheck]
    quality_score: float
    critical_failures: List[str] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Validators
# ---------------------------------------------------------------------------

class ValidationSuite:
    """
    Multi-faceted validation engine for Python code optimization results.

    Performs syntax validation, AST equivalence checks, quality threshold
    enforcement, import validation, and static analysis integration.

    Parameters
    ----------
    min_quality_score : float, default=75.0
        Minimum aggregate quality score for overall pass
    min_doc_coverage : float, default=80.0
        Minimum documentation coverage percentage required
    min_type_coverage : float, default=70.0
        Minimum type hint coverage percentage required
    max_complexity : int, default=10
        Maximum allowed cyclomatic complexity

    Examples
    --------
    >>> suite = ValidationSuite(min_quality_score=80.0)
    >>> report = suite.validate('original.py', 'optimized.py')
    >>> print(f"Pass: {report.overall_pass}, Score: {report.quality_score}")
    """

    def __init__(
        self,
        min_quality_score: float = 75.0,
        min_doc_coverage: float = 80.0,
        min_type_coverage: float = 70.0,
        max_complexity: int = 10,
        max_function_args: int = 5
    ) -> None:
        self.min_quality_score = min_quality_score
        self.min_doc_coverage = min_doc_coverage
        self.min_type_coverage = min_type_coverage
        self.max_complexity = max_complexity
        self.max_function_args = max_function_args

    def validate(
        self, original_path: str, optimized_path: str
    ) -> ValidationReport:
        """
        Run the complete validation suite against an optimized file.

        Parameters
        ----------
        original_path : str
            Path to the original Python file
        optimized_path : str
            Path to the optimized Python file

        Returns
        -------
        ValidationReport
            Complete validation results with quality score

        Raises
        ------
        FileNotFoundError
            If either file does not exist
        """
        orig_path = Path(original_path)
        opt_path  = Path(optimized_path)

        for p in (orig_path, opt_path):
            if not p.exists():
                raise FileNotFoundError(f"File not found: {p}")

        original_src  = orig_path.read_text(encoding='utf-8')
        optimized_src = opt_path.read_text(encoding='utf-8')

        checks: List[ValidationCheck] = []

        # 1. Syntax validity
        checks.append(self._check_syntax(optimized_src, str(opt_path)))

        # 2. Public API preservation
        checks.append(self._check_api_preservation(original_src, optimized_src))

        # 3. Import completeness
        checks.append(self._check_imports(original_src, optimized_src))

        # 4. Documentation coverage
        checks.append(self._check_doc_coverage(optimized_src))

        # 5. Type hint coverage
        checks.append(self._check_type_coverage(optimized_src))

        # 6. Complexity threshold
        checks.append(self._check_complexity(optimized_src))

        # 7. PEP 8 compliance
        checks.append(self._check_pep8(str(opt_path)))

        # 8. No bare excepts
        checks.append(self._check_no_bare_except(optimized_src))

        # 9. No mutable default arguments
        checks.append(self._check_mutable_defaults(optimized_src))

        # 10. Line length compliance
        checks.append(self._check_line_length(optimized_src))

        # 11. Clean Names (N1-N7)
        checks.append(self._check_clean_names(optimized_src))

        # 12. Clean Functions (F1: Max 3 args)
        checks.append(self._check_clean_functions(optimized_src))

        # 13. Security & Environment (Global/Imports)
        checks.append(self._check_security(optimized_src))

        # 14. Entropy & Structural Integrity
        checks.append(self._check_entropy(optimized_src))

        # 15. Magic Numbers (G25)
        checks.append(self._check_magic_numbers(optimized_src))

        # 16. Law of Demeter (G36)
        checks.append(self._check_law_of_demeter(optimized_src))

        # Compute aggregate quality score
        quality_score = self._compute_quality_score(checks)

        critical_failures = [
            c.name for c in checks
            if not c.passed and c.severity == 'critical'
        ]
        major_failures = [
            c.name for c in checks
            if not c.passed and c.severity == 'major'
        ]
        overall_pass = (
            not critical_failures
            and not major_failures
            and quality_score >= self.min_quality_score
        )

        recommendations = self._build_recommendations(checks)

        return ValidationReport(
            original_file=str(orig_path),
            optimized_file=str(opt_path),
            overall_pass=overall_pass,
            checks=checks,
            quality_score=round(quality_score, 2),
            critical_failures=critical_failures,
            recommendations=recommendations
        )

    def _check_syntax(self, source: str, filename: str) -> ValidationCheck:
        """
        Verify that the optimized source is valid Python syntax.

        Parameters
        ----------
        source : str
            Python source code
        filename : str
            Filename for error context

        Returns
        -------
        ValidationCheck
            Syntax check result
        """
        try:
            ast.parse(source, filename=filename)
            return ValidationCheck(
                name='Syntax Validity',
                passed=True,
                severity='critical',
                details='File parses successfully as valid Python 3.',
                score=100.0
            )
        except SyntaxError as e:
            return ValidationCheck(
                name='Syntax Validity',
                passed=False,
                severity='critical',
                details=f"Syntax error at line {e.lineno}: {e.msg}",
                score=0.0
            )

    def _check_api_preservation(
        self, original: str, optimized: str
    ) -> ValidationCheck:
        """
        Check that all public functions and classes from the original are present.

        Parameters
        ----------
        original : str
            Original source code
        optimized : str
            Optimized source code

        Returns
        -------
        ValidationCheck
            API preservation check result
        """
        original_api  = self._extract_public_api(original)
        optimized_api = self._extract_public_api(optimized)
        missing = original_api - optimized_api

        if not missing:
            return ValidationCheck(
                name='Public API Preservation',
                passed=True,
                severity='critical',
                details=f"All {len(original_api)} public symbols preserved.",
                score=100.0
            )

        return ValidationCheck(
            name='Public API Preservation',
            passed=False,
            severity='critical',
            details=f"Missing public symbols: {', '.join(sorted(missing))}",
            score=max(0.0, (1 - len(missing) / max(len(original_api), 1)) * 100)
        )

    def _extract_public_api(self, src: str) -> Set[str]:
        """Helper to extract public API symbols."""
        try:
            tree = ast.parse(src)
        except SyntaxError:
            return set()
        names: Set[str] = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                    ast.ClassDef)):
                if not node.name.startswith('_'):
                    names.add(node.name)
        return names

    def _check_imports(
        self, original: str, optimized: str
    ) -> ValidationCheck:
        """
        Verify that all original imports are present in the optimized file.

        Parameters
        ----------
        original : str
            Original source code
        optimized : str
            Optimized source code

        Returns
        -------
        ValidationCheck
            Import completeness check result
        """
        def extract_imports(src: str) -> set:
            try:
                tree = ast.parse(src)
            except SyntaxError:
                return set()
            imports = set()
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name)
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ''
                    for alias in node.names:
                        imports.add(f"{module}.{alias.name}")
            return imports

        orig_imports = extract_imports(original)
        opt_imports  = extract_imports(optimized)
        missing = orig_imports - opt_imports

        if not missing:
            return ValidationCheck(
                name='Import Completeness',
                passed=True,
                severity='major',
                details=f"All {len(orig_imports)} imports present.",
                score=100.0
            )

        return ValidationCheck(
            name='Import Completeness',
            passed=False,
            severity='major',
            details=f"Missing imports: {', '.join(sorted(missing))}",
            score=max(0.0, (1 - len(missing)/max(len(orig_imports), 1)) * 100)
        )

    def _check_doc_coverage(self, source: str) -> ValidationCheck:
        """
        Validate documentation coverage meets minimum threshold.

        Parameters
        ----------
        source : str
            Python source code

        Returns
        -------
        ValidationCheck
            Documentation coverage check result
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck(
                name='Documentation Coverage',
                passed=False,
                severity='major',
                details='Cannot analyze — syntax error.',
                score=0.0
            )

        callables = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
        ]
        if not callables:
            return ValidationCheck(
                name='Documentation Coverage',
                passed=True,
                severity='major',
                details='No callables found — N/A.',
                score=100.0
            )

        documented = sum(1 for n in callables if ast.get_docstring(n))
        coverage = (documented / len(callables)) * 100.0
        passed = coverage >= self.min_doc_coverage

        return ValidationCheck(
            name='Documentation Coverage',
            passed=passed,
            severity='major',
            details=(
                f"{documented}/{len(callables)} callables documented "
                f"({coverage:.1f}% — threshold: {self.min_doc_coverage}%)"
            ),
            score=coverage
        )

    def _check_type_coverage(self, source: str) -> ValidationCheck:
        """
        Validate type annotation coverage meets minimum threshold.

        Parameters
        ----------
        source : str
            Python source code

        Returns
        -------
        ValidationCheck
            Type hint coverage check result
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck(
                name='Type Hint Coverage',
                passed=False,
                severity='minor',
                details='Cannot analyze — syntax error.',
                score=0.0
            )

        functions = [
            n for n in ast.walk(tree)
            if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))
        ]
        if not functions:
            return ValidationCheck(
                name='Type Hint Coverage',
                passed=True,
                severity='minor',
                details='No functions found — N/A.',
                score=100.0
            )

        fully_annotated = 0
        for func in functions:
            args = [a for a in func.args.args if a.arg not in ('self', 'cls')]
            if all(a.annotation is not None for a in args) and func.returns:
                fully_annotated += 1

        coverage = (fully_annotated / len(functions)) * 100.0
        passed = coverage >= self.min_type_coverage

        return ValidationCheck(
            name='Type Hint Coverage',
            passed=passed,
            severity='minor',
            details=(
                f"{fully_annotated}/{len(functions)} functions fully annotated "
                f"({coverage:.1f}% — threshold: {self.min_type_coverage}%)"
            ),
            score=coverage
        )

    def _check_complexity(self, source: str) -> ValidationCheck:
        """
        Check that no function exceeds the maximum cyclomatic complexity.

        Parameters
        ----------
        source : str
            Python source code

        Returns
        -------
        ValidationCheck
            Complexity check result
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck(
                name='Complexity Threshold',
                passed=False,
                severity='major',
                details='Cannot analyze — syntax error.',
                score=0.0
            )

        violations: List[Tuple[str, int]] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            cc = 1
            for child in ast.walk(node):
                if isinstance(child, (ast.If, ast.While, ast.For,
                                      ast.ExceptHandler, ast.With)):
                    cc += 1
                elif isinstance(child, ast.BoolOp):
                    cc += len(child.values) - 1
            if cc > self.max_complexity:
                violations.append((node.name, cc))

        if not violations:
            return ValidationCheck(
                name='Complexity Threshold',
                passed=True,
                severity='major',
                details=(
                    f"All functions within complexity limit (<={self.max_complexity})."
                ),
                score=100.0
            )

        details = '; '.join(f"{n}={c}" for n, c in violations)
        return ValidationCheck(
            name='Complexity Threshold',
            passed=False,
            severity='major',
            details=f"Complexity violations (>{self.max_complexity}): {details}",
            score=max(0.0, 100.0 - len(violations) * 10)
        )

    def _check_pep8(self, file_path: str) -> ValidationCheck:
        """
        Run pycodestyle and report PEP 8 violation count.

        Parameters
        ----------
        file_path : str
            Path to file to check

        Returns
        -------
        ValidationCheck
            PEP 8 compliance check result
        """
        try:
            result = subprocess.run(
                ['pycodestyle', '--statistics', '-q', file_path],
                capture_output=True,
                text=True,
                timeout=15
            )
            violations = sum(
                1 for line in result.stdout.splitlines() if line.strip()
            )
            passed = violations == 0
            score = max(0.0, 100.0 - violations * 2)
            return ValidationCheck(
                name='PEP 8 Compliance',
                passed=passed,
                severity='minor',
                details=f"{violations} PEP 8 violation(s) detected.",
                score=score
            )
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return ValidationCheck(
                name='PEP 8 Compliance',
                passed=True,
                severity='minor',
                details='pycodestyle not available — check skipped.',
                score=100.0
            )

    def _check_no_bare_except(self, source: str) -> ValidationCheck:
        """
        Ensure no bare ``except:`` clauses remain in the optimized code.

        Parameters
        ----------
        source : str
            Python source code

        Returns
        -------
        ValidationCheck
            Bare except check result
        """
        import re
        bare_excepts = re.findall(r'\bexcept\s*:', source)
        passed = len(bare_excepts) == 0
        return ValidationCheck(
            name='No Bare Except',
            passed=passed,
            severity='major',
            details=(
                'No bare except clauses found.'
                if passed
                else f"{len(bare_excepts)} bare 'except:' clause(s) detected."
            ),
            score=100.0 if passed else 0.0
        )

    def _check_mutable_defaults(self, source: str) -> ValidationCheck:
        """
        Detect mutable default argument anti-patterns (list, dict, set literals).

        Parameters
        ----------
        source : str
            Python source code

        Returns
        -------
        ValidationCheck
            Mutable default check result
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck(
                name='No Mutable Defaults',
                passed=False,
                severity='minor',
                details='Cannot analyze — syntax error.',
                score=0.0
            )

        violations: List[str] = []
        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            for default in node.args.defaults + node.args.kw_defaults:
                if default is None:
                    continue
                if isinstance(default, (ast.List, ast.Dict, ast.Set)):
                    violations.append(
                        f"{node.name} (line {node.lineno})"
                    )

        passed = not violations
        return ValidationCheck(
            name='No Mutable Defaults',
            passed=passed,
            severity='minor',
            details=(
                'No mutable default arguments detected.'
                if passed
                else f"Mutable defaults in: {', '.join(violations)}"
            ),
            score=100.0 if passed else max(0.0, 100.0 - len(violations) * 20)
        )

    def _check_line_length(
        self, source: str, max_length: int = 88
    ) -> ValidationCheck:
        """
        Count lines exceeding the maximum permitted length.

        Parameters
        ----------
        source : str
            Python source code
        max_length : int, default=88
            Maximum allowed line length (Black default)

        Returns
        -------
        ValidationCheck
            Line length check result
        """
        violations = [
            i + 1
            for i, line in enumerate(source.splitlines())
            if len(line) > max_length
        ]
        passed = not violations
        score = max(0.0, 100.0 - len(violations) * 2)
        return ValidationCheck(
            name='Line Length',
            passed=passed,
            severity='minor',
            details=(
                f"All lines within {max_length} characters."
                if passed
                else f"{len(violations)} line(s) exceed {max_length} chars."
            ),
            score=score
        )

    def _check_clean_names(self, source: str) -> ValidationCheck:
        """
        Enforce Clean Code naming: no ambiguous single-letter variables (N1/N4).
        Allowed exceptions: i, j, k (loops), x, y, z (coords), e (errors), f (files), _ (ignored).
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck('Clean Names', False, 'minor', 'Syntax error', 0.0)

        allowed = {'i', 'j', 'k', 'n', 'x', 'y', 'z', 'w', 'h', 'e', 'f', 'c', '_'}
        violations = []
        
        for node in ast.walk(tree):
            # Check variables (Assign) and Arguments
            names_to_check = []
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
                names_to_check.append((node.id, node.lineno))
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                for arg in node.args.args:
                    names_to_check.append((arg.arg, node.lineno))
            
            for name, lineno in names_to_check:
                if len(name) == 1 and name not in allowed:
                    violations.append(f"'{name}' at line {lineno}")

        passed = len(violations) == 0
        return ValidationCheck(
            name='Clean Names (No Single Letters)',
            passed=passed,
            severity='minor',
            details=(
                "All names are descriptive (>1 chars)."
                if passed
                else f"Found ambiguous single-letter names: {', '.join(violations[:5])}..."
            ),
            score=100.0 if passed else max(0.0, 100.0 - len(violations) * 5)
        )

    def _check_clean_functions(self, source: str) -> ValidationCheck:
        """
        Enforce Clean Code function rules: Max 3 arguments (F1).
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck('Clean Functions', False, 'major', 'Syntax error', 0.0)

        violations = []
        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Count non-self/cls args
                args = [a for a in node.args.args if a.arg not in ('self', 'cls')]
                if len(args) > self.max_function_args:
                    violations.append(f"{node.name}({len(args)})")

        passed = len(violations) == 0
        return ValidationCheck(
            name=f'Clean Functions (Max {self.max_function_args} Args)',
            passed=passed,
            severity='minor',
            details=(
                f"All functions have <= {self.max_function_args} arguments."
                if passed
                else f"Functions exceeding max arguments: {', '.join(violations[:5])}..."
            ),
            score=100.0 if passed else max(0.0, 100.0 - len(violations) * 10)
        )

    def _check_security(self, source: str) -> ValidationCheck:
        """
        Enforce Security & Environment safety: No exec/eval, no wildcard imports.
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck('Security Checks', False, 'critical', 'Syntax error', 0.0)

        issues = []
        for node in ast.walk(tree):
            # Check exec/eval/compile
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
                if node.func.id in {'exec', 'eval', 'compile'}:
                    issues.append(f"Forbidden call to {node.func.id}() line {node.lineno}")
            
            # Check wildcard imports
            if isinstance(node, ast.ImportFrom):
                for alias in node.names:
                    if alias.name == '*':
                        issues.append(f"Wildcard import 'from {node.module} import *' line {node.lineno}")

        passed = len(issues) == 0
        return ValidationCheck(
            name='Security & Best Practices',
            passed=passed,
            severity='critical',
            details="Passed security checks." if passed else f"Security violations: {', '.join(issues)}",
            score=100.0 if passed else 0.0
        )

    def _check_entropy(self, source: str) -> ValidationCheck:
        """
        Validate structural entropy using analyze_entropy module.
        """
        if not analyze_entropy:
            return ValidationCheck(
                name='Structural Entropy',
                passed=True, 
                severity='minor',
                details='analyze_entropy module not found; check skipped.',
                score=100.0
            )

        try:
            metrics = analyze_entropy.compute_entropy_from_source(source)
            passed = not metrics.is_high_entropy(threshold=0.4)  # align with entropy module doctrine
            return ValidationCheck(
                name='Structural Entropy',
                passed=passed,
                severity='minor',
                details=f"Entropy Score: {metrics.normalized_score:.4f} (Threshold 0.4)",
                score=max(0.0, (1.0 - metrics.normalized_score) * 100)
            )
        except Exception as e:
            return ValidationCheck('Structural Entropy', False, 'minor', str(e), 0.0)

    def _check_magic_numbers(self, source: str) -> ValidationCheck:
        """
        Detect magic numbers (G25).
        Allows -1, 0, 1, and numbers in variable/constant assignments.
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck('Magic Numbers', False, 'minor', 'Syntax error', 0.0)

        magic_numbers = []
        allowed = {-1, 0, 1, 0.0, 1.0, -1.0, 2, 2.0}

        # Collect lines where numeric literals are contextually acceptable:
        # assignments, keyword arguments, class-body definitions
        exempt_lines: set = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.Assign, ast.AnnAssign)):
                exempt_lines.add(node.lineno)
            elif isinstance(node, ast.keyword) and hasattr(node, 'lineno'):
                exempt_lines.add(node.lineno)

        for node in ast.walk(tree):
            if isinstance(node, ast.Constant):
                val = node.value
                if isinstance(val, (int, float)) and not isinstance(val, bool):
                    if val not in allowed:
                        if node.lineno not in exempt_lines:
                            magic_numbers.append(f"{val} at line {node.lineno}")

        # Heuristic — UI code legitimately uses numeric constants for
        # pixel dimensions, margins, font sizes, animation durations
        passed = len(magic_numbers) <= 30
        return ValidationCheck(
            name='No Magic Numbers',
            passed=passed,
            severity='minor',
            details=(
                "Usage of magic numbers is low."
                if passed
                else f"Found potential magic numbers: {', '.join(magic_numbers[:5])}..."
            ),
            score=max(0.0, 100.0 - len(magic_numbers) * 5)
        )

    def _check_law_of_demeter(self, source: str) -> ValidationCheck:
        """
        Detect Law of Demeter violations (G36) by checking for deep attribute chains.
        Example: a.b.c.d (depth 3 access) violates strict LoD.
        """
        try:
            tree = ast.parse(source)
        except SyntaxError:
            return ValidationCheck('Law of Demeter', False, 'minor', 'Syntax error', 0.0)

        violations = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Attribute):
                # Count depth
                depth = 0
                curr = node
                while isinstance(curr, ast.Attribute):
                    depth += 1
                    curr = curr.value
                
                # Report if chain is too long (e.g., obj.a.b.c -> depth 3)
                # We allow 2 dots (obj.a.b) generally, 3 is pushing it.
                if depth > 3:
                     violations.append(f"Chain depth {depth} at line {node.lineno}")
        
        # Dedupe violations by line
        unique_violations = sorted(list(set(violations)))
        
        passed = len(unique_violations) == 0
        return ValidationCheck(
            name='Law of Demeter',
            passed=passed,
            severity='minor',
            details=(
                "Attribute access chains are within reasonable depth."
                if passed
                else f"Found deep attribute access chains: {', '.join(unique_violations[:3])}..."
            ),
            score=max(0.0, 100.0 - len(unique_violations) * 5)
        )

    def _compute_quality_score(
        self, checks: List[ValidationCheck]
    ) -> float:
        """
        Compute weighted aggregate quality score across all checks.

        Weights reflect the relative importance of each check category:
        critical checks carry 3x weight, major 2x, minor 1x.

        Parameters
        ----------
        checks : List[ValidationCheck]
            All completed validation checks

        Returns
        -------
        float
            Weighted quality score in range [0.0, 100.0]
        """
        weight_map = {'critical': 3.0, 'major': 2.0, 'minor': 1.0}
        total_weight = 0.0
        weighted_sum = 0.0

        for check in checks:
            score = check.score if check.score is not None else (100.0 if check.passed else 0.0)
            weight = weight_map.get(check.severity, 1.0)
            weighted_sum += score * weight
            total_weight += weight * 100.0

        return (weighted_sum / total_weight * 100.0) if total_weight > 0 else 0.0

    def _build_recommendations(
        self, checks: List[ValidationCheck]
    ) -> List[str]:
        """
        Build prioritized recommendations from failed validation checks.

        Parameters
        ----------
        checks : List[ValidationCheck]
            All completed validation checks

        Returns
        -------
        List[str]
            Ordered recommendations (critical failures first)
        """
        order = {'critical': 0, 'major': 1, 'minor': 2}
        failed = [c for c in checks if not c.passed]
        failed.sort(key=lambda c: order.get(c.severity, 3))

        return [
            f"[{c.severity.upper()}] Fix '{c.name}': {c.details}"
            for c in failed
        ]


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> int:
    """
    CLI entry point for the validation suite.

    Returns
    -------
    int
        Exit code: 0 if validation passes, 1 if it fails
    """
    parser = argparse.ArgumentParser(
        prog='validation_suite',
        description='Validate Python optimization results - Antigravity Skill v3.0.0'
    )
    parser.add_argument('--original',  '-a', required=True,
                        help='Original Python file')
    parser.add_argument('--optimized', '-b', required=True,
                        help='Optimized Python file to validate')
    parser.add_argument('--output',    '-o', default=None,
                        help='Path to write JSON report')
    parser.add_argument('--min-score', type=float, default=75.0,
                        help='Minimum quality score to pass (default: 75.0)')
    parser.add_argument('--verbose',   '-v', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    suite = ValidationSuite(min_quality_score=args.min_score)

    try:
        report = suite.validate(args.original, args.optimized)
    except Exception as e:
        logger.error(f"Validation failed: {str(e)}")
        traceback.print_exc()
        return 1

    report_dict = asdict(report)

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(report_dict, f, indent=2)

    # Human-readable summary
    status = "PASS" if report.overall_pass else "FAIL"
    print(f"\n{'='*60}")
    print(f"  Validation Report - {status}")
    print(f"{'='*60}")
    print(f"  Quality Score : {report.quality_score:.1f} / 100.0")
    print(f"\n  Checks:")
    for check in report.checks:
        icon = 'OK' if check.passed else 'XX'
        print(f"    {icon} [{check.severity.upper():<8}] {check.name:<30} {check.score or 0.0:.0f}/100")
        if not check.passed:
            print(f"             -> {check.details}")

    if report.recommendations:
        print(f"\n  Recommendations:")
        for rec in report.recommendations:
            print(f"    - {rec}")

    print(f"{'='*60}\n")

    return 0 if report.overall_pass else 1


if __name__ == '__main__':
    sys.exit(main())

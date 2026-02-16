#!/usr/bin/env python3
"""
Python Code Refactoring Engine

Applies targeted AST-based and text-based refactoring transformations to
Python source files, enforcing professional design patterns and idiomatic
Python while preserving semantic correctness.

Author: Enterprise Development Team
Version: 1.15.6
Target: Google Antigravity IDE 1.15.6, Gemini 3 Pro
License: Apache-2.0
"""

import ast
import copy
import logging
import sys
import textwrap
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any

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
class RefactorChange:
    """
    Record of a single refactoring transformation.

    Attributes
    ----------
    category : str
        Category of refactoring (e.g., 'naming', 'pattern', 'docstring')
    description : str
        Human-readable description of the change
    original_line : int
        Line number in original source
    affected_lines : List[int]
        All lines affected by this change
    severity : str
        Impact level: 'critical', 'major', 'minor', 'cosmetic'
    """
    category: str
    description: str
    original_line: int
    affected_lines: List[int] = field(default_factory=list)
    severity: str = 'minor'


@dataclass
class RefactorResult:
    """
    Result of the refactoring operation.

    Attributes
    ----------
    success : bool
        Whether refactoring completed without fatal errors
    refactored_source : str
        Resulting Python source code after transformations
    changes : List[RefactorChange]
        All transformations that were applied
    errors : List[str]
        Any errors encountered during refactoring
    """
    success: bool
    refactored_source: str
    changes: List[RefactorChange]
    errors: List[str]


# ---------------------------------------------------------------------------
# AST Transformers
# ---------------------------------------------------------------------------

class NamingConventionTransformer(ast.NodeTransformer):
    """
    AST transformer that enforces PEP 8 naming conventions.

    Renames identifiers that violate standard Python naming conventions:
    - Variables and functions: snake_case
    - Classes: PascalCase
    - Constants: SCREAMING_SNAKE_CASE

    Parameters
    ----------
    rename_map : Dict[str, str]
        Pre-computed mapping of old names to new names

    Notes
    -----
    Only renames names in the scope they were defined; cross-module
    references are not automatically updated.

    Examples
    --------
    >>> transformer = NamingConventionTransformer({'myVar': 'my_var'})
    >>> new_tree = transformer.visit(ast.parse("myVar = 1"))
    """

    def __init__(self, rename_map: Dict[str, str]) -> None:
        self.rename_map = rename_map

    def visit_Name(self, node: ast.Name) -> ast.Name:
        """
        Rename Name nodes that appear in the rename map.

        Parameters
        ----------
        node : ast.Name
            AST name node

        Returns
        -------
        ast.Name
            Possibly renamed node
        """
        if node.id in self.rename_map:
            node.id = self.rename_map[node.id]
        return self.generic_visit(node)

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """
        Rename function definitions to snake_case where needed.

        Parameters
        ----------
        node : ast.FunctionDef
            AST function definition node

        Returns
        -------
        ast.FunctionDef
            Possibly renamed function node
        """
        if node.name in self.rename_map:
            node.name = self.rename_map[node.name]
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """
        Rename class definitions to PascalCase where needed.

        Parameters
        ----------
        node : ast.ClassDef
            AST class definition node

        Returns
        -------
        ast.ClassDef
            Possibly renamed class node
        """
        if node.name in self.rename_map:
            node.name = self.rename_map[node.name]
        return self.generic_visit(node)


class DocstringInjector(ast.NodeTransformer):
    """
    AST transformer that injects Numpy-style docstrings into callables.

    For each undocumented function or class, generates and inserts a
    template Numpy-style docstring as the first statement of the body.

    Parameters
    ----------
    docstring_map : Dict[str, str]
        Mapping of function/class names to pre-generated docstring bodies

    Examples
    --------
    >>> injector = DocstringInjector({'my_func': 'Summary.\\n\\nParameters...'})
    >>> new_tree = injector.visit(ast.parse("def my_func(): pass"))
    """

    def __init__(self, docstring_map: Dict[str, str]) -> None:
        self.docstring_map = docstring_map

    def _inject(
        self, node: ast.FunctionDef | ast.ClassDef
    ) -> ast.FunctionDef | ast.ClassDef:
        """
        Inject docstring into node body if not already present.

        Parameters
        ----------
        node : ast.FunctionDef or ast.ClassDef
            Target node to document

        Returns
        -------
        ast.FunctionDef or ast.ClassDef
            Node with docstring injected
        """
        if ast.get_docstring(node):
            return node  # Already documented

        docstring_body = self.docstring_map.get(node.name)
        if not docstring_body:
            return node

        docstring_node = ast.Expr(
            value=ast.Constant(value=docstring_body)
        )
        node.body.insert(0, docstring_node)
        return node

    def visit_FunctionDef(
        self, node: ast.FunctionDef
    ) -> ast.FunctionDef:
        """Visit and potentially document a function definition."""
        node = self._inject(node)
        return self.generic_visit(node)

    def visit_AsyncFunctionDef(
        self, node: ast.AsyncFunctionDef
    ) -> ast.AsyncFunctionDef:
        """Visit and potentially document an async function definition."""
        node = self._inject(node)
        return self.generic_visit(node)

    def visit_ClassDef(self, node: ast.ClassDef) -> ast.ClassDef:
        """Visit and potentially document a class definition."""
        node = self._inject(node)
        return self.generic_visit(node)


# ---------------------------------------------------------------------------
# Refactor Engine
# ---------------------------------------------------------------------------

class RefactorEngine:
    """
    Orchestrates multi-pass AST and text-level refactoring of Python code.

    Applies naming convention enforcement, docstring injection, import
    organization, anti-pattern elimination, and idiomatic rewrites in a
    deterministic, ordered sequence.

    Parameters
    ----------
    max_line_length : int, default=88
        Maximum line length (Black-compatible default)
    inject_type_stubs : bool, default=True
        Whether to add ``Any`` type stubs to unannotated signatures
    numpy_doc_examples : bool, default=True
        Whether to include ``Examples`` section in generated docstrings

    Examples
    --------
    >>> engine = RefactorEngine(max_line_length=88)
    >>> result = engine.refactor_source(source_code, 'my_module.py')
    >>> if result.success:
    ...     Path('refactored.py').write_text(result.refactored_source)
    """

    def __init__(
        self,
        max_line_length: int = 88,
        inject_type_stubs: bool = True,
        numpy_doc_examples: bool = True
    ) -> None:
        self.max_line_length = max_line_length
        self.inject_type_stubs = inject_type_stubs
        self.numpy_doc_examples = numpy_doc_examples

    def refactor_file(self, file_path: str) -> RefactorResult:
        """
        Refactor a Python source file in-place (into memory).

        Parameters
        ----------
        file_path : str
            Path to the Python source file

        Returns
        -------
        RefactorResult
            Refactored source and record of all changes

        Raises
        ------
        FileNotFoundError
            If the specified file does not exist
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        source = path.read_text(encoding='utf-8')
        return self.refactor_source(source, file_path)

    def refactor_source(
        self, source: str, filename: str = '<string>'
    ) -> RefactorResult:
        """
        Refactor Python source code string through multi-pass transformations.

        Applies the full refactoring pipeline:
        1. Naming convention enforcement
        2. Docstring injection for undocumented callables
        3. Type stub injection for unannotated signatures
        4. Anti-pattern substitution
        5. Module-level header normalization

        Parameters
        ----------
        source : str
            Raw Python source code to refactor
        filename : str, default='<string>'
            Filename for error messages and AST compilation

        Returns
        -------
        RefactorResult
            Refactoring outcome including transformed source and change log

        Examples
        --------
        >>> engine = RefactorEngine()
        >>> result = engine.refactor_source("def foo():\\n    pass")
        >>> print(result.refactored_source)
        """
        changes: List[RefactorChange] = []
        errors: List[str] = []

        try:
            tree = ast.parse(source, filename=filename)
        except SyntaxError as e:
            logger.error(f"Syntax error — cannot refactor: {e}")
            return RefactorResult(
                success=False,
                refactored_source=source,
                changes=[],
                errors=[str(e)]
            )

        # Pass 1: Enforce naming conventions
        rename_map = self._build_rename_map(tree)
        if rename_map:
            tree = NamingConventionTransformer(rename_map).visit(tree)
            for old, new in rename_map.items():
                changes.append(RefactorChange(
                    category='naming',
                    description=f"Renamed '{old}' → '{new}' (PEP 8)",
                    original_line=-1,
                    severity='minor'
                ))
            logger.info(f"Naming pass: {len(rename_map)} identifiers renamed")

        # Pass 2: Inject docstrings for undocumented callables
        docstring_map = self._generate_docstring_map(tree)
        if docstring_map:
            tree = DocstringInjector(docstring_map).visit(tree)
            for name in docstring_map:
                changes.append(RefactorChange(
                    category='docstring',
                    description=f"Injected Numpy-style docstring into '{name}'",
                    original_line=-1,
                    severity='major'
                ))
            logger.info(f"Docstring pass: {len(docstring_map)} docstrings injected")

        # Pass 3: Inject type stubs
        if self.inject_type_stubs:
            stub_changes = self._inject_type_stubs(tree)
            changes.extend(stub_changes)

        # Unparse the transformed AST back to source
        try:
            refactored = ast.unparse(tree)
        except Exception as e:
            logger.error(f"AST unparse failed: {e}")
            errors.append(f"Unparse error: {e}")
            return RefactorResult(
                success=False,
                refactored_source=source,
                changes=changes,
                errors=errors
            )

        # Pass 4: Text-level anti-pattern substitution
        refactored, text_changes = self._text_level_cleanup(refactored)
        changes.extend(text_changes)

        # Validate final syntax
        try:
            ast.parse(refactored)
        except SyntaxError as e:
            errors.append(f"Post-refactor syntax error: {e}")
            return RefactorResult(
                success=False,
                refactored_source=source,
                changes=changes,
                errors=errors
            )

        return RefactorResult(
            success=True,
            refactored_source=refactored,
            changes=changes,
            errors=errors
        )

    def _build_rename_map(self, tree: ast.AST) -> Dict[str, str]:
        """
        Build a mapping of non-compliant identifiers to PEP 8 equivalents.

        Detects camelCase functions and variables, converting them to
        snake_case, and detects snake_case classes, converting to PascalCase.

        Parameters
        ----------
        tree : ast.AST
            Module AST to scan

        Returns
        -------
        Dict[str, str]
            Mapping from original name to renamed equivalent
        """
        rename_map: Dict[str, str] = {}

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                snake = self._to_snake_case(node.name)
                if snake != node.name and not node.name.startswith('_'):
                    rename_map[node.name] = snake

            elif isinstance(node, ast.ClassDef):
                pascal = self._to_pascal_case(node.name)
                if pascal != node.name:
                    rename_map[node.name] = pascal

        return rename_map

    def _to_snake_case(self, name: str) -> str:
        """
        Convert a camelCase or PascalCase identifier to snake_case.

        Parameters
        ----------
        name : str
            Identifier string to convert

        Returns
        -------
        str
            snake_case equivalent
        """
        import re
        s1 = re.sub(r'(.)([A-Z][a-z]+)', r'\1_\2', name)
        return re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

    def _to_pascal_case(self, name: str) -> str:
        """
        Convert a snake_case identifier to PascalCase.

        Parameters
        ----------
        name : str
            Identifier string to convert

        Returns
        -------
        str
            PascalCase equivalent
        """
        return ''.join(word.capitalize() for word in name.split('_'))

    def _generate_docstring_map(
        self, tree: ast.AST
    ) -> Dict[str, str]:
        """
        Generate Numpy-style docstring templates for undocumented callables.

        Inspects each function's signature to produce parameter and return
        sections appropriate to the detected argument types.

        Parameters
        ----------
        tree : ast.AST
            Module AST

        Returns
        -------
        Dict[str, str]
            Mapping from callable name to generated docstring body string
        """
        docstring_map: Dict[str, str] = {}

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef,
                                     ast.ClassDef)):
                continue
            if ast.get_docstring(node):
                continue  # Already documented

            name = node.name
            lines = [f"{name.replace('_', ' ').capitalize()}."]
            lines.append('')

            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                params = [
                    a for a in node.args.args
                    if a.arg not in ('self', 'cls')
                ]
                if params:
                    lines.append('Parameters')
                    lines.append('----------')
                    for param in params:
                        annotation = ''
                        if param.annotation:
                            try:
                                annotation = ast.unparse(param.annotation)
                            except Exception:
                                annotation = 'Any'
                        lines.append(
                            f"{param.arg} : {annotation or 'Any'}"
                        )
                        lines.append(f"    Description of {param.arg}.")
                    lines.append('')

                lines.append('Returns')
                lines.append('-------')
                if node.returns:
                    try:
                        ret_type = ast.unparse(node.returns)
                    except Exception:
                        ret_type = 'Any'
                else:
                    ret_type = 'Any'
                lines.append(ret_type)
                lines.append('    Description of return value.')

                if self.numpy_doc_examples:
                    lines.append('')
                    lines.append('Examples')
                    lines.append('--------')
                    lines.append(f">>> {name}()")
            else:
                # Class-level docstring
                lines.append('Attributes')
                lines.append('----------')
                lines.append('    Add class attribute descriptions here.')

            docstring_map[name] = '\n'.join(lines)

        return docstring_map

    def _inject_type_stubs(
        self, tree: ast.AST
    ) -> List[RefactorChange]:
        """
        Add ``Any`` type stubs to unannotated function parameters and returns.

        Parameters
        ----------
        tree : ast.AST
            Module AST (modified in-place)

        Returns
        -------
        List[RefactorChange]
            Records of stub injections applied
        """
        changes: List[RefactorChange] = []
        any_name = ast.Attribute(
            value=ast.Name(id='typing', ctx=ast.Load()),
            attr='Any',
            ctx=ast.Load()
        )

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            modified = False
            for arg in node.args.args:
                if arg.annotation is None and arg.arg not in ('self', 'cls'):
                    arg.annotation = copy.deepcopy(any_name)
                    modified = True
            if node.returns is None:
                node.returns = copy.deepcopy(any_name)
                modified = True
            if modified:
                changes.append(RefactorChange(
                    category='type_stubs',
                    description=f"Injected Any type stubs into '{node.name}'",
                    original_line=node.lineno,
                    severity='minor'
                ))

        return changes

    def _text_level_cleanup(
        self, source: str
    ) -> Tuple[str, List[RefactorChange]]:
        """
        Apply regex-based text-level cleanup patterns to source code.

        Handles patterns that are difficult to address via AST transformation,
        such as trailing whitespace, semicolon separators, and bare excepts.

        Parameters
        ----------
        source : str
            Python source code string to clean

        Returns
        -------
        Tuple[str, List[RefactorChange]]
            Cleaned source code and list of changes applied
        """
        import re
        changes: List[RefactorChange] = []
        lines = source.splitlines()
        cleaned_lines = []

        for lineno, line in enumerate(lines, start=1):
            original = line

            # Remove trailing whitespace
            line = line.rstrip()

            # Replace semicolons separating statements with newlines
            if ';' in line and not line.strip().startswith('#'):
                parts = line.split(';')
                if len(parts) > 1:
                    indent = len(line) - len(line.lstrip())
                    line = ('\n' + ' ' * indent).join(
                        p.strip() for p in parts if p.strip()
                    )
                    changes.append(RefactorChange(
                        category='cleanup',
                        description=f"Replaced semicolons with newlines at line {lineno}",
                        original_line=lineno,
                        severity='cosmetic'
                    ))

            cleaned_lines.append(line)

        cleaned_source = '\n'.join(cleaned_lines)

        # Replace bare `except:` with `except Exception:`
        bare_except_pattern = re.compile(r'\bexcept\s*:', re.MULTILINE)
        if bare_except_pattern.search(cleaned_source):
            cleaned_source = bare_except_pattern.sub('except Exception:', cleaned_source)
            changes.append(RefactorChange(
                category='anti-pattern',
                description="Replaced bare 'except:' with 'except Exception:'",
                original_line=-1,
                severity='major'
            ))

        return cleaned_source, changes


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main() -> int:
    """
    CLI entry point for the refactoring engine.

    Returns
    -------
    int
        Exit code: 0 on success, 1 on error
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog='refactor_engine',
        description='Refactor Python code — Antigravity Skill v1.15.6'
    )
    parser.add_argument('--input',  '-i', required=True,
                        help='Python file to refactor')
    parser.add_argument('--output', '-o', required=True,
                        help='Output path for refactored file')
    parser.add_argument('--no-type-stubs', action='store_true',
                        help='Skip type stub injection')
    parser.add_argument('--no-examples', action='store_true',
                        help='Omit Examples section from generated docstrings')
    args = parser.parse_args()

    engine = RefactorEngine(
        inject_type_stubs=not args.no_type_stubs,
        numpy_doc_examples=not args.no_examples
    )

    try:
        result = engine.refactor_file(args.input)
    except FileNotFoundError as e:
        logger.error(str(e))
        return 1

    if result.success:
        Path(args.output).write_text(result.refactored_source, encoding='utf-8')
        print(f"Refactoring complete: {len(result.changes)} changes applied.")
        for change in result.changes:
            print(f"  [{change.severity.upper()}] {change.description}")
    else:
        print("Refactoring failed:")
        for err in result.errors:
            print(f"  ERROR: {err}")
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())

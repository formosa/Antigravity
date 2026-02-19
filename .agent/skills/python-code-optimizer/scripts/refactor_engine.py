#!/usr/bin/env python3
"""
Python Code Refactoring Engine

Applies targeted AST-based and text-based refactoring transformations to
Python source files, enforcing professional design patterns and idiomatic
Python while preserving semantic correctness.

Author: Enterprise Development Team
Version: 3.0.0
Target: Google Antigravity IDE 1.16.5, Gemini 3 Flash
License: Apache-2.0
"""

import ast
import copy
import builtins
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

    def visit_Attribute(self, node: ast.Attribute) -> ast.Attribute:
        """
        Rename attribute access that matches the rename map.

        Parameters
        ----------
        node : ast.Attribute
            AST attribute node

        Returns
        -------
        ast.Attribute
            Possibly renamed attribute node
        """
        if node.attr in self.rename_map:
            node.attr = self.rename_map[node.attr]
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


class StringDependencyVisitor(ast.NodeVisitor):
    """
    AST visitor to identify local variable dependencies within a node.

    Used to determine which variables must be passed as arguments to
    extracted string helper functions.
    """

    def __init__(self) -> None:
        self.dependencies: Set[str] = set()

    def visit_Name(self, node: ast.Name) -> None:
        """Collect variable names loaded in the node."""
        if isinstance(node.ctx, ast.Load):
            # Ignore builtins to avoid cluttering signatures
            if node.id in builtins.__dict__:
                return
            self.dependencies.add(node.id)

    def visit_Attribute(self, node: ast.Attribute) -> None:
        """
        Visit attributes to ensure root objects are captured.

        For 'self.theme.color', this naturally visits 'self' via generic_visit.
        """
        self.generic_visit(node)


class LargeStringModularizer(ast.NodeTransformer):
    """
    AST transformer that extracts large strings into module-level helper functions.

    Identifies ast.Constant (str) and ast.JoinedStr nodes that exceed
    complexity thresholds and replaces them with calls to generated
    helper functions, improving code readability.
    """

    def __init__(self, min_length: int = 200, min_lines: int = 4) -> None:
        self.min_length = min_length
        self.min_lines = min_lines
        self.new_functions: List[ast.FunctionDef] = []
        self.in_function = False
        self._extracted_hashes: Dict[str, str] = {}

    def visit_FunctionDef(self, node: ast.FunctionDef) -> ast.FunctionDef:
        """Track context to ensure we only refactor strings inside functions."""
        self.in_function = True
        node = self.generic_visit(node)
        self.in_function = False
        return node

    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> ast.AsyncFunctionDef:
        """Track context for async functions."""
        self.in_function = True
        node = self.generic_visit(node)
        self.in_function = False
        return node

    def visit_Assign(self, node: ast.Assign) -> ast.Assign:
        """Check assignments for large string values."""
        if not self.in_function:
            return self.generic_visit(node)

        # Check if value is a string or f-string
        if isinstance(node.value, (ast.Constant, ast.JoinedStr)):
            if self._is_large_string(node.value):
                # We found a candidate.
                # Heuristic for name: if assigning to 's', use 's'
                target_name = "content"
                if len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
                    target_name = node.targets[0].id

                replacement_call = self._extract_to_helper(node.value, target_name)
                node.value = replacement_call
                return node

        return self.generic_visit(node)

    def visit_Return(self, node: ast.Return) -> ast.Return:
        """Check returns for large string values."""
        if not self.in_function or not node.value:
            return self.generic_visit(node)

        if isinstance(node.value, (ast.Constant, ast.JoinedStr)):
            if self._is_large_string(node.value):
                replacement_call = self._extract_to_helper(node.value, "return")
                node.value = replacement_call
                return node

        return self.generic_visit(node)

    # QSS/CSS/HTML markers — strings containing these are domain templates
    # that must NOT be extracted into helper functions.
    _TEMPLATE_MARKERS = frozenset({
        'QWidget', 'QPushButton', 'QLabel', 'QLineEdit', 'QTextEdit',
        'QScrollBar', 'QComboBox', 'QCheckBox', 'QRadioButton',
        'QTabWidget', 'QMenu', 'QToolTip', 'QHeaderView', 'QTreeView',
        'QListWidget', 'QTableWidget', 'QProgressBar', 'QSlider',
        'QGroupBox', 'QFrame', 'QMainWindow', 'QDialog', 'QStatusBar',
        'QSplitter', 'QTabBar', 'QScrollArea', 'QToolBar', 'QMenuBar',
        'background-color:', 'font-family:', 'border-radius:',
        'font-size:', 'font-weight:', 'padding:', 'margin:',
        'border:', '<html', '<div', '<style',
    })

    def _is_large_string(self, node: ast.AST) -> bool:
        """Determine if a node represents a string exceeding complexity limits."""
        val = ""
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            val = node.value
        elif isinstance(node, ast.JoinedStr):
            # Approximation for f-strings
            try:
                val = ast.unparse(node)
            except Exception:
                return False
        else:
            return False

        # Exclude QSS/CSS/HTML template strings from extraction
        if any(marker in val for marker in self._TEMPLATE_MARKERS):
            return False

        lines = val.count('\n') + 1
        if isinstance(node, ast.JoinedStr):
             # unparse might escape newlines, so count literal \n too just in case
             lines = max(lines, val.count('\\n') + 1)
        
        return len(val) >= self.min_length or lines >= self.min_lines


    def _extract_to_helper(self, node: ast.AST, context_hint: str) -> ast.Call:
        """Generate helper function and return a Call node."""
        # 1. Analyze dependencies
        visitor = StringDependencyVisitor()
        visitor.visit(node)
        deps = sorted(list(visitor.dependencies))

        # 2. Check for duplicate content (same string already extracted)
        content_hash = str(abs(hash(ast.dump(node))))[:8]
        if content_hash in self._extracted_hashes:
            func_name = self._extracted_hashes[content_hash]
            return ast.Call(
                func=ast.Name(id=func_name, ctx=ast.Load()),
                args=[ast.Name(id=dep, ctx=ast.Load()) for dep in deps],
                keywords=[]
            )

        # 3. Generate unique name (prefer assignment context over return)
        if context_hint != "return":
            func_name = f"_get_{context_hint}_content"
        else:
            func_name = f"_get_{context_hint}_{content_hash}"
        self._extracted_hashes[content_hash] = func_name

        # 4. Create FunctionDef
        args = [ast.arg(arg=dep, annotation=None) for dep in deps]
        func_def = ast.FunctionDef(
            name=func_name,
            args=ast.arguments(
                posonlyargs=[], args=args, kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            body=[ast.Return(value=node)],
            decorator_list=[],
            lineno=1  # Dummy
        )
        self.new_functions.append(func_def)

        # 5. Create Call
        call = ast.Call(
            func=ast.Name(id=func_name, ctx=ast.Load()),
            args=[ast.Name(id=dep, ctx=ast.Load()) for dep in deps],
            keywords=[]
        )
        return call


def _infer_param_description(name: str) -> str:
    """
    Generate a context-aware parameter description from its name.

    Parameters
    ----------
    name : str
        Parameter name to generate description for

    Returns
    -------
    str
        Human-readable description string
    """
    _PATTERNS = {
        'file_path': 'Path to the target file.',
        'path': 'File system path.',
        'source': 'Source code string.',
        'text': 'Text content to process.',
        'config': 'Configuration object.',
        'widget': 'Qt widget instance.',
        'parent': 'Parent widget or object.',
        'event': 'Event object from the framework.',
        'index': 'Position index.',
        'name': 'Identifier name.',
        'value': 'Value to set or process.',
        'items': 'Collection of items.',
        'data': 'Data payload.',
        'callback': 'Callable to invoke.',
        'timeout': 'Timeout duration in seconds.',
        'encoding': 'Character encoding.',
        'fmt': 'Format specification string.',
        'level': 'Severity or verbosity level.',
        'key': 'Lookup key.',
        'msg': 'Message string.',
        'message': 'Message string.',
        'args': 'Positional arguments.',
        'kwargs': 'Keyword arguments.',
        'filename': 'Name of the file.',
        'directory': 'Directory path.',
        'url': 'URL string.',
        'size': 'Size dimension.',
        'count': 'Number of items.',
        'flag': 'Boolean flag.',
        'enabled': 'Whether the feature is enabled.',
        'mode': 'Operating mode.',
        'options': 'Configuration options.',
        'result': 'Computation result.',
        'output': 'Output destination.',
        'prefix': 'String prefix.',
        'suffix': 'String suffix.',
        'pattern': 'Search or match pattern.',
        'depth': 'Recursion or nesting depth.',
        'width': 'Width dimension.',
        'height': 'Height dimension.',
        'color': 'Color value.',
        'label': 'Display label.',
        'title': 'Title string.',
        'content': 'Content payload.',
        'template': 'Template string.',
        'context': 'Execution context.',
        'state': 'Current state.',
        'status': 'Status indicator.',
    }
    lower = name.lower()
    for pattern, desc in _PATTERNS.items():
        if lower == pattern or lower.endswith(f'_{pattern}'):
            return desc
    # Fallback: convert name to readable form
    readable = name.replace('_', ' ')
    return f"The {readable}."


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
        numpy_doc_examples: bool = True,
        string_restore_min_newlines: int = 4,
        string_restore_min_length: int = 200
    ) -> None:
        self.max_line_length = max_line_length
        self.inject_type_stubs = inject_type_stubs
        self.numpy_doc_examples = numpy_doc_examples
        self.string_restore_min_newlines = string_restore_min_newlines
        self.string_restore_min_length = string_restore_min_length

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

        # Pass 4: Large String Modularization
        modularizer = LargeStringModularizer(
            min_length=self.string_restore_min_length,
            min_lines=self.string_restore_min_newlines
        )
        tree = modularizer.visit(tree)
        if modularizer.new_functions:
            # Inject new functions after imports
            insert_idx = 0
            for i, node in enumerate(tree.body):
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    insert_idx = i + 1

            for func in reversed(modularizer.new_functions):
                tree.body.insert(insert_idx, func)

            ast.fix_missing_locations(tree)

            changes.append(RefactorChange(
                category='structural',
                description=f"Extracted {len(modularizer.new_functions)} large strings to helper functions",
                original_line=-1,
                severity='major'
            ))
            logger.info(f"Modularization pass: {len(modularizer.new_functions)} strings extracted")

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



        # Pass 5: Text-level anti-pattern substitution
        refactored, text_changes = self._text_level_cleanup(refactored)
        changes.extend(text_changes)

        # Pass 6: Restore collapsed multiline strings
        refactored, string_changes = self._restore_multiline_strings(refactored)
        changes.extend(string_changes)

        # Pass 7: Restore collapsed f-string formatting
        refactored, fstring_changes = self._restore_fstring_formatting(refactored)
        changes.extend(fstring_changes)

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

    # Framework method names that MUST NOT be renamed (Qt, unittest, etc.)
    _FRAMEWORK_NAMES: frozenset = frozenset({
        # Qt virtual overrides (PySide6 / PyQt6)
        'paintEvent', 'resizeEvent', 'mousePressEvent', 'mouseReleaseEvent',
        'mouseMoveEvent', 'mouseDoubleClickEvent', 'wheelEvent',
        'keyPressEvent', 'keyReleaseEvent', 'focusInEvent', 'focusOutEvent',
        'enterEvent', 'leaveEvent', 'closeEvent', 'showEvent', 'hideEvent',
        'timerEvent', 'changeEvent', 'moveEvent', 'dragEnterEvent',
        'dragMoveEvent', 'dragLeaveEvent', 'dropEvent', 'contextMenuEvent',
        'sizeHint', 'minimumSizeHint', 'paintSection', 'drawWidget',
        'setStyleSheet', 'eventFilter', 'childEvent',
        # QSyntaxHighlighter / QAbstractItemModel / QAbstractItemDelegate
        'highlightBlock', 'createIndex', 'headerData', 'setData',
        'insertRows', 'removeRows', 'canFetchMore', 'fetchMore',
        'createEditor', 'setEditorData', 'setModelData',
        'updateEditorGeometry', 'sizeHintForColumn', 'sizeHintForRow',
        # Qt property/signal patterns
        'setupUi', 'retranslateUi',
        # unittest
        'setUp', 'tearDown', 'setUpClass', 'tearDownClass',
        # dataclasses / descriptors
        '__post_init__', '__init_subclass__', '__class_getitem__',
    })

    def _build_rename_map(self, tree: ast.AST) -> Dict[str, str]:
        """
        Build a mapping of non-compliant identifiers to PEP 8 equivalents.

        Detects camelCase functions and variables, converting them to
        snake_case, and detects snake_case classes, converting to PascalCase.
        Excludes dunder methods, Qt/framework overrides, and AST visitor
        convention methods (``visit_*``).

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
                if (snake != node.name
                        and not (node.name.startswith('__')
                                 and node.name.endswith('__'))
                        and node.name not in self._FRAMEWORK_NAMES
                        and not node.name.startswith('visit_')):
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

        Preserves existing casing within each underscore-delimited
        segment. For example, ``my_class`` becomes ``MyClass`` but
        ``AnimatedToggleWidget`` (no underscores) is unchanged.

        Parameters
        ----------
        name : str
            Identifier string to convert

        Returns
        -------
        str
            PascalCase equivalent
        """
        return ''.join(
            word[0].upper() + word[1:] if word else ''
            for word in name.split('_')
        )

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
            readable = name.lstrip('_').replace('_', ' ')
            summary = readable[0].upper() + readable[1:] if readable else readable
            lines = [f"{summary}."]
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
                        lines.append(f"    {_infer_param_description(param.arg)}")
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
                lines.append(f'    Result of {readable}.')

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

        Only targets top-level (module-scope) functions with zero existing
        annotations. Class methods and partially-annotated functions are
        skipped to avoid polluting framework overrides and intentional
        omissions.

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

        # Collect IDs of methods defined inside classes
        _class_method_ids: set = set()
        for cls_node in ast.walk(tree):
            if isinstance(cls_node, ast.ClassDef):
                for item in cls_node.body:
                    if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                        _class_method_ids.add(id(item))

        for node in ast.walk(tree):
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue

            # Skip class methods that are framework overrides
            # (their camelCase names indicate external API contracts)
            if id(node) in _class_method_ids:
                if node.name in self._FRAMEWORK_NAMES:
                    continue

            # Skip if function already has ANY annotation (partial
            # annotation implies the developer intentionally omitted
            # the rest)
            non_self_args = [
                a for a in node.args.args
                if a.arg not in ('self', 'cls')
            ]
            has_any_annotation = (
                any(a.annotation is not None for a in non_self_args)
                or node.returns is not None
            )
            if has_any_annotation:
                continue

            modified = False
            for arg in non_self_args:
                if arg.annotation is None:
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

    def _restore_multiline_strings(
        self, source: str
    ) -> Tuple[str, List[RefactorChange]]:
        """
        Restore collapsed single-line strings to multiline triple-quoted format.

        After ast.unparse(), multiline strings are collapsed into single-line
        strings with escaped newline characters. This pass detects those
        strings via tokenization and restores them to readable form.

        Parameters
        ----------
        source : str
            Python source code (post ast.unparse)

        Returns
        -------
        Tuple[str, List[RefactorChange]]
            Restored source and list of changes applied
        """
        import tokenize as _tok
        import io

        MIN_ESCAPED_NEWLINES = self.string_restore_min_newlines
        MIN_TOKEN_LENGTH = self.string_restore_min_length

        changes: List[RefactorChange] = []

        try:
            tokens = list(
                _tok.generate_tokens(io.StringIO(source).readline)
            )
        except _tok.TokenError:
            return source, changes

        # Collect replacement descriptors
        replacements = []

        for tok in tokens:
            if tok.type != _tok.STRING:
                continue

            raw = tok.string
            if raw.lower().startswith('f'):
                continue
            escaped_count = raw.count('\\n')
            if tok.start[0] != tok.end[0]:
                continue
            if escaped_count < MIN_ESCAPED_NEWLINES:
                continue
            if len(raw) < MIN_TOKEN_LENGTH:
                continue

            # Locate quote delimiter (ast.unparse uses single quotes)
            body_start = raw.find("'")
            if body_start == -1:
                body_start = raw.find('"')
            if body_start == -1:
                continue

            prefix = raw[:body_start]

            # Extract inner content (between quotes)
            inner = raw[body_start + 1:-1]

            # Convert escaped newlines to real newlines
            inner = inner.replace('\\n', '\n')
            # Unescape single-quotes that ast.unparse may have escaped
            inner = inner.replace("\\'", "'")

            # Build triple-quoted replacement
            new_text = prefix + '"""' + inner + '"""'

            replacements.append((
                tok.start[0], tok.start[1],
                tok.end[0], tok.end[1],
                new_text
            ))

        if not replacements:
            return source, changes

        # Apply replacements in reverse order to preserve positions
        lines = source.splitlines(True)
        for start_row, start_col, end_row, end_col, new_text in reversed(replacements):
            sr = start_row - 1
            er = end_row - 1

            before = lines[sr][:start_col]
            after = lines[er][end_col:]

            new_lines = (before + new_text + after).splitlines(True)
            lines[sr:er + 1] = new_lines

        restored = ''.join(lines)

        # Validate syntax after restoration
        try:
            ast.parse(restored)
        except SyntaxError:
            return source, []  # Safe fallback: return original

        changes.append(RefactorChange(
            category='readability',
            description=(
                "Restored {} collapsed string(s) to "
                "multiline triple-quoted format"
            ).format(len(replacements)),
            original_line=-1,
            severity='major'
        ))

        return restored, changes

    def _restore_fstring_formatting(
        self, source: str
    ) -> Tuple[str, List[RefactorChange]]:
        """
        Restore collapsed f-strings to readable multiline triple-quoted format.

        After ast.unparse(), multiline f-strings are collapsed into single-line
        strings with escaped newline characters. This pass detects those
        f-strings via tokenization and restores them to readable form.

        Parameters
        ----------
        source : str
            Python source code (post ast.unparse)

        Returns
        -------
        Tuple[str, List[RefactorChange]]
            Restored source and list of changes applied
        """
        import tokenize as _tok
        import io

        changes: List[RefactorChange] = []

        try:
            tokens = list(
                _tok.generate_tokens(io.StringIO(source).readline)
            )
        except _tok.TokenError:
            return source, changes

        replacements = []

        for tok in tokens:
            if tok.type != _tok.STRING:
                continue

            raw = tok.string
            # Only process f-strings
            if not raw.lower().startswith('f'):
                continue
            # Skip already-multiline tokens
            if tok.start[0] != tok.end[0]:
                continue

            escaped_count = raw.count('\\n')
            if escaped_count < self.string_restore_min_newlines:
                continue
            if len(raw) < self.string_restore_min_length:
                continue

            # Locate the opening quote after the 'f' prefix
            prefix_end = 1  # skip 'f'
            quote_char = raw[prefix_end]
            if quote_char not in ("'", '"'):
                continue

            # Extract inner content (between quotes)
            inner = raw[prefix_end + 1:-1]

            # Convert escaped newlines/tabs to real characters
            inner = inner.replace('\\n', '\n')
            inner = inner.replace('\\t', '\t')

            # Build triple-quoted replacement
            new_text = 'f"""' + inner + '"""'

            replacements.append((
                tok.start[0], tok.start[1],
                tok.end[0], tok.end[1],
                new_text
            ))

        if not replacements:
            return source, changes

        # Apply replacements in reverse order to preserve positions
        lines = source.splitlines(True)
        for start_row, start_col, end_row, end_col, new_text in reversed(replacements):
            sr = start_row - 1
            er = end_row - 1

            before = lines[sr][:start_col]
            after = lines[er][end_col:]

            new_lines = (before + new_text + after).splitlines(True)
            lines[sr:er + 1] = new_lines

        restored = ''.join(lines)

        # Validate syntax after restoration
        try:
            ast.parse(restored)
        except SyntaxError:
            return source, changes  # Safe fallback

        changes.append(RefactorChange(
            category='readability',
            description=(
                "Restored {} collapsed f-string(s) to "
                "multiline triple-quoted format"
            ).format(len(replacements)),
            original_line=-1,
            severity='major'
        ))

        return restored, changes


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
        description='Refactor Python code — Antigravity Skill v3.0.0'
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

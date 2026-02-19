"""Tests for framework method exclusion and type stub injection scope."""

import ast
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from refactor_engine import RefactorEngine


class TestFrameworkExclusion(unittest.TestCase):
    """Verify that framework override methods are never renamed."""

    def setUp(self):
        self.engine = RefactorEngine()

    def test_highlight_block_not_renamed(self):
        source = (
            "from PySide6.QtGui import QSyntaxHighlighter\n"
            "class MyHighlighter(QSyntaxHighlighter):\n"
            "    def highlightBlock(self, text):\n"
            "        pass\n"
        )
        result = self.engine.refactor_source(source)
        self.assertIn("highlightBlock", result.refactored_source)
        self.assertNotIn("highlight_block", result.refactored_source)

    def test_paint_event_not_renamed(self):
        source = (
            "from PySide6.QtWidgets import QWidget\n"
            "class MyWidget(QWidget):\n"
            "    def paintEvent(self, event):\n"
            "        pass\n"
        )
        result = self.engine.refactor_source(source)
        self.assertIn("paintEvent", result.refactored_source)
        self.assertNotIn("paint_event", result.refactored_source)

    def test_regular_camel_case_is_renamed(self):
        source = "def myFunction():\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertIn("my_function", result.refactored_source)
        self.assertNotIn("myFunction", result.refactored_source)

    def test_type_stubs_injected_into_class_methods(self):
        source = (
            "class MyClass:\n"
            "    def my_method(self, arg1, arg2):\n"
            "        pass\n"
        )
        engine = RefactorEngine(inject_type_stubs=True)
        result = engine.refactor_source(source)
        # Unannotated class method should now receive Any stubs
        self.assertIn("typing.Any", result.refactored_source)

    def test_type_stubs_skip_framework_overrides(self):
        source = (
            "class MyWidget:\n"
            "    def paintEvent(self, event):\n"
            "        pass\n"
        )
        engine = RefactorEngine(inject_type_stubs=True)
        result = engine.refactor_source(source)
        # Framework override should NOT receive Any stubs
        tree = ast.parse(result.refactored_source)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == "paintEvent":
                args = [a for a in node.args.args if a.arg != "self"]
                for arg in args:
                    self.assertIsNone(
                        arg.annotation,
                        f"Framework method 'paintEvent' arg '{arg.arg}' "
                        f"should not have type stubs injected"
                    )


if __name__ == "__main__":
    unittest.main()

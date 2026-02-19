"""Tests for naming convention enforcement in RefactorEngine."""

import unittest
from refactor_engine import RefactorEngine


class TestNamingConventions(unittest.TestCase):
    """Verify naming fixes preserve valid names and convert invalid ones."""

    def setUp(self):
        self.engine = RefactorEngine()

    def test_pascal_case_class_preserved(self):
        """Already-PascalCase class names must NOT be renamed."""
        source = "class AnimatedToggleWidget:\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("AnimatedToggleWidget", result.refactored_source)
        self.assertNotIn("Animatedtogglewidget", result.refactored_source)

    def test_multi_word_pascal_preserved(self):
        """Multi-word PascalCase names like LLMSummarizer are preserved."""
        source = "class LLMSummarizer:\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("LLMSummarizer", result.refactored_source)

    def test_snake_case_class_converted(self):
        """Genuinely snake_case class names ARE converted to PascalCase."""
        source = "class my_widget:\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("MyWidget", result.refactored_source)

    def test_qt_override_not_renamed(self):
        """Qt virtual method overrides must NOT be renamed to snake_case."""
        source = (
            "class MyWidget:\n"
            "    def paintEvent(self, event):\n"
            "        pass\n"
            "    def resizeEvent(self, event):\n"
            "        pass\n"
            "    def sizeHint(self):\n"
            "        pass\n"
        )
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("paintEvent", result.refactored_source)
        self.assertIn("resizeEvent", result.refactored_source)
        self.assertIn("sizeHint", result.refactored_source)

    def test_visit_methods_not_renamed(self):
        """AST visitor methods like visit_Name must NOT be renamed."""
        source = (
            "class MyVisitor:\n"
            "    def visit_Name(self, node):\n"
            "        pass\n"
            "    def visit_FunctionDef(self, node):\n"
            "        pass\n"
        )
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("visit_Name", result.refactored_source)
        self.assertIn("visit_FunctionDef", result.refactored_source)

    def test_camel_case_function_renamed(self):
        """Genuinely camelCase functions ARE renamed to snake_case."""
        source = "def myFunction():\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("my_function", result.refactored_source)

    def test_attribute_references_updated(self):
        """When a class is renamed, its attribute references update too."""
        source = (
            "class my_helper:\n"
            "    pass\n\n"
            "def use_it():\n"
            "    x = my_helper()\n"
        )
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("MyHelper", result.refactored_source)
        # The Name reference should also be updated
        self.assertNotIn("my_helper", result.refactored_source)


if __name__ == "__main__":
    unittest.main()

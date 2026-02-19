"""Tests for the large string modularizer in refactor_engine."""

import unittest
import ast
import textwrap
from refactor_engine import RefactorEngine, LargeStringModularizer

class TestLargeStringModularizer(unittest.TestCase):
    def setUp(self):
        self.engine = RefactorEngine()

    def test_static_string_extraction(self):
        source = """
def static_string_fn():
    content = \"\"\"
    This is a long static string.
    It has multiple lines.
    Line 3.
    Line 4.
    Line 5.
    \"\"\"
    return content
"""
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("def _get_content", result.refactored_source)
        self.assertIn("content = _get_content", result.refactored_source)

    def test_f_string_extraction_with_dependencies(self):
        source = """
def f_string_fn(user, items):
    summary = f\"\"\"
    User: {user.name}
    Items: {len(items)}
    Welcome to the system.
    This is a long multiline string designed to trigger the refactoring logic.
    It needs to be at least 4 lines long.
    \"\"\"
    return summary
"""
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        
        # Check for helper function definition
        self.assertIn("def _get_summary_content", result.refactored_source)
        # Check arguments (user, items) - sorted alphabetically
        self.assertIn("def _get_summary_content(items, user):", result.refactored_source)
        
        # Check for call replacement
        self.assertIn("summary = _get_summary_content", result.refactored_source)

    def test_return_statement_extraction(self):
        source = """
def return_fn():
    return \"\"\"
    This is a long string being returned directly.
    It has multiple lines.
    Line 3.
    Line 4.
    Line 5.
    Line 6.
    Line 7.
    Line 8.
    \"\"\"
"""
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("def _get_return_", result.refactored_source)
        self.assertIn("return _get_return_", result.refactored_source)

    def test_no_refactor_on_small_string(self):
        source = """
def small_string_fn():
    s = "Small string"
    return s
"""
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("_get_", result.refactored_source)
        # ast.unparse uses single quotes usually
        self.assertTrue("s = 'Small string'" in result.refactored_source or 's = "Small string"' in result.refactored_source)

    def test_duplicate_string_deduplication(self):
        """Same string in assignment and return produces only one helper."""
        # Use a long single-line string literal to avoid indentation issues
        long_str = "'" + "A" * 300 + "'"
        source = textwrap.dedent(f'''
            def build():
                s = {long_str}
                return {long_str}
        ''')
        tree = ast.parse(source)
        mod = LargeStringModularizer(min_length=100, min_lines=1)
        tree = mod.visit(tree)
        # Only one helper should be generated despite two extraction sites
        self.assertEqual(len(mod.new_functions), 1)

if __name__ == '__main__':
    unittest.main()

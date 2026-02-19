"""Tests for docstring generation quality."""

import unittest
from refactor_engine import RefactorEngine


class TestDocstringQuality(unittest.TestCase):
    """Verify generated docstrings use context-aware descriptions."""

    def setUp(self):
        self.engine = RefactorEngine()

    def test_no_generic_description_of(self):
        """Generated docstrings must NOT contain 'Description of ...'."""
        source = "def process(file_path, data, callback):\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("Description of", result.refactored_source)

    def test_context_aware_param_descriptions(self):
        """Known param names should get specific descriptions."""
        source = "def load(file_path, encoding):\n    pass\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("Path to the target file", result.refactored_source)
        self.assertIn("Character encoding", result.refactored_source)

    def test_no_generic_return_description(self):
        """Return docs should NOT say 'Description of return value'."""
        source = "def compute(x):\n    return x * 2\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("Description of return value", result.refactored_source)


if __name__ == "__main__":
    unittest.main()

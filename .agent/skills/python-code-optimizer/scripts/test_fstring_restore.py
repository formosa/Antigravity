"""Tests for f-string restoration in RefactorEngine."""

import unittest
from refactor_engine import RefactorEngine


class TestFstringRestore(unittest.TestCase):
    """Verify _restore_fstring_formatting behavior."""

    def setUp(self):
        self.engine = RefactorEngine(
            string_restore_min_newlines=2,
            string_restore_min_length=50
        )

    def test_collapsed_fstring_restored(self):
        """Collapsed f-string exceeding thresholds is restored to multiline."""
        source = "x = f'line1\\nline2\\nline3\\nline4\\nline5\\nline6\\nline7\\nline8\\nline9\\nline10'\n"
        restored, changes = self.engine._restore_fstring_formatting(source)
        self.assertIn('f"""', restored)
        self.assertNotIn('\\n', restored.split('f"""')[1].split('"""')[0])
        self.assertEqual(len(changes), 1)

    def test_short_fstring_unchanged(self):
        """Short f-string below thresholds is not touched."""
        source = "x = f'hello {name}'\n"
        restored, changes = self.engine._restore_fstring_formatting(source)
        self.assertEqual(restored, source)
        self.assertEqual(len(changes), 0)

    def test_expressions_preserved(self):
        """F-string expressions like {var} are preserved after restoration."""
        source = "x = f'{a}\\n{b}\\n{c}\\n{d}\\n{e}\\nend of a long long long long long string'\n"
        restored, changes = self.engine._restore_fstring_formatting(source)
        self.assertIn('{a}', restored)
        self.assertIn('{b}', restored)
        self.assertIn('{e}', restored)

    def test_syntax_error_fallback(self):
        """If restoration would break syntax, original is returned."""
        # Triple quotes inside content would break f\"""...\"""
        source = 'x = f\'has \\"\\"\\"\\" inside\\nline2\\nline3\\nline4\\nline5\\nsome more long content here\'\n'
        restored, changes = self.engine._restore_fstring_formatting(source)
        # Should either return original or a valid result
        try:
            compile(restored, '<test>', 'exec')
        except SyntaxError:
            self.fail("Restoration produced invalid syntax")


if __name__ == "__main__":
    unittest.main()

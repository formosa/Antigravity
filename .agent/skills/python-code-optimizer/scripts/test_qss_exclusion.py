"""Tests for QSS template string exclusion from modularization."""

import unittest
from refactor_engine import RefactorEngine


class TestQSSExclusion(unittest.TestCase):
    """Verify QSS/CSS template strings are NOT extracted into helpers."""

    def setUp(self):
        self.engine = RefactorEngine()

    def test_qss_fstring_not_extracted(self):
        """Large QSS f-string must NOT be split into a helper function."""
        source = '''
def build_style(t):
    return f"""
        QWidget {{
            background-color: {t.bg};
            color: {t.fg};
            font-family: {t.font};
            font-size: 13px;
            border-radius: 4px;
            padding: 8px;
        }}
        QPushButton {{
            background-color: {t.btn_bg};
            border: 1px solid {t.border};
        }}
    """
'''
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("_get_", result.refactored_source)

    def test_qss_static_string_not_extracted(self):
        """Large QSS static string must NOT be extracted."""
        source = '''
def build_style():
    qss = """
        QWidget {
            background-color: #1a1a2e;
            color: #eee;
            font-family: monospace;
            font-size: 14px;
            padding: 4px 8px;
        }
        QPushButton {
            background-color: #0f3460;
            border-radius: 4px;
        }
    """
    return qss
'''
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("_get_", result.refactored_source)

    def test_non_qss_string_still_extracted(self):
        """Large non-QSS strings should still be extracted normally."""
        lines = "\\n".join(f"    Line {i}" for i in range(20))
        source = f'''
def build_content():
    content = """{lines}"""
    return content
'''
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("_get_content", result.refactored_source)


if __name__ == "__main__":
    unittest.main()

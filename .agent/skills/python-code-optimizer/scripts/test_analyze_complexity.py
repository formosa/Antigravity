"""Tests for the complexity analyzer."""

import os
import tempfile
import unittest

from analyze_complexity import ComplexityAnalyzer


class TestComplexityAnalyzer(unittest.TestCase):
    """Verify complexity metrics for representative code patterns."""

    def setUp(self):
        self.analyzer = ComplexityAnalyzer()

    def _write_temp(self, source: str) -> str:
        fd, path = tempfile.mkstemp(suffix=".py")
        with os.fdopen(fd, "w") as f:
            f.write(source)
        return path

    def test_linear_function_complexity_one(self):
        path = self._write_temp("def linear():\n    return 1\n")
        try:
            report = self.analyzer.analyze(path)
            self.assertEqual(len(report.functions), 1)
            self.assertEqual(report.functions[0].cyclomatic_complexity, 1)
        finally:
            os.unlink(path)

    def test_branching_increases_complexity(self):
        source = "def branch(x):\n    if x > 0:\n        return x\n    return -x\n"
        path = self._write_temp(source)
        try:
            report = self.analyzer.analyze(path)
            self.assertGreaterEqual(report.functions[0].cyclomatic_complexity, 2)
        finally:
            os.unlink(path)

    def test_maintainability_index_range(self):
        path = self._write_temp("def simple():\n    x = 1\n    return x\n")
        try:
            report = self.analyzer.analyze(path)
            self.assertGreaterEqual(report.maintainability_index, 0.0)
            self.assertLessEqual(report.maintainability_index, 100.0)
        finally:
            os.unlink(path)


if __name__ == "__main__":
    unittest.main()

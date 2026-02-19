"""Tests for the structural entropy analyzer."""

import ast
import unittest

from analyze_entropy import compute_entropy, compute_entropy_from_source


class TestEntropyAnalysis(unittest.TestCase):
    """Verify entropy scoring across representative code patterns."""

    def test_simple_function_low_entropy(self):
        source = "def add(a, b):\n    return a + b\n"
        metrics = compute_entropy_from_source(source)
        self.assertLessEqual(metrics.normalized_score, 0.4)
        self.assertFalse(metrics.is_high_entropy())

    def test_deeply_nested_high_entropy(self):
        # Create a function with extreme nesting and complexity to exceed 0.4 threshold
        parts = []
        parts.append("def monster():")
        indent = "    "
        # Nest 12 levels deep (exceeds MAX_ALLOWED_NESTING_DEPTH=10)
        for i in range(12):
            parts.append(f"{indent * (i+1)}if True:")
            parts.append(f"{indent * (i+2)}print({i})")
        
        # Add branching complexity (approx 20 branches)
        for i in range(20):
             parts.append(f"{indent * 12}if x == {i}: pass")
             
        source = "\n".join(parts)
        
        metrics = compute_entropy_from_source(source)
        # With max nesting (factor=1.0 * 0.25) and high branch density/count
        # It should comfortably exceed 0.4
        self.assertGreater(metrics.normalized_score, 0.4)
        self.assertTrue(metrics.is_high_entropy())

    def test_score_bounds(self):
        source = "x = 1\n"
        metrics = compute_entropy_from_source(source)
        self.assertGreaterEqual(metrics.normalized_score, 0.0)
        self.assertLessEqual(metrics.normalized_score, 1.0)

    def test_threshold_parameter(self):
        source = "def f():\n    if True:\n        pass\n"
        metrics = compute_entropy_from_source(source)
        # Should not be high entropy at lenient threshold
        self.assertFalse(metrics.is_high_entropy(threshold=0.9))


if __name__ == "__main__":
    unittest.main()

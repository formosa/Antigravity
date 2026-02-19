"""Tests for the validation suite."""

import os
import tempfile
import unittest

from validation_suite import ValidationSuite


class TestValidationSuite(unittest.TestCase):
    """Verify validation checks produce correct pass/fail results."""

    def setUp(self):
        self.suite = ValidationSuite()

    def _write_temp(self, source: str) -> str:
        fd, path = tempfile.mkstemp(suffix=".py")
        with os.fdopen(fd, "w") as f:
            f.write(source)
        return path

    def test_syntax_check_passes_valid_code(self):
        check = self.suite._check_syntax("x = 1\n", "test.py")
        self.assertTrue(check.passed)

    def test_syntax_check_fails_invalid_code(self):
        check = self.suite._check_syntax("def :\n", "test.py")
        self.assertFalse(check.passed)

    def test_clean_names_detects_single_letter(self):
        source = "def fn():\n    a = 1\n    b = 2\n"
        check = self.suite._check_clean_names(source)
        # 'a' and 'b' are not in the allowed set
        self.assertFalse(check.passed)

    def test_clean_names_allows_loop_vars(self):
        source = "for i in range(10):\n    pass\n"
        check = self.suite._check_clean_names(source)
        self.assertTrue(check.passed)

    def test_clean_functions_detects_excess_args(self):
        source = "def fn(a, b, c, d, e, f):\n    pass\n"
        check = self.suite._check_clean_functions(source)
        self.assertFalse(check.passed)

    def test_clean_functions_passes_within_limit(self):
        source = "def fn(a, b, c):\n    pass\n"
        check = self.suite._check_clean_functions(source)
        self.assertTrue(check.passed)

    def test_security_detects_eval(self):
        source = "result = eval('1 + 1')\n"
        check = self.suite._check_security(source)
        self.assertFalse(check.passed)

    def test_security_detects_wildcard_import(self):
        source = "from os import *\n"
        check = self.suite._check_security(source)
        self.assertFalse(check.passed)

    def test_magic_numbers_detects_bare_literal(self):
        # Exceeds the threshold of 30 allowed magic numbers
        nums = " + ".join(str(float(i)) for i in range(2, 35))
        source = f"def fn():\n    return {nums}\n"
        check = self.suite._check_magic_numbers(source)
        self.assertFalse(check.passed)

    def test_api_preservation_detects_removal(self):
        original = "def public_fn():\n    pass\n"
        optimized = "def other_fn():\n    pass\n"
        check = self.suite._check_api_preservation(original, optimized)
        self.assertFalse(check.passed)


if __name__ == "__main__":
    unittest.main()

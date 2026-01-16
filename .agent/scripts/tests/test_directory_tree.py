#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Unit tests for directory_tree.py."""

import tempfile
import unittest
from contextlib import contextmanager
from pathlib import Path
from typing import Dict, Union

import importlib.util
import sys

# Import from hyphenated module name
_spec = importlib.util.spec_from_file_location(
    "directory_tree",
    Path(__file__).parent / "directory_tree.py"
)
_module = importlib.util.module_from_spec(_spec)
sys.modules["directory_tree"] = _module
_spec.loader.exec_module(_module)

generate_dir_tree = _module.generate_dir_tree
_compile_regex_pattern = _module._compile_regex_pattern
_format_size_human_readable = _module._format_size_human_readable
TreeStyle = _module.TreeStyle


@contextmanager
def create_test_tree(structure: Dict[str, Union[dict, str, None]]):
    """Create temporary filesystem tree. Keys=paths, values=dict|str|None."""
    def _create(base: Path, struct: dict) -> None:
        for name, content in struct.items():
            path = base / name
            if isinstance(content, dict):
                path.mkdir(parents=True, exist_ok=True)
                _create(path, content)
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content or "", encoding="utf-8")

    with tempfile.TemporaryDirectory() as tmpdir:
        root = Path(tmpdir)
        _create(root, structure)
        yield root


class TestCompileRegexPattern(unittest.TestCase):
    def test_none_returns_match_nothing(self):
        pattern = _compile_regex_pattern(None)
        self.assertEqual(pattern.pattern, "(?!)")

    def test_invalid_regex_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            _compile_regex_pattern("[invalid")
        self.assertIn("Invalid regex pattern", str(ctx.exception))

    def test_invalid_regex_in_list_raises_valueerror(self):
        with self.assertRaises(ValueError) as ctx:
            _compile_regex_pattern([r"\.py$", "[invalid"])
        self.assertIn("Invalid regex", str(ctx.exception))


class TestTreeStyle(unittest.TestCase):
    def test_utf8_has_box_chars(self):
        self.assertIn("├", TreeStyle.UTF8.value.middle)

    def test_ascii_has_ascii_chars(self):
        self.assertEqual(TreeStyle.ASCII.value.middle, "+-- ")


class TestGenerateDirTree(unittest.TestCase):
    def test_basic_generation(self):
        with create_test_tree({"folder": {"file.txt": "x"}}) as root:
            lines = generate_dir_tree(root)
            self.assertIn("folder", "\n".join(lines))

    def test_ascii_mode(self):
        with create_test_tree({"folder": {"file.txt": "x"}}) as root:
            lines = generate_dir_tree(root, use_ascii=True)
            self.assertNotIn("├", "\n".join(lines))


if __name__ == "__main__":
    unittest.main()

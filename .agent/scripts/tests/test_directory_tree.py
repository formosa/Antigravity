#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Unit tests for directory_tree.py.

role: unit test suite for directory tree generation logic
entrypoints: main
reads: directory_tree.py (via dynamic import)
writes: nothing (uses tempfile)
external_io: fs
state_model: stateless
failure_surface: none
coupling: highly coupled to directory_tree.py
determinism: deterministic
concurrency: thread-safe; process-local
"""

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
    Path(__file__).resolve().parents[1] / "directory_tree.py"
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
    """
    Create a temporary filesystem tree for testing.

    purpose: test fixture for filesystem structure simulation
    preconditions: structure keys are paths, values are dict|str|None
    postconditions: temporary directory created and populated
    mutates: filesystem
    reads: none
    writes: filesystem
    external_io: fs
    determinism: deterministic
    idempotency: no
    concurrency: not thread-safe (global tempfile)
    ordering: none
    aliasing: none
    security: none
    coupling: minimal

    Parameters
    ----------
    structure : Dict[str, Union[dict, str, None]]
        filesystem structure definition
    """
    def _create(base: Path, struct: dict) -> None:
        """
        Recursively create the directory structure.

        purpose: internal helper for tree creation
        """
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
    """
    Test suite for regex pattern compilation logic.

    role: logic validation
    lifecycle: instance-per-test
    mutability: immutable
    ownership: none
    concurrency: process-local
    cache_behavior: none
    serialization: non-serializable
    coupling: minimal
    failure_surface: minimal
    """
    def test_none_returns_match_nothing(self):
        """
        Verify that None input returns a pattern that matches nothing.

        purpose: boundary test
        """
        pattern = _compile_regex_pattern(None)
        self.assertEqual(pattern.pattern, "(?!)")

    def test_invalid_regex_raises_valueerror(self):
        """
        Verify that invalid regex strings raise ValueError.

        purpose: error handling test
        """
        with self.assertRaises(ValueError) as ctx:
            _compile_regex_pattern("[invalid")
        self.assertIn("Invalid regex pattern", str(ctx.exception))

    def test_invalid_regex_in_list_raises_valueerror(self):
        """
        Verify that invalid regex strings within a list raise ValueError.

        purpose: error handling test for list input
        """
        with self.assertRaises(ValueError) as ctx:
            _compile_regex_pattern([r"\.py$", "[invalid"])
        self.assertIn("Invalid regex", str(ctx.exception))


class TestTreeStyle(unittest.TestCase):
    """
    Test suite for TreeStyle enumeration properties.

    role: logic validation
    """
    def test_utf8_has_box_chars(self):
        """
        Verify that UTF8 style contains box-drawing characters.

        purpose: property test
        """
        self.assertIn("├", TreeStyle.UTF8.value.middle)

    def test_ascii_has_ascii_chars(self):
        """
        Verify that ASCII style uses standard ASCII characters.

        purpose: property test
        """
        self.assertEqual(TreeStyle.ASCII.value.middle, "+-- ")


class TestGenerateDirTree(unittest.TestCase):
    """
    Test suite for high-level directory tree generation.

    role: integration/logic validation
    """
    def test_basic_generation(self):
        """
        Verify basic tree string generation for a simple structure.

        purpose: functionality test
        """
        with create_test_tree({"folder": {"file.txt": "x"}}) as root:
            lines = generate_dir_tree(root)
            self.assertIn("folder", "\n".join(lines))

    def test_ascii_mode(self):
        """
        Verify that ASCII mode avoids UTF-8 box characters.

        purpose: functionality test
        """
        with create_test_tree({"folder": {"file.txt": "x"}}) as root:
            lines = generate_dir_tree(root, use_ascii=True)
            self.assertNotIn("├", "\n".join(lines))


if __name__ == "__main__":
    unittest.main()

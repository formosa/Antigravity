"""Tests for type stub injection scoping."""

import unittest
from refactor_engine import RefactorEngine


class TestTypeStubInjection(unittest.TestCase):
    """Verify type stubs are only injected where appropriate."""

    def setUp(self):
        self.engine = RefactorEngine(inject_type_stubs=True)

    def test_class_methods_are_stubbed(self):
        """Methods inside classes should now get Any stubs."""
        source = (
            "class Foo:\n"
            "    def bar(self, x):\n"
            "        return x\n"
        )
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("typing.Any", result.refactored_source)

    def test_partially_annotated_preserved(self):
        """Functions with some annotations should NOT get extra Any stubs."""
        source = "def fn(x: int, y):\n    return x + y\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("typing.Any", result.refactored_source)

    def test_fully_unannotated_toplevel_stubbed(self):
        """Top-level functions with no annotations DO get stubs."""
        source = "def fn(x, y):\n    return x + y\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertIn("typing.Any", result.refactored_source)

    def test_self_and_cls_excluded(self):
        """self and cls params never get stubs even in top-level functions."""
        source = "def fn(self, x):\n    return x\n"
        result = self.engine.refactor_source(source)
        self.assertTrue(result.success)
        src = result.refactored_source
        # 'self' should not have annotation
        self.assertNotIn("self: typing.Any", src)

    def test_stubs_disabled(self):
        """When inject_type_stubs=False, no stubs are added."""
        engine = RefactorEngine(inject_type_stubs=False)
        source = "def fn(x, y):\n    return x + y\n"
        result = engine.refactor_source(source)
        self.assertTrue(result.success)
        self.assertNotIn("typing.Any", result.refactored_source)


if __name__ == "__main__":
    unittest.main()

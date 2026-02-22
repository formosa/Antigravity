"""
Package initialization files for block_atomic_validator.
Each subdirectory needs an __init__.py file.
"""

# ============================================================
# FILE: src/block_atomic_validator/__init__.py
# ============================================================
"""
Block-Atomic Validator for DDR System.

Validates block-atomic tag hierarchy in DDR documentation.
"""

__version__ = "1.0.0"
__author__ = "DDR System Team"

from .core.validator import BlockAtomicValidator
from .core.models import (
    Tag,
    Violation,
    ViolationType,
    ValidationResult,
    ValidationContext,
)
from .core.parser import RSTParser

__all__ = [
    "BlockAtomicValidator",
    "Tag",
    "Violation",
    "ViolationType",
    "ValidationResult",
    "ValidationContext",
    "RSTParser",
]


# ============================================================
# FILE: src/block_atomic_validator/core/__init__.py
# ============================================================
"""Core validation engine components."""

from .validator import BlockAtomicValidator
from .models import (
    Tag,
    Violation,
    ViolationType,
    ValidationResult,
    ValidationContext,
)
from .parser import RSTParser

__all__ = [
    "BlockAtomicValidator",
    "Tag",
    "Violation",
    "ViolationType",
    "ValidationResult",
    "ValidationContext",
    "RSTParser",
]


# ============================================================
# FILE: src/block_atomic_validator/rules/__init__.py
# ============================================================
"""Validation rule implementations."""

from .ordering_rule import OrderingRule
from .citation_rule import CitationRule
from .consistency_rule import ConsistencyRule

__all__ = [
    "OrderingRule",
    "CitationRule",
    "ConsistencyRule",
]


# ============================================================
# FILE: src/block_atomic_validator/reporters/__init__.py
# ============================================================
"""Output reporters and formatters."""

from .ide_reporter import IDEReporter

__all__ = [
    "IDEReporter",
]


# ============================================================
# FILE: src/block_atomic_validator/utils/__init__.py
# ============================================================
"""Utility functions and helpers."""

__all__ = []


# ============================================================
# FILE: tests/__init__.py
# ============================================================
"""Test suite for block_atomic_validator."""

# Empty - test discovery only


# ============================================================
# FILE: antigravity_hooks/__init__.py
# ============================================================
"""
Antigravity IDE integration hooks.

Provides entrypoints for IDE skill integration.
"""

from .skill_entrypoint import (
    initialize,
    validate,
    validate_on_save,
    validate_on_open,
    validate_project,
    get_fix_suggestions,
    get_skill_status,
)

__all__ = [
    "initialize",
    "validate",
    "validate_on_save",
    "validate_on_open",
    "validate_project",
    "get_fix_suggestions",
    "get_skill_status",
]

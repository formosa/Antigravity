"""
Data models for block-atomic validation.

Implements: DDR tag structure representation
Requirements: tag_syntax.md, tag_immutability.md
"""

from dataclasses import dataclass, field
from typing import List, Optional, Set
from pathlib import Path
from enum import Enum
import re


class ViolationType(Enum):
    """
    Types of block-atomic validation violations.

    Attributes
    ----------
    ORDERING_VIOLATION : str
        Block tag appears after atomic child.
    MISSING_BLOCK_CITATION : str
        Atomic tag does not cite parent block.
    ORPHANED_ATOMIC : str
        Atomic tag has no corresponding block.
    PREFIX_MISMATCH : str
        Block/atomic prefix inconsistency.
    """
    ORDERING_VIOLATION = "ordering_violation"
    MISSING_BLOCK_CITATION = "missing_block_citation"
    ORPHANED_ATOMIC = "orphaned_atomic"
    PREFIX_MISMATCH = "prefix_mismatch"


@dataclass
class Tag:
    """
    Represents a DDR tag from RST directive.

    Ref: |patterns/tag_syntax.md|

    Attributes
    ----------
    tag_id : str
        Full tag identifier (e.g., "BRD-5.2").
    tier : str
        Tier prefix (BRD, NFR, FSD, SAD, ICD, TDD, ISP).
    block_number : int
        Block sequence number (N in TIER-N).
    atomic_number : Optional[int]
        Atomic sequence number (M in TIER-N.M).
    line_number : int
        Line number in source file.
    title : str
        Tag title/description.
    links : List[str]
        Parent tag citations from :links: directive.
    content : str
        Tag content text.
    """
    tag_id: str
    tier: str
    block_number: int
    atomic_number: Optional[int]
    line_number: int
    title: str
    links: List[str] = field(default_factory=list)
    content: str = ""

    @property
    def is_atomic(self) -> bool:
        """Check if tag is atomic-level (TIER-N.M)."""
        return self.atomic_number is not None

    @property
    def is_block(self) -> bool:
        """Check if tag is block-level (TIER-N)."""
        return self.atomic_number is None

    def get_block_id(self) -> str:
        """
        Get corresponding block ID for this tag.

        Returns
        -------
        str
            Block ID (TIER-N format).
        """
        return f"{self.tier}-{self.block_number}"

    def validates_block_citation(self) -> bool:
        """
        Check if atomic tag cites its block parent.

        Returns
        -------
        bool
            True if atomic cites block, or if tag is block-level.
        """
        if self.is_block:
            return True  # Blocks don't need to cite themselves

        expected_block_id = self.get_block_id()
        return expected_block_id in self.links

    @staticmethod
    def parse_tag_id(tag_id: str) -> dict:
        """
        Parse tag ID into components.

        Parameters
        ----------
        tag_id : str
            Tag ID in format TIER-N or TIER-N.M.

        Returns
        -------
        dict
            Dict with keys: tier, block_number, atomic_number.

        Raises
        ------
        ValueError
            If tag_id format is invalid.
        """
        # Pattern: TIER-N or TIER-N.M
        pattern = r'^([A-Z]{3})-(\d+)(?:\.(\d+))?$'
        match = re.match(pattern, tag_id)

        if not match:
            raise ValueError(f"Invalid tag ID format: {tag_id}")

        tier, block, atomic = match.groups()

        return {
            'tier': tier,
            'block_number': int(block),
            'atomic_number': int(atomic) if atomic else None
        }


@dataclass
class Violation:
    """
    Represents a validation rule violation.

    Attributes
    ----------
    type : ViolationType
        Category of violation.
    severity : str
        Severity level (error, warning).
    message : str
        Human-readable description.
    tag_id : str
        Tag where violation occurred.
    line_number : int
        Line number in source file.
    related_tag_id : Optional[str]
        Related tag (e.g., expected block parent).
    fix_suggestion : Optional[str]
        Suggested fix for violation.
    """
    type: ViolationType
    severity: str
    message: str
    tag_id: str
    line_number: int
    related_tag_id: Optional[str] = None
    fix_suggestion: Optional[str] = None

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'type': self.type.value,
            'severity': self.severity,
            'message': self.message,
            'tag_id': self.tag_id,
            'line_number': self.line_number,
            'related_tag_id': self.related_tag_id,
            'fix_suggestion': self.fix_suggestion
        }


@dataclass
class ValidationResult:
    """
    Result of validation operation.

    Attributes
    ----------
    file_path : Path
        Path to validated file.
    tier : str
        DDR tier of file.
    total_tags : int
        Total tags in file.
    violations : List[Violation]
        List of detected violations.
    is_valid : bool
        True if no violations found.
    """
    file_path: Path
    tier: str
    total_tags: int
    violations: List[Violation]
    is_valid: bool

    @property
    def error_count(self) -> int:
        """Count of error-level violations."""
        return sum(1 for v in self.violations if v.severity == "error")

    @property
    def warning_count(self) -> int:
        """Count of warning-level violations."""
        return sum(1 for v in self.violations if v.severity == "warning")

    def to_dict(self) -> dict:
        """Convert to dictionary for JSON serialization."""
        return {
            'file_path': str(self.file_path),
            'tier': self.tier,
            'total_tags': self.total_tags,
            'is_valid': self.is_valid,
            'error_count': self.error_count,
            'warning_count': self.warning_count,
            'violations': [v.to_dict() for v in self.violations]
        }

    def __str__(self) -> str:
        """Human-readable summary."""
        status = "✅ VALID" if self.is_valid else "❌ INVALID"
        return (
            f"{status} | {self.file_path.name} | "
            f"Tier: {self.tier} | Tags: {self.total_tags} | "
            f"Errors: {self.error_count} | Warnings: {self.warning_count}"
        )

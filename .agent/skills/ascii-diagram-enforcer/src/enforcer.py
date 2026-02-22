"""
ASCII Diagram Enforcer - Core Validation Engine

This module implements the primary validation logic for enforcing mandatory ASCII
topology diagrams in SAD-tier (System Architecture Document) sections of the DDR
System.

Implements: DDR constraint enforcement for SAD tier diagram requirements
Requirements: |tier-sad.md|, |patterns/knowledge-source-template.md|

Author: DDR System Integration Team
Version: 1.0.0
"""

import re
from typing import List, Dict, Tuple, Optional, Set
from dataclasses import dataclass, field
from enum import Enum

from .diagram_detector import DiagramDetector
from .sad_parser import SADParser
from .validators import DiagramValidator


class ViolationSeverity(Enum):
    """Violation severity levels aligned with DDR reconciliation system."""
    ERROR = "ERROR"
    WARNING = "WARNING"
    INFO = "INFO"


@dataclass
class Violation:
    """
    Represents a single validation violation.

    Attributes
    ----------
    rule_id : str
        Unique identifier for violated rule (e.g., 'SAD-DIAGRAM-001').
    severity : ViolationSeverity
        Severity level of violation.
    target_tag : str
        SAD tag ID where violation occurred.
    line_number : int
        Line number in document where violation detected.
    description : str
        Human-readable violation description.
    suggested_fix : Optional[str]
        Recommended remediation action.
    """
    rule_id: str
    severity: ViolationSeverity
    target_tag: str
    line_number: int
    description: str
    suggested_fix: Optional[str] = None


@dataclass
class ValidationResult:
    """
    Container for complete validation results.

    Attributes
    ----------
    section_id : str
        Unique identifier for validated section.
    is_valid : bool
        Overall validation status.
    violations : List[Violation]
        Collection of detected violations.
    sad_tags_found : int
        Total SAD tags in section.
    diagrams_found : int
        Total ASCII diagrams detected.
    missing_diagrams : Set[str]
        Tag IDs missing required diagrams.
    """
    section_id: str
    is_valid: bool
    violations: List[Violation] = field(default_factory=list)
    sad_tags_found: int = 0
    diagrams_found: int = 0
    missing_diagrams: Set[str] = field(default_factory=set)

    def to_reconciliation_item(self) -> Dict:
        """
        Convert violation to DDR reconciliation pending_item format.

        Returns
        -------
        dict
            Reconciliation-compatible pending item object.
        """
        if not self.violations:
            return {}

        return {
            "target_tag": list(self.missing_diagrams)[0] if self.missing_diagrams else "SAD-section",
            "source_trigger": "ascii_diagram_enforcer validation",
            "issue_type": "CONSTRAINT_VIOLATION",
            "description": f"Missing or invalid ASCII diagrams: {len(self.violations)} violation(s)"
        }


class ASCIIDiagramEnforcer:
    """
    Primary enforcement engine for SAD-tier ASCII diagram requirements.

    This enforcer validates that every SAD block-level tag includes a properly
    formatted ASCII topology diagram illustrating architectural patterns, as
    mandated by the DDR System specification.

    Parameters
    ----------
    strict_mode : bool, default=True
        If True, treat all violations as blocking errors.
    min_diagram_lines : int, default=3
        Minimum lines required for valid ASCII diagram.
    auto_flag_dirty : bool, default=True
        Automatically update reconciliation manifest DIRTY flag on violations.

    Attributes
    ----------
    detector : DiagramDetector
        ASCII pattern detection engine.
    parser : SADParser
        RST directive parser for SAD sections.
    validator : DiagramValidator
        Diagram quality validation logic.

    Notes
    -----
    Integrates with DDR reconciliation system via `to_reconciliation_item()`.
    Supports real-time validation in Antigravity IDE via hooks.
    """

    def __init__(
        self,
        strict_mode: bool = True,
        min_diagram_lines: int = 3,
        auto_flag_dirty: bool = True
    ):
        """
        Initialize enforcer with configuration parameters.

        Implements: Core enforcer initialization
        Requirements: |skill.yaml| configuration
        """
        self.strict_mode = strict_mode
        self.min_diagram_lines = min_diagram_lines
        self.auto_flag_dirty = auto_flag_dirty

        # Initialize sub-components
        self.detector = DiagramDetector(min_lines=min_diagram_lines)
        self.parser = SADParser()
        self.validator = DiagramValidator()

        # Violation tracking
        self.violations: List[Violation] = []

    def validate_section(self, content: str, section_id: str) -> ValidationResult:
        """
        Validate complete SAD section for diagram compliance.

        Primary validation workflow:
        1. Parse SAD tags from RST content
        2. Detect ASCII diagrams in content
        3. Match diagrams to SAD block tags
        4. Validate diagram quality
        5. Generate violation report

        Parameters
        ----------
        content : str
            Raw RST content of SAD section.
        section_id : str
            Unique identifier for section (e.g., 'sad-root').

        Returns
        -------
        ValidationResult
            Complete validation results with violations.

        Examples
        --------
        >>> enforcer = ASCIIDiagramEnforcer()
        >>> content = read_file('docs/04_sad/architecture.rst')
        >>> result = enforcer.validate_section(content, 'sad-root')
        >>> if not result.is_valid:
        ...     print(f"Found {len(result.violations)} violations")

        Notes
        -----
        Block-level SAD tags (SAD-N) require diagrams; atomic tags (SAD-N.M) inherit
        from parent block and do not require separate diagrams.
        """
        result = ValidationResult(section_id=section_id, is_valid=True)

        # Step 1: Parse SAD tags
        sad_tags = self.parser.extract_sad_tags(content)
        result.sad_tags_found = len(sad_tags)

        # Step 2: Detect ASCII diagrams
        diagrams = self.detector.find_diagrams(content)
        result.diagrams_found = len(diagrams)

        # Step 3: Extract block-level tags (require diagrams)
        block_tags = self._filter_block_tags(sad_tags)

        # Step 4: Match diagrams to block tags
        tag_diagram_map = self._associate_diagrams_to_tags(block_tags, diagrams, content)

        # Step 5: Validate each block tag
        for tag in block_tags:
            tag_id = tag['id']

            # Rule SAD-DIAGRAM-001: Every block tag must have diagram
            if tag_id not in tag_diagram_map:
                violation = Violation(
                    rule_id="SAD-DIAGRAM-001",
                    severity=ViolationSeverity.ERROR,
                    target_tag=tag_id,
                    line_number=tag['line_number'],
                    description=f"Block-level SAD tag '{tag_id}' missing mandatory ASCII diagram",
                    suggested_fix="Insert ASCII topology diagram illustrating architectural pattern"
                )
                result.violations.append(violation)
                result.missing_diagrams.add(tag_id)
                continue

            # Rule SAD-DIAGRAM-002/003/004: Validate diagram quality
            diagram = tag_diagram_map[tag_id]
            quality_violations = self.validator.validate_diagram(
                diagram,
                tag_id,
                tag['line_number']
            )
            result.violations.extend(quality_violations)

        # Determine overall validity
        result.is_valid = not any(
            v.severity == ViolationSeverity.ERROR for v in result.violations
        )

        return result

    def _filter_block_tags(self, tags: List[Dict]) -> List[Dict]:
        """
        Extract block-level SAD tags (SAD-N format, not SAD-N.M).

        Parameters
        ----------
        tags : List[Dict]
            All parsed SAD tags.

        Returns
        -------
        List[Dict]
            Only block-level tags requiring diagrams.
        """
        block_pattern = re.compile(r'^SAD-\d+$')
        return [tag for tag in tags if block_pattern.match(tag['id'])]

    def _associate_diagrams_to_tags(
        self,
        block_tags: List[Dict],
        diagrams: List[Dict],
        content: str
    ) -> Dict[str, Dict]:
        """
        Match detected diagrams to their corresponding block tags.

        Strategy: Associate diagram with nearest preceding block tag.

        Parameters
        ----------
        block_tags : List[Dict]
            Block-level SAD tags.
        diagrams : List[Dict]
            Detected ASCII diagrams.
        content : str
            Original content for line number validation.

        Returns
        -------
        Dict[str, Dict]
            Mapping of tag_id -> diagram object.
        """
        tag_diagram_map = {}

        for tag in block_tags:
            tag_line = tag['line_number']

            # Find diagram appearing after this tag but before next tag
            next_tag_line = self._find_next_tag_line(block_tags, tag)

            for diagram in diagrams:
                diagram_line = diagram['start_line']

                # Diagram must appear between this tag and next tag
                if tag_line < diagram_line < next_tag_line:
                    tag_diagram_map[tag['id']] = diagram
                    break

        return tag_diagram_map

    def _find_next_tag_line(self, tags: List[Dict], current_tag: Dict) -> int:
        """
        Determine line number of next block tag after current tag.

        Parameters
        ----------
        tags : List[Dict]
            All block tags.
        current_tag : Dict
            Current tag to find successor for.

        Returns
        -------
        int
            Line number of next tag, or infinity if last tag.
        """
        current_line = current_tag['line_number']
        next_lines = [t['line_number'] for t in tags if t['line_number'] > current_line]
        return min(next_lines) if next_lines else float('inf')

    def generate_report(self, result: ValidationResult) -> str:
        """
        Generate human-readable validation report.

        Parameters
        ----------
        result : ValidationResult
            Validation results to format.

        Returns
        -------
        str
            Formatted report text.
        """
        report_lines = [
            "=" * 70,
            "ASCII Diagram Enforcer - Validation Report",
            "=" * 70,
            f"Section ID: {result.section_id}",
            f"Status: {'VALID' if result.is_valid else 'INVALID'}",
            f"SAD Tags Found: {result.sad_tags_found}",
            f"Diagrams Found: {result.diagrams_found}",
            f"Violations: {len(result.violations)}",
            ""
        ]

        if result.violations:
            report_lines.append("VIOLATIONS:")
            report_lines.append("-" * 70)

            for v in result.violations:
                report_lines.extend([
                    f"[{v.severity.value}] {v.rule_id}",
                    f"  Tag: {v.target_tag} (Line {v.line_number})",
                    f"  Issue: {v.description}",
                    f"  Fix: {v.suggested_fix or 'N/A'}",
                    ""
                ])
        else:
            report_lines.append("✓ No violations detected - All SAD sections compliant")

        report_lines.append("=" * 70)
        return "\n".join(report_lines)

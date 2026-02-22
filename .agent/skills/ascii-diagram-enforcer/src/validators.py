"""
Diagram Quality Validators

Validates ASCII diagram structural quality, ensuring diagrams meet DDR System
requirements for clarity, completeness, and architectural representation.

Implements: Diagram quality validation rules
Requirements: |tier-sad.md| diagram standards

Author: DDR System Integration Team
Version: 1.0.0
"""

import re
from typing import List, Dict, Set
from enum import Enum

from .enforcer import Violation, ViolationSeverity


class DiagramValidator:
    """
    ASCII diagram quality validation engine.

    Validates diagrams against DDR System quality standards:
    - Recognized box drawing characters
    - Component relationship clarity
    - Minimum structural complexity
    - Consistency in notation

    Attributes
    ----------
    RECOGNIZED_BOX_CHARS : Set[str]
        Standard box drawing characters accepted by DDR.
    MIN_COMPONENTS : int
        Minimum components for architectural diagram.
    MIN_CONNECTIONS : int
        Minimum connections for relationship clarity.

    Notes
    -----
    Validation rules correspond to skill.yaml rule definitions:
    - SAD-DIAGRAM-002: Recognized box characters
    - SAD-DIAGRAM-003: Component relationships
    - SAD-DIAGRAM-004: Minimum structural clarity
    """

    # Recognized box drawing characters (ASCII + Unicode box drawing)
    RECOGNIZED_BOX_CHARS = {
        # ASCII box characters
        '+', '-', '|', '/', '\\',
        # Unicode single line
        '┌', '┐', '└', '┘', '─', '│', '├', '┤', '┬', '┴', '┼',
        # Unicode double line
        '═', '║', '╔', '╗', '╚', '╝', '╠', '╣', '╦', '╩', '╬',
        # Unicode rounded
        '╭', '╮', '╯', '╰',
        # Arrows
        '<', '>', '^', 'v', '←', '→', '↑', '↓', '↔', '↕'
    }

    MIN_COMPONENTS = 2    # Minimum boxes/nodes for architecture
    MIN_CONNECTIONS = 1   # Minimum connections between components

    def __init__(self):
        """
        Initialize diagram validator.

        Implements: Validator initialization
        Requirements: DDR quality standards
        """
        pass

    def validate_diagram(
        self,
        diagram: Dict,
        tag_id: str,
        tag_line: int
    ) -> List[Violation]:
        """
        Validate diagram quality against all rules.

        Validation checks:
        1. Box character recognition (SAD-DIAGRAM-002)
        2. Component relationships (SAD-DIAGRAM-003)
        3. Structural clarity (SAD-DIAGRAM-004)

        Parameters
        ----------
        diagram : Dict
            Diagram object from DiagramDetector.
        tag_id : str
            SAD tag associated with diagram.
        tag_line : int
            Line number of SAD tag.

        Returns
        -------
        List[Violation]
            Detected quality violations (empty if valid).

        Examples
        --------
        >>> validator = DiagramValidator()
        >>> diagram = {
        ...     'content': '+---+\\n| A |\\n+---+',
        ...     'start_line': 10
        ... }
        >>> violations = validator.validate_diagram(diagram, 'SAD-1', 5)
        >>> len(violations)
        0  # Valid diagram
        """
        violations = []
        content = diagram['content']
        diagram_line = diagram['start_line']

        # Rule SAD-DIAGRAM-002: Recognized box characters
        unrecognized_violations = self._check_unrecognized_chars(
            content, tag_id, diagram_line
        )
        violations.extend(unrecognized_violations)

        # Rule SAD-DIAGRAM-003: Component relationships
        relationship_violations = self._check_component_relationships(
            content, tag_id, diagram_line
        )
        violations.extend(relationship_violations)

        # Rule SAD-DIAGRAM-004: Structural clarity
        clarity_violations = self._check_structural_clarity(
            content, tag_id, diagram_line
        )
        violations.extend(clarity_violations)

        return violations

    def _check_unrecognized_chars(
        self,
        content: str,
        tag_id: str,
        line: int
    ) -> List[Violation]:
        """
        Validate that diagram uses recognized box drawing characters.

        Rule: SAD-DIAGRAM-002
        Severity: WARNING (non-blocking but should be fixed)

        Parameters
        ----------
        content : str
            Diagram content.
        tag_id : str
            Associated SAD tag.
        line : int
            Diagram start line.

        Returns
        -------
        List[Violation]
            Violations for unrecognized characters.
        """
        violations = []

        # Extract all non-alphanumeric, non-whitespace characters
        special_chars = set(re.findall(r'[^\w\s]', content))

        # Find unrecognized characters
        unrecognized = special_chars - self.RECOGNIZED_BOX_CHARS

        # Filter out common label characters (allow parentheses, colons, etc.)
        allowed_label_chars = {'(', ')', ':', ',', '.', ';', '!', '?', '&', '*', '#', '@'}
        unrecognized = unrecognized - allowed_label_chars

        if unrecognized:
            violations.append(Violation(
                rule_id="SAD-DIAGRAM-002",
                severity=ViolationSeverity.WARNING,
                target_tag=tag_id,
                line_number=line,
                description=(
                    f"Diagram contains unrecognized box characters: {', '.join(sorted(unrecognized))}. "
                    f"Use standard ASCII/Unicode box drawing characters for consistency."
                ),
                suggested_fix="Replace unrecognized characters with standard box drawing characters"
            ))

        return violations

    def _check_component_relationships(
        self,
        content: str,
        tag_id: str,
        line: int
    ) -> List[Violation]:
        """
        Validate that diagram shows component relationships.

        Rule: SAD-DIAGRAM-003
        Severity: ERROR (blocking)

        Architecture diagrams must show relationships between components,
        not just isolated boxes. Requires arrows, lines, or connectors.

        Parameters
        ----------
        content : str
            Diagram content.
        tag_id : str
            Associated SAD tag.
        line : int
            Diagram start line.

        Returns
        -------
        List[Violation]
            Violations for missing relationships.
        """
        violations = []

        # Count components (boxes)
        box_pattern = re.compile(r'[+┌┐└┘╔╗╚╝][\-─═]+[+┌┐└┘╔╗╚╝]')
        components = len(box_pattern.findall(content))

        # Count connections (arrows, lines)
        connection_patterns = [
            r'[-=]{2,}>',      # -->
            r'<[-=]{2,}',      # <--
            r'<[-=]{2,}>',     # <-->
            r'\|',             # Vertical connector
            r'[-=]{3,}',       # Horizontal connector
            r'[/\\]'           # Diagonal connector
        ]
        connections = sum(len(re.findall(p, content)) for p in connection_patterns)

        # Validation checks
        if components < self.MIN_COMPONENTS:
            violations.append(Violation(
                rule_id="SAD-DIAGRAM-003",
                severity=ViolationSeverity.ERROR,
                target_tag=tag_id,
                line_number=line,
                description=(
                    f"Diagram has only {components} component(s). "
                    f"Architectural diagrams require at least {self.MIN_COMPONENTS} components "
                    f"to illustrate system structure."
                ),
                suggested_fix=f"Add additional components to show system architecture (minimum {self.MIN_COMPONENTS})"
            ))

        if connections < self.MIN_CONNECTIONS:
            violations.append(Violation(
                rule_id="SAD-DIAGRAM-003",
                severity=ViolationSeverity.ERROR,
                target_tag=tag_id,
                line_number=line,
                description=(
                    f"Diagram has only {connections} connection(s). "
                    f"Must show relationships between components using arrows or connectors."
                ),
                suggested_fix="Add arrows (-->, <--, etc.) or lines to show component relationships"
            ))

        return violations

    def _check_structural_clarity(
        self,
        content: str,
        tag_id: str,
        line: int
    ) -> List[Violation]:
        """
        Validate diagram has minimum structural clarity.

        Rule: SAD-DIAGRAM-004
        Severity: WARNING

        Diagrams should have sufficient complexity to convey architectural
        meaning. Very simple diagrams may lack necessary detail.

        Parameters
        ----------
        content : str
            Diagram content.
        tag_id : str
            Associated SAD tag.
        line : int
            Diagram start line.

        Returns
        -------
        List[Violation]
            Violations for insufficient clarity.
        """
        violations = []
        lines = content.split('\n')

        # Check minimum line count (already validated by detector, but double-check)
        min_lines = 3
        if len(lines) < min_lines:
            violations.append(Violation(
                rule_id="SAD-DIAGRAM-004",
                severity=ViolationSeverity.WARNING,
                target_tag=tag_id,
                line_number=line,
                description=(
                    f"Diagram has only {len(lines)} line(s). "
                    f"Minimum {min_lines} lines recommended for structural clarity."
                ),
                suggested_fix=f"Expand diagram to at least {min_lines} lines"
            ))

        # Check for component labels
        # Labels make diagrams self-documenting
        has_text_labels = bool(re.search(r'[A-Za-z]{2,}', content))
        if not has_text_labels:
            violations.append(Violation(
                rule_id="SAD-DIAGRAM-004",
                severity=ViolationSeverity.WARNING,
                target_tag=tag_id,
                line_number=line,
                description=(
                    "Diagram lacks text labels for components. "
                    "Label boxes with component names for clarity."
                ),
                suggested_fix="Add descriptive labels inside boxes (e.g., 'Core', 'UI', 'Runtime')"
            ))

        return violations

    def get_diagram_statistics(self, content: str) -> Dict:
        """
        Calculate diagram structural statistics.

        Parameters
        ----------
        content : str
            Diagram content.

        Returns
        -------
        Dict
            Statistical metrics:
            - line_count: int
            - char_count: int
            - box_count: int
            - arrow_count: int
            - label_count: int

        Examples
        --------
        >>> validator = DiagramValidator()
        >>> stats = validator.get_diagram_statistics('+---+\\n| A |\\n+---+')
        >>> stats['box_count']
        1
        """
        lines = content.split('\n')

        # Count boxes
        box_pattern = re.compile(r'[+┌┐└┘╔╗╚╝][\-─═]+[+┌┐└┘╔╗╚╝]')
        boxes = len(box_pattern.findall(content))

        # Count arrows
        arrow_patterns = [r'[-=]+>', r'<[-=]+', r'<[-=]+>']
        arrows = sum(len(re.findall(p, content)) for p in arrow_patterns)

        # Count labels (words inside boxes)
        labels = len(re.findall(r'\|\s*([A-Za-z]+)\s*\|', content))

        return {
            'line_count': len(lines),
            'char_count': len(content),
            'box_count': boxes,
            'arrow_count': arrows,
            'label_count': labels
        }

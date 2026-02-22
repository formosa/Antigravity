"""
ASCII Diagram Detector

Pattern matching engine for identifying ASCII topology diagrams in documentation.
Recognizes box-and-arrow, hierarchical, and network topology diagram styles.

Implements: ASCII diagram detection for SAD-tier validation
Requirements: |tier-sad.md| diagram format compliance

Author: DDR System Integration Team
Version: 1.0.0
"""

import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass


@dataclass
class DiagramMatch:
    """
    Represents a detected ASCII diagram.

    Attributes
    ----------
    start_line : int
        Line number where diagram begins.
    end_line : int
        Line number where diagram ends.
    content : str
        Raw ASCII diagram content.
    style : str
        Detected diagram style (box_and_arrow, hierarchical, network_topology).
    confidence : float
        Detection confidence score (0.0-1.0).
    box_chars : Set[str]
        Box drawing characters found in diagram.
    """
    start_line: int
    end_line: int
    content: str
    style: str
    confidence: float
    box_chars: Set[str]


class DiagramDetector:
    """
    ASCII diagram detection and classification engine.

    Identifies diagrams using multi-pattern heuristic matching across three
    recognized styles: box-and-arrow, hierarchical, and network topology.

    Parameters
    ----------
    min_lines : int, default=3
        Minimum consecutive lines required for valid diagram.
    confidence_threshold : float, default=0.6
        Minimum confidence score for positive detection.

    Attributes
    ----------
    BOX_CHARS : Set[str]
        Standard box drawing characters (ASCII art).
    ARROW_CHARS : Set[str]
        Directional arrow characters.
    CONNECTOR_CHARS : Set[str]
        Line connector characters.

    Notes
    -----
    Detection algorithm uses weighted scoring across multiple features:
    - Box character density
    - Arrow/connector presence
    - Horizontal alignment patterns
    - Structural consistency
    """

    # Box drawing characters (ASCII art)
    BOX_CHARS = {
        '+', '-', '|', '/',  '\\',
        '┌', '┐', '└', '┘', '─', '│',
        '├', '┤', '┬', '┴', '┼',
        '═', '║', '╔', '╗', '╚', '╝',
        '╠', '╣', '╦', '╩', '╬'
    }

    # Arrow and directional characters
    ARROW_CHARS = {
        '<', '>', '^', 'v', 'V',
        '←', '→', '↑', '↓', '↔', '↕',
        '⇐', '⇒', '⇑', '⇓', '⇔', '⇕'
    }

    # Connector characters
    CONNECTOR_CHARS = {'=', '-', '_', '~'}

    def __init__(self, min_lines: int = 3, confidence_threshold: float = 0.6):
        """
        Initialize diagram detector with configuration.

        Implements: Detector initialization with validation parameters
        Requirements: |skill.yaml| min_diagram_lines configuration
        """
        self.min_lines = min_lines
        self.confidence_threshold = confidence_threshold

    def find_diagrams(self, content: str) -> List[Dict]:
        """
        Locate all ASCII diagrams in document content.

        Scanning strategy:
        1. Split content into lines
        2. Identify candidate regions (consecutive lines with box chars)
        3. Classify diagram style
        4. Calculate confidence score
        5. Filter by minimum confidence

        Parameters
        ----------
        content : str
            Raw document content to scan.

        Returns
        -------
        List[Dict]
            Detected diagrams with metadata.

        Examples
        --------
        >>> detector = DiagramDetector()
        >>> content = '''
        ... .. sad:: Architecture
        ...    :id: SAD-1
        ...
        ... +-------+     +-------+
        ... | Core  | --> | UI    |
        ... +-------+     +-------+
        ... '''
        >>> diagrams = detector.find_diagrams(content)
        >>> len(diagrams)
        1
        """
        lines = content.split('\n')
        diagrams = []

        i = 0
        while i < len(lines):
            # Check if current line starts diagram region
            if self._is_diagram_line(lines[i]):
                diagram_match = self._extract_diagram(lines, i)

                if diagram_match and diagram_match.confidence >= self.confidence_threshold:
                    diagrams.append({
                        'start_line': diagram_match.start_line,
                        'end_line': diagram_match.end_line,
                        'content': diagram_match.content,
                        'style': diagram_match.style,
                        'confidence': diagram_match.confidence
                    })
                    i = diagram_match.end_line + 1
                else:
                    i += 1
            else:
                i += 1

        return diagrams

    def _is_diagram_line(self, line: str) -> bool:
        """
        Quick heuristic check if line could be part of diagram.

        Parameters
        ----------
        line : str
            Single line to evaluate.

        Returns
        -------
        bool
            True if line contains diagram-like characters.
        """
        stripped = line.strip()
        if not stripped or len(stripped) < 3:
            return False

        # Must contain box or arrow characters
        char_set = set(stripped)
        return bool(char_set & (self.BOX_CHARS | self.ARROW_CHARS | self.CONNECTOR_CHARS))

    def _extract_diagram(self, lines: List[str], start_idx: int) -> Optional[DiagramMatch]:
        """
        Extract complete diagram starting at given line index.

        Parameters
        ----------
        lines : List[str]
            All document lines.
        start_idx : int
            Starting line index.

        Returns
        -------
        Optional[DiagramMatch]
            Extracted diagram or None if invalid.
        """
        diagram_lines = []
        current_idx = start_idx

        # Collect consecutive diagram lines
        while current_idx < len(lines) and self._is_diagram_line(lines[current_idx]):
            diagram_lines.append(lines[current_idx])
            current_idx += 1

        # Validate minimum length
        if len(diagram_lines) < self.min_lines:
            return None

        # Join content
        content = '\n'.join(diagram_lines)

        # Classify style and calculate confidence
        style = self._classify_style(content)
        confidence = self._calculate_confidence(content, style)

        # Extract box characters used
        box_chars = set(content) & self.BOX_CHARS

        return DiagramMatch(
            start_line=start_idx,
            end_line=current_idx - 1,
            content=content,
            style=style,
            confidence=confidence,
            box_chars=box_chars
        )

    def _classify_style(self, content: str) -> str:
        """
        Determine diagram style based on structural patterns.

        Parameters
        ----------
        content : str
            Diagram content to classify.

        Returns
        -------
        str
            Style identifier: box_and_arrow, hierarchical, or network_topology.
        """
        # Box-and-arrow: rectangular boxes with arrows/lines
        if self._has_box_pattern(content) and self._has_arrows(content):
            return "box_and_arrow"

        # Hierarchical: tree-like structure with vertical connectors
        elif self._has_tree_pattern(content):
            return "hierarchical"

        # Network topology: interconnected nodes
        elif self._has_network_pattern(content):
            return "network_topology"

        else:
            return "unknown"

    def _has_box_pattern(self, content: str) -> bool:
        """Check for rectangular box patterns (corners + edges)."""
        # Look for corner patterns like +---+ or ┌───┐
        corner_pattern = re.compile(r'[+┌┐└┘╔╗╚╝][\-─═]+[+┌┐└┘╔╗╚╝]')
        return bool(corner_pattern.search(content))

    def _has_arrows(self, content: str) -> bool:
        """Check for arrow or connector sequences."""
        arrow_patterns = [
            r'[-=]+>',  # -->
            r'<[-=]+',  # <--
            r'<[-=]+>', # <-->
            r'[-=]{2,}' # Horizontal connectors
        ]
        return any(re.search(pattern, content) for pattern in arrow_patterns)

    def _has_tree_pattern(self, content: str) -> bool:
        """Check for hierarchical tree structure."""
        # Look for branching patterns with vertical bars and horizontal branches
        tree_patterns = [
            r'\|',          # Vertical stem
            r'[├└]',        # Branch characters
            r'[\\/]',       # Diagonal connectors
        ]
        return sum(bool(re.search(p, content)) for p in tree_patterns) >= 2

    def _has_network_pattern(self, content: str) -> bool:
        """Check for network topology (multiple interconnected nodes)."""
        # Count boxes and connectors
        boxes = len(re.findall(r'[+┌┐└┘][\-─]+[+┌┐└┘]', content))
        arrows = len(re.findall(r'<?[-=]+>?', content))

        # Network topology has multiple boxes with multiple connections
        return boxes >= 2 and arrows >= 2

    def _calculate_confidence(self, content: str, style: str) -> float:
        """
        Calculate confidence score for diagram detection.

        Scoring factors (weighted):
        - Box character density: 30%
        - Arrow/connector presence: 20%
        - Alignment consistency: 25%
        - Style coherence: 25%

        Parameters
        ----------
        content : str
            Diagram content.
        style : str
            Classified style.

        Returns
        -------
        float
            Confidence score (0.0-1.0).
        """
        score = 0.0
        total_chars = len(content)

        if total_chars == 0:
            return 0.0

        # Factor 1: Box character density (30%)
        box_char_count = sum(content.count(c) for c in self.BOX_CHARS)
        box_density = box_char_count / total_chars
        score += min(box_density * 3, 0.3)  # Cap at 30%

        # Factor 2: Arrow/connector presence (20%)
        arrow_count = sum(content.count(c) for c in self.ARROW_CHARS | self.CONNECTOR_CHARS)
        if arrow_count > 0:
            score += 0.2

        # Factor 3: Alignment consistency (25%)
        lines = content.split('\n')
        if self._has_consistent_alignment(lines):
            score += 0.25

        # Factor 4: Style coherence (25%)
        if style != "unknown":
            score += 0.25

        return min(score, 1.0)

    def _has_consistent_alignment(self, lines: List[str]) -> bool:
        """
        Check if diagram lines have consistent horizontal alignment.

        Parameters
        ----------
        lines : List[str]
            Diagram lines to check.

        Returns
        -------
        bool
            True if lines show structural alignment.
        """
        if len(lines) < 2:
            return False

        # Check for similar line lengths (within 20% variance)
        lengths = [len(line.rstrip()) for line in lines if line.strip()]
        if not lengths:
            return False

        avg_length = sum(lengths) / len(lengths)
        variance = sum(abs(l - avg_length) for l in lengths) / len(lengths)

        return variance / avg_length < 0.2 if avg_length > 0 else False

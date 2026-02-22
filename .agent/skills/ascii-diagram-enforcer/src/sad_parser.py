"""
SAD-Tier RST Directive Parser

Extracts SAD (System Architecture Document) tags from reStructuredText content
using Sphinx-Needs directive syntax.

Implements: SAD tag extraction for diagram enforcement
Requirements: |patterns/tag-syntax.md|, |concepts/tier-sad.md|

Author: DDR System Integration Team
Version: 1.0.0
"""

import re
from typing import List, Dict, Optional, Tuple


class SADParser:
    """
    Parser for SAD-tier reStructuredText directives.

    Extracts tag metadata from Sphinx-Needs `.. sad::` directives, validating
    tag ID format and citation structure according to DDR System conventions.

    Attributes
    ----------
    SAD_DIRECTIVE_PATTERN : re.Pattern
        Regex pattern for matching `.. sad::` directives.
    TAG_ID_PATTERN : re.Pattern
        Regex pattern for validating SAD tag IDs.
    BLOCK_TAG_PATTERN : re.Pattern
        Regex pattern for block-level tags (SAD-N).
    ATOMIC_TAG_PATTERN : re.Pattern
        Regex pattern for atomic-level tags (SAD-N.M).

    Notes
    -----
    Tag format specification:
    - Block-level: SAD-N (where N is integer)
    - Atomic-level: SAD-N.M (where N.M are integers)

    Directive syntax:
    ```rst
    .. sad:: Title or Description
       :id: SAD-N
       :links: PARENT-X, PARENT-Y
    ```
    """

    # Regex patterns for SAD directive parsing
    SAD_DIRECTIVE_PATTERN = re.compile(
        r'^\.\.\s+sad::\s+(.+?)$\n'              # Directive header with title
        r'(?:\s+:id:\s+(.+?)$\n)?'              # Optional :id: field
        r'(?:\s+:links:\s+(.+?)$\n)?',          # Optional :links: field
        re.MULTILINE
    )

    TAG_ID_PATTERN = re.compile(r'^SAD-\d+(?:\.\d+)?$')
    BLOCK_TAG_PATTERN = re.compile(r'^SAD-\d+$')
    ATOMIC_TAG_PATTERN = re.compile(r'^SAD-\d+\.\d+$')

    def __init__(self):
        """
        Initialize SAD parser.

        Implements: Parser initialization
        Requirements: DDR tag syntax compliance
        """
        pass

    def extract_sad_tags(self, content: str) -> List[Dict]:
        """
        Extract all SAD tags from document content.

        Parsing workflow:
        1. Locate `.. sad::` directive blocks
        2. Extract :id: and :links: fields
        3. Validate tag ID format
        4. Determine tag level (block vs atomic)
        5. Record line numbers for violation reporting

        Parameters
        ----------
        content : str
            Raw RST document content.

        Returns
        -------
        List[Dict]
            Parsed SAD tag metadata. Each dict contains:
            - id: str - Tag identifier (e.g., 'SAD-1')
            - title: str - Directive title/description
            - links: List[str] - Parent tag citations
            - line_number: int - Line where tag appears
            - level: str - 'block' or 'atomic'

        Examples
        --------
        >>> parser = SADParser()
        >>> content = '''
        ... .. sad:: Hub-and-Spoke Architecture
        ...    :id: SAD-1
        ...    :links: FSD-1
        ... '''
        >>> tags = parser.extract_sad_tags(content)
        >>> tags[0]['id']
        'SAD-1'
        >>> tags[0]['level']
        'block'
        """
        tags = []
        lines = content.split('\n')

        # Enhanced pattern that handles multi-line directives
        for line_idx, line in enumerate(lines, start=1):
            # Check for directive start
            if line.strip().startswith('.. sad::'):
                tag_data = self._parse_directive_block(lines, line_idx - 1)
                if tag_data:
                    tags.append(tag_data)

        return tags

    def _parse_directive_block(self, lines: List[str], start_idx: int) -> Optional[Dict]:
        """
        Parse complete directive block starting at given line.

        Parameters
        ----------
        lines : List[str]
            All document lines.
        start_idx : int
            Index of `.. sad::` line.

        Returns
        -------
        Optional[Dict]
            Parsed tag data or None if invalid.
        """
        # Extract directive header
        header_line = lines[start_idx]
        title_match = re.match(r'^\.\.\s+sad::\s+(.+)$', header_line.strip())
        if not title_match:
            return None

        title = title_match.group(1).strip()

        # Parse indented fields (:id:, :links:)
        tag_id = None
        links = []

        current_idx = start_idx + 1
        while current_idx < len(lines):
            line = lines[current_idx]

            # Stop at next directive or unindented content
            if not line.strip() or not line.startswith((' ', '\t')):
                # Allow one blank line, then stop
                if current_idx + 1 < len(lines) and lines[current_idx + 1].startswith((' ', '\t')):
                    current_idx += 1
                    continue
                else:
                    break

            # Parse :id: field
            id_match = re.match(r'^\s+:id:\s+(.+)$', line)
            if id_match:
                tag_id = id_match.group(1).strip()

            # Parse :links: field
            links_match = re.match(r'^\s+:links:\s+(.+)$', line)
            if links_match:
                links_str = links_match.group(1).strip()
                links = [l.strip() for l in links_str.split(',')]

            current_idx += 1

        # Validate tag ID
        if not tag_id or not self.TAG_ID_PATTERN.match(tag_id):
            return None

        # Determine tag level
        if self.BLOCK_TAG_PATTERN.match(tag_id):
            level = 'block'
        elif self.ATOMIC_TAG_PATTERN.match(tag_id):
            level = 'atomic'
        else:
            level = 'unknown'

        return {
            'id': tag_id,
            'title': title,
            'links': links,
            'line_number': start_idx + 1,  # Convert to 1-based line number
            'level': level
        }

    def is_block_tag(self, tag_id: str) -> bool:
        """
        Check if tag ID represents block-level tag.

        Parameters
        ----------
        tag_id : str
            Tag identifier to check.

        Returns
        -------
        bool
            True if block-level (SAD-N format).

        Examples
        --------
        >>> parser = SADParser()
        >>> parser.is_block_tag('SAD-1')
        True
        >>> parser.is_block_tag('SAD-1.2')
        False
        """
        return bool(self.BLOCK_TAG_PATTERN.match(tag_id))

    def is_atomic_tag(self, tag_id: str) -> bool:
        """
        Check if tag ID represents atomic-level tag.

        Parameters
        ----------
        tag_id : str
            Tag identifier to check.

        Returns
        -------
        bool
            True if atomic-level (SAD-N.M format).

        Examples
        --------
        >>> parser = SADParser()
        >>> parser.is_atomic_tag('SAD-1')
        False
        >>> parser.is_atomic_tag('SAD-1.2')
        True
        """
        return bool(self.ATOMIC_TAG_PATTERN.match(tag_id))

    def extract_block_parent(self, atomic_tag_id: str) -> Optional[str]:
        """
        Extract parent block tag ID from atomic tag.

        Parameters
        ----------
        atomic_tag_id : str
            Atomic tag identifier (e.g., 'SAD-1.2').

        Returns
        -------
        Optional[str]
            Parent block tag ID (e.g., 'SAD-1') or None if invalid.

        Examples
        --------
        >>> parser = SADParser()
        >>> parser.extract_block_parent('SAD-1.2')
        'SAD-1'
        >>> parser.extract_block_parent('SAD-5.10')
        'SAD-5'
        """
        if not self.is_atomic_tag(atomic_tag_id):
            return None

        # Extract block number (everything before last dot)
        parts = atomic_tag_id.split('.')
        return parts[0]

    def validate_citation_hierarchy(
        self,
        tag_id: str,
        cited_tags: List[str]
    ) -> Tuple[bool, List[str]]:
        """
        Validate that cited parent tags follow proper tier hierarchy.

        SAD tags must cite FSD tags (primarily) per DDR rules.

        Parameters
        ----------
        tag_id : str
            SAD tag being validated.
        cited_tags : List[str]
            Tags cited in :links: field.

        Returns
        -------
        Tuple[bool, List[str]]
            (is_valid, error_messages)

        Examples
        --------
        >>> parser = SADParser()
        >>> valid, errors = parser.validate_citation_hierarchy('SAD-1', ['FSD-2'])
        >>> valid
        True
        >>> valid, errors = parser.validate_citation_hierarchy('SAD-1', ['TDD-1'])
        >>> valid
        False
        >>> errors
        ['SAD cannot cite TDD (forward reference violation)']
        """
        errors = []

        # Valid parent tiers for SAD: FSD
        VALID_PARENT_PREFIXES = {'FSD'}

        for cited_tag in cited_tags:
            # Extract tier prefix
            prefix = cited_tag.split('-')[0]

            if prefix not in VALID_PARENT_PREFIXES:
                errors.append(
                    f"SAD cannot cite {prefix} (invalid parent tier). "
                    f"SAD must cite FSD tags."
                )

        return len(errors) == 0, errors

"""
RST parser for extracting DDR tags from documentation.

Implements: Sphinx-Needs directive parsing
Requirements: tag-syntax.md RST directive format
"""

from typing import List, Optional, Dict
import re

from .models import Tag


class RSTParser:
    """
    Parses RST files to extract DDR tag directives.

    Supports Sphinx-Needs directive format:
    .. tier:: Title
       :id: TIER-N
       :links: PARENT-X, PARENT-Y

    Ref: |patterns/tag-syntax.md|
    """

    def __init__(self):
        """
        Initialize RST parser.

        Implements: Tag extraction protocol
        """
        # Pattern for directive start: .. tier::
        self.directive_pattern = re.compile(
            r'^\.\.\s+(brd|nfr|fsd|sad|icd|tdd|isp)::\s+(.+)$',
            re.IGNORECASE
        )

        # Pattern for :id: field
        self.id_pattern = re.compile(r'^\s+:id:\s+([A-Z]{3}-\d+(?:\.\d+)?)$')

        # Pattern for :links: field
        self.links_pattern = re.compile(r'^\s+:links:\s+(.+)$')

    def parse_tags(self, content: str) -> List[Tag]:
        """
        Extract all DDR tags from RST content.

        Parameters
        ----------
        content : str
            RST file content.

        Returns
        -------
        List[Tag]
            List of parsed tags in document order.
        """
        lines = content.split('\n')
        tags = []
        current_tag = None
        current_line_num = 0

        for line_num, line in enumerate(lines, start=1):
            # Check for directive start
            directive_match = self.directive_pattern.match(line)
            if directive_match:
                # Save previous tag if exists
                if current_tag:
                    tags.append(current_tag)

                tier = directive_match.group(1).upper()
                title = directive_match.group(2).strip()
                current_line_num = line_num

                # Initialize new tag (ID not yet known)
                current_tag = {
                    'tier': tier,
                    'title': title,
                    'line_number': line_num,
                    'links': [],
                    'content': ''
                }
                continue

            # If we're inside a tag directive
            if current_tag:
                # Check for :id: field
                id_match = self.id_pattern.match(line)
                if id_match:
                    tag_id = id_match.group(1)
                    current_tag['tag_id'] = tag_id

                    # Parse tag components
                    parsed = Tag.parse_tag_id(tag_id)
                    current_tag['block_number'] = parsed['block_number']
                    current_tag['atomic_number'] = parsed['atomic_number']
                    continue

                # Check for :links: field
                links_match = self.links_pattern.match(line)
                if links_match:
                    links_str = links_match.group(1)
                    # Split on commas and clean whitespace
                    links = [l.strip() for l in links_str.split(',')]
                    current_tag['links'] = links
                    continue

                # Check if we've left the directive (non-indented line)
                if line and not line.startswith(' '):
                    # Save current tag and reset
                    if 'tag_id' in current_tag:
                        tags.append(self._create_tag(current_tag))
                    current_tag = None
                    continue

                # Accumulate content
                if line.strip():
                    current_tag['content'] += line.strip() + ' '

        # Save last tag if exists
        if current_tag and 'tag_id' in current_tag:
            tags.append(self._create_tag(current_tag))

        return tags

    def _create_tag(self, tag_dict: Dict) -> Tag:
        """
        Create Tag instance from parsed dictionary.

        Parameters
        ----------
        tag_dict : Dict
            Dictionary with parsed tag fields.

        Returns
        -------
        Tag
            Tag instance.
        """
        return Tag(
            tag_id=tag_dict['tag_id'],
            tier=tag_dict['tier'],
            block_number=tag_dict['block_number'],
            atomic_number=tag_dict.get('atomic_number'),
            line_number=tag_dict['line_number'],
            title=tag_dict['title'],
            links=tag_dict.get('links', []),
            content=tag_dict.get('content', '').strip()
        )

    def find_tag_by_id(self, tags: List[Tag], tag_id: str) -> Optional[Tag]:
        """
        Find tag by ID in list.

        Parameters
        ----------
        tags : List[Tag]
            List of tags to search.
        tag_id : str
            Tag ID to find.

        Returns
        -------
        Optional[Tag]
            Matching tag or None.
        """
        for tag in tags:
            if tag.tag_id == tag_id:
                return tag
        return None

    def get_tags_by_tier(self, tags: List[Tag], tier: str) -> List[Tag]:
        """
        Filter tags by tier.

        Parameters
        ----------
        tags : List[Tag]
            List of all tags.
        tier : str
            Tier to filter (BRD, NFR, etc.).

        Returns
        -------
        List[Tag]
            Tags matching tier.
        """
        return [tag for tag in tags if tag.tier == tier]

    def get_block_tags(self, tags: List[Tag]) -> List[Tag]:
        """
        Get only block-level tags (TIER-N).

        Parameters
        ----------
        tags : List[Tag]
            List of all tags.

        Returns
        -------
        List[Tag]
            Block-level tags only.
        """
        return [tag for tag in tags if tag.is_block]

    def get_atomic_tags(self, tags: List[Tag]) -> List[Tag]:
        """
        Get only atomic-level tags (TIER-N.M).

        Parameters
        ----------
        tags : List[Tag]
            List of all tags.

        Returns
        -------
        List[Tag]
            Atomic-level tags only.
        """
        return [tag for tag in tags if tag.is_atomic]

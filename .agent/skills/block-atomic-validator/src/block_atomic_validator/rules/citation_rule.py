"""
Citation rule: Atomic tags must cite their block parent.

Implements: Block parent citation requirement
Requirements: Atomic tags (TIER-N.M) must cite parent block (TIER-N) via :links:
"""

from typing import List, Dict

from ..core.models import Tag, Violation, ViolationType


class CitationRule:
    """
    Validates atomic tags cite their block parent.

    Ref: |constraints/tag-citation-required.md|

    Parameters
    ----------
    config : Dict
        Configuration dictionary.
    """

    def __init__(self, config: Dict):
        """
        Initialize citation rule.

        Implements: Parent citation validation
        """
        self.config = config
        self.severity = config.get('validation_rules', {}) \
                             .get('missing_block_citation', {}) \
                             .get('severity', 'error')

    def validate(self, tags: List[Tag], context) -> List[Violation]:
        """
        Check atomic tags cite block parents.

        Parameters
        ----------
        tags : List[Tag]
            All tags in document.
        context : ValidationContext
            Validation context with file info.

        Returns
        -------
        List[Violation]
            List of citation violations found.
        """
        violations = []

        # Build tag lookup
        tag_lookup = {tag.tag_id: tag for tag in tags}

        # Check each atomic tag
        for tag in tags:
            if not tag.is_atomic:
                continue

            expected_block_id = tag.get_block_id()

            # Check if block exists
            if expected_block_id not in tag_lookup:
                # This is orphaned atomic - handled by consistency rule
                continue

            # Check if atomic cites its block parent
            if not tag.validates_block_citation():
                violation = Violation(
                    type=ViolationType.MISSING_BLOCK_CITATION,
                    severity=self.severity,
                    message=(
                        f"Atomic tag {tag.tag_id} must cite parent "
                        f"block {expected_block_id} in :links: directive"
                    ),
                    tag_id=tag.tag_id,
                    line_number=tag.line_number,
                    related_tag_id=expected_block_id,
                    fix_suggestion=(
                        f"Add '{expected_block_id}' to :links: directive. "
                        f"Current links: {', '.join(tag.links) if tag.links else 'none'}"
                    )
                )
                violations.append(violation)

        return violations

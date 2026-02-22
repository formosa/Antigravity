"""
Ordering rule: Block tags must precede atomic children.

Implements: Block-atomic precedence constraint
Requirements: Block tags (TIER-N) appear before atomic (TIER-N.M) in document
"""

from typing import List, Dict

from ..core.models import Tag, Violation, ViolationType


class OrderingRule:
    """
    Validates block tags appear before their atomic children.

    Ref: |constraints/block_atomic_ordering.md|

    Parameters
    ----------
    config : Dict
        Configuration dictionary.
    """

    def __init__(self, config: Dict):
        """
        Initialize ordering rule.

        Implements: Precedence validation
        """
        self.config = config
        self.severity = config.get('validation_rules', {}) \
                             .get('ordering_violation', {}) \
                             .get('severity', 'error')

    def validate(self, tags: List[Tag], context) -> List[Violation]:
        """
        Check block-atomic ordering for all tags.

        Parameters
        ----------
        tags : List[Tag]
            All tags in document (in document order).
        context : ValidationContext
            Validation context with file info.

        Returns
        -------
        List[Violation]
            List of ordering violations found.
        """
        violations = []

        # Build position map: tag_id -> position_index
        position_map = {tag.tag_id: idx for idx, tag in enumerate(tags)}

        # Check each atomic tag
        for tag in tags:
            if not tag.is_atomic:
                continue

            block_id = tag.get_block_id()

            # Find block tag position
            if block_id not in position_map:
                # This is orphaned atomic - handled by consistency rule
                continue

            block_position = position_map[block_id]
            atomic_position = position_map[tag.tag_id]

            # Block must come before atomic
            if block_position > atomic_position:
                violation = Violation(
                    type=ViolationType.ORDERING_VIOLATION,
                    severity=self.severity,
                    message=(
                        f"Block tag {block_id} must appear before "
                        f"atomic child {tag.tag_id}"
                    ),
                    tag_id=tag.tag_id,
                    line_number=tag.line_number,
                    related_tag_id=block_id,
                    fix_suggestion=(
                        f"Move block tag {block_id} to appear before "
                        f"line {tag.line_number}"
                    )
                )
                violations.append(violation)

        return violations

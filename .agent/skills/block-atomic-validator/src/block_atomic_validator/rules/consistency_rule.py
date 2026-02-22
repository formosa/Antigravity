"""
Consistency rule: No orphaned atomics, prefix consistency.

Implements: Block-atomic structural consistency
Requirements: All atomic tags must have corresponding block, prefix matches
"""

from typing import List, Dict, Set

from ..core.models import Tag, Violation, ViolationType


class ConsistencyRule:
    """
    Validates structural consistency of block-atomic relationships.

    Checks:
    1. No orphaned atomic tags (TIER-N.M without TIER-N)
    2. Prefix consistency (tier matches between block/atomic)

    Ref: |constraints/tag-immutability.md|, |patterns/tag-syntax.md|

    Parameters
    ----------
    config : Dict
        Configuration dictionary.
    """

    def __init__(self, config: Dict):
        """
        Initialize consistency rule.

        Implements: Structural validation
        """
        self.config = config
        self.orphan_severity = config.get('validation_rules', {}) \
                                    .get('orphaned_atomic', {}) \
                                    .get('severity', 'error')
        self.prefix_severity = config.get('validation_rules', {}) \
                                    .get('prefix_mismatch', {}) \
                                    .get('severity', 'warning')

    def validate(self, tags: List[Tag], context) -> List[Violation]:
        """
        Check structural consistency.

        Parameters
        ----------
        tags : List[Tag]
            All tags in document.
        context : ValidationContext
            Validation context with file info.

        Returns
        -------
        List[Violation]
            List of consistency violations found.
        """
        violations = []

        # Build set of all block IDs
        block_ids = {tag.tag_id for tag in tags if tag.is_block}

        # Check each atomic tag
        for tag in tags:
            if not tag.is_atomic:
                continue

            expected_block_id = tag.get_block_id()

            # Check for orphaned atomic
            if expected_block_id not in block_ids:
                violation = Violation(
                    type=ViolationType.ORPHANED_ATOMIC,
                    severity=self.orphan_severity,
                    message=(
                        f"Atomic tag {tag.tag_id} has no corresponding "
                        f"block tag {expected_block_id}"
                    ),
                    tag_id=tag.tag_id,
                    line_number=tag.line_number,
                    related_tag_id=expected_block_id,
                    fix_suggestion=(
                        f"Create block tag {expected_block_id} or remove "
                        f"orphaned atomic tag {tag.tag_id}"
                    )
                )
                violations.append(violation)
                continue  # Don't check prefix if orphaned

            # Check prefix consistency
            violations.extend(
                self._check_prefix_consistency(tag, expected_block_id)
            )

        return violations

    def _check_prefix_consistency(
        self,
        atomic_tag: Tag,
        block_id: str
    ) -> List[Violation]:
        """
        Verify tier prefix matches between atomic and block.

        Parameters
        ----------
        atomic_tag : Tag
            Atomic tag to check.
        block_id : str
            Expected block ID.

        Returns
        -------
        List[Violation]
            Prefix mismatch violations.
        """
        violations = []

        # Extract tier from block_id
        block_tier = block_id.split('-')[0]

        # Compare tiers
        if atomic_tag.tier != block_tier:
            violation = Violation(
                type=ViolationType.PREFIX_MISMATCH,
                severity=self.prefix_severity,
                message=(
                    f"Atomic tag {atomic_tag.tag_id} has tier '{atomic_tag.tier}' "
                    f"but expected block has tier '{block_tier}'"
                ),
                tag_id=atomic_tag.tag_id,
                line_number=atomic_tag.line_number,
                related_tag_id=block_id,
                fix_suggestion=(
                    f"Change tag ID from {atomic_tag.tag_id} to "
                    f"{block_tier}-{atomic_tag.block_number}.{atomic_tag.atomic_number}"
                )
            )
            violations.append(violation)

        return violations

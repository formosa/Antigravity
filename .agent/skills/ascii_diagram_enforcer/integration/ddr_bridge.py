"""
DDR System Bridge

Integration layer connecting ASCII Diagram Enforcer with broader DDR System
components including traceability auditor, manifest manager, and other skills.

Implements: Cross-skill integration for DDR ecosystem
Requirements: DDR Core Skill >=2.0.0

Author: DDR System Integration Team
Version: 1.0.0
"""

import logging
from typing import Dict, List, Optional, Set
from pathlib import Path

from ascii_diagram_enforcer.src import ValidationResult, ViolationSeverity


logger = logging.getLogger(__name__)


class DDRBridge:
    """
    Bridge connecting ASCII Diagram Enforcer to DDR System ecosystem.

    Provides interfaces for:
    - Traceability chain validation
    - Cross-tier impact analysis
    - Manifest synchronization
    - Integration with other DDR skills

    Parameters
    ----------
    context : SkillContext
        IDE context with access to other skills.

    Attributes
    ----------
    context : SkillContext
        IDE integration context.
    ddr_core : Optional[object]
        Reference to DDR Core skill if available.

    Notes
    -----
    Gracefully degrades if DDR Core skill is not installed.
    All methods return meaningful results even without full DDR ecosystem.
    """

    def __init__(self, context):
        """
        Initialize DDR bridge with IDE context.

        Implements: Bridge initialization with graceful degradation
        Requirements: Optional DDR Core skill integration
        """
        self.context = context
        self.ddr_core = self._get_ddr_core_skill()

        if self.ddr_core:
            logger.info("DDR Core skill detected - full integration enabled")
        else:
            logger.warning("DDR Core skill not found - limited integration mode")

    def _get_ddr_core_skill(self):
        """
        Attempt to get reference to DDR Core skill.

        Returns
        -------
        Optional[object]
            DDR Core skill instance or None.
        """
        try:
            return self.context.get_skill('ddr_core')
        except Exception as e:
            logger.debug(f"DDR Core skill not available: {e}")
            return None

    def validate_traceability_chain(
        self,
        sad_tag: str,
        document_content: str
    ) -> Dict[str, any]:
        """
        Validate complete traceability chain from SAD tag to BRD root.

        Ensures diagram-validated SAD tags have proper citations back to
        business requirements per DDR hierarchy rules.

        Parameters
        ----------
        sad_tag : str
            SAD tag ID to validate (e.g., 'SAD-1').
        document_content : str
            Document content containing tag.

        Returns
        -------
        Dict[str, any]
            Traceability validation results with keys:
            - is_valid: bool - Complete chain exists
            - chain: List[str] - Tag IDs in chain
            - missing_links: List[str] - Broken citations

        Examples
        --------
        >>> bridge = DDRBridge(context)
        >>> result = bridge.validate_traceability_chain('SAD-1', content)
        >>> result['chain']
        ['SAD-1', 'FSD-1', 'BRD-2']

        Notes
        -----
        Requires DDR Core skill for full validation.
        Returns simplified results if DDR Core unavailable.
        """
        if not self.ddr_core:
            logger.warning("DDR Core unavailable - traceability check limited")
            return {
                "is_valid": None,
                "chain": [sad_tag],
                "missing_links": [],
                "error": "DDR Core skill not available"
            }

        try:
            # Delegate to DDR Core's traceability auditor
            chain_result = self.ddr_core.validate_chain(sad_tag, document_content)

            return {
                "is_valid": chain_result.get('valid', False),
                "chain": chain_result.get('chain', [sad_tag]),
                "missing_links": chain_result.get('broken_citations', [])
            }

        except Exception as e:
            logger.error(f"Traceability validation error: {e}")
            return {
                "is_valid": False,
                "chain": [sad_tag],
                "missing_links": [],
                "error": str(e)
            }

    def analyze_downstream_impact(
        self,
        sad_tag: str
    ) -> Dict[str, any]:
        """
        Analyze downstream impact if SAD tag is modified.

        Identifies TDD/ISP tags that cite this SAD tag and would require
        review if the architecture diagram changes.

        Parameters
        ----------
        sad_tag : str
            SAD tag to analyze.

        Returns
        -------
        Dict[str, any]
            Impact analysis with keys:
            - affected_tdd: List[str] - TDD tags citing this SAD
            - affected_isp: List[str] - ISP tags citing this SAD
            - total_impact: int - Total affected tags

        Examples
        --------
        >>> impact = bridge.analyze_downstream_impact('SAD-1')
        >>> impact['affected_tdd']
        ['TDD-1', 'TDD-3']
        """
        if not self.ddr_core:
            return {
                "affected_tdd": [],
                "affected_isp": [],
                "total_impact": 0,
                "error": "DDR Core skill not available"
            }

        try:
            impact = self.ddr_core.analyze_impact(sad_tag)

            return {
                "affected_tdd": impact.get('tdd_tags', []),
                "affected_isp": impact.get('isp_tags', []),
                "total_impact": impact.get('total_count', 0)
            }

        except Exception as e:
            logger.error(f"Impact analysis error: {e}")
            return {
                "affected_tdd": [],
                "affected_isp": [],
                "total_impact": 0,
                "error": str(e)
            }

    def sync_with_manifest_manager(
        self,
        section_id: str,
        validation_result: ValidationResult
    ) -> Dict[str, any]:
        """
        Synchronize validation results with DDR Manifest Manager skill.

        Ensures diagram violations are properly tracked across the entire
        DDR documentation system.

        Parameters
        ----------
        section_id : str
            Section identifier.
        validation_result : ValidationResult
            Validation results to sync.

        Returns
        -------
        Dict[str, any]
            Synchronization results.

        Examples
        --------
        >>> result = enforcer.validate_section(content, 'sad-root')
        >>> sync = bridge.sync_with_manifest_manager('sad-root', result)
        >>> sync['synced']
        True
        """
        manifest_manager = self._get_manifest_manager()

        if not manifest_manager:
            logger.warning("Manifest Manager skill not available")
            return {
                "synced": False,
                "error": "Manifest Manager skill not installed"
            }

        try:
            # Convert to manifest format
            pending_items = [
                result.to_reconciliation_item()
            ] if not validation_result.is_valid else []

            # Sync with manager
            sync_result = manifest_manager.update_section(
                section_id=section_id,
                integrity_status="DIRTY" if not validation_result.is_valid else "CLEAN",
                pending_items=pending_items
            )

            return {
                "synced": True,
                "manifest_updated": sync_result.get('updated', False)
            }

        except Exception as e:
            logger.error(f"Manifest sync error: {e}")
            return {
                "synced": False,
                "error": str(e)
            }

    def _get_manifest_manager(self):
        """
        Get reference to Manifest Manager skill.

        Returns
        -------
        Optional[object]
            Manifest Manager skill or None.
        """
        try:
            return self.context.get_skill('manifest_manager')
        except Exception:
            return None

    def get_related_sad_tags(
        self,
        sad_tag: str
    ) -> Dict[str, List[str]]:
        """
        Find related SAD tags at same abstraction level.

        Useful for suggesting architectural consistency checks across
        sibling components.

        Parameters
        ----------
        sad_tag : str
            SAD tag to find siblings for.

        Returns
        -------
        Dict[str, List[str]]
            Related tags with keys:
            - siblings: List[str] - Peer SAD tags
            - children: List[str] - Child atomic tags

        Examples
        --------
        >>> related = bridge.get_related_sad_tags('SAD-1')
        >>> related['siblings']
        ['SAD-2', 'SAD-3']
        >>> related['children']
        ['SAD-1.1', 'SAD-1.2']
        """
        # Extract block number
        if '.' in sad_tag:
            # Atomic tag - find parent
            block_tag = sad_tag.split('.')[0]
            parent_num = int(block_tag.split('-')[1])
        else:
            # Block tag
            block_tag = sad_tag
            parent_num = int(sad_tag.split('-')[1])

        # Generate sibling range (simple heuristic)
        siblings = [
            f"SAD-{i}" for i in range(max(1, parent_num - 2), parent_num + 3)
            if i != parent_num
        ]

        # Generate child range for block tags
        if '.' not in sad_tag:
            children = [f"{block_tag}.{i}" for i in range(1, 6)]
        else:
            children = []

        return {
            "siblings": siblings,
            "children": children
        }

    def generate_cross_skill_report(
        self,
        validation_result: ValidationResult
    ) -> str:
        """
        Generate comprehensive report integrating data from multiple DDR skills.

        Parameters
        ----------
        validation_result : ValidationResult
            Validation results to report on.

        Returns
        -------
        str
            Formatted cross-skill integration report.

        Examples
        --------
        >>> report = bridge.generate_cross_skill_report(result)
        >>> print(report)
        === DDR System Integration Report ===
        ASCII Diagram Validation: FAILED
        Traceability Status: CLEAN
        ...
        """
        lines = [
            "=" * 70,
            "DDR System Integration Report",
            "=" * 70,
            "",
            f"ASCII Diagram Validation: {'PASSED' if validation_result.is_valid else 'FAILED'}",
            f"SAD Tags Validated: {validation_result.sad_tags_found}",
            f"Diagrams Detected: {validation_result.diagrams_found}",
            f"Violations: {len(validation_result.violations)}",
            ""
        ]

        # Add traceability info if available
        if self.ddr_core:
            lines.append("Traceability Status: Connected to DDR Core")
        else:
            lines.append("Traceability Status: Limited (DDR Core not installed)")

        lines.append("")
        lines.append("=" * 70)

        return "\n".join(lines)

    def check_tier_consistency(
        self,
        document_path: Path
    ) -> Dict[str, any]:
        """
        Verify document is in correct tier directory.

        Ensures SAD documents are in docs/04_sad/ per DDR structure.

        Parameters
        ----------
        document_path : Path
            Document path to check.

        Returns
        -------
        Dict[str, any]
            Consistency check results.

        Examples
        --------
        >>> check = bridge.check_tier_consistency(Path('docs/04_sad/arch.rst'))
        >>> check['is_consistent']
        True
        """
        expected_tier = "04_sad"

        is_consistent = expected_tier in document_path.parts

        if not is_consistent:
            suggested_path = document_path.parent.parent / expected_tier / document_path.name
        else:
            suggested_path = None

        return {
            "is_consistent": is_consistent,
            "expected_tier": expected_tier,
            "actual_path": str(document_path),
            "suggested_path": str(suggested_path) if suggested_path else None
        }

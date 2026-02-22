"""
Contextual validation for DDR tier classifications.

Implements Step 5 from classification-scoring.md: semantic validation,
parent availability checks, and downstream feasibility verification.
"""

from typing import Dict, List, Tuple
from enum import Enum

from .scoring_matrix import FactorPresence


class Tier(Enum):
    """DDR tier enumeration."""
    BRD = "BRD"
    NFR = "NFR"
    FSD = "FSD"
    SAD = "SAD"
    ICD = "ICD"
    TDD = "TDD"
    ISP = "ISP"


class ContextualValidator:
    """
    Performs contextual validation on proposed tier assignments.

    Validates that:
    1. Assignment makes semantic sense for the tier
    2. Parent tier availability (can it cite required parents?)
    3. Downstream design decisions are enabled

    Implements: classification-scoring.md Step 5

    Examples
    --------
    >>> validator = ContextualValidator()
    >>> passed, notes = validator.validate(
    ...     Tier.NFR,
    ...     "System must have < 1s latency",
    ...     factors,
    ...     {'existing_brd_tags': ['BRD-8']}
    ... )
    >>> print(passed)
    True
    """

    def __init__(self):
        """Initialize validator with tier-specific rules."""
        self.tier_requirements = self._load_tier_requirements()

    def validate(
        self,
        assigned_tier: Tier,
        fragment: str,
        factors: Dict[str, FactorPresence],
        context: Dict
    ) -> Tuple[bool, List[str]]:
        """
        Perform contextual validation on tier assignment.

        Parameters
        ----------
        assigned_tier : Tier
            Proposed tier assignment.
        fragment : str
            Original information fragment.
        factors : Dict[str, FactorPresence]
            Detected factors from scoring.
        context : Dict
            Validation context:
            - existing_brd_tags: Available BRD tags
            - existing_nfr_tags: Available NFR tags
            - project_domain: Project domain

        Returns
        -------
        Tuple[bool, List[str]]
            (Validation passed, Validation notes/warnings)
        """
        notes = []
        passed = True

        # Semantic validation
        semantic_ok, semantic_notes = self._validate_semantic_fit(
            assigned_tier, fragment, factors
        )
        notes.extend(semantic_notes)
        if not semantic_ok:
            passed = False

        # Parent availability check
        parent_ok, parent_notes = self._validate_parent_availability(
            assigned_tier, context
        )
        notes.extend(parent_notes)
        if not parent_ok:
            passed = False

        # Downstream feasibility
        downstream_ok, downstream_notes = self._validate_downstream_feasibility(
            assigned_tier, fragment, factors
        )
        notes.extend(downstream_notes)
        if not downstream_ok:
            # Downgrade to warning only
            notes.append("WARNING: Limited downstream design enablement")

        if passed and not notes:
            notes.append("All validation checks passed")

        return passed, notes

    def _validate_semantic_fit(
        self,
        tier: Tier,
        fragment: str,
        factors: Dict[str, FactorPresence]
    ) -> Tuple[bool, List[str]]:
        """
        Validate that fragment semantically matches tier's purpose.

        Parameters
        ----------
        tier : Tier
            Proposed tier.
        fragment : str
            Information fragment.
        factors : Dict[str, FactorPresence]
            Detected factors.

        Returns
        -------
        Tuple[bool, List[str]]
            (Semantic fit OK, Notes)
        """
        notes = []

        if tier == Tier.BRD:
            # BRD should be technology-agnostic
            if factors['technology_agnostic'] == FactorPresence.NONE:
                notes.append(
                    "WARNING: BRD should be technology-agnostic, "
                    "but specific technologies detected"
                )
                return False, notes

            # BRD should include rationale
            if factors['includes_rationale'] == FactorPresence.NONE:
                notes.append(
                    "NOTE: BRD content typically includes business rationale"
                )

        elif tier == Tier.NFR:
            # NFR should have numeric metrics
            if factors['numeric_metrics'] == FactorPresence.NONE:
                notes.append(
                    "WARNING: NFR should include specific numeric constraints"
                )
                return False, notes

        elif tier == Tier.FSD:
            # FSD should NOT have implementation details
            if factors['executable_code'] != FactorPresence.NONE:
                notes.append(
                    "ERROR: FSD must not contain executable code"
                )
                return False, notes

            if factors['class_names'] != FactorPresence.NONE:
                notes.append(
                    "WARNING: FSD should not reference specific class names"
                )

        elif tier == Tier.SAD:
            # SAD should name patterns
            if factors['pattern_names'] == FactorPresence.NONE:
                notes.append(
                    "NOTE: SAD typically names architectural patterns"
                )

        elif tier == Tier.ICD:
            # ICD should define schemas
            if factors['schema_definition'] == FactorPresence.NONE:
                notes.append(
                    "WARNING: ICD should define data schemas or contracts"
                )
                return False, notes

        elif tier == Tier.TDD:
            # TDD should have class names
            if factors['class_names'] == FactorPresence.NONE:
                notes.append(
                    "NOTE: TDD typically specifies class/component names"
                )

        elif tier == Tier.ISP:
            # ISP should have executable code
            if factors['executable_code'] == FactorPresence.NONE:
                notes.append(
                    "WARNING: ISP should contain code stubs"
                )
                return False, notes

        if not notes:
            notes.append(f"Semantic fit for {tier.value} validated")

        return True, notes

    def _validate_parent_availability(
        self,
        tier: Tier,
        context: Dict
    ) -> Tuple[bool, List[str]]:
        """
        Check if required parent tags exist for citation.

        Parameters
        ----------
        tier : Tier
            Proposed tier.
        context : Dict
            Context with existing_*_tags lists.

        Returns
        -------
        Tuple[bool, List[str]]
            (Parents available, Notes)
        """
        notes = []

        # BRD has no parent requirement
        if tier == Tier.BRD:
            notes.append("BRD is root tier (no parent required)")
            return True, notes

        # Check for required parents
        required_parents = self._get_required_parent_tiers(tier)

        for parent_tier in required_parents:
            context_key = f'existing_{parent_tier.lower()}_tags'
            if context_key in context:
                available = context[context_key]
                if not available:
                    notes.append(
                        f"WARNING: No {parent_tier} tags available for citation"
                    )
                    return False, notes
                else:
                    notes.append(
                        f"Parent {parent_tier} tags available for citation: "
                        f"{len(available)} tags"
                    )
            else:
                notes.append(
                    f"NOTE: Parent {parent_tier} tag availability not provided"
                )

        return True, notes

    def _validate_downstream_feasibility(
        self,
        tier: Tier,
        fragment: str,
        factors: Dict[str, FactorPresence]
    ) -> Tuple[bool, List[str]]:
        """
        Verify that classification enables downstream design decisions.

        Parameters
        ----------
        tier : Tier
            Proposed tier.
        fragment : str
            Information fragment.
        factors : Dict[str, FactorPresence]
            Detected factors.

        Returns
        -------
        Tuple[bool, List[str]]
            (Enables downstream, Notes)
        """
        notes = []

        # Check if fragment provides enough specificity for child tiers
        if tier == Tier.BRD:
            # BRD should enable NFR/FSD derivation
            if factors['numeric_metrics'] == FactorPresence.NONE:
                notes.append(
                    "NOTE: Consider adding measurable success criteria "
                    "for NFR derivation"
                )

        elif tier == Tier.NFR:
            # NFR should enable FSD feature specs
            notes.append("NFR constraints can guide FSD feature specifications")

        elif tier == Tier.FSD:
            # FSD should enable SAD architecture
            if factors['user_behavior'] != FactorPresence.NONE:
                notes.append("FSD behavior enables SAD architectural decisions")
            else:
                notes.append(
                    "NOTE: Limited behavioral context may constrain SAD options"
                )

        elif tier == Tier.SAD:
            # SAD should enable ICD/TDD
            if factors['pattern_names'] != FactorPresence.NONE:
                notes.append("SAD patterns enable ICD contract definitions")
            else:
                notes.append(
                    "NOTE: Consider adding pattern names for clearer TDD guidance"
                )

        elif tier == Tier.ICD:
            # ICD should enable TDD class design
            if factors['schema_definition'] != FactorPresence.NONE:
                notes.append("ICD schemas enable TDD class structure")

        elif tier == Tier.TDD:
            # TDD should enable ISP stub generation
            if factors['class_names'] != FactorPresence.NONE:
                notes.append("TDD class names enable ISP stub generation")

        # ISP is terminal tier
        if tier == Tier.ISP:
            notes.append("ISP is terminal tier (no downstream)")

        return True, notes

    def _get_required_parent_tiers(self, tier: Tier) -> List[str]:
        """
        Get list of required parent tiers for citation.

        Parameters
        ----------
        tier : Tier
            Target tier.

        Returns
        -------
        List[str]
            Required parent tier names.
        """
        parent_map = {
            Tier.BRD: [],
            Tier.NFR: ['BRD'],
            Tier.FSD: ['BRD', 'NFR'],
            Tier.SAD: ['FSD'],
            Tier.ICD: ['SAD', 'NFR'],
            Tier.TDD: ['SAD', 'ICD'],
            Tier.ISP: ['TDD']
        }

        return parent_map.get(tier, [])

    def _load_tier_requirements(self) -> Dict:
        """
        Load tier-specific validation requirements.

        Returns
        -------
        Dict
            Tier validation rules.
        """
        return {
            'BRD': {
                'must_be_agnostic': True,
                'must_have_rationale': True,
                'must_have_metrics': True
            },
            'NFR': {
                'must_have_numeric': True,
                'must_cite_brd': True
            },
            'FSD': {
                'no_implementation': True,
                'no_code': True
            },
            'SAD': {
                'should_name_patterns': True,
                'should_have_diagram': True
            },
            'ICD': {
                'must_define_schema': True
            },
            'TDD': {
                'should_name_classes': True,
                'no_logic': True
            },
            'ISP': {
                'must_have_code': True,
                'must_be_stub': True
            }
        }

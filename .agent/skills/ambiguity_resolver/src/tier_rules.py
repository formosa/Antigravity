"""
DDR tier hierarchy and precedence rules.

Implements abstraction ordering and tie-breaker logic from
classification_scoring.md Step 4.
"""

from typing import List
from enum import Enum


class Tier(Enum):
    """DDR tier enumeration in abstraction order (high to low)."""
    BRD = "BRD"
    NFR = "NFR"
    FSD = "FSD"
    SAD = "SAD"
    ICD = "ICD"
    TDD = "TDD"
    ISP = "ISP"


class TierHierarchy:
    """
    DDR tier hierarchy with abstraction ordering and validation rules.

    Implements:
    - Abstraction precedence (BRD > NFR > ... > ISP)
    - Valid parent-child relationships
    - Tie-breaker selection logic

    Attributes
    ----------
    abstraction_order : List[Tier]
        Tiers ordered from highest to lowest abstraction.
    valid_citations : Dict[Tier, List[Tier]]
        Valid parent tiers each tier can cite.

    Examples
    --------
    >>> hierarchy = TierHierarchy()
    >>> winner = hierarchy.select_highest_abstraction([Tier.NFR, Tier.FSD])
    >>> print(winner)
    Tier.NFR
    """

    def __init__(self):
        """Initialize tier hierarchy rules."""
        # Abstraction order: leftward = higher abstraction
        self.abstraction_order = [
            Tier.BRD,
            Tier.NFR,
            Tier.FSD,
            Tier.SAD,
            Tier.ICD,
            Tier.TDD,
            Tier.ISP
        ]

        # Valid parent citations per tier (from tier_hierarchy.md)
        self.valid_citations = {
            Tier.BRD: [],  # Root authority
            Tier.NFR: [Tier.BRD],
            Tier.FSD: [Tier.BRD, Tier.NFR],
            Tier.SAD: [Tier.FSD],
            Tier.ICD: [Tier.SAD, Tier.NFR],
            Tier.TDD: [Tier.SAD, Tier.ICD],
            Tier.ISP: [Tier.TDD]
        }

        # Tier characteristics for validation
        self.tier_characteristics = {
            Tier.BRD: {
                'layer': 'Context',
                'question': 'Why build it?',
                'persona': 'Strategist',
                'technology_agnostic': True,
                'requires_metrics': True
            },
            Tier.NFR: {
                'layer': 'Boundaries',
                'question': 'What limits?',
                'persona': 'SysAdmin',
                'requires_numeric': True,
                'uses_rfc2119': True
            },
            Tier.FSD: {
                'layer': 'Behavior',
                'question': 'What does it?',
                'persona': 'Product Owner',
                'no_implementation': True,
                'user_focused': True
            },
            Tier.SAD: {
                'layer': 'Structure',
                'question': 'How organize?',
                'persona': 'Architect',
                'requires_diagram': True,
                'names_patterns': True
            },
            Tier.ICD: {
                'layer': 'Contracts',
                'question': 'What shape?',
                'persona': 'Data Engineer',
                'defines_schemas': True,
                'uses_json_yaml': True
            },
            Tier.TDD: {
                'layer': 'Blueprints',
                'question': 'What classes?',
                'persona': 'Lead Developer',
                'names_classes': True,
                'no_logic': True
            },
            Tier.ISP: {
                'layer': 'Prompts',
                'question': 'What stubs?',
                'persona': 'Code Generator',
                'has_code': True,
                'stub_only': True
            }
        }

    def select_highest_abstraction(self, candidates: List[Tier]) -> Tier:
        """
        Select tier with highest abstraction from candidates.

        Implements tie-breaker rule: BRD > NFR > FSD > SAD > ICD > TDD > ISP

        Parameters
        ----------
        candidates : List[Tier]
            Tied tier candidates.

        Returns
        -------
        Tier
            Highest abstraction tier.

        Examples
        --------
        >>> hierarchy = TierHierarchy()
        >>> winner = hierarchy.select_highest_abstraction([Tier.ICD, Tier.NFR])
        >>> print(winner.value)
        'NFR'
        """
        if not candidates:
            return Tier.BRD  # Default to highest

        # Find leftmost (highest abstraction) tier in candidates
        for tier in self.abstraction_order:
            if tier in candidates:
                return tier

        return candidates[0]  # Fallback

    def get_abstraction_level(self, tier: Tier) -> int:
        """
        Get numeric abstraction level (0=highest, 6=lowest).

        Parameters
        ----------
        tier : Tier
            Target tier.

        Returns
        -------
        int
            Abstraction level (0-6).
        """
        return self.abstraction_order.index(tier)

    def is_valid_parent(self, child: Tier, parent: Tier) -> bool:
        """
        Check if parent tier is valid citation for child tier.

        Parameters
        ----------
        child : Tier
            Child tier attempting citation.
        parent : Tier
            Proposed parent tier.

        Returns
        -------
        bool
            True if citation is valid.

        Examples
        --------
        >>> hierarchy = TierHierarchy()
        >>> hierarchy.is_valid_parent(Tier.TDD, Tier.SAD)
        True
        >>> hierarchy.is_valid_parent(Tier.TDD, Tier.ISP)
        False
        """
        valid_parents = self.valid_citations.get(child, [])
        return parent in valid_parents

    def get_valid_parents(self, tier: Tier) -> List[Tier]:
        """
        Get all valid parent tiers for citation.

        Parameters
        ----------
        tier : Tier
            Target tier.

        Returns
        -------
        List[Tier]
            Valid parent tiers.
        """
        return self.valid_citations.get(tier, [])

    def get_characteristics(self, tier: Tier) -> dict:
        """
        Get tier characteristics for validation.

        Parameters
        ----------
        tier : Tier
            Target tier.

        Returns
        -------
        dict
            Tier characteristics.
        """
        return self.tier_characteristics.get(tier, {})

    def compare_abstraction(self, tier1: Tier, tier2: Tier) -> int:
        """
        Compare abstraction levels of two tiers.

        Parameters
        ----------
        tier1 : Tier
            First tier.
        tier2 : Tier
            Second tier.

        Returns
        -------
        int
            -1 if tier1 > tier2 (higher abstraction)
             0 if tier1 == tier2
             1 if tier1 < tier2 (lower abstraction)
        """
        level1 = self.get_abstraction_level(tier1)
        level2 = self.get_abstraction_level(tier2)

        if level1 < level2:
            return -1
        elif level1 > level2:
            return 1
        else:
            return 0

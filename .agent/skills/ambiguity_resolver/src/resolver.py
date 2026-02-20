"""
Core ambiguity resolution logic for DDR tier classification.

This module implements the multi-factor scoring protocol that resolves
ambiguous tier classifications when the decision tree yields multiple
candidate tiers.
"""

import logging
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from .scoring_matrix import ScoringMatrix, FactorPresence
from .validators import ContextualValidator
from .tier_rules import TierHierarchy
from .utils import load_config, format_rst_output


logger = logging.getLogger(__name__)


class Tier(Enum):
    """DDR tier enumeration in abstraction order."""
    BRD = "BRD"
    NFR = "NFR"
    FSD = "FSD"
    SAD = "SAD"
    ICD = "ICD"
    TDD = "TDD"
    ISP = "ISP"


@dataclass
class ClassificationResult:
    """
    Result of ambiguity resolution.

    Attributes
    ----------
    assigned_tier : Tier
        Final tier assignment.
    confidence : float
        Confidence score (0-1).
    scores : Dict[Tier, int]
        Raw scores for all tiers.
    factors_detected : Dict[str, FactorPresence]
        Detected factors and their presence levels.
    tie_breaker_applied : bool
        Whether tie-breaker rule was needed.
    validation_passed : bool
        Whether contextual validation passed.
    validation_notes : List[str]
        Validation observations and warnings.
    reasoning : str
        Human-readable explanation of classification.
    """
    assigned_tier: Tier
    confidence: float
    scores: Dict[Tier, int]
    factors_detected: Dict[str, FactorPresence]
    tie_breaker_applied: bool
    validation_passed: bool
    validation_notes: List[str]
    reasoning: str


class AmbiguityResolver:
    """
    Resolves ambiguous DDR tier classifications using multi-factor scoring.

    Implements the scoring protocol from classification_scoring.md with
    tie-breaker rules and contextual validation.

    Parameters
    ----------
    config_path : str
        Path to scoring weights configuration.
    enable_validation : bool, optional
        Enable contextual validation (default: True).

    Attributes
    ----------
    scoring_matrix : ScoringMatrix
        10-factor scoring matrix implementation.
    validator : ContextualValidator
        Contextual validation engine.
    hierarchy : TierHierarchy
        Tier precedence and rules.

    Examples
    --------
    >>> resolver = AmbiguityResolver()
    >>> fragment = "System must aggregate logs to single file with 50MB rotation"
    >>> result = resolver.resolve(fragment, candidate_tiers=[Tier.NFR, Tier.ICD])
    >>> print(result.assigned_tier)
    Tier.NFR
    """

    def __init__(
        self,
        config_path: str = "config/scoring_weights.yaml",
        enable_validation: bool = True
    ):
        """
        Initialize resolver with configuration.

        Implements: Protocol from classification_scoring.md
        """
        self.config = load_config(config_path)
        self.scoring_matrix = ScoringMatrix(self.config['weights'])
        self.validator = ContextualValidator() if enable_validation else None
        self.hierarchy = TierHierarchy()

        logger.info(
            f"AmbiguityResolver initialized with validation={'enabled' if enable_validation else 'disabled'}"
        )

    def resolve(
        self,
        fragment: str,
        candidate_tiers: Optional[List[Tier]] = None,
        context: Optional[Dict] = None
    ) -> ClassificationResult:
        """
        Resolve ambiguous tier classification for information fragment.

        Implements the complete scoring protocol:
        1. Score each factor (Step 1)
        2. Calculate tier scores (Step 2)
        3. Sum and compare (Step 3)
        4. Apply tie-breaker (Step 4)
        5. Contextual validation (Step 5)

        Parameters
        ----------
        fragment : str
            Information fragment to classify.
        candidate_tiers : List[Tier], optional
            Pre-identified candidate tiers from decision tree.
            If None, considers all tiers.
        context : Dict, optional
            Additional context for validation:
            - existing_brd_tags: Available BRD tags for citation
            - project_domain: Project domain context

        Returns
        -------
        ClassificationResult
            Complete classification with reasoning.

        Requirements
        ------------
        |classification_scoring.md| - Multi-factor scoring protocol
        """
        logger.info(f"Resolving ambiguity for fragment (length={len(fragment)})")

        # Step 1: Score each factor
        factors_detected = self.scoring_matrix.analyze_fragment(fragment)

        # Step 2 & 3: Calculate tier scores
        scores = self._calculate_tier_scores(
            factors_detected,
            candidate_tiers or list(Tier)
        )

        logger.debug(f"Tier scores: {scores}")

        # Step 4: Apply tie-breaker if needed
        assigned_tier, tie_breaker_applied = self._select_tier(scores)

        # Step 5: Contextual validation
        validation_passed, validation_notes = self._validate_assignment(
            assigned_tier,
            fragment,
            factors_detected,
            context or {}
        )

        # Calculate confidence
        confidence = self._calculate_confidence(
            scores,
            assigned_tier,
            validation_passed
        )

        # Generate reasoning
        reasoning = self._generate_reasoning(
            fragment,
            scores,
            factors_detected,
            assigned_tier,
            tie_breaker_applied,
            validation_notes
        )

        result = ClassificationResult(
            assigned_tier=assigned_tier,
            confidence=confidence,
            scores=scores,
            factors_detected=factors_detected,
            tie_breaker_applied=tie_breaker_applied,
            validation_passed=validation_passed,
            validation_notes=validation_notes,
            reasoning=reasoning
        )

        logger.info(
            f"Classification complete: {assigned_tier.value} "
            f"(confidence={confidence:.2f})"
        )

        return result

    def _calculate_tier_scores(
        self,
        factors: Dict[str, FactorPresence],
        candidate_tiers: List[Tier]
    ) -> Dict[Tier, int]:
        """
        Calculate total score for each tier based on detected factors.

        Implements: classification_scoring.md Step 2

        Parameters
        ----------
        factors : Dict[str, FactorPresence]
            Detected factors and their presence levels.
        candidate_tiers : List[Tier]
            Tiers to score (filters computation).

        Returns
        -------
        Dict[Tier, int]
            Total score per tier.
        """
        scores = {tier: 0 for tier in candidate_tiers}

        for factor_name, presence in factors.items():
            if presence == FactorPresence.NONE:
                continue

            # Get factor weights for each tier
            factor_weights = self.scoring_matrix.get_weights(factor_name)

            for tier in candidate_tiers:
                if tier in factor_weights:
                    weight = factor_weights[tier]

                    # Scale weight by presence level
                    if presence == FactorPresence.PARTIAL:
                        weight = int(weight * 0.5)

                    scores[tier] += weight

        return scores

    def _select_tier(
        self,
        scores: Dict[Tier, int]
    ) -> Tuple[Tier, bool]:
        """
        Select winning tier, applying tie-breaker if needed.

        Implements: classification_scoring.md Step 4
        Tie-breaker: Higher abstraction (leftward in hierarchy)

        Parameters
        ----------
        scores : Dict[Tier, int]
            Calculated tier scores.

        Returns
        -------
        Tuple[Tier, bool]
            (Selected tier, Whether tie-breaker was applied)
        """
        if not scores:
            logger.warning("No scores provided, defaulting to BRD")
            return Tier.BRD, False

        max_score = max(scores.values())
        winners = [tier for tier, score in scores.items() if score == max_score]

        if len(winners) == 1:
            return winners[0], False

        # Tie-breaker: Select highest abstraction (leftward)
        logger.info(f"Tie detected among: {[t.value for t in winners]}")
        selected = self.hierarchy.select_highest_abstraction(winners)

        return selected, True

    def _validate_assignment(
        self,
        assigned_tier: Tier,
        fragment: str,
        factors: Dict[str, FactorPresence],
        context: Dict
    ) -> Tuple[bool, List[str]]:
        """
        Perform contextual validation on tier assignment.

        Implements: classification_scoring.md Step 5

        Parameters
        ----------
        assigned_tier : Tier
            Proposed tier assignment.
        fragment : str
            Original information fragment.
        factors : Dict[str, FactorPresence]
            Detected factors.
        context : Dict
            Additional context for validation.

        Returns
        -------
        Tuple[bool, List[str]]
            (Validation passed, Validation notes)
        """
        if not self.validator:
            return True, ["Validation disabled"]

        return self.validator.validate(
            assigned_tier,
            fragment,
            factors,
            context
        )

    def _calculate_confidence(
        self,
        scores: Dict[Tier, int],
        assigned_tier: Tier,
        validation_passed: bool
    ) -> float:
        """
        Calculate confidence score (0-1) for classification.

        Confidence factors:
        - Score margin (higher is better)
        - Absolute score (higher is better)
        - Validation result (passed adds confidence)

        Parameters
        ----------
        scores : Dict[Tier, int]
            All tier scores.
        assigned_tier : Tier
            Selected tier.
        validation_passed : bool
            Whether contextual validation passed.

        Returns
        -------
        float
            Confidence score (0-1).
        """
        assigned_score = scores[assigned_tier]
        total_possible = len(self.scoring_matrix.factors) * 3  # Max weight per factor

        # Base confidence from score ratio
        base_confidence = min(assigned_score / total_possible, 1.0)

        # Margin bonus: difference between winner and runner-up
        sorted_scores = sorted(scores.values(), reverse=True)
        if len(sorted_scores) > 1:
            margin = sorted_scores[0] - sorted_scores[1]
            margin_bonus = min(margin / 10.0, 0.2)  # Up to +0.2
        else:
            margin_bonus = 0.2

        # Validation bonus
        validation_bonus = 0.1 if validation_passed else -0.15

        confidence = min(max(base_confidence + margin_bonus + validation_bonus, 0.0), 1.0)

        return round(confidence, 3)

    def _generate_reasoning(
        self,
        fragment: str,
        scores: Dict[Tier, int],
        factors: Dict[str, FactorPresence],
        assigned_tier: Tier,
        tie_breaker_applied: bool,
        validation_notes: List[str]
    ) -> str:
        """
        Generate human-readable explanation of classification decision.

        Parameters
        ----------
        fragment : str
            Original fragment.
        scores : Dict[Tier, int]
            All tier scores.
        factors : Dict[str, FactorPresence]
            Detected factors.
        assigned_tier : Tier
            Final assignment.
        tie_breaker_applied : bool
            Whether tie-breaker was used.
        validation_notes : List[str]
            Validation observations.

        Returns
        -------
        str
            Formatted reasoning explanation.
        """
        lines = []
        lines.append(f"FRAGMENT: \"{fragment[:100]}...\"" if len(fragment) > 100 else f"FRAGMENT: \"{fragment}\"")
        lines.append("")

        lines.append("FACTORS DETECTED:")
        for factor_name, presence in factors.items():
            if presence != FactorPresence.NONE:
                lines.append(f"  - {factor_name}: {presence.value}")
        lines.append("")

        lines.append("TIER SCORES:")
        sorted_tiers = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        for tier, score in sorted_tiers:
            marker = "← SELECTED" if tier == assigned_tier else ""
            lines.append(f"  {tier.value}: {score} {marker}")
        lines.append("")

        if tie_breaker_applied:
            lines.append("TIE-BREAKER: Higher abstraction rule applied")
            lines.append("")

        lines.append("VALIDATION:")
        for note in validation_notes:
            lines.append(f"  - {note}")
        lines.append("")

        lines.append(f"FINAL ASSIGNMENT: {assigned_tier.value}")

        return "\n".join(lines)

    def resolve_batch(
        self,
        fragments: List[str],
        context: Optional[Dict] = None
    ) -> List[ClassificationResult]:
        """
        Resolve multiple fragments in batch.

        Parameters
        ----------
        fragments : List[str]
            Multiple fragments to classify.
        context : Dict, optional
            Shared context for all fragments.

        Returns
        -------
        List[ClassificationResult]
            Classification results for each fragment.
        """
        results = []
        for i, fragment in enumerate(fragments):
            logger.info(f"Processing fragment {i+1}/{len(fragments)}")
            result = self.resolve(fragment, context=context)
            results.append(result)

        return results


def resolve_ambiguity(
    fragment: str,
    candidate_tiers: Optional[List[str]] = None,
    context: Optional[Dict] = None,
    output_format: str = "detailed"
) -> Dict:
    """
    Main entry point for ambiguity resolution (Antigravity IDE integration).

    Parameters
    ----------
    fragment : str
        Information fragment to classify.
    candidate_tiers : List[str], optional
        Pre-identified candidate tiers (e.g., ["NFR", "ICD"]).
    context : Dict, optional
        Additional context for validation.
    output_format : str, optional
        Output format: "detailed", "summary", or "rst_directive".

    Returns
    -------
    Dict
        Classification result in requested format.

    Examples
    --------
    >>> result = resolve_ambiguity(
    ...     "System must aggregate logs to single file with 50MB rotation",
    ...     candidate_tiers=["NFR", "ICD"]
    ... )
    >>> print(result['assigned_tier'])
    'NFR'
    """
    resolver = AmbiguityResolver()

    # Convert string tier names to Tier enum
    tier_candidates = None
    if candidate_tiers:
        tier_candidates = [Tier[t] for t in candidate_tiers]

    result = resolver.resolve(fragment, tier_candidates, context)

    # Format output
    if output_format == "summary":
        return {
            'assigned_tier': result.assigned_tier.value,
            'confidence': result.confidence,
            'validation_passed': result.validation_passed
        }
    elif output_format == "rst_directive":
        return {
            'assigned_tier': result.assigned_tier.value,
            'rst_output': format_rst_output(result)
        }
    else:  # detailed
        return {
            'assigned_tier': result.assigned_tier.value,
            'confidence': result.confidence,
            'scores': {t.value: s for t, s in result.scores.items()},
            'factors_detected': {k: v.value for k, v in result.factors_detected.items()},
            'tie_breaker_applied': result.tie_breaker_applied,
            'validation_passed': result.validation_passed,
            'validation_notes': result.validation_notes,
            'reasoning': result.reasoning
        }

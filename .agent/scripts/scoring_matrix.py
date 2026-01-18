"""
Scoring Matrix Tool.

Resolves ambiguous tier classification using multi-factor weighted scoring.

Meta
----
Tool Definition : .agent/tools/ddr_scoring_matrix.md
Knowledge Source: .agent/knowledge/sources/protocols/classification_scoring.md
Architect       : Antigravity IDE

Usage
-----
    python scoring_matrix.py --fragment "Text to score" --candidates "FSD,SAD"

Exit Codes
----------
0 : Success (JSON result printed to stdout)
1 : Error (Details printed to stderr)
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from typing import Optional


@dataclass
class ScoringResult:
    """Result of scoring matrix resolution."""
    winner: str
    scores: dict[str, float]
    justification: str
    tie_broken: bool = False
    factors_matched: list[str] = None


# Scoring matrix from classification_scoring.md §Step 1 — VERIFIED
# Factor weights per tier (0-3 scale)
SCORING_MATRIX: dict[str, dict[str, int]] = {
    "numeric_metrics": {
        "description": "Contains numeric metrics (percentages, times, counts)",
        "patterns": [r"\b\d+\s*(?:ms|seconds?|minutes?|hours?|%|MB|GB|KB)\b", r"\b(?:\d+\.?\d*)\s*(?:requests?|calls?)/sec"],
        "keywords": ["threshold", "limit", "maximum", "minimum", "within", "at least"],
        "BRD": 1, "NFR": 3, "FSD": 1, "SAD": 0, "ICD": 2, "TDD": 0, "ISP": 0
    },
    "hardware_reference": {
        "description": "References hardware specifications",
        "patterns": [r"\b(?:cpu|gpu|ram|memory|disk|network)\b", r"\b(?:nvidia|intel|amd)\b"],
        "keywords": ["hardware", "processor", "core", "thread", "bandwidth", "storage"],
        "BRD": 1, "NFR": 3, "FSD": 0, "SAD": 1, "ICD": 0, "TDD": 0, "ISP": 0
    },
    "user_behavior": {
        "description": "Describes user behavior or interactions",
        "patterns": [r"\buser\s+(?:can|shall|should|will|must)\b", r"\bwhen\s+(?:the\s+)?user\b"],
        "keywords": ["user", "click", "interact", "navigate", "input", "view", "display"],
        "BRD": 2, "NFR": 0, "FSD": 3, "SAD": 0, "ICD": 0, "TDD": 0, "ISP": 0
    },
    "pattern_naming": {
        "description": "Names architectural or design patterns",
        "patterns": [r"\b(?:pattern|architecture)\s+\w+\b", r"\b(?:microservice|monolith|layered|event.driven)\b"],
        "keywords": ["pattern", "topology", "architecture", "component", "layer", "service"],
        "BRD": 0, "NFR": 0, "FSD": 0, "SAD": 3, "ICD": 0, "TDD": 1, "ISP": 0
    },
    "schema_definition": {
        "description": "Defines JSON, YAML, or data schemas",
        "patterns": [r"\bjson\s+schema\b", r"\bapi\s+(?:endpoint|contract)\b", r"\{\s*\""],
        "keywords": ["json", "yaml", "xml", "schema", "field", "type", "format", "payload"],
        "BRD": 0, "NFR": 0, "FSD": 0, "SAD": 0, "ICD": 3, "TDD": 0, "ISP": 1
    },
    "class_names": {
        "description": "Contains class or method names",
        "patterns": [r"\bclass\s+[A-Z]\w+\b", r"\bdef\s+\w+\(", r"\bmethod\s+\w+\b"],
        "keywords": ["class", "method", "function", "constructor", "attribute", "property"],
        "BRD": 0, "NFR": 0, "FSD": 0, "SAD": 0, "ICD": 0, "TDD": 3, "ISP": 2
    },
    "executable_code": {
        "description": "Contains executable code snippets",
        "patterns": [r"\bif\s+\w+\s*[=<>!]+", r"\breturn\s+\w+", r"\bfor\s+\w+\s+in\b"],
        "keywords": ["return", "if", "else", "for", "while", "import", "def", "class"],
        "BRD": 0, "NFR": 0, "FSD": 0, "SAD": 0, "ICD": 0, "TDD": 0, "ISP": 3
    },
    "must_shall_modality": {
        "description": "Uses 'must' or 'shall' modal verbs",
        "patterns": [r"\b(?:must|shall)\s+(?:not\s+)?(?:\w+)\b"],
        "keywords": ["must", "shall", "required", "mandatory"],
        "BRD": 2, "NFR": 3, "FSD": 2, "SAD": 1, "ICD": 1, "TDD": 1, "ISP": 0
    },
    "includes_rationale": {
        "description": "Includes reasoning or justification",
        "patterns": [r"\bbecause\s+\w+", r"\bin\s+order\s+to\b", r"\bso\s+that\b"],
        "keywords": ["because", "therefore", "rationale", "reason", "justification", "why"],
        "BRD": 3, "NFR": 1, "FSD": 1, "SAD": 3, "ICD": 0, "TDD": 2, "ISP": 0
    },
    "technology_agnostic": {
        "description": "Technology-agnostic language",
        "patterns": [r"\b(?:any|all|generic|agnostic)\s+(?:system|platform|technology)\b"],
        "keywords": ["agnostic", "independent", "portable", "standard", "interoperable"],
        "BRD": 3, "NFR": 1, "FSD": 2, "SAD": 0, "ICD": 0, "TDD": 0, "ISP": 0
    }
}

# Tier hierarchy for tie-breaking (higher index = higher abstraction)
TIER_PRECEDENCE = ["ISP", "TDD", "ICD", "SAD", "FSD", "NFR", "BRD"]
VALID_TIERS = ["BRD", "NFR", "FSD", "SAD", "ICD", "TDD", "ISP"]


def evaluate_factor(text: str, factor_key: str) -> tuple[bool, list[str]]:
    """
    Evaluate whether a factor is present in the text.

    Parameters
    ----------
    text : str
        The text fragment to analyze.
    factor_key : str
        The factor key from SCORING_MATRIX.

    Returns
    -------
    tuple[bool, list[str]]
        Whether factor is present and which indicators matched.
    """
    factor = SCORING_MATRIX[factor_key]
    text_lower = text.lower()
    indicators = []

    # Check patterns
    for pattern in factor.get("patterns", []):
        if re.search(pattern, text_lower, re.IGNORECASE):
            indicators.append(f"pattern:{pattern[:25]}")

    # Check keywords
    for keyword in factor.get("keywords", []):
        if keyword in text_lower:
            indicators.append(f"keyword:{keyword}")

    return len(indicators) > 0, indicators


def score_fragment(text: str, candidates: list[str]) -> ScoringResult:
    """
    Apply scoring matrix to resolve ambiguous classification.

    Parameters
    ----------
    text : str
        The information fragment to score.
    candidates : list[str]
        List of candidate tier codes to compare.

    Returns
    -------
    ScoringResult
        Result with winner, all scores, and justification.
    """
    # Initialize scores for candidates
    scores: dict[str, float] = {tier: 0.0 for tier in candidates}
    factors_matched: list[str] = []

    # Evaluate each factor
    for factor_key, factor in SCORING_MATRIX.items():
        present, indicators = evaluate_factor(text, factor_key)

        if present:
            factors_matched.append(f"{factor_key}: {', '.join(indicators[:2])}")
            # Add weights for each candidate tier
            for tier in candidates:
                weight = factor.get(tier, 0)
                scores[tier] += weight

    # Find winner(s)
    max_score = max(scores.values())
    winners = [tier for tier, score in scores.items() if score == max_score]

    tie_broken = False
    if len(winners) > 1:
        # Apply tie-breaker: higher abstraction wins
        tie_broken = True
        winners.sort(key=lambda t: TIER_PRECEDENCE.index(t), reverse=True)

    winner = winners[0]

    justification = f"Scored {len(factors_matched)} factors. "
    if tie_broken:
        justification += f"Tie broken by abstraction precedence (favor higher). "
    justification += f"Winner: {winner} with {scores[winner]} points."

    return ScoringResult(
        winner=winner,
        scores=scores,
        justification=justification,
        tie_broken=tie_broken,
        factors_matched=factors_matched
    )


def main() -> int:
    """
    CLI entry point for scoring_matrix.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Resolve ambiguous tier classification using scoring matrix."
    )
    parser.add_argument(
        "--fragment",
        required=True,
        help="Information fragment to score"
    )
    parser.add_argument(
        "--candidates",
        required=True,
        help="Comma-separated list of candidate tiers (e.g., 'FSD,SAD')"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include detailed factor breakdown"
    )

    args = parser.parse_args()

    # Parse candidates
    candidates = [c.strip().upper() for c in args.candidates.split(",")]

    # Validate candidates
    invalid = [c for c in candidates if c not in VALID_TIERS]
    if invalid:
        print(f"Error: Invalid tier(s): {', '.join(invalid)}. "
              f"Valid tiers: {', '.join(VALID_TIERS)}", file=sys.stderr)
        return 1

    if len(candidates) < 2:
        print("Error: Need at least 2 candidate tiers for scoring matrix",
              file=sys.stderr)
        return 1

    try:
        result = score_fragment(args.fragment, candidates)

        output = {
            "winner": result.winner,
            "scores": {tier: round(score, 1) for tier, score in result.scores.items()},
            "justification": result.justification,
            "tie_broken": result.tie_broken
        }

        if args.verbose and result.factors_matched:
            output["factors_matched"] = result.factors_matched

        print(json.dumps(output, indent=2))
        return 0

    except Exception as e:
        print(f"Error scoring fragment: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

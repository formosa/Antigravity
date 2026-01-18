"""
Classify Information Tool.

Classifies unstructured information fragments into DDR tiers using the
decision tree algorithm from the classification protocol.

Meta
----
Tool Definition : .agent/tools/ddr_classify_information.md
Knowledge Source: .agent/knowledge/sources/protocols/classification_decision_tree.md
                  .agent/knowledge/sources/protocols/classification_scoring.md
Architect       : Antigravity IDE

Usage
-----
    python classify_information.py --input "Information text to classify"
    python classify_information.py --input "The system shall respond within 100ms"

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
class ClassificationResult:
    """Result of tier classification."""
    tier: str
    confidence: float
    rationale: str
    question_path: list[str]
    ambiguous: bool = False
    candidates: Optional[list[str]] = None


# Keywords and patterns for each decision question
CLASSIFICATION_PATTERNS: dict[str, dict] = {
    "Q1_WHY": {
        "tier": "BRD",
        "keywords": [
            "business value", "roi", "return on investment", "market",
            "strategic", "stakeholder", "customer need", "competitive",
            "revenue", "cost saving", "mission", "vision", "objective",
            "goal", "benefit", "value proposition", "business case",
            "priority", "scope", "success criteria", "kpi"
        ],
        "patterns": [
            r"\bwhy\s+(?:we|should|must|need)\b",
            r"\bbusiness\s+(?:need|requirement|objective)\b",
            r"\bstakeholder\b",
            r"\bstrategic\s+(?:goal|objective|initiative)\b"
        ],
        "question": "Does it answer WHY? (Business value, ROI, market need)"
    },
    "Q2_LIMITS": {
        "tier": "NFR",
        "keywords": [
            "performance", "latency", "throughput", "response time",
            "availability", "uptime", "reliability", "scalability",
            "security", "compliance", "sla", "constraint", "limit",
            "maximum", "minimum", "threshold", "capacity", "bandwidth",
            "memory", "cpu", "gpu", "hardware", "within", "less than",
            "at least", "no more than", "milliseconds", "seconds"
        ],
        "patterns": [
            r"\b(?:shall|must)\s+(?:not\s+)?(?:exceed|be\s+(?:less|greater|within))\b",
            r"\b\d+\s*(?:ms|seconds?|minutes?|hours?|%)\b",
            r"\b(?:99|99\.9|99\.99)%\s*(?:uptime|availability)\b",
            r"\bsla\b",
            r"\b(?:max|min|maximum|minimum)\s+\d+\b"
        ],
        "question": "Does it define LIMITS? (Performance, SLAs, constraints)"
    },
    "Q3_WHAT": {
        "tier": "FSD",
        "keywords": [
            "feature", "capability", "user", "shall", "function",
            "behavior", "interaction", "use case", "scenario",
            "workflow", "action", "input", "output", "display",
            "notify", "alert", "enable", "allow", "support",
            "provide", "when", "then", "given"
        ],
        "patterns": [
            r"\buser\s+(?:can|shall|should|must|will)\b",
            r"\bthe\s+system\s+(?:shall|should|must|will)\b",
            r"\bfeature\s*:\s*\w+\b",
            r"\buse\s+case\b",
            r"\bwhen\s+.+\s+then\b"
        ],
        "question": "Does it describe WHAT? (Features, capabilities, behaviors)"
    },
    "Q4_HOW": {
        "tier": "SAD",
        "keywords": [
            "architecture", "component", "module", "layer", "service",
            "pattern", "topology", "design", "structure", "subsystem",
            "orchestration", "integration", "communication", "process",
            "pipeline", "flow", "separation", "coupling", "cohesion",
            "dependency", "microservice", "monolith"
        ],
        "patterns": [
            r"\b(?:architecture|design)\s+pattern\b",
            r"\bcomponent\s+diagram\b",
            r"\b(?:layer|tier)ed\s+architecture\b",
            r"\b(?:service|module)\s+(?:boundary|interface)\b",
            r"\bprocess\s+(?:flow|topology)\b"
        ],
        "question": "Does it define HOW? (Patterns, topology, organization)"
    },
    "Q5_SCHEMA": {
        "tier": "ICD",
        "keywords": [
            "schema", "format", "json", "xml", "protobuf", "api",
            "endpoint", "request", "response", "payload", "message",
            "field", "type", "contract", "interface", "protocol",
            "header", "body", "parameter", "data model", "dto"
        ],
        "patterns": [
            r"\bapi\s+(?:endpoint|contract|spec)\b",
            r"\b(?:json|xml|protobuf)\s+schema\b",
            r"\brequest/response\b",
            r"\bdata\s+(?:format|structure|model)\b",
            r"\binterface\s+(?:contract|definition)\b"
        ],
        "question": "Does it define SCHEMA? (Data formats, contracts)"
    },
    "Q6_CLASS": {
        "tier": "TDD",
        "keywords": [
            "class", "method", "function", "attribute", "property",
            "inheritance", "implementation", "algorithm", "logic",
            "constructor", "destructor", "interface", "abstract",
            "concrete", "signature", "parameter", "return type",
            "exception", "private", "public", "protected"
        ],
        "patterns": [
            r"\bclass\s+\w+\b",
            r"\bmethod\s+signature\b",
            r"\b(?:implements|extends|inherits)\b",
            r"\bfunction\s+\w+\s*\(",
            r"\breturn\s+type\b"
        ],
        "question": "Does it specify CLASS structure? (Methods, dependencies)"
    }
}

# Final fallback tier
DEFAULT_TIER = "ISP"
DEFAULT_QUESTION = "Is it executable code skeleton? (Stub implementation)"


def calculate_score(text: str, question_key: str) -> tuple[float, list[str]]:
    """
    Calculate the match score for a classification question.

    Parameters
    ----------
    text : str
        The information fragment to analyze.
    question_key : str
        The key of the question in CLASSIFICATION_PATTERNS.

    Returns
    -------
    tuple[float, list[str]]
        Score (0.0-1.0) and list of matched terms.
    """
    config = CLASSIFICATION_PATTERNS[question_key]
    text_lower = text.lower()
    matched_terms = []

    # Check keywords
    for keyword in config["keywords"]:
        if keyword in text_lower:
            matched_terms.append(f"keyword:{keyword}")

    # Check patterns
    for pattern in config["patterns"]:
        if re.search(pattern, text_lower, re.IGNORECASE):
            matched_terms.append(f"pattern:{pattern[:30]}")

    # Calculate score based on matches
    keyword_weight = 0.6
    pattern_weight = 0.4

    keyword_score = min(1.0, len([m for m in matched_terms if m.startswith("keyword:")]) / 3)
    pattern_score = min(1.0, len([m for m in matched_terms if m.startswith("pattern:")]) / 2)

    total_score = (keyword_score * keyword_weight) + (pattern_score * pattern_weight)

    return total_score, matched_terms


def classify_information(text: str) -> ClassificationResult:
    """
    Classify an information fragment into a DDR tier.

    Implements the decision tree algorithm:
    Q1: WHY? → BRD
    Q2: LIMITS? → NFR
    Q3: WHAT? → FSD
    Q4: HOW? → SAD
    Q5: SCHEMA? → ICD
    Q6: CLASS? → TDD
    Default: → ISP

    Parameters
    ----------
    text : str
        The information fragment to classify.

    Returns
    -------
    ClassificationResult
        Classification result with tier, confidence, and rationale.
    """
    scores: dict[str, tuple[float, list[str]]] = {}
    question_path: list[str] = []

    # Compute scores for all questions
    for question_key in CLASSIFICATION_PATTERNS:
        score, matched = calculate_score(text, question_key)
        scores[question_key] = (score, matched)

    # Apply decision tree in order (Q1 → Q6)
    decision_order = ["Q1_WHY", "Q2_LIMITS", "Q3_WHAT", "Q4_HOW", "Q5_SCHEMA", "Q6_CLASS"]
    threshold = 0.3  # Minimum score to accept a match

    winning_question = None
    winning_score = 0.0

    for question_key in decision_order:
        score, matched = scores[question_key]
        question_path.append(f"{question_key}: {score:.2f}")

        if score >= threshold:
            winning_question = question_key
            winning_score = score
            break

    # Check for ambiguity (multiple high scores)
    high_scores = [(k, s) for k, (s, _) in scores.items() if s >= threshold]
    if len(high_scores) > 1:
        # Sort by score descending
        high_scores.sort(key=lambda x: x[1], reverse=True)
        top_two = high_scores[:2]
        if top_two[0][1] - top_two[1][1] < 0.1:
            # Scores are very close - ambiguous
            candidates = [CLASSIFICATION_PATTERNS[k]["tier"] for k, _ in high_scores]
            return ClassificationResult(
                tier=CLASSIFICATION_PATTERNS[top_two[0][0]]["tier"],
                confidence=top_two[0][1],
                rationale=f"Ambiguous: close scores between {', '.join(candidates)}. "
                          f"Apply scoring_matrix for resolution.",
                question_path=question_path,
                ambiguous=True,
                candidates=candidates
            )

    # Determine result
    if winning_question:
        config = CLASSIFICATION_PATTERNS[winning_question]
        _, matched = scores[winning_question]
        return ClassificationResult(
            tier=config["tier"],
            confidence=winning_score,
            rationale=f"Matched {config['question']} "
                      f"Terms: {', '.join(matched[:5])}",
            question_path=question_path
        )
    else:
        # Default to ISP
        return ClassificationResult(
            tier=DEFAULT_TIER,
            confidence=0.5,
            rationale=f"No strong match in decision tree. "
                      f"Defaulting to {DEFAULT_TIER} (executable code skeleton).",
            question_path=question_path
        )


def main() -> int:
    """
    CLI entry point for classify_information.

    Returns
    -------
    int
        Exit code (0=success, 1=error).
    """
    parser = argparse.ArgumentParser(
        description="Classify information fragments into DDR tiers."
    )
    parser.add_argument(
        "--input",
        required=True,
        help="Information fragment to classify"
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Include detailed scoring breakdown"
    )

    args = parser.parse_args()

    if not args.input.strip():
        print("Error: Input cannot be empty", file=sys.stderr)
        return 1

    try:
        result = classify_information(args.input)

        output = {
            "tier": result.tier,
            "confidence": round(result.confidence, 3),
            "rationale": result.rationale,
            "ambiguous": result.ambiguous
        }

        if result.ambiguous and result.candidates:
            output["candidates"] = result.candidates
            output["next_step"] = "Use scoring_matrix tool to resolve ambiguity"

        if args.verbose:
            output["question_path"] = result.question_path

        print(json.dumps(output, indent=2))
        return 0

    except Exception as e:
        print(f"Error classifying information: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())

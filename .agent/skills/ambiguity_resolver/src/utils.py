"""
Utility functions for the ambiguity_resolver skill.

Includes configuration loading, output formatting, and helper functions.
"""

import yaml
import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional


logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict:
    """
    Load YAML configuration file.

    Parameters
    ----------
    config_path : str
        Path to YAML configuration file.

    Returns
    -------
    Dict
        Parsed configuration.

    Examples
    --------
    >>> config = load_config("config/scoring_weights.yaml")
    >>> print(config['numeric_metrics']['NFR'])
    3
    """
    path = Path(config_path)

    if not path.exists():
        logger.warning(f"Config file not found: {config_path}, using defaults")
        return _get_default_config()

    try:
        with open(path, 'r') as f:
            config = yaml.safe_load(f)
            logger.info(f"Loaded configuration from {config_path}")
            return config
    except Exception as e:
        logger.error(f"Failed to load config {config_path}: {e}")
        return _get_default_config()


def _get_default_config() -> Dict:
    """
    Get default configuration if file loading fails.

    Returns
    -------
    Dict
        Default scoring weights.
    """
    return {
        'numeric_metrics': {'BRD': 1, 'NFR': 3, 'FSD': 1, 'ICD': 2},
        'hardware_reference': {'BRD': 1, 'NFR': 3, 'SAD': 1},
        'user_behavior': {'BRD': 2, 'FSD': 3},
        'pattern_names': {'SAD': 3, 'TDD': 1},
        'schema_definition': {'ICD': 3, 'ISP': 1},
        'class_names': {'TDD': 3, 'ISP': 2},
        'executable_code': {'ISP': 3},
        'modal_keywords': {'BRD': 2, 'NFR': 3, 'FSD': 2},
        'includes_rationale': {'BRD': 3, 'SAD': 3, 'TDD': 2},
        'technology_agnostic': {'BRD': 3, 'NFR': 1, 'FSD': 2}
    }


def format_rst_output(result) -> str:
    """
    Format classification result as RST directive.

    Parameters
    ----------
    result : ClassificationResult
        Classification result object.

    Returns
    -------
    str
        Formatted RST directive with metadata.

    Examples
    --------
    >>> rst = format_rst_output(result)
    >>> print(rst)
    .. nfr:: System must aggregate logs to single file
       :id: NFR-<next>
       :links: BRD-<parent>
    """
    tier = result.assigned_tier.value.lower()

    # Extract first sentence of fragment for title
    lines = result.reasoning.split('\n')
    fragment_line = [l for l in lines if l.startswith('FRAGMENT:')]
    if fragment_line:
        fragment = fragment_line[0].replace('FRAGMENT: "', '').replace('"', '')
        # Limit to 80 chars
        if len(fragment) > 80:
            fragment = fragment[:77] + '...'
    else:
        fragment = "Content from classification"

    # Format RST directive
    rst_lines = [
        f".. {tier}:: {fragment}",
        f"   :id: {result.assigned_tier.value}-<next>",
        f"   :links: <parent>",
        "",
        f"   # Classification confidence: {result.confidence:.3f}",
        f"   # Factors: {', '.join([k for k, v in result.factors_detected.items() if v.value != 'none'])}",
        f"   # Validation: {'passed' if result.validation_passed else 'FAILED'}",
    ]

    if result.tie_breaker_applied:
        rst_lines.append("   # Tie-breaker: Higher abstraction rule applied")

    if result.validation_notes:
        rst_lines.append("   #")
        for note in result.validation_notes[:3]:  # Limit to 3 notes
            rst_lines.append(f"   # {note}")

    return '\n'.join(rst_lines)


def format_detailed_output(result) -> str:
    """
    Format classification result as detailed text report.

    Parameters
    ----------
    result : ClassificationResult
        Classification result object.

    Returns
    -------
    str
        Formatted detailed report.
    """
    lines = [
        "=" * 70,
        "DDR AMBIGUITY RESOLUTION REPORT",
        "=" * 70,
        "",
        f"ASSIGNED TIER: {result.assigned_tier.value}",
        f"CONFIDENCE: {result.confidence:.3f}",
        "",
        "TIER SCORES:",
        "-" * 70
    ]

    # Sort scores by value
    sorted_scores = sorted(
        result.scores.items(),
        key=lambda x: x[1],
        reverse=True
    )

    for tier, score in sorted_scores:
        marker = " ← SELECTED" if tier == result.assigned_tier else ""
        lines.append(f"  {tier.value:6s}: {score:3d}{marker}")

    lines.extend([
        "",
        "FACTORS DETECTED:",
        "-" * 70
    ])

    for factor, presence in result.factors_detected.items():
        if presence.value != 'none':
            lines.append(f"  • {factor:25s}: {presence.value}")

    lines.extend([
        "",
        "VALIDATION:",
        "-" * 70,
        f"  Status: {'✓ PASSED' if result.validation_passed else '✗ FAILED'}",
        ""
    ])

    for note in result.validation_notes:
        lines.append(f"  - {note}")

    if result.tie_breaker_applied:
        lines.extend([
            "",
            "TIE-BREAKER: Higher abstraction hierarchy rule applied",
            ""
        ])

    lines.extend([
        "",
        "=" * 70
    ])

    return '\n'.join(lines)


def calculate_score_margin(scores: Dict) -> float:
    """
    Calculate margin between winner and runner-up.

    Parameters
    ----------
    scores : Dict
        Tier scores.

    Returns
    -------
    float
        Score margin (0+ points).
    """
    if len(scores) < 2:
        return 0.0

    sorted_scores = sorted(scores.values(), reverse=True)
    return float(sorted_scores[0] - sorted_scores[1])


def get_top_factors(factors: Dict, top_n: int = 5) -> list:
    """
    Get top N factors by presence.

    Parameters
    ----------
    factors : Dict[str, FactorPresence]
        Detected factors.
    top_n : int
        Number of top factors to return.

    Returns
    -------
    list
        Top factor names.
    """
    # Filter to present factors
    present_factors = {
        k: v for k, v in factors.items()
        if v.value != 'none'
    }

    # Sort by presence (yes > partial > none)
    presence_order = {'yes': 2, 'partial': 1, 'none': 0}
    sorted_factors = sorted(
        present_factors.items(),
        key=lambda x: presence_order.get(x[1].value, 0),
        reverse=True
    )

    return [k for k, v in sorted_factors[:top_n]]


def export_result_json(result, filepath: str) -> None:
    """
    Export classification result to JSON file.

    Parameters
    ----------
    result : ClassificationResult
        Classification result.
    filepath : str
        Output JSON filepath.
    """
    output = {
        'assigned_tier': result.assigned_tier.value,
        'confidence': result.confidence,
        'scores': {t.value: s for t, s in result.scores.items()},
        'factors_detected': {k: v.value for k, v in result.factors_detected.items()},
        'tie_breaker_applied': result.tie_breaker_applied,
        'validation_passed': result.validation_passed,
        'validation_notes': result.validation_notes,
        'reasoning': result.reasoning
    }

    with open(filepath, 'w') as f:
        json.dump(output, f, indent=2)

    logger.info(f"Result exported to {filepath}")


def truncate_text(text: str, max_length: int = 100) -> str:
    """
    Truncate text to maximum length with ellipsis.

    Parameters
    ----------
    text : str
        Input text.
    max_length : int
        Maximum length.

    Returns
    -------
    str
        Truncated text.
    """
    if len(text) <= max_length:
        return text
    return text[:max_length - 3] + '...'


def validate_fragment(fragment: str, max_length: int = 2000) -> tuple:
    """
    Validate input fragment.

    Parameters
    ----------
    fragment : str
        Input fragment to validate.
    max_length : int
        Maximum allowed length.

    Returns
    -------
    tuple
        (is_valid: bool, error_message: Optional[str])
    """
    if not fragment or not fragment.strip():
        return False, "Fragment cannot be empty"

    if len(fragment) > max_length:
        return False, f"Fragment exceeds maximum length ({max_length} chars)"

    return True, None


def setup_logging(level: str = "INFO") -> None:
    """
    Configure logging for the skill.

    Parameters
    ----------
    level : str
        Logging level (DEBUG, INFO, WARNING, ERROR).
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)

    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    logger.info(f"Logging configured at {level} level")

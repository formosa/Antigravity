"""
DDR Ambiguity Resolver Skill

Resolves ambiguous DDR tier classifications using multi-factor scoring
when the decision tree yields multiple candidate tiers.

Main Components
---------------
- AmbiguityResolver: Core resolution engine
- ScoringMatrix: 10-factor scoring implementation
- ContextualValidator: Semantic validation
- TierHierarchy: Abstraction ordering and rules

Usage
-----
Basic classification:
    >>> from ambiguity_resolver import resolve_ambiguity
    >>> result = resolve_ambiguity("System must have < 1s latency")
    >>> print(result['assigned_tier'])
    'NFR'

Advanced usage with context:
    >>> from ambiguity_resolver import AmbiguityResolver, Tier
    >>> resolver = AmbiguityResolver()
    >>> result = resolver.resolve(
    ...     fragment="Log aggregation to single file",
    ...     candidate_tiers=[Tier.NFR, Tier.ICD],
    ...     context={'existing_brd_tags': ['BRD-3.5']}
    ... )

Batch processing:
    >>> results = resolver.resolve_batch(fragments)

For complete documentation, see README.md and docs/.
"""

from .resolver import (
    AmbiguityResolver,
    ClassificationResult,
    Tier,
    resolve_ambiguity
)

from .scoring_matrix import (
    ScoringMatrix,
    FactorPresence
)

from .validators import (
    ContextualValidator
)

from .tier_rules import (
    TierHierarchy
)

from .utils import (
    load_config,
    format_rst_output,
    format_detailed_output,
    setup_logging
)


__version__ = "1.0.0"
__author__ = "DDR System Team"
__license__ = "MIT"

__all__ = [
    # Main interface
    'resolve_ambiguity',
    'AmbiguityResolver',

    # Data structures
    'ClassificationResult',
    'Tier',
    'FactorPresence',

    # Components
    'ScoringMatrix',
    'ContextualValidator',
    'TierHierarchy',

    # Utilities
    'load_config',
    'format_rst_output',
    'format_detailed_output',
    'setup_logging',

    # Metadata
    '__version__',
]


# Convenience imports for common use cases
def quick_classify(fragment: str, output_format: str = "summary") -> dict:
    """
    Quick classification helper function.

    Parameters
    ----------
    fragment : str
        Information fragment to classify.
    output_format : str
        Output format: "summary", "detailed", or "rst_directive".

    Returns
    -------
    dict
        Classification result.

    Examples
    --------
    >>> result = quick_classify("System must have < 1s latency")
    >>> print(result['assigned_tier'])
    'NFR'
    """
    return resolve_ambiguity(fragment, output_format=output_format)


# Version check helper
def check_compatibility(antigravity_version: str) -> bool:
    """
    Check if Antigravity IDE version is compatible.

    Parameters
    ----------
    antigravity_version : str
        Antigravity IDE version string (e.g., "1.16.5").

    Returns
    -------
    bool
        True if compatible.
    """
    from packaging import version
    required = version.parse("1.16.5")
    current = version.parse(antigravity_version)
    return current >= required

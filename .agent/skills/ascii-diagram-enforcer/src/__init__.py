"""
ASCII Diagram Enforcer - Source Package

Main package initialization exposing public API for ASCII diagram validation
in DDR System SAD-tier documentation.

Implements: Public API surface for skill integration
Requirements: DDR System Tier 4 (SAD) compliance

Author: DDR System Integration Team
Version: 1.0.0
"""

from .enforcer import (
    ASCIIDiagramEnforcer,
    ValidationResult,
    Violation,
    ViolationSeverity
)
from .diagram_detector import DiagramDetector, DiagramMatch
from .sad_parser import SADParser
from .validators import DiagramValidator


__version__ = "1.0.0"
__author__ = "DDR System Integration Team"
__license__ = "MIT"

__all__ = [
    # Core enforcer
    "ASCIIDiagramEnforcer",
    "ValidationResult",
    "Violation",
    "ViolationSeverity",

    # Detection engine
    "DiagramDetector",
    "DiagramMatch",

    # Parser
    "SADParser",

    # Validator
    "DiagramValidator",
]


# Package-level configuration
DEFAULT_CONFIG = {
    "strict_mode": True,
    "min_diagram_lines": 3,
    "auto_flag_dirty": True,
    "confidence_threshold": 0.6
}


def get_version() -> str:
    """
    Get package version string.

    Returns
    -------
    str
        Semantic version identifier.

    Examples
    --------
    >>> from ascii_diagram_enforcer.src import get_version
    >>> get_version()
    '1.0.0'
    """
    return __version__


def create_enforcer(**kwargs):
    """
    Factory function for creating enforcer instance with defaults.

    Parameters
    ----------
    **kwargs
        Configuration overrides for enforcer initialization.

    Returns
    -------
    ASCIIDiagramEnforcer
        Configured enforcer instance.

    Examples
    --------
    >>> from ascii_diagram_enforcer.src import create_enforcer
    >>> enforcer = create_enforcer(strict_mode=False)
    >>> enforcer.strict_mode
    False

    Notes
    -----
    Default configuration values are merged with provided kwargs.
    Provided values override defaults.
    """
    config = DEFAULT_CONFIG.copy()
    config.update(kwargs)

    return ASCIIDiagramEnforcer(
        strict_mode=config["strict_mode"],
        min_diagram_lines=config["min_diagram_lines"],
        auto_flag_dirty=config["auto_flag_dirty"]
    )

"""
Pre-Save Validation Hook

Blocks document save operations when ERROR-level violations exist in strict mode.
Provides user feedback and remediation options before allowing save.

Implements: Pre-save blocking validation for DDR compliance
Requirements: Antigravity IDE 1.16.5+ save event API

Author: DDR System Integration Team
Version: 1.0.0
"""

import logging
from typing import Dict, Optional
from pathlib import Path

from ascii_diagram_enforcer.src import ASCIIDiagramEnforcer, ViolationSeverity


logger = logging.getLogger(__name__)


def validate_before_save(document, context) -> Dict[str, any]:
    """
    Pre-save validation hook handler.

    This function is called by Antigravity IDE before saving a document.
    In strict mode, it prevents saving documents with ERROR-level violations.

    Parameters
    ----------
    document : Document
        Document being saved.
    context : SkillContext
        IDE context with configuration and UI access.

    Returns
    -------
    Dict[str, any]
        Hook result with keys:
        - allow_save: bool - Whether to permit save operation
        - violations: List[Violation] - Detected violations
        - message: Optional[str] - User feedback message

    Examples
    --------
    Hook is automatically invoked by IDE:
    >>> # User presses Ctrl+S
    >>> result = validate_before_save(doc, ctx)
    >>> if not result['allow_save']:
    ...     # Save blocked, user sees error dialog

    Notes
    -----
    Only validates SAD-tier documents in docs/04_sad/ directories.
    Non-SAD documents always pass validation.
    """
    # Check if this is a SAD document
    if not _is_sad_document(document):
        logger.debug(f"Skipping non-SAD document: {document.path}")
        return {
            "allow_save": True,
            "violations": [],
            "message": None
        }

    # Get configuration
    config = context.get_config()
    strict_mode = config.get('strict_mode', True)

    # Create enforcer
    enforcer = ASCIIDiagramEnforcer(
        strict_mode=strict_mode,
        min_diagram_lines=config.get('min_diagram_lines', 3),
        auto_flag_dirty=config.get('auto_flag_dirty', True)
    )

    # Validate document
    content = document.get_text()
    section_id = _extract_section_id(document)

    logger.info(f"Pre-save validation: {document.path}")
    result = enforcer.validate_section(content, section_id)

    # Count ERROR-level violations
    error_count = sum(
        1 for v in result.violations
        if v.severity == ViolationSeverity.ERROR
    )

    warning_count = sum(
        1 for v in result.violations
        if v.severity == ViolationSeverity.WARNING
    )

    # Determine if save should be allowed
    if strict_mode and error_count > 0:
        # Block save in strict mode with errors
        logger.warning(
            f"Blocking save: {error_count} ERROR violations in {document.path}"
        )

        message = _format_blocking_message(error_count, warning_count)

        return {
            "allow_save": False,
            "violations": result.violations,
            "message": message,
            "error_count": error_count,
            "warning_count": warning_count
        }

    elif warning_count > 0:
        # Allow save but show warning
        logger.info(
            f"Allowing save with warnings: {warning_count} WARNING violations"
        )

        message = _format_warning_message(warning_count)

        return {
            "allow_save": True,
            "violations": result.violations,
            "message": message,
            "warning_count": warning_count
        }

    else:
        # Clean save - no violations
        logger.info(f"Clean save: {document.path}")

        return {
            "allow_save": True,
            "violations": [],
            "message": "✓ All ASCII diagram requirements satisfied"
        }


def _is_sad_document(document) -> bool:
    """
    Check if document is SAD-tier RST file.

    Parameters
    ----------
    document : Document
        Document to check.

    Returns
    -------
    bool
        True if SAD-tier document requiring validation.
    """
    path = Path(document.path)

    return (
        path.suffix in ['.rst', '.md'] and
        '04_sad' in path.parts
    )


def _extract_section_id(document) -> str:
    """
    Extract section ID from document path for validation.

    Parameters
    ----------
    document : Document
        Document to extract from.

    Returns
    -------
    str
        Section identifier (e.g., 'sad-architecture').
    """
    path = Path(document.path)
    return f"sad-{path.stem}"


def _format_blocking_message(error_count: int, warning_count: int) -> str:
    """
    Format user-facing message for blocked save.

    Parameters
    ----------
    error_count : int
        Number of ERROR violations.
    warning_count : int
        Number of WARNING violations.

    Returns
    -------
    str
        Formatted message for display.
    """
    lines = [
        "❌ Cannot Save Document",
        "",
        f"Found {error_count} ERROR-level violation(s) that must be fixed:",
        "",
        "• Missing or invalid ASCII diagrams in SAD sections",
        "• Block-level SAD tags require topology diagrams",
        "",
        "Actions:",
        "1. View violations in the Problems panel",
        "2. Use 'Insert ASCII Diagram Template' quick fix",
        "3. Or disable strict mode in skill settings",
    ]

    if warning_count > 0:
        lines.append("")
        lines.append(f"Also found {warning_count} WARNING(s) - can be fixed later")

    return "\n".join(lines)


def _format_warning_message(warning_count: int) -> str:
    """
    Format user-facing message for save with warnings.

    Parameters
    ----------
    warning_count : int
        Number of WARNING violations.

    Returns
    -------
    str
        Formatted message for display.
    """
    return (
        f"⚠️ Saved with {warning_count} warning(s)\n\n"
        f"Consider addressing diagram quality issues:\n"
        f"• Unrecognized box characters\n"
        f"• Insufficient structural clarity\n"
        f"• Missing component labels"
    )

"""
On-Demand Validation Hook

Manual validation trigger for user-initiated diagram checks.
Provides detailed validation reports and violation summaries.

Implements: Manual validation command for DDR compliance checking
Requirements: Antigravity IDE 1.16.5+ command API

Author: DDR System Integration Team
Version: 1.0.0
"""

import logging
from typing import Dict, List, Optional
from pathlib import Path

from ascii_diagram_enforcer.src import (
    ASCIIDiagramEnforcer,
    ValidationResult,
    ViolationSeverity
)


logger = logging.getLogger(__name__)


def validate_on_request(document, context) -> Dict[str, any]:
    """
    Manual validation command handler.

    Triggered by user via command palette or keyboard shortcut.
    Generates comprehensive validation report with violation details.

    Parameters
    ----------
    document : Document
        Document to validate (usually active document).
    context : SkillContext
        IDE context with UI and configuration access.

    Returns
    -------
    Dict[str, any]
        Validation results with keys:
        - success: bool - Whether validation completed
        - result: ValidationResult - Complete validation data
        - report: str - Human-readable report

    Examples
    --------
    >>> # User executes: DDR: Validate ASCII Diagrams (Ctrl+Shift+D)
    >>> result = validate_on_request(doc, ctx)
    >>> # Report displayed in IDE panel

    Notes
    -----
    Shows informational message for non-SAD documents.
    Displays full report in IDE panel with syntax highlighting.
    """
    # Check if document is valid for validation
    if not document:
        logger.warning("No active document for validation")
        context.show_warning(
            title="No Document",
            message="Open a SAD-tier document to validate ASCII diagrams."
        )
        return {
            "success": False,
            "result": None,
            "report": None
        }

    # Check if this is a SAD document
    if not _is_sad_document(document):
        logger.info(f"Non-SAD document: {document.path}")
        context.show_info(
            title="Not a SAD Document",
            message=(
                f"Current document is not in the SAD tier (docs/04_sad/).\n\n"
                f"ASCII Diagram Enforcer only validates System Architecture "
                f"Document (SAD) files per DDR System requirements."
            )
        )
        return {
            "success": False,
            "result": None,
            "report": "Document is not a SAD-tier file"
        }

    # Get configuration
    config = context.get_config()

    # Create enforcer
    enforcer = ASCIIDiagramEnforcer(
        strict_mode=config.get('strict_mode', True),
        min_diagram_lines=config.get('min_diagram_lines', 3),
        auto_flag_dirty=config.get('auto_flag_dirty', True)
    )

    # Run validation
    content = document.get_text()
    section_id = _extract_section_id(document)

    logger.info(f"Manual validation requested: {document.path}")
    result = enforcer.validate_section(content, section_id)

    # Generate report
    report = enforcer.generate_report(result)

    # Display report in panel
    _display_report_panel(context, result, report)

    # Show summary notification
    _show_summary_notification(context, result)

    return {
        "success": True,
        "result": result,
        "report": report
    }


def _is_sad_document(document) -> bool:
    """
    Check if document is SAD-tier file.

    Parameters
    ----------
    document : Document
        Document to check.

    Returns
    -------
    bool
        True if SAD-tier document.
    """
    path = Path(document.path)

    return (
        path.suffix in ['.rst', '.md'] and
        '04_sad' in path.parts
    )


def _extract_section_id(document) -> str:
    """
    Extract section ID from document path.

    Parameters
    ----------
    document : Document
        Document to extract from.

    Returns
    -------
    str
        Section identifier.
    """
    path = Path(document.path)
    return f"sad-{path.stem}"


def _display_report_panel(context, result: ValidationResult, report: str):
    """
    Display validation report in IDE panel.

    Parameters
    ----------
    context : SkillContext
        IDE context.
    result : ValidationResult
        Validation results.
    report : str
        Formatted report text.
    """
    # Determine panel title based on result
    if result.is_valid:
        title = "✓ ASCII Diagram Validation - PASSED"
        panel_style = "success"
    else:
        title = "✗ ASCII Diagram Validation - FAILED"
        panel_style = "error"

    # Show report in bottom panel
    context.show_panel(
        title=title,
        content=report,
        syntax="text",
        location="bottom",
        style=panel_style
    )

    logger.info(f"Displayed validation report: {title}")


def _show_summary_notification(context, result: ValidationResult):
    """
    Show brief notification summary of validation results.

    Parameters
    ----------
    context : SkillContext
        IDE context.
    result : ValidationResult
        Validation results.
    """
    error_count = sum(
        1 for v in result.violations
        if v.severity == ViolationSeverity.ERROR
    )

    warning_count = sum(
        1 for v in result.violations
        if v.severity == ViolationSeverity.WARNING
    )

    if result.is_valid:
        context.show_success(
            title="Validation Passed",
            message=(
                f"All {result.sad_tags_found} SAD tag(s) have valid ASCII diagrams.\n"
                f"Found {result.diagrams_found} diagram(s) - all compliant."
            ),
            duration=3000  # 3 seconds
        )
    else:
        context.show_error(
            title="Validation Failed",
            message=(
                f"Found {error_count} ERROR(s) and {warning_count} WARNING(s).\n"
                f"See validation report for details."
            ),
            duration=5000  # 5 seconds
        )


def validate_multiple_files(file_paths: List[str], context) -> Dict[str, any]:
    """
    Validate multiple SAD files in batch mode.

    Useful for validating entire SAD directory or specific file sets.

    Parameters
    ----------
    file_paths : List[str]
        Paths to files to validate.
    context : SkillContext
        IDE context.

    Returns
    -------
    Dict[str, any]
        Batch validation results with per-file breakdown.

    Examples
    --------
    >>> paths = ['docs/04_sad/arch.rst', 'docs/04_sad/topology.rst']
    >>> results = validate_multiple_files(paths, context)
    >>> results['total_files']
    2
    """
    config = context.get_config()
    enforcer = ASCIIDiagramEnforcer(
        strict_mode=config.get('strict_mode', True),
        min_diagram_lines=config.get('min_diagram_lines', 3),
        auto_flag_dirty=False  # Don't auto-flag in batch mode
    )

    results = {
        "total_files": len(file_paths),
        "valid_files": 0,
        "invalid_files": 0,
        "file_results": {}
    }

    for file_path in file_paths:
        path = Path(file_path)

        # Skip non-SAD files
        if not ('04_sad' in path.parts and path.suffix in ['.rst', '.md']):
            continue

        # Read and validate
        content = path.read_text(encoding='utf-8')
        section_id = f"sad-{path.stem}"

        result = enforcer.validate_section(content, section_id)

        # Track results
        if result.is_valid:
            results["valid_files"] += 1
        else:
            results["invalid_files"] += 1

        results["file_results"][str(file_path)] = {
            "is_valid": result.is_valid,
            "violations": len(result.violations),
            "sad_tags": result.sad_tags_found,
            "diagrams": result.diagrams_found
        }

    logger.info(
        f"Batch validation complete: {results['valid_files']} valid, "
        f"{results['invalid_files']} invalid"
    )

    return results

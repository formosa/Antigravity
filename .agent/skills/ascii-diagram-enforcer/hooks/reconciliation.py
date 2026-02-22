"""
Reconciliation Integration Hook

Integrates ASCII diagram validation with DDR System reconciliation manifests.
Automatically updates DIRTY flags and pending items when violations detected.

Implements: DDR reconciliation system integration
Requirements: DDR reconciliation manifest format compliance

Author: DDR System Integration Team
Version: 1.0.0
"""

import logging
import re
from typing import Dict, List, Optional, Tuple
from datetime import date
from pathlib import Path

from ascii_diagram_enforcer.src import (
    ASCIIDiagramEnforcer,
    ValidationResult,
    ViolationSeverity
)


logger = logging.getLogger(__name__)


def integrate_with_manifest(document, validation_result: ValidationResult, context) -> Dict[str, any]:
    """
    Update reconciliation manifest based on validation results.

    Automatically sets DIRTY flag and injects pending items when violations
    are detected. Maintains DDR System reconciliation integrity.

    Parameters
    ----------
    document : Document
        Validated document.
    validation_result : ValidationResult
        Validation results to integrate.
    context : SkillContext
        IDE context for file operations.

    Returns
    -------
    Dict[str, any]
        Integration results with keys:
        - manifest_updated: bool - Whether manifest was modified
        - dirty_flag_set: bool - Whether DIRTY status was set
        - pending_items_added: int - Count of pending items added

    Examples
    --------
    >>> result = enforcer.validate_section(content, 'sad-root')
    >>> integration = integrate_with_manifest(doc, result, ctx)
    >>> integration['dirty_flag_set']
    True  # If violations were found

    Notes
    -----
    Only updates manifest if auto_flag_dirty configuration is enabled.
    Preserves existing pending items from other sources.
    """
    config = context.get_config()

    # Check if auto-flagging is enabled
    if not config.get('auto_flag_dirty', True):
        logger.info("Auto-flagging disabled, skipping manifest update")
        return {
            "manifest_updated": False,
            "dirty_flag_set": False,
            "pending_items_added": 0
        }

    # Only update if violations exist
    if validation_result.is_valid:
        logger.debug("Validation passed, no manifest update needed")
        return {
            "manifest_updated": False,
            "dirty_flag_set": False,
            "pending_items_added": 0
        }

    # Parse current manifest
    content = document.get_text()
    manifest_data = _parse_manifest(content)

    if not manifest_data:
        logger.warning("No reconciliation manifest found in document")
        return {
            "manifest_updated": False,
            "dirty_flag_set": False,
            "pending_items_added": 0,
            "error": "No manifest found"
        }

    # Update manifest with violations
    updated_manifest = _update_manifest_with_violations(
        manifest_data,
        validation_result
    )

    # Replace manifest in document
    new_content = _replace_manifest(content, updated_manifest)
    document.set_text(new_content)

    logger.info(
        f"Updated reconciliation manifest: "
        f"DIRTY={updated_manifest['integrity_status']}, "
        f"pending_items={len(updated_manifest['pending_items'])}"
    )

    return {
        "manifest_updated": True,
        "dirty_flag_set": updated_manifest['integrity_status'] == "DIRTY",
        "pending_items_added": len(updated_manifest['pending_items'])
    }


def _parse_manifest(content: str) -> Optional[Dict]:
    """
    Parse reconciliation manifest from document content.

    Parameters
    ----------
    content : str
        Document content containing manifest.

    Returns
    -------
    Optional[Dict]
        Parsed manifest data or None if not found.
    """
    # Find manifest block
    manifest_pattern = re.compile(
        r'^\.\.\s+reconciliation_manifest:\s*$\n'
        r'((?:\s+:[^:]+:.*$\n)+)',
        re.MULTILINE
    )

    match = manifest_pattern.search(content)
    if not match:
        return None

    # Parse fields
    fields_text = match.group(1)
    manifest = {}

    # Parse each field
    field_pattern = re.compile(r'^\s+:([^:]+):\s+(.+)$', re.MULTILINE)

    for field_match in field_pattern.finditer(fields_text):
        field_name = field_match.group(1).strip()
        field_value = field_match.group(2).strip()

        # Remove quotes and parse value
        field_value = field_value.strip('"')

        # Parse lists
        if field_value.startswith('[') and field_value.endswith(']'):
            # Simple list parsing
            field_value = eval(field_value)  # Safe for controlled input

        manifest[field_name] = field_value

    return manifest


def _update_manifest_with_violations(
    manifest: Dict,
    validation_result: ValidationResult
) -> Dict:
    """
    Update manifest fields based on validation violations.

    Parameters
    ----------
    manifest : Dict
        Current manifest data.
    validation_result : ValidationResult
        Validation results.

    Returns
    -------
    Dict
        Updated manifest data.
    """
    updated = manifest.copy()

    # Set DIRTY flag
    updated['integrity_status'] = "DIRTY"

    # Update timestamp
    updated['timestamp'] = date.today().isoformat()

    # Generate pending items for violations
    pending_items = _generate_pending_items(validation_result)

    # Merge with existing pending items (preserve non-diagram issues)
    existing_items = manifest.get('pending_items', [])

    # Remove old diagram violations
    existing_items = [
        item for item in existing_items
        if 'ascii_diagram_enforcer' not in item.get('source_trigger', '')
    ]

    # Add new violations
    updated['pending_items'] = existing_items + pending_items

    return updated


def _generate_pending_items(validation_result: ValidationResult) -> List[Dict]:
    """
    Generate pending_items from validation violations.

    Parameters
    ----------
    validation_result : ValidationResult
        Validation results.

    Returns
    -------
    List[Dict]
        Pending items in DDR reconciliation format.
    """
    pending_items = []

    # Group violations by target tag
    violations_by_tag = {}
    for violation in validation_result.violations:
        tag = violation.target_tag
        if tag not in violations_by_tag:
            violations_by_tag[tag] = []
        violations_by_tag[tag].append(violation)

    # Create pending items
    for tag, violations in violations_by_tag.items():
        # Count ERROR vs WARNING
        errors = sum(1 for v in violations if v.severity == ViolationSeverity.ERROR)
        warnings = sum(1 for v in violations if v.severity == ViolationSeverity.WARNING)

        # Determine issue type
        if errors > 0:
            issue_type = "CONSTRAINT_VIOLATION"
        else:
            issue_type = "QUALITY_WARNING"

        # Create description
        descriptions = [v.description for v in violations[:3]]  # First 3
        if len(violations) > 3:
            descriptions.append(f"... and {len(violations) - 3} more")

        description = "; ".join(descriptions)

        pending_items.append({
            "target_tag": tag,
            "source_trigger": "ascii_diagram_enforcer validation",
            "issue_type": issue_type,
            "description": description
        })

    return pending_items


def _replace_manifest(content: str, updated_manifest: Dict) -> str:
    """
    Replace manifest block in document content.

    Parameters
    ----------
    content : str
        Original document content.
    updated_manifest : Dict
        Updated manifest data.

    Returns
    -------
    str
        Content with updated manifest.
    """
    # Format new manifest
    new_manifest_text = _format_manifest(updated_manifest)

    # Find and replace old manifest
    manifest_pattern = re.compile(
        r'^\.\.\s+reconciliation_manifest:.*?(?=\n\n|\n\.\.|$)',
        re.MULTILINE | re.DOTALL
    )

    new_content = manifest_pattern.sub(new_manifest_text, content)

    return new_content


def _format_manifest(manifest: Dict) -> str:
    """
    Format manifest dict as RST directive.

    Parameters
    ----------
    manifest : Dict
        Manifest data to format.

    Returns
    -------
    str
        Formatted RST manifest block.
    """
    lines = [".. reconciliation_manifest:"]

    # Required fields in order
    fields = [
        'section_id',
        'integrity_status',
        'timestamp',
        'tag_count',
        'tag_inventory',
        'pending_items'
    ]

    for field in fields:
        if field not in manifest:
            continue

        value = manifest[field]

        # Format value
        if isinstance(value, str):
            formatted_value = f'"{value}"'
        elif isinstance(value, list):
            if field == 'pending_items' and len(value) > 0:
                # Pretty-format pending items
                formatted_value = "[\n"
                for item in value:
                    formatted_value += "     {\n"
                    for k, v in item.items():
                        formatted_value += f'       "{k}": "{v}",\n'
                    formatted_value = formatted_value.rstrip(',\n') + '\n'
                    formatted_value += "     },\n"
                formatted_value = formatted_value.rstrip(',\n') + '\n   ]'
            else:
                formatted_value = str(value)
        else:
            formatted_value = str(value)

        lines.append(f"   :{field}: {formatted_value}")

    return "\n".join(lines)


def clear_diagram_violations(document, context) -> Dict[str, any]:
    """
    Clear diagram-related pending items from manifest.

    Used when violations are resolved and manifest should be cleaned.

    Parameters
    ----------
    document : Document
        Document with manifest to clean.
    context : SkillContext
        IDE context.

    Returns
    -------
    Dict[str, any]
        Clearing results.

    Examples
    --------
    >>> # After fixing all diagram issues
    >>> result = clear_diagram_violations(doc, ctx)
    >>> result['items_removed']
    3
    """
    content = document.get_text()
    manifest = _parse_manifest(content)

    if not manifest:
        return {
            "success": False,
            "error": "No manifest found"
        }

    # Remove diagram violations
    existing_items = manifest.get('pending_items', [])
    initial_count = len(existing_items)

    cleaned_items = [
        item for item in existing_items
        if 'ascii_diagram_enforcer' not in item.get('source_trigger', '')
    ]

    removed_count = initial_count - len(cleaned_items)

    # Update manifest
    manifest['pending_items'] = cleaned_items

    # Set CLEAN if no items remain
    if len(cleaned_items) == 0:
        manifest['integrity_status'] = "CLEAN"

    manifest['timestamp'] = date.today().isoformat()

    # Replace in document
    new_content = _replace_manifest(content, manifest)
    document.set_text(new_content)

    logger.info(f"Cleared {removed_count} diagram violations from manifest")

    return {
        "success": True,
        "items_removed": removed_count,
        "status": manifest['integrity_status']
    }

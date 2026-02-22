"""
Antigravity IDE skill entrypoint for block-atomic validator.

Implements: IDE integration hooks for validation triggers
Requirements: Antigravity IDE 1.16.5+ plugin API
"""

from pathlib import Path
from typing import Dict, List, Optional
import json

from block_atomic_validator.core.validator import BlockAtomicValidator
from block_atomic_validator.core.models import ValidationResult
from block_atomic_validator.reporters.ide_reporter import IDEReporter


# Global validator instance (initialized on IDE load)
_validator: Optional[BlockAtomicValidator] = None
_reporter: Optional[IDEReporter] = None


def initialize(config: Dict) -> None:
    """
    Initialize validator with IDE-provided configuration.

    Called by Antigravity IDE on skill load.

    Parameters
    ----------
    config : Dict
        Configuration from skill_manifest.yaml merged with user settings.
    """
    global _validator, _reporter
    _validator = BlockAtomicValidator(config)
    _reporter = IDEReporter(config)


def validate(
    file_path: str,
    content: Optional[str] = None,
    context: Optional[Dict] = None
) -> Dict:
    """
    Main validation entrypoint called by IDE.

    Parameters
    ----------
    file_path : str
        Path to RST file to validate.
    content : Optional[str]
        File content (if IDE hasn't saved yet).
    context : Optional[Dict]
        Additional context (project_root, tier, etc.).

    Returns
    -------
    Dict
        Validation result in Antigravity diagnostic format.

    Raises
    ------
    RuntimeError
        If validator not initialized.
    """
    if _validator is None:
        raise RuntimeError(
            "Validator not initialized. Call initialize() first."
        )

    path = Path(file_path)

    # If content provided, write to temp file for validation
    if content is not None:
        import tempfile
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.rst',
            delete=False
        ) as tmp:
            tmp.write(content)
            tmp_path = Path(tmp.name)

        result = _validator.validate_file(tmp_path)
        tmp_path.unlink()  # Clean up temp file

        # Update result path to original
        result.file_path = path
    else:
        result = _validator.validate_file(path)

    # Convert to IDE diagnostic format
    return _reporter.format_for_ide(result)


def validate_on_save(file_path: str) -> Dict:
    """
    Validation hook triggered on file save.

    Parameters
    ----------
    file_path : str
        Path to saved RST file.

    Returns
    -------
    Dict
        Validation result in IDE format.
    """
    return validate(file_path)


def validate_on_open(file_path: str) -> Dict:
    """
    Validation hook triggered on file open.

    Parameters
    ----------
    file_path : str
        Path to opened RST file.

    Returns
    -------
    Dict
        Validation result in IDE format.
    """
    return validate(file_path)


def validate_project(project_root: str) -> List[Dict]:
    """
    Validate all RST files in project.

    Called by IDE build/check commands.

    Parameters
    ----------
    project_root : str
        Root directory of DDR project.

    Returns
    -------
    List[Dict]
        List of validation results in IDE format.
    """
    if _validator is None:
        raise RuntimeError(
            "Validator not initialized. Call initialize() first."
        )

    root = Path(project_root)
    results = _validator.validate_project(root)

    return [_reporter.format_for_ide(result) for result in results]


def get_fix_suggestions(
    file_path: str,
    line_number: int
) -> List[Dict]:
    """
    Get auto-fix suggestions for violation at line.

    Called when user invokes "Quick Fix" in IDE.

    Parameters
    ----------
    file_path : str
        Path to RST file.
    line_number : int
        Line number with violation.

    Returns
    -------
    List[Dict]
        List of suggested fixes in IDE format.
    """
    if _validator is None:
        return []

    path = Path(file_path)
    result = _validator.validate_file(path)

    # Find violations at this line
    line_violations = [
        v for v in result.violations
        if v.line_number == line_number
    ]

    # Convert to IDE fix format
    fixes = []
    for violation in line_violations:
        if violation.fix_suggestion:
            fixes.append({
                'title': f"Fix: {violation.type.value}",
                'description': violation.fix_suggestion,
                'line': line_number,
                'type': violation.type.value
            })

    return fixes


def get_skill_status() -> Dict:
    """
    Get current skill status for IDE status bar.

    Returns
    -------
    Dict
        Status information.
    """
    return {
        'skill_name': 'block_atomic_validator',
        'version': '1.0.0',
        'initialized': _validator is not None,
        'status': 'ready' if _validator else 'not_initialized'
    }

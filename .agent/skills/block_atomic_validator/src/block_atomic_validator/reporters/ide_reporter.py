"""
IDE reporter for Antigravity IDE diagnostic format.

Implements: Conversion of validation results to IDE-native format
Requirements: Antigravity IDE 1.16.5+ diagnostic API
"""

from typing import Dict, List
from pathlib import Path

from ..core.models import ValidationResult, Violation, ViolationType


class IDEReporter:
    """
    Formats validation results for Antigravity IDE.

    Converts ValidationResult objects to IDE diagnostic format
    compatible with Antigravity 1.16.5+ diagnostic system.

    Parameters
    ----------
    config : Dict
        Configuration dictionary.
    """

    def __init__(self, config: Dict):
        """
        Initialize IDE reporter.

        Implements: Diagnostic formatting protocol
        """
        self.config = config

        # Map violation types to IDE severity levels
        self.severity_map = {
            'error': 'error',
            'warning': 'warning',
            'info': 'information',
            'hint': 'hint'
        }

        # Map violation types to diagnostic codes
        self.code_map = {
            ViolationType.ORDERING_VIOLATION: 'DDR001',
            ViolationType.MISSING_BLOCK_CITATION: 'DDR002',
            ViolationType.ORPHANED_ATOMIC: 'DDR003',
            ViolationType.PREFIX_MISMATCH: 'DDR004'
        }

    def format_for_ide(self, result: ValidationResult) -> Dict:
        """
        Convert ValidationResult to Antigravity diagnostic format.

        Parameters
        ----------
        result : ValidationResult
            Validation result to format.

        Returns
        -------
        Dict
            IDE-compatible diagnostic structure.
        """
        diagnostics = []

        for violation in result.violations:
            diagnostic = self._format_violation(violation)
            diagnostics.append(diagnostic)

        return {
            'file': str(result.file_path),
            'tier': result.tier,
            'total_tags': result.total_tags,
            'is_valid': result.is_valid,
            'summary': {
                'errors': result.error_count,
                'warnings': result.warning_count,
                'total_violations': len(result.violations)
            },
            'diagnostics': diagnostics
        }

    def _format_violation(self, violation: Violation) -> Dict:
        """
        Format single violation as IDE diagnostic.

        Parameters
        ----------
        violation : Violation
            Violation to format.

        Returns
        -------
        Dict
            IDE diagnostic object.
        """
        return {
            'code': self.code_map.get(violation.type, 'DDR000'),
            'severity': self.severity_map.get(
                violation.severity,
                'warning'
            ),
            'message': violation.message,
            'source': 'block_atomic_validator',
            'range': {
                'start': {
                    'line': violation.line_number,
                    'character': 0
                },
                'end': {
                    'line': violation.line_number,
                    'character': 9999  # End of line
                }
            },
            'relatedInformation': self._get_related_info(violation),
            'tags': self._get_diagnostic_tags(violation),
            'data': {
                'violation_type': violation.type.value,
                'tag_id': violation.tag_id,
                'related_tag_id': violation.related_tag_id,
                'fix_suggestion': violation.fix_suggestion
            }
        }

    def _get_related_info(self, violation: Violation) -> List[Dict]:
        """
        Generate related information for violation.

        Parameters
        ----------
        violation : Violation
            Violation to generate info for.

        Returns
        -------
        List[Dict]
            Related information entries.
        """
        related = []

        if violation.related_tag_id:
            related.append({
                'message': f"Related tag: {violation.related_tag_id}",
                'location': {
                    'uri': '',  # Same file
                    'range': {
                        'start': {'line': 0, 'character': 0},
                        'end': {'line': 0, 'character': 0}
                    }
                }
            })

        return related

    def _get_diagnostic_tags(self, violation: Violation) -> List[str]:
        """
        Get diagnostic tags for IDE rendering.

        Parameters
        ----------
        violation : Violation
            Violation to get tags for.

        Returns
        -------
        List[str]
            Diagnostic tags (e.g., 'unnecessary', 'deprecated').
        """
        tags = []

        # Add tags based on violation type
        if violation.type == ViolationType.ORPHANED_ATOMIC:
            tags.append('unnecessary')

        if violation.severity == 'warning':
            tags.append('warning')

        return tags

    def format_summary(self, results: List[ValidationResult]) -> Dict:
        """
        Generate project-wide validation summary.

        Parameters
        ----------
        results : List[ValidationResult]
            All validation results for project.

        Returns
        -------
        Dict
            Project summary.
        """
        total_files = len(results)
        valid_files = sum(1 for r in results if r.is_valid)
        total_errors = sum(r.error_count for r in results)
        total_warnings = sum(r.warning_count for r in results)

        # Group violations by type
        violation_counts = {}
        for result in results:
            for violation in result.violations:
                vtype = violation.type.value
                violation_counts[vtype] = violation_counts.get(vtype, 0) + 1

        return {
            'total_files': total_files,
            'valid_files': valid_files,
            'invalid_files': total_files - valid_files,
            'total_errors': total_errors,
            'total_warnings': total_warnings,
            'violation_breakdown': violation_counts,
            'status': 'valid' if valid_files == total_files else 'invalid'
        }

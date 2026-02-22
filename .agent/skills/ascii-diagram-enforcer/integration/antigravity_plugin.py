"""
Antigravity IDE Plugin Interface

Bridges ASCII Diagram Enforcer with Antigravity IDE 1.16.5+ plugin system.
Provides real-time validation, gutter icons, quick fixes, and reconciliation
integration.

Implements: Antigravity IDE plugin interface
Requirements: Antigravity IDE 1.16.5+ API

Author: DDR System Integration Team
Version: 1.0.0
"""

import logging
from typing import List, Dict, Optional, Callable
from pathlib import Path

# Antigravity IDE API imports (assumed available in IDE environment)
try:
    from antigravity.plugin import SkillPlugin, SkillContext
    from antigravity.editor import Document, TextRange, Annotation
    from antigravity.actions import QuickFix, EditorAction
    from antigravity.events import DocumentEvent, SaveEvent
except ImportError:
    # Fallback for development/testing without IDE
    class SkillPlugin: pass
    class SkillContext: pass
    class Document: pass
    class TextRange: pass
    class Annotation: pass
    class QuickFix: pass
    class EditorAction: pass
    class DocumentEvent: pass
    class SaveEvent: pass

from ..src.enforcer import ASCIIDiagramEnforcer, ValidationResult, ViolationSeverity


logger = logging.getLogger(__name__)


class ASCIIDiagramEnforcerPlugin(SkillPlugin):
    """
    Antigravity IDE plugin for ASCII Diagram Enforcer Skill.

    Integrates real-time validation, inline annotations, gutter icons, and
    quick-fix actions for SAD-tier ASCII diagram enforcement.

    Parameters
    ----------
    context : SkillContext
        IDE plugin context providing access to editor, filesystem, etc.

    Attributes
    ----------
    enforcer : ASCIIDiagramEnforcer
        Core validation engine.
    active_documents : Dict[str, ValidationResult]
        Cache of validation results per document path.

    Notes
    -----
    Plugin lifecycle hooks:
    - on_activate(): Plugin initialization
    - on_deactivate(): Cleanup
    - on_document_opened(): Document load validation
    - on_document_changed(): Real-time validation
    - on_before_save(): Pre-save blocking validation
    """

    def __init__(self, context: SkillContext):
        """
        Initialize plugin with IDE context.

        Implements: Plugin initialization hook
        Requirements: Antigravity Plugin API
        """
        super().__init__(context)
        self.context = context

        # Load configuration from skill.yaml
        config = context.get_config()
        self.enforcer = ASCIIDiagramEnforcer(
            strict_mode=config.get('strict_mode', True),
            min_diagram_lines=config.get('min_diagram_lines', 3),
            auto_flag_dirty=config.get('auto_flag_dirty', True)
        )

        self.active_documents: Dict[str, ValidationResult] = {}

        logger.info("ASCII Diagram Enforcer Plugin initialized")

    def on_activate(self):
        """
        Plugin activation hook.

        Register event handlers, commands, and UI elements.
        """
        logger.info("Activating ASCII Diagram Enforcer Plugin")

        # Register commands
        self.context.register_command(
            command_id="ddr:validate-ascii-diagrams",
            handler=self._cmd_validate_diagrams,
            label="DDR: Validate ASCII Diagrams",
            keybinding="Ctrl+Shift+D"
        )

        self.context.register_command(
            command_id="ddr:insert-diagram-template",
            handler=self._cmd_insert_template,
            label="DDR: Insert ASCII Diagram Template",
            keybinding="Ctrl+Alt+D"
        )

        # Register event listeners
        self.context.on('document.opened', self._on_document_opened)
        self.context.on('document.changed', self._on_document_changed)
        self.context.on('document.before_save', self._on_before_save)

        logger.info("Plugin activated successfully")

    def on_deactivate(self):
        """
        Plugin deactivation hook.

        Clean up resources and unregister handlers.
        """
        logger.info("Deactivating ASCII Diagram Enforcer Plugin")
        self.active_documents.clear()

    def _on_document_opened(self, event: DocumentEvent):
        """
        Handle document open event.

        Validate if document is SAD-tier RST file.

        Parameters
        ----------
        event : DocumentEvent
            Document event containing document reference.
        """
        doc = event.document

        # Only validate SAD-tier files
        if not self._is_sad_document(doc):
            return

        logger.info(f"Validating opened SAD document: {doc.path}")
        self._validate_document(doc)

    def _on_document_changed(self, event: DocumentEvent):
        """
        Handle document change event (real-time validation).

        Debounced to avoid excessive validation on each keystroke.

        Parameters
        ----------
        event : DocumentEvent
            Document change event.
        """
        doc = event.document

        if not self._is_sad_document(doc):
            return

        # Debounce: validate after 500ms of inactivity
        self.context.debounce(
            key=f"validate_{doc.path}",
            delay_ms=500,
            callback=lambda: self._validate_document(doc)
        )

    def _on_before_save(self, event: SaveEvent) -> bool:
        """
        Handle pre-save validation (blocking).

        In strict mode, prevents save if ERROR-level violations exist.

        Parameters
        ----------
        event : SaveEvent
            Save event with document reference.

        Returns
        -------
        bool
            True to allow save, False to block.
        """
        doc = event.document

        if not self._is_sad_document(doc):
            return True  # Allow save for non-SAD documents

        logger.info(f"Pre-save validation for: {doc.path}")
        result = self._validate_document(doc)

        # In strict mode, block save on ERROR violations
        if self.enforcer.strict_mode and not result.is_valid:
            error_count = sum(
                1 for v in result.violations
                if v.severity == ViolationSeverity.ERROR
            )

            # Show blocking dialog
            self.context.show_error(
                title="ASCII Diagram Violations",
                message=(
                    f"Cannot save: {error_count} ERROR-level violation(s) found.\n\n"
                    f"Fix violations or disable strict mode in skill configuration."
                ),
                actions=[
                    ("View Details", lambda: self._show_violation_panel(result)),
                    ("Cancel Save", None)
                ]
            )

            return False  # Block save

        return True  # Allow save

    def _validate_document(self, doc: Document) -> ValidationResult:
        """
        Validate document and update UI annotations.

        Parameters
        ----------
        doc : Document
            Document to validate.

        Returns
        -------
        ValidationResult
            Validation results.
        """
        content = doc.get_text()
        section_id = self._extract_section_id(doc)

        # Run validation
        result = self.enforcer.validate_section(content, section_id)

        # Cache result
        self.active_documents[doc.path] = result

        # Update UI
        self._update_annotations(doc, result)
        self._update_gutter_icons(doc, result)

        logger.info(
            f"Validation complete: {doc.path} - "
            f"Valid={result.is_valid}, Violations={len(result.violations)}"
        )

        return result

    def _update_annotations(self, doc: Document, result: ValidationResult):
        """
        Add inline error/warning annotations to document.

        Parameters
        ----------
        doc : Document
            Target document.
        result : ValidationResult
            Validation results.
        """
        # Clear existing annotations from this plugin
        doc.clear_annotations(source="ascii_diagram_enforcer")

        for violation in result.violations:
            # Map severity to annotation type
            if violation.severity == ViolationSeverity.ERROR:
                annotation_type = "error"
            elif violation.severity == ViolationSeverity.WARNING:
                annotation_type = "warning"
            else:
                annotation_type = "info"

            # Create annotation
            annotation = Annotation(
                type=annotation_type,
                message=violation.description,
                line=violation.line_number,
                source="ascii_diagram_enforcer",
                code=violation.rule_id
            )

            # Add quick fixes if available
            if violation.suggested_fix:
                annotation.add_quick_fix(
                    QuickFix(
                        label=violation.suggested_fix,
                        action=self._create_quick_fix_action(doc, violation)
                    )
                )

            doc.add_annotation(annotation)

    def _update_gutter_icons(self, doc: Document, result: ValidationResult):
        """
        Add gutter icons for violations.

        Parameters
        ----------
        doc : Document
            Target document.
        result : ValidationResult
            Validation results.
        """
        # Clear existing gutter icons
        doc.clear_gutter_icons(source="ascii_diagram_enforcer")

        for violation in result.violations:
            icon_type = (
                "error" if violation.severity == ViolationSeverity.ERROR
                else "warning"
            )

            doc.add_gutter_icon(
                line=violation.line_number,
                icon=icon_type,
                tooltip=violation.description,
                source="ascii_diagram_enforcer"
            )

    def _create_quick_fix_action(
        self,
        doc: Document,
        violation: Violation
    ) -> Callable:
        """
        Create quick fix action for violation.

        Parameters
        ----------
        doc : Document
            Target document.
        violation : Violation
            Violation to fix.

        Returns
        -------
        Callable
            Quick fix action handler.
        """
        def apply_fix():
            if violation.rule_id == "SAD-DIAGRAM-001":
                # Missing diagram: insert template
                self._insert_diagram_template_at_line(doc, violation.line_number)
            elif violation.rule_id == "SAD-DIAGRAM-003":
                # Missing relationships: show examples
                self._show_diagram_examples()

        return apply_fix

    def _cmd_validate_diagrams(self):
        """Command handler: Manual validation trigger."""
        doc = self.context.get_active_document()
        if not doc:
            return

        if not self._is_sad_document(doc):
            self.context.show_info(
                "Current document is not a SAD-tier file",
                "ASCII Diagram Enforcer only validates SAD-tier documentation."
            )
            return

        result = self._validate_document(doc)
        self._show_violation_panel(result)

    def _cmd_insert_template(self):
        """Command handler: Insert diagram template."""
        doc = self.context.get_active_document()
        if not doc:
            return

        cursor_line = doc.get_cursor_position().line
        self._insert_diagram_template_at_line(doc, cursor_line)

    def _insert_diagram_template_at_line(self, doc: Document, line: int):
        """
        Insert ASCII diagram template at specified line.

        Parameters
        ----------
        doc : Document
            Target document.
        line : int
            Line number for insertion.
        """
        template = """
+-------------------+          +-------------------+
|   Component A     | -------> |   Component B     |
+-------------------+          +-------------------+
"""

        doc.insert_text(line, template)
        self.context.show_info(
            "Diagram template inserted",
            "Customize the template for your architecture."
        )

    def _show_diagram_examples(self):
        """Show panel with ASCII diagram examples."""
        examples_path = Path(__file__).parent.parent / "tests" / "test_data" / "sample_diagrams.txt"

        if examples_path.exists():
            content = examples_path.read_text()
            self.context.show_panel(
                title="ASCII Diagram Examples",
                content=content,
                syntax="text"
            )
        else:
            self.context.show_info(
                "Examples not found",
                "Sample diagrams file is missing from installation."
            )

    def _show_violation_panel(self, result: ValidationResult):
        """
        Display detailed violation report in IDE panel.

        Parameters
        ----------
        result : ValidationResult
            Validation results to display.
        """
        report = self.enforcer.generate_report(result)

        self.context.show_panel(
            title="ASCII Diagram Validation Report",
            content=report,
            syntax="text",
            location="bottom"
        )

    def _is_sad_document(self, doc: Document) -> bool:
        """
        Check if document is SAD-tier RST file.

        Parameters
        ----------
        doc : Document
            Document to check.

        Returns
        -------
        bool
            True if SAD-tier document.
        """
        path = Path(doc.path)

        # Check file location and extension
        return (
            path.suffix in ['.rst', '.md'] and
            '04_sad' in path.parts
        )

    def _extract_section_id(self, doc: Document) -> str:
        """
        Extract section ID from document path.

        Parameters
        ----------
        doc : Document
            Document to extract from.

        Returns
        -------
        str
            Section identifier (e.g., 'sad-root').
        """
        path = Path(doc.path)
        return f"sad-{path.stem}"

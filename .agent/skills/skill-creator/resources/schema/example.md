---
name: generate-pyside6-ui-widget
description: Generates a complete, responsive PySide6 widget or layout component, integrating native SVG rendering, specifically architected for the Maggie software application.
# HUMAN CONTEXT: This example demonstrates advanced agentic capabilities
# by utilizing progressive disclosure (triggering only when UI generation is requested),
# context-first XML fencing (separating triggers from execution logic),
# and silent reasoning checkpoints (ensuring PySide6 and asset constraints are met
# before emitting code) to maintain a highly optimized context window.
---

<when_to_use>

- The developer requests the creation, refactoring, or modernization of a user interface element.
- The prompt contains keywords such as: "widget", "PySide6", "UI", "layout", or "interface".
- The active task involves building visual components for the Maggie application frontend.
</when_to_use>

<how_to_use>

1. **Context Verification (Silent):** Confirm the required PySide6 modules (e.g., `QtWidgets`, `QtGui`, `QtSvg`) are available in the workspace context.
2. **Design Blueprinting (Silent):** Plan the widget hierarchy, prioritizing non-blocking UI patterns and responsive layouts (e.g., `QVBoxLayout`, `QGridLayout`).
3. **Asset Integration:** If icons or vector graphics are required, strictly utilize SVG formats rendered via `QSvgWidget` or `QIcon` to ensure lossless scaling across different monitor resolutions and maintain the application's visual fidelity.
4. **Code Generation:** Emit the production-ready Python code within a fenced code block. Ensure all classes inherit from the appropriate PySide6 base classes and include comprehensive type hints.
5. **Verification Artifact:** Output a brief, Markdown-formatted summary of the signals and slots implemented for the developer to review and approve.
</how_to_use>

<constraints>
- Never utilize synchronous blocking calls (e.g., `time.sleep()`) within the main GUI thread; you must rely on `QThread` or `QTimer` for asynchronous operations to keep the Maggie UI responsive.
- Do not hardcode absolute pixel dimensions; utilize dynamic sizing, spacers, and stretch factors.
- All emitted code must be fully type-hinted and production-ready. Do not generate placeholder logic.
</constraints>

<resources_reference>

- `ui_templates/maggie_base_widget.py`
- `assets/svg_icons/`
</resources_reference>

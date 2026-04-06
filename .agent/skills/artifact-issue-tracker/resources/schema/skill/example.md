---
name: generate-pyside6-ui-widget
version: 1.0.0
description: Generates responsive PySide6 widgets and layout components for the Maggie application. Use when the task is to create or refactor a PySide6 widget, dialog, or layout for Maggie UI work. Do not use for backend-only logic changes or generic Python refactors unrelated to the user interface.
---

<when_to_use>

- Use when the developer requests a new or refactored PySide6 widget, dialog, panel, or layout for the Maggie application.
- Use when the prompt mentions `PySide6`, `QtWidgets`, `QDialog`, `layout`, `widget`, or another Maggie UI component.
- Do not use when the request is limited to backend services, data models, or generic Python cleanup without UI changes.
- Example prompt: "Create a PySide6 settings dialog for Maggie."
- Example prompt: "Refactor this Maggie widget to use a responsive grid layout."
</when_to_use>

<how_to_use>

1. Confirm the target UI surface, required inputs, and expected user-visible behavior before generating code.
2. Check whether the relevant PySide6 modules and any required assets are available in the workspace.
3. Plan the widget hierarchy, layout strategy, and signal-slot interactions using the smallest structure that satisfies the request.
4. Generate production-ready code with explicit imports, concrete widget behavior, and no placeholder logic.
5. Verify the output by summarizing the created widget structure and the user interactions it supports.
</how_to_use>

<constraints>
- Do not use blocking calls in the main GUI thread when a non-blocking Qt alternative is available.
- Do not hardcode brittle pixel dimensions when layouts, spacers, or stretch factors can express the same intent.
- Do not emit placeholder methods, fake assets, or TODO-only business logic.
</constraints>

<resources_reference>

- Read `resources/ui_conventions.md` to apply Maggie-specific UI rules and layout conventions.
- Run `scripts/preview_widget.py` to render the generated widget for verification when a preview workflow exists.
</resources_reference>

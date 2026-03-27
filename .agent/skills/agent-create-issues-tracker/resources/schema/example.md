---
name: issues-tracker-init
description: Initializes a new blank Issues Tracker markdown file from the shared template when the user asks for a fresh tracker.
---

<when_to_use>

- The user asks to initialize a new Issues Tracker.
- The task needs a blank tracker, not a populated issue list or resolution report.
</when_to_use>

<how_to_use>

1. Resolve `SUBJECT_SYSTEM_NAME`, `AUTHOR_NAME`, and `OUTPUT_PATH`.
2. Read `.agent/schemas/issues-tracker/template.md`.
3. Replace only the supported placeholders.
4. Refuse to overwrite an existing target unless explicit approval is present.
5. Validate the written file with the local validator before returning success.
</how_to_use>

<constraints>

- Do not fabricate issues.
- Do not leave unresolved placeholders.
- Keep the output scoped to blank initialization.
</constraints>

# Naming Migration Map

This document records the Antigravity asset naming migration from underscore-based naming to kebab-case.

## Scope

- `.agent/rules/*.md`
- `.agent/workflows/*.md`
- `.agent/personas/*.mdc`
- `.agent/skills/*/`

## Conversion Rule

- `snake_case`/underscore names in Antigravity config assets were renamed to `kebab-case`.
- Python source files were intentionally left in `snake_case`.
- Skill static documentation directories `references/` were migrated to `resources/` where present.

## Compatibility Note

External automation that still references legacy underscore names should be updated to kebab-case paths.

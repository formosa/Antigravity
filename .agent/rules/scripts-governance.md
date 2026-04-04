---
name: "scripts-governance"
description: "Glob-scoped collection governance rule for the `.agent/scripts/` directory, covering live script inventory accuracy, generated root and tests indexes, compiled-artifact exclusion, and alignment between script implementations and linked tool definitions."
version: "1.0.0"
trigger: "glob"
globs: ".agent/scripts/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. Scope Boundary: This rule governs only assets under `.agent/scripts/`, including the root scripts directory, the `.agent/scripts/tests/` subtree, and the generated `index.md` files in both locations.
2. Root Inventory Boundary: `.agent/scripts/index.md` MUST inventory only live root-level Python scripts under `.agent/scripts/`. It MUST exclude `__init__.py`, generated index files, compiled artifacts, caches, and files inside `.agent/scripts/tests/`.
3. Tests Inventory Boundary: `.agent/scripts/tests/index.md` MUST inventory only live Python files under `.agent/scripts/tests/`. It MUST exclude generated index files, compiled artifacts, caches, and non-Python files.
4. Generated Index Contract: Both script index files MUST remain deterministic generated discovery indexes with the standard full-form section order: `Use This Index`, `Selection Map`, `Manifest`, detailed records, `Category Totals`, and `Index Boundaries`.
5. Tool Alignment Required: When a root script is referenced by a tool definition under `.agent/tools/`, the root scripts index MUST link that script to the matching tool definition. Scripts without a matching tool definition MUST NOT invent one.
6. Live Files Only: Script indexes and any supporting generation logic MUST reflect only files that currently exist in the repository. They MUST NOT retain stale references to removed scripts or tests.
7. Compiled Artifact Exclusion: Agents MUST NOT index, document, or rely on entries under `__pycache__/` or compiled Python artifacts such as `.pyc` files as durable script assets.
8. Tests Naming Boundary: The governed test subtree is `.agent/scripts/tests/`. Agents MUST NOT introduce parallel `test/` naming for this directory family.
9. Internal Generator Ownership: `.agent/scripts/update_index.py` is an internal maintenance utility for scripts-index regeneration. It MUST be inventoried as a root script but MUST NOT be exposed as a separate tool definition unless a later task explicitly adds one.

</constraints>

<verification_step>

1. Confirm the target change stays within `.agent/scripts/` or the corresponding scripts governance rule surface under `.agent/rules/`.
2. Regenerate the root and tests script indexes and confirm each index inventories only the files within its governed boundary.
3. Confirm the generated indexes exclude `__init__.py`, `index.md`, `__pycache__/`, `.pyc`, and any removed scripts.
4. Confirm every linked tool definition in the root scripts index points to a real `.agent/tools/*.md` file whose command references the indexed script implementation.
5. Confirm `.agent/scripts/tests/` remains the only governed tests subtree name and that no live discovery path still points to the retired underscore-prefixed legacy scripts index.

</verification_step>

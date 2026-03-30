---
name: codex-brainstorm
description: Creates, seeds, validates, and updates the DDR App Framework brainstorming compendium in `brainstorm.md` using the governed `BRAIN-ENTRY-1.0` Markdown format. Use when Codex must capture or reorganize DDR App Framework ideas, architectural hypotheses, OSS library candidates, or repair the canonical brainstorm document derived from the v6.3 reference source.
---

<when_to_use>

- The user asks to create, initialize, seed, repair, validate, or update `brainstorm.md`.
- The task is to capture a new DDR App Framework idea, design hypothesis, workflow concept, or library candidate in the governed brainstorm compendium.
- The brainstorm document is missing and must be created from the canonical DDR App Framework reference source.
- The brainstorm document exists but needs structural cleanup, ID assignment, section placement, or field completion before new ideas are appended.
</when_to_use>

<how_to_use>

1. Resolve inputs before editing:
   - Optional: `BRAINSTORM_PATH` (default `brainstorm.md`)
   - Optional: `MODE` (`auto` by default)
   - Optional: `SOURCE_REFERENCE_PATH` (default `.agent/skills/codex-brainstorm/resources/DDR_AppFramework_Brainstorm.docx`)
   - Required for updates: the user-provided idea content or library candidate details
   - Optional for updates: target section, category, status, and priority hints
2. Run pre-flight checks:
   - If `MODE` is `auto` and `BRAINSTORM_PATH` does not exist, initialize it with:
     - `python .agent/skills/codex-brainstorm/scripts/init_brainstorm.py <BRAINSTORM_PATH> --source-reference <SOURCE_REFERENCE_PATH>`
   - If the target already exists and initialization was explicitly requested, require overwrite approval before replacing it.
   - Read `## PART I — Document Manifest` before changing any entry content.
   - Read `.agent/schemas/brainstorm/README.md` and `.agent/schemas/brainstorm/brainstorm.d.ts` for the canonical field contract.
3. Apply update rules:
   - Treat Part I as governed manifest content. Only update controlled metadata such as `Last Revised` and explicit Part Registry additions.
   - Add `IDEA` entries only under Part II and `LIB` entries only under Part III.
   - Assign the next sequential `BRAIN-II-###` or `BRAIN-III-###` identifier. Never renumber or delete an existing entry.
   - Preserve canonical seeded entries. Extend the document by appending or revising entries in place.
   - Populate every required field. Use `TBD` only for genuinely unknown values that cannot yet be resolved.
4. Validate after every write:
   - `python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py <BRAINSTORM_PATH>`
   - If a pre-edit snapshot is available and append-only enforcement is needed, add:
     - `--baseline <PRE_EDIT_PATH>`
   - If validation fails, halt and return the exact validator failure.
5. Return one concise success line with the updated path after validation passes.

Examples:

- Initialize:
  - `python .agent/skills/codex-brainstorm/scripts/init_brainstorm.py brainstorm.md --source-reference .agent/skills/codex-brainstorm/resources/DDR_AppFramework_Brainstorm.docx`
- Validate:
  - `python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md`
</how_to_use>

<constraints>

- Do not treat brainstorm entries as authoritative engineering decisions; promoted ideas belong in ADRs or the formal DDR specification.
- Do not invent category IDs, status values, priority values, tier references, or extension IDs outside the controlled vocabularies.
- Do not remove or rename existing `BRAIN-II-###` or `BRAIN-III-###` identifiers.
- Do not move a `LIB` entry into Part II or an `IDEA` entry into Part III.
- Do not overwrite an existing brainstorm document during initialization without explicit approval.
- Do not rewrite Part I prose during routine entry maintenance beyond controlled metadata updates and explicit registry changes.
</constraints>

<resources_reference>

- `.agent/schemas/brainstorm/README.md`
- `.agent/schemas/brainstorm/brainstorm.d.ts`
- `.agent/schemas/brainstorm/seed.md`
- `.agent/skills/codex-brainstorm/scripts/init_brainstorm.py`
- `.agent/skills/codex-brainstorm/scripts/validate_brainstorm.py`
- `.agent/skills/codex-brainstorm/resources/DDR_AppFramework_Brainstorm.docx`
</resources_reference>

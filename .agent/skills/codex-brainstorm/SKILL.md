---
name: codex-brainstorm
version: 1.0.2
description: Creates, seeds, validates, and updates the DDR App Framework brainstorming compendium in `brainstorm.md` using the governed `BRAIN-ENTRY-1.1` Markdown format, visual semantics, structured citations, and stable Mermaid diagrams. Use when the task is to capture or reorganize brainstorm ideas, architectural hypotheses, or library candidates. Do not use when the task is to finalize normative spec text or write an implementation plan.
---

<when_to_use>

- The user asks to create, initialize, seed, repair, validate, or update `brainstorm.md`.
- The task is to capture a new DDR App Framework idea, design hypothesis, workflow concept, or library candidate in the governed brainstorm compendium.
- The brainstorm document is missing and must be created from the canonical DDR App Framework reference source.
- The brainstorm document exists but needs structural cleanup, ID assignment, section placement, field completion, citation repair, or visual-semantics normalization before new ideas are appended.
- Do not use this skill when the request is to produce a final specification artifact or a task-by-task implementation plan.
- Example prompt: "Add a new brainstorm entry for a DAG diff visualizer to brainstorm.md."
- Example prompt: "Repair brainstorm.md, normalize IDs and citations, and append this new workflow idea."
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
   - Read `resources/schema/brainstorm/README.md` and `resources/schema/brainstorm/brainstorm.d.ts` for the canonical field contract.
3. Run the evidence pass before drafting substantive content:
   - For every new or materially revised assertion, recommendation, or factual comparison, gather supporting evidence from current online sources.
   - Prefer this source hierarchy in order:
     - Official vendor or project documentation, release notes, or repository releases
     - Standards bodies, government sources, or academic publications
     - Reputable secondary analysis only as supporting context
   - Do not use anonymous forums, social threads, or aggregators as the final authority for brainstorm claims.
   - Treat a source as `CURRENT` only when it was published or materially updated within 183 days of the entry `revised_date`.
   - Older evergreen sources may supplement a claim, but they must not be the only support for a new recommendation or factual assertion.
4. Apply update rules:
   - Treat Part I as governed manifest content. Only update controlled metadata such as `Last Revised`, the Font Color Index, the citation catalog, and explicit Part Registry additions.
   - Add `IDEA` entries only under Part II and `LIB` entries only under Part III.
   - Assign the next sequential `BRAIN-II-###` or `BRAIN-III-###` identifier. Never renumber or delete an existing entry.
   - Preserve canonical seeded entries. Extend the document by appending or revising entries in place.
   - Populate every required field, including `citation_ids`. Use `TBD` only for genuinely unknown values that cannot yet be resolved.
   - Limit `references` to ADR IDs, spec sections, local artifact paths, or related brainstorm IDs. External bibliography belongs in the citation catalog.
   - Add inline `[C#]` markers inside long-form prose whenever the entry makes an assumption, assertion, or recommendation.
   - Use only the governed visual classes: `brain-governance`, `brain-evidence`, `brain-hypothesis`, `brain-recommendation`, and `brain-risk`.
   - Use `<span class="...">` tags only for short badges, labels, and callouts. Do not wrap entire paragraphs or YAML keys.
   - Prefer advanced but stable Mermaid blocks: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, and `erDiagram`, with `accTitle` and `accDescr` in every diagram.
5. Validate after every write:
   - `python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py <BRAINSTORM_PATH>`
   - To surface non-fatal quality gaps as warnings, add:
     - `--audit`
   - If a pre-edit snapshot is available and append-only enforcement is needed, add:
     - `--baseline <PRE_EDIT_PATH>`
   - If validation fails, halt and return the exact validator failure.
6. Return one concise success line with the updated path after validation passes. If `--audit` reports warnings, mention that the document passed validation with follow-up recommendations.

Examples:

- Initialize:
  - `python .agent/skills/codex-brainstorm/scripts/init_brainstorm.py brainstorm.md --source-reference .agent/skills/codex-brainstorm/resources/DDR_AppFramework_Brainstorm.docx`
- Validate:
  - `python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md`
- Validate with audit:
  - `python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md --audit`
</how_to_use>

<constraints>

- Do not treat brainstorm entries as authoritative engineering decisions; promoted ideas belong in ADRs or the formal DDR specification.
- Do not invent category IDs, status values, priority values, tier references, extension IDs, citation IDs, or authority types outside the controlled vocabularies.
- Do not remove or rename existing `BRAIN-II-###` or `BRAIN-III-###` identifiers.
- Do not move a `LIB` entry into Part II or an `IDEA` entry into Part III.
- Do not overwrite an existing brainstorm document during initialization without explicit approval.
- Do not rewrite Part I prose during routine entry maintenance beyond controlled metadata updates, explicit registry changes, the governed citation catalog, and the governed visual-semantics sections.
- Do not leave a substantive new claim supported only by uncited prose, stale-only evidence, or an external URL embedded directly in `references`.
- Do not commit renderer-specific Mermaid syntax such as `architecture-beta`, ELK-only directives, or other unstable extensions into the governed document.
</constraints>

<resources_reference>

- Read `resources/schema/brainstorm/README.md` to confirm brainstorm governance and entry semantics.
- Read `resources/schema/brainstorm/brainstorm.d.ts` to verify the active brainstorm artifact contract.
- Read `resources/schema/brainstorm/seed.md` to preserve the canonical seeded structure and section conventions.
- Run `.agent/skills/codex-brainstorm/scripts/init_brainstorm.py` when the governed brainstorm document must be initialized from scratch.
- Run `.agent/skills/codex-brainstorm/scripts/validate_brainstorm.py` after edits to confirm structural validity.
- Read `.agent/skills/codex-brainstorm/resources/DDR_AppFramework_Brainstorm.docx` as the canonical source reference when seeding or repairing the compendium.
</resources_reference>

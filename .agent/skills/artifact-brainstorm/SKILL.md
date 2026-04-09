---
name: artifact-brainstorm
version: 1.0.3
description: Serves as the Artifact-Centric Owner for Antigravity brainstorm artifacts by creating, seeding, repairing, validating, and auditing governed `brainstorm.md` compendia against the canonical `brainstorm` schema, citation protocol, and Mermaid/visual-semantics rules. Use when the task is to create or maintain a governed brainstorm artifact or its entry content. Do not use when the task is to author the canonical brainstorm schema, finalize normative spec text, or write an implementation plan.
---

<when_to_use>

- The user asks to create, initialize, seed, repair, validate, audit, or update `brainstorm.md`.
- The task is to capture or reorganize brainstorm entries such as design ideas, architectural hypotheses, workflow concepts, or library candidates inside the governed brainstorm artifact.
- The brainstorm artifact is missing and must be initialized from the canonical seed and schema-owned source reference.
- The brainstorm artifact exists but needs structural cleanup, citation repair, ID assignment, section placement, field completion, or visual-semantics normalization before new entries are appended.
- Do not use this skill when the request is to change `.agent/schemas/brainstorm/` itself, redefine the brainstorm contract, produce a final specification artifact, or write a task-by-task implementation plan.
- Example prompt: "Add a new brainstorm entry for a DAG diff visualizer to brainstorm.md."
- Example prompt: "Repair brainstorm.md, normalize IDs and citations, and append this new workflow idea."
- Example prompt: "Initialize a governed brainstorm artifact from the canonical seed and validate it."

</when_to_use>

<how_to_use>

## Operating mode

- **Owner subtype:** `Artifact-Centric Owner` for the `brainstorm` artifact family.
- **Owned artifact surface:** `brainstorm.md` by default, or an explicitly supplied alternate path.
- **Canonical schema authority:** `.agent/schemas/brainstorm/`.
- **Reference source:** `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml`.

## Deterministic protocol

1. Resolve inputs before editing:
   - Optional: `BRAINSTORM_PATH` (default `brainstorm.md`)
   - Optional: `MODE` (`auto` by default)
   - Optional: `SOURCE_REFERENCE_PATH` (default `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml`)
   - Required for updates: user-provided idea content, library candidate details, or requested repair objective
   - Optional for updates: target section, category, status, priority, or baseline snapshot path
2. Load the local contract surfaces:
   - Read `.agent/schemas/brainstorm/README.md` and `.agent/schemas/brainstorm/brainstorm.d.ts` first.
   - Read `resources/schema/brainstorm/README.md` and `resources/schema/brainstorm/brainstorm.d.ts` only as packaged mirrors after consulting the canonical schema.
   - Read `## PART I â€” Document Manifest` in the target artifact before changing any entry content.
3. Apply hard RFQ or halt gates before mutation:
   - If the request asks to redefine the canonical brainstorm schema and author or repair the final brainstorm artifact in the same pass, halt and route schema work through `core-schema` first.
   - If explicit initialization would overwrite an existing brainstorm artifact, require overwrite approval before replacing it.
   - If the target artifact path or intended operation is ambiguous enough that proceeding would silently redefine the owned artifact boundary, halt and request clarification.
   - If the canonical seed or source reference is missing, halt and return the exact missing-path failure.
4. Initialize or open the owned artifact:
   - If `MODE` is `auto` and `BRAINSTORM_PATH` does not exist, initialize it with:
     - `python .agent/skills/artifact-brainstorm/scripts/init_brainstorm.py <BRAINSTORM_PATH> --source-reference <SOURCE_REFERENCE_PATH>`
   - Otherwise open the existing artifact in place and preserve append-only ID governance.
5. Run the evidence pass before drafting substantive content:
   - For every new or materially revised assertion, recommendation, or factual comparison, gather supporting evidence from current online sources.
   - Prefer official vendor or project documentation, release notes, repository releases, standards bodies, government sources, or academic publications.
   - Use reputable secondary analysis only as supporting context.
   - Do not use anonymous forums, social threads, or aggregators as the final authority for brainstorm claims.
   - Treat a source as `CURRENT` only when it was published or materially updated within 183 days of the entry `revised_date`.
6. Apply owner-managed update rules:
   - Treat Part I as governed manifest content. Only update controlled metadata such as `Last Revised`, the Font Color Index, the citation catalog, and explicit Part Registry additions.
   - Add `IDEA` entries only under Part II and `LIB` entries only under Part III.
   - Assign the next sequential `BRAIN-II-###` or `BRAIN-III-###` identifier. Never renumber or delete an existing entry.
   - Preserve canonical seeded entries. Extend the artifact by appending or revising entries in place.
   - Populate every required field, including `citation_ids`. Use `TBD` only for genuinely unknown values that cannot yet be resolved.
   - Limit `references` to ADR IDs, spec sections, local artifact paths, or related brainstorm IDs. External bibliography belongs in the citation catalog.
   - Add inline `[C#]` markers inside long-form prose whenever the entry makes an assumption, assertion, or recommendation.
   - Use only the governed visual classes: `brain-governance`, `brain-evidence`, `brain-hypothesis`, `brain-recommendation`, and `brain-risk`.
   - Use `<span class="...">` tags only for short badges, labels, and callouts. Do not wrap entire paragraphs or YAML keys.
   - Prefer stable Mermaid blocks: `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, and `erDiagram`, with `accTitle` and `accDescr` in every diagram.
7. Validate after every write:
   - `python .agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py <BRAINSTORM_PATH>`
   - Add `--audit` to surface non-fatal quality gaps as warnings.
   - Add `--baseline <PRE_EDIT_PATH>` when append-only preservation against a prior snapshot must be enforced.
   - If validation fails, halt and return the exact validator failure.
8. Return one concise success line with the updated artifact path after validation passes. If `--audit` reports warnings, mention that the artifact passed validation with follow-up recommendations.

Examples:

- Initialize:
  - `python .agent/skills/artifact-brainstorm/scripts/init_brainstorm.py brainstorm.md --source-reference .agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml`
- Validate:
  - `python .agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py brainstorm.md`
- Validate with audit:
  - `python .agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py brainstorm.md --audit`

</how_to_use>

<constraints>

- Do not treat brainstorm entries as authoritative engineering decisions; promoted ideas belong in ADRs or the formal DDR specification.
- Do not author or revise `.agent/schemas/brainstorm/` through this skill; canonical schema work belongs to `core-schema`.
- Do not invent category IDs, status values, priority values, tier references, extension IDs, citation IDs, or authority types outside the controlled vocabularies.
- Do not remove or rename existing `BRAIN-II-###` or `BRAIN-III-###` identifiers.
- Do not move a `LIB` entry into Part II or an `IDEA` entry into Part III.
- Do not overwrite an existing brainstorm artifact during initialization without explicit approval.
- Do not rewrite Part I prose during routine entry maintenance beyond controlled metadata updates, explicit registry changes, the governed citation catalog, and the governed visual-semantics sections.
- Do not leave a substantive new claim supported only by uncited prose, stale-only evidence, or an external URL embedded directly in `references`.
- Do not commit renderer-specific Mermaid syntax such as `architecture-beta`, ELK-only directives, or other unstable extensions into the governed artifact.

</constraints>

<resources_reference>

- Read `.agent/schemas/brainstorm/README.md` to confirm canonical brainstorm governance, ownership metadata, and artifact semantics.
- Read `.agent/schemas/brainstorm/brainstorm.d.ts` to verify the active brainstorm artifact contract.
- Read `.agent/schemas/brainstorm/seed.md` to preserve the canonical seeded structure and section conventions.
- Read `resources/schema/brainstorm/README.md` only as the packaged mirror bundled with this skill after consulting the canonical schema.
- Run `.agent/skills/artifact-brainstorm/scripts/init_brainstorm.py` when the governed brainstorm artifact must be initialized from scratch.
- Run `.agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py` after edits to confirm structural validity.
- Read `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml` as the schema-owned source reference when seeding or repairing the compendium.

</resources_reference>

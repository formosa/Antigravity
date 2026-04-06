# DESIGN_JUSTIFICATION: Antigravity Brainstorm Assets v1.0.3

<document_purpose>
This document establishes the canonical local contract for Antigravity brainstorm artifacts and the owner-managed lifecycle used to seed, validate, repair, and maintain governed `brainstorm.md` compendia.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: artifact-brainstorm
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/brainstorm/brainstorm.d.ts`
2. `.agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py`
3. `.agent/skills/artifact-brainstorm/scripts/init_brainstorm.py`
4. `.agent/skills/artifact-brainstorm/SKILL.md`
5. `.agent/schemas/brainstorm/seed.md`
6. `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml`
7. Vendored mirrors under `.agent/skills/<skill>/resources/schema/brainstorm/` are derived copies and must not override the canonical contract.
8. External references listed below are informative only and must not override the local contract unless the contract is intentionally revised.
</authority_order>

<schema_evaluation_and_justification>

- The brainstorm document is a living, append-only repository for early-stage ideas, library candidates, and design hypotheses. It is intentionally non-normative so promising directions can be preserved before promotion into ADRs or the formal specification.
- The canonical file remains `brainstorm.md`, initialized from `.agent/schemas/brainstorm/seed.md`, with permanent manifest content in Part I and governed entry placement in Parts II and III.
- Structured YAML entry blocks keep the contract machine-checkable while preserving a human-readable brainstorming compendium for architectural exploration.
- Citation-catalog governance, recency-class rules, and inline `[C#]` markers force substantive claims to stay evidence-backed instead of devolving into uncited speculation.
- Stable visual-semantics classes and Mermaid accessibility requirements keep the artifact expressive without binding it to renderer-specific extensions.
- `artifact-brainstorm` is the dedicated `Artifact-Centric Owner` for brainstorm artifacts, owning initialization, repair, validation, and lifecycle governance while leaving canonical schema authoring to `core-schema`.
- This v1.0.2 update migrates the schema-owned source-reference asset from `.docx` to `.xhtml` while preserving the existing type contract, seeded structure, entry IDs, and artifact wire shape.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local contract surface: `.agent/schemas/brainstorm/brainstorm.d.ts`
2. Local validator contract: `.agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py`
3. Local scaffolding contract: `.agent/skills/artifact-brainstorm/scripts/init_brainstorm.py`
4. Local seeded artifact basis: `.agent/schemas/brainstorm/seed.md`
5. Local source-reference basis: `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml`

</authoritative_reference_repository>

## Canonical Shape

- The canonical file is `brainstorm.md`.
- Missing files are initialized from `.agent/schemas/brainstorm/seed.md`.
- The document is organized into:
  - `## PART I — Document Manifest`
  - `## PART II — Application Design Concepts`
  - `## PART III — Open-Source Library Candidates`
- Part I includes the governed sections for:
  - `§6 Visual Semantics and Font Color Index`
  - `§7 Citation and Research Protocol`
  - `§8 Mermaid Diagram Standards`
- Part III includes a structured `Citations and References` catalog.
- Each brainstorm entry is encoded as:
  - `#### [BRAIN-II-001] Entry Title` or `#### [BRAIN-III-001] Entry Title`
  - followed immediately by a fenced `yaml` block containing the entry fields
- Each external citation is encoded as:
  - `#### [C1] Citation Title`
  - followed immediately by a fenced `yaml` block containing the citation fields

## Entry Contract

Common fields:

- `entry_type`
- `entry_id`
- `title`
- `category`
- `priority`
- `status`
- `authored_by`
- `authored_date`
- `revised_date`
- `description`
- `detail`
- `open_questions`
- `tags`
- `ddr_relevance`
- `citation_ids`
- `references`

IDEA-only fields:

- `motivation`
- `prior_art`
- `ddr_constraints`
- `risks`
- `dependencies`

LIB-only fields:

- `repository`
- `language`
- `license`
- `commercial_use`
- `latest_release`
- `maintenance`
- `install_size_kb`
- `maturity`
- `verdict`
- `rejection_reason`

Citation fields:

- `citation_id`
- `publisher`
- `title`
- `url`
- `published_date`
- `accessed_date`
- `authority_type`
- `recency_class`
- `support_note`
- `related_entries`

## Governance Rules

- Part I is permanent governing content. Routine updates should not rewrite its prose except for controlled metadata, the Font Color Index, the citation catalog, and explicitly governed maintenance sections.
- IDs are append-only and immutable once assigned.
- `IDEA` entries live in Part II. `LIB` entries live in Part III.
- Seeded entries from the canonical seed must remain present in derived documents.
- The section index tables are navigational. Validator enforcement focuses on part placement, field validity, ID governance, citation integrity, Mermaid policy, and visual-semantics compliance.
- `references` is reserved for non-bibliographic cross-links such as ADR IDs, spec sections, local artifact paths, or related brainstorm IDs.
- External evidence must live in the citation catalog and be referenced inline with `[C#]` markers.

## Evidence and Diagram Rules

- Every substantive assertion, recommendation, or factual comparison in entry prose must have supporting inline citation markers.
- `citation_ids` must exactly match the external citations used inline by the entry.
- A citation classified as `CURRENT` must be published or materially updated within 183 days of the entry `revised_date`.
- Governed visual classes are limited to `brain-governance`, `brain-evidence`, `brain-hypothesis`, `brain-recommendation`, and `brain-risk`.
- Supported Mermaid blocks are `flowchart`, `sequenceDiagram`, `stateDiagram-v2`, `classDiagram`, and `erDiagram`. Every diagram must include `accTitle` and `accDescr`.

## Validation

Validate any brainstorm file with:

```powershell
python .agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py brainstorm.md
```

Run validation plus non-fatal audit warnings with:

```powershell
python .agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py brainstorm.md --audit
```

Stronger append-only validation against a previous version:

```powershell
python .agent/skills/artifact-brainstorm/scripts/validate_brainstorm.py brainstorm.md --baseline previous-brainstorm.md
```

<modification_history>

| Date       | Version | Classification  | Description                                                                                                                                                                                                                                    |
| :--------- | :------ | :-------------- | :--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-03-30 | v1.0.0  | Initial Release | Established the canonical brainstorm Markdown contract, seed structure, citation model, and validator-backed governance for DDR App Framework brainstorming artifacts.                                                                         |
| 2026-04-03 | v1.0.1  | Governance      | Promoted `artifact-brainstorm` to the canonical Artifact-Centric Owner, moved the source-reference document into `.agent/schemas/brainstorm/`, modernized schema governance documentation, and preserved the existing type contract unchanged. |
| 2026-04-03 | v1.0.2  | Governance      | Migrated the schema-owned source-reference asset from the legacy `.docx` source to `.agent/schemas/brainstorm/DDR_AppFramework_Brainstorm.xhtml` and aligned the canonical guidance with the new reference format.                             |
| 2026-04-04 | v1.0.3  | Governance      | Repointed canonical schema-authoring guidance from `dev-schema` to `core-schema` so brainstorm ownership language aligns with the new foundational `core-*` family without changing the brainstorm artifact contract.                          |

</modification_history>
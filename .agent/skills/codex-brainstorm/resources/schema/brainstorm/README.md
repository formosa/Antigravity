# Brainstorm Compendium Format

This package defines the governed Markdown contract for the DDR App Framework brainstorming
compendium managed by `codex-brainstorm`.

## Purpose

The brainstorm document is a living, append-only repository for early-stage ideas, library
candidates, and design hypotheses related to the DDR App Framework. It is not an authoritative
design artifact. Promotion to ADRs or the formal DDR specification happens outside this file.

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

- Part I is permanent governing content. Routine updates should not rewrite its prose except for
  controlled metadata, the Font Color Index, the citation catalog, and explicitly governed
  maintenance sections.
- IDs are append-only and immutable once assigned.
- `IDEA` entries live in Part II. `LIB` entries live in Part III.
- Seeded entries from the canonical seed must remain present in derived documents.
- The section index tables are navigational. Validator enforcement focuses on part placement,
  field validity, ID governance, citation integrity, Mermaid policy, and visual-semantics
  compliance.
- `references` is reserved for non-bibliographic cross-links such as ADR IDs, spec sections,
  local artifact paths, or related brainstorm IDs.
- External evidence must live in the citation catalog and be referenced inline with `[C#]`
  markers.

## Evidence and Diagram Rules

- Every substantive assertion, recommendation, or factual comparison in entry prose must have
  supporting inline citation markers.
- `citation_ids` must exactly match the external citations used inline by the entry.
- A citation classified as `CURRENT` must be published or materially updated within 183 days of
  the entry `revised_date`.
- Governed visual classes are limited to `brain-governance`, `brain-evidence`,
  `brain-hypothesis`, `brain-recommendation`, and `brain-risk`.
- Supported Mermaid blocks are `flowchart`, `sequenceDiagram`, `stateDiagram-v2`,
  `classDiagram`, and `erDiagram`. Every diagram must include `accTitle` and `accDescr`.

## Validation

Validate any brainstorm file with:

```powershell
python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md
```

Run validation plus non-fatal audit warnings with:

```powershell
python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md --audit
```

Stronger append-only validation against a previous version:

```powershell
python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md --baseline previous-brainstorm.md
```

## Design Basis

The canonical seed is a Markdown normalization of:

- `.agent/skills/codex-brainstorm/resources/DDR_AppFramework_Brainstorm.docx`

The seeded document preserves the manifest, taxonomy, section indexes, citation catalog, and
initial entries while moving the actual entry bodies into structured YAML blocks that are easier
for agents to update and validate safely.

<schema_governance>
```yaml
primary_owner_skill: codex-brainstorm
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

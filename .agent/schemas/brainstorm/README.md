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
- Each brainstorm entry is encoded as:
  - `#### [BRAIN-II-001] Entry Title` or `#### [BRAIN-III-001] Entry Title`
  - followed immediately by a fenced `yaml` block containing the entry fields

## Entry Contract

Common fields:

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

## Governance Rules

- Part I is permanent governing content. Routine updates should not rewrite its prose.
- IDs are append-only and immutable once assigned.
- `IDEA` entries live in Part II. `LIB` entries live in Part III.
- Seeded entries from the canonical seed must remain present in derived documents.
- The section index tables are navigational. Validator enforcement focuses on part placement,
  field validity, and ID governance rather than requiring every category to have its own
  dedicated subsection.

## Validation

Validate any brainstorm file with:

```powershell
python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md
```

Stronger append-only validation against a previous version:

```powershell
python .agent/skills/codex-brainstorm/scripts/validate_brainstorm.py brainstorm.md --baseline previous-brainstorm.md
```

## Design Basis

The canonical seed is a Markdown normalization of:

- `.agent/assets/proposals/active/v6.3/DDR_AppFramework_Brainstorm.docx`

The seeded document preserves the manifest, taxonomy, section indexes, and initial entries while
moving the actual entry bodies into structured YAML blocks that are easier for agents to update
and validate safely.

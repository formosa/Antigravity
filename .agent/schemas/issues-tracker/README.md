# DESIGN_JUSTIFICATION: Antigravity Issues Tracker Assets v1.0.1

<document_purpose>
This document establishes the canonical local contract for Antigravity Issues Tracker artifacts and the owner-managed lifecycle used to initialize blank `IT-1.0` trackers, maintain and migrate populated `IT-1.1` trackers, and validate legacy lineage artifacts.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: artifact-issue-tracker
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/issues-tracker/issues-tracker.d.ts`
2. `.agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py`
3. `.agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py`
4. `.agent/skills/artifact-issue-tracker/SKILL.md`
5. `.agent/schemas/issues-tracker/template.md`
6. `.agent/schemas/issues-tracker/example.md`
7. `.agent/schemas/issues-tracker/example-it-1.1.md`
8. Vendored mirrors under `.agent/skills/<skill>/resources/schema/issues-tracker/` are derived copies and must not override the canonical contract.
</authority_order>

<schema_evaluation_and_justification>

- The Issues Tracker family is now owned end to end by `artifact-issue-tracker`, which acts as the Artifact-Centric Owner for tracker initialization, maintenance, migration, and validation.
- `IT-1.0` remains the canonical blank initialization profile because new trackers should stay lean and readable before any issue content exists.
- `IT-1.1` remains the populated maintenance profile because comparative analysis, recommendation, and citation requirements apply only after a tracker is actively maintained.
- Keeping `IT-1.0` and `IT-1.1` as separate profiles preserves a validator-first lifecycle without collapsing blank and populated trackers into one overloaded format.
- Historical `v4` and `v5` lineage trackers remain valid repository artifacts and must stay structurally checkable through the legacy validator path, but they are not generation targets.
- `agent-create-issue-report` remains a separate single-issue non-owner contract and is intentionally excluded from Issues Tracker ownership.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local contract surface: `.agent/schemas/issues-tracker/issues-tracker.d.ts`
2. Local blank and legacy validator: `.agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py`
3. Local populated validator: `.agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py`
4. Local blank initialization template: `.agent/schemas/issues-tracker/template.md`
5. Local canonical blank example: `.agent/schemas/issues-tracker/example.md`
6. Local canonical populated example: `.agent/schemas/issues-tracker/example-it-1.1.md`

</authoritative_reference_repository>

## Contract Profiles

### `IT-1.0` Blank Initialization Contract

Use `IT-1.0` when creating a new blank tracker.

Reference artifacts:

- `.agent/assets/proposals/active/v6.2/DDR_v6.1_Issues_Tracker.md` for current lineage
- `.agent/schemas/issues-tracker/template.md` for blank initialization
- `.agent/schemas/issues-tracker/example.md` for the blank initialized example

Properties:

- no HTML parser header
- no per-issue `AGENT_CONTEXT` blocks
- required sections:
  - `DOCUMENT METADATA`
  - `ISSUE SCHEMA`
  - `ISSUE REGISTRY`
  - `ISSUES`
  - `RESOLUTION WORKFLOW`
  - `APPENDIX: CROSS-ISSUE DEPENDENCY MAP`
- blank initialization state:
  - `open_issues: 0`
  - `resolved_issues: 0`
  - zero `### ISSUE-` entries
  - exactly one empty registry row
  - footer counts equal `0 issues identified | 0 resolved`

### `IT-1.1` Populated Update Contract

Use `IT-1.1` when updating an existing populated tracker in place.

Reference artifacts:

- `.agent/schemas/issues-tracker/example-it-1.1.md`
- `.agent/assets/proposals/active/v6.3/DDR_v6.2_Issues_Tracker.md` as the primary migration target

Additional populated-entry requirements:

- every issue entry must include:
  - `Resolution-[NNN]: Option C - ...`
  - `Comparative Analysis-[NNN]`
  - `Recommendation-[NNN]`
  - `Supporting Citations-[NNN]`
- `Recommendation-[NNN]` must declare exactly one endorsed option:
  - `**Endorsed Option:** \`Option A|B|C\``
- `Supporting Citations-[NNN]` must use single-line markdown bullets with a valid `http` or `https` URL
- registry rows must be sorted by severity then issue number
- header counts use:
  - `open_issues = OPEN + IN_REVIEW`
  - `resolved_issues = RESOLVED`

The `IT-1.0` blank template remains the generation target for new trackers. Migration to
`IT-1.1` happens only when a populated tracker is updated.

## Legacy Profiles

Historical `v4` and `v5` trackers remain valid repository artifacts, but they are not the
generation target for new trackers or updated populated trackers.

- Legacy markers:
  - HTML `AGENT PARSING HEADER`
  - per-issue `AGENT_CONTEXT` blocks
- Historical references:
  - `.agent/assets/proposals/processed/v4/DDR_v4_Issues_Tracker.md`
  - `.agent/assets/proposals/processed/v5/DDR_v5_Issues_Tracker.md`

## Validation

`IT-1.0` blank initialization validation:

```powershell
python .agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py .agent/schemas/issues-tracker/example.md --mode canonical
```

`IT-1.1` populated update validation:

```powershell
python .agent/skills/artifact-issue-tracker/scripts/validate_updated_issues_tracker.py .agent/schemas/issues-tracker/example-it-1.1.md
```

Legacy validation:

```powershell
python .agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py .agent/assets/proposals/processed/v4/DDR_v4_Issues_Tracker.md --mode legacy
python .agent/skills/artifact-issue-tracker/scripts/validate_issues_tracker.py .agent/assets/proposals/processed/v5/DDR_v5_Issues_Tracker.md --mode legacy
```

## Design Basis

The package remains validator-first and keeps the blank and populated contracts separate so
initialization and maintenance can evolve without collapsing into one overloaded format.

<modification_history>

| Date       | Version | Classification | Description |
| :--------- | :------ | :------------- | :---------- |
| 2026-03-28 | v1.0.0  | Initial Release | Established the shared Issues Tracker contracts for blank initialization, populated maintenance, and legacy validation. |
| 2026-04-04 | v1.0.1  | Governance | Promoted `artifact-issue-tracker` to the canonical Artifact-Centric Owner, consolidated tracker lifecycle ownership under one skill, and updated validation and governance references without changing `IT-1.0` or `IT-1.1` wire shapes. |

</modification_history>

# Issues Tracker Format

This package defines the shared Issues Tracker contracts used by:

- `agent-create-issues-tracker` for blank initialization
- `agent-update-issues-tracker` for populated tracker maintenance and migration

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
python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py .agent/schemas/issues-tracker/example.md --mode canonical
```

`IT-1.1` populated update validation:

```powershell
python .agent/skills/agent-update-issues-tracker/scripts/validate_updated_issues_tracker.py .agent/schemas/issues-tracker/example-it-1.1.md
```

Legacy validation:

```powershell
python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py .agent/assets/proposals/processed/v4/DDR_v4_Issues_Tracker.md --mode legacy
python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py .agent/assets/proposals/processed/v5/DDR_v5_Issues_Tracker.md --mode legacy
```

## Design Basis

The package remains validator-first and keeps the blank and populated contracts separate so
initialization and maintenance can evolve without collapsing into one overloaded format.

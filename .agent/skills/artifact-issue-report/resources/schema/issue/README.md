# DESIGN_JUSTIFICATION: Antigravity Issue Assets v2.0.0

<document_purpose>
This document establishes the canonical local contract for Antigravity issue-report artifacts and the owner-managed lifecycle used to generate, maintain, validate, and upgrade standalone issue reports.
</document_purpose>

<schema_governance>
```yaml
primary_owner_skill: artifact-issue-report
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

<authority_order>
1. `.agent/schemas/issue/issue.d.ts`
2. `.agent/skills/artifact-issue-report/scripts/validate_issue_report.py`
3. `.agent/skills/artifact-issue-report/SKILL.md`
4. `.agent/schemas/issue/example.md`
5. `.agent/schemas/issue/example-legacy-v4.md`
6. Vendored mirrors under `.agent/skills/<skill>/resources/schema/issue/` are derived copies and must not override the canonical contract.
</authority_order>

<schema_evaluation_and_justification>

- The `issue` artifact family is now owned end to end by `artifact-issue-report`, which acts as the Artifact-Centric Owner for issue-report generation, maintenance, validation, and first-write legacy upgrades.
- The canonical generation target is the validator-backed two-option issue report shape already enforced by the active issue-report validator. The canonical schema now matches that live contract instead of preserving the stale legacy example shape.
- The required `updated` field and required `Implementation Note` make report state explicit, which is necessary for deterministic maintenance and for distinguishing unresolved analysis from confirmed resolved implementation.
- Restricting canonical generation to exactly `Option A` and `Option B` preserves the standalone report's narrow scope and avoids duplicating the broader three-option strategy surface owned by Issues Tracker maintenance.
- Historical v4/v5 issue reports remain structurally valid repository artifacts for read-only validation and upgrade-on-write flows, but they are no longer treated as the canonical generation target.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. Local canonical schema contract: `.agent/schemas/issue/issue.d.ts`
2. Local canonical validator contract: `.agent/skills/artifact-issue-report/scripts/validate_issue_report.py`
3. Local canonical example artifact: `.agent/schemas/issue/example.md`
4. Local historical legacy example artifact: `.agent/schemas/issue/example-legacy-v4.md`

</authoritative_reference_repository>

## Canonical Profile

Use the canonical profile for all newly generated or maintained issue reports.

Required frontmatter:

- `id`
- `title`
- `format_version`
- `target_platform`
- `target_model`
- `subject`
- `created`
- `updated`
- `status`
- `severity`
- `type`
- `resolved` only when `status: RESOLVED`

Required body sections:

- `## Optimized Resolution Strategy for "<ISSUE-ID>"`
- `### Agent Context`
- `### 1. Validation Audit of <ISSUE-ID>`
- `### 2. Suggested Strategies for Optimal Resolution of <ISSUE-ID>`
- `#### Option A: ...`
- `#### Option B: ...`
- `### 3. Comparative Analysis and Recommended Strategy`
- `#### Comparative Analysis`
- `#### Endorsement and Contextual Justification`
- `### 4. Implementation Note`

Canonical rules:

- Generate exactly two options: `Option A` and `Option B`
- Keep `* **Supporting Insights:**` and `* **Citations:**` under both options
- Preserve tracker resolution callouts only when they are present in the source tracker
- Use repo-relative local evidence references whenever project files are cited

## Legacy Compatibility

Historical v4/v5 issue reports remain valid for read-only validation and first-write migration.

Legacy markers may include:

- no `updated` frontmatter field
- no `### 4. Implementation Note`
- a legacy `Option C`

Legacy artifacts are not generation targets. The owner skill may preserve them read-only or migrate them to the canonical profile when the task explicitly modifies them.

## Validation

Canonical validation:

```powershell
python .agent/skills/artifact-issue-report/scripts/validate_issue_report.py .agent/schemas/issue/example.md --mode canonical
```

Legacy validation:

```powershell
python .agent/skills/artifact-issue-report/scripts/validate_issue_report.py .agent/schemas/issue/example-legacy-v4.md --mode legacy
```

Compatibility alias validation:

```powershell
python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py .agent/schemas/issue/example.md --mode canonical
```

<modification_history>

| Date       | Version | Classification  | Description |
| :--------- | :------ | :-------------- | :---------- |
| 2026-03-02 | v1.0.0  | Initial Release | Constructed `issue.d.ts` per Antigravity schema standards with strict typing and YAML context annotations. |
| 2026-04-04 | v2.0.0  | Major revision  | Promoted `artifact-issue-report` to the canonical owner, aligned the canonical issue schema with the live two-option validator contract, and split legacy v4/v5 compatibility into an explicit non-canonical example path. |

</modification_history>

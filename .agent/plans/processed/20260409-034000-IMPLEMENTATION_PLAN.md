---
task: "Remediate identified agentic scaffolding hygiene, governance, and contract-compliance issues across .agent/ to eliminate recurring drift patterns and close structural gaps targeting Antigravity IDE v1.21.9."
model: "gemini-3-pro-preview"
version: "1.0.0"
output_path: ".agent/plans/20260409-034000-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260409-034000-IMPLEMENTATION_PLAN.md"
---

<objective>
Eliminate all identified structural, governance, and hygiene issues in the `.agent/` agentic scaffolding so that every asset surface complies with its governing schema, index, and rule contract under Antigravity IDE v1.21.9, and recurring drift patterns are prevented through targeted governance enhancements.
</objective>

<phases>
- phase_id: "PHASE_1_HYGIENE_AND_STALENESS"
  objectives:
    - "Remove 13 identical .bak files from .agent/schemas/ that serve no governance purpose"
    - "Annotate legacy processed plans with a non-compliance notice without altering their historical content"
  task_references: ["IOC-01", "IOC-02"]
  entry_criteria:
    - "All .bak files confirmed byte-identical to their canonical .d.ts counterparts"
    - "Processed plans confirmed as pre-current-contract historical artifacts"
  exit_criteria:
    - "Zero .bak files remain under .agent/schemas/"
    - "Both processed plans carry a leading non-compliance notice"
  assigned_model: "gemini-3-flash-preview"

- phase_id: "PHASE_2_GOVERNANCE_GAP_CLOSURE"
  objectives:
    - "Create tools-governance rule for .agent/tools/"
    - "Create evals-governance rule for .agent/evals/"
    - "Create config-governance rule for .agent/config/"
    - "Regenerate rules index to reflect newly added rules"
  task_references: ["IOC-03", "IOC-04", "IOC-05", "IOC-06"]
  entry_criteria:
    - "PHASE_1 exit criteria verified"
    - "Existing governance rules reviewed for structural conventions"
  exit_criteria:
    - "Three new governance rules exist in .agent/rules/ with proper frontmatter"
    - "Rules index reflects accurate total count and covers all nine rules"
  assigned_model: "gemini-3-pro-preview"

- phase_id: "PHASE_3_VERIFICATION_AND_INDEX_SYNC"
  objectives:
    - "Verify all indexes are current and accurate"
    - "Run structural validation across modified surfaces"
  task_references: ["IOC-07"]
  entry_criteria:
    - "PHASE_2 exit criteria verified"
  exit_criteria:
    - "All indexes match their governed asset sets"
    - "No stale, orphan, or non-compliant entries remain"
  assigned_model: "gemini-3-flash-preview"
</phases>

<atomic_steps>

#### Group 1 â€” Schema Backup File Cleanup (PHASE_1_HYGIENE_AND_STALENESS)

- [X] 1. DELETE all 13 `.bak` files under `.agent/schemas/` â€” these are byte-identical copies of their canonical `.d.ts` counterparts confirmed via SHA-256 comparison, serve no governance or rollback purpose, and constitute accumulated build debris that violates the schemas-governance rule's expectation that `.agent/schemas/<schema-id>/` contains only the canonical `.d.ts`, `README.md`, and `example.md` (plus optional `seed.md`). Target files:
  - `.agent/schemas/brainstorm/brainstorm.d.ts.bak`
  - `.agent/schemas/gemini/gemini.d.ts.bak`
  - `.agent/schemas/implementation-plan/implementation-plan.d.ts.bak`
  - `.agent/schemas/index/index.d.ts.bak`
  - `.agent/schemas/issue/issue.d.ts.bak`
  - `.agent/schemas/issues-tracker/issues-tracker.d.ts.bak`
  - `.agent/schemas/rule/rule.d.ts.bak`
  - `.agent/schemas/schema/schema.d.ts.bak`
  - `.agent/schemas/security-policy/security-policy.d.ts.bak`
  - `.agent/schemas/skill/skill.d.ts.bak`
  - `.agent/schemas/task/task.d.ts.bak`
  - `.agent/schemas/walkthrough/walkthrough.d.ts.bak`
  - `.agent/schemas/workflow/workflow.d.ts.bak`

#### Group 2 â€” Legacy Processed Plan Annotation (PHASE_1_HYGIENE_AND_STALENESS)

- [X] 2. MODIFY `.agent/plans/processed/ddr_v4_logic_fix.md` â€” Prepend a Markdown comment block (non-rendering) documenting that this artifact predates the current implementation-plan contract (v1.21.9): it uses deprecated model `Gemini 3.1 Pro`, omits required `version`, `output_path`, and `processed_path` frontmatter, uses non-standard section numbering (Â§1â€“Â§7) instead of `<objective>/<phases>/<atomic_steps>/<verification>/<risks_and_mitigations>`, and employs `bash` verification gates (`cat | grep`) on a Windows PowerShell workspace. Do not alter any existing content; the notice is informational only.

- [X] 3. MODIFY `.agent/plans/processed/ddr_v6_3_canonical_spec_repair.md` â€” Prepend a Markdown comment block (non-rendering) documenting that this artifact predates the current contract: it uses deprecated model `gemini-3.1-pro`, omits `output_path` and `processed_path` frontmatter, uses un-grouped `<atomic_steps>` (numbered list without `####` group headers or `- [ ]` completion trackers), and has a non-1:1 mapping between atomic steps and verification items (10 steps, 5 verification items). Do not alter any existing content.

#### Group 3 â€” Tools Governance Rule (PHASE_2_GOVERNANCE_GAP_CLOSURE)

- [X] 4. CREATE `.agent/rules/tools-governance.md` â€” A new glob-scoped governance rule for `.agent/tools/` mirroring the structural conventions of the existing governance rules. The rule must enforce: (a) tool definition frontmatter compliant with a `ToolDefinition` contract (type, name, description, command, runtime, confirmation, args), (b) alignment between each tool definition's `command` field and its linked `.agent/scripts/` implementation, (c) tools index (`index.md`) accuracy and freshness, (d) prohibition of tool definitions without a working implementation script. Frontmatter: `name: tools-governance`, `trigger: glob`, `globs: .agent/tools/**`, `priority: critical`, `execution_tier: standard`. Body wrapped in `<constraints>` and `<verification_step>` blocks.

#### Group 4 â€” Evals Governance Rule (PHASE_2_GOVERNANCE_GAP_CLOSURE)

- [X] 5. CREATE `.agent/rules/evals-governance.md` â€” A new glob-scoped governance rule for `.agent/evals/` covering: (a) eval case files must follow the established case-format pattern (failure family, bad pattern, compliant pattern, fallback), (b) eval case IDs must be unique and sequential within each eval file, (c) eval files must reference only rules, tools, or scripts that currently exist, (d) evals should not reference deprecated models or stale file paths. Frontmatter: `name: evals-governance`, `trigger: glob`, `globs: .agent/evals/**`, `priority: high`, `execution_tier: standard`. Body wrapped in `<constraints>` and `<verification_step>` blocks.

#### Group 5 â€” Config Governance Rule (PHASE_2_GOVERNANCE_GAP_CLOSURE)

- [X] 6. CREATE `.agent/rules/config-governance.md` â€” A new glob-scoped governance rule for `.agent/config/` covering: (a) `runtime-target.yaml` must declare `target_platform`, `rules_surfaces`, `approved_models`, `deprecated_models`, `windows_execution`, and `search_policy` sections, (b) approved model IDs in `runtime-target.yaml` are the single source of truth for model references across all skills and schemas, (c) any model string appearing in the deprecated list must not be used as a primary model in new skill or schema files, (d) `evidence_date` must remain current within 90 days of the last confirmed platform verification. Frontmatter: `name: config-governance`, `trigger: glob`, `globs: .agent/config/**`, `priority: critical`, `execution_tier: standard`. Body wrapped in `<constraints>` and `<verification_step>` blocks.

#### Group 6 â€” Rules Index Regeneration (PHASE_2_GOVERNANCE_GAP_CLOSURE)

- [X] 7. MODIFY `.agent/rules/index.md` â€” Regenerate the rules index to include the three newly created governance rules (`tools-governance`, `evals-governance`, `config-governance`) alongside the existing six. Update the total count from `6` to `9`, add selection map entries, manifest entries, and rule record sections for each new rule. Maintain existing section ordering and format conventions.

#### Group 7 â€” Cross-Surface Verification (PHASE_3_VERIFICATION_AND_INDEX_SYNC)

- [X] 8. Verify that `.agent/schemas/index.md` remains accurate after schema `.bak` cleanup â€” confirm the table-only index still lists exactly 13 schema entries with correct versions, primary skills, and descriptions; no `.bak` files should appear or have been referenced.

- [X] 9. Verify that `.agent/tools/index.md` remains accurate â€” confirm it lists exactly 2 tools, both with valid implementation links and correct manifest metadata.

- [X] 10. Verify that `.agent/scripts/index.md` remains accurate â€” confirm it lists exactly 6 root scripts with correct categories and tool linkage.

- [X] 11. Verify that `.agent/skills/index.md` remains accurate â€” confirm it lists exactly 11 skills with correct categories and correct manifest metadata.

- [X] 12. Verify that `.agent/workflows/index.md` remains accurate â€” confirm it lists exactly 1 workflow with correct metadata.

- [X] 13. Run a final sweep confirming zero `.bak` files remain under `.agent/schemas/`, all three new governance rules parse valid frontmatter, the rules index total is `9`, and processed plans carry their non-compliance notices.

</atomic_steps>

<verification>

1. Run `Get-ChildItem -Path ".agent/schemas" -Recurse -Filter "*.bak" | Measure-Object` and confirm `Count` is `0`.
2. Inspect the first 5 lines of `.agent/plans/processed/ddr_v4_logic_fix.md` and confirm a Markdown comment block noting deprecated model, missing frontmatter, and non-standard structure is present, and the original content starting with `---` immediately follows.
3. Inspect the first 5 lines of `.agent/plans/processed/ddr_v6_3_canonical_spec_repair.md` and confirm a Markdown comment block noting deprecated model, missing frontmatter, and non-1:1 verification is present.
4. Confirm `.agent/rules/tools-governance.md` exists, has valid YAML frontmatter with `trigger: glob`, `globs: .agent/tools/**`, `priority: critical`, and contains non-empty `<constraints>` and `<verification_step>` blocks.
5. Confirm `.agent/rules/evals-governance.md` exists, has valid YAML frontmatter with `trigger: glob`, `globs: .agent/evals/**`, `priority: high`, and contains non-empty `<constraints>` and `<verification_step>` blocks.
6. Confirm `.agent/rules/config-governance.md` exists, has valid YAML frontmatter with `trigger: glob`, `globs: .agent/config/**`, `priority: critical`, and contains non-empty `<constraints>` and `<verification_step>` blocks.
7. Confirm `.agent/rules/index.md` total rules count reads `9`, the selection map contains entries for `tools-governance`, `evals-governance`, and `config-governance`, and each new rule has a corresponding manifest entry and rule record section.
8. Inspect `.agent/schemas/index.md` and confirm it contains exactly 13 data rows (one per schema), no `.bak` references, and all version/primary-skill values match the live schema directories.
9. Inspect `.agent/tools/index.md` and confirm it lists 2 tools with valid implementation paths pointing to existing `.agent/scripts/` files.
10. Inspect `.agent/scripts/index.md` and confirm it lists 6 root scripts with accurate categories and tool linkage.
11. Inspect `.agent/skills/index.md` and confirm it lists 11 skills with accurate categories.
12. Inspect `.agent/workflows/index.md` and confirm it lists 1 workflow with accurate metadata.
13. Run `Get-ChildItem -Path ".agent/schemas" -Recurse -Filter "*.bak" | Measure-Object` (reconfirm), validate each new rule's YAML parses cleanly, and spot-check all three processed plan notices.

</verification>

<risks_and_mitigations>

- **Risk:** Deleting `.bak` files removes the only pre-edit backup for canonical schemas.
  **Mitigation:** All 13 `.bak` files are byte-identical to their canonical `.d.ts` counterparts (SHA-256 verified). The repository's version control system provides full history recovery if needed. No governance surface references these files.

- **Risk:** Annotating processed plans could be misread as retroactive contract enforcement.
  **Mitigation:** Annotations are non-rendering Markdown comments that explicitly state the artifact predates the current contract and is retained as a historical reference only. No content is altered.

- **Risk:** New governance rules introduce enforcement requirements that lag behind existing tooling.
  **Mitigation:** All three new rules describe structural requirements already implicit in the existing tools, evals, and config surfaces. No new validation scripts or enforcement tooling is introduced â€” the rules formalize what is already expected.

- **Risk:** Rules index regeneration could introduce format drift from the generated index contract.
  **Mitigation:** The regenerated index will follow the exact same section ordering, manifest format, and record structure used by the current 6-rule index. The index schema (`index.d.ts`) governs the structural contract.

</risks_and_mitigations>

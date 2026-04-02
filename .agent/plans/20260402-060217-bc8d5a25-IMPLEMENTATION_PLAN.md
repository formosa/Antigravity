---
task: "Resolve all five identified gaps in the Asset Directory Index schema (index.d.ts) so that it is maximally optimized for indexing rules, skills, workflows, and schemas asset directories in addition to tools."
model: "gemini-3.1-pro-preview"
version: "1.0.0"
output_path: ".agent/plans/20260402-060217-bc8d5a25-IMPLEMENTATION_PLAN.md"
processed_path: ".agent/plans/processed/20260402-060217-bc8d5a25-IMPLEMENTATION_PLAN.md"
# HUMAN CONTEXT: This artifact addresses five concrete gaps discovered during an audit
# of the Asset Directory Index schema against all five agent-asset directory types
# (tools, rules, skills, workflows, schemas). All edits are scoped to the index
# schema package and its README. No other schemas, skills, or asset files are modified.
# Upon executor confirmation of all steps and verification checks, this file
# must be relocated to the processed_path above.
---

<objective>
Patch `.agent/schemas/index/index.d.ts` and `.agent/schemas/index/README.md` to close five identified coverage gaps so that the Asset Directory Index schema deterministically supports tools, rules, skills, workflows, and schemas directories without asset-type-specific blind spots or undocumented exceptions.
</objective>

<phases>
- phase_id: "PHASE_1_SCHEMA_PATCH"
  objectives:
    - "Add recognized optional fields to AssetDirectoryManifestEntry for rules, skills, and workflows"
    - "Add escape-hatch index signature to AssetDirectoryRecord for parity with AssetDirectoryManifestEntry"
    - "Bump schema version to v1.1.0 in header comment"
  task_references: ["GAP-1-RULE-ACTIVATION", "GAP-2-ASSET-STRUCTURE", "GAP-3-TURBO-STEPS", "GAP-5-RECORD-ESCAPE-HATCH"]
  entry_criteria:
    - "Current index.d.ts is readable and matches the v1.0.0 baseline audited in the prior conversation turn"
  exit_criteria:
    - "index.d.ts compiles without error and contains all four new field groups plus the record-level escape hatch"
  assigned_model: "gemini-3.1-pro-preview"

- phase_id: "PHASE_2_README_UPDATE"
  objectives:
    - "Document the schemas/index.md governance exception in README.md"
    - "Add modification-history row for v1.1.0"
    - "Update schema_evaluation_and_justification to reflect multi-asset-type coverage"
  task_references: ["GAP-4-SCHEMAS-INDEX-EXCEPTION"]
  entry_criteria:
    - "PHASE_1_SCHEMA_PATCH complete and exit criteria verified"
  exit_criteria:
    - "README.md documents the schemas-index exception and the v1.1.0 changelog entry exists"
  assigned_model: "gemini-3-flash"

- phase_id: "PHASE_3_EXAMPLE_PATCH"
  objectives:
    - "Update example.md to demonstrate at least one newly added field so the example remains representative of the schema surface"
  task_references: ["GAP-1-RULE-ACTIVATION", "GAP-2-ASSET-STRUCTURE"]
  entry_criteria:
    - "PHASE_2_README_UPDATE complete and exit criteria verified"
  exit_criteria:
    - "example.md contains at least one instance of a newly added manifest field"
  assigned_model: "gemini-3-flash"
</phases>

<atomic_steps>

#### Group 1 — Schema Patch: AssetDirectoryManifestEntry (PHASE_1_SCHEMA_PATCH)

- [ ] 1. MODIFY `.agent/schemas/index/index.d.ts` — Add three recognized optional fields for rule-asset activation metadata to `AssetDirectoryManifestEntry`: `trigger` (constrained to the value set from `rule.d.ts`: `'auto' | 'manual' | 'glob' | 'always_on' | '@mention'`), `globs` (`string`, required when trigger is `'glob'`), and `priority` (`'low' | 'medium' | 'high' | 'critical'`). Include JSDoc annotations stating these fields are relevant when the indexed asset type is `rules`. Place these after the existing `confirmation` field to maintain logical field ordering.

- [ ] 2. MODIFY `.agent/schemas/index/index.d.ts` — Add one recognized optional field for asset-structure differentiation to `AssetDirectoryManifestEntry`: `asset_structure` (constrained to `'flat-file' | 'folder-package'`). Include a JSDoc annotation explaining that `flat-file` applies to tools, rules, and workflows (single `.md` file per asset), while `folder-package` applies to skills (directory with `SKILL.md`). Place this after the existing `definition` field.

- [ ] 3. MODIFY `.agent/schemas/index/index.d.ts` — Add one recognized optional field for workflow turbo-annotation visibility to `AssetDirectoryManifestEntry`: `has_turbo_steps` (`boolean`). Include a JSDoc annotation explaining this surfaces whether the workflow contains `// turbo` or `// turbo-all` step-level auto-run annotations. Place this after the `destructive_capability` field.

#### Group 2 — Schema Patch: AssetDirectoryRecord (PHASE_1_SCHEMA_PATCH)

- [ ] 4. MODIFY `.agent/schemas/index/index.d.ts` — Add an index signature `[key: string]: string | string[] | boolean | undefined` to `AssetDirectoryRecord`, mirroring the existing escape hatch on `AssetDirectoryManifestEntry`. Include a JSDoc annotation stating this permits asset-type-specific record fields without forcing schema churn, and that additional fields should remain explicit flat scalars or lists.

#### Group 3 — Schema Patch: Version Bump (PHASE_1_SCHEMA_PATCH)

- [ ] 5. MODIFY `.agent/schemas/index/index.d.ts` — Update the file-level comment block from `OPTIMIZED FOR DIRECTORY-LEVEL AGENT ASSET INDEX DOCUMENTS` to `OPTIMIZED FOR DIRECTORY-LEVEL AGENT ASSET INDEX DOCUMENTS (v1.1.0)` and update the purpose JSDoc on `AssetDirectoryIndexDefinition` to list `tools, rules, skills, workflows, and schemas` as explicitly supported directory types.

#### Group 4 — README Update (PHASE_2_README_UPDATE)

- [ ] 6. MODIFY `.agent/schemas/index/README.md` — In the `<schema_evaluation_and_justification>` section, add a new bullet documenting the **Schemas-Directory Governance Exception**: the `.agent/schemas/index.md` registry uses a deliberately lighter table-only format and is not required to conform to `AssetDirectoryIndexDefinition`. State the rationale: the schemas index is a flat lookup table maintained by `dev-create-schema` and does not require the full routing, manifest, and boundary apparatus designed for runtime asset discovery.

- [ ] 7. MODIFY `.agent/schemas/index/README.md` — In the `<schema_evaluation_and_justification>` section, update the existing **Generic Asset Coverage** bullet to explicitly name all five supported asset types (tools, rules, skills, workflows, schemas) and to reference the newly added fields (`trigger`, `globs`, `priority`, `asset_structure`, `has_turbo_steps`, and the record-level escape hatch).

- [ ] 8. MODIFY `.agent/schemas/index/README.md` — In the `<modification_history>` table, append a new row: date `2026-04-02`, version `v1.1.0`, classification `Multi-Asset Optimization`, description summarizing: added rule-activation fields, asset-structure discriminant, workflow turbo-step visibility, record-level escape hatch, and documented the schemas-index governance exception.

#### Group 5 — Example Patch (PHASE_3_EXAMPLE_PATCH)

- [ ] 9. MODIFY `.agent/schemas/index/example.md` — In the fenced YAML manifest, add the field `asset_structure: flat-file` to each of the three existing tool entries to demonstrate the newly added discriminant field. This is a minimal, non-breaking addition that makes the example representative of the v1.1.0 schema surface.

</atomic_steps>

<verification>

1. Open `.agent/schemas/index/index.d.ts` and confirm `AssetDirectoryManifestEntry` contains `trigger?: 'auto' | 'manual' | 'glob' | 'always_on' | '@mention'`, `globs?: string`, and `priority?: 'low' | 'medium' | 'high' | 'critical'` with JSDoc annotations. Confirm they appear after the `confirmation` field.

2. Open `.agent/schemas/index/index.d.ts` and confirm `AssetDirectoryManifestEntry` contains `asset_structure?: 'flat-file' | 'folder-package'` with a JSDoc annotation. Confirm it appears after the `definition` field.

3. Open `.agent/schemas/index/index.d.ts` and confirm `AssetDirectoryManifestEntry` contains `has_turbo_steps?: boolean` with a JSDoc annotation. Confirm it appears after the `destructive_capability` field.

4. Open `.agent/schemas/index/index.d.ts` and confirm `AssetDirectoryRecord` contains `[key: string]: string | string[] | boolean | undefined` with a JSDoc annotation matching the rationale on `AssetDirectoryManifestEntry`.

5. Open `.agent/schemas/index/index.d.ts` and confirm the file-level comment includes `(v1.1.0)` and the `AssetDirectoryIndexDefinition` JSDoc explicitly lists tools, rules, skills, workflows, and schemas.

6. Open `.agent/schemas/index/README.md` and confirm the `<schema_evaluation_and_justification>` section contains a new bullet documenting the schemas-directory governance exception with rationale.

7. Open `.agent/schemas/index/README.md` and confirm the **Generic Asset Coverage** bullet now names all five asset types and references the six newly added schema elements.

8. Open `.agent/schemas/index/README.md` and confirm the `<modification_history>` table contains a row with date `2026-04-02`, version `v1.1.0`, classification `Multi-Asset Optimization`, and a description covering all five resolved gaps.

9. Open `.agent/schemas/index/example.md` and confirm each of the three tool manifest entries now includes `asset_structure: flat-file`.

</verification>

<risks_and_mitigations>

- **Risk:** Adding new typed fields to `AssetDirectoryManifestEntry` may invalidate existing index documents that lack those fields.
  **Mitigation:** All new fields are declared as optional (`?`). Existing index documents remain valid because they simply omit the new fields. No existing document requires modification to maintain schema compliance.

- **Risk:** The record-level `[key: string]` escape hatch on `AssetDirectoryRecord` may invite uncontrolled field proliferation.
  **Mitigation:** The JSDoc annotation explicitly constrains additional fields to flat scalars or lists, matching the precedent already established on `AssetDirectoryManifestEntry`. The authority-boundary rules in the index document structure further contain this risk by deferring to linked asset definitions for authoritative semantics.

- **Risk:** Documenting the schemas-index as a governance exception may appear to weaken the schema's authority.
  **Mitigation:** The exception is scoped and justified: the schemas index is a static lookup table maintained by a dedicated skill, not a runtime discovery surface. Documenting the exception explicitly is strictly preferable to the current state of undocumented divergence.

</risks_and_mitigations>

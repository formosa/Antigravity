---
name: "config-governance"
version: "1.0.0"
description: "Glob-scoped collection governance rule for the `.agent/config/` directory, covering runtime-target manifest completeness, model-ID authority, deprecated-model enforcement, and evidence-date currency across the full config surface."
trigger: "glob"
globs: ".agent/config/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. Scope Boundary: This rule governs only assets under `.agent/config/`. It MUST NOT impose governance requirements on `.agent/rules/`, `.agent/schemas/`, or `.agent/skills/`.
2. Runtime Target Completeness: `.agent/config/runtime-target.yaml` MUST declare the following top-level sections: `target_platform`, `rules_surfaces`, `approved_models`, `deprecated_models`, `windows_execution`, and `search_policy`. Omission of any required section MUST be treated as a contract violation.
3. Model ID Authority: The `approved_models` list in `runtime-target.yaml` is the single source of truth for model IDs permitted in new skill definitions, schema contracts, and implementation plan artifacts across the `.agent/` scaffolding. Any model ID not present in `approved_models` MUST NOT be used as a primary or assigned model in newly created or modified files.
4. Deprecated Model Enforcement: Any model string appearing in the `deprecated_models` list in `runtime-target.yaml` MUST NOT be used as a primary model in new skill or schema files. Deprecated models MAY appear only in historical documentation, modification history tables, and deprecation notices that explicitly mark them as deprecated.
5. Evidence Date Currency: The `evidence_date` field in `runtime-target.yaml` MUST remain current within 90 days of the last confirmed platform verification. If the evidence date exceeds 90 days from the current date, agents SHOULD flag the runtime target for revalidation.
6. Platform Version Consistency: The `target_platform.version` value in `runtime-target.yaml` MUST match the Antigravity IDE version referenced across all schema READMEs, skill descriptions, and governance documentation that cite a specific platform version.
7. Source URL Maintenance: The `source_urls` list in `runtime-target.yaml` MUST contain only accessible, relevant URLs. Removed or broken URLs MUST be replaced or removed in a maintenance task.

</constraints>

<verification_step>

1. Confirm `runtime-target.yaml` contains all six required top-level sections: `target_platform`, `rules_surfaces`, `approved_models`, `deprecated_models`, `windows_execution`, and `search_policy`.
2. Confirm all model IDs in `approved_models` are valid and distinct from any entry in `deprecated_models`.
3. Confirm the `evidence_date` is within 90 days of the current date; flag for revalidation if exceeded.
4. Confirm the `target_platform.version` value is consistently referenced across schema READMEs and skill definitions that cite a specific platform version.

</verification_step>

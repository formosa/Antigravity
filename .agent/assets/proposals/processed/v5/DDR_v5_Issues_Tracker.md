<!--
  AGENT PARSING HEADER — DO NOT MODIFY
  =====================================
  skill:                DDR-v5-Issues-Tracker
  version:              1.0.0
  target_agent:         Gemini 3.1 Pro
  platform:             Google Antigravity >=1.18
  context_mode:         progressive_disclosure
  schema_version:       IT-1.0
  document_type:        issues_tracker
  subject_system:       DDR System Specification v5.0
  subject_file:         ddr_system_v5.0.yaml
  last_updated:         2026-03-25
  total_issues:         12
  open_issues:          1
  resolved_issues:      11
  load_trigger:         "DDR issue", "track issue", "DDR problem", "DDR review", "DDR assessment"

  ANTIGRAVITY 1.18 DEPLOYMENT NOTES
  ===================================
  recommended_path:     <workspace-root>/.agents/skills/DDR-Issues-Tracker/SKILL.md
  global_path:          ~/.gemini/antigravity/skills/DDR-Issues-Tracker/SKILL.md
  plan_mode_hint:       Use Antigravity Plan Mode before executing resolution options.
                        Plan Mode maps the full change set (spec sections + YAML fields)
                        before any file is touched. Enables pre-flight impact review.
  context_budget:       Gemini 3.1 Pro supports 1M token context / 64K output tokens.
                        This document uses progressive_disclosure to stay within
                        a single skill load. The ISSUE REGISTRY table is the primary
                        context gate — parse it before loading individual issue blocks.
  artifact_integration: Issue entries are structured for Antigravity Artifact output.
                        Each ISSUE-NNN block can be rendered as a standalone Artifact
                        for Google-Doc-style comment feedback from human reviewers.
  workflow_path:        .agent/workflows/ddr-issue-resolution.md
                        Create a numbered-step Workflow to chain: identify → add entry
                        → update registry → update header metadata.
  gemini_md_hook:       Add to ~/.gemini/GEMINI.md or .antigravity/rules.md:
                        "When working on DDR System issues, load the skill at
                        .agents/skills/DDR-Issues-Tracker/SKILL.md before proceeding."
  deep_think_mode:      Recommended ON for CRITICAL and MAJOR severity issues.
                        Toggle in Antigravity model settings before issuing resolution
                        prompts to force extended chain-of-thought on logic-heavy changes.
-->

# DDR System v5.0 — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the DDR System Specification v5.0. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read only the `<!-- AGENT_CONTEXT -->` blocks within each issue before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              ITR-5a1b2c3d-4e5f-6a7b-8c9d-0e1f2a3b4c5d
  title:           "DDR System v5.0 — Issues Tracker"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System Specification v5.0"
  created:         "2026-03-25"
  last_modified:   "2026-03-25"
  author:          "Anthony Formosa"
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT      # Specification makes contradictory claims
    - DESIGN_INADEQUACY     # Feature is absent, under-specified, or insufficient
    - UNNECESSARY_COMPLEXITY # System is more complex than the problem demands
    - AXIOM_VIOLATION       # A rule or behavior contradicts a stated axiom
    - SCHEMA_DEFECT         # Machine-readable schema is incorrect or incomplete
    - MIGRATION_GAP         # Version migration is incomplete or unresolved
    - LIFECYCLE_GAP         # A state, transition, or lifecycle path is undefined
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every new issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

<!-- AGENT_CONTEXT
id:          ISSUE-[NNN]
status:      OPEN | IN_REVIEW | RESOLVED | WONT_FIX | DEFERRED
severity:    CRITICAL | MAJOR | MODERATE | MINOR
type:        [TYPE_VALUE]
tier_refs:   [list of DDR tiers affected, e.g. FCL, CL, SAL]
section_ref: [§ reference in ddr_system_v5.0.yaml]
rule_refs:   [list of specific rule IDs affected, e.g. CIT-R2, AX-3]
created:     YYYY-MM-DD
updated:     YYYY-MM-DD
resolved:    null | YYYY-MM-DD
-->

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the specific issue. 2–4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the spec, plus the logical chain that makes this a problem.
Use inline code formatting for rule IDs and tier names.]

#### Impact Assessment-[NNN]
[What breaks, is ambiguous, or fails if this issue is not resolved.
State the concrete failure mode.]

#### Resolution-[NNN]: Option A — [Short Label]
[Detailed description of first resolution approach. Include specific rule/section changes
required, draft replacement language where applicable, and any trade-offs.]

#### Resolution-[NNN]: Option B — [Short Label]
[Detailed description of second, distinctly different resolution approach. Must not be
a minor variant of Option A — must represent a meaningfully different design decision.]

#### Notes-[NNN]
[Any cross-references, dependencies on other issues, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID                                                                                                        | Severity   | Type                    | Status     | Tiers Affected       | Title                                                                        |
| --------------------------------------------------------------------------------------------------------- | ---------- | ----------------------- | ---------- | -------------------- | ---------------------------------------------------------------------------- |
| \[ISSUE-001\](#issue-001-schema-omits-supersede_pending-from-ddrnode-status-enum)                         | `CRITICAL` | `SCHEMA_DEFECT`         | `RESOLVED` | All (schema)         | Schema omits SUPERSEDE_PENDING from DdrNode status enum                      |
| \[ISSUE-002\](#issue-002-schema-missing-derivation_mode-field-on-parentcitation)                          | `CRITICAL` | `SCHEMA_DEFECT`         | `RESOLVED` | All (schema)         | Schema missing `derivation_mode` field on ParentCitation                     |
| \[ISSUE-003\](#issue-003-cl-node_schema-property-not-permitted-by-tierdefinition-schema)                  | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | CL (schema)          | CL `node_schema` property not permitted by TierDefinition schema             |
| \[ISSUE-004\](#issue-004-lifecycle-block-not-covered-by-ddr_node_schema)                                  | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | All (schema)         | `lifecycle` block not covered by ddr_node_schema                             |
| \[ISSUE-005\](#issue-005-are_scoring_profiles-not-covered-by-ddr_node_schema)                             | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | ARE (schema)         | `are_scoring_profiles` not covered by ddr_node_schema                        |
| \[ISSUE-006\](#issue-006-errata_log-not-covered-by-ddr_node_schema)                                       | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | All (schema)         | `errata_log` not covered by ddr_node_schema                                  |
| \[ISSUE-007\](#issue-007-reconciliation_manifest_schema-not-covered-by-ddr_node_schema)                   | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | All (schema)         | `reconciliation_manifest_schema` not covered by ddr_node_schema              |
| \[ISSUE-008\](#issue-008-verify_citation_logic-not-permitted-by-tierdefinition-schema)                    | `MODERATE` | `SCHEMA_DEFECT`         | `RESOLVED` | CL (schema)          | `verify_citation_logic` not permitted by TierDefinition schema               |
| [ISSUE-009](#issue-009-errata_log-references-v4-versions-in-a-v5-specification)                           | `MODERATE` | `MIGRATION_GAP`         | `RESOLVED` | All                  | `errata_log` references v4 versions in a v5 specification                    |
| \[ISSUE-010\](#issue-010-atomicinclusionrule-schema-missing-verification_mode-and-applies_when-fields)    | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | All (schema)         | AtomicInclusionRule schema missing `verification_mode` and `applies_when`    |
| \[ISSUE-011\](#issue-011-extensionentry-schema-missing-scoring_profile-property)                          | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | ARE (schema)         | ExtensionEntry schema missing `scoring_profile` property                     |
| \[ISSUE-012\](#issue-012-candidate_pool-schema-missing-activation_states-and-checkpoint_path)             | `MAJOR`    | `SCHEMA_DEFECT`         | `RESOLVED` | ARE (schema)         | `candidate_pool` schema missing `activation_states` and `checkpoint_path`    |

---

## ISSUES

---

### ISSUE-001: Schema Omits SUPERSEDE_PENDING from DdrNode Status Enum

<!-- AGENT_CONTEXT
id:          ISSUE-001
status:      RESOLVED
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.1 (node_schema_fields), §7 (operations), lifecycle
rule_refs:   [AX-3, INV-6]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §3.1, §7, lifecycle

#### Problem Statement-001

The `ddr_node_schema.yaml` `DdrNode.status` enum (line 753) lists only 5 values: `[DRAFT, ACTIVE, DIRTY, DEPRECATED, SUPERSEDED]`. However, the `ddr_system_v5.0.yaml` specification explicitly defines `SUPERSEDE_PENDING` as a sixth status value (§3.1 `status` field, `lifecycle.status_transitions`, `operations.SUPERSEDE`, `CDL-7.1` node content). Any YAML file containing a node in `SUPERSEDE_PENDING` status will fail schema validation, making the transactional SUPERSEDE operation unrepresentable in a schema-valid file.

#### Evidence & Justification-001

- `ddr_node_schema.yaml` line 753: `enum: [DRAFT, ACTIVE, DIRTY, DEPRECATED, SUPERSEDED]` — 5 values.
- `ddr_system_v5.0.yaml` §3.1 `node_schema_fields.status` (line 193): *"DRAFT | ACTIVE | DIRTY | DEPRECATED | SUPERSEDED | SUPERSEDE_PENDING"* — 6 values.
- `lifecycle.status_transitions` (lines 2412–2470): defines transitions `ACTIVE → SUPERSEDE_PENDING`, `DIRTY → SUPERSEDE_PENDING`, `DEPRECATED → SUPERSEDE_PENDING`, `SUPERSEDE_PENDING → SUPERSEDED`, and `SUPERSEDE_PENDING → {prior_status}`.
- `CDL-7.1` node content (lines 2279-2280): `StatusEnum` includes `SUPERSEDE_PENDING`.
- `lifecycle.prohibited_transitions` (lines 2472–2509): defines prohibited exits from `SUPERSEDE_PENDING`.

The specification describes `SUPERSEDE_PENDING` as a normative, machine-verifiable status entered during every SUPERSEDE operation. The schema rejects it. This is a direct contradiction between the two files that are supposed to be co-authoritative.

#### Impact Assessment-001

- **Validation failure**: Any DDR project file capturing a mid-SUPERSEDE snapshot will fail schema validation, since `SUPERSEDE_PENDING` is not a valid enum value.
- **Tooling incompatibility**: Any validator built from the schema will reject structurally correct in-flight SUPERSEDE states, producing false violations.
- **Specification integrity**: The system file and the schema file contradict each other on a normative structural property, violating the single-source-of-truth principle.
- **AX-3 violation**: The SUPERSEDE operation cannot be deterministically represented and validated if the schema rejects one of its required intermediate states.

#### Resolution-001: Option A — Add SUPERSEDE_PENDING to DdrNode.status Enum

Add `SUPERSEDE_PENDING` to the `DdrNode.status` enum in `ddr_node_schema.yaml`:

```yaml
status:
  type: string
  enum: [DRAFT, ACTIVE, DIRTY, DEPRECATED, SUPERSEDED, SUPERSEDE_PENDING]
```

Update the description to include the SUPERSEDE_PENDING transition semantics already documented in the system file. This is a single-line schema fix that brings the schema into alignment with the specification.

#### Resolution-001: Option B — Model SUPERSEDE_PENDING as an Operational State Outside the Schema Enum

Retain the 5-value enum and add a separate optional boolean field `supersede_pending` (or reuse the existing `prior_status` field's presence as the indicator) to signal in-flight SUPERSEDE status without extending the core status enum. Update the specification to describe SUPERSEDE_PENDING as a runtime-only operational state that is never persisted to a serialized YAML file.

The rationale: SUPERSEDE_PENDING is transient and should never appear in a persisted file. The schema validates at-rest state, not in-flight state. Add a normative note: *"SUPERSEDE_PENDING is an in-memory operational state. Serialized DDR files must not contain nodes with status SUPERSEDE_PENDING; such nodes must either commit to SUPERSEDED or rollback to prior_status before serialization."*

#### Notes-001

Option A is the simpler fix but implies that serialized files may contain SUPERSEDE_PENDING nodes, which the specification describes as transient. Option B is more architecturally principled but requires updating the specification's `node_schema_fields` and `lifecycle` sections to explicitly distinguish runtime states from persistable states — a concept not currently present in the specification. If Option B is chosen, ISSUE-001 interacts with any future "DAG serialization contract" work.

---

### ISSUE-002: Schema Missing `derivation_mode` Field on ParentCitation

<!-- AGENT_CONTEXT
id:          ISSUE-002
status:      RESOLVED
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.1 (node_schema_fields), §3.2, §3.7, ParentCitation def
rule_refs:   [CIT-R2, CIT-R6, AX-3]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §3.1, §3.2, §3.7

#### Problem Statement-002

The `ddr_node_schema.yaml` `ParentCitation` definition (lines 808–828) requires only `id` and `edge_type` and sets `additionalProperties: false`. The `derivation_mode` field — which is defined in the specification's `node_schema_fields` (§3.1), used in `CIT-R2`, `CIT-R6`, edge type definitions (§3.2), and the canonical DAG nodes — is entirely absent from the schema's `ParentCitation`. Any YAML file including `derivation_mode` on a parent citation will fail schema validation.

#### Evidence & Justification-002

- `ddr_node_schema.yaml` `ParentCitation` (lines 808–828): only `id` and `edge_type` are declared; `additionalProperties: false` blocks any additional fields.
- `ddr_system_v5.0.yaml` §3.1 `parent_ids` field (lines 183-189): *"each entry is a typed edge reference: {id, edge_type, derivation_mode?}. For edge_type='derives', derivation_mode MAY be supplied as semantic|traceability."*
- `CIT-R2` (line 304-309): *"For edge_type='derives', derivation_mode may be provided as semantic|traceability."*
- `CIT-R6` (line 322-325): *"Any derives edge used as an authority linkage (traceability citation) MUST set derivation_mode to 'traceability'."*
- Canonical nodes (e.g., SIL-1.1 at line 2111): `derivation_mode: semantic` is used directly.

The specification treats `derivation_mode` as a normative optional field with a `CIT-R6` mandatory-use condition. The schema completely omits it and actively rejects it.

#### Impact Assessment-002

- **Validation failure**: 5 canonical DAG nodes in `ddr_system_v5.0.yaml` that use `derivation_mode` (SIL-1.1, GPCL-2.1, FCL-3.1, CL-4.1, SAL-5.1) will fail schema validation against `ddr_node_schema.yaml`.
- **Self-validation broken**: The system file *cannot validate against its own schema* — the file that defines the schema rules cannot pass the schema it defines.
- **CIT-R6 unenforceble**: The rule requiring `derivation_mode: traceability` for authority linkages cannot be structurally validated because the field doesn't exist in the schema.

#### Resolution-002: Option A — Add `derivation_mode` to ParentCitation Schema

Add the optional `derivation_mode` field to the `ParentCitation` definition:

```yaml
ParentCitation:
  type: object
  title: "Parent Citation"
  description: "A single typed parent-child citation (§3.7 CIT-R1 through CIT-R6)."
  required: [id, edge_type]
  additionalProperties: false
  properties:
    id:
      type: string
      pattern: "^(XPD-0\\.[0-9]+|[A-Z]{2,5}-[0-9]+\\.[0-9]+)$"
      description: "Parent node ID."
    edge_type:
      type: string
      enum: [derives, constrains, implements, extends]
      description: "Semantic relationship type (§3.2)."
    derivation_mode:
      type: string
      enum: [semantic, traceability]
      description: >
        Optional subtype for 'derives' edges (§3.2, CIT-R2, CIT-R6).
        'semantic' = child content derived from parent requirements.
        'traceability' = parent cited as authority linkage only.
        Default: semantic when omitted. Valid only when edge_type = derives.
```

#### Resolution-002: Option B — Remove `derivation_mode` from Specification and Canonical Nodes

If the intention is to keep the schema minimal, remove all references to `derivation_mode` from the specification's `node_schema_fields`, `CIT-R2`, `CIT-R6`, `edge_type_definitions`, and all canonical node `parent_ids` entries. Revert to the v4.0 ISSUE-001 Option A approach (reintroduce `cites` as a distinct edge type) to restore audit trail precision without an optional annotation field.

This would be a significant regression, undoing the v4.0 ISSUE-001 resolution. It is listed here as the structurally distinct alternative.

#### Notes-002

Option A is strongly preferred. Option B would require re-opening a resolved v4.0 design decision. These two issues (001 and 002) taken together mean that `ddr_system_v5.0.yaml` cannot currently validate against `ddr_node_schema.yaml` — the system file fails its own schema.

---

### ISSUE-003: CL `node_schema` Property Not Permitted by TierDefinition Schema

<!-- AGENT_CONTEXT
id:          ISSUE-003
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [CL]
section_ref: §5 (Tier 4 CL)
rule_refs:   [CL-R9, CL-R9-imposed]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `CL` | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §5 Tier 4

#### Problem Statement-003

The CL tier definition in `ddr_system_v5.0.yaml` (lines 717–728) includes a `node_schema` property defining the `constraint_origin` enum field. The `TierDefinition` schema in `ddr_node_schema.yaml` (lines 526–569) does not include `node_schema` as a permitted property and sets `additionalProperties: false`. The CL tier definition will fail schema validation.

#### Evidence & Justification-003

- `ddr_system_v5.0.yaml` CL tier (line 717–728): declares `node_schema.constraint_origin` with `type: enum`, `values: [derived, imposed]`.
- `ddr_node_schema.yaml` `TierDefinition` (lines 526–569): permitted properties are `tier_id`, `label`, `layer_label`, `core_question`, `is_optional`, `is_terminal_leaf`, `is_merge_node`, `activation_condition`, `root_when`, `design_decision`, `parent_relationships`, `child_relationships`, `atomic_inclusion_rules`, `atomic_exclusion_rules`. No `node_schema` property. `additionalProperties: false`.

#### Impact Assessment-003

- The system file's CL tier definition is structurally valid per the specification but rejected by its own schema.
- The `constraint_origin` field — which was introduced in v5.0 to resolve v4.0 ISSUE-002 (FCL→CL edge direction inversion) — cannot be validated as part of the tier definition.
- Tooling that validates the system file against the schema will report a false violation on the CL tier.

#### Resolution-003: Option A — Add `node_schema` Property to TierDefinition

Extend the `TierDefinition` schema definition to include an optional `node_schema` property:

```yaml
TierDefinition:
  properties:
    # ... existing properties ...
    node_schema:
      type: object
      description: >
        Optional tier-specific node property declarations. Defines additional
        fields that nodes in this tier must carry beyond the base DdrNode schema.
      additionalProperties:
        type: object
        properties:
          type:
            type: string
          values:
            type: array
            items:
              type: string
          default:
            type: string
          required:
            type: boolean
          description:
            type: string
```

Additionally, add `constraint_origin` as an optional property on `DdrNode` itself (in the schema) so that CL-tier nodes can carry it and pass node-level validation.

#### Resolution-003: Option B — Encode `constraint_origin` as a CL Atomic Inclusion Rule Instead

Remove the `node_schema` block from the CL tier definition. Instead, encode the `constraint_origin` requirement as a structural atomic inclusion rule `CL-R11`:

> *"Every CL node must declare a `constraint_origin` field in its content header with value `derived` or `imposed`. VALIDATE enforces this as a structural pattern match."*

Move the runtime enforcement from a schema-level field to a content-level convention. This avoids extending the `TierDefinition` schema for a single tier's custom property, keeping the schema simpler. The trade-off is that `constraint_origin` becomes a content convention rather than a schema-enforced property.

#### Notes-003

Option A is preferred because `constraint_origin` is referenced by `CL-R9`, `CL-R9-imposed`, and `verify_citation_logic` as a machine-evaluable branching condition. Making it a content convention (Option B) would weaken the deterministic enforcement that the v5.0 design requires.

---

### ISSUE-004: `lifecycle` Block Not Covered by ddr_node_schema

<!-- AGENT_CONTEXT
id:          ISSUE-004
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §3.8, lifecycle
rule_refs:   [AX-3]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. lifecycle (§3.8)

#### Problem Statement-004

The `ddr_system_v5.0.yaml` contains a top-level `lifecycle` block (lines 2411-2550) defining `status_transitions`, `prohibited_transitions`, and `guard_definitions`. This block carries an authority comment declaring it the *"machine-parseable authority for DDR node status lifecycle semantics."* The `ddr_node_schema.yaml` does not list `lifecycle` as a permitted top-level property and sets `additionalProperties: false` at the root level. The entire lifecycle state machine will fail schema validation.

#### Evidence & Justification-004

- `ddr_system_v5.0.yaml` lines 2411-2550: `lifecycle:` block with `status_transitions`, `prohibited_transitions`, `guard_definitions`.
- `ddr_system_v5.0.yaml` line 2407: Authority comment: *"This lifecycle block is the machine-parseable authority for DDR node status lifecycle semantics."*
- `ddr_node_schema.yaml` line 30: `additionalProperties: false` at root.
- `ddr_node_schema.yaml` `properties` (lines 32–356): does not include `lifecycle`.

#### Impact Assessment-004

- The machine-parseable lifecycle state machine — the normative authority for all status transitions — will cause the system file to fail its own schema validation.
- Any tooling relying on schema validation to gate file acceptance will reject the system file.
- The lifecycle block is the resolution artifact for v4.0 ISSUE-006 and ISSUE-007. Its exclusion from the schema undermines those resolved issues.

#### Resolution-004: Option A — Add `lifecycle` Property to the Root Schema

Add `lifecycle` as an optional top-level property in `ddr_node_schema.yaml` with a structured definition:

```yaml
lifecycle:
  type: object
  description: "Node status lifecycle state machine (§3.8)."
  additionalProperties: false
  properties:
    status_transitions:
      type: array
      items:
        $ref: "#/$defs/StatusTransition"
    prohibited_transitions:
      type: array
      items:
        $ref: "#/$defs/ProhibitedTransition"
    guard_definitions:
      type: array
      items:
        $ref: "#/$defs/GuardDefinition"
```

And define the corresponding `$defs` entries for `StatusTransition`, `ProhibitedTransition`, and `GuardDefinition`.

#### Resolution-004: Option B — Extract Lifecycle to a Separate Schema File

Create a new `ddr_lifecycle_schema.yaml` that validates only the lifecycle block. Update the system file to reference both schemas. Keep the node schema focused on structural node validation and the lifecycle schema focused on state machine validation. This separates concerns and avoids growing the node schema with non-node definitions.

#### Notes-004

This issue is one of several (ISSUE-004 through ISSUE-007) where the system file contains top-level blocks not covered by the schema. They can be addressed individually or as a batch. Option A is the simpler approach for each; Option B may be preferred if a schema-per-concern design pattern is adopted.

---

### ISSUE-005: `are_scoring_profiles` Not Covered by ddr_node_schema

<!-- AGENT_CONTEXT
id:          ISSUE-005
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [ARE_E5]
section_ref: §9 (E5 ARE), are_scoring_profiles
rule_refs:   [ARE-R2, ARE-R5]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** ARE (E5), schema | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §9, are_scoring_profiles

#### Problem Statement-005

The `ddr_system_v5.0.yaml` contains a top-level `are_scoring_profiles` block (lines 1716-1814) defining `standard_v1`, `conservative_v1`, and `custom` profile schemas including `input_signals`, `score_bands`, `minimum_surfacing_threshold`, and `override_policy`. This block is the normative rubric for `ARE-R2` and `ARE-R5` compliance. The `ddr_node_schema.yaml` does not include `are_scoring_profiles` as a permitted root property, causing schema validation failure.

#### Evidence & Justification-005

- `ddr_system_v5.0.yaml` lines 1716-1814: `are_scoring_profiles:` with three profile definitions.
- `ARE-R5` (line 1577): *"Every ARE deployment must declare a scoring_profile in its Extension contract. The scoring_profile value must reference a profile defined in are_scoring_profiles."*
- `ddr_node_schema.yaml` root `additionalProperties: false` and no `are_scoring_profiles` property listed.

#### Impact Assessment-005

- Schema validation rejects the system file due to the unrecognized `are_scoring_profiles` property.
- `ARE-R5` compliance cannot be structurally validated because the profiles it references are not schema-representable.
- This was the resolution artifact for v4.0 ISSUE-009. Its exclusion from the schema leaves that resolution incomplete.

#### Resolution-005: Option A — Add `are_scoring_profiles` to Root Schema

Add `are_scoring_profiles` as an optional top-level property with structured definitions for scoring profiles, signals, bands, and custom profile requirements.

#### Resolution-005: Option B — Subsume Under `extension_system` or `extension_catalog`

Move `are_scoring_profiles` to be a child of the existing `extension_system` block (or the E5 entry in `extension_catalog`), avoiding a new top-level property. Update the system file to nest `are_scoring_profiles` under `extension_system` and extend the `extension_system` schema definition to accommodate it.

#### Notes-005

Option B is more architecturally coherent — scoring profiles are an ARE-specific concern and logically belong under the extension system's schema umbrella. Option A is a simpler, lower-risk fix. This issue is related to ISSUE-004, ISSUE-006, and ISSUE-007 as part of a pattern of top-level blocks missing from the schema.

---

### ISSUE-006: `errata_log` Not Covered by ddr_node_schema

<!-- AGENT_CONTEXT
id:          ISSUE-006
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §1 (system_metadata)
rule_refs:   [AX-3]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §1

#### Problem Statement-006

The `ddr_system_v5.0.yaml` contains a top-level `errata_log` block (lines 100–114) documenting a corrected issue (ISSUE-011 from v4.0). The `ddr_node_schema.yaml` does not include `errata_log` as a permitted root property, and the root-level `additionalProperties: false` will cause schema validation failure.

#### Evidence & Justification-006

- `ddr_system_v5.0.yaml` lines 100–114: `errata_log:` with one erratum entry containing `issue_id`, `description`, `resolution`, `authority`, `version_introduced`, `version_fixed`.
- `ddr_node_schema.yaml` root `additionalProperties: false` — no `errata_log` allowed.

#### Impact Assessment-006

- Schema validation rejects the system file.
- The formal record of corrections to prior versions — an audit trail requirement — is structurally unrepresentable in a schema-valid file.

#### Resolution-006: Option A — Add `errata_log` to Root Schema

Add `errata_log` as an optional top-level property with an array of erratum entries:

```yaml
errata_log:
  type: array
  description: "Record of corrections to prior specification versions."
  items:
    $ref: "#/$defs/ErratumEntry"
```

Define `ErratumEntry` in `$defs` with required fields `issue_id`, `description`, `resolution`, `authority`, `version_introduced`, `version_fixed`.

#### Resolution-006: Option B — Nest Under `system_metadata`

Move `errata_log` to be a child of `system_metadata` since it documents specification-level corrections. Add it to the `system_metadata` schema definition. Update the system file to nest `errata_log` under `system_metadata`.

#### Notes-006

Option B is more structurally coherent — errata are metadata about the system specification, not an independent top-level concept. Part of the same pattern as ISSUE-004, ISSUE-005, and ISSUE-007.

---

### ISSUE-007: `reconciliation_manifest_schema` Not Covered by ddr_node_schema

<!-- AGENT_CONTEXT
id:          ISSUE-007
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §7 (operations)
rule_refs:   [AX-3]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §7

#### Problem Statement-007

The `ddr_system_v5.0.yaml` `operations` block contains a `reconciliation_manifest_schema` sub-block (lines 1290–1317) defining `manifest_item_types` including `MISSING_MEDIATOR`, `SUPERSEDE_FAILED`, and `SUPERSEDE_PENDING_DETECTED` with their fields and severity levels. The `ddr_node_schema.yaml` `Operation` schema under `operations` (lines 226–251) does not include a `reconciliation_manifest_schema` property and the `operations` definition sets `additionalProperties: false`.

#### Evidence & Justification-007

- `ddr_system_v5.0.yaml` lines 1290–1317: `reconciliation_manifest_schema:` block under `operations`.
- `ddr_node_schema.yaml` `operations` (lines 226–251): permitted properties are `core_operations`, `design_decision_removed_ops`, `dirty_flag_triggers`, `dirty_flag_notes`, `resolution_workflow`, `reconciliation_manifest_tracks`. No `reconciliation_manifest_schema`.

#### Impact Assessment-007

- The `reconciliation_manifest_schema` formalizes the manifest item types introduced by v4.0 ISSUE-005, ISSUE-007, and ISSUE-008 resolutions. Its rejection by the schema means these resolution artifacts cannot be structurally validated.
- Tooling that validates manifest output cannot reference a schema-embedded type definition.

#### Resolution-007: Option A — Add `reconciliation_manifest_schema` to Operations Schema

Extend the `operations` object definition in `ddr_node_schema.yaml` to include `reconciliation_manifest_schema` as a permitted property, with structured definitions for `manifest_item_types`.

#### Resolution-007: Option B — Separate Manifest Schema into Its Own File

Extract the reconciliation manifest schema into a standalone `ddr_manifest_schema.yaml` that can be independently validated and version-controlled. Reference it from the system file. This supports future growth of manifest item types without bloating the node schema.

#### Notes-007

Part of the pattern with ISSUE-004, ISSUE-005, ISSUE-006. A batch resolution addressing all four schema-gap issues simultaneously would be most efficient.

---

### ISSUE-008: `verify_citation_logic` Not Permitted by TierDefinition Schema

<!-- AGENT_CONTEXT
id:          ISSUE-008
status:      RESOLVED
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   [CL]
section_ref: §5 (Tier 4 CL)
rule_refs:   [CL-R9, CL-R9-imposed]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `CL` | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §5 Tier 4

#### Problem Statement-008

The CL tier definition in `ddr_system_v5.0.yaml` (lines 807–813) includes a `verify_citation_logic` block defining conditional enforcement of `CL-R9` vs. `CL-R9-imposed` based on `constraint_origin`. The `TierDefinition` schema does not include `verify_citation_logic` as a permitted property and sets `additionalProperties: false`.

#### Evidence & Justification-008

- `ddr_system_v5.0.yaml` lines 807–813: `verify_citation_logic:` with `branches` defining conditional rule enforcement.
- `ddr_node_schema.yaml` `TierDefinition` (lines 526–569): no `verify_citation_logic` property; `additionalProperties: false`.

#### Impact Assessment-008

- The conditional citation enforcement logic — the key mechanism for the v5.0 CL imposed/derived distinction — cannot be schema-validated.
- This is semantically related to ISSUE-003 (both involve CL-specific tier definition properties not in the schema).

#### Resolution-008: Option A — Add `verify_citation_logic` to TierDefinition Schema

Add an optional `verify_citation_logic` property to the `TierDefinition` schema, typed as an object with a `branches` array.

#### Resolution-008: Option B — Merge Verification Logic into Atomic Inclusion Rules

Eliminate the separate `verify_citation_logic` block by encoding the conditional enforcement directly within `CL-R9` and `CL-R9-imposed` using the existing `applies_when` convention (which `CL-R9` already uses at line 785). Remove the `verify_citation_logic` block entirely — the `applies_when` conditions on the rules themselves already express the conditional logic. This avoids extending the schema for a one-off structural block.

#### Notes-008

Option B is preferred because the `applies_when` condition on `CL-R9` and `CL-R9-imposed` already captures the branching logic — the `verify_citation_logic` block is effectively redundant with those conditions. Removing it simplifies both the system file and the schema. Note, however, that `applies_when` itself is not in the `AtomicInclusionRule` schema (see ISSUE-010).

---

### ISSUE-009: `errata_log` References v4 Versions in a v5 Specification

<!-- AGENT_CONTEXT
id:          ISSUE-009
status:      OPEN
severity:    MODERATE
type:        MIGRATION_GAP
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §1 (errata_log)
rule_refs:   [AX-3]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MODERATE` | **Type:** `MIGRATION_GAP`
**Tiers Affected:** All | **Spec Section:** §1

> **Resolution (2026-03-25):** Option A — Cleared legacy v4 errata log entries and added archival note to schema. §1.2

#### Problem Statement-009

The `errata_log` in `ddr_system_v5.0.yaml` (lines 100–114) records an erratum with `version_introduced: "4.0.0"` and `version_fixed: "4.0.1"`. This erratum documents a correction that occurred during the v4.0 lifecycle and has been superseded by the v5.0 specification. Including v4-era errata in a v5.0 specification without clear lineage policy creates ambiguity about whether errata are inherited across major versions.

#### Evidence & Justification-009

- `errata_log` entry (lines 101–114): `issue_id: "ISSUE-011"`, `version_introduced: "4.0.0"`, `version_fixed: "4.0.1"`.
- The v5.0 specification header (line 35): `lineage: "Supersedes DDR v4.0"` — v4.0 is fully superseded.
- `version_history` (lines 1943–1948): v4.0 is listed as a historical version; the active version is v5.0.

The erratum describes a fix applied within v4.0 (4.0.0 → 4.0.1). In v5.0, the ORL-R7 mapping issue is resolved by design (ORL is absorbed into GPCL). Carrying this erratum forward in the v5.0 file without an inheritance policy creates confusion about whether future readers should be concerned about a problem that no longer applies.

#### Impact Assessment-009

- Readers and tooling processing the v5.0 errata log will encounter historical references to v4.0 issues, structures (ORL-R7, GPCL-R10 destination collision), and version numbers that have no current applicability.
- No normative policy defines whether errata are inherited, archived, or reset on major version increments.

#### Resolution-009: Option A — Archive v4 Errata and Keep Only v5-Applicable Errata

Clear the `errata_log` block and add a normative note:

> *"Errata from prior DDR versions (v4.0 and earlier) are archived in those versions' documentation. This errata_log records only corrections applicable to v5.0 and later. As of v5.0.0, no errata have been filed."*

Set `errata_log: []` or include the policy note as a non-erratum entry.

#### Resolution-009: Option B — Define an Errata Inheritance Policy

Add a normative `errata_policy` block that defines how errata are handled across versions:

```yaml
errata_policy:
  inheritance: "carry_forward"
  description: >
    Errata from superseded versions are retained for audit completeness.
    Each entry carries version_introduced and version_fixed to indicate
    the version lifecycle of the correction. Readers should ignore errata
    with version_fixed values predating the current ddr_version unless
    performing historical audit.
```

This establishes a clear convention and preserves the audit trail.

#### Notes-009

Option A is cleaner for a v5.0 specification that declares it supersedes v4.0. Option B preserves the full audit history but adds complexity. The choice depends on whether the DDR Architecture Board values clean-slate versioning or complete historical traceability.

---

### ISSUE-010: AtomicInclusionRule Schema Missing `verification_mode` and `applies_when` Fields

<!-- AGENT_CONTEXT
id:          ISSUE-010
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [XPD, SIL, GPCL, FCL, CL, SAL, ICL, CDL, ISL]
section_ref: §5, AtomicInclusionRule $def
rule_refs:   [AX-3, CL-R9]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** All | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §5

#### Problem Statement-010

The `AtomicInclusionRule` definition in `ddr_node_schema.yaml` (lines 490–500) declares only three properties: `rule_id`, `statement`, `violation_consequence`, with `additionalProperties: false`. The system file uses two additional properties across all tier definitions: `verification_mode` (on every atomic inclusion rule per v4.0 ISSUE-004 resolution) and `applies_when` (on `CL-R9` and `CL-R9-imposed`). Both fields will cause schema validation failure.

#### Evidence & Justification-010

- `ddr_node_schema.yaml` `AtomicInclusionRule` (lines 490–500): three properties only; `additionalProperties: false`.
- `ddr_system_v5.0.yaml`: every `atomic_inclusion_rules` entry across all 9 tiers includes `verification_mode: structural | semantic` (e.g., XPD-R1 at line 402, FCL-R1 at line 637).
- `ddr_system_v5.0.yaml` `CL-R9` (line 785): `applies_when: "constraint_origin == 'derived'"`.
- `CL-R9-imposed` (line 789): `applies_when: "constraint_origin == 'imposed'"`.
- `verification_mode` was introduced as the resolution for v4.0 ISSUE-004 (AX-3 determinism violation). Its absence from the schema means the resolution is incomplete.

#### Impact Assessment-010

- **Pervasive validation failure**: Every single atomic inclusion rule across all 9 tier definitions in the system file will fail schema validation due to the `verification_mode` field.
- **CL conditional rules broken**: `CL-R9` and `CL-R9-imposed` will additionally fail due to `applies_when`.
- **v4.0 ISSUE-004 resolution incomplete**: The `verification_mode` field was the core resolution artifact. Its absence from the schema means VALIDATE cannot structurally distinguish structural from semantic rules per the filed resolution.

#### Resolution-010: Option A — Add Both Fields to AtomicInclusionRule Schema

Update the `AtomicInclusionRule` definition:

```yaml
AtomicInclusionRule:
  type: object
  required: [rule_id, statement, violation_consequence, verification_mode]
  additionalProperties: false
  properties:
    rule_id:
      type: string
    statement:
      type: string
    violation_consequence:
      type: string
    verification_mode:
      type: string
      enum: [structural, semantic]
      description: >
        Classification for VALIDATE evaluation (v5.0 §5, resolves v4.0 ISSUE-004).
        structural = mechanically verifiable.
        semantic = requires human judgment; emits REVIEW_REQUIRED.
    applies_when:
      type: string
      description: >
        Optional guard condition; rule is enforced only when the condition evaluates
        to true. Used for conditional rules like CL-R9 vs CL-R9-imposed.
```

Make `verification_mode` required (it appears on every rule in the system file). Make `applies_when` optional (it appears only on CL rules).

#### Resolution-010: Option B — Separate Conditional Rules into a Distinct Schema Type

Create a `ConditionalAtomicInclusionRule` extending `AtomicInclusionRule` with `applies_when`, and keep `AtomicInclusionRule` simpler. Use a `oneOf` in the tier definition to allow either type. This preserves schema minimalism for the common case while supporting the conditional case.

Add `verification_mode` to both types as a required field.

#### Notes-010

Option A is simpler and avoids schema type proliferation. Option B is more schema-purist but adds complexity for a single field used on only 2 of ~60+ rules. This issue has the widest blast radius of all issues identified — it affects every atomic inclusion rule in the system file.

---

### ISSUE-011: ExtensionEntry Schema Missing `scoring_profile` Property

<!-- AGENT_CONTEXT
id:          ISSUE-011
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [ARE_E5]
section_ref: §9 (E5 ARE)
rule_refs:   [ARE-R5, EXT-R1]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** ARE (E5), schema | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §9

#### Problem Statement-011

The `ExtensionEntry` schema in `ddr_node_schema.yaml` (lines 637–662) permits only `id`, `name`, `contract`, `reads`, `annotates`, `rules`, and `notes`, with `additionalProperties: false`. The E5 (ARE) entry in `ddr_system_v5.0.yaml` (line 1544) includes a `scoring_profile: standard_v1` field that is not a permitted property. The E5 extension entry will fail schema validation.

#### Evidence & Justification-011

- `ddr_node_schema.yaml` `ExtensionEntry` (lines 637–662): permitted properties are `id`, `name`, `contract`, `reads`, `annotates`, `rules`, `notes`; `additionalProperties: false`.
- `ddr_system_v5.0.yaml` E5 entry (line 1544): `scoring_profile: standard_v1`.
- `ARE-R5` (line 1576–1581): *"Every ARE deployment must declare a scoring_profile in its Extension contract."* — the specification mandates this field.

The specification requires `scoring_profile` on the ARE extension contract. The schema actively rejects it. `ARE-R5` is structurally unenforceable because the field it mandates cannot pass schema validation.

#### Impact Assessment-011

- The E5 extension entry in the system file will fail schema validation due to the unrecognized `scoring_profile` property.
- `ARE-R5` compliance cannot be structurally validated because the field it requires is rejected by the schema.
- This is the same class of defect as ISSUE-002 (a specification-mandated field missing from the schema and blocked by `additionalProperties: false`).

#### Resolution-011: Option A — Add `scoring_profile` to ExtensionEntry Schema

Add an optional `scoring_profile` property to the `ExtensionEntry` schema:

```yaml
ExtensionEntry:
  properties:
    # ... existing properties ...
    scoring_profile:
      type: string
      description: >
        Scoring profile reference for Extensions that produce confidence-scored
        candidates (e.g. ARE). Must reference a profile defined in
        are_scoring_profiles. Omission defaults to standard_v1 per ARE-R5.
```

This is a single-property addition that brings the schema into alignment with `ARE-R5`.

#### Resolution-011: Option B — Move `scoring_profile` into Extension `contract` String

Remove the standalone `scoring_profile` field from the E5 entry and encode the profile declaration within the `contract` string value (e.g., `"ARE-1.0 / DDR-Core-5.x / scoring:standard_v1"`). Update `ARE-R5` to define a parsing convention for extracting the profile reference from the contract string.

This avoids extending the schema but introduces a micro-parsing requirement for the `contract` field and weakens machine-readability.

#### Notes-011

Option A is strongly preferred. Option B trades a simple schema addition for a string-parsing convention that undermines the deterministic machine-readability principle (AX-3). This issue is part of the same pattern as ISSUE-004 through ISSUE-007 — specification features not accommodated by the schema.

---

### ISSUE-012: `candidate_pool` Schema Missing `activation_states` and `checkpoint_path`

<!-- AGENT_CONTEXT
id:          ISSUE-012
status:      RESOLVED
severity:    MAJOR
type:        SCHEMA_DEFECT
tier_refs:   [ARE_E5]
section_ref: §8 (Extension System, candidate_pool)
rule_refs:   [ARE-R6, ARE-R7, AX-3]
created:     2026-03-25
updated:     2026-03-25
resolved:    2026-03-25
-->

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** ARE (E5), schema | **Spec Section:**

> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml. §8

#### Problem Statement-012

The `candidate_pool` object within `extension_system` in `ddr_node_schema.yaml` (lines 271–285) permits only `description`, `candidate_status_value`, `visibility_rule`, `effect_on_core_status`, `promotion_mechanism`, and `discard_trigger`, with `additionalProperties: false`. The system file's `candidate_pool` block (lines 1336–1428) includes `activation_states` (with `active`, `paused`, `disabled` state definitions and `transitions`) and `checkpoint_path` — neither of which is a permitted schema property. The entire ARE tri-state activation lifecycle definition will fail schema validation.

#### Evidence & Justification-012

- `ddr_node_schema.yaml` `candidate_pool` (lines 271–285): six permitted properties only; `additionalProperties: false`.
- `ddr_system_v5.0.yaml` `candidate_pool` (lines 1336–1428): includes `activation_states` (lines 1346–1407) defining the `active`, `paused`, `disabled` states with full transition semantics, and `checkpoint_path` (lines 1408–1414) defining the canonical persistence path.
- `ARE-R6` (lines 1582–1592): mandates the tri-state activation lifecycle defined in `activation_states`.
- `ARE-R7` (lines 1593–1605): mandates checkpoint persistence per `checkpoint_path`.

The `activation_states` block is the normative authority for the ARE tri-state lifecycle introduced as a v5.0 resolution for v4.0 ISSUE-010. Its exclusion from the schema leaves that resolution structurally incomplete.

#### Impact Assessment-012

- The system file's `extension_system.candidate_pool` block will fail schema validation due to the unrecognized `activation_states` and `checkpoint_path` properties.
- `ARE-R6` and `ARE-R7` compliance cannot be structurally validated because the state definitions and checkpoint path they reference are not schema-representable.
- The ARE tri-state lifecycle — the key v5.0 enhancement for ARE operational control — is structurally invisible to schema-based tooling.

#### Resolution-012: Option A — Add `activation_states` and `checkpoint_path` to `candidate_pool` Schema

Extend the `candidate_pool` schema definition to include both properties:

```yaml
candidate_pool:
  properties:
    # ... existing properties ...
    activation_states:
      type: object
      description: >
        Tri-state activation lifecycle for ARE: active, paused, disabled.
        Defines state semantics, transition effects, and persistence rules.
      additionalProperties: false
      properties:
        active:
          type: object
        paused:
          type: object
        disabled:
          type: object
        transitions:
          type: array
          items:
            $ref: "#/$defs/ActivationTransition"
    checkpoint_path:
      type: string
      description: >
        Canonical filesystem path for ARE Pool checkpoint persistence.
        Written on active→paused; deleted on any transition to disabled.
```

Define `ActivationTransition` in `$defs` with `from`, `to`, `effect`, and optional `permitted` fields.

#### Resolution-012: Option B — Extract ARE Lifecycle to a Separate Schema File

Create a new `ddr_are_lifecycle_schema.yaml` that validates the ARE-specific activation states, transitions, and checkpoint semantics independently of the core node schema. This separates the ARE lifecycle concern from the general extension system schema and avoids growing the node schema with extension-specific definitions.

#### Notes-012

Option A is simpler and consistent with the single-schema approach used elsewhere. Option B is appropriate only if a schema-per-concern pattern is adopted across the board (as discussed in ISSUE-004 through ISSUE-007, and also ISSUE-005 Option B). This issue is part of the same pattern — the schema was not updated when v5.0 features were added to the system file.

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue RESOLVED until all steps are confirmed.

```plaintext
1. IDENTIFY issue ID and selected Resolution Option (A or B)
2. DRAFT the specific changes to ddr_system_v5.0.yaml and/or ddr_node_schema.yaml
3. VERIFY draft changes do not introduce new issues (check cross-references in Notes fields)
4. UPDATE the issue entry:
   - Set status: IN_REVIEW
   - Set updated: [date]
5. HUMAN REVIEW of draft changes
6. On approval:
   - Set status: RESOLVED
   - Set resolved: [date]
   - Record resolution: "Option [A|B]: [one-line summary]"
7. UPDATE ISSUE REGISTRY table
8. UPDATE document header metadata (open_issues, resolved_issues)
```

---

## APPENDIX: CROSS-ISSUE DEPENDENCY MAP

> Issues that share a dependency — resolving one may affect the other.

| Issue     | Depends On          | Nature of Dependency                                                                                    |
| --------- | ------------------- | ------------------------------------------------------------------------------------------------------- |
| ISSUE-001 | —                   | Independent; DdrNode status enum fix.                                                                   |
| ISSUE-002 | —                   | Independent; ParentCitation field addition.                                                             |
| ISSUE-003 | ISSUE-008           | Both address CL-specific TierDefinition properties. Resolve together for consistency.                   |
| ISSUE-004 | ISSUE-005, 006, 007 | All four are missing top-level schema properties. Can be batch-resolved.                                |
| ISSUE-005 | ISSUE-004, 006, 007 | Same pattern as ISSUE-004. If Option B is chosen, nesting under extension_system couples it there.      |
| ISSUE-006 | ISSUE-004, 005, 007 | Same pattern. Option B nests under system_metadata.                                                     |
| ISSUE-007 | ISSUE-004, 005, 006 | Same pattern. Related to operations schema scope.                                                       |
| ISSUE-008 | ISSUE-003, 010      | CL tier schema gap; depends on ISSUE-010 if Option B is chosen (relies on applies_when in schema).      |
| ISSUE-009 | —                   | Independent; errata policy decision.                                                                    |
| ISSUE-010 | —                   | Independent; ISSUE-008 Option B depends on this issue (applies_when must exist in the schema first).    |
| ISSUE-011 | —                   | Independent; ExtensionEntry schema gap. Same pattern as ISSUE-004 through ISSUE-007.                    |
| ISSUE-012 | —                   | Independent; candidate_pool schema gap. Same pattern as ISSUE-004 through ISSUE-007.                    |

---

*DDR System v5.0 — Issues Tracker — IT-1.0*
*12 issues identified | 12 resolved | Last updated: 2026-03-25*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*
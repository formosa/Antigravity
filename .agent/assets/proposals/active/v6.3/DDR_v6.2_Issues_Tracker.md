# DDR System v6.2 — Issues Tracker

> **AGENT INSTRUCTION:** This document is the authoritative single source of truth for all
> identified issues with the DDR System v6.2. When processing this document:
>
> 1. Parse the `## ISSUE REGISTRY` table first to assess scope.
> 2. Read the issue heading plus the `Status`, `Severity`, and `Type` metadata lines before reading full content.
> 3. Use `STATUS`, `SEVERITY`, and `TYPE` fields for filtering and prioritization.
> 4. Do NOT infer, create, or modify issues without explicit instruction to do so.
> 5. When adding a new issue, follow the `## ISSUE SCHEMA` exactly and append to `## ISSUES`.
> 6. After any modification, update the `## ISSUE REGISTRY` table and the header metadata counts.

---

## DOCUMENT METADATA

```yaml
document:
  id:              ITR-4c0a27e4-e80c-4cb7-a369-bd0e494dad9c
  title:           "DDR System v6.2 — Issues Tracker"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  last_modified:   "2026-03-27"
  author:          "HuggingFormosa"
  open_issues:     7
  resolved_issues: 0
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT       # Specification makes contradictory claims
    - DESIGN_INADEQUACY      # Feature is absent, under-specified, or insufficient
    - UNNECESSARY_COMPLEXITY # System is more complex than the problem demands
    - AXIOM_VIOLATION        # A rule or behavior contradicts a stated axiom
    - SCHEMA_DEFECT          # Machine-readable schema is incorrect or incomplete
    - MIGRATION_GAP          # Version migration is incomplete or unresolved
    - LIFECYCLE_GAP          # A state, transition, or lifecycle path is undefined
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every new issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.
> If an issue later becomes `RESOLVED`, a one-line blockquote resolution note may be
> inserted above `#### Problem Statement-[NNN]`, but initialization leaves that note absent.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the specific issue. 2-4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the spec, plus the logical chain that makes this a problem.
Use inline code formatting for rule IDs and tier names.]

#### Impact Assessment-[NNN]
[What breaks, is ambiguous, or fails if this issue is not resolved.
State the concrete failure mode.]

#### Resolution-[NNN]: Option A - [Short Label]
[Detailed description of first resolution approach. Include specific rule/section changes
required, draft replacement language where applicable, and any trade-offs.]

#### Resolution-[NNN]: Option B - [Short Label]
[Detailed description of second, distinctly different resolution approach. Must not be
a minor variant of Option A - must represent a meaningfully different design decision.]

#### Notes-[NNN]
[Any cross-references, dependencies on other issues, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID | Severity | Type | Status | Tiers Affected | Title |
| --- | --- | --- | --- | --- | --- |
| [ISSUE-001](#issue-001-require-the-full-system-definition-normative-surface) | `CRITICAL` | `SCHEMA_DEFECT` | `OPEN` | `System-definition files` | Require the full system-definition normative surface |
| [ISSUE-002](#issue-002-enforce-the-mandatory-active-tier-set) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | `All files (root topology)` | Enforce the mandatory active tier set |
| [ISSUE-003](#issue-003-close-supersede_pending-exit-semantics-machine-readably) | `MAJOR` | `LIFECYCLE_GAP` | `OPEN` | `Lifecycle authority` | Close `SUPERSEDE_PENDING` exit semantics machine-readably |
| [ISSUE-004](#issue-004-harden-are-operational-contracts-in-the-schema) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | `Extension System, Extension Catalog` | Harden ARE operational contracts in the schema |
| [ISSUE-005](#issue-005-normalize-express-mode-unbundle-operation-names) | `MODERATE` | `LOGICAL_CONFLICT` | `OPEN` | `Express Mode, Operations, ISL scaffold` | Normalize Express Mode UNBUNDLE operation names |
| [ISSUE-006](#issue-006-type-remaining-normative-rule-identifiers) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | `DAG invariants, tier rules, extension rules` | Type remaining normative rule identifiers |
| [ISSUE-007](#issue-007-align-the-icl-tier-skip-error-code-with-inv-2) | `MINOR` | `LOGICAL_CONFLICT` | `OPEN` | `ICL-6.1, DAG invariants` | Align the ICL tier-skip error code with `INV-2` |

---

## ISSUES

---

### ISSUE-001: Require the Full System-Definition Normative Surface

**Status:** `OPEN` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `System-definition files` | **Spec Section:** `Schema Root, §5-§9`

#### Problem Statement-001

The schema distinguishes project-instance files from system-definition files, but it only requires `lifecycle` when `system_metadata` is present. Other normative sections described as authoritative for system-definition files can still be omitted while remaining schema-valid.

#### Evidence & Justification-001

- `ddr_node_schema_v6.2.yaml:34-36` requires only `lifecycle` when `system_metadata` exists.
- `ddr_node_schema_v6.2.yaml:247-251` says `tier_definitions` are "Required for system-definition files," but no corresponding root conditional requires them.
- The same schema surfaces `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations` as top-level authority sections at `ddr_node_schema_v6.2.yaml:205-289`, yet none are conditionally required for a system-definition profile.
- A direct `jsonschema` validation probe accepted a document containing `ddr_version`, `active_tiers`, `nodes`, `system_metadata`, and `lifecycle` while omitting `tier_definitions`, `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations`.

#### Impact Assessment-001

An incomplete system-definition document can claim authoritative status and still pass the published schema. That weakens the self-hosting contract of DDR v6.2 and allows machine-valid specification files to omit large portions of the normative surface they are supposed to govern.

#### Resolution-001: Option A - Add a Definition Profile Conditional

Add an explicit root conditional keyed to `system_metadata` that requires the minimum normative section set for a system-definition artifact. At minimum this should cover `lifecycle`, `tier_definitions`, `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations`, with any other sections the project considers authoritative for self-hosting spec files.

#### Resolution-001: Option B - Introduce Explicit Document Profiles

Add a root-level `document_profile` enum such as `project_instance | system_definition` and split root requirements by profile rather than inferring profile from `system_metadata`. This is a larger refactor, but it makes document intent explicit and gives future versions a cleaner place to encode profile-specific obligations.

#### Notes-001

- Confirmed from Audit 1 and strengthened with a direct schema validation probe.
- If resolved via explicit profiles, the same mechanism can also tighten the extension-system authority tracked in ISSUE-004.

---

### ISSUE-002: Enforce the Mandatory Active Tier Set

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All files (root topology)` | **Spec Section:** `§3.5`

#### Problem Statement-002

The schema text declares seven mandatory tiers, but the `active_tiers` contract only enforces `minItems: 7` plus enum membership. That allows documents to omit mandatory tiers as long as the count stays at seven.

#### Evidence & Justification-002

- `ddr_node_schema_v6.2.yaml:79-88` says the mandatory tiers are `SIL`, `GPCL`, `FCL`, `SAL`, `ICL`, `CDL`, and `ISL`, while `XPD` and `CL` are optional.
- The same block enforces only `enum`, `minItems: 7`, and `uniqueItems: true`; it does not contain per-tier `contains` constraints for the mandatory members.
- A direct `jsonschema` validation probe accepted `active_tiers: [XPD, SIL, GPCL, FCL, CL, SAL, ICL]`, which still omits mandatory `CDL` and `ISL`.

#### Impact Assessment-002

Files can validate while silently dropping mandatory tiers from the canonical DDR topology. That shifts a core structural invariant out of the schema and into downstream runtime checks, making "schema-valid" weaker than the published topology contract implies.

#### Resolution-002: Option A - Add Mandatory `contains` Constraints

Add one `contains: {const: <TIER>}` constraint per mandatory tier inside an `allOf` block for `active_tiers`. This is the smallest repair because it preserves the current array shape while making the existing prose requirement machine-enforceable.

#### Resolution-002: Option B - Encode Tier Sets as Profile-Specific Contracts

Replace the current loose array rule with profile-aware tier-set contracts that distinguish the mandatory base set from the optional `XPD` and `CL` expansions. This creates a clearer topology contract, but it is a wider root-schema redesign than Option A.

#### Notes-002

- Confirmed from Audit 4 with a direct schema validation probe.
- Independent of ISSUE-001: the mandatory tier set matters for all DDR documents, not only system-definition files.

---

### ISSUE-003: Close `SUPERSEDE_PENDING` Exit Semantics Machine-Readably

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `Lifecycle authority` | **Spec Section:** `§3.8`

#### Problem Statement-003

The lifecycle authority correctly models two legal exits from `SUPERSEDE_PENDING`, but the prohibition table does not machine-close the rest of the state space. The prose says all other exits are prohibited, while the machine-readable blacklist names only `DRAFT`.

#### Evidence & Justification-003

- `ddr_system_v6.2.yaml:2591-2603` defines the only legal exits from `SUPERSEDE_PENDING` as `SUPERSEDE_COMPLETE -> SUPERSEDED` and `SUPERSEDE_ROLLBACK -> prior_status`.
- `ddr_system_v6.2.yaml:2640-2646` lists only `to: [DRAFT]` under `prohibited_transitions` for `SUPERSEDE_PENDING`, even though the reason text says "All other transitions from SUPERSEDE_PENDING are prohibited."
- `ddr_node_schema_v6.2.yaml:1096-1107` models `ProhibitedTransition.to` as an explicit list of status enums, with no machine-readable way to say "all remaining statuses except the allowed rollback form."

#### Impact Assessment-003

Any consumer that interprets `prohibited_transitions` as a closed blacklist can incorrectly treat `SUPERSEDE_PENDING -> ACTIVE`, `DIRTY`, or `DEPRECATED` as not explicitly prohibited. That opens the door to lifecycle divergence across implementations even though the prose intent is clear.

#### Resolution-003: Option A - Add Explicit Closed Exit Metadata

Augment the lifecycle contract with a machine-readable field such as `allowed_targets`, `allows_prior_status_rollback`, or `closed_exit_set` for `SUPERSEDE_PENDING`. This keeps the current table structure while making the exit space fully deterministic for validators.

#### Resolution-003: Option B - Make Allowed Transitions the Sole Authority

Refactor lifecycle validation so `status_transitions` is the only authoritative transition graph and `prohibited_transitions` becomes derived documentation rather than a parallel blacklist. This is a bigger model change, but it removes the need to maintain two partially redundant views of the same state machine.

#### Notes-003

- Confirmed from Audit 4 by comparing the lifecycle authority block against the schema's `ProhibitedTransition` shape.
- This is a machine-completeness gap, not a disagreement with the intended rollback design itself.

---

### ISSUE-004: Harden ARE Operational Contracts in the Schema

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Extension System, Extension Catalog` | **Spec Section:** `§8.2, §9 E5`

#### Problem Statement-004

Several ARE safety contracts are described normatively in the system file but remain only weakly typed in the schema. The most visible gaps are the candidate-pool activation-state model and the end-to-end scoring-profile contract that governs promotion surfacing.

#### Evidence & Justification-004

- `ddr_node_schema_v6.2.yaml:355-360` defines `candidate_pool.activation_states` only as a generic `object`, while `ddr_system_v6.2.yaml:1437-1498` supplies concrete `active`, `paused`, and `disabled` semantics and transition rules.
- A direct `jsonschema` validation probe accepted `activation_states: {banana: {disabled_to_paused: true}}`, showing the tri-state contract is not structurally enforced.
- `ddr_node_schema_v6.2.yaml:941-945` says `ExtensionEntry.scoring_profile` is "Required for E5 (ARE)" and "Must reference a profile defined in are_scoring_profiles," but the field is typed only as `string`.
- Direct `jsonschema` probes accepted both an `E5` extension entry with no `scoring_profile` and an `E5` entry with `scoring_profile: does_not_exist`.
- `ddr_node_schema_v6.2.yaml:983-1002` types `score_bands[].range` as any two-number array and `minimum_surfacing_threshold` as any number; a direct validation probe accepted reversed ranges, overlapping/out-of-band ranges, and `minimum_surfacing_threshold: -0.25`.

#### Impact Assessment-004

The ARE extension's promotion gating and pool-lifecycle safeguards cannot be trusted from the schema boundary alone. Tooling that relies on structural validation may accept impossible activation states, broken scoring references, or mathematically invalid promotion thresholds and only fail much later at runtime.

#### Resolution-004: Option A - Promote ARE Contracts into JSON Schema

Add a typed `activation_states` object with explicit `active`, `paused`, and `disabled` members; add conditional enforcement so `id: E5` requires `scoring_profile`; and constrain `scoring_profile` to known profile identifiers. Also add numeric bounds for thresholds and any structural bounds the schema can reasonably express for score-band ranges.

#### Resolution-004: Option B - Pair the Current Schema with a Required ARE Contract Validator

If full cross-reference and range semantics are considered too awkward for pure JSON Schema, declare these ARE rules runtime-authoritative and ship a deterministic validator that checks activation-state topology, `scoring_profile` existence, threshold bounds, and range sanity. This keeps the schema lighter, but it must be explicitly treated as an incomplete front door rather than the whole contract.

#### Notes-004

- Confirmed from Audit 1 and Audit 4 with multiple direct schema validation probes.
- If ISSUE-001 is resolved by a system-definition profile, ensure `extension_system`, `extension_catalog`, and `are_scoring_profiles` remain part of the required authoritative surface.

---

### ISSUE-005: Normalize Express Mode UNBUNDLE Operation Names

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `Express Mode, Operations, ISL scaffold` | **Spec Section:** `§4, §7, ISL-8.1`

#### Problem Statement-005

The v6.2 operational surface uses two different names for the Express Mode commit phase. Some sections treat the commit operation as `UNBUNDLE`, while others treat it as `UNBUNDLE_EXECUTE`.

#### Evidence & Justification-005

- `ddr_system_v6.2.yaml:377-385` and `391-393` describe `UNBUNDLE_SCAN` as the pre-flight phase and `UNBUNDLE_EXECUTE` as the atomic commit phase.
- `ddr_system_v6.2.yaml:1233-1264` defines `UNBUNDLE_SCAN` and `UNBUNDLE` as the two core operations, but the `UNBUNDLE` entry repeatedly references `UNBUNDLE_EXECUTE`.
- `ddr_system_v6.2.yaml:2544-2549` exposes scaffold functions `unbundle_scan(...)` and `unbundle_execute(...)`, reinforcing the `*_EXECUTE` naming in code-oriented guidance.

#### Impact Assessment-005

Implementers can reasonably ship different operation names for the same behavior depending on which section they treat as canonical. That creates avoidable ambiguity in validators, test names, generated docs, and any public CLI or API surface that mirrors the operations table.

#### Resolution-005: Option A - Make `UNBUNDLE_EXECUTE` Canonical Everywhere

Rename the operations-table entry from `UNBUNDLE` to `UNBUNDLE_EXECUTE` and keep the two-phase pair as `UNBUNDLE_SCAN` plus `UNBUNDLE_EXECUTE` throughout prose, contracts, and scaffolds. This is the cleanest match to the existing pre-flight/commit split already described elsewhere in the spec.

#### Resolution-005: Option B - Collapse the Commit Phase Back to `UNBUNDLE`

Keep `UNBUNDLE` as the canonical public operation and rename the prose and scaffold commit-phase references from `UNBUNDLE_EXECUTE` to `UNBUNDLE`. This preserves the shorter top-level vocabulary, but it gives up the explicit symmetry of `SCAN` versus `EXECUTE`.

#### Notes-005

- Confirmed from Audit 1 by aligning the Express Mode prose, operations table, and ISL scaffold.
- Independent of ISSUE-003: this is naming drift, not a lifecycle-state defect.

---

### ISSUE-006: Type Remaining Normative Rule Identifiers

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `DAG invariants, tier rules, extension rules` | **Spec Section:** `§3.5, §5, §9`

#### Problem Statement-006

Several rule-bearing schema objects still accept arbitrary identifier strings even though sibling rule families already use typed patterns. This leaves key normative identifiers structurally looser than the rest of the contract.

#### Evidence & Justification-006

- `ddr_node_schema_v6.2.yaml:595-603` defines `DagInvariant.id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:676-683` defines `AtomicExclusionRule.rule_id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:919-926` defines `ExtensionRule.rule_id` only as `type: string`, even though `CitationRule.rule_id` and `ExtensionIntegrationRule.rule_id` are pattern-typed elsewhere in the same schema family.
- A direct `jsonschema` validation probe accepted `dag_invariants: [{id: "tier-skip", statement: "bad id still passes"}]`.

#### Impact Assessment-006

Malformed or inconsistent rule identifiers can enter authoritative documents without early rejection. That weakens programmatic cross-referencing, automated filtering, and the reliability of any tooling that expects IDs like `INV-*`, tier-rule IDs, or `ARE-R*` style labels to be structurally well-formed.

#### Resolution-006: Option A - Add Pattern Constraints Per Rule Family

Add explicit regex patterns for each currently untyped rule-ID family, such as `^INV-[0-9]+$` for `DagInvariant.id`, the appropriate `^[A-Z]+-R[0-9]+(?:-imposed)?$` style for atomic rule families, and a typed pattern for extension rules. This is the lowest-blast-radius fix and aligns these families with the stricter rule-ID typing already used elsewhere.

#### Resolution-006: Option B - Centralize Rule-ID Definitions

Create reusable `$defs` for each rule-ID family and reference them wherever those IDs appear, including any future alias or mapping surfaces. This is a larger cleanup, but it reduces drift and gives the spec one place to evolve identifier formats.

#### Notes-006

- Confirmed from Audit 4 and extended slightly to include the adjacent `ExtensionRule` gap visible in the same schema cluster.
- ISSUE-007 becomes easier to resolve cleanly if identifier families are centralized here first.

---

### ISSUE-007: Align the ICL Tier-Skip Error Code with `INV-2`

**Status:** `OPEN` | **Severity:** `MINOR` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `ICL-6.1, DAG invariants` | **Spec Section:** `ICL-6.1, §3.5`

#### Problem Statement-007

The ICL contract names the tier-skip error as `INV-TIER-SKIP`, while the canonical DAG invariant list names that rule `INV-2`. The spec therefore exposes two identifiers for the same invariant without saying they are aliases.

#### Evidence & Justification-007

- `ddr_system_v6.2.yaml:2386-2388` lists `INV-TIER-SKIP (tier skip)` in the `ICL-6.1` error-code set.
- `ddr_system_v6.2.yaml:257-262` defines the authoritative tier-skipping invariant as `INV-2`.
- No alias map or translation note appears nearby to explain whether `INV-TIER-SKIP` is a friendly label, a legacy alias, or an accidental mismatch.

#### Impact Assessment-007

Validator outputs, test fixtures, and documentation can diverge on which identifier represents the tier-skipping rule. Even though the semantics are obvious to a human reader, the dual naming adds unnecessary friction for programmatic cross-reference and support documentation.

#### Resolution-007: Option A - Use `INV-2` in the ICL Error Contract

Replace `INV-TIER-SKIP` with `INV-2` in the `ICL-6.1` error-code list so the contract points directly at the authoritative invariant identifier already defined in `dag_invariants`. This is the smallest fix and removes ambiguity immediately.

#### Resolution-007: Option B - Add an Explicit Alias Map

If the project wants human-readable mnemonics in error payloads, add a small alias table that maps mnemonic labels like `INV-TIER-SKIP` to canonical IDs like `INV-2`. This preserves the friendlier surface while making the translation explicit and machine-readable.

#### Notes-007

- Confirmed from Audit 3.
- If ISSUE-006 centralizes rule-ID typing or alias definitions, resolve this mismatch against that same authority rather than adding a one-off exception.

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue `RESOLVED` until all steps are confirmed.

```plaintext
1. IDENTIFY the issue ID and selected Resolution Option (A or B)
2. DRAFT the specific changes to .agent\assets\proposals\active\v6.2\ddr_system_v6.2.yaml and .agent\assets\proposals\active\v6.2\ddr_node_schema_v6.2.yaml and/or associated schemas
3. VERIFY the draft changes do not introduce new issues (check cross-references in Notes fields)
4. UPDATE the issue entry:
   - Set status: IN_REVIEW
   - Set updated: [date]
5. HUMAN REVIEW of draft changes
6. On approval:
   - Set status: RESOLVED
   - Set resolved: [date]
   - Record resolution: "Option [A|B]: [one-line summary]"
7. UPDATE the ISSUE REGISTRY table
8. UPDATE document header metadata (`open_issues`, `resolved_issues`)
```

---

## APPENDIX: CROSS-ISSUE DEPENDENCY MAP

> Issues that share a dependency - resolving one may affect the other.

| Issue | Depends On | Nature of Dependency |
| --- | --- | --- |
| ISSUE-001 | (none) | Root-profile defect; independently actionable. |
| ISSUE-002 | (none) | Topology defect on the shared root contract; independently actionable. |
| ISSUE-003 | (none) | Lifecycle machine-completeness defect; independently actionable. |
| ISSUE-004 | ISSUE-001 | If system-definition profiles are formalized, ensure the ARE authority sections remain required within that profile. |
| ISSUE-005 | (none) | Naming drift in the operational surface; independently actionable. |
| ISSUE-006 | (none) | Identifier-typing cleanup; independently actionable. |
| ISSUE-007 | ISSUE-006 | If identifier families are centralized, align the ICL alias against that same rule-ID authority. |

---

*DDR System v6.2 Issues Tracker — IT-1.0*
*7 issues identified | 0 resolved | Last updated: 2026-03-27*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*

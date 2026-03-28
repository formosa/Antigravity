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
  last_modified:   "2026-03-28"
  author:          "HuggingFormosa"
  open_issues:     11
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
| [ISSUE-004](#issue-004-harden-are-operational-contracts-in-the-schema) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | `Extension System, Extension Catalog, ARE Scoring Profiles` | Harden ARE operational contracts in the schema |
| [ISSUE-008](#issue-008-machine-close-active-tier-topology-consistency) | `MAJOR` | `SCHEMA_DEFECT` | `OPEN` | `All files (root topology, node set)` | Machine-close active-tier topology consistency |
| [ISSUE-009](#issue-009-close-the-operation-identifier-surface-machine-readably) | `MAJOR` | `LOGICAL_CONFLICT` | `OPEN` | `Operations, lifecycle authority, ISL scaffold` | Close the operation identifier surface machine-readably |
| [ISSUE-005](#issue-005-normalize-express-mode-unbundle-operation-names) | `MODERATE` | `LOGICAL_CONFLICT` | `OPEN` | `Express Mode, Operations, ISL scaffold` | Normalize Express Mode UNBUNDLE operation names |
| [ISSUE-006](#issue-006-type-remaining-normative-rule-identifiers) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | `DAG invariants, tier rules, extension rules` | Type remaining normative rule identifiers |
| [ISSUE-010](#issue-010-lock-express-mode-group-compositions-structurally) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | `Express Mode` | Lock Express Mode group compositions structurally |
| [ISSUE-011](#issue-011-enforce-top-level-express-mode-contract-for-express-projects) | `MODERATE` | `SCHEMA_DEFECT` | `OPEN` | `Project instances (express mode)` | Enforce top-level Express Mode contract for express projects |
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

The lifecycle authority correctly models the legal exits from `SUPERSEDE_PENDING`, but the prohibition table does not machine-close the rest of the state space and exhibits the same incompleteness pattern for other non-terminal statuses. The prose treats undefined transitions as prohibited, while the machine-readable blacklists leave several status pairs unstated.

#### Evidence & Justification-003

- `ddr_system_v6.2.yaml:2591-2603` defines the only legal exits from `SUPERSEDE_PENDING` as `SUPERSEDE_COMPLETE -> SUPERSEDED` and `SUPERSEDE_ROLLBACK -> prior_status`.
- `ddr_system_v6.2.yaml:2609-2646` shows that the prohibition table is only partially explicit: `DRAFT` omits `SUPERSEDE_PENDING`, `ACTIVE` omits direct `SUPERSEDED`, `DIRTY` omits direct `SUPERSEDED`, `DEPRECATED` omits direct `SUPERSEDED`, and `SUPERSEDE_PENDING` lists only `DRAFT` even though its reason text says "All other transitions from SUPERSEDE_PENDING are prohibited."
- `ddr_node_schema_v6.2.yaml:1096-1107` models `ProhibitedTransition.to` as an explicit list of status enums, with no machine-readable way to say "all remaining statuses except the allowed rollback form."

#### Impact Assessment-003

Any consumer that interprets `prohibited_transitions` as a closed blacklist can incorrectly treat several undefined edges as not explicitly prohibited, with `SUPERSEDE_PENDING -> ACTIVE|DIRTY|DEPRECATED` as the most visible example. That opens the door to lifecycle divergence across implementations and weakens the claim in `INV-8` that the state machine is complete and closed.

#### Resolution-003: Option A - Add Explicit Closed Transition Metadata

Augment the lifecycle contract with machine-readable fields such as `allowed_targets`, `allows_prior_status_rollback`, or `closed_transition_set` for any status whose blacklist is meant to be exhaustive. At minimum this must close `SUPERSEDE_PENDING`; ideally it should eliminate the current ambiguity for `DRAFT`, `ACTIVE`, `DIRTY`, and `DEPRECATED` at the same time.

#### Resolution-003: Option B - Make Allowed Transitions the Sole Authority

Refactor lifecycle validation so `status_transitions` is the only authoritative transition graph and `prohibited_transitions` becomes derived documentation rather than a parallel blacklist. This is a bigger model change, but it removes the need to maintain two partially redundant views of the same state machine.

#### Notes-003

- Confirmed from the compiled audits and direct comparison of `status_transitions` against `prohibited_transitions`.
- The broadening beyond `SUPERSEDE_PENDING` strengthens the case for Option B, because hand-maintained blacklists are already drifting across multiple statuses.
- This remains a machine-completeness gap, not a disagreement with the intended rollback design itself.

---

### ISSUE-004: Harden ARE Operational Contracts in the Schema

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Extension System, Extension Catalog, ARE Scoring Profiles` | **Spec Section:** `§8.2, §9 E5`

#### Problem Statement-004

Several ARE safety contracts are described normatively in the system file but remain only weakly typed in the schema. The gaps span the candidate-pool activation-state model, `E5` scoring-profile enforcement, custom-profile structural typing, and numeric bounds for score bands and surfacing thresholds.

#### Evidence & Justification-004

- `ddr_node_schema_v6.2.yaml:355-360` defines `candidate_pool.activation_states` only as a generic `object`, while `ddr_system_v6.2.yaml:1437-1498` supplies concrete `active`, `paused`, and `disabled` semantics and transition rules.
- A direct `jsonschema` validation probe accepted `activation_states: {banana: {disabled_to_paused: true}}`, showing the tri-state contract is not structurally enforced.
- `ddr_node_schema_v6.2.yaml:941-945` says `ExtensionEntry.scoring_profile` is "Required for E5 (ARE)" and "Must reference a profile defined in are_scoring_profiles," but the field is typed only as `string`.
- Direct `jsonschema` probes accepted both an `E5` extension entry with no `scoring_profile` and an `E5` entry with `scoring_profile: does_not_exist`.
- `ddr_node_schema_v6.2.yaml:423-434` types `standard_v1` and `conservative_v1` as `$ref: "#/$defs/ScoringProfile"` but types `custom` only as a generic `object` with `additionalProperties: true` and a `required_fields` array.
- `ddr_node_schema_v6.2.yaml:963-1003` defines `ScoringProfile` as requiring `input_signals`, `score_bands`, `minimum_surfacing_threshold`, and `override_policy`, but the `custom` slot does not reference that shape.
- `ddr_system_v6.2.yaml:1652-1672` makes ARE-R2 and ARE-R5 depend on standard or custom scoring profiles satisfying the declared profile contract, including `required_fields` for custom profiles.
- A direct `jsonschema` validation probe accepted `are_scoring_profiles: { custom: { required_fields: [] } }`, which leaves the custom profile path structurally empty while still schema-valid.
- `ddr_node_schema_v6.2.yaml:983-1002` types `score_bands[].range` as any two-number array and `minimum_surfacing_threshold` as any number; direct validation probes accepted reversed ranges, out-of-band values, and `minimum_surfacing_threshold: -0.25`.

#### Impact Assessment-004

The ARE extension's promotion gating and pool-lifecycle safeguards cannot be trusted from the schema boundary alone. Tooling that relies on structural validation may accept impossible activation states, broken scoring references, structurally incomplete custom profiles, or mathematically invalid promotion thresholds and only fail much later at runtime.

#### Resolution-004: Option A - Promote ARE Contracts into JSON Schema

Add a typed `activation_states` object with explicit `active`, `paused`, and `disabled` members; add conditional enforcement so `id: E5` requires `scoring_profile`; constrain `scoring_profile` to known or structurally declared profile identifiers; type `are_scoring_profiles.custom` via `allOf` against `ScoringProfile`; and add numeric bounds for thresholds and range items, with a runtime ordering check if the two-element array form is retained.

#### Resolution-004: Option B - Pair the Current Schema with a Required ARE Contract Validator

If full cross-reference and range semantics are considered too awkward for pure JSON Schema, declare these ARE rules runtime-authoritative and ship a deterministic validator that checks activation-state topology, `scoring_profile` existence/default behavior, custom profile structural completeness, threshold bounds, and range sanity. This keeps the schema lighter, but it must be explicitly treated as an incomplete front door rather than the whole contract.

#### Notes-004

- Confirmed from the compiled audits with multiple direct schema validation probes.
- This issue intentionally absorbs the ARE-specific audit findings about custom profile typing and numeric bounds instead of splitting them into separate tracker entries.
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
- ISSUE-009 tracks the wider operation-identifier taxonomy problem; ISSUE-005 remains intentionally narrow on the `UNBUNDLE` vs `UNBUNDLE_EXECUTE` conflict.

---

### ISSUE-006: Type Remaining Normative Rule Identifiers

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `DAG invariants, tier rules, extension rules` | **Spec Section:** `§3.5, §5, §9`

#### Problem Statement-006

Several rule-bearing schema objects still accept arbitrary identifier strings even though sibling rule families already use typed patterns. This leaves key normative identifiers structurally looser than the rest of the contract.

#### Evidence & Justification-006

- `ddr_node_schema_v6.2.yaml:595-603` defines `DagInvariant.id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:649-655` defines `AtomicInclusionRule.rule_id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:676-683` defines `AtomicExclusionRule.rule_id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:919-926` defines `ExtensionRule.rule_id` only as `type: string`, even though `CitationRule.rule_id` and `ExtensionIntegrationRule.rule_id` are pattern-typed elsewhere in the same schema family.
- Direct `jsonschema` validation probes accepted `dag_invariants: [{id: "tier-skip", statement: "bad id still passes"}]`, malformed `atomic_inclusion_rules[].rule_id` values such as `not-a-rule`, and malformed extension rule IDs such as `wrongprefix-1`.

#### Impact Assessment-006

Malformed or inconsistent rule identifiers can enter authoritative documents without early rejection. That weakens programmatic cross-referencing, automated filtering, and the reliability of any tooling that expects IDs like `INV-*`, tier-rule IDs, or `ARE-R*` style labels to be structurally well-formed.

#### Resolution-006: Option A - Add Pattern Constraints Per Rule Family

Add explicit regex patterns for each currently untyped rule-ID family, such as `^INV-[0-9]+$` for `DagInvariant.id`, the appropriate `^[A-Z]+-R[0-9]+(?:-imposed)?$` style for atomic rule families, and either a unified `^[A-Z]{2,3}-R[0-9]+$` pattern or per-extension prefixes for extension rules. This is the lowest-blast-radius fix and aligns these families with the stricter rule-ID typing already used elsewhere.

#### Resolution-006: Option B - Centralize Rule-ID Definitions

Create reusable `$defs` for each rule-ID family and reference them wherever those IDs appear, including any future alias or mapping surfaces and any extension-prefix normalization. This is a larger cleanup, but it reduces drift and gives the spec one place to evolve identifier formats.

#### Notes-006

- Confirmed from the compiled audits and widened to include `AtomicInclusionRule.rule_id` plus the extension-prefix centralization question.
- The extension-rule prefix problem is intentionally handled inside ISSUE-006 rather than as a separate tracker entry.
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

### ISSUE-008: Machine-Close Active-Tier Topology Consistency

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All files (root topology, node set)` | **Spec Section:** `§3.5, Schema Root`

#### Problem Statement-008

The schema treats `active_tiers` as an ordered declaration of the active DDR topology, but it does not fully enforce the consequences of that declaration. Canonical tier ordering, node-tier membership against `active_tiers`, and representative coverage of the declared topology can all drift while remaining schema-valid.

#### Evidence & Justification-008

- `ddr_node_schema_v6.2.yaml:79-88` describes `active_tiers` as an ordered list with mandatory and optional members, but enforces only enum membership, `minItems: 7`, and `uniqueItems: true`.
- `ddr_node_schema_v6.2.yaml:90-97` describes `nodes` as the instantiated DDR graph and says system-definition files use tier-representative nodes encoding the canonical topology.
- `ddr_system_v6.2.yaml:4` states that the authoritative specification's nodes section "encodes the canonical 9-tier topology with all DAG edges."
- `ddr_system_v6.2.yaml:264-266` defines `INV-3`, under which `XPD` and `CL` are conditionally activatable, implying that inactive tiers are absent from the instantiated topology.
- Direct `jsonschema` validation probes accepted each of the following invalid shapes: a misordered `active_tiers` array, a document with `CL` omitted from `active_tiers` but containing a `CL` node, and a system-definition-shaped document with an empty `nodes` array.

#### Impact Assessment-008

Declared topology and instantiated topology can diverge silently. That weakens any validator, traversal engine, or code generator that derives predecessor logic, root detection, or coverage checks from `active_tiers`, because "schema-valid" no longer guarantees a coherent active graph.

#### Resolution-008: Option A - Add Topology Closure Constraints

Tighten the root contract so `active_tiers` is restricted to the canonical DDR order variants permitted by optional `XPD` and `CL`, then add a deterministic topology validator that enforces node-tier membership against `active_tiers` and, for system-definition files, requires one representative node per active tier. This preserves the current document shape while closing the topology contract.

#### Resolution-008: Option B - Introduce an Explicit Topology Profile Object

Replace the current loose `active_tiers` array contract with a profile-aware topology object that explicitly declares optional-tier activation and drives both allowed node tiers and required representative coverage. This is a broader redesign, but it makes the topology contract first-class instead of inferred from multiple weakly coupled fields.

#### Notes-008

- Complements ISSUE-002 rather than replacing it: ISSUE-002 fixes mandatory tier presence only.
- If ISSUE-001 is resolved via explicit document profiles, the same mechanism can carry this topology closure cleanly.

---

### ISSUE-009: Close the Operation Identifier Surface Machine-Readably

**Status:** `OPEN` | **Severity:** `MAJOR` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `Operations, lifecycle authority, ISL scaffold` | **Spec Section:** `§7, §3.8, SAL-5.1, ICL-6.1`

#### Problem Statement-009

The specification presents a closed set of core operations, but the broader operational surface does not use a single canonical identifier family. The operations table, lifecycle authority, and scaffold guidance expose partially overlapping but non-identical operation names, while the schema types those names only as free strings.

#### Evidence & Justification-009

- `ddr_node_schema_v6.2.yaml:864-870` defines `Operation.name` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:1062-1075` defines `StatusTransition.operation` only as `type: string`.
- `ddr_system_v6.2.yaml:1168-1256` defines the 8 core operations as `INSERT`, `DELETE`, `MODIFY`, `SUPERSEDE`, `VERIFY`, `VALIDATE`, `UNBUNDLE_SCAN`, and `UNBUNDLE`.
- `ddr_system_v6.2.yaml:2557-2607` uses additional lifecycle operation tokens not present in the core-operations table, including `MODIFY|PROPAGATION`, `VERIFY+VALIDATE`, `SUPERSEDE_COMPLETE`, and `SUPERSEDE_ROLLBACK`.
- `ddr_system_v6.2.yaml:2548-2549` exposes `unbundle_execute(...)` in the scaffold surface, reinforcing the broader naming drift already captured narrowly by ISSUE-005.
- Direct `jsonschema` validation probes accepted arbitrary operation names such as `BANANA` in both `operations.core_operations[].name` and `lifecycle.status_transitions[].operation`.

#### Impact Assessment-009

Tooling cannot reliably treat operation identifiers as a closed, canonical namespace. Validators, audit logs, generated APIs, CLI surfaces, and test fixtures can disagree about whether they are comparing atomic operations, lifecycle subphases, or composite aliases, which undermines `AX-3` determinism.

#### Resolution-009: Option A - Split Canonical Operation, Phase, and Effect

Introduce a closed `OperationNameEnum` for the true public operation set, then model lifecycle-specific detail separately using fields such as `phase`, `transition_kind`, or `side_effect`. For example, `SUPERSEDE_COMPLETE` and `SUPERSEDE_ROLLBACK` become `operation: SUPERSEDE` plus explicit phase metadata, while `MODIFY|PROPAGATION` becomes `operation: MODIFY` plus a propagation side-effect annotation.

#### Resolution-009: Option B - Add an Authoritative Alias/Taxonomy Layer

Keep the current strings, but add a machine-readable alias map and operation taxonomy that classifies each token as canonical, composite, lifecycle-subphase, or scaffold alias. Validators must normalize all operation identifiers through that authority before comparison. This is less disruptive, but it preserves more conceptual complexity than Option A.

#### Notes-009

- ISSUE-005 should remain narrow and continue to track the specific `UNBUNDLE` vs `UNBUNDLE_EXECUTE` conflict.
- If Option A is adopted, ISSUE-005 can likely be resolved as part of this broader cleanup.

---

### ISSUE-010: Lock Express Mode Group Compositions Structurally

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Express Mode` | **Spec Section:** `§4`

#### Problem Statement-010

The specification defines a fixed 4-group Express Mode partition, but the schema does not enforce those group compositions. Group IDs are typed, yet the constituent `tiers` arrays remain effectively open.

#### Evidence & Justification-010

- `ddr_system_v6.2.yaml:353-370` defines the canonical Express Mode groups as `G1 = [XPD, SIL, GPCL]`, `G2 = [FCL, CL]`, `G3 = [SAL, ICL]`, and `G4 = [CDL, ISL]`.
- `ddr_node_schema_v6.2.yaml:229-239` models `express_mode.groups` only as an array of `ExpressModeGroup` items, with no machine-readable rule that all four canonical groups appear exactly once.
- `ddr_node_schema_v6.2.yaml:632-644` constrains `group_id` to `G1|G2|G3|G4`, but `tiers` remains only an unconstrained array of strings.
- A direct `jsonschema` validation probe accepted `group_id: G1` with `tiers: [ISL]`.

#### Impact Assessment-010

A document can claim DDR v6.2 Express Mode while redefining the actual group partition. That destabilizes `UNBUNDLE` semantics, group-to-tier allocation logic, and any implementation that assumes the fixed four-group mapping described by the authoritative specification.

#### Resolution-010: Option A - Encode Canonical Group Definitions in the Schema

Constrain `express_mode.groups` so each canonical `group_id` has a fixed `tiers` array and appears exactly once. This is the smallest repair and makes the published G1-G4 partition machine-authoritative.

#### Resolution-010: Option B - Remove Group Definitions from Authored Documents

Treat Express Mode grouping as version-defined system metadata rather than authored content. Documents would declare Express Mode availability, but G1-G4 compositions would be derived from DDR version and therefore not restatable or drift-prone at the document level.

#### Notes-010

- Independent of ISSUE-005: this is a structural-definition defect, not an operation-name defect.
- ISSUE-011 is synergistic: if express-mode documents must carry the top-level `express_mode` section, its group definitions also need to be machine-closed.
- If ISSUE-001 introduces a stricter system-definition profile, `express_mode` should remain part of that required authority surface.

---

### ISSUE-011: Enforce Top-Level Express Mode Contract for Express Projects

**Status:** `OPEN` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Project instances (express mode)` | **Spec Section:** `§4, Express Mode`

#### Problem Statement-011

When `project.mode: express`, the schema correctly forces `express_mode_group` on every node but does not require the top-level `express_mode` object. The section remains entirely optional at the root even though it carries the authoritative `UNBUNDLE` contract.

#### Evidence & Justification-011

- `ddr_node_schema_v6.2.yaml:55-68` adds a conditional requirement for per-node `express_mode_group` when `project.mode` is `express`.
- `ddr_node_schema_v6.2.yaml:229-242` still defines the top-level `express_mode` block as optional and does not require `groups`, `unbundle_determinism_rule`, or `deferred_fragment_handling` when express mode is declared.
- `ddr_system_v6.2.yaml:353-391` supplies the full normative Express Mode contract, including the G1-G4 groups, `UNBUNDLE_SCAN` / `UNBUNDLE_EXECUTE` semantics, determinism rules, and deferred-fragment handling.
- A direct `jsonschema` validation probe accepted a document with `project.mode: express`, nodes carrying `express_mode_group`, and no top-level `express_mode` object.

#### Impact Assessment-011

An Express Mode project-instance can be schema-valid while omitting the authoritative unbundle contract. That breaks deterministic `UNBUNDLE` behavior, validator expectations, and the self-hosting guarantee that every declared consumption mode carries its governing rules.

#### Resolution-011: Option A - Add Explicit Conditional Requirement

Add a root `allOf` clause so `project.mode: express` requires the top-level `express_mode` object, and require at least `groups`, `unbundle_determinism_rule`, and `deferred_fragment_handling` inside that block. This is the minimal targeted repair.

#### Resolution-011: Option B - Leverage Document Profiles

Adopt `document_profile` or another profile-aware root contract, then define an express-capable profile whose required sections include the full `express_mode` authority block by construction. This is the cleaner long-term architecture, especially if ISSUE-001 also moves toward explicit profiles.

#### Notes-011

- Independent of ISSUE-005, but it shares the same operational surface.
- If ISSUE-001 is resolved via explicit document profiles, this gap can be eliminated there rather than via a standalone conditional.

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
| ISSUE-005 | ISSUE-009 | If operation identifiers are normalized through a closed taxonomy, the narrow `UNBUNDLE` naming conflict may resolve as part of that broader cleanup. |
| ISSUE-006 | (none) | Identifier-typing cleanup; independently actionable, including extension-prefix normalization. |
| ISSUE-007 | ISSUE-006 | If identifier families are centralized, align the ICL alias against that same rule-ID authority. |
| ISSUE-008 | ISSUE-002 | Broader topology-closure companion; ISSUE-002 fixes mandatory tier presence only. |
| ISSUE-009 | ISSUE-005 | Broader operation-taxonomy defect; may subsume the narrow `UNBUNDLE` naming fix if a canonical identifier model is adopted. |
| ISSUE-010 | ISSUE-011 | If express-mode documents must carry the top-level `express_mode` block, the group compositions in that block also need to be machine-closed. |
| ISSUE-011 | ISSUE-001 | If explicit document profiles are introduced, the express-mode profile should require the full `express_mode` authority block. |

---

*DDR System v6.2 Issues Tracker — IT-1.0*
*11 issues identified | 0 resolved | Last updated: 2026-03-28*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*

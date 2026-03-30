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
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  last_modified:   "2026-03-28"
  author:          "HuggingFormosa"
  open_issues:     0
  resolved_issues: 11
  status_values:   [OPEN, IN_REVIEW, RESOLVED, WONT_FIX, DEFERRED]
  severity_values: [CRITICAL, MAJOR, MODERATE, MINOR]
  type_values:
    - LOGICAL_CONFLICT
    - DESIGN_INADEQUACY
    - UNNECESSARY_COMPLEXITY
    - AXIOM_VIOLATION
    - SCHEMA_DEFECT
    - MIGRATION_GAP
    - LIFECYCLE_GAP
```

---

## ISSUE SCHEMA

> **AGENT INSTRUCTION:** Every updated issue entry MUST conform exactly to this schema.
> Fields marked `[REQUIRED]` must be populated. Fields marked `[CONDITIONAL]` are
> required only when the condition in brackets is met. Do not add fields not in this schema.
> If an issue later becomes `RESOLVED`, a one-line blockquote resolution note may be
> inserted above `#### Problem Statement-[NNN]`.

```markdown
---

### ISSUE-[NNN]: [Brief Imperative Title]

**Status:** `OPEN` | **Severity:** `[SEVERITY]` | **Type:** `[TYPE]`
**Tiers Affected:** `[TIERS]` | **Spec Section:** `[§ REF]`

#### Problem Statement-[NNN]
[Concise description of the issue. 2-4 sentences maximum.]

#### Evidence & Justification-[NNN]
[Quoted or cited material from the local spec plus the logic that makes this a problem.]

#### Impact Assessment-[NNN]
[Concrete failure mode if the issue is not resolved.]

#### Resolution-[NNN]: Option A - [Short Label]
[First resolution approach.]

#### Resolution-[NNN]: Option B - [Short Label]
[Second, materially different approach.]

#### Resolution-[NNN]: Option C - [Short Label]
[Third, materially different approach.]

#### Comparative Analysis-[NNN]
[Direct comparison of Options A, B, and C.]

#### Recommendation-[NNN]
**Endorsed Option:** `Option A|B|C`
[Precise technical justification for the endorsed option.]

#### Supporting Citations-[NNN]
- [Source Name](https://example.com): One-line explanation of why the source supports the endorsed option.

#### Notes-[NNN]
[Cross-references, dependencies, or implementation context.]
```

---

## ISSUE REGISTRY

> **AGENT INSTRUCTION:** This table is the primary index. Maintain sort order by severity
> then issue number. Update this table whenever any issue's status or severity changes.

| ID | Severity | Type | Status | Tiers Affected | Title |
| --- | --- | --- | --- | --- | --- |
| [ISSUE-001](#issue-001-require-the-full-system-definition-normative-surface) | `CRITICAL` | `SCHEMA_DEFECT` | `RESOLVED` | `System-definition files` | Require the full system-definition normative surface |
| [ISSUE-002](#issue-002-enforce-the-mandatory-active-tier-set) | `MAJOR` | `SCHEMA_DEFECT` | `RESOLVED` | `All files (root topology)` | Enforce the mandatory active tier set |
| [ISSUE-003](#issue-003-close-supersede_pending-exit-semantics-machine-readably) | `MAJOR` | `LIFECYCLE_GAP` | `RESOLVED` | `Lifecycle authority` | Close `SUPERSEDE_PENDING` exit semantics machine-readably |
| [ISSUE-004](#issue-004-harden-are-operational-contracts-in-the-schema) | `MAJOR` | `SCHEMA_DEFECT` | `RESOLVED` | `Extension System, Extension Catalog, ARE Scoring Profiles` | Harden ARE operational contracts in the schema |
| [ISSUE-008](#issue-008-machine-close-active-tier-topology-consistency) | `MAJOR` | `SCHEMA_DEFECT` | `RESOLVED` | `All files (root topology, node set)` | Machine-close active-tier topology consistency |
| [ISSUE-009](#issue-009-close-the-operation-identifier-surface-machine-readably) | `MAJOR` | `LOGICAL_CONFLICT` | `RESOLVED` | `Operations, lifecycle authority, ISL scaffold` | Close the operation identifier surface machine-readably |
| [ISSUE-005](#issue-005-normalize-express-mode-unbundle-operation-names) | `MODERATE` | `LOGICAL_CONFLICT` | `RESOLVED` | `Express Mode, Operations, ISL scaffold` | Normalize Express Mode UNBUNDLE operation names |
| [ISSUE-006](#issue-006-type-remaining-normative-rule-identifiers) | `MODERATE` | `SCHEMA_DEFECT` | `RESOLVED` | `DAG invariants, tier rules, extension rules` | Type remaining normative rule identifiers |
| [ISSUE-010](#issue-010-lock-express-mode-group-compositions-structurally) | `MODERATE` | `SCHEMA_DEFECT` | `RESOLVED` | `Express Mode` | Lock Express Mode group compositions structurally |
| [ISSUE-011](#issue-011-enforce-top-level-express-mode-contract-for-express-projects) | `MODERATE` | `SCHEMA_DEFECT` | `RESOLVED` | `Project instances (express mode)` | Enforce top-level Express Mode contract for express projects |
| [ISSUE-007](#issue-007-align-the-icl-tier-skip-error-code-with-inv-2) | `MINOR` | `LOGICAL_CONFLICT` | `RESOLVED` | `ICL-6.1, DAG invariants` | Align the ICL tier-skip error code with `INV-2` |

---

## ISSUES

---

### ISSUE-001: Require the Full System-Definition Normative Surface

**Status:** `RESOLVED` | **Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `System-definition files` | **Spec Section:** `Schema Root, §5-§9`

> Resolution (2026-03-28): Option B - Introduced explicit document profiles and required the full system_definition normative surface in the v6.3 schema.

#### Problem Statement-001

The schema distinguishes project-instance files from system-definition files, but it only requires `lifecycle` when `system_metadata` is present. Other normative sections described as authoritative for system-definition files can still be omitted while remaining schema-valid.

#### Evidence & Justification-001

- `ddr_node_schema_v6.2.yaml:34-36` requires only `lifecycle` when `system_metadata` exists.
- `ddr_node_schema_v6.2.yaml:247-251` says `tier_definitions` are "Required for system-definition files," but no corresponding root conditional requires them.
- The same schema surfaces `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations` as top-level authority sections at `ddr_node_schema_v6.2.yaml:205-289`, yet none are conditionally required for a system-definition profile.
- `ddr_system_v6.2.yaml:1-6` states that the authoritative system file represents all normative sections from the specification, which is stronger than the root schema currently enforces.
- A direct `jsonschema` validation probe accepted a document containing `ddr_version`, `active_tiers`, `nodes`, `system_metadata`, and `lifecycle` while omitting `tier_definitions`, `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations`.

#### Impact Assessment-001

An incomplete system-definition document can claim authoritative status and still pass the published schema. That weakens the self-hosting contract of DDR v6.2 and allows machine-valid specification files to omit large portions of the normative surface they are supposed to govern.

#### Resolution-001: Option A - Add a Definition Profile Conditional

Add an explicit root conditional keyed to `system_metadata` that requires the minimum normative section set for a system-definition artifact. At minimum this should cover `lifecycle`, `tier_definitions`, `dag_invariants`, `citation_rules`, `constraint_precedence`, and `operations`, with any other sections the project considers authoritative for self-hosting spec files.

#### Resolution-001: Option B - Introduce Explicit Document Profiles

Add a root-level `document_profile` enum such as `project_instance | system_definition` and split root requirements by profile rather than inferring profile from `system_metadata`. This is a larger refactor, but it makes document intent explicit and gives future versions a cleaner place to encode profile-specific obligations.

#### Resolution-001: Option C - Split Root Entry Schemas

Keep the shared node and section definitions, but publish separate root entry schemas for project-instance files and system-definition files. The system-definition entry schema would hard-require the authoritative section set, while the project-instance entry schema would retain the lean root contract. This avoids adding a new in-band discriminator, but it introduces multiple schema IDs and a wider tooling/distribution surface.

#### Comparative Analysis-001

Option A is the smallest patch and preserves backward compatibility, but it continues to infer document intent indirectly from `system_metadata`. Option B makes document intent explicit in-band and gives one schema artifact a clean place to express profile-specific requirements. Option C produces the strongest separation of concerns, yet it increases operational complexity by forcing tooling to choose between multiple root schema entry points.

#### Recommendation-001

**Endorsed Option:** `Option B`

Option B best aligns with a comprehensive and stable DDR contract because it makes authored intent explicit instead of inferred. A `document_profile` discriminator is easier for validators, generators, and humans to reason about than a special-case conditional on `system_metadata`, and it gives future DDR revisions a durable place to encode additional profile-specific rules without piling more inference onto the root.

It also keeps the framework single-source and self-describing. Compared with separate root schemas, an explicit profile field preserves one canonical schema artifact while still allowing precise branching of required sections.

#### Supporting Citations-001

- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance for branching required properties from an explicit discriminator or profile field.
- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance for closing object contracts with explicit required properties and `additionalProperties` behavior.

#### Notes-001

- Confirmed from both audit sets and strengthened with a direct schema validation probe.
- ISSUE-004 and ISSUE-011 become cleaner to resolve if explicit document profiles are adopted here first.

---

### ISSUE-002: Enforce the Mandatory Active Tier Set

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All files (root topology)` | **Spec Section:** `§3.5`

> Resolution (2026-03-28): Option A - Closed `active_tiers` to canonical variants that always include the mandatory base tier set.

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

#### Resolution-002: Option C - Enumerate the Canonical Tier-Set Variants

Replace the current member-based rule with a closed set of the four legal ordered arrays: base only, base plus `XPD`, base plus `CL`, and base plus both optional tiers. This machine-closes both required-member presence and ordering, but it hardcodes policy that overlaps the broader topology work tracked in ISSUE-008.

#### Comparative Analysis-002

Option A directly fixes the defect named in this issue with minimal blast radius. Option B is architecturally cleaner if document profiles are already being introduced, but it broadens the change surface. Option C is stricter than either A or B for this one field, yet it partially collapses into the broader topology-closure work and makes a narrow fix carry too much policy.

#### Recommendation-002

**Endorsed Option:** `Option A`

Option A is the best near-term repair because it closes the mandatory-member gap without prematurely redesigning the root topology model. It upgrades the current prose requirement into machine-readable validation while keeping compatibility with the current document shape and leaving the wider ordering and node-membership concerns to ISSUE-008.

#### Supporting Citations-002

- [JSON Schema Array Reference](https://json-schema.org/understanding-json-schema/reference/array): Official guidance that `contains` can enforce the presence of required members within an array.

#### Notes-002

- Confirmed from Audit 4 with a direct schema validation probe.
- ISSUE-008 remains necessary even after this repair because mandatory-tier presence alone does not close ordering, node-tier membership, or representative coverage.

---

### ISSUE-003: Close `SUPERSEDE_PENDING` Exit Semantics Machine-Readably

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `Lifecycle authority` | **Spec Section:** `§3.8`

> Resolution (2026-03-28): Option B - Made `status_transitions` the sole lifecycle authority and removed `prohibited_transitions`.

#### Problem Statement-003

The lifecycle authority correctly models the legal exits from `SUPERSEDE_PENDING`, but the prohibition table does not machine-close the rest of the state space and exhibits the same incompleteness pattern for other non-terminal statuses. The prose treats undefined transitions as prohibited, while the machine-readable blacklists leave several status pairs unstated.

#### Evidence & Justification-003

- `ddr_system_v6.2.yaml:2591-2603` defines the only legal exits from `SUPERSEDE_PENDING` as `SUPERSEDE_COMPLETE -> SUPERSEDED` and `SUPERSEDE_ROLLBACK -> prior_status`.
- `ddr_system_v6.2.yaml:2609-2646` shows that the prohibition table is only partially explicit: `DRAFT` omits `SUPERSEDE_PENDING`, `ACTIVE` omits direct `SUPERSEDED`, `DIRTY` omits direct `SUPERSEDED`, `DEPRECATED` omits direct `SUPERSEDED`, and `SUPERSEDE_PENDING` lists only `DRAFT` even though its reason text says "All other transitions from SUPERSEDE_PENDING are prohibited."
- `ddr_node_schema_v6.2.yaml:1096-1107` models `ProhibitedTransition.to` as an explicit list of status enums, with no machine-readable way to say "all remaining statuses except the allowed rollback form."
- The incompleteness is therefore systemic, not limited to the `SUPERSEDE_PENDING` row that originally exposed it most clearly.

#### Impact Assessment-003

Any consumer that interprets `prohibited_transitions` as a closed blacklist can incorrectly treat several undefined edges as not explicitly prohibited, with `SUPERSEDE_PENDING -> ACTIVE|DIRTY|DEPRECATED` as the most visible example. That opens the door to lifecycle divergence across implementations and weakens the claim in `INV-8` that the state machine is complete and closed.

#### Resolution-003: Option A - Add Explicit Closed Transition Metadata

Augment the lifecycle contract with machine-readable fields such as `allowed_targets`, `allows_prior_status_rollback`, or `closed_transition_set` for any status whose blacklist is meant to be exhaustive. At minimum this must close `SUPERSEDE_PENDING`; ideally it should eliminate the current ambiguity for `DRAFT`, `ACTIVE`, `DIRTY`, and `DEPRECATED` at the same time.

#### Resolution-003: Option B - Make Allowed Transitions the Sole Authority

Refactor lifecycle validation so `status_transitions` is the only authoritative transition graph and `prohibited_transitions` becomes derived documentation rather than a parallel blacklist. This is a bigger model change, but it removes the need to maintain two partially redundant views of the same state machine.

#### Resolution-003: Option C - Generate Prohibitions from the Authoritative Graph

Keep `status_transitions` as the source of truth, but generate `prohibited_transitions` automatically from `StatusEnum` and the legal transition graph during schema build or validator generation. This preserves a human-readable prohibition table while eliminating manual drift, but it introduces a generation pipeline and makes one published artifact partly derived rather than purely hand-authored.

#### Comparative Analysis-003

Option A repairs the immediate ambiguity, but it retains a dual-authority model that is already drifting. Option B most directly restores lifecycle closure by making one graph authoritative and treating any blacklist view as documentation. Option C also removes manual drift, yet it adds build-time generation complexity and still leaves two published representations to keep conceptually aligned.

#### Recommendation-003

**Endorsed Option:** `Option B`

Option B is the strongest long-term fix because the defect is not just a missing row entry; it is the presence of two lifecycle authorities with different closure properties. A single explicit transition graph is easier to validate, easier to reason about, and harder to let drift than a transition graph plus a hand-maintained blacklist.

The systemic nature of the current omissions makes incremental blacklist repairs less compelling. Once `status_transitions` is definitive, any human-readable prohibited view can be derived without being allowed to redefine behavior.

#### Supporting Citations-003

- [State Chart XML (SCXML)](https://www.w3.org/TR/scxml/): The W3C state-machine model represents legal behavior as explicit per-state transitions, which supports using one authoritative transition graph instead of a parallel blacklist.
- [JSON Schema Enumerated Values](https://json-schema.org/understanding-json-schema/reference/enum): A closed status vocabulary pairs naturally with a single explicit transition graph when modeling finite lifecycle states.

#### Notes-003

- Confirmed from the compiled audits and direct comparison of `status_transitions` against `prohibited_transitions`.
- The widening beyond `SUPERSEDE_PENDING` is evidence-based and makes the issue materially stronger, not broader without support.

---

### ISSUE-004: Harden ARE Operational Contracts in the Schema

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Extension System, Extension Catalog, ARE Scoring Profiles` | **Spec Section:** `§8.2, §9 E5`

> Resolution (2026-03-28): Option B - Hardened ARE structures in schema and delegated profile-resolution plus score-band semantics to deterministic ARE conformance validation.

#### Problem Statement-004

Several ARE safety contracts are described normatively in the system file but remain only weakly typed in the schema. The gaps span the candidate-pool activation-state model, `E5` scoring-profile enforcement, the structural shape of the custom-profile path, and numeric bounds for score bands and surfacing thresholds.

#### Evidence & Justification-004

- `ddr_node_schema_v6.2.yaml:355-360` defines `candidate_pool.activation_states` only as a generic `object`, while `ddr_system_v6.2.yaml:1437-1498` supplies concrete `active`, `paused`, and `disabled` semantics and transition rules.
- A direct `jsonschema` validation probe accepted `activation_states: {banana: {disabled_to_paused: true}}`, showing the tri-state contract is not structurally enforced.
- `ddr_node_schema_v6.2.yaml:941-945` says `ExtensionEntry.scoring_profile` is "Required for E5 (ARE)" and "Must reference a profile defined in are_scoring_profiles," but the field is typed only as `string`.
- Direct `jsonschema` probes accepted both an `E5` extension entry with no `scoring_profile` and an `E5` entry with `scoring_profile: does_not_exist`.
- `ddr_node_schema_v6.2.yaml:423-434` types `standard_v1` and `conservative_v1` as `$ref: "#/$defs/ScoringProfile"` but types `custom` only as a generic `object` with `additionalProperties: true` and a `required_fields` array.
- `ddr_system_v6.2.yaml:1888-1904` confirms that the current `custom` slot behaves like a prose template of required field names, not like a machine-typed scoring profile definition.
- A direct `jsonschema` validation probe accepted `are_scoring_profiles: { custom: { required_fields: [] } }`, which leaves the custom profile path structurally empty while still schema-valid.
- `ddr_node_schema_v6.2.yaml:983-1002` types `score_bands[].range` as any two-number array and `minimum_surfacing_threshold` as any number; direct validation probes accepted reversed ranges, out-of-band values, and `minimum_surfacing_threshold: -0.25`.

#### Impact Assessment-004

The ARE extension's promotion gating and pool-lifecycle safeguards cannot be trusted from the schema boundary alone. Tooling that relies on structural validation may accept impossible activation states, broken scoring references, structurally incomplete custom profiles, or mathematically invalid promotion thresholds and only fail much later at runtime.

#### Resolution-004: Option A - Promote ARE Contracts into JSON Schema

Add a typed `activation_states` object with explicit `active`, `paused`, and `disabled` members; add conditional enforcement so `id: E5` requires `scoring_profile`; constrain `scoring_profile` to known or structurally declared profile identifiers; type the custom profile path against `ScoringProfile`; and add numeric bounds for thresholds and range items, with a runtime ordering check if the two-element array form is retained.

#### Resolution-004: Option B - Use a Hybrid Structural Schema plus ARE Conformance Validator

Use JSON Schema to close the structural rules that it expresses well: typed activation states, `E5`-conditional `scoring_profile` presence, machine-typed profile objects, and basic numeric bounds. Then make a deterministic ARE-specific validator authoritative for cross-reference existence, score-band ordering and non-overlap, and any semantic checks that span multiple objects. This intentionally splits enforcement by concern without leaving the schema front door weak.

#### Resolution-004: Option C - Pair the Current Schema with a Required ARE Contract Validator

If full cross-reference and range semantics are considered too awkward for pure JSON Schema, declare these ARE rules runtime-authoritative and ship a deterministic validator that checks activation-state topology, `scoring_profile` existence/default behavior, custom profile structural completeness, threshold bounds, and range sanity. This keeps the schema lighter, but it must be explicitly treated as an incomplete front door rather than the whole contract.

#### Comparative Analysis-004

Option A gives the strongest schema boundary, but some ARE obligations are inherently cross-object or mathematical in ways that become awkward in plain JSON Schema. Option C is operationally workable if tooling already exists, yet it leaves too many obvious structural defects undetectable at the first validation boundary. Option B combines the best properties of both approaches by pushing obvious structural failures into schema validation while reserving cross-reference and higher-order checks for a deterministic validator.

#### Recommendation-004

**Endorsed Option:** `Option B`

Option B is the best fit for DDR because ARE is both safety-sensitive and structurally rich. The schema should reject malformed activation-state objects, missing `E5` scoring-profile declarations, and out-of-range numeric values as early as possible. But the framework also needs authoritative checks that JSON Schema does not express cleanly, such as profile-reference resolution and ordered, non-overlapping score-band semantics.

This hybrid split preserves early failure, improves interoperability at the schema boundary, and still acknowledges that some ARE guarantees belong in a deterministic validator rather than in awkward schema contortions.

#### Supporting Citations-004

- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance for conditional requirements such as making `scoring_profile` mandatory when an extension entry is `E5`.
- [JSON Schema Numeric Reference](https://json-schema.org/understanding-json-schema/reference/numeric): Official guidance for enforcing `minimum` and `maximum` bounds on numeric thresholds and range endpoints.
- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance for closing object shapes so activation-state and profile structures cannot drift into arbitrary maps.

#### Notes-004

- Confirmed from the compiled audits with multiple direct schema validation probes.
- The current custom-profile slot is under-typed enough that it behaves more like documentation than an authoritative profile definition; whichever option is chosen should close that gap explicitly.
- If ISSUE-001 is resolved by explicit profiles, ensure `extension_system`, `extension_catalog`, and `are_scoring_profiles` remain part of the required authoritative surface.

---

### ISSUE-005: Normalize Express Mode UNBUNDLE Operation Names

**Status:** `RESOLVED` | **Severity:** `MODERATE` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `Express Mode, Operations, ISL scaffold` | **Spec Section:** `§4, §7, ISL-8.1`

> Resolution (2026-03-28): Option A - Made `UNBUNDLE_EXECUTE` the sole commit-phase token across the live Express Mode surface.

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

#### Resolution-005: Option C - Separate Public Operation from Commit Phase

Keep `UNBUNDLE` as the canonical public operation name, but model `SCAN` and `EXECUTE` as explicit phases beneath that operation rather than as competing top-level operation names. The operations table would expose `UNBUNDLE` plus phase metadata, while lifecycle and scaffold surfaces would refer to `phase: scan|execute` or equivalent. This is conceptually clean, but it broadens the narrow naming fix into a wider operation-taxonomy redesign.

#### Comparative Analysis-005

Option A is the narrowest direct repair and already matches most of the existing prose and scaffold surface. Option B is equally small in scope, but it removes the explicit phase symmetry that the rest of the spec increasingly relies on. Option C gives the cleanest conceptual model, yet it is better understood as a subset of the broader operation-taxonomy cleanup tracked in ISSUE-009 rather than as a narrow rename.

#### Recommendation-005

**Endorsed Option:** `Option A`

Option A is the best fit for this issue because it resolves the actual naming drift with the least ambiguity and the least interpretive work. The current prose, determinism rules, and scaffold already distinguish scan from commit explicitly, so making `UNBUNDLE_EXECUTE` canonical everywhere harmonizes the existing direction of the specification instead of reversing it.

#### Supporting Citations-005

- [JSON Schema Enumerated Values](https://json-schema.org/understanding-json-schema/reference/enum): A fixed canonical operation vocabulary is easiest to validate when one token is authoritative for one behavior.
- [State Chart XML (SCXML)](https://www.w3.org/TR/scxml/): The W3C state-machine model supports explicit phase-like transitions and reinforces the value of unambiguous operation or event naming.

#### Notes-005

- Confirmed from Audit 1 by aligning the Express Mode prose, operations table, and ISL scaffold.
- ISSUE-009 remains the broader taxonomy problem; if ISSUE-009 adopts explicit operation/phase separation, this narrow naming conflict may be resolved within that larger cleanup.

---

### ISSUE-006: Type Remaining Normative Rule Identifiers

**Status:** `RESOLVED` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `DAG invariants, tier rules, extension rules` | **Spec Section:** `§3.5, §5, §9`

> Resolution (2026-03-28): Option B - Centralized invariant, atomic-rule, citation-rule, and extension-rule identifier typing in reusable schema definitions.

#### Problem Statement-006

Several rule-bearing schema objects still accept arbitrary identifier strings even though sibling rule families already use typed patterns. This leaves key normative identifiers structurally looser than the rest of the contract.

#### Evidence & Justification-006

- `ddr_node_schema_v6.2.yaml:595-603` defines `DagInvariant.id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:649-655` defines `AtomicInclusionRule.rule_id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:676-683` defines `AtomicExclusionRule.rule_id` only as `type: string`.
- `ddr_node_schema_v6.2.yaml:919-926` defines `ExtensionRule.rule_id` only as `type: string`, even though `CitationRule.rule_id` and `ExtensionIntegrationRule.rule_id` are pattern-typed elsewhere in the same schema family.
- Direct `jsonschema` validation probes accepted `dag_invariants: [{id: "tier-skip", statement: "bad id still passes"}]`, malformed `atomic_inclusion_rules[].rule_id` values such as `!!invalid`, malformed `atomic_exclusion_rules[].rule_id` values such as `not-a-rule`, and malformed extension rule IDs such as `wrongprefix-1`.

#### Impact Assessment-006

Malformed or inconsistent rule identifiers can enter authoritative documents without early rejection. That weakens programmatic cross-referencing, automated filtering, and the reliability of any tooling that expects IDs like `INV-*`, tier-rule IDs, or `ARE-R*` style labels to be structurally well-formed.

#### Resolution-006: Option A - Add Pattern Constraints Per Rule Family

Add explicit regex patterns for each currently untyped rule-ID family, such as `^INV-[0-9]+$` for `DagInvariant.id`, a permissive but structured pattern for atomic rule families that preserves bridge and suffix forms such as `GPCL-FCL-BR1` and `CL-R9-imposed`, and either a unified `^[A-Z]{2,3}-R[0-9]+$` pattern or per-extension prefixes for extension rules. This is the lowest-blast-radius fix and aligns these families with the stricter rule-ID typing already used elsewhere.

#### Resolution-006: Option B - Centralize Rule-ID Definitions

Create reusable `$defs` for each rule-ID family and reference them wherever those IDs appear. This is a larger cleanup, but it reduces drift, keeps rule-ID logic in one place, and makes future additions or alias handling easier to maintain.

#### Resolution-006: Option C - Add a Canonical Rule Registry

Introduce a machine-readable rule registry in the authoritative system-definition file and validate rule references against that registry at runtime, using regex patterns only as secondary hygiene. This would make the registry the single source of truth for legal IDs and descriptions, but it is a materially larger contract change than tightening the existing schema fields.

#### Comparative Analysis-006

Option A closes the defect quickly, but it risks scattering identifier logic across multiple field definitions. Option B keeps schema-driven enforcement while consolidating the shared rule-ID logic into reusable building blocks. Option C offers the strongest semantic authority, yet it requires a larger change in how rule identity is modeled and validated across the framework.

#### Recommendation-006

**Endorsed Option:** `Option B`

Option B best balances rigor and maintainability. The DDR framework already relies on recurring rule-ID families, and centralizing them in `$defs` makes the schema easier to audit, easier to evolve, and less likely to drift as more rules or aliases are introduced in later versions.

It also preserves the schema as the first-line authority for syntactic rule identity instead of offloading that concern into a separate runtime registry.

#### Supporting Citations-006

- [JSON Schema Structuring](https://json-schema.org/understanding-json-schema/structuring): Official guidance that reusable subschemas in `$defs` reduce duplication and improve maintainability.
- [JSON Schema Regular Expressions](https://json-schema.org/understanding-json-schema/reference/regular_expressions): Official guidance for expressing identifier-family constraints with `pattern` and `patternProperties`.

#### Notes-006

- Confirmed from the compiled audits and direct schema probes.
- Operation-name typing is intentionally handled by ISSUE-009 rather than being folded into this rule-ID issue.
- ISSUE-007 becomes easier to resolve cleanly if identifier families are centralized here first.

---

### ISSUE-007: Align the ICL Tier-Skip Error Code with `INV-2`

**Status:** `RESOLVED` | **Severity:** `MINOR` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `ICL-6.1, DAG invariants` | **Spec Section:** `ICL-6.1, §3.5`

> Resolution (2026-03-28): Option A - Replaced the undocumented `INV-TIER-SKIP` alias in `ICL-6.1` with the canonical invariant ID `INV-2`.

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

#### Resolution-007: Option C - Separate Canonical IDs from Display Labels

Keep `INV-2` as the only canonical rule ID, but add a distinct human-facing `display_label` or `error_label` field in validator outputs for surfaces that want a mnemonic such as `TIER_SKIP`. This preserves friendly messaging without letting aliases compete with normative identifiers.

#### Comparative Analysis-007

Option A resolves the ambiguity with the smallest change and no new data model surface. Option B preserves dual naming, but it introduces alias-maintenance overhead for a single known mismatch. Option C is cleaner than a raw alias map if the framework eventually wants user-facing labels broadly, yet it is more machinery than this isolated mismatch currently justifies.

#### Recommendation-007

**Endorsed Option:** `Option A`

Option A is the best fit because the existing defect is simple: one authoritative rule has two names. Using the canonical invariant identifier directly removes unnecessary translation logic and keeps the error surface aligned with the rest of the normative rule system.

#### Supporting Citations-007

- [JSON Schema Enumerated Values](https://json-schema.org/understanding-json-schema/reference/enum): Canonical machine-readable identifiers are easiest to validate and normalize when one value is authoritative for one concept.
- [JSON Schema Regular Expressions](https://json-schema.org/understanding-json-schema/reference/regular_expressions): Identifier-format enforcement is simpler and more reliable when a single canonical rule-family format is preferred over ad hoc aliases.

#### Notes-007

- Confirmed from Audit 3.
- If ISSUE-006 centralizes rule-ID typing or alias definitions, resolve this mismatch against that same authority rather than adding a one-off exception.

---

### ISSUE-008: Machine-Close Active-Tier Topology Consistency

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All files (root topology, node set)` | **Spec Section:** `§3.5, Schema Root`

> Resolution (2026-03-28): Option A - Closed `active_tiers` to canonical topology variants and made representative active-tier coverage normative for system-definition artifacts.

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

#### Resolution-008: Option C - Derive the Active Topology from Nodes

For system-definition files, derive the authoritative active-tier topology directly from the tier-representative node set and treat `active_tiers` as generated or documentary. Project-instance validators would reconstruct the active tier set from nodes and reject mismatches. This removes one authored source of drift, but it weakens explicitness and forces more work onto every consumer.

#### Comparative Analysis-008

Option A closes the main defect while preserving the current model and adding deterministic validation where pure schema expression is insufficient. Option B gives the cleanest long-term data model, but it is materially more invasive. Option C removes one duplicated declaration, yet it makes simple consumers infer too much from the node set and undercuts the clarity of having an explicit topology declaration.

#### Recommendation-008

**Endorsed Option:** `Option A`

Option A is the strongest practical fix for v6.2 because it hardens the current contract instead of replacing it. Canonical ordering can be closed at the schema layer, while node-tier membership and representative-coverage checks can be enforced deterministically by validation tooling that already needs graph awareness.

This keeps the topology declaration explicit while ensuring it actually governs the instantiated graph.

#### Supporting Citations-008

- [JSON Schema Array Reference](https://json-schema.org/understanding-json-schema/reference/array): Official guidance for array-level constraints that support canonical member and ordering policies.
- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance for applying stronger topology requirements to profile-specific documents such as system-definition files.

#### Notes-008

- Complements ISSUE-002 rather than replacing it: ISSUE-002 fixes mandatory tier presence only.
- If ISSUE-001 is resolved via explicit document profiles, the same mechanism can carry this topology closure more cleanly.

---

### ISSUE-009: Close the Operation Identifier Surface Machine-Readably

**Status:** `RESOLVED` | **Severity:** `MAJOR` | **Type:** `LOGICAL_CONFLICT`
**Tiers Affected:** `Operations, lifecycle authority, ISL scaffold` | **Spec Section:** `§7, §3.8, SAL-5.1, ICL-6.1`

> Resolution (2026-03-28): Option A - Split canonical operation identity from phase, propagation side-effects, and prerequisite chaining in the v6.3 contract.

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

#### Resolution-009: Option C - Introduce a Canonical Operations Registry

Define a single operations registry object that assigns each token an `operation_id`, `kind` (canonical, phase, composite, alias), and normalization target, then reference registry IDs from the operations table, lifecycle rules, and scaffold guidance. This gives one explicit normalization authority, but it adds an additional registry layer rather than simplifying the current model directly.

#### Comparative Analysis-009

Option A repairs the model by separating what an operation is from how it participates in lifecycle execution. Option B keeps more compatibility at the cost of continuing to normalize multiple overlapping string dialects. Option C provides the strongest central catalog, but it is a heavier data-model addition than simply decomposing the current conflated fields into canonical operation plus explicit phase or effect metadata.

#### Recommendation-009

**Endorsed Option:** `Option A`

Option A most directly restores determinism because it removes the core ambiguity instead of normalizing around it. A closed public operation enum plus explicit phase or effect fields makes it possible for validators and tooling to compare like with like rather than guessing whether a token is an operation, a subphase, or a composite alias.

That decomposition also integrates cleanly with ISSUE-005, which is really one narrow manifestation of this broader taxonomy problem.

#### Supporting Citations-009

- [State Chart XML (SCXML)](https://www.w3.org/TR/scxml/): The W3C state-machine model distinguishes explicit transitions and events, which supports separating canonical operation identity from lifecycle subphase semantics.
- [JSON Schema Enumerated Values](https://json-schema.org/understanding-json-schema/reference/enum): Official guidance for closing the canonical operation namespace once operation identity is separated from phase or side-effect metadata.

#### Notes-009

- ISSUE-005 should remain narrow and continue to track the specific `UNBUNDLE` versus `UNBUNDLE_EXECUTE` conflict.
- If Option A is adopted, ISSUE-005 can likely be resolved as part of this broader cleanup.

---

### ISSUE-010: Lock Express Mode Group Compositions Structurally

**Status:** `RESOLVED` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Express Mode` | **Spec Section:** `§4`

> Resolution (2026-03-28): Option A - Bound each canonical Express Mode group ID to its fixed tier composition and required the full four-group set.

#### Problem Statement-010

The specification defines a fixed 4-group Express Mode partition, but the schema does not enforce those group compositions. Group IDs are typed, yet the constituent `tiers` arrays remain effectively open.

#### Evidence & Justification-010

- `ddr_system_v6.2.yaml:353-370` defines the canonical Express Mode groups as `G1 = [XPD, SIL, GPCL]`, `G2 = [FCL, CL]`, `G3 = [SAL, ICL]`, and `G4 = [CDL, ISL]`.
- `ddr_node_schema_v6.2.yaml:229-239` models `express_mode.groups` only as an array of `ExpressModeGroup` items, with no machine-readable rule that all four canonical groups appear exactly once.
- `ddr_node_schema_v6.2.yaml:632-644` constrains `group_id` to `G1|G2|G3|G4`, but `tiers` remains only an unconstrained array of strings.
- A direct `jsonschema` validation probe accepted `group_id: G1` with `tiers: [ISL]` and also accepted a malformed `G1` group with the canonical members partially missing.

#### Impact Assessment-010

A document can claim DDR v6.2 Express Mode while redefining the actual group partition. That destabilizes `UNBUNDLE` semantics, group-to-tier allocation logic, and any implementation that assumes the fixed four-group mapping described by the authoritative specification.

#### Resolution-010: Option A - Encode Canonical Group Definitions in the Schema

Constrain `express_mode.groups` so each canonical `group_id` has a fixed `tiers` array and appears exactly once. This is the smallest repair and makes the published G1-G4 partition machine-authoritative.

#### Resolution-010: Option B - Remove Group Definitions from Authored Documents

Treat Express Mode grouping as version-defined system metadata rather than authored content. Documents would declare Express Mode availability, but G1-G4 compositions would be derived from DDR version and therefore not restatable or drift-prone at the document level.

#### Resolution-010: Option C - Replace the Groups Array with a Fixed-Key Object

Replace `express_mode.groups` with a closed object keyed by `G1`, `G2`, `G3`, and `G4`, each with const-bound tier members and label metadata. This is easier to validate than an array of loosely ordered entries, but it changes the authored data shape and requires migration of existing documents.

#### Comparative Analysis-010

Option A preserves the current authored shape and closes the defect directly. Option B is conceptually the cleanest because it removes authored duplication, but it relocates authority and requires broader design changes around how Express Mode metadata is surfaced. Option C provides very strong machine closure for authored content, yet it introduces an avoidable migration when the current array shape can be constrained sufficiently.

#### Recommendation-010

**Endorsed Option:** `Option A`

Option A is the best repair for v6.2 because it gives the framework structural closure without changing the authored model. The current `groups` array can be made authoritative by tying each `group_id` to one canonical member list and by requiring all four groups exactly once.

#### Supporting Citations-010

- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance for closing authored object structures so unexpected shapes are rejected rather than tolerated.
- [JSON Schema Enumerated Values](https://json-schema.org/understanding-json-schema/reference/enum): Official guidance for constraining fixed identifiers such as the canonical `G1` through `G4` group set.

#### Notes-010

- Independent of ISSUE-005: this is a structural-definition defect, not an operation-name defect.
- If express-mode documents continue to carry a top-level `express_mode` block, this group contract must be machine-closed there as well.

---

### ISSUE-011: Enforce Top-Level Express Mode Contract for Express Projects

**Status:** `RESOLVED` | **Severity:** `MODERATE` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `Project instances (express mode)` | **Spec Section:** `§4, Express Mode`

> Resolution (2026-03-28): Option B - Required the full top-level `express_mode` authority block through the explicit express document profile.

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

#### Resolution-011: Option C - Require `express_mode` Whenever Nodes Use Express Grouping

Add a cross-root conditional that requires the top-level `express_mode` block whenever any node includes `express_mode_group`, and forbid `express_mode_group` when the block is absent. This catches malformed files even when `project.mode` is missing or incorrect, but it still leaves document intent less explicit than a real profile contract.

#### Comparative Analysis-011

Option A directly fixes the exact defect and is easy to implement. Option B produces the cleanest architecture if document profiles are already being formalized, because it removes another special-case root conditional and makes express-mode authority explicit by profile. Option C hardens observed usage, but it still makes intent partly inferential and would be a weaker foundation than an explicit profile model.

#### Recommendation-011

**Endorsed Option:** `Option B`

Option B best aligns this issue with the broader root-contract direction needed by ISSUE-001. Express Mode is not just a node annotation detail; it is a document-level consumption profile with its own authoritative rules. Encoding that through an explicit profile model keeps the contract coherent and avoids proliferating one-off root conditionals.

#### Supporting Citations-011

- [JSON Schema Conditional Subschemas](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance for expressing profile-specific required sections when a document declares a specific operating mode.
- [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance for closing required document-level sections once the active profile is known.

#### Notes-011

- Independent of ISSUE-005, but it shares the same operational surface.
- If ISSUE-001 is resolved via explicit document profiles, this gap should be closed there rather than by stacking another special-case conditional onto the current root schema.

---

## RESOLUTION WORKFLOW

> **AGENT INSTRUCTION:** When a resolution is executed for any issue, follow this workflow
> exactly. Do not mark an issue `RESOLVED` until all steps are confirmed.

```plaintext
1. IDENTIFY the issue ID and selected Resolution Option (A/B/C)
2. DRAFT and APPLY the specific changes to .agent\assets\proposals\active\v6.3\ddr_system_v6.3.yaml and .agent\assets\proposals\active\v6.3\ddr_node_schema_v6.3.yaml and any directly affected associated artifacts
3. VERIFY the draft changes do not introduce new issues (check cross-references in Notes fields)
4. UPDATE the associated Issue Report immediately:
   - Set status: RESOLVED
   - Set updated: [date]
   - Set resolved: [date]
   - Replace the pending implementation note with an implemented-change summary and validation evidence
5. UPDATE the issue entry in this tracker immediately:
   - Set status: RESOLVED
   - Record resolution: "Option [A|B|C]: [one-line summary]"
6. UPDATE the ISSUE REGISTRY table
7. UPDATE document header metadata (`open_issues`, `resolved_issues`, `last_modified`)
8. VALIDATE the updated Issue Report and Issues Tracker before continuing to the next OPEN issue
```

---

## APPENDIX: CROSS-ISSUE DEPENDENCY MAP

> Issues that share a dependency - resolving one may affect the other.

| Issue | Depends On | Nature of Dependency |
| --- | --- | --- |
| ISSUE-001 | (none) | Root-profile defect; independently actionable. |
| ISSUE-002 | (none) | Mandatory-tier presence defect on the shared root contract; independently actionable. |
| ISSUE-003 | (none) | Lifecycle machine-completeness defect; independently actionable. |
| ISSUE-004 | ISSUE-001 | If system-definition profiles are formalized, ensure the ARE authority sections remain required within that profile. |
| ISSUE-005 | ISSUE-009 | The narrow `UNBUNDLE` naming conflict is one manifestation of the broader operation-identifier taxonomy defect. |
| ISSUE-006 | (none) | Identifier-typing cleanup; independently actionable. |
| ISSUE-007 | ISSUE-006 | If identifier families are centralized, align the ICL alias against that same rule-ID authority. |
| ISSUE-008 | ISSUE-002 | Broader topology-closure companion; ISSUE-002 fixes mandatory tier presence only. |
| ISSUE-009 | (none) | Operation-taxonomy defect; independently actionable. |
| ISSUE-010 | (none) | Express Mode structural-definition defect; independently actionable. |
| ISSUE-011 | ISSUE-001 | If explicit document profiles are introduced, the express-mode profile should require the full `express_mode` authority block. |

---

*DDR System v6.2 Issues Tracker — IT-1.1*
*11 issues identified | 11 resolved | Last updated: 2026-03-28*
*Optimized for Google Antigravity >=1.18 · Gemini 3.1 Pro · Progressive Disclosure Context Architecture*

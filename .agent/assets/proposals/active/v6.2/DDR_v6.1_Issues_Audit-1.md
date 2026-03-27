### Evaluation of Existing Issue Resolutions

When evaluating these options, the maximally optimized strategy must prioritize strict type safety and predictable deserialization. Schemas that rely on scattered `if/then` conditionals create massive overhead when mapped into object-oriented models, Abstract Syntax Trees (ASTs), or desktop UI data models. Discriminated unions (explicit variants) are almost always superior for deterministic system design.

| Issue ID & Focus | Recommended Optimized Strategy | Architectural Rationale |
| :--- | :--- | :--- |
| **ISSUE-001**<br>*(Lifecycle required)* | **Option A:** Make `lifecycle` conditional based on document profile. | Demanding `lifecycle` in every project-instance file bloats the graph. Option B forces the system definition to leak into project instances. Option A preserves the lean node-graph intent. |
| **ISSUE-002**<br>*(Undefined states)* | **Option A:** Constrain to typed references. | Permitting arbitrary strings or templated variables like `"{prior_status}"` defeats the purpose of an enumerable state machine. The schema must use a strict `StatusEnum`. |
| **ISSUE-003**<br>*(`extends` in parent\_ids)* | **Option B:** Split Core and Global Edge Enums. | Removing `extends` from the global vocabulary loses semantic value. Splitting into `CoreCitationEdgeType` and `ExtensionEdgeType` provides absolute type safety for downstream parsers. |
| **ISSUE-004**<br>*(`derivation_mode` rule)* | **Option B:** Split citation variants. | Using `if/then` constraints in JSON Schema (Option A) creates ambiguous types during codegen. Defining explicit `DerivesCitation` and `NonDerivesCitation` classes ensures downstream parsing tools never encounter unexpected fields. |
| **ISSUE-005**<br>*(Extension shadow keys)* | **Option A:** Explicitly block reserved suffixes. | AX-6 demands Declarative Integrity. If an extension can publish `HRE::content`, it creates a shadowing risk that compromises the core node schema. Option A is non-negotiable. |
| **ISSUE-006**<br>*(`prior_status` scope)* | **Option B:** Split Transient and Settled Node Variants. | If `prior_status` only exists during a supersede event, baking it into the base `DdrNode` pollutes the data model. A distinct `SupersedePendingNode` variant guarantees valid rollback states at the type level. |
| **ISSUE-007**<br>*(Lifecycle openness)* | **Option A:** Close the existing object. | A deterministic system cannot tolerate rogue keys in its core authority blocks. `additionalProperties: false` must be enforced globally. |
| **ISSUE-008**<br>*(`constraint_origin` scope)* | **Option B:** Introduce Tier-Specific Variants. | Adding `constraint_origin` to the base `DdrNode` breaks tier encapsulation. Defining a specific `CLNode` schema ensures non-CL tiers cannot carry CL-specific data. |
| **ISSUE-009**<br>*(Express Mode grouping)* | **Option B:** Split Root Profiles. | Similar to ISSUE-001, separating `FullProject` and `ExpressProject` at the schema root ensures that validation rules are contextual and tightly bound to the mode being consumed. |
| **ISSUE-010**<br>*(Lifecycle guard IDs)* | **Option A:** Constrain to the versioned guard set. | A regex pattern (Option B) allows phantom guards like `gc-999` to pass structural validation. Hardcoding the exact enum (`gc-001` through `gc-009`) guarantees referential integrity. |

-----

### New Issues of Concern (Require Dedicated Reports)

The current tracker misses two critical structural vulnerabilities in the v6.1 schema that compromise the DAG's determinism.

#### ISSUE-011: Node ID Prefix and Tier Enum Disconnection

**Severity:** `CRITICAL` | **Type:** `SCHEMA_DEFECT`
**Tiers Affected:** `All` | **Spec Section:** `§3.1, §3.6`

**Problem Statement:**
The `DdrNode` schema defines `id` with the regex `^(XPD-0\.[0-9]+|[A-Z]{2,5}-[0-9]+\.[0-9]+)$` and `tier` as a separate enum. There is no schema-level validation enforcing that the alphabetic prefix of the `id` matches the declared `tier`.

**Impact Assessment:**
A node can be structurally valid with `tier: FCL` but `id: SAL-5.1`. This semantic schizophrenia completely breaks `VERIFY` traversal logic, edge-type validation, and any visualization tools mapping the DAG. Downstream systems parsing the AST will encounter conflicting routing instructions.

**Proposed Resolution (Option B Alignment):**
If `DdrNode` is split into Tier-Specific Variants (as recommended for ISSUE-008), each tier variant can strictly bind its ID regex. For example, the `FCLNode` variant would enforce the `^FCL-[0-9]+\.[0-9]+$` pattern, guaranteeing prefix-to-tier alignment at the type level.

-----

#### ISSUE-012: Rollback Target Type Conflict in Lifecycle Machine

**Severity:** `MAJOR` | **Type:** `LIFECYCLE_GAP`
**Tiers Affected:** `All` | **Spec Section:** `§3.8`

**Problem Statement:**
If ISSUE-002 Option A is implemented (restricting `from` and `to` lifecycle targets to literal `StatusEnum` values), the `SUPERSEDE_ROLLBACK` transition `to: "{prior_status}"` becomes a type violation. The machine schema cannot validate a templated string against a strict Enum array.

**Impact Assessment:**
Attempting to harden the lifecycle transitions will immediately break the `SUPERSEDE` rollback mechanism. The schema will reject the `{prior_status}` token, leaving the rollback state undefined in the strict type system.

**Proposed Resolution:**
Instead of a templated token, the lifecycle schema must either support a defined `dynamic_target` field specifically mapped to `prior_status`, or the transitions must be explicitly expanded. The explicit expansion would define three discrete rollback paths: `SUPERSEDE_PENDING` to `ACTIVE`, `SUPERSEDE_PENDING` to `DEPRECATED`, and `SUPERSEDE_PENDING` to `DIRTY`, conditionally gated by the `prior_status` value.

-----

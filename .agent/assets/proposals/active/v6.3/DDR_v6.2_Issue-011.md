---
document:
  id:              DDR_v6.2_Issue-011
  title:           "Resolution Report for ISSUE-011: Enforce Top-Level Express Mode Contract for Express Projects"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  resolved:        "2026-03-28"
  status:          "RESOLVED"
  severity:        "MODERATE"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-011"

### Agent Context

```yaml
id:          ISSUE-011
status:      RESOLVED
severity:    MODERATE
type:        SCHEMA_DEFECT
tier_refs:   ["Project instances (express mode)"]
section_ref: "\u00a74, Express Mode"
rule_refs:   []
updated:     2026-03-28
resolved:    2026-03-28
```

### 1. Validation Audit of ISSUE-011

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:55-68`, `.agent/assets/proposals/active/v6.2/ddr_node_schema_v6.2.yaml:229-242`, and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:353-391` was conducted to investigate the claims of "ISSUE-011: Enforce Top-Level Express Mode Contract for Express Projects".

The schema already requires `express_mode_group` on nodes when `project.mode` is `express`, but it does not require the top-level `express_mode` object that carries the governing UNBUNDLE contract. DDR therefore enforces the per-node marker while leaving the document-level Express Mode authority optional.

**Findings:**

1. **Express Mode Can Be Declared Without Its Governing Contract:** The root schema does not require the top-level `express_mode` block even when express consumption is declared.
2. **Node-Level Markers Are Stronger Than Document-Level Authority:** The schema currently cares more about per-node grouping labels than about the root contract they rely on.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-011

The resolution goal is to ensure that any document declaring Express Mode also carries the full root-level authority needed to make UNBUNDLE behavior deterministic.

#### Option A: Add Explicit Conditional Requirement

Add a root `allOf` clause so `project.mode: express` requires the top-level `express_mode` object, and require at least `groups`, `unbundle_determinism_rule`, and `deferred_fragment_handling` inside that block. This is the minimal targeted repair.

* **Supporting Insights:** A direct conditional requirement fixes the immediate gap quickly, but it adds another special case to an already weak root contract.
* **Citations:** [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object)

#### Option B: Leverage Document Profiles

Adopt `document_profile` or another profile-aware root contract, then define an express-capable profile whose required sections include the full `express_mode` authority block by construction. This is the cleaner long-term architecture, especially if ISSUE-001 also moves toward explicit profiles.

* **Supporting Insights:** A profile-aware root contract treats Express Mode as a document-level operating mode rather than as a one-off conditional.
* **Citations:** [JSON Schema conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals), [JSON Schema object reference](https://json-schema.org/understanding-json-schema/reference/object)

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Architectural Coherence:** Option B aligns the issue with broader profile-based root repair; Option A is the smaller local patch.
2. **Profile Explicitness:** Option B makes Express Mode first-class at the document root; Option A still treats it as a conditional wrinkle.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option B (Recommended Strategy)**.

The updated tracker now favors the profile-based direction because this issue is structurally the same kind of root-contract weakness as ISSUE-001. Express Mode is a document-level operating mode with its own authoritative rules.

**Option B** is recommended because:

* **Aligns with the Broader Root Fix:** The same explicit-profile mechanism can close both root gaps coherently.
* **Makes Operating Mode Explicit:** Validators know up front that the full Express Mode authority block is required.
* **Avoids Stacking Special Cases:** The schema gains one clearer architectural branch instead of another isolated conditional.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml`.

The v6.3 schema now expresses Express Mode as part of the explicit `document_profile` model. `project_instance_express` requires the top-level `express_mode` authority block with `groups`, `unbundle_determinism_rule`, and `deferred_fragment_handling`, and node-level `express_mode_group` enforcement now hangs from that profile while `project.mode` is retained only as a consistency check.

Validation evidence:
- `.venv\Scripts\python.exe` YAML-parse check succeeded for both v6.3 YAML artifacts.
- Draft 2020-12 validation of `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` against `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` succeeded with the profile-based express-mode root contract.

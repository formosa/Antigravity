---
document:
  id:              DDR_v6.2_Issue-007
  title:           "Resolution Report for ISSUE-007: Align the ICL Tier-Skip Error Code with `INV-2`"
  format_version:  "IT-1.1"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-28"
  updated:         "2026-03-28"
  resolved:        "2026-03-28"
  status:          "RESOLVED"
  severity:        "MINOR"
  type:            "LOGICAL_CONFLICT"
---

## Optimized Resolution Strategy for "ISSUE-007"

### Agent Context

```yaml
id:          ISSUE-007
status:      RESOLVED
severity:    MINOR
type:        LOGICAL_CONFLICT
tier_refs:   ["ICL-6.1", "DAG invariants"]
section_ref: "ICL-6.1, \u00a73.5"
rule_refs:   ["INV-2", "INV-TIER-SKIP"]
updated:     2026-03-28
resolved:    2026-03-28
```

### 1. Validation Audit of ISSUE-007

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:257-262` and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2386-2388` was conducted to investigate the claims of "ISSUE-007: Align the ICL Tier-Skip Error Code with `INV-2`".

The canonical DAG invariant list defines tier skipping as `INV-2`, but the ICL error-code surface names the same condition `INV-TIER-SKIP`. No alias table or translation note explains the relationship between the two strings.

**Findings:**

1. **One Invariant Has Two Names:** The same tier-skipping rule is exposed under two identifiers without an explicit alias relationship.
2. **Cross-Reference Is Needlessly Frictional:** Validators, tests, and docs must normalize the mismatch themselves.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-007

The resolution goal is to restore one clear naming relationship between the ICL contract and the canonical invariant list.

#### Option A: Use `INV-2` in the ICL Error Contract

Replace `INV-TIER-SKIP` with `INV-2` in the `ICL-6.1` error-code list so the contract points directly at the authoritative invariant identifier already defined in `dag_invariants`. This is the smallest fix and removes ambiguity immediately.

* **Supporting Insights:** Pointing the ICL surface directly at `INV-2` collapses the ambiguity immediately.
* **Citations:** No authoritative external reference identified for this specific claim.

#### Option B: Add an Explicit Alias Map

If the project wants human-readable mnemonics in error payloads, add a small alias table that maps mnemonic labels like `INV-TIER-SKIP` to canonical IDs like `INV-2`. This preserves the friendlier surface while making the translation explicit and machine-readable.

* **Supporting Insights:** An alias map is only worthwhile if DDR intends to support mnemonic labels more broadly.
* **Citations:** No authoritative external reference identified for this specific claim.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Canonicality:** Option A keeps one identifier authoritative; Option B preserves two names and adds translation machinery.
2. **Scope:** Option A is a narrow content fix; Option B introduces a new normalization surface.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The mismatch is small, localized, and currently undocumented. The cleanest repair is therefore to use the already authoritative invariant ID instead of adding alias infrastructure.

**Option A** is recommended because:

* **Restores One Canonical Identifier:** All rule references can point directly at the invariant list.
* **Lowest Blast Radius:** A naming correction is easier to validate than a new alias mechanism.
* **Avoids One-Off Alias Debt:** Broader mnemonic labeling can be introduced systematically later if needed.

### 4. Implementation Note

Implemented in `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml`.

The v6.3 system file now replaces `INV-TIER-SKIP` with the canonical invariant identifier `INV-2` in `ICL-6.1` and updates the surrounding version-lock text to the v6.3 contract. The ICL error surface now points directly at the invariant defined in `dag_invariants` instead of relying on an undocumented alias.

Validation evidence:
- `.venv\Scripts\python.exe` YAML-parse check succeeded for both v6.3 YAML artifacts.
- Draft 2020-12 validation of `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` against `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml` succeeded after the ICL rule-reference alignment.

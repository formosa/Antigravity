---
document:
  id:              DDR_v6.2_Issue-007
  title:           "Resolution Report for ISSUE-007: Align the ICL Tier-Skip Error Code with `INV-2`"
  format_version:  "IT-1.0"
  target_platform: "Google Antigravity >=1.18"
  target_model:    "Gemini 3.1 Pro"
  subject:         "DDR System v6.2"
  created:         "2026-03-27"
  updated:         "2026-03-27"
  status:          "OPEN"
  severity:        "MINOR"
  type:            "LOGICAL_CONFLICT"
---

## Optimized Resolution Strategy for "ISSUE-007"

### Agent Context

```yaml
id:          ISSUE-007
status:      OPEN
severity:    MINOR
type:        LOGICAL_CONFLICT
tier_refs:   ["ICL-6.1", "DAG invariants"]
section_ref: "ICL-6.1, §3.5"
rule_refs:   ["INV-2", "INV-TIER-SKIP"]
updated:     2026-03-27
```

### 1. Validation Audit of ISSUE-007

An evaluation of `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:257-262` and `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2386-2388` was conducted to investigate the claims of "ISSUE-007: Align the ICL Tier-Skip Error Code with `INV-2`."

The canonical DAG invariant list defines the no-tier-skipping rule as `INV-2` at `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:257-262`. The ICL error-code set later names the same condition `INV-TIER-SKIP` at `.agent/assets/proposals/active/v6.2/ddr_system_v6.2.yaml:2386-2388`. No nearby alias table or translation note explains whether `INV-TIER-SKIP` is intentional shorthand, a legacy alias, or an accidental mismatch.

**Findings:**

1. **One Invariant Currently Has Two Identifiers:** The same tier-skipping rule is exposed under two different labels without a declared relationship between them.
2. **Programmatic Cross-Reference Becomes Needlessly Frictional:** Validator outputs, tests, and documentation must either normalize the mismatch themselves or risk treating the two labels as separate concepts.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-007

The resolution goal is to restore one clear, machine-understandable naming relationship between the ICL contract and the canonical DAG invariant set.

#### Option A: Use `INV-2` in the ICL Error Contract

Replace `INV-TIER-SKIP` with `INV-2` in the `ICL-6.1` error-code list so the error contract points directly at the already authoritative invariant identifier. This is the smallest fix and removes ambiguity immediately without requiring any new aliasing machinery. It favors canonical consistency over mnemonic readability.

* **Supporting Insights:** The DAG invariant list is already the place where the rule is normatively defined. Reusing that identifier in the ICL surface keeps all references anchored to the same authority.
* **Citations:** No authoritative external reference identified for this specific claim.

#### Option B: Add an Explicit Alias Map

If the project wants human-readable mnemonics in operational outputs, add a small alias table that maps labels like `INV-TIER-SKIP` to canonical IDs like `INV-2`. This preserves the friendlier mnemonic surface while making the translation explicit and machine-readable. The tradeoff is that it introduces new alias infrastructure for what is currently a single isolated mismatch.

* **Supporting Insights:** An alias map is more flexible if the project intends to expose both canonical IDs and human-facing mnemonics across multiple surfaces. Without a broader alias strategy, though, it risks being a one-off mechanism for one inconsistency.
* **Citations:** No authoritative external reference identified for this specific claim.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific cascading tradeoffs relative to DDR System v6.2 invariants:

1. **Canonicality vs Translation Layer:** Option A collapses the mismatch to one identifier, while Option B preserves two names and adds machinery to map between them.
2. **Implementation Scope:** Option A is a narrow contract edit in the ICL error-code list; Option B requires a broader alias surface plus consumer agreement on how aliases are exposed.
3. **Future Flexibility:** Option B leaves room for human-readable mnemonics more generally, but Option A is the cleaner resolution when the current inconsistency is isolated and undocumented.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

The validated mismatch is small and localized, and the canonical DAG invariant identifier already exists. Aligning the ICL surface to `INV-2` resolves the ambiguity immediately and avoids introducing alias infrastructure before the project has decided it needs a generalized alias strategy.

**Option A** is recommended because:

* **Restores One Canonical Identifier:** All rule references can point at the invariant list without translation.
* **Has the Lowest Blast Radius:** A focused naming correction is easier to validate than a new alias mechanism.
* **Avoids One-Off Alias Debt:** If broader aliasing is needed later, it can be introduced systematically rather than as a special exception here.

### 4. Implementation Note

Implementation remains pending. This report documents the validated defect and recommended direction only; it did not apply a repository patch.

---
document:
  id:              DDR_v6.3_Issue-001
  title:           "Resolution Report for ISSUE-001: Require an explicit webhook profile discriminator"
  format_version:  "v6.1"
  target_platform: "Google Antigravity 1.21.9"
  target_model:    "Gemini 3 Pro Preview"
  subject:         "DDR Reference Manual v6.3"
  created:         "2026-04-04"
  updated:         "2026-04-04"
  status:          "OPEN"
  severity:        "CRITICAL"
  type:            "SCHEMA_DEFECT"
---

## Optimized Resolution Strategy for "ISSUE-001"

### Agent Context

```yaml
id:          ISSUE-001
status:      OPEN
severity:    CRITICAL
type:        SCHEMA_DEFECT
tier_refs:   [Schema, Validation]
section_ref: §4.3 Webhook Event Contract
rule_refs:   [SCH-R1, VAL-R2]
updated:     2026-04-04
```

### 1. Validation Audit of ISSUE-001

An evaluation of `ddr/ddr_ref_manual_v6.3.md` and the corresponding webhook event examples was conducted to investigate the claims of "ISSUE-001: Require an explicit webhook profile discriminator."

The audit confirms that the current webhook payload description allows multiple profile-specific properties to coexist without an explicit discriminator that closes the object shape for each profile. That ambiguity weakens downstream validation because a structurally invalid hybrid payload can still look superficially acceptable during manual review.

The strongest local evidence is the mismatch between the profile prose and the absence of a machine-readable field that selects which profile branch is active. Without that discriminator, validators and maintainers must infer intent from optional property combinations instead of a single authoritative switch.

**Findings:**

1. **Ambiguous Branch Selection:** The schema surface does not provide one field that deterministically selects the active webhook profile branch, so payload interpretation depends on loose optional-property combinations.
2. **Weak Structural Closure:** Because the branch is inferred instead of declared, invalid cross-profile mixtures are harder to reject consistently in automated validation and harder to reason about during maintenance.

### 2. Suggested Strategies for Optimal Resolution of ISSUE-001

Two materially different strategies can restore deterministic profile selection while preserving the surrounding webhook contract.

#### Option A: Add an explicit `webhook_profile` discriminator field

Add a required `webhook_profile` field whose enum values map directly to the supported webhook profiles, and drive conditional validation from that discriminator.

* **Supporting Insights:** A discriminator makes the active profile machine-readable at the first decision point, which localizes validation logic and keeps branch selection explicit for both humans and tooling.
* **Citations:** [JSON Schema Conditionals](https://json-schema.org/understanding-json-schema/reference/conditionals): Official guidance on using explicit conditional branches for profile-specific requirements.

#### Option B: Split webhook profiles into separate top-level object contracts

Replace the shared mixed object with separate profile-specific object definitions and require callers to choose the correct contract at the integration boundary.

* **Supporting Insights:** A hard object split maximizes closure strength, but it also increases migration and maintenance overhead because every shared property must now be duplicated or abstracted across multiple contracts.
* **Citations:** [JSON Schema Object Reference](https://json-schema.org/understanding-json-schema/reference/object): Official guidance on closing object contracts with explicit properties and shape constraints.

### 3. Comparative Analysis and Recommended Strategy

#### Comparative Analysis

Each strategy entails specific tradeoffs relative to DDR webhook contract invariants:

1. **Branch Clarity vs. Migration Overhead:** **Option A** restores deterministic branch selection with one additive field, while **Option B** achieves stronger shape isolation at the cost of a broader contract split.
2. **Local Repair vs. Structural Duplication:** **Option A** keeps the common object surface centralized, while **Option B** risks duplicating shared properties and maintenance logic across multiple profile objects.

#### Endorsement and Contextual Justification

The most balanced and minimally disruptive solution is **Option A (Recommended Strategy)**.

Option A is preferred because it restores explicit machine-readable branch selection without forcing an immediate object-family split. It narrows the ambiguity at the exact decision point that validators and maintainers already need, while keeping the migration surface smaller than a full contract separation.

**Option A** is recommended because:

* **Deterministic Validation:** It gives validators one authoritative field to branch on instead of inferring intent from loosely related optional properties.
* **Lower Blast Radius:** It keeps the surrounding object family intact, which reduces migration cost compared with splitting the contract into multiple top-level schemas.
* **Future Flexibility:** It preserves the option to introduce stronger profile-specific closure later if additive conditional validation is no longer sufficient.

### 4. Implementation Note

Implementation remains pending. This canonical example illustrates the report contract only and did not apply a repository patch.

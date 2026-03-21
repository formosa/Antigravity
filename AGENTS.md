# AGENTS.md — DDR System Repository

## Project Identity

This repository contains the DDR System Specification v4.0. The single
authoritative specification file is:

  .agent/assets/proposals/active/ddr_system_v4.0.yaml

The Markdown document is a human-readable reference only:

  .agent/assets/proposals/active/DDR System(Opus_v4).md

All modifications must target the YAML file exclusively. The Markdown document
must never be modified.

Active issue report for the current task:

  .agent/assets/proposals/active/DDR_v4_Issue-013.md

---

## Current Task Scope

Implement the endorsed resolution for ISSUE-013 as described in
`DDR_v4_Issue-013.md`, Section 3 (Endorsement: Option A).

The resolution requires exactly three additive mutations to
`ddr_system_v4.0.yaml`. No other changes are in scope:

1. Append `FCL-R7` to the FCL tier's `atomic_inclusion_rules` block.
2. Append `DDE-R5` to the E7 DDE extension's `rules` block.
3. Update the FCL entry in `compliance_checklist.atomic_rule_validation`
   to reference `FCL-R7`.

---

## Modification Constraints

The following constraints are absolute. Any mutation that violates them is a
hard failure. Do not proceed past the point of a constraint violation; report
the violation and stop.

### MC-1 — Additive Only

No existing rule, field, key, tier, extension entry, axiom, operation, or
lifecycle block may be removed, renamed, or have its statement altered.
This resolution is strictly additive.

### MC-2 — Target File Only

Modify only: `.agent/assets/proposals/active/ddr_system_v4.0.yaml`
No other file may be modified for any reason.

### MC-3 — Rule ID Conventions

- The new FCL inclusion rule must use the ID `FCL-R7`.
- The new DDE rule must use the ID `DDE-R5`.
- Both IDs must follow the existing file convention: `TIER-RN` where N is
  the next sequential integer after the current highest rule in that block.
- These IDs are non-negotiable.

### MC-4 — Atomic Rule Schema

Every atomic rule entry in this file uses exactly the following fields:

- `rule_id` (required)
- `statement` (required, block scalar `>`)
- `violation_consequence` (required, block scalar `>`)
- `verification_mode` (required, value: `structural` or `semantic`)
- `applies_when` (optional, conditional rules only)

No other fields exist on atomic rule entries in this schema. Do not introduce
any field not listed above (e.g., `normative_note`, `rationale`, `note`,
`example`). Any FCL-E2 boundary clarification required for FCL-R7 must be
encoded within the `statement` field itself.

### MC-5 — FCL-R7 Semantic Scope

FCL-R7 mandates logical data entity enumeration: entity names and CRUD
relationships only (created, read, updated, deleted). This is not a data
schema. FCL-E2 prohibits data schemas (structural definitions with field
types, column names, constraints, and table structures). These two rules
address different levels of abstraction and do not conflict. The FCL-R7
statement must make this boundary explicit by excluding field types, column
names, schema constraints, and relational keys from its scope, and must
reference FCL-E2 to make the compatibility machine-readable.

### MC-6 — FCL-R7 Verification Mode

FCL-R7 must carry `verification_mode: semantic`. This is correct and
intentional: determining whether a capability modifies persistent data and
whether the enumerated entities are complete requires human judgment. This
is not a defect.

### MC-7 — DDE `annotates` Field Is Unchanged

The E7 DDE extension `annotates` field currently reads: `[ICL, SAL, FCL]`.
This field must not be modified. DDE retains its FCL annotation capability.
DDE-R5 governs only the *nature* of that annotation (confirmation only;
discovery prohibited). Option B (removing FCL from `annotates`) is not the
endorsed strategy and must not be implemented.

### MC-8 — DDE-R5 Role Definition

DDE-R5 must define DDE's FCL annotation role as confirmation validation:
verifying that entities enumerated under FCL-R7 have corresponding ICL
schema definitions. DDE-R5 must explicitly prohibit discovery-mode FCL
annotations (inferring unstated data entities from capability semantics
when no FCL-R7 enumeration is present). A missing FCL-R7 enumeration is a
Core FCL validation failure, not a DDE discovery trigger.

### MC-9 — No New Structural Elements

Do not introduce new edge types, tier IDs, extension IDs, axioms, advisory
types, or manifest item types. The `UPSTREAM_GAP` advisory type described
in Option B of the issue report must not be introduced.

### MC-10 — YAML Formatting

All new content must match the indentation depth, block scalar style (`>`),
and spacing conventions of its immediate siblings in the file. The output
must be valid YAML that parses without errors.

---

## DDR Invariants — Must Not Be Violated

| Invariant | Requirement for This Task |
|---|---|
| **AX-3 (Determinism)** | FCL-R7 must be mechanically checkable by VALIDATE independent of any Extension. `verification_mode: semantic` satisfies this — VALIDATE emits REVIEW_REQUIRED for semantic rules, which is the correct normative path. |
| **AX-5 (Extensibility)** | FCL completeness for data entities must be verifiable with DDE disabled. FCL-R7 must contain no reference to DDE or any Extension in its statement. |
| **AX-6 (Declarative Integrity)** | Core is self-contained. FCL-R7 must not condition its requirements on any Extension's activation state. |
| **EXT-R2 (Contract Enumeration)** | DDE must enumerate exactly which tiers it reads and annotates. The `annotates` field is the contract declaration. It must remain `[ICL, SAL, FCL]`. |
| **EXT-R5 (Extension Removal)** | Disabling DDE must leave Core CLEAN/DIRTY status unchanged. FCL-R7 ensures this: FCL completeness no longer depends on DDE being active. |

---

## Validation Criteria

Before committing, verify all of the following:

- [ ] FCL-R7 exists in `atomic_inclusion_rules` immediately after FCL-R6.
- [ ] FCL-R7 contains exactly: `rule_id`, `statement`, `violation_consequence`,
      `verification_mode`. No other fields.
- [ ] FCL-R7 `statement` references FCL-E2 and excludes schema-level detail.
- [ ] FCL-R7 `verification_mode` is `semantic`.
- [ ] FCL-R1 through FCL-R6 are byte-for-byte unchanged.
- [ ] FCL-E1, FCL-E2, FCL-E3 are byte-for-byte unchanged.
- [ ] DDE-R5 exists in the E7 rules list immediately after DDE-R4.
- [ ] DDE-R5 contains exactly: `rule_id`, `statement`. No other fields.
- [ ] DDE-R5 `statement` prohibits discovery-mode and permits confirmation-mode.
- [ ] DDE-R1 through DDE-R4 are byte-for-byte unchanged.
- [ ] DDE `annotates` field is unchanged: `[ICL, SAL, FCL]`.
- [ ] `compliance_checklist.atomic_rule_validation` FCL entry references FCL-R7.
- [ ] No other checklist items have been modified.
- [ ] The modified YAML parses without errors.

---

## Commit Message

Use the following commit message exactly:

```
ISSUE-013 Resolution: Add FCL-R7 data entity enumeration rule and DDE-R5 confirmation governance
```

---

## PR Description Requirements

The PR description must include:

1. Root cause statement: backwards validation dependency created by DDE's
   discovery-mode FCL annotation.
2. Resolution: Option A — FCL-R7 additive inclusion rule + DDE-R5 governance.
3. Rationale for Option A over Option B: root cause resolution vs. symptom
   treatment; AX-5 and AX-6 compliance.
4. Enumeration of the three mutations applied, each with its YAML section path.
5. Explicit confirmation that no existing rules were modified or removed.

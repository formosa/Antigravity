# AGENTS.md
# DDR System — Codex Task Instructions
# Scope: Resolution of ISSUE-011 only
# Do not apply these instructions to any other task or issue.

---

## Repository Layout (Relevant Files Only)

The following files are the only artifacts relevant to this task.
Do not read, modify, or reference any other files.

| Role | Path |
|---|---|
| PRIMARY MODIFICATION TARGET | `.agent\assets\proposals\active\ddr_system_v4.0.yaml` |
| SECONDARY MODIFICATION TARGET | `.agent\assets\proposals\active\DDR System(Opus_v4).md` |
| ISSUE REPORT (read-only reference) | `.agent\assets\proposals\active\DDR_v4_Issue-011.md` |

---

## Task Objective

Resolve ISSUE-011 by correcting a single defective entry in the `rule_map`
block of `ddr_system_v4.0.yaml` and synchronizing the corresponding row in
the Appendix B Rule-Level Cross-Reference table of `DDR System(Opus_v4).md`.

No other changes are permitted.

---

## Confirmed Structural Facts (Do Not Re-Derive)

The following facts have been established by prior audit and are authoritative.
Do not contradict them.

1. `system_metadata.status` in `ddr_system_v4.0.yaml` is `Finalized`.

2. The `rule_map` block contains this defective entry:
```yaml
   - from_rule_ids: "ORL-R7"
     to_rule_ids: "GPCL-R10"
     consolidation_status: "1:1"
     notes: "NOTE — Audit C-3: mapping marked TBD in source doc; assigned here pending board confirmation."
```

3. `GPCL-R10` is defined in `ddr_system_v4.0.yaml` with the statement:
   `"Must cite parent SIL IDs for each constraint."`
   Its semantic domain is: **citation / traceability**.

4. `GPCL-R10` is already assigned to `ORL-R4` with `consolidation_status: "1:1"`:
```yaml
   - from_rule_ids: "ORL-R4"
     to_rule_ids: "GPCL-R10"
     consolidation_status: "1:1"
     notes: "Maps to parent SIL citation rule."
```

5. A `1:1` mapping requires that the destination rule is the exclusive
   semantic equivalent of the source rule. Two source rules cannot each
   hold a `1:1` claim to the same destination rule.

6. The defect is therefore a **semantic category error and a destination
   collision**, not a missing rule definition.

7. The `tier_map` narrative in `ddr_system_v4.0.yaml` states:
   `"ORL-R1 through ORL-R7 become GPCL-R6 through GPCL-R10
   (ORL-R5 and ORL-R6 consolidated into GPCL-R9)."`
   This implies ORL-R7 must resolve to one of GPCL-R6 through GPCL-R10,
   but GPCL-R10 is already taken. The correct destination must be
   determined by semantic analysis of ORL-R7's source definition.

8. No `errata_log` block currently exists in `ddr_system_v4.0.yaml`.
   One must be introduced as a top-level block as part of this fix.

9. The YAML `rule_map` entry fields are exactly:
   `from_rule_ids`, `to_rule_ids`, `consolidation_status`, `notes`.
   Use only these field names. Do not invent new fields.

---

## Inviolable Constraints

These constraints must not be violated by any modification produced during
this task. If a proposed change would violate one of the following, stop,
report the conflict, and await human instruction before proceeding.

**AX-3 (Determinism):**
A `system_metadata.status` of `Finalized` requires all `rule_map` entries
to be fully resolved. The `notes` field must not contain any text indicating
an unresolved state (e.g., "TBD", "pending board confirmation", "Audit C-3").

**Semantic Equivalence:**
A `consolidation_status` of `"1:1"` is valid only when the destination rule's
normative statement is a direct semantic equivalent of the source rule. A rule
in the citation/traceability domain (GPCL-R10) cannot be the `1:1` destination
of a rule from a different semantic domain.

**Destination Exclusivity:**
No two `rule_map` entries may hold `consolidation_status: "1:1"` to the same
`to_rule_ids` value. Verify the full `rule_map` before assigning any `1:1`
destination.

**Scope Containment:**
Modify only the single `ORL-R7` entry in `rule_map`. Do not alter any other
`rule_map` entry, any `tier_map` entry, any `tier_definitions` block, any
`axioms` block, any `dag_invariants` block, or any `citation_rules` block.

**Cross-Artifact Consistency:**
Every change to `rule_map` in `ddr_system_v4.0.yaml` must be mirrored in
the corresponding row of the Rule-Level Cross-Reference table in Appendix B
of `DDR System(Opus_v4).md`. The two artifacts must be in agreement after
the fix is applied.

---

## Valid Consolidation Status Values

Use only these values for `consolidation_status`. Do not invent new values.

| Value | Meaning |
|---|---|
| `"1:1"` | Source rule has a direct semantic equivalent in v4.0 |
| `"N:1"` | Source rule is one of multiple rules consolidated into one destination |
| `"N:1 Consolidated"` | Synonym for N:1; used in some existing entries |
| `"Absorbed"` | Source rule's semantics are subsumed into a broader destination rule; no standalone equivalent exists |

---

## Required Modifications

### Modification 1 — `ddr_system_v4.0.yaml`: Correct the ORL-R7 rule_map Entry

Locate the defective `rule_map` entry for `ORL-R7` (confirmed in Structural
Facts above). Replace it with a corrected entry that:

- Sets `to_rule_ids` to the semantically correct GPCL destination rule,
  determined by matching ORL-R7's source semantic domain to an available
  GPCL rule definition.
- Sets `consolidation_status` to the applicable valid value from the table
  above.
- Sets `notes` to a clear, factual description of the mapping rationale with
  no unresolved annotations.

Before assigning a destination, verify:
1. The destination rule exists in `ddr_system_v4.0.yaml` under
   `tier_definitions[GPCL].atomic_inclusion_rules`.
2. No other `rule_map` entry holds `consolidation_status: "1:1"` to the same
   destination.
3. The destination rule's normative statement is semantically compatible with
   ORL-R7's source definition.

### Modification 2 — `ddr_system_v4.0.yaml`: Update `system_metadata`

Update the following fields only:
```yaml
system_metadata:
  status: Finalized          # remains Finalized — defect is now resolved
  date: "<today's date>"     # update to patch date
  lineage: "Supersedes DDR v4.0.0 (errata: ISSUE-011)"
```

Do not modify any other `system_metadata` fields.

### Modification 3 — `ddr_system_v4.0.yaml`: Introduce `errata_log`

Add the following block as a new top-level key in `ddr_system_v4.0.yaml`,
positioned immediately after the `system_metadata` block:
```yaml
errata_log:
  - issue_id: "ISSUE-011"
    description: >
      ORL-R7 was incorrectly mapped to GPCL-R10 with consolidation_status 1:1.
      GPCL-R10 is already the exclusive 1:1 destination of ORL-R4.
      The mapping also contained a TBD annotation, violating AX-3 in a
      Finalized artifact.
    resolution: >
      Corrected ORL-R7 destination to <confirmed-destination>.
      Applied consolidation_status <confirmed-status>.
      Removed TBD annotation. Restored AX-3 compliance.
    authority: "DDR Architecture Board"
    version_introduced: "4.0.0"
    version_fixed: "4.0.1"
```

Replace `<confirmed-destination>` and `<confirmed-status>` with the actual
values determined during Modification 1.

### Modification 4 — `DDR System(Opus_v4).md`: Synchronize Appendix B

Locate the Rule-Level Cross-Reference table in Appendix B. The current row
for ORL-R7 is grouped with ORL-R1 through ORL-R4 in a single row:
```
| ORL-R1 through ORL-R4, ORL-R7 | GPCL-R6, GPCL-R7, GPCL-R8, GPCL-R10 | 1:1 / TBD | Existing mapping documented rules |
```

Split this row so that ORL-R7 has its own entry reflecting the corrected
mapping. The existing ORL-R1 through ORL-R4 row should retain only those
four rules and their confirmed destinations.

Do not modify any other row in the Appendix B tables.

---

## Validation Checks

After applying all four modifications, verify each of the following manually
by reading the modified file content. There are no automated test scripts
for this repository. Each check is a direct inspection of file content.

| # | Check | Expected Result |
|---|---|---|
| V1 | Does the `rule_map` entry for `ORL-R7` contain any form of "TBD" or "pending"? | No |
| V2 | Is the `to_rule_ids` for `ORL-R7` the same as `to_rule_ids` for any other `rule_map` entry with `consolidation_status: "1:1"`? | No |
| V3 | Does the assigned destination rule exist in `tier_definitions[GPCL].atomic_inclusion_rules`? | Yes |
| V4 | Does the `errata_log` block exist at the top level of `ddr_system_v4.0.yaml`? | Yes |
| V5 | Does `errata_log[0].issue_id` equal `"ISSUE-011"`? | Yes |
| V6 | Does the Appendix B Rule-Level Cross-Reference table in `DDR System(Opus_v4).md` contain an entry for ORL-R7 that matches the corrected `rule_map` entry? | Yes |
| V7 | Have any `rule_map` entries other than ORL-R7 been modified? | No |
| V8 | Have any `tier_definitions`, `axioms`, `dag_invariants`, or `citation_rules` blocks been modified? | No |

If any check fails, report the specific failure and do not commit.

---

## Output Requirements

Return the following before committing anything:

1. **Semantic Classification Summary** — State the determined semantic domain
   of ORL-R7, the selected destination rule, and the consolidation status,
   with a one-sentence justification.

2. **YAML Diff** — Unified diff of all changes to `ddr_system_v4.0.yaml`.

3. **Markdown Diff** — Unified diff of all changes to `DDR System(Opus_v4).md`.

4. **Validation Report** — Explicit PASS or FAIL for each of V1 through V8
   with a one-line justification per check.

Await explicit approval of the Validation Report before creating any commit.

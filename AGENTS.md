# AGENTS.md — DDR System v4.0 | ISSUE-010 Resolution Session

## 1. Project Identity

This repository contains the **DDR System Specification v4.0** — a formal
requirements-traceability framework built on a Directed Acyclic Graph (DAG)
architecture. All schema modifications are subject to the invariants in §3
of this file. A violation of any invariant is a defect, regardless of
whether the change passes syntactic or structural validation.

---

## 2. Repository Structure

Locate the following files before taking any action. Do not assume paths —
search the repository for files matching these names if their location is
unclear; but, they should be located in: `.agent\assets\proposals\active\`

| Filename | Role |
|---|---|
| `ddr_node_schema.yaml` | **PRIMARY MODIFICATION TARGET.** JSON Schema 2020-12 definition of `DdrNode` and all `$defs` types. |
| `ddr_system_v4.0.yaml` | Current DDR System specification in YAML. Modify only if explicitly required by the issue report. |
| `DDR System(Opus_v4).md` | **READ-ONLY.** Original Markdown specification. Never modify this file. |
| `DDR_v4_Issue-010.md` | **READ-ONLY.** Issue report and endorsed resolution strategy. Treat as the authoritative task specification. |

---

## 3. Invariants — Never Violate

These rules are derived directly from the DDR System Specification v4.0.
If any proposed change would violate one of these invariants, **STOP and
report the conflict** rather than proceeding.

### INV-1 — Closed Schema Convention (project-wide)
Every object type definition in `ddr_node_schema.yaml` uses
`additionalProperties: false`. This is an established project-wide
convention. Any modified or new field definition must preserve this
convention. An `additionalProperties: true` declaration is never
acceptable on any object type in this schema.

### INV-2 — EXT-R3 Namespace Enforcement
Every key within `extension_annotations` must conform to the format:
```
EXTENSION_ID::annotation_key
```

Where:
- `EXTENSION_ID` is one or more uppercase alphanumeric characters or
  underscores (e.g., `HRE`, `DGA`)
- `annotation_key` is lowercase snake_case

This is the normative constraint being mechanically enforced by this
resolution. The regex encoding this rule is:
```
^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$
```

### INV-3 — AX-6 Core Field Protection (Declarative Integrity)
`extension_annotations` is read-only Extension metadata. Its keys must
**never** share names with `DdrNode` top-level Core fields (`content`,
`parent_ids`, `status`, `tier`, `id`). The schema modification in this
session must make this structurally unenforceable for non-conforming keys.

### INV-4 — Patch Scope Restriction
This is a v4.x patch change. Patch changes:
- Modify existing field definitions only
- Do **not** introduce new `$defs` type definitions
- Do **not** rename, add, or remove any top-level `DdrNode` field
- Do **not** alter the root `DdrNode` object's `additionalProperties: false`
  declaration

### INV-5 — Single-File Modification Boundary
The only file that requires modification to resolve ISSUE-010 is
`ddr_node_schema.yaml`. If analysis reveals a required change to any
other file, **stop and report** before proceeding — do not modify
additional files without explicit confirmation.

---

## 4. Validation Requirements

After applying the schema modification, verify the following before
committing. If Python and PyYAML are available in the environment, use:
```
python -c "import yaml; yaml.safe_load(open('ddr_node_schema.yaml'))"
```

If this tooling is not available, perform a structural review manually.

Regardless of tooling availability, confirm all of the following:

1. The `extension_annotations` field contains `patternProperties` with
   the key `"^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$"` and
   `additionalProperties: false` — both must be present together.
2. `additionalProperties: true` does not appear anywhere in
   `ddr_node_schema.yaml`.
3. The root `DdrNode` object's `additionalProperties: false` declaration
   is present and unchanged.
4. The count of `$defs` type definitions before and after the edit is
   identical.
5. No field other than `extension_annotations` was modified.
6. The canonical example key `HRE::min_hardware_profile` matches the
   applied regex (manual confirmation acceptable).

---

## 5. Prohibited Actions

- Do **not** modify `DDR System(Opus_v4).md` for any reason.
- Do **not** introduce new `$defs` type definitions.
- Do **not** alter the `DdrNode` root-level `additionalProperties: false`
  declaration.
- Do **not** rename, add, or remove any top-level field of `DdrNode`.
- Do **not** implement Option B from `DDR_v4_Issue-010.md` — it is a
  breaking change reserved for a future major version. Option A is the
  exclusively endorsed strategy for this session.
- Do **not** modify `ddr_system_v4.0.yaml` to retroactively fix any
  pre-existing EXT-R3 violations discovered during analysis. Report them
  separately; do not remediate them in this session.
- Do **not** silently proceed past a failed validation check. Report
  failures explicitly before taking any further action.

---

## 6. Commit Message Format

Use the following exact format for the resolution commit:
```
ISSUE-010 Resolution: Enforce EXT-R3 namespace convention via patternProperties

Problem: extension_annotations used additionalProperties: true, making
EXT-R3 compliance a prose-only rule with no machine-verifiable enforcement.
Core field name shadows and namespace-less keys passed schema validation
without error (AX-6, EXT-R3).

Solution (Option A): Replaced additionalProperties: true with
patternProperties + additionalProperties: false using regex
^[A-Z][A-Z0-9_]+::[a-z][a-z0-9_]+$ on extension_annotations in
ddr_node_schema.yaml. Non-breaking for all compliant annotations.

Validation: [list each check result as PASS or FAIL]
Files changed: ddr_node_schema.yaml (1 field definition, ~5 lines)
```

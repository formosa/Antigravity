---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/tier_hierarchy.md
  - protocols/traceability_chain.md
related:
  - constraints/tag_citation_required.md
  - constraints/sibling_prohibition.md
agents:
  - traceability_auditor
---

# Trace Complete Chain

> **Scope**: Rule-based validation that every ISP tag traces back to a BRD root through a complete citation chain.
>
> **Excludes**: Chain repair (see orphan resolution workflows); impact analysis.

## Summary

This protocol defines the four terminal conditions when traversing citations upward from any tag. A valid chain must reach a BRD root. All other terminal conditions are errors.

## Prerequisites

- Target tag to trace
- Access to all documentation files with `:links:` directives

## Procedure

### Step 1: Begin Traversal

Starting from the target tag, read its `:links:` directive to identify parent citations.

### Step 2: Evaluate Terminal Conditions

Traverse citations upward until one of these conditions is reached:

| Condition | Result | Severity |
| :---------- | :------- | :--------- |
| BRD Root Reached | VALID | — |
| Cycle Detected (A→B→A) | ERROR | Circular Dependency |
| Missing Parent | ERROR | Broken Chain / Orphan |
| Sibling Citation (A.1→A.2) | ERROR | Invalid Topology |

### Step 3: Report

Document chain status for each traced tag using the standard report format from `traceability_chain.md`.

## Outcomes

| Result | Condition | Next Action |
| :------- | :---------- | :------------ |
| Valid | BRD root reached | Document in audit report |
| Error | Any non-BRD terminal | Invoke orphan resolution |

---

## References

- `protocols/traceability_chain.md` — Full validation protocol
- `constraints/tag_citation_required.md` — Citation mandate
- `constraints/sibling_prohibition.md` — Sibling citation prohibition
- Source: `documentation_system.md` §27.3.3.2 Trace Complete Chain

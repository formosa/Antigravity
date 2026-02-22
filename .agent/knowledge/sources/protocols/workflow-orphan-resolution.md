---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/tier-hierarchy.md
  - protocols/traceability-chain.md
related:
  - protocols/abstraction-upward.md
  - protocols/abstraction-downward.md
agents:
  - traceability_auditor
  - manifest_manager
---

# Workflow: Orphan Resolution

> **Scope**: Procedure for resolving orphaned tags via upward abstraction or downward specification.
>
> **Excludes**: Initial orphan detection (see `traceability-chain.md`); lateral abstraction.

## Summary

Resolves orphaned tags (missing parents) by classifying the orphan type and applying the appropriate resolution strategy — Upward Abstraction for implementation-level orphans, Downward Specification for high-level orphans.

## Prerequisites

- Orphan tag identified by `@traceability_auditor`
- Access to existing DDR documentation
- Understanding of tier adjacency rules

## Procedure

### Step 1: Classify Orphan

| Orphan Type            | Condition                        | Strategy                 |
| :--------------------- | :------------------------------- | :----------------------- |
| BRD Tier               | Tag is BRD                       | No action (Root allowed) |
| Implementation Detail  | Tag contains technical specifics | Upward Abstraction       |
| High-Level Requirement | Tag is abstract/strategic        | Downward Specification   |

### Step 2: Execute Resolution

**Upward Abstraction**:

1. Synthesize parent tag in N-1 tier.
2. Example: ISP orphan → Create TDD parent.
3. Link orphan to new parent via `:links:`.

**Downward Specification**:

1. Decompose into child tags in N+1 tier.
2. Example: NFR orphan → Create FSD children.
3. Link children to orphan parent.

### Step 3: Validate Synthesis

Invoke `@traceability_auditor` to confirm chain completeness.

### Step 4: Update Documentation

Invoke `@manifest_manager` to update reconciliation manifests.

## Outcomes

| Result    | Condition                    | Next Action         |
| :-------- | :--------------------------- | :------------------ |
| Resolved  | Chain complete to BRD        | Close orphan ticket |
| Cascading | New parent is also orphan    | Repeat from Step 1  |
| Blocked   | Cannot determine parent tier | Escalate to user    |

---

## References

- `protocols/abstraction-upward.md` — Parent synthesis protocol
- `protocols/abstraction-downward.md` — Child decomposition protocol
- `protocols/traceability-chain.md` — Orphan detection
- Source: `.agent/assets/documentation_system.md` §27.3.1.4, §27.5.2 Orphan Resolution
---
archetype: protocol
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/information_flow.md
related:
  - protocols/abstraction_upward.md
  - protocols/abstraction_lateral.md
agents:
  - ddr_orchestrator
---

# Abstraction Downward

> **Scope**: Protocol for decomposing high-level requirements into concrete child specifications.
>
> **Excludes**: Upward abstraction; lateral expansion; classification.

## Summary

Downward specification decomposes abstract parent requirements into concrete child implementations. It extracts specific mechanisms, quantitative constraints, and technical details from high-level statements, creating properly-linked child tags.

## Prerequisites

- Parent tag needing decomposition
- Understanding of child tier's content requirements
- Knowledge of implementation options

## Procedure

### Step 1: Identify Implementation Vectors

What specific technologies, patterns, or mechanisms enable this requirement?

| Parent Tier | Child Tier | Vector Types |
|:------------|:-----------|:-------------|
| BRD → NFR | Quantitative constraints | Latency, throughput, resource limits |
| NFR → FSD | Capability requirements | User-facing behaviors |
| FSD → SAD | Architectural patterns | Topology, concurrency model |
| SAD → ICD | Data contracts | Schemas, message formats |
| ICD → TDD | Component structures | Classes, methods, dependencies |
| TDD → ISP | Code skeletons | Stubs with docstrings |

### Step 2: Extract Measurables

Convert qualitative goals to quantitative specifications:

| Qualitative (BRD) | Quantitative (NFR) |
|:------------------|:-------------------|
| "Fast response" | "< 1 second average latency" |
| "Sub-250ms IPC" | "< 1ms metadata, < 20ms 1MB payload" |
| "High reliability" | "99.9% uptime, < 5s recovery" |

### Step 3: Partition by Concern

Separate into appropriate child categories:

**Parent**: BRD-8.1 "Sub-250ms IPC dispatch; <1s LLM response"

| Concern | Child Tag | Content |
|:--------|:----------|:--------|
| Metadata latency | NFR-4.1 | IPC Dispatch: < 1ms metadata-only |
| Payload latency | NFR-4.2 | Round Trip: < 20ms for 1MB payload |
| Model latency | NFR-4.3 | LLM Inference: < 1s average |

### Step 4: Maintain Traceability

All derived children MUST cite the parent:

```rst
.. nfr:: IPC Dispatch: Sub-millisecond (< 1ms) for metadata-only.
   :id: NFR-4.1
   :links: BRD-8.1
```

### Step 5: Validate Completeness

Check that children collectively cover parent scope:
- No gaps (missing aspects of parent)
- No overlaps (duplicate coverage)
- No scope creep (beyond parent intent)

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Success | Children fully cover parent | Document in reconciliation manifest |
| Incomplete | Gaps remain | Create additional children |
| Over-specified | Children exceed parent scope | Revise or escalate to parent tier |

---

## References

- `concepts/information_flow.md` — Cascade principles
- `protocols/abstraction_upward.md` — Reverse protocol
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.2

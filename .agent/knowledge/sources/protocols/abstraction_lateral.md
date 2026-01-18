---
archetype: protocol
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
related:
  - protocols/abstraction_upward.md
  - protocols/abstraction_downward.md
  - constraints/sibling_prohibition.md
agents:
  - ddr_orchestrator
---

# Abstraction Lateral

> **Scope**: Protocol for generating sibling tags when a tag implies parallel concerns at the same abstraction level.
>
> **Excludes**: Vertical abstraction (upward/downward); sibling citation rules.

## Summary

Lateral expansion identifies when an isolated tag implies peer requirements at the same abstraction level. It generates sibling tags for parallel concerns, ensuring comprehensive coverage within a tier while maintaining proper parent citations.

## Prerequisites

- Existing tag that appears isolated
- Understanding of parallel concerns at same abstraction
- Knowledge of tier's content scope

## Procedure

### Step 1: Identify Isolation Pattern

A tag is a candidate for lateral expansion when:
- It addresses one instance of a pattern (e.g., one fault type)
- Similar concerns exist at the same level (e.g., other faults)
- The concern is not exhaustively covered

### Step 2: Enumerate Parallel Concerns

List all peer-level concerns the isolated tag implies:

**Example**: FSD-7.1 "LogServer Fault: Senders continue, drop logs silently."

| Implied Parallel Concern |
|:-------------------------|
| What about Service faults? |
| What about Core faults? |
| What about timeout scenarios? |
| What about network failures? |

### Step 3: Create Parent Block (if missing)

If siblings share a common theme, create a block-level parent:

```rst
.. fsd:: Error Handling Strategy
   :id: FSD-7
   :links: BRD-2, NFR-5
```

### Step 4: Generate Siblings

Create atomic tags for each parallel concern:

```rst
.. fsd:: LogServer Fault: Senders continue, drop logs silently.
   :id: FSD-7.1
   :links: FSD-7

.. fsd:: Service Fault: Core detects, marks unavailable, enters error state.
   :id: FSD-7.2
   :links: FSD-7

.. fsd:: Timeout: Core detects non-response > 5s, triggers error handling.
   :id: FSD-7.3
   :links: FSD-7

.. fsd:: Core Fault: Services disconnect, attempt periodic reconnect.
   :id: FSD-7.4
   :links: FSD-7
```

### Step 5: Validate Coverage

Check that siblings:
- Address the same abstraction level
- Provide comprehensive coverage of the concern
- Cite the same parent (block or upstream tier)
- Do not cite each other (see `sibling_prohibition.md`)

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Complete set | All parallel concerns covered | Update reconciliation manifest |
| Partial set | Some concerns remain | Continue sibling generation |
| Over-expansion | Too granular for tier | Merge or demote to lower tier |

---

## References

- `protocols/abstraction_upward.md` — Creating missing parents
- `protocols/abstraction_downward.md` — Decomposing parents
- `constraints/sibling_prohibition.md` — No peer citations
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.3

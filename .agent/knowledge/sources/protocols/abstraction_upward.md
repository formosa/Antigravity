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
  - protocols/abstraction_downward.md
  - protocols/abstraction_lateral.md
agents:
  - traceability_auditor
  - orphan_detective
---

# Abstraction Upward

> **Scope**: Protocol for synthesizing missing parent requirements from orphaned child specifications.
>
> **Excludes**: Downward specification; lateral expansion; classification.

## Summary

Upward abstraction synthesizes parent tags when orphaned specifications exist without proper citations. It extracts strategic intent or constraint boundaries from implementation details, creating missing parent requirements that justify the orphaned child.

## Prerequisites

- Identified orphan tag (no valid parent citation)
- Understanding of tier immediately above the orphan
- Familiarity with parent tier's language and constraints

## Procedure

### Step 1: Identify the Essence

Strip implementation details; preserve the "why" or "what limit":

| Child Tier | Extract | Discard |
|:-----------|:--------|:--------|
| ISP → TDD | Class responsibility | Code syntax |
| TDD → SAD | Pattern rationale | Method signatures |
| SAD → FSD | User capability | Topology details |
| FSD → NFR | Constraint boundary | Feature behavior |
| NFR → BRD | Business objective | Technical metrics |

### Step 2: Elevate Abstraction

Transform technical specifics into parent tier language:

| Original (TDD) | Abstracted (SAD) |
|:---------------|:-----------------|
| "Spawns receiver thread to poll ROUTER socket" | "Non-blocking I/O via dedicated polling threads" |

| Original (FSD) | Abstracted (BRD) |
|:---------------|:-----------------|
| "Wake word detection using pvporcupine" | "Hands-free voice activation for accessibility" |

### Step 3: Validate Scope

Ensure synthesized parent:
- Encompasses multiple potential child implementations
- Uses tier-appropriate language
- Doesn't duplicate existing tags
- Cites its own parent tier (unless BRD)

### Step 4: Create Parent Tag

Apply appropriate tier template and establish bidirectional link:

**Before** (orphan):
```rst
.. tdd:: Spawns receiver thread to poll ROUTER socket.
   :id: TDD-1.7
   (no :links:)
```

**After** (linked):
```rst
.. sad:: Receiver Threads: Dedicated thread per process to poll ZMQ sockets.
   :id: SAD-4.1
   :links: NFR-5.1

.. tdd:: Spawns receiver thread to poll ROUTER socket.
   :id: TDD-1.7
   :links: SAD-4.1
```

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Success | Parent created, orphan linked | Validate chain to BRD |
| Duplicate found | Existing parent covers this | Link orphan to existing tag |
| Chain incomplete | New parent also orphaned | Recurse upward abstraction |

---

## References

- `concepts/information_flow.md` — Traceability principles
- `protocols/abstraction_downward.md` — Reverse protocol
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.1

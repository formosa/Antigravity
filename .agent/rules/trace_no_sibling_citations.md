---
type: rule
name: "Trace No Sibling Citations"
activation: glob
globs:
  - "docs/**/*.rst"
priority: 85
trigger:
  - "sibling"
  - "peer"
  - "lateral"
severity: mandatory
description: "Tags cannot cite peer tags at the same abstraction level."
---
# Trace No Sibling Citations Rule

## Rule Statement

**ALL TIERS: Tags MUST NOT cite peer tags at the same abstraction level.**

## Detection

| Pattern | Example |
| :-------- | :--------- |
| Same prefix in `:links:` | FSD-4.4 links to FSD-4.3 |
| Same block parent | Both tags under FSD-4 |
| Sequential dependency | "This follows from..." sibling |

## Enforcement

| Violation | Severity | Resolution |
| :---------- | :--------: | :----------- |
| Sibling citation | ERROR | Remove sibling link |
| Sequential dependency | WARNING | Express in prose, not citation |

## Pattern Detection

```plaintext
TAG-X.1 citing TAG-X.2 → VIOLATION
TAG-X citing TAG-Y → VALID
FSD-4.4 citing FSD-4.3 → VIOLATION
FSD-4.4 citing FSD-4 → VALID
```

## Examples

### ✅ Correct

.. code-block:: rst

   .. fsd:: LogServer Fault handling
      :id: FSD-7.1
      :links: FSD-7

Cites block parent, not siblings.

### ❌ Incorrect

.. code-block:: rst

   .. fsd:: VAD (Stage 2): Refines Stage 1.
      :id: FSD-4.4
      :links: FSD-4.3

**Why**: FSD-4.3 and FSD-4.4 are peers under FSD-4.

## Related Rules

- [trace_complete_chain.md](trace_complete_chain.md) — Complete chain to BRD root
- [ddr_traceability_mandate.md](ddr_traceability_mandate.md) — Parent citation required
- [trace_no_forward_references.md](trace_no_forward_references.md) — No downward citations

## References

- Knowledge: `constraints/sibling_prohibition.md`
- Source: DDR Meta-Standard §3.6

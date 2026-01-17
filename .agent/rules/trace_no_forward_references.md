---
type: rule
name: "Trace No Forward References"
globs:
  - "docs/**/*.rst"
priority: 85
trigger:
  - "forward"
  - "reference"
  - "citation"
severity: mandatory
description: "Tags cannot cite tags in lower (more concrete) tiers."
---
# Trace No Forward References Rule

## Rule Statement

**ALL TIERS: Citations MUST only reference tags in higher (more abstract) tiers.**

## Valid Citation Matrix

| Child Tier | May Cite |
|:-----------|:---------|
| NFR | BRD |
| FSD | BRD, NFR |
| SAD | FSD |
| ICD | SAD, NFR |
| TDD | SAD, ICD |
| ISP | TDD |

## Detection

| Pattern | Example |
|:--------|:--------|
| Lower cites higher | TDD-1 links to ISP-3 |
| Downward reference | FSD-4 links to SAD-1 |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Forward reference | ERROR | Remove invalid citation |
| Downward citation | ERROR | Reverse or restructure |

## Enforcement Protocol

1. Extract tier from tag ID
2. Extract tier from cited parent
3. Verify child tier is lower than parent tier
4. Report FORWARD_REFERENCE error if validation fails

## Examples

### ✅ Correct

.. code-block:: rst

   .. tdd:: CoreProcess class structure.
      :id: TDD-1
      :links: SAD-2, ICD-1

### ❌ Incorrect

.. code-block:: rst

   .. sad:: System architecture.
      :id: SAD-2
      :links: TDD-1

**Why**: SAD cannot cite TDD (lower tier).

## References

- Knowledge: `protocols/traceability_chain.md`
- Source: DDR Meta-Standard §4.1

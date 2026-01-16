---
archetype: protocol
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/information_flow.md
related:
  - constraints/tag_citation_required.md
  - protocols/impact_analysis.md
agents:
  - traceability_auditor
---

# Traceability Chain

> **Scope**: Protocol for validating complete traceability from any tag to BRD root.
>
> **Excludes**: Chain synthesis (abstraction protocols); impact analysis.

## Summary

Every DDR tag (except BRD root) must have a complete traceability chain to the BRD tier. This protocol validates that chains are complete, properly ordered, and contain no violations (orphans, cycles, forward references).

## Prerequisites

- Target tag to validate
- Access to all documentation files
- Understanding of valid citation hierarchy

## Procedure

### Step 1: Extract Citation

Parse the target tag's `:links:` directive:

```rst
.. tdd:: CoreProcess class structure
   :id: TDD-1
   :links: SAD-2, FSD-1.1
```

Citations: `[SAD-2, FSD-1.1]`

### Step 2: Validate Citation Targets

For each cited tag:
1. Verify tag exists in documentation
2. Verify tag is in valid parent tier
3. Verify no forward references (lower tier cannot cite higher)

**Valid Citation Matrix**:

| Child Tier | May Cite |
|:-----------|:---------|
| NFR | BRD |
| FSD | BRD, NFR |
| SAD | FSD |
| ICD | SAD, NFR |
| TDD | SAD, ICD |
| ISP | TDD |

### Step 3: Recurse Upward

For each cited parent, repeat Steps 1-2 until reaching BRD.

**Example Chain**: ISP-3.1 → TDD-3 → SAD-2, ICD-1 → FSD-1.3, NFR-4 → BRD-5.2, BRD-2

### Step 4: Detect Violations

| Violation | Detection | Severity |
|:----------|:----------|:---------|
| **Orphan** | Tag has empty `:links:` (non-BRD) | ERROR |
| **Missing parent** | Cited tag doesn't exist | ERROR |
| **Forward reference** | TDD cites ISP | ERROR |
| **Sibling citation** | FSD-1.2 cites FSD-1.1 | ERROR |
| **Broken chain** | Parent is orphan | WARNING |
| **Cycle** | A → B → C → A | ERROR |

### Step 5: Generate Report

| Tag | Status | Chain | Issue |
|:----|:-------|:------|:------|
| TDD-1.7 | ✅ VALID | TDD-1.7 → SAD-4.1 → NFR-5.1 → BRD-2 | — |
| ICD-5 | ❌ ORPHAN | ICD-5 → (none) | Missing parent citation |
| FSD-4.3 | ❌ BROKEN | FSD-4.3 → NFR-99 (missing) | Parent not found |

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| Valid chain | Complete path to BRD | Document in audit report |
| Orphan | No parent citation | Use `abstraction_upward.md` |
| Missing parent | Cited tag not found | Locate or create parent |
| Cycle detected | Circular reference | Break cycle, restructure |

---

## References

- `concepts/information_flow.md` — Traceability principles
- `constraints/tag_citation_required.md` — Citation mandate
- `protocols/impact_analysis.md` — Downstream effects
- Source: `ddr_meta_standard.txt` §4.1 Upstream Citation Mandates

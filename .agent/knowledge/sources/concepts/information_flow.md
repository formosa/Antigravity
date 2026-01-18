---
archetype: concept
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/ddr_overview.md
  - concepts/tier_hierarchy.md
related:
  - protocols/abstraction_upward.md
  - protocols/abstraction_downward.md
  - constraints/tag_citation_required.md
---

# Information Flow

> **Scope**: How requirements cascade downward and traceability flows upward through the DDR hierarchy.
>
> **Excludes**: Specific abstraction protocols (see `protocols/abstraction_*.md`); tag syntax details.

## Summary

The DDR operates on a principle of **unidirectional flow**: requirements cascade downward from business intent to implementation, while traceability citations flow upward from implementation to business justification. This creates a complete audit trail from any code stub back to the strategic objective it serves.

## Definition

**Information flow** describes the directional movement of content through the DDR hierarchy:
- **Downward cascade**: High-level requirements decompose into increasingly specific implementations
- **Upward traceability**: Every artifact cites its justification from higher tiers

## Characteristics

### Downward Cascade (Specification)

Requirements flow from abstract to concrete:

```
BRD: "Enable real-time AI assistant"
  ↓ decomposes to
NFR: "Response latency < 1 second"
  ↓ constrains
FSD: "Runtime Process handles LLM inference"
  ↓ structures as
SAD: "GPU-dedicated process using DEALER socket"
  ↓ contracts as
ICD: "Inference request JSON schema"
  ↓ designs as
TDD: "RuntimeProcess class with infer() method"
  ↓ stubs as
ISP: "def infer(self, prompt: str) -> str: pass"
```

### Upward Traceability (Citation)

Every non-BRD tag MUST cite parent tags that justify its existence:

```
ISP-3.1 ← TDD-3
TDD-3 ← SAD-2, ICD-1
SAD-2 ← FSD-1.3
FSD-1.3 ← BRD-5.2, NFR-4
NFR-4 ← BRD-2
BRD-2 (root - no citation)
```

### The Audit Trail

For any ISP tag, you can trace the complete justification chain:
1. Which TDD defines its structure?
2. Which SAD/ICD shapes that design?
3. Which FSD requires that capability?
4. Which NFR constrains it?
5. Which BRD justifies building it?

### Cascade Invalidation

When a parent tag changes, all downstream citations are potentially affected:

```
BRD-5.2 modified → Flags DIRTY:
  → NFR-4 (cites BRD-5.2)
    → FSD-1.3 (cites NFR-4)
      → SAD-2 (cites FSD-1.3)
        → ... cascade continues
```

## Context

Information flow principles govern:

- **Classification**: Where new information belongs in the hierarchy
- **Impact analysis**: What downstream content needs review after changes
- **Orphan resolution**: How to synthesize missing parent requirements
- **Validation**: Ensuring every artifact has complete traceability

---

## References

- `concepts/tier_hierarchy.md` — The seven-tier structure
- `protocols/abstraction_upward.md` — Synthesizing missing parents
- `protocols/abstraction_downward.md` — Decomposing requirements
- Source: `ddr_meta_standard.txt` §4. Traceability & Reconciliation System

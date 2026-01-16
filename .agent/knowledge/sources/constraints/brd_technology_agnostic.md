---
archetype: constraint
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_brd.md
related:
  - constraints/brd_measurable_metrics.md
tiers:
  - BRD
agents:
  - brd_strategist
---

# BRD Technology Agnostic

> **Scope**: Rule that BRD content must not contain technology-specific terms.
>
> **Excludes**: Other BRD constraints; tier definitions.

## Summary

The BRD tier captures business intent in language accessible to all stakeholders. Technology-specific terms (like specific libraries, programming languages, or hardware) belong in lower tiers. BRD must describe WHAT to achieve, not HOW.

## Rule Statement

**BRD: Content MUST NOT contain technology-specific terms, implementation details, or solution-prescriptive language.**

## Rationale

- BRD addresses stakeholders who may not be technical
- Technology decisions emerge from constraints (NFR) and design (SAD)
- Technology-agnostic requirements support multiple implementation options
- Premature technology prescription limits architectural freedom

## Detection

How to identify violations:

| Pattern | Examples |
|:--------|:---------|
| Programming languages | Python, JavaScript, React |
| Libraries/frameworks | ZeroMQ, PySide6, pvporcupine |
| Hardware specifics | RTX 3080, AMD Ryzen, CUDA |
| Protocols | TCP, MQTT, REST API |
| File formats | JSON, YAML, Protobuf |
| Database names | PostgreSQL, Redis, SQLite |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Technology term in BRD | ERROR | Abstract to business language |
| Implementation detail | ERROR | Move to appropriate tier |
| Solution prescription | WARNING | Reframe as objective |

## Examples

### ✅ Correct

```rst
.. brd:: Enable hands-free voice interaction for accessibility.
   :id: BRD-5.7
```

```rst
.. brd:: System must operate without internet connectivity.
   :id: BRD-3.1
```

```rst
.. brd:: Response time must feel instantaneous to users.
   :id: BRD-8
```

### ❌ Incorrect

```rst
.. brd:: Wake word detection using pvporcupine.
   :id: BRD-5.7
```
**Why**: "pvporcupine" is a specific library. Correct: "Hands-free voice activation"

```rst
.. brd:: Use ZeroMQ for inter-process communication.
   :id: BRD-4.1
```
**Why**: "ZeroMQ" prescribes implementation. Correct: "Enable reliable message passing between components"

```rst
.. brd:: Deploy on RTX 3080 GPU.
   :id: BRD-6.1
```
**Why**: Hardware specifics belong in NFR. Correct: "Support GPU-accelerated inference"

---

## References

- `concepts/tier_brd.md` — BRD tier definition
- `constraints/brd_measurable_metrics.md` — Related BRD constraint
- Source: `ddr_meta_standard.txt` §2.1 Business Requirements Document

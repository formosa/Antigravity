---
archetype: constraint
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-18
requires:
  - vocabulary/glossary.md
  - concepts/tier_fsd.md
related: []
tiers:
  - FSD
agents:
  - fsd_analyst
---

# FSD No Implementation

> **Scope**: Rule that FSD content must not contain implementation details, code, or algorithms.
>
> **Excludes**: Other tier constraints; FSD structure.

## Summary

FSD (Feature Specifications Document) describes WHAT the system does from a user/stakeholder perspective. It must not prescribe HOW things work internally—implementation details belong in SAD, TDD, and ISP tiers.

## Rule Statement

**FSD: Content MUST describe capabilities and behaviors, NOT implementation mechanisms, code, or algorithms.**

## Rationale

- FSD addresses product owners and UX designers
- Implementation decisions emerge from architecture (SAD)
- Premature implementation in FSD constrains design options
- FSD should remain stable even if implementation changes

## Detection

How to identify violations:

| Pattern | Examples |
|:--------|:---------|
| Code snippets | Python/JSON in FSD content |
| Class/method names | "CoreProcess.run()" |
| Algorithm descriptions | "Uses binary search to..." |
| Library references | "via PySide6 widget" |
| Data structure specifics | "stored in Dict[str, Tuple]" |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Code in FSD | ERROR | Remove; move to TDD/ISP |
| Algorithm detail | ERROR | Abstract to behavior |
| Class reference | WARNING | Describe capability instead |
| Library mention | ERROR | Abstract to feature |

## Examples

### ✅ Correct

```rst
.. fsd:: Voice pipeline processes audio through wake word detection, then voice activity detection, then speech recognition.
   :id: FSD-4
   :links: BRD-5.7
```

```rst
.. fsd:: System maintains awareness states: sleeping, waking, active, busy, error.
   :id: FSD-2.3
   :links: BRD-2
```

```rst
.. fsd:: User receives visual feedback within 100ms of voice input.
   :id: FSD-8.1
   :links: BRD-8, NFR-4
```

### ❌ Incorrect

```rst
.. fsd:: Use pvporcupine.create() for wake word detection.
   :id: FSD-4.1
```
**Why**: Library-specific API. Correct: "Detect wake word with < 200ms latency"

```rst
.. fsd:: Implement using transitions.Machine for state management.
   :id: FSD-2.3
```
**Why**: Implementation detail. Correct: "Maintain hierarchical state machine"

```rst
.. fsd:: Store active requests in Dict[str, Tuple[bytes, float]].
   :id: FSD-1.5
```
**Why**: Data structure belongs in TDD. Correct: "Track pending requests"

---

## References

- `concepts/tier_fsd.md` — FSD tier definition
- Source: `ddr_meta_standard.txt` §2.3 Feature Specifications Document

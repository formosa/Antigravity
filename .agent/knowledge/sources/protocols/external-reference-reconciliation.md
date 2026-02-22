---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/metadata-schema.md
  - sources/protocols/implementation-guardrails.md
related:
  - sources/patterns/source-citation-style.md
---

# External Reference Reconciliation

> **Scope**: Deterministic handling of externally supplied DDR references (e.g., Google Docs) when access may be restricted.
> **Excludes**: Granting network/auth permissions.

## Summary

This protocol prevents hallucination and policy drift by requiring explicit evidence capture, deferred reconciliation, and repository-first enforcement whenever external reference sources cannot be retrieved.

## Prerequisites

- External reference URL or exported file
- Current repository canonical sources
- Validation tooling

## Procedure

1. Attempt retrieval of external reference and capture command evidence.
2. If retrieval fails, log `external_reference_unresolved` with timestamp, URL, and failure details.
3. Continue implementation using `.agent/knowledge/**` + `.agent/assets/documentation_system.md` only.
4. Create deferred reconciliation task referencing unresolved source.
5. When external source becomes available, run structured diff against canonical sources and applied explicit, traceable updates.

## Outcomes

| Result     | Condition           | Next Action                                          |
| :--------- | :------------------ | :--------------------------------------------------- |
| Retrieved  | Source accessible   | Diff and reconcile immediately                       |
| Unresolved | Source inaccessible | Continue with canonical sources + open deferred task |

---

## References

- `sources/protocols/implementation-guardrails.md` — Safe execution controls
- `sources/patterns/source-citation-style.md` — Provenance conventions
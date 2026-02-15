---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/metadata_schema.md
  - sources/patterns/source_citation_style.md
related:
  - sources/protocols/traceability_chain.md
---

# Implementation Guardrails

> **Scope**: Deterministic execution protocol to reduce agent hallucination and patch drift during DDR modifications.
> **Excludes**: Business prioritization of change requests.

## Summary

This protocol defines mandatory preflight, execution, and postflight checks for any agent modifying DDR knowledge files.

## Prerequisites

- Local repository access
- Baseline validation script availability
- Approved modification specification

## Procedure

1. Capture baseline inventory and validation output.
2. Apply only explicitly listed modifications.
3. Re-run validation after each logical batch.
4. Halt on first schema error and record the failing unit ID.
5. produce final delta report with changed files and rule outcomes.

## Outcomes

| Result | Condition | Next Action |
| :------- | :---------- | :------------ |
| Pass | All checks green | Merge-ready |
| Soft fail | Non-blocking warnings | Open follow-up issue |
| Hard fail | Schema/path/provenance violation | Block merge |

---

## References

- `sources/patterns/metadata_schema.md` — Validation rules
- `sources/patterns/source_citation_style.md` — Provenance syntax

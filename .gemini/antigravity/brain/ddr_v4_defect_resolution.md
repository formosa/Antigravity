# Decision Record: DDR v4 Specification Fixes

**Date**: 2026-02-27T03:10:00Z
**Implemented by**: Gemini 3 Flash via Implementation Planning Skill v3.0
**Planned by**: Gemini 3.1 Pro via Implementation Planning Skill v3.0
**Objective**: Resolve 6 confirmed logical and structural defects in the DDR System v4.0 specification identified during adversarial audit.

## Decision Summary

The following 6 modifications were applied to `DDR System(Opus_v4).md`:

1. **R1 (CL-R9 Citation Rule):** Restricted CL-R9 to FCL-only citations. This eliminates a three-way structural contradiction between citation constraints (CIT-R2, CIT-R4) and tier-skipping rules.
2. **R2 (SUPERSEDE Operation):** Explicitly defined automatic `parent_ids` retargeting with content-only `DIRTY` propagation. This resolves ambiguity that previously allowed for manual-only interpretations.
3. **R3 (DELETE Orphan Resolution):** Added a mandatory resolution protocol for structural orphans (re-attach, cascade, or supersede). This reinforces Axiom AX-1 (Traceability).
4. **R4 (CDL-R7 Propagation):** Added a CDL rule requiring language-specific blueprints when CL declares multiple targets. This removes a "dark dependency" from Tier 4 (CL) to Tier 8 (ISL).
5. **R5 (Tier-Skipping Invariant):** Qualified the "no tier-skipping" invariant with the "active" keyword to align with the specification's conditional-activation model.
6. **R6 (UNBUNDLE Determinism):** Added an explicit content-annotation requirement for Express Mode unbundling to ensure deterministic tier allocation without "invention" (AX-3).

## Constraints Established

- **CL-R9 Restriction:** Future modifications MUST NOT re-introduce the "or GPCL" citation option in CL-R9 without a corresponding structural amendment to CIT-R2.
- **Table Alignment:** All future edits to specification tables MUST be followed by an execution of the `md060-strict-aligner` skill to maintain strict vertical pipe alignment.

## Files Modified

- `.agent/assets/proposals/future/DDR System(Opus_v4).md` — MODIFY (6 targeted sections)

## Research Citations Used

- [logical_audit_report.md.resolved](file:///C:/Users/email/.gemini/antigravity/brain/78e5b4c1-2e19-489b-8f34-955cd0d3ba30/logical_audit_report.md.resolved) — 2026-02-26 — Primary source for all 6 requirements.

## Verification Artifacts

- **Grep Assertions:** 7/7 grep tests passed (confirming insertion/replacement of all key strings).
- **Linter Status:** All MD060 violations resolved via `align_table.py`.
- **Manual Audit:** Confirmed CDL rules table growth to 7 rows and §11 checklist synchronization.

## Rollback Reference

- Git pre-execution state available via `git checkout HEAD~1`.

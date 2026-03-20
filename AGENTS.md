# AGENTS.md — DDR System Repository

## Project Overview

This repository contains the DDR System Specification v4.0, a formal software
documentation and requirements traceability framework using a directed acyclic
graph (DAG) architecture. The authoritative specification file is:
  `ddr_system_v4_0.yaml`

The original Markdown reference document is:
  `DDR System(Opus_v4).md`

Issue resolution reports are located in:
  `issues/` (e.g., `DDR_v4_Issue-002.md`)

## Inviolable Axioms (must not be broken by any edit)

- AX-1: Every node must have a complete, honest, and traceable audit chain.
- AX-2: Technology and implementation specificity are deferred until logically
  necessary. Tiers above CL (XPD, SIL, GPCL, FCL) must contain no technology,
  hardware, or implementation references.
- AX-3: All VERIFY validation rules must be fully deterministic and mechanically
  verifiable from node properties alone — no ambiguous checks permitted.

## Schema Modification Rules

- All changes to `ddr_system_v4_0.yaml` must be backward-compatible unless a
  version bump is explicitly instructed.
- New fields added to tier node schemas must include a default value that
  preserves validity of all pre-existing nodes.
- New rules must be co-registered in the rules index and the VERIFY logic block.
- DAG topology (parent/child tier relationships and edge types) must not be
  altered without an explicit version bump instruction.

## Validation Checklist (run before committing any change)

1. Confirm `constraint_origin` defaults to `derived` in schema — no existing
   CL nodes require migration.
2. Confirm `CL-R9` is preserved verbatim for `constraint_origin: derived` nodes.
3. Confirm `CL-R9-imposed` is added as a new, distinct rule with its own rule ID.
4. Confirm VERIFY logic branches correctly on `constraint_origin` value.
5. Confirm no axiom (AX-1, AX-2, AX-3) is violated by the combined changeset.
6. Confirm version increment: `4.0` → `4.1` (minor, non-breaking).

## PR Instructions

- PR title format: `fix(CL): resolve ISSUE-002 — add constraint_origin field`
- PR description must cite the endorsed resolution strategy (Option B) from
  `DDR_v4_Issue-002.md` and enumerate every modified YAML node by path.
- Do not squash commits; preserve the atomic change history.

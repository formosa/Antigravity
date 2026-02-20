---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/tier_hierarchy.md
  - concepts/agent_registry.md
related:
  - patterns/worked_example_feature.md
  - protocols/traceability_chain.md
agents:
  - ddr_orchestrator
---

# Workflow: Document New Feature

> **Scope**: End-to-end procedure for documenting a new feature through all DDR tiers.
>
> **Excludes**: Individual tag authoring rules; validation details (see tier-specific sources).

## Summary

This workflow guides the complete documentation of a new feature from business requirements (BRD) through implementation stubs (ISP), ensuring full traceability and manifest synchronization.

## Prerequisites

- Feature description from stakeholder
- Access to existing DDR documentation
- Understanding of the 7-tier hierarchy

## Procedure

### Step 1: Gather Requirements

Interview user for business context. Identify ROI, strategic objectives, and success metrics.

### Step 2: Create BRD

Generate Business Requirement Tags with measurable metrics. No technology references.

### Step 3: Derive Constraints

Define NFRs — performance targets, resource limits, SLAs. All values must be numeric.

### Step 4: Create NFR

Generate Non-Functional Requirement Tags citing BRD parents.

### Step 5: Specify Behavior

Define user-facing FSD Tags describing system capabilities. No implementation details.

### Step 6: Design Architecture

Select SAD Patterns & Components. Cite FSD and/or NFR parents.

### Step 7: Define Contracts

Create ICD Schemas (JSON/YAML). Cite SAD parents.

### Step 8: Blueprint Components

Design TDD Classes & Methods. Cite SAD and ICD parents.

### Step 9: Generate Stubs

Create ISP Traceable Code Stubs with NumPy docstrings. Cite TDD parents.

### Step 10: Validate Traceability

Run full chain audit via `@traceability_auditor`. All ISP tags must trace to BRD root.

### Step 11: Update Manifests

Invoke `@manifest_manager` to synchronize reconciliation data.

### Step 12: Present Summary

Report all created artifacts with traceability status.

## Outcomes

| Result     | Condition                | Next Action              |
| :--------- | :----------------------- | :----------------------- |
| Complete   | All 12 steps pass        | Feature documented       |
| Blocked    | Traceability audit fails | Fix orphans, re-validate |
| Incomplete | Missing tier artifacts   | Return to relevant step  |

---

## References

- `concepts/tier_hierarchy.md` — Tier structure
- `patterns/worked_example_feature.md` — Complete worked example
- `protocols/traceability_chain.md` — Chain validation
- Source: `.agent/assets/documentation_system.md` §27.5.1 Workflow: Document New Feature
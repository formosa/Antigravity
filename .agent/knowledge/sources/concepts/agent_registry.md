---
archetype: concept
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
related:
  - patterns/evaluation_framework.md
  - protocols/traceability_chain.md
agents:
  - ddr_orchestrator
  - traceability_auditor
  - manifest_manager
  - antipattern_scanner
---

# Agent Registry

> **Scope**: Canonical registry of all DDR agent handles and their operational roles.
>
> **Excludes**: Agent implementation details; evaluation metrics (see `evaluation_framework.md`).

## Summary

The DDR system operates through specialized agents, each responsible for a distinct domain. Agents are divided into Core Agents (system-wide operations) and Tier Specialists (tier-specific authoring and validation).

## Definition

The **Agent Registry** is the authoritative lookup for all DDR agent handles, their roles, required context, and routing rules.

## Characteristics

### Core Agents

| Handle                  | Role                                                      | Context                        |
| :---------------------- | :-------------------------------------------------------- | :----------------------------- |
| `@ddr_orchestrator`     | System coordinator, tier classification, and routing.     | Docs Context, Rules            |
| `@traceability_auditor` | Cross-tier validation, orphan detection, cycle detection. | Full Graph, Validation Rules   |
| `@manifest_manager`     | Managing reconciliation manifests and integrity status.   | Manifests, File System         |
| `@antipattern_scanner`  | Detecting structural violations (e.g., tech in BRD).      | Regex Rules, Anti-Pattern List |

### Tier Specialists

| Handle               | Tier | Focus                                                            |
| :------------------- | :--- | :--------------------------------------------------------------- |
| `@brd_strategist`    | BRD  | Business alignment, ROI, strategic objectives (No tech details). |
| `@nfr_enforcer`      | NFR  | Quantifiable constraints, SLAs, hardware limits.                 |
| `@fsd_analyst`       | FSD  | User flows, behavior specifications, feature definitions.        |
| `@sad_architect`     | SAD  | System topology, design patterns, component selection.           |
| `@icd_dataengineer`  | ICD  | Data schemas (JSON/YAML), API contracts.                         |
| `@tdd_designer`      | TDD  | Class/component blueprints, method signatures.                   |
| `@isp_codegenerator` | ISP  | Implementation stubs, PySide6/ZMQ code generation.               |

## Context

- **Total Agents**: 11 (4 Core + 7 Tier Specialists)
- **Routing**: `@ddr_orchestrator` classifies input and routes to the appropriate Tier Specialist.
- **Validation**: `@traceability_auditor` operates across all tiers.

---

## References

- `concepts/tier_hierarchy.md` — Tier structure
- `patterns/evaluation_framework.md` — Agent evaluation metrics
- `protocols/traceability_chain.md` — Chain validation
- Source: `.agent/assets/documentation_system.md` §27.3.1–27.3.4 Route to Specialist
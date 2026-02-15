---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-13
updated: 2026-02-13
requires:
  - concepts/agent_registry.md
  - concepts/tier_hierarchy.md
related:
  - protocols/traceability_chain.md
  - constraints/isp_stub_only.md
  - constraints/isp_numpy_docstrings.md
---

# Evaluation Framework

> **Scope**: Standard evaluation metrics for DDR agent performance validation.
>
> **Excludes**: Agent implementation; test execution infrastructure.

## Summary

The Evaluation Framework defines quantitative pass/fail metrics for each DDR core agent. These evaluations ensure classification accuracy, traceability completeness, anti-pattern detection, stub purity, and docstring compliance.

## Structure

### Classification Accuracy

| Field | Value |
| :------ | :------ |
| **Target** | `@ddr_orchestrator` |
| **Metric** | Correct tier assignment vs Ground Truth |
| **Pass** | >95% accuracy |

### Traceability Completeness

| Field | Value |
| :------ | :------ |
| **Target** | `@traceability_auditor` |
| **Metric** | All ISP tags trace to BRD root |
| **Pass** | 100% (No orphans allowed) |

### Anti-Pattern Detection

| Field | Value |
| :------ | :------ |
| **Target** | `@antipattern_scanner` |
| **Metric** | Zero violations of "Technology in BRD" rules |
| **Pass** | 0 False Negatives |

### Stub Purity

| Field | Value |
| :------ | :------ |
| **Target** | `@isp_codegenerator` |
| **Metric** | `violations_per_stub` (Logic > `pass`) |
| **Pass** | 0 (Zero tolerance for logic in stubs) |

### Docstring Completeness

| Field | Value |
| :------ | :------ |
| **Target** | `@isp_codegenerator` |
| **Metric** | Presence of Implements/References sections |
| **Pass** | 100% compliance |

## Anti-Patterns

- Evaluating agents on subjective criteria (e.g., "good documentation")
- Using pass/fail without quantitative thresholds
- Skipping stub purity checks for "simple" stubs

---

## References

- `concepts/agent_registry.md` — Agent definitions
- `constraints/isp_stub_only.md` — Stub purity constraint
- `constraints/isp_numpy_docstrings.md` — Docstring format
- Source: `documentation_system.md` §27.6 Evaluation Framework

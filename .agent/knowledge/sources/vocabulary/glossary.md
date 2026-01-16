---
archetype: vocabulary
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires: []
related: []
---

# Glossary

> **Scope**: Normative terminology for all DDR documentation and agent operations.
>
> **Excludes**: Implementation-specific technical terms not used across tiers.

## Summary

The DDR controlled vocabulary prevents semantic drift and synonym hallucination by LLMs. All nouns in documentation must validate against this glossary. Non-compliant terms are validation errors.

## Terms

| Term | Definition | Usage | Avoid |
|:-----|:-----------|:------|:------|
| **Core Process** | The central orchestrator using ZeroMQ ROUTER pattern | "Core Process routes messages" | "manager", "controller", "hub" |
| **UI Process** | PySide6-based user interaction handler | "UI Process renders interface" | "frontend", "GUI service" |
| **Runtime Process** | GPU-optimized inference engine | "Runtime Process executes model" | "model server", "inference server" |
| **Audio Process** | Real-time audio I/O with WWD and VAD | "Audio Process captures wake word" | "voice handler", "audio service" |
| **LogServer** | Centralized logging using PULL socket | "LogServer aggregates logs" | "log manager", "log collector" |
| **Tool** | Modular capability extending Core Process | "Tool provides weather lookup" | "plugin", "extension", "module" |
| **Routine** | Multi-step Tool sequence with context | "Routine executes morning briefing" | "workflow", "script", "procedure" |
| **HSM** | Hierarchical State Machine via transitions library | "HSM transitions to active state" | "state machine", "FSM" |
| **Service** | Any process communicating via ZeroMQ sockets | "Service binds to endpoint" | "server", "daemon", "worker" |

## Abbreviations

| Abbrev | Expansion | Context |
|:-------|:----------|:--------|
| BRD | Business Requirements Document | Tier 1: Strategic justification |
| NFR | Non-Functional Requirements | Tier 2: Constraints and targets |
| FSD | Feature Specifications Document | Tier 3: System capabilities |
| SAD | System Architecture Document | Tier 4: Structure and patterns |
| ICD | Interface & Contract Definitions | Tier 5: Data schemas |
| TDD | Technical Design Document | Tier 6: Component blueprints |
| ISP | Implementation Stubs & Prompts | Tier 7: Code skeletons |
| DDR | Development Documentation Roadmap | The complete documentation system |
| WWD | Wake Word Detection | Audio trigger system |
| VAD | Voice Activity Detection | Speech boundary detection |
| IPC | Inter-Process Communication | ZeroMQ messaging |
| HSM | Hierarchical State Machine | State management pattern |

## Enforcement

When validating documentation:
1. Scan all nouns related to architecture/components
2. Verify each term exists in this glossary
3. Flag non-compliant terms as errors with suggested corrections

**Example Error:**
```
✗ ERROR: Term "Model Server" not in glossary.
  → Did you mean "Runtime Process"?
```

---

## References

- Source: `ddr_meta_standard.txt` §5. Controlled Vocabulary & Glossary

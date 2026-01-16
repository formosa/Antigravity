---
archetype: context
status: active
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
project: maggie
scope: vocabulary
---

# Project Glossary

> **Scope**: Terminology specific to the Maggie application.
>
> **Excludes**: DDR framework terms (see `sources/vocabulary/glossary.md`).

## Summary

Project-specific controlled vocabulary for Maggie AI Assistant. Supplements DDR glossary for all documentation tiers.

## Terms

| Term | Definition | Usage | Avoid |
|:-----|:-----------|:------|:------|
| **Core Process** | Central orchestrator using ZeroMQ ROUTER pattern | "Core Process routes messages" | "manager", "controller", "hub" |
| **UI Process** | PySide6-based user interaction handler | "UI Process renders interface" | "frontend", "GUI service" |
| **Runtime Process** | GPU-optimized inference engine | "Runtime Process executes model" | "model server", "inference server" |
| **Audio Process** | Real-time audio I/O with WWD and VAD | "Audio Process captures wake word" | "voice handler", "audio service" |
| **LogServer** | Centralized logging using PULL socket | "LogServer aggregates logs" | "log manager", "log collector" |
| **Tool** | Modular capability extending Core Process | "Tool provides weather lookup" | "plugin", "extension", "module" |
| **Routine** | Multi-step Tool sequence with context | "Routine executes morning briefing" | "workflow", "script", "procedure" |
| **Service** | Any process communicating via ZeroMQ sockets | "Service binds to endpoint" | "server", "daemon", "worker" |

## Abbreviations

| Abbrev | Expansion | Context |
|:-------|:----------|:--------|
| WWD | Wake Word Detection | Audio trigger system |
| VAD | Voice Activity Detection | Speech boundary detection |
| IPC | Inter-Process Communication | ZeroMQ messaging |
| HSM | Hierarchical State Machine | State management (transitions library) |

---

## References

- DDR glossary: `../sources/vocabulary/glossary.md`

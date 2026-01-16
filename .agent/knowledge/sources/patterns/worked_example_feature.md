---
archetype: pattern
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/tier_hierarchy.md
  - concepts/information_flow.md
related:
  - patterns/worked_example_classification.md
---

# Worked Example: Feature

> **Scope**: End-to-end demonstration of documenting a feature across all seven DDR tiers.
>
> **Excludes**: Individual tier definitions; classification process.

## Summary

This worked example traces a single feature—centralized logging—from business objective (BRD) through implementation stub (ISP), demonstrating proper tier content, citations, and traceability.

## Feature: Centralized Logging

A complete correlated logging system for debugging multi-process applications.

---

## Tier 1: BRD (Business Requirements)

**Question**: Why do we need this?

```rst
.. brd:: Observability: Enable comprehensive debugging through correlated, centralized logging.
   :id: BRD-3.5
```

**Key characteristics**:
- Technology-agnostic (no mention of loguru, files, etc.)
- Business value focused (debugging capability)
- Measurable impact (debugging efficiency)

---

## Tier 2: NFR (Non-Functional Requirements)

**Question**: What are the limits?

```rst
.. nfr:: Log Management Constraints
   :id: NFR-7
   :links: BRD-3.5

.. nfr:: Logs must be aggregated to single unified file.
   :id: NFR-7.1
   :links: NFR-7

.. nfr:: Automatic rotation every 50MB.
   :id: NFR-7.2
   :links: NFR-7

.. nfr:: Retention period: 30 days minimum.
   :id: NFR-7.3
   :links: NFR-7

.. nfr:: Log correlation via request_id in every message.
   :id: NFR-7.4
   :links: NFR-7
```

**Key characteristics**:
- Numeric constraints (50MB, 30 days)
- Cites BRD justification
- Defines measurable requirements

---

## Tier 3: FSD (Feature Specifications)

**Question**: What does it do?

```rst
.. fsd:: Centralized Logging System
   :id: FSD-6
   :links: BRD-3.5, NFR-7

.. fsd:: All processes push logs to central LogServer.
   :id: FSD-6.1
   :links: FSD-6

.. fsd:: Logs include structured metadata (source, level, timestamp).
   :id: FSD-6.2
   :links: FSD-6

.. fsd:: Request correlation via request_id propagation.
   :id: FSD-6.3
   :links: FSD-6, NFR-7.4
```

**Key characteristics**:
- Describes behavior without implementation
- Cites BRD and NFR
- User/operator focused

---

## Tier 4: SAD (System Architecture)

**Question**: How is it organized?

```rst
.. sad:: Logging Architecture
   :id: SAD-6
   :links: FSD-6

.. sad:: Decoupled Sink: LogServer (PULL) receives from all processes (PUSH).
   :id: SAD-6.1
   :links: SAD-6, FSD-6.1

.. sad:: Non-Blocking: PUSH socket with HWM prevents sender blocking.
   :id: SAD-6.2
   :links: SAD-6, NFR-5.1
```

**ASCII Diagram** (required for SAD):
```
+-------------+     +-------------+     +---------------+
| Core (PUSH) |---->|             |<----| Runtime (PUSH)|
+-------------+     |  LogServer  |     +---------------+
+-------------+     |   (PULL)    |     +-------------+
| UI (PUSH)   |---->|             |<----| Audio (PUSH)|
+-------------+     +-------------+     +-------------+
                           |
                           v
                    [unified.log]
```

---

## Tier 5: ICD (Interface Contracts)

**Question**: What are the data shapes?

```rst
.. icd:: Log Frame Structure
   :id: ICD-6
   :links: SAD-6.1

.. icd:: Log Metadata Schema (JSON)
   :id: ICD-6.1
   :links: ICD-6, FSD-6.2

   .. code-block:: json

      {
        "source": "Core|UI|Runtime|Audio",
        "level": "DEBUG|INFO|WARNING|ERROR",
        "timestamp": "ISO-8601",
        "request_id": "uuid-v4-or-null"
      }

.. icd:: Log Configuration (YAML)
   :id: ICD-6.2
   :links: ICD-6, NFR-7.2

   .. code-block:: yaml

      logging:
        path: "logs/unified.log"
        rotation_mb: 50
        retention_days: 30
        format: json
```

---

## Tier 6: TDD (Technical Design)

**Question**: What classes exist?

```rst
.. tdd:: Component: LogServer
   :id: TDD-6
   :links: SAD-6.1, ICD-6

.. tdd:: Class Name: LogServer
   :id: TDD-6.1
   :links: TDD-6

.. tdd:: Dependencies: zmq, loguru, yaml
   :id: TDD-6.2
   :links: TDD-6

.. tdd:: Socket: Bind PULL to logging.pull_bind
   :id: TDD-6.3
   :links: TDD-6, ICD-6.2

.. tdd:: Method: run() - Main receive loop
   :id: TDD-6.4
   :links: TDD-6

.. tdd:: Method: write_log(frame) - Process and persist
   :id: TDD-6.5
   :links: TDD-6, ICD-6.1
```

---

## Tier 7: ISP (Implementation Stubs)

**Question**: What's the code skeleton?

```rst
.. isp:: Stub: LogServer
   :id: ISP-6
   :links: TDD-6

   .. code-block:: python

      import zmq
      from loguru import logger

      class LogServer:
          """
          Centralized logging aggregator using ZMQ PULL socket.

          Ref: |TDD-6|, |FSD-6|

          Attributes
          ----------
          socket : zmq.Socket
              PULL socket receiving log frames.
          """

          def __init__(self, config_path: str):
              """
              Initialize PULL socket and loguru configuration.

              Implements: |TDD-6.3|
              Requirements: |NFR-7.2|
              """
              pass

          def run(self) -> None:
              """
              Main loop: receive frames, write to unified log.

              Implements: |TDD-6.4|
              """
              pass

          def write_log(self, frame: list) -> None:
              """
              Parse frame metadata and write structured log entry.

              Implements: |TDD-6.5|
              Requirements: |FSD-6.2|
              """
              pass
```

---

## Traceability Chain

```
ISP-6 → TDD-6 → SAD-6.1 → FSD-6 → NFR-7 → BRD-3.5
              ↘ ICD-6 ↗
```

Every implementation decision traces back to business value.

---

## References

- `concepts/tier_hierarchy.md` — Tier structure
- `concepts/information_flow.md` — Citation flow
- `patterns/worked_example_classification.md` — Classification process
- Source: `20. Advanced Integration Patterns.md`

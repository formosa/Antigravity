---
type: rule
name: "BRD Technology Agnostic"
globs:
  - "docs/01_brd/*.rst"
priority: 80
trigger:
  - "technology"
  - "implementation"
  - "library"
severity: mandatory
description: "BRD content must not contain technology-specific terms or implementation details."
---
# BRD Technology Agnostic Rule

## Rule Statement

**BRD: Content MUST NOT contain technology-specific terms, implementation details, or solution-prescriptive language.**

## Detection

| Pattern | Examples |
|:--------|:---------|
| Programming languages | Python, JavaScript, React |
| Libraries/frameworks | ZeroMQ, PySide6, pvporcupine |
| Hardware specifics | RTX 3080, AMD Ryzen, CUDA |
| Protocols | TCP, MQTT, REST API |
| File formats | JSON, YAML, Protobuf |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Technology term in BRD | ERROR | Abstract to business language |
| Implementation detail | ERROR | Move to appropriate tier |
| Solution prescription | WARNING | Reframe as objective |

## Forbidden Terms

| Category | Terms |
|:---------|:------|
| Languages | Python, JavaScript, React, Go |
| Libraries | ZeroMQ, ONNX, PySide6, pvporcupine |
| Infrastructure | Docker, PostgreSQL, Redis, SQLite |
| Hardware | GPU, CUDA, RTX 3080, CPU core, RAM |
| Protocols | socket, thread, API, REST, GraphQL |

## Enforcement Protocol

1. Scan BRD content for forbidden terms
2. Any detection → ERROR
3. Abstract to business capability

## Examples

### ✅ Correct

.. code-block:: rst

   .. brd:: Enable hands-free voice interaction for accessibility.
      :id: BRD-5.7

### ❌ Incorrect

.. code-block:: rst

   .. brd:: Wake word detection using pvporcupine.
      :id: BRD-5.7

**Why**: "pvporcupine" is a specific library.

## References

- Knowledge: `constraints/brd_technology_agnostic.md`
- Source: DDR Meta-Standard §2.1

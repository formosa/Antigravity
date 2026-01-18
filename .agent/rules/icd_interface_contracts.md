---
type: rule
name: "ICD Interface Contracts"
globs:
  - "docs/05_icd/*.rst"
priority: 80
trigger:
  - "schema"
  - "payload"
  - "contract"
  - "type"
severity: mandatory
description: "ICD tags must specify language-agnostic data shapes using PascalCase for schemas and camelCase for properties."
---
# ICD Interface Contracts Rule

## Rule Statement
**ICD Content MUST specify language-agnostic data shapes (YAML/JSON) using PascalCase for schemas and camelCase for properties. PROHIBIT implementation-specific symbols.**

## Detection
| Pattern | Examples |
|:--------|:---------|
| Language implementation | `Dict[str, Any]`, `struct Message` |
| Library symbols | `ZMQ_ROUTER`, `PySide6.QtCore.QPoint` |
| Wrong casing | `my_property` (snake_case), `schema_name` (snake_case) |
| Missing schema | Description without concrete format |

## Enforcement
| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Implementation symbol | ERROR | Use generic data type (string, int, object) |
| Wrong casing | ERROR | Convert to camelCase/PascalCase |
| No concrete schema | ERROR | Add YAML or JSON schema block |

## Forbidden Terms
| Category | Terms |
|:---------|:------|
| Types | Dict, List, Tuple (Pythonic), struct, class, void* |
| Libraries | ZeroMQ, ZMQ, ONNX, PySide6 |
| Protocols | TCP Socket, ThreadID (implementation level) |

## Enforcement Protocol
1. **Scan** ICD definitions for code-block schemas (YAML/JSON).
2. **Verify** `PascalCase` for Schema Names (e.g., `MessageHeader`).
3. **Verify** `camelCase` for properties (e.g., `requestId`).
4. **Block** library-specific constants or types.

## Examples

### ✅ Correct
```rst
.. icd:: AudioPacket metadata schema.

   .. code-block:: json

      {
        "packetId": "uuid",
        "timestamp": "iso8601",
        "sampleRate": 16000
      }
```

### ❌ Incorrect
```rst
.. icd:: AudioPacket metadata dictionary in Python.

   .. code-block:: python

      packet = {"id": 1, "time": "now"}
```
**Why**: Uses Python-specific implementation and snake_case properties.

## References

- Knowledge: `concepts/tier_icd.md`
- Source: DDR Meta-Standard §2.5

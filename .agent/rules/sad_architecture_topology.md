---
type: rule
name: "SAD Architecture Topology"
globs:
  - "docs/04_sad/*.rst"
priority: 80
trigger:
  - "structure"
  - "topology"
  - "boundary"
  - "architecture"
severity: mandatory
description: "SAD sections must define the architectural pattern and include at least one ASCII topology diagram."
---
# SAD Architecture Topology Rule

## Rule Statement
**SAD Sections MUST define the high-level architectural pattern and include mandatory ASCII topology diagrams using `+---+` and `<--->` notation.**

## Detection
| Pattern | Examples |
|:--------|:---------|
| Missing diagram | Section with text only |
| Non-standard diagram | Mermaid or image links (without ASCII fallback) |
| Implementation detail | Step-by-step logic in SAD |
| Granular logic | "If message type is X, then Y" |

## Enforcement
| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Missing diagram | ERROR | Add ASCII topology diagram |
| Implementation detail | ERROR | Move to TDD or ISP tier |
| No pattern definition | WARNING | Explicitly name the architecture pattern |

## Forbidden Terms
| Category | Terms |
|:---------|:------|
| Logic | if, else, while, return, calculate |
| Code | Python, class, method, function |
| Granularity | line 45, variable name |

## Enforcement Protocol
1. **Verify** section explicitly names an architectural pattern (e.g., Hub-and-Spoke, MVC).
2. **Scan** for `+---+` notation indicating an ASCII diagram.
3. **Ensure** diagram illustrates component boundaries and communication flow.
4. **Block** implementation-level logic.

## Examples

### ✅ Correct
```rst
.. sad:: The system uses a Hub-and-Spoke topology for message distribution.

   +---------------+          +----------------+          +---------------+
   |   Producer    | <------> |      Hub       | <------> |   Consumer    |
   +---------------+          +----------------+          +---------------+
```

### ❌ Incorrect
```rst
.. sad:: The components communicate via ZeroMQ sockets in a circular pattern.
```
**Why**: Missing mandatory ASCII topology diagram.

## References

- Knowledge: `concepts/tier_sad.md`
- Source: DDR Meta-Standard §2.4

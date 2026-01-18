---
type: rule
name: "TDD Structural Blueprints"
globs:
  - "docs/06_tdd/*.rst"
priority: 80
trigger:
  - "logic"
  - "flow"
  - "if"
  - "loop"
  - "calculation"
  - "implementation"
severity: mandatory
description: "TDD content must define structure (classes, signatures) but PROHIBIT implementation logic."
---
# TDD Structural Blueprints Rule

## Rule Statement
**TDD Content MUST define WHAT exists (classes, modules, signatures) and HOW it's wired, but PROHIBIT implementation logic (if/else, loops, calculations).**

## Detection
| Pattern | Examples |
|:--------|:---------|
| Control flow leakage | `if response is valid`, `for item in items` |
| Algorithmic logic | `calculate_hash()`, `logic to determine X` |
| Multi-line bodies | Complex method implementations |
| Business logic | "Process the payment if balance > 0" |

## Enforcement
| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Logic Leakage | ERROR | Move logic to ISP tier; use `...`, `pass`, or `@abstractmethod` |
| Missing structure | ERROR | Add class/module definitions |
| State mutation logic | ERROR | Describe state shape, not mutation steps |

## Forbidden Terms
| Category | Terms |
|:---------|:------|
| Control Flow | if, else, for, while, switch, case |
| Logic | calculate, determine, decide, process (verb) |
| Detail | line by line, step by step |

## Enforcement Protocol
1. **Scan** TDD content for method signatures and class structures.
2. **Verify** method bodies use `...`, `pass` or `@abstractmethod`.
3. **Block** any control flow keywords (`if`, `for`).
4. **Ensure** wiring (dependencies/imports) is documented without behavioral steps.

## Examples

### ✅ Correct
```rst
.. tdd:: CoreController class signature.

   .. code-block:: python

      class CoreController:
          def handle_event(self, event: Event) -> None: ...
```

### ❌ Incorrect
```rst
.. tdd:: CoreController handles events by checking the type.

   .. code-block:: python

      def handle_event(self, event):
          if event.type == "voice":
              self.process_voice(event)
```
**Why**: Contains implementation logic (`if` statement).

## References

- Knowledge: `concepts/tier_tdd.md`
- Source: DDR Meta-Standard §2.6

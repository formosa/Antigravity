---
type: rule
priority: 80
trigger:
  - "algorithm"
  - "code"
  - "class"
  - "function"
  - "variable"
severity: mandatory
description: "FSD tags must describe WHAT the system does from a user perspective and prohibit implementation details."
---
# FSD Behavioral Specs Rule

## Rule Statement
**FSD Content MUST describe WHAT the system does from a user/stakeholder perspective and PROHIBIT technical implementation or solution design details (e.g., class names, functions, variables).**

## Detection
| Pattern | Examples |
|:--------|:---------|
| Implementation leakage | "The CoreController class", "The SQL table" |
| Low-level algorithms | "Sort using a quicksort algorithm", "Iterate over the array" |
| Code blocks | Python, JavaScript, CSS blocks |
| Internal data structures | "Dictionary with request_id as key" |

## Enforcement
| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Implementation detail | ERROR | Reframe as user-facing behavior |
| Class/Function names | ERROR | Use descriptive business terms |
| Technical design | ERROR | Move to TDD or SAD tier |

## Forbidden Terms
| Category | Terms |
|:---------|:------|
| Programming | Python, class, function, method, loop, variable |
| Persistence | SQL, Database, Table, Column, Index |
| Structure | Dictionary, List, Array, Pointer |
| Logic | Quicksort, regex, hash, boolean |

## Enforcement Protocol
1. **Scan** FSD content for technical implementation terminology.
2. **Verify** content is framed from a user or system-as-a-black-box perspective.
3. **If** technical leakage detected → **ERROR**.
4. **Suggest** a behavioral alternative (e.g., "The system shall validate input" vs "The InputValidator class checks").

## Examples

### ✅ Correct
```rst
.. fsd:: The system shall provide a visual confirmation when the voice command is recognized.
   :id: FSD-1.4
```

### ❌ Incorrect
```rst
.. fsd:: The UIHandler class calls the play_animation() function.
   :id: FSD-1.4
```
**Why**: References internal class names and functions.

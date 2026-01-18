---
type: rule
name: "Immutable Assets Protection"
globs:
  - ".agent/assets/**/*"
priority: 100
trigger:
  - "edit"
  - "update"
  - "modify"
  - "delete"
  - "overwrite"
severity: mandatory
description: "The .agent/assets/ directory contains strict project standards and reference schemas. These files are READ-ONLY. You are strictly forbidden from editing, modifying, overwriting, or deleting any file in this directory. EXCEPTION: If a user request specifically requires changes to these files, you must HALT execution, list the specific files to be changed, and explicitly ask the user for approval before proceeding."
---

# Immutable Assets Protection

## Rule Statement

**Files in `.agent/assets/` are READ-ONLY reference schemas. Modifications require explicit user approval.**

## Detection

| Pattern | Location |
|:--------|:---------|
| Edit command targeting `.agent/assets/*` | Any agent tool call |
| Overwrite request | File write operations |

## Enforcement

| Violation | Severity | Resolution |
|:----------|:--------:|:-----------|
| Unauthorized edit | ERROR | Halt and request user approval |
| Deletion attempt | ERROR | Block and report |

## Enforcement Protocol

1. Detect any file operation targeting `.agent/assets/`
2. HALT execution immediately
3. List specific files to be changed
4. Request explicit user approval
5. Only proceed with documented approval

## Examples

### ✅ Correct

```
Agent: "I need to modify antigravity_types.d.ts. May I proceed?"
User: "Yes, approved."
Agent: [proceeds with modification]
```

### ❌ Incorrect

```
Agent: [silently modifies antigravity_types.d.ts]
```

**Why**: Protected files require explicit approval before modification.

---
type: rule
name: dev-protected-files
activation: always_on
priority: 100
severity: mandatory
description: "Protects .agent/assets/ directory from unauthorized modifications."
---
# Immutable Assets Protection

## Rule Statement

**Files in `.agent/assets/` are READ-ONLY reference schemas. Modifications require explicit user approval.**

## Detection

| Pattern                                  | Location              |
| :--------------------------------------- | :-------------------- |
| Edit command targeting `.agent/assets/*` | Any agent tool call   |
| Overwrite request                        | File write operations |

## Enforcement

| Violation         | Severity   | Resolution                     |
| :---------------- | :--------: | :----------------------------- |
| Unauthorized edit | ERROR      | Halt and request user approval |
| Deletion attempt  | ERROR      | Block and report               |

## Enforcement Protocol

1. Detect any file operation targeting `.agent/assets/`
2. HALT execution immediately
3. List specific files to be changed
4. Request explicit user approval
5. Only proceed with documented approval

## Examples

### ✅ Correct

```plaintext
Agent: "I need to modify security-policy.d.ts. May I proceed?"
User: "Yes, approved."
Agent: [proceeds with modification]
```

### ❌ Incorrect

```plaintext
Agent: [silently modifies rule.d.ts]
```

**Why**: Protected files require explicit approval before modification.

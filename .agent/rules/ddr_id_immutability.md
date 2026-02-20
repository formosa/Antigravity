---
type: rule
name: ddr_id_immutability
activation: always_on
priority: 100
severity: mandatory
---
# Antigravity Agent Rules — DDR Tag ID Immutability

## Rule Statement

**Once assigned, a DDR Tag ID (e.g., BRD-1.2, TDD-4.5) MUST NEVER BE CHANGED.**

## Scope

This rule applies to all files within the `docs/` directory ending in `.rst`.

## Protocol

1. **Check existence**: Before creating a new tag, verify the ID is not already in use in `needs.json` or any `.rst` file.
2. **Deletion**: If a requirement is no longer needed, the tag may be DELETED, but the ID MUST NOT be reused for a different requirement.
3. **Refactoring**: If a requirement is split, the original ID should remain with the most representative chunk, and a new ID assigned to the others.
4. **Modification**: Content within a tag (rationale, implementation details) may be updated, but the ID must remain constant.

## Enforcement Level

- **Violation**: Changing an ID
- **Severity**: FATAL
- **Action**: Abort operation and notify user of traceability breach.

## References

- Knowledge: `protocols/id_allocation.md`
- Source: DDR Meta-Standard §1.4
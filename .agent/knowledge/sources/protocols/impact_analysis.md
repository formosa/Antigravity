---
archetype: protocol
status: draft
version: 1.0.0
created: 2026-01-16
updated: 2026-01-16
requires:
  - vocabulary/glossary.md
  - concepts/information_flow.md
  - protocols/traceability_chain.md
related:
  - protocols/reconciliation_dirty_flag.md
agents:
  - traceability_auditor
---

# Impact Analysis

> **Scope**: Protocol for determining downstream effects when a parent tag is modified.
>
> **Excludes**: Dirty flag handling; inventory synchronization.

## Summary

When a parent tag is modified, all downstream citations are potentially affected. Impact analysis identifies all tags that cite the modified parent (directly or transitively), enabling targeted review and reconciliation.

## Prerequisites

- Identification of modified parent tag
- Access to needs.json or citation graph
- Understanding of cascade propagation

## Procedure

### Step 1: Identify Modified Tag

Record the tag being changed and the nature of modification:

| Modification Type | Impact Level |
|:------------------|:-------------|
| Content change | Review all citing children |
| ID change | CRITICAL - all citations break |
| Deletion | All citing children become orphans |
| Scope expansion | May require new children |
| Scope reduction | May orphan some children |

### Step 2: Build Downstream Graph

Find all tags that cite the modified parent (directly):

```
Modified: BRD-5.2 "Privacy-preserving operation"

Direct Citations (Level 1):
├── NFR-3 (cites BRD-5.2)
├── NFR-4 (cites BRD-5.2)
└── FSD-1.3 (cites BRD-5.2)
```

### Step 3: Expand Transitively

For each Level 1 child, find its citations (Level 2), and continue:

```
Level 1: NFR-4
├── Level 2: FSD-1.3 (cites NFR-4)
│   └── Level 3: SAD-2 (cites FSD-1.3)
│       └── Level 4: TDD-1 (cites SAD-2)
│           └── Level 5: ISP-1 (cites TDD-1)
```

### Step 4: Generate Impact Report

| Tag | Level | Path from Modified | Action Required |
|:----|:-----:|:-------------------|:----------------|
| NFR-4 | 1 | BRD-5.2 → NFR-4 | Review for consistency |
| FSD-1.3 | 2 | BRD-5.2 → NFR-4 → FSD-1.3 | Verify still valid |
| SAD-2 | 3 | ... → FSD-1.3 → SAD-2 | Check architecture |
| TDD-1 | 4 | ... → SAD-2 → TDD-1 | Review design |
| ISP-1 | 5 | ... → TDD-1 → ISP-1 | Regenerate stub |

### Step 5: Flag Affected Sections

For each affected tier, set dirty flag in reconciliation manifest:

```rst
.. reconciliation_manifest:
   :section_id: fsd-root
   :integrity_status: "DIRTY"
   :pending_items: [
     {
       "target_tag": "FSD-1.3",
       "source_trigger": "BRD-5.2 modified",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Parent requirement changed"
     }
   ]
```

## Outcomes

| Result | Condition | Next Action |
|:-------|:----------|:------------|
| No citations | Parent has no children | No impact |
| Local impact | Only direct children affected | Review Level 1 only |
| Cascade impact | Multiple levels affected | Full reconciliation pass |
| Critical impact | ID changed/deleted | Emergency citation repair |

---

## References

- `concepts/information_flow.md` — Cascade principles
- `protocols/reconciliation_dirty_flag.md` — Flagging mechanism
- Source: `ddr_meta_standard.txt` §4.3 Integrity Maintenance Rules

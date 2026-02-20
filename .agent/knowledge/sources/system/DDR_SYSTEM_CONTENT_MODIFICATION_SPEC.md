---
title: "DDR System Content Modification Specification"
description: "Implementation-grade specification for normalizing DDR knowledge assets."
status: published
tags:
  - "DDR"
  - "Normalization"
  - "Specification"
last_updated: "2026-02-15"
---
# DDR System Content Modification Specification (Implementation-Grade)

Date: 2026-02-15
Audience: Agents implementing DDR knowledge-base normalization
Primary Scope: `.agent/knowledge/` (authoritative DDR source of truth)
Reference Basis: `.agent/assets/documentation_system.md`

---

## 0) How to Use This Document

This is a **content-level implementation specification** for agents. It enumerates **every known modification unit** required to normalize the current DDR knowledge assets into a maximally optimized, machine-validatable, low-ambiguity design.

For each modification unit, this document provides:

1. File path
2. Exact content segment requiring change (anchor/current)
3. Enhanced replacement segment
4. Rationale
5. Validation checks

If a listed anchor cannot be found exactly, agents MUST:

- stop that unit,
- run the validation commands in §6,
- record deviation in implementation notes,
- continue remaining units.

---

## 1) Canonical Design Decisions (Normative)

The implementation MUST enforce these system-wide decisions:

1. **Lifecycle status enum** is canonicalized to: `draft | review | active | deprecated`.
2. **Metadata path convention** is canonicalized to knowledge-root-relative notation:
   - `sources/...`
   - `context/...`
3. **Source citation convention** in body text uses explicit repo path:
   - `.agent/assets/documentation_system.md` + section reference.
4. **Index policy** is explicit: `_index.md` files are in-scope knowledge artifacts and include minimal frontmatter.
5. **Forward Reference** definition is corrected to align with DDR directionality:
   - invalid = citation from higher abstraction tier to lower abstraction tier.
6. **Agent anti-hallucination safeguards** are operationalized via deterministic validation gates (see §5 and §6).

---

## 2) Complete Modification Unit Catalog

## MU-001 — Root knowledge index frontmatter and governance banner

**File**: `.agent/knowledge/_index.md`

**Anchor to locate**:

```md
# Knowledge Base Index
```

**Replace file header with**:

```md
---
archetype: index
status: active
version: 1.1.0
created: 2026-01-16
updated: 2026-02-15
scope: knowledge-root
index_policy: in_scope_requires_frontmatter
path_convention: knowledge-root-relative
---

# Knowledge Base Index
```

**Rationale**: Removes index-governance ambiguity and makes root policy machine-readable.

**Validation**:

- frontmatter parse succeeds
- `archetype: index` allowed by metadata schema (MU-004 / MU-014)

---

## MU-002 — Sources index frontmatter and path convention declaration

**File**: `.agent/knowledge/sources/_index.md`

**Anchor to locate**:

```md
# Knowledge Source Index
```

**Replace file header with**:

```md
---
archetype: index
status: active
version: 1.1.0
created: 2026-01-16
updated: 2026-02-15
scope: sources-index
path_convention: knowledge-root-relative
---

# Knowledge Source Index
```

**Rationale**: Ensures indexes are validator-visible and explicit about path semantics.

**Validation**:

- frontmatter parse succeeds
- no schema exception needed for `_index.md`

---

## MU-003 — Context index frontmatter and project-alignment note

**File**: `.agent/knowledge/context/_index.md`

**Anchor to locate**:

```md
# Project Context Index
```

**Replace file header with**:

```md
---
archetype: index
status: active
version: 1.1.0
created: 2026-01-16
updated: 2026-02-15
scope: context-index
project: antigravity
context_mode: namespaced
---

# Project Context Index
```

**Add this section near the end (after Precedence)**:

```md
## Context Namespace Policy

Context files are project-scoped overlays and MUST declare their namespace.

- `context/glossary.md` is currently retained for Maggie terminology compatibility.
- Future contexts SHOULD split by namespace (e.g., `maggie_*`, `antigravity_*`) to avoid semantic bleed.
```

**Rationale**: Resolves repository/project identity ambiguity and introduces explicit context strategy.

**Validation**:

- section present exactly once
- index frontmatter valid

---

## MU-004 — Canonical template status enum, archetypes, and schema rules

**File**: `.agent/knowledge/sources/patterns/knowledge_source_template.md`

### MU-004A — Frontmatter status normalization

**Anchor**:

```md
status: validated
```

**Replace with**:

```md
status: active
```

### MU-004B — Universal template block enum correction

**Anchor block**:

```md
archetype: concept | protocol | constraint | pattern | vocabulary
status: active | review | validated
```

**Replace block with**:

```md
archetype: concept | protocol | constraint | pattern | vocabulary | context | index
status: draft | review | active | deprecated
schema_version: 1
```

### MU-004C — Required-fields table correction

**Anchor row**:

```md
| `status` | enum | One of: draft, review, validated |
```

**Replace row with**:

```md
| `status` | enum | One of: draft, review, active, deprecated |
```

### MU-004D — Add index scope policy section

**Insert section after “Frontmatter (Optional)”**:

```md
### Index File Policy (Normative)

`_index.md` files are first-class knowledge artifacts and MUST include frontmatter.

Minimum required fields for index files:
- `archetype: index`
- `status`
- `version`
- `created`
- `updated`
- `scope`
```

### MU-004E — Add path convention section

**Insert section after “Body (Required)”**:

```md
### Path Convention (Normative)

All `requires` and `related` entries MUST be written relative to `.agent/knowledge/` root.

Examples:
- `sources/vocabulary/glossary.md`
- `context/glossary.md`

Relative parent navigation (e.g., `../context/glossary.md`) MUST NOT be used.
```

**Rationale**: Removes internal contradictions in the canonical authoring pattern.

**Validation**:

- no remaining `validated` in status enum examples/tables
- schema_version appears in universal template
- index/path policy sections exist

---

## MU-005 — Vocabulary glossary normalization (status, forward reference, metadata path)

**File**: `.agent/knowledge/sources/vocabulary/glossary.md`

### MU-005A — Frontmatter status

**Anchor**:

```md
status: validated
```

**Replace with**:

```md
status: active
```

### MU-005B — `related` metadata path

**Anchor**:

```md
related:
  - ../context/glossary.md
```

**Replace with**:

```md
related:
  - context/glossary.md
```

### MU-005C — Forward Reference definition correction

**Anchor row**:

```md
| **Forward Reference** | Invalid citation where a lower tier cites a higher tier |
```

**Replace row with**:

```md
| **Forward Reference** | Invalid citation where a higher abstraction tier cites a lower abstraction tier (e.g., BRD citing SAD) |
```

### MU-005D — References section path normalization

**Anchor**:

```md
- Project glossary: `../context/glossary.md`
```

**Replace with**:

```md
- Project glossary: `context/glossary.md`
```

**Rationale**: Fixes semantic contradiction and normalizes metadata/reference paths.

**Validation**:

- no `../context/` in file
- forward-reference wording aligns with hierarchy docs

---

## MU-006 — Persona content strategy status normalization

**File**: `.agent/knowledge/sources/patterns/persona_content_strategy.md`

**Anchor**:

```md
status: validated
```

**Replace with**:

```md
status: active
```

**Rationale**: Aligns with canonical status lifecycle.

**Validation**:

- file status ∈ canonical enum

---

## MU-007 — Context glossary reference path normalization

**File**: `.agent/knowledge/context/glossary.md`

**Anchor**:

```md
- DDR glossary: `../sources/vocabulary/glossary.md`
```

**Replace with**:

```md
- DDR glossary: `sources/vocabulary/glossary.md`
```

**Rationale**: Enforces single path convention for cross-layer references.

**Validation**:

- no `../sources/` path remains in this file

---

## MU-008 — Classification decision tree source citation normalization

**File**: `.agent/knowledge/sources/protocols/classification_decision_tree.md`

**Anchor**:

```md
- Source: `4. Information Assessment & Classification Framework.md` §4.1
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §4 (Information Assessment & Classification Framework), §4.1
```

**Rationale**: Eliminates non-resolvable source title citation.

**Validation**:

- source line contains `.agent/assets/documentation_system.md`

---

## MU-009 — Classification scoring source citation normalization

**File**: `.agent/knowledge/sources/protocols/classification_scoring.md`

**Anchor**:

```md
- Source: `4. Information Assessment & Classification Framework.md` §4.2, §4.3
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §4 (Information Assessment & Classification Framework), §4.2, §4.3
```

**Rationale**: Same as MU-008.

**Validation**:

- source line contains `.agent/assets/documentation_system.md`

---

## MU-010 — Abstraction upward source citation normalization

**File**: `.agent/knowledge/sources/protocols/abstraction_upward.md`

**Anchor**:

```md
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.1
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §5 (Vertical Abstraction & Specification Protocols), §5.1
```

---

## MU-011 — Abstraction downward source citation normalization

**File**: `.agent/knowledge/sources/protocols/abstraction_downward.md`

**Anchor**:

```md
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.2
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §5 (Vertical Abstraction & Specification Protocols), §5.2
```

---

## MU-012 — Abstraction lateral source citation normalization

**File**: `.agent/knowledge/sources/protocols/abstraction_lateral.md`

**Anchor**:

```md
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.3
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §5 (Vertical Abstraction & Specification Protocols), §5.3
```

---

## MU-013 — Worked example citations normalization

### MU-013A

**File**: `.agent/knowledge/sources/patterns/worked_example_classification.md`

**Anchor**:

```md
- Source: `4. Information Assessment & Classification Framework.md` §4.3
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §4 (Information Assessment & Classification Framework), §4.3
```

### MU-013B

**File**: `.agent/knowledge/sources/patterns/worked_example_feature.md`

**Anchor**:

```md
- Source: `20. Advanced Integration Patterns.md`
```

**Replace with**:

```md
- Source: `.agent/assets/documentation_system.md` §20 (Advanced Integration Patterns)
```

**Rationale (MU-010 to MU-013)**: Makes provenance deterministic and validator-friendly.

**Validation**:

- all source lines use `.agent/assets/documentation_system.md`

---

## MU-014 — Add canonical metadata schema source

**File to create**: `.agent/knowledge/sources/patterns/metadata_schema.md`

**Create with content**:

```md
---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/knowledge_source_template.md
related:
  - sources/patterns/source_citation_style.md
  - sources/vocabulary/glossary.md
---

# Metadata Schema

> **Scope**: Canonical machine-validation schema for DDR knowledge files.
>
> **Excludes**: Semantic correctness of domain statements.

## Summary

Defines normative frontmatter fields, enums, and scope classes used by validation tooling.

## Structure

### In-Scope Archetypes

- concept
- protocol
- constraint
- pattern
- vocabulary
- context
- index

### Required Frontmatter Fields

- archetype
- status
- version
- created
- updated
- requires
- related

### Status Enum

- draft
- review
- active
- deprecated

### Path Rules

- Paths MUST be knowledge-root-relative (`sources/...`, `context/...`).
- Relative parent navigation (`../`) is prohibited.

### Index Rule

`_index.md` files are in-scope and MUST carry frontmatter with `archetype: index`.

---

## References

- `sources/patterns/knowledge_source_template.md` — Authoring template
```

**Rationale**: Makes validation contract explicit and stable.

**Validation**:

- new file included in sources index (MU-016)

---

## MU-015 — Add canonical source citation style source

**File to create**: `.agent/knowledge/sources/patterns/source_citation_style.md`

**Create with content**:

```md
---
archetype: pattern
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/metadata_schema.md
related:
  - sources/patterns/knowledge_source_template.md
---

# Source Citation Style

> **Scope**: Standard syntax for provenance citations in DDR knowledge documents.
>
> **Excludes**: Citation topology between DDR tags (`:links:`).

## Summary

All provenance references must resolve to concrete repository paths and stable section identifiers.

## Structure

### Canonical Form

- Source: `.agent/assets/documentation_system.md` §X (Section Title), §X.Y

### Rules

1. Repository path is mandatory.
2. Section number is mandatory when available.
3. Section title is recommended for human readability.
4. Free-text source titles without path are prohibited.

### Examples

✅ Correct:
- Source: `.agent/assets/documentation_system.md` §5 (Vertical Abstraction & Specification Protocols), §5.2

❌ Incorrect:
- Source: `5. Vertical Abstraction & Specification Protocols.md` §5.2

---

## References

- `sources/patterns/metadata_schema.md` — Validation contract
```

**Rationale**: Prevents provenance drift and non-resolvable references.

**Validation**:

- all existing noncanonical source lines remediated

---

## MU-016 — Update sources index for new pattern documents

**File**: `.agent/knowledge/sources/_index.md`

**Add entries to Quick Lookup table**:

```md
| Metadata Schema | pattern | `patterns/metadata_schema.md` |
| Source Citation Style | pattern | `patterns/source_citation_style.md` |
```

**Add entries to Patterns section**:

```md
- `Metadata Schema` (`patterns/metadata_schema.md`) — Canonical validation fields and enums
- `Source Citation Style` (`patterns/source_citation_style.md`) — Provenance citation standard
```

**Adjust counts**:

- Total files and patterns counts must be updated consistently across header, section title, and progress summary.

**Rationale**: Prevents orphan pattern docs and keeps inventory accurate.

**Validation**:

- counts match actual file inventory

---

## MU-017 — Forward-reference consistency reinforcement in traceability protocol

**File**: `.agent/knowledge/sources/protocols/traceability_chain.md`

**Anchor**:

```md
| **Forward reference** | TDD cites ISP | ERROR |
```

**Replace with**:

```md
| **Forward reference** | Higher abstraction tier cites lower abstraction tier (e.g., BRD cites SAD) | ERROR |
```

**Add clarifier below citation matrix**:

```md
Forward-reference rule: `:links:` MUST point upward in justification authority (toward BRD), never downward.
```

**Rationale**: Synchronizes protocol language with corrected glossary semantics.

**Validation**:

- glossary and traceability definitions are semantically identical

---

## MU-018 — Add anti-hallucination execution protocol for agents (new)

**File to create**: `.agent/knowledge/sources/protocols/implementation_guardrails.md`

**Create with content**:

```md
---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/metadata_schema.md
  - sources/patterns/source_citation_style.md
related:
  - sources/protocols/traceability_chain.md
---

# Implementation Guardrails

> **Scope**: Deterministic execution protocol to reduce agent hallucination and patch drift during DDR modifications.
>
> **Excludes**: Business prioritization of change requests.

## Summary

This protocol defines mandatory preflight, execution, and postflight checks for any agent modifying DDR knowledge files.

## Prerequisites

- Local repository access
- Baseline validation script availability
- Approved modification specification

## Procedure

1. Capture baseline inventory and validation output.
2. Apply only explicitly listed modifications.
3. Re-run validation after each logical batch.
4. Halt on first schema error and record the failing unit ID.
5. Produce final delta report with changed files and rule outcomes.

## Outcomes

| Result | Condition | Next Action |
| :------- | :---------- | :------------ |
| Pass | All checks green | Merge-ready |
| Soft fail | Non-blocking warnings | Open follow-up issue |
| Hard fail | Schema/path/provenance violation | Block merge |

---

## References

- `sources/patterns/metadata_schema.md` — Validation rules
- `sources/patterns/source_citation_style.md` — Provenance syntax
```

**Rationale**: Gives executing agents a strict process to minimize hallucinations and omissions.

**Validation**:

- protocol appears in sources index protocol list and quick lookup (MU-016 extension)

---

## MU-019 — Legacy external DDR reference reconciliation protocol

**File to create**: `.agent/knowledge/sources/protocols/external_reference_reconciliation.md`

**Create with content**:

```md
---
archetype: protocol
status: active
version: 1.0.0
created: 2026-02-15
updated: 2026-02-15
requires:
  - sources/patterns/metadata_schema.md
  - sources/protocols/implementation_guardrails.md
related:
  - sources/patterns/source_citation_style.md
---

# External Reference Reconciliation

> **Scope**: Deterministic handling of externally supplied DDR references (e.g., Google Docs) when access may be restricted.
>
> **Excludes**: Granting network/auth permissions.

## Summary

This protocol prevents hallucination and policy drift by requiring explicit evidence capture, deferred reconciliation, and repository-first enforcement whenever external reference sources cannot be retrieved.

## Prerequisites

- External reference URL or exported file
- Current repository canonical sources
- Validation tooling

## Procedure

1. Attempt retrieval of external reference and capture command evidence.
2. If retrieval fails, log `external_reference_unresolved` with timestamp, URL, and failure details.
3. Continue implementation using `.agent/knowledge/**` + `.agent/assets/documentation_system.md` only.
4. Create deferred reconciliation task referencing unresolved source.
5. When external source becomes available, run structured diff against canonical sources and apply explicit, traceable updates.

## Outcomes

| Result | Condition | Next Action |
| :------- | :---------- | :------------ |
| Retrieved | Source accessible | Diff and reconcile immediately |
| Unresolved | Source inaccessible | Continue with canonical sources + open deferred task |

---

## References

- `sources/protocols/implementation_guardrails.md` — Safe execution controls
- `sources/patterns/source_citation_style.md` — Provenance conventions
```

**Rationale**: Integrates externally supplied legacy documentation safely without introducing unverifiable content.

**Validation**:

- unresolved external references are logged with command evidence
- deferred reconciliation task exists for each unresolved source

---

## 3) Cross-File Consistency Requirements

After applying all MUs, the implementation MUST satisfy all conditions below:

1. No file in `.agent/knowledge/sources/**/*.md` has `status: validated`.
2. No metadata `requires`/`related` path contains `../`.
3. No `- Source:` line lacks `.agent/assets/documentation_system.md` path.
4. All `_index.md` files under `.agent/knowledge/` have frontmatter.
5. `forward reference` semantic meaning is identical in glossary and traceability protocol.
6. Sources index counts match actual file inventory after added files.
7. External-reference unresolved states (if any) are explicitly logged with retrieval evidence and deferred reconciliation task IDs.

---

## 4) Implementation Ordering (Strict)

Apply changes in this order to reduce cascading failures:

1. MU-004 (template normalization)
2. MU-014, MU-015, MU-018 (new normative docs)
3. MU-001, MU-002, MU-003 (index frontmatter policies)
4. MU-005, MU-006, MU-007, MU-017 (semantic normalization)
5. MU-008 through MU-013 (source citation cleanup)
6. MU-016 (index inventory/count reconciliation)
7. Full validation suite (§6)

---

## 5) Anti-Error / Anti-Hallucination Techniques (Mandatory)

1. **Anchor-based edits only**: Every edit must match the provided anchor before replacement.
2. **Unit-ID traceability**: Commit message and implementation report must list MU IDs completed.
3. **No inferred paths**: If source path uncertain, use only `.agent/assets/documentation_system.md` as canonical source.
4. **Incremental validation**: run checks after each workstream batch.
5. **Idempotency check**: running the same patch pipeline twice must produce no additional changes.
6. **Diff boundedness**: changes must remain within files enumerated by MUs unless explicitly justified.
7. **Count reconciliation lock**: update index counts only after file create/delete operations are complete.

---

## 6) Validation Commands (Required)

### 6.1 Frontmatter + status/path sanity

```bash
python - <<'PY'
import glob,re
files=glob.glob('.agent/knowledge/**/*.md', recursive=True)
errs=[]
for f in files:
    txt=open(f).read()
    if f.endswith('_index.md') or '/sources/' in f or '/context/' in f:
        if not txt.startswith('---\n') or '\n---\n' not in txt:
            errs.append((f,'missing_frontmatter'))
            continue
        fm=txt.split('\n---\n',1)[0]
        if 'status: validated' in fm:
            errs.append((f,'status_validated_forbidden'))
        if re.search(r'^\s*-\s*\.\./', fm, flags=re.M):
            errs.append((f,'relative_parent_path_forbidden'))
print('errors',len(errs))
for e in errs: print(e)
PY
```

### 6.2 Source citation normalization

```bash
python - <<'PY'
import glob
bad=[]
for f in glob.glob('.agent/knowledge/**/*.md', recursive=True):
    for i,l in enumerate(open(f),1):
        if l.strip().startswith('- Source:') and '.agent/assets/documentation_system.md' not in l:
            bad.append((f,i,l.strip()))
print('noncanonical_source_lines',len(bad))
for b in bad: print(b)
PY
```

### 6.3 Inventory reconciliation check

```bash
python - <<'PY'
import glob
all_sources=glob.glob('.agent/knowledge/sources/**/*.md', recursive=True)
print('sources_file_count',len(all_sources))
PY
```

### 6.4 Broken markdown link scan

```bash
python - <<'PY'
import re,glob,os
errs=[]
for f in glob.glob('.agent/knowledge/**/*.md', recursive=True):
    txt=open(f).read()
    for m in re.finditer(r'\[[^\]]+\]\(([^)]+)\)', txt):
        link=m.group(1)
        if '://' in link or link.startswith('#') or not link.endswith('.md'):
            continue
        target=os.path.normpath(os.path.join(os.path.dirname(f), link))
        if not os.path.exists(target):
            errs.append((f,link,target))
print('broken_md_links',len(errs))
for e in errs: print(e)
PY
```

---

## 7) Deliverable Expectations for Implementing Agents

The implementing agent MUST output:

1. Completed MU checklist (`MU-001` … `MU-019`)
2. Final changed-file list
3. Validation command outputs from §6
4. Exceptions/deferrals with explicit reasons
5. Follow-up recommendations (if any) separated from required work

---

## 8) Definition of Implementation Completion

Implementation is complete only when:

- All required MUs are applied or formally deferred with justification.
- All required validation commands pass with zero blocking errors.
- Source and index inventories are internally consistent.
- No unresolved contradiction remains for status lifecycle, path policy, or forward-reference semantics.

---
archetype: vocabulary
status: active
version: 2.0.0
created: 2026-01-16
updated: 2026-01-18
requires: []
related:
  - context/glossary.md
---

# DDR Glossary

> **Scope**: Terminology for the DDR framework and agent operations.
>
> **Excludes**: Project-specific terms (see `context/glossary.md`).

## Summary

DDR controlled vocabulary prevents semantic drift by LLMs. Universal to all DDR projects. Project terminology maintained separately in context layer.

## Terms

| Term                  | Definition                                                                                             |
| :-------------------- | :----------------------------------------------------------------------------------------------------- |
| **Tag**               | Traceable documentation element with unique ID (e.g., `BRD-1.2`)                                       |
| **Citation**          | Parent reference via `:links:` directive                                                               |
| **Tier**              | One of seven DDR abstraction levels (BRD through ISP)                                                  |
| **Traceability**      | Complete chain of citations from any tag to BRD root                                                   |
| **Orphan**            | Tag without required parent citation                                                                   |
| **Manifest**          | Reconciliation status block tracking section integrity                                                 |
| **Archetype**         | Knowledge source type (concept, protocol, constraint, pattern, vocabulary)                             |
| **Anti-Pattern**      | Structural violation of DDR tier rules (e.g., technology in BRD)                                       |
| **Dirty Flag**        | Manifest status indicating a section requires re-verification                                          |
| **Leaf Node**         | ISP tag with no children — terminal node in the documentation graph                                    |
| **Root Node**         | BRD tag with no parents — entry point of every traceability chain                                      |
| **Stub Purity**       | Constraint requiring ISP code to contain only `pass` statements                                        |
| **Forward Reference** | Invalid citation where a higher abstraction tier cites a lower abstraction tier (e.g., BRD citing SAD) |
| **Sibling Citation**  | Invalid citation where a tag cites a peer at the same tier level                                       |
| **Deprecation**       | Marking a tag as superseded while preserving its ID and citation validity                              |

## Abbreviations

| Abbrev   | Expansion                         | Description                     |
| :------- | :-------------------------------- | :------------------------------ |
| DDR      | Development Documentation Roadmap | The documentation framework     |
| BRD      | Business Requirements Document    | Tier 1: Strategic justification |
| NFR      | Non-Functional Requirements       | Tier 2: Constraints and targets |
| FSD      | Feature Specifications Document   | Tier 3: System capabilities     |
| SAD      | System Architecture Document      | Tier 4: Structure and patterns  |
| ICD      | Interface & Contract Definitions  | Tier 5: Data schemas            |
| TDD      | Technical Design Document         | Tier 6: Component blueprints    |
| ISP      | Implementation Stubs & Prompts    | Tier 7: Code skeletons          |

## Enforcement

1. Scan nouns related to DDR operations
2. Verify against this glossary for framework terms
3. Verify against `context/glossary.md` for project terms
4. Flag unknown terms as errors

---

## References

- Project glossary: `context/glossary.md`
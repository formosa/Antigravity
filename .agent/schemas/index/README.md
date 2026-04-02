# DESIGN_JUSTIFICATION: Asset Directory Index Schema v1.0.0

<document_purpose>
This document establishes the schema contract for folder-level agent asset indexes such as `.agent/tools/index.md` and `.agent/skills/index.md`. The target artifact is a deterministic registry that supports both first-pass agent routing and fast human scanning without becoming the authoritative execution contract for the assets it lists.
</document_purpose>

<schema_evaluation_and_justification>

- **Header Without Frontmatter:** The example index uses a plain Markdown H1 plus a compact blockquote preamble instead of YAML frontmatter. The schema preserves that format so folder indexes remain lightweight and immediately readable in rendered Markdown while still exposing explicit routing metadata.
- **Deterministic Scan Order:** The schema requires `Use This Index`, `Selection Map`, `Manifest`, `Detailed Records`, `Category Totals`, and `Index Boundaries` in a stable top-to-bottom sequence. This reduces ambiguity for agents consuming the file linearly.
- **Manifest + Records Split:** The fenced YAML manifest provides normalized machine-oriented fields, while the detailed records provide concise explanatory prose. This avoids overloading either representation and keeps machine parsing separate from human interpretation.
- **Authority Boundary Preservation:** The schema requires an explicit authority rule in the preamble and an `Index Boundaries` section. This prevents the index from silently superseding the linked asset definitions and reduces hallucination surface area.
- **Generic Asset Coverage:** The manifest model is intentionally generic enough for tools, skills, rules, workflows, and similar folder assets. It supports stable common fields while allowing additional flat scalar or list metadata when a specific asset class needs it.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [`.agent/tools/index.md`](../../tools/index.md)
   - Canonical example for the initial schema. Establishes the H1 plus blockquote preamble, intent-first selection map, fenced YAML manifest, detailed records, category totals, and explicit boundary rules.

2. [`.agent/tools/cleanup_temp_assets.md`](../../tools/cleanup_temp_assets.md)
   - Demonstrates why the directory index must defer to linked asset definitions for exact invocation, safety, and operational semantics.

3. [`.agent/schemas/skill/skill.d.ts`](../skill/skill.d.ts)
   - Local reference for repository schema style, including strong JSDoc guidance and explicit separation between metadata and body content.

4. [`.agent/schemas/workflow/workflow.d.ts`](../workflow/workflow.d.ts)
   - Local reference for concise schema contracts that model ordered Markdown sections without introducing unnecessary structural complexity.

5. [`.agent/skills/dev-create-schema/SKILL.md`](../../skills/dev-create-schema/SKILL.md)
   - Governing workflow used to scaffold, validate, and index this schema definition.

</authoritative_reference_repository>

<modification_history>

| Date | Version | Classification | Description |
| :--- | :--- | :--- | :--- |
| 2026-04-01 | v1.0.0 | Initial Release | Created `index.d.ts` and supporting documentation for generic folder-level agent asset indexes, using `.agent/tools/index.md` as the seed example. |

</modification_history>

<schema_governance>
```yaml
primary_owner_skill: dev-create-schema
distribution_model: canonical-plus-vendored-mirror
```
</schema_governance>

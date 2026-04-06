# DESIGN_JUSTIFICATION: Asset Directory Index Schema v1.2.2

<document_purpose>
This document establishes the schema contract for folder-level agent asset indexes such as `.agent/tools/index.md` and `.agent/skills/index.md`. The target artifact is a deterministic registry that supports both first-pass agent routing and fast human scanning without becoming the authoritative execution contract for the assets it lists.
</document_purpose>

<schema_evaluation_and_justification>

- **Header Without Frontmatter:** The example index uses a plain Markdown H1 plus a compact blockquote preamble instead of YAML frontmatter. The schema preserves that format so full-form directory indexes remain lightweight and immediately readable in rendered Markdown while still exposing explicit routing metadata.
- **Deterministic Scan Order:** The schema requires `Use This Index`, `Selection Map`, `Manifest`, `Detailed Records`, `Category Totals`, and `Index Boundaries` in a stable top-to-bottom sequence. This reduces ambiguity for agents consuming the file linearly.
- **Manifest + Records Split:** The fenced YAML manifest provides normalized machine-oriented fields, while the detailed records provide concise explanatory prose. This avoids overloading either representation and keeps machine parsing separate from human interpretation.
- **Authority Boundary Preservation:** The schema requires an explicit authority rule in the preamble and an `Index Boundaries` section. This prevents the index from silently superseding the linked asset definitions and reduces hallucination surface area.
- **Shared Metadata Coverage:** The manifest model standardizes common discovery metadata across full-form indexes, including rule activation fields (`trigger`, `globs`, `priority`), the `asset_structure` discriminant, and flat manifest/record escape hatches for low-entropy asset-specific extensions.
- **Current Adoption Boundary:** [`.agent/tools/index.md`](../../tools/index.md), [`.agent/skills/index.md`](../../skills/index.md), [`.agent/workflows/index.md`](../../workflows/index.md), and [`.agent/rules/index.md`](../../rules/index.md) are the current conforming examples of the full-form contract.
- **Schemas-Directory Governance Exception:** [`.agent/schemas/index.md`](../index.md) is a generated table-only lookup maintained by `core-schema`. It intentionally does not conform to `AssetDirectoryIndexDefinition` because schema discovery does not require the selection-map, manifest, detailed-record, and authority-boundary apparatus used for runtime asset routing.

</schema_evaluation_and_justification>

<authoritative_reference_repository>

1. [`.agent/tools/index.md`](../../tools/index.md)
   - Canonical example for the initial schema. Establishes the H1 plus blockquote preamble, intent-first selection map, fenced YAML manifest, detailed records, category totals, and explicit boundary rules.

2. [`.agent/skills/index.md`](../../skills/index.md)
   - Live full-form example showing the same discovery-index contract applied to folder-packaged skill assets and directory-backed implementations.

3. [`.agent/workflows/index.md`](../../workflows/index.md)
   - Live full-form example showing the contract applied to reusable workflow assets with deterministic index synchronization.

4. [`.agent/rules/index.md`](../../rules/index.md)
   - Live full-form example showing the contract applied to flat-file rule assets with trigger metadata, priority metadata, and explicit authority boundaries.

5. [`.agent/schemas/index.md`](../index.md)
   - Generated table-only schema registry that is intentionally outside the full-form directory-index contract and therefore documents the governance exception described above.

6. [`.agent/tools/cleanup_temp_assets.md`](../../tools/cleanup_temp_assets.md)
   - Demonstrates why the directory index must defer to linked asset definitions for exact invocation, safety, and operational semantics.

7. [`.agent/schemas/skill/skill.d.ts`](../skill/skill.d.ts)
   - Local reference for repository schema style, including strong JSDoc guidance and explicit separation between metadata and body content.

8. [`.agent/schemas/workflow/workflow.d.ts`](../workflow/workflow.d.ts)
   - Local reference for concise schema contracts that model ordered Markdown sections without introducing unnecessary structural complexity.

9. [`.agent/skills/core-schema/SKILL.md`](../../skills/core-schema/SKILL.md)
   - Governing workflow used to scaffold, validate, and index this schema definition.

</authoritative_reference_repository>

<modification_history>

| Date       | Version | Classification   | Description                                                                                                                                                                                               |
| :--------- | :------ | :--------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| 2026-04-01 | v1.0.0  | Initial Release  | Created `index.d.ts` and supporting documentation for generic folder-level agent asset indexes, using `.agent/tools/index.md` as the seed example.                                                        |
| 2026-04-02 | v1.1.0  | Schema Hardening | Typed shared rule metadata, added `asset_structure`, added record escape-hatch parity, corrected live-adoption claims, and documented the generated schemas-index exception.                              |
| 2026-04-03 | v1.2.0  | Adoption Update  | Promoted `.agent/workflows/index.md` to the full-form directory-index contract and updated the live-adoption guidance to treat workflows as a governed index surface rather than a lightweight exception. |
| 2026-04-03 | v1.2.1  | Adoption Update  | Promoted `.agent/rules/index.md` to the full-form directory-index contract and updated the live examples to treat rules as a governed index surface alongside tools, skills, and workflows.               |
| 2026-04-04 | v1.2.2  | Naming Alignment | Repointed the schemas-directory governance exception and governing workflow reference from `dev-schema` to `core-schema` after the foundational `core-*` family migration.                                |

</modification_history>

<schema_governance>

```yaml
primary_owner_skill: core-schema
distribution_model: canonical-plus-vendored-mirror
```

</schema_governance>

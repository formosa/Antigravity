---
name: "dev-schema-governance"
version: "1.0.0"
description: "Glob-scoped governance rule for `.agent/schemas/` assets covering canonical `.d.ts` contracts, schema README governance blocks, example fidelity, and the table-only schema index."
trigger: "glob"
globs: ".agent/schemas/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>

1. Scope Boundary: This rule governs only assets under `.agent/schemas/`. It MUST NOT impose rule-asset frontmatter or XML-fencing requirements on files under `.agent/rules/`.
2. Canonical Type Contract: `.agent/schemas/<schema-id>/<schema-id>.d.ts` files MUST remain the authoritative type contract for each schema and MUST stay synchronized with the adjacent example and governance README.
3. Schema README Governance: Canonical schema READMEs under `.agent/schemas/<schema-id>/README.md` MUST preserve accurate `<document_purpose>`, `<schema_governance>`, `<authority_order>`, and `<modification_history>` content aligned with the adjacent schema directory, including the correct `primary_owner_skill`.
4. Modification History Required: Material schema changes MUST append a new `README.md` modification-history row that matches the delivered version and describes the actual contract or governance change.
5. Example and Template Fidelity: Example or template markdown under `.agent/schemas/` MUST remain aligned with the adjacent `.d.ts` contract and MUST NOT contain unresolved `TODO`, `N/A`, or generic filler text that would misrepresent the schema.
6. Schema Index Exception: `.agent/schemas/index.md` MUST remain a generated table-only governance exception aligned with the current `dev-schema` index script. It MUST NOT be expanded into the richer full-form index contract used by rules, skills, tools, and workflows.

</constraints>

<verification_step>

1. If the target file is a canonical `.d.ts` schema, confirm the adjacent README and example or template remain synchronized with the updated contract surface.
2. If the target file is a canonical schema `README.md`, confirm the governance blocks, owner metadata, and modification history accurately reflect the adjacent schema directory.
3. If the target file is a schema example or template markdown asset, confirm it still reflects the adjacent `.d.ts` contract and does not contain unresolved placeholders.
4. If the target file is `.agent/schemas/index.md`, confirm it remains a generated table-only registry rather than a full-form discovery index.

</verification_step>

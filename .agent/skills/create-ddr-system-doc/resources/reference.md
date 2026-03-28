<document_purpose>
Define the generation contract for creating authoritative DDR System Markdown documentation from a schema/specification pair.
</document_purpose>

<source_precedence>

1. Treat the specification YAML as the authority for actual values, rule statements, examples, version metadata, lifecycle transitions, extension catalogs, and tier content.
2. Treat the schema YAML as the authority for validation, requiredness, optionality, and field-level structure.
3. If the specification and schema disagree, fail fast and report the exact mismatch. Do not silently reconcile the divergence in prose.
</source_precedence>

<generation_rules>

- Preserve rule IDs, extension IDs, tier IDs, status values, operation names, and scoring-profile identifiers exactly as written in source.
- Prefer tables for structured lists of objects and checklists for validation criteria.
- Use the representative `nodes` section to render topology and the architecture diagram.
- Use `tier_definitions` as the source of truth for per-tier summaries, relationships, and atomic inclusion/exclusion rules.
- Use `lifecycle` as the authority for status transitions and guards.
- Use `are_scoring_profiles` only in the ARE extension subsection; do not invent an independent top-level section for it.
- Omit empty optional sections only when the specification omits the source block entirely. If a source block exists but is empty, state that it is empty.
</generation_rules>

<style_rules>

- Keep the document authoritative, compact, and technically literal.
- Summarize only where the source is narrative; do not paraphrase away important constraints.
- Avoid placeholders, TODOs, or speculative language.
- Prefer repo-relative paths in user-facing examples and absolute fidelity in generated content.
</style_rules>

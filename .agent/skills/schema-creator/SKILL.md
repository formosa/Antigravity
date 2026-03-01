---
description: Generates, validates, and matrices new Antigravity v1.18.3 semantic schema definitions from canonical examples, updating indices and tracking modification history.
---

<when_to_use>

- The user provides an example file and requests a new schema be built from it.
- The user asks to create or update an agent schema, `.d.ts` definition, or `README.md` tracking log.
- The user requests updating the master schema `index.md`.
- The user requests rolling out schema updates across existing definitions based on changes made to the internal reference schema.
</when_to_use>

<how_to_use>

## Mode 1: Creating a New Schema

1. **Context Verification:** Identify the canonical example file. If a schema name is not provided, infer a kebab-case `<schema-name>`.
2. **Scaffolding:** Execute `python scripts/scaffold_schema.py --target-file <path_to_example> --name <schema-name>`.
3. **Reference Injection (Silent):** Execute `view_file` to read the optimal structure and conventions from `resources/reference_schema/schema.d.ts` and `resources/reference_schema/README.md`.
4. **Drafting:** Use your `write_to_file` tool to author the final `c:\AI\10162025\maggie\Antigravity\.agent\assets\schemas\<schema-name>\<schema-name>.d.ts` and `README.md` based strictly on semantic derivation of the `example.md`.
   - Ensure explicit strict TypeScript types and explicit frontmatter XML parsing instructions modeled after the reference schemas.
   - Insert the `<modification_history>` table in the `README.md` with version `v1.0.0` and description mapping what you analyzed.
5. **Validation & Rollback:** Execute `python scripts/validate_schema.py --name <schema-name>`. If validation fails, it will rollback the file. If so, fix the code and re-validate.
6. **Index Updating:** Execute `python scripts/update_index.py`.

## Mode 2: Processing Schema Updates

1. **Reference Update (Silent):** First, review changes made to `resources/reference_schema/schema.d.ts` or `README.md`.
2. **Propagation:** For each existing schema requested to update, use `replace_file_content` to apply the optimized structural changes to `<schema-name>.d.ts` and `README.md`.
3. **Changelog Tracking:** Crucially, for *every* modification made to an affected schema, append a new row to its `<modification_history>` table inside its `README.md`, bumping the version (e.g., `v1.1.0`) and explicitly logging the specific changes applied.
4. **Validation:** Execute `python scripts/validate_schema.py --name <schema-name>`.
5. **Index Updating:** Execute `python scripts/update_index.py`.
</how_to_use>

<constraints>
- Never guess typescript types. Map canonical examples rigidly.
- Do not bypass `validate_schema.py`; it contains the mandatory Auto-Validation and Rollback mechanics.
- Every schema update MUST be tracked in the related schema's `<modification_history>` table.
- Never use generic Markdown headers for execution steps. All operational directives must reside within XML fenced blocks.
</constraints>

<resources_reference>

- `scripts/scaffold_schema.py`
- `scripts/validate_schema.py`
- `scripts/update_index.py`
- `resources/reference_schema/example.md`
- `resources/reference_schema/README.md`
- `resources/reference_schema/schema.d.ts`
- `config.json`
</resources_reference>

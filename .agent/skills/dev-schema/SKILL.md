---
name: dev-schema
version: 2.3.1
description: Authors and updates canonical Antigravity `.d.ts` schema files via scaffold, strict validation, schema-governance README maintenance, and owner-aware index synchronization. Use when the task is to create a new schema from an example artifact, update an existing schema definition, or regenerate the schema directory index for an owner-managed asset family. Do not use for creating workflows, skills, implementation plans, or project features outside the schema authoring contract.
---

<when_to_use>
- The user asks to create a new `.d.ts` schema file from an example artifact or document.
- The user asks to update an existing Antigravity schema or schema README.
- The user asks to regenerate or synchronize the `.agent/schemas/index.md` directory index.
- Example prompt: "Create a new schema for the release-notes artifact."
- Example prompt: "Update the issues-tracker schema to add a new severity field."
- Example prompt: "Regenerate the schema index after adding the new plan schema."
- Do not use when the task is to create a workflow, skill, implementation plan, or any ordinary project feature outside the `.agent/schemas/` directory tree.
- Do not use when the user only wants to read or validate an existing schema without modifying it.
</when_to_use>

<how_to_use>

## Mode A: Create a new schema

1. Confirm the source example file path and the target schema name in `kebab-case`.
2. **IF** the source example file does not exist, **THEN** report the missing file and halt.
3. **IF** the example file exists, **THEN** scaffold the schema directory:
   - `python .agent/skills/dev-schema/scripts/scaffold_schema.py --target-file <path_to_example> --name <schema-name>`
4. Author the generated `.d.ts` schema using only local reference patterns. Do not guess TypeScript types; derive them strictly from the example.
5. Author or update the schema `README.md` to describe purpose, authority order, schema governance, and modification history.
6. Validate the schema:
   - `python .agent/skills/dev-schema/scripts/validate_schema.py --name <schema-name>`
7. **IF** validation fails, **THEN** fix all reported errors and re-run validation before proceeding.
8. **IF** validation passes, **THEN** update the schema directory index:
   - `python .agent/skills/dev-schema/scripts/update_index.py`

## Mode B: Update an existing schema

1. Read the requested reference changes from the user or from the diff.
2. Confirm the target schema exists in `.agent/schemas/<schema-name>/`.
3. **IF** the target schema does not exist, **THEN** switch to Mode A.
4. Apply deterministic, minimal changes to the target `.d.ts` schema file.
5. Append a changelog entry in the schema's `README.md` modification history table and keep `<schema_governance>` current.
6. Validate the updated schema:
   - `python .agent/skills/dev-schema/scripts/validate_schema.py --name <schema-name>`
7. **IF** validation fails, **THEN** halt, report the failure, and fix before proceeding.
8. Update the index:
   - `python .agent/skills/dev-schema/scripts/update_index.py`

</how_to_use>

<constraints>
- Do not guess TypeScript types. Derive all types strictly from the source example or user specification.
- Do not skip validation. Halt on any validation failure and fix before proceeding.
- Every schema creation or modification must be recorded in the schema `README.md` modification history.
- Every canonical schema `README.md` must declare `<schema_governance>` with `primary_owner_skill` and `distribution_model: canonical-plus-vendored-mirror`.
- Keep all file paths repo-relative and written with forward slashes.
- Do not reference files that do not exist in the repository.
- Do not add new frontmatter keys or structural sections to schema files without a demonstrated requirement.
</constraints>

<resources_reference>
- Run `.agent/skills/dev-schema/scripts/scaffold_schema.py` to create the initial schema directory and copy the source example.
- Run `.agent/skills/dev-schema/scripts/validate_schema.py` to type-check the generated `.d.ts` file and roll back on failure.
- Run `.agent/skills/dev-schema/scripts/update_index.py` to rebuild the `.agent/schemas/index.md` directory index after any schema change.
- Read `.agent/skills/dev-skill/resources/owner-skill-pattern.md` when the schema change affects owner-skill governance, validation-first lifecycle wording, or canonical-versus-vendored mirror policy.
- Read `.agent/skills/dev-schema/resources/schema/schema/schema.d.ts` to understand the TypeScript interface contract for canonical Antigravity schema files.
- Read `.agent/skills/dev-schema/resources/schema/schema/README.md` to understand the authority order, governance metadata, and vendored-mirror distribution model.
- Read `.agent/skills/dev-schema/resources/schema/schema/example.md` to see a representative example of a correctly structured schema artifact.
- Read `.agent/skills/dev-schema/config.json` to check the resolved schema output directory and auto-validation toggle.
</resources_reference>

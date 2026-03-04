---
name: dev-create-schema
version: 2.0.0
description: Creates and updates Antigravity schemas via scaffold, strict validation, and index synchronization.
---

<when_to_use>

- The user asks to create a new `.d.ts` schema from an example.
- The user asks to update existing schemas or schema index documentation.
</when_to_use>

<how_to_use>

## Mode A: Create schema

1. Confirm source example and schema name (`kebab-case`).
2. Scaffold:
   - `python .agent/skills/dev-create-schema/scripts/scaffold_schema.py --target-file <path_to_example> --name <schema-name>`
3. Author generated schema/README using local reference patterns only.
4. Validate:
   - `python .agent/skills/dev-create-schema/scripts/validate_schema.py --name <schema-name>`
5. Update index:
   - `python .agent/skills/dev-create-schema/scripts/update_index.py`

## Mode B: Update schema(s)

1. Read requested reference changes.
2. Apply deterministic updates to target schema files.
3. Append changelog entry in each affected schema README.
4. Validate each schema.
5. Update index.

If validation fails, halt, report failure, and fix before proceeding.
</how_to_use>

<constraints>
- Do not guess TypeScript types.
- Do not skip validation.
- Every update must be recorded in modification history/changelog.
- Keep references and paths repo-relative.
</constraints>

<resources_reference>

- `.agent/skills/dev-create-schema/scripts/scaffold_schema.py`
- `.agent/skills/dev-create-schema/scripts/validate_schema.py`
- `.agent/skills/dev-create-schema/scripts/update_index.py`
- `.agent/skills/dev-create-schema/resources/schema/schema.d.ts`
- `.agent/skills/dev-create-schema/resources/schema/README.md`
- `.agent/skills/dev-create-schema/resources/schema/example.md`
- `.agent/skills/dev-create-schema/config.json`
</resources_reference>

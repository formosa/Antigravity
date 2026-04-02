---
name: dev-create-skill
version: 2.2.0
description: Creates or refines Antigravity-compatible skills with explicit trigger boundaries, root README lifecycle governance, vendored schema mirrors, and validation-first packaging hygiene. Use when the task is to scaffold a new skill or standardize an existing skill folder. Do not use for creating workflows, schemas, or ordinary project features outside the skill contract.
---

<when_to_use>
- Use when the user asks to create, scaffold, template, standardize, or harden a skill in `.agent/skills/...`.
- Use when the task is to improve skill triggering, `SKILL.md` structure, bundled resource layout, or skill packaging and validation behavior.
- Do not use when the request is to create a workflow, schema, implementation plan, or ordinary project code change outside a skill folder.
- Example prompt: "Create a new skill for generating release notes."
- Example prompt: "Standardize this existing skill so it validates and packages cleanly."
</when_to_use>

<how_to_use>
1. Gather 2-3 concrete requests that the target skill must handle. Extract the trigger phrases, required inputs, expected outputs, and adjacent tasks it must reject.
2. Decide the minimum skill shape:
   - Leave the skill instruction-only unless deterministic scripts or assets remove repeated code or reduce ambiguity.
   - Add scripts only for repeatable, high-risk, or machine-verifiable steps.
   - Add resources only when detailed reference material should stay out of `SKILL.md` until needed.
3. Scaffold the base skill directory with `python .agent/skills/dev-create-skill/scripts/init_skill.py <skill-name> --path <output-directory>` and add opt-in flags only for the directories or examples you actually need.
4. Write the target `SKILL.md`:
   - make `description` explicit about what the skill does, when it should trigger, and when it should not
   - use `<when_to_use>` to add positive triggers, exclusions, and concrete example prompts
   - use `<how_to_use>` to define ordered actions, required inputs, expected outputs, and verification
   - use `<constraints>` to state hard boundaries and anti-patterns
   - use `<resources_reference>` to list each file with whether it should be read or run, and why
5. Author the root `README.md` so it contains exactly `<document_purpose>`, `<authority_order>`, `<schema_relationships>`, and `<modification_history>`, and make the latest history row match the `SKILL.md` version.
6. Add only the files the skill will actually use, then ensure every referenced path exists and uses repo-relative forward-slash notation.
7. Sync vendored schema mirrors with `python .agent/skills/dev-create-skill/scripts/sync_schema_mirrors.py <path-to-skill>` so `resources/schema/<schema-id>/` reflects the canonical `.agent/schemas/` directories before validation or packaging.
8. Validate with `python .agent/skills/dev-create-skill/scripts/quick_validate.py <path-to-skill>`. Resolve all structural errors, then address any quality warnings about weak descriptions, missing exclusions, or ambiguous resource entries.
9. Trigger-test the finished skill with at least one prompt that should invoke it and one adjacent prompt that should not. Refine the description or exclusions until routing is predictable.
10. Package with `python .agent/skills/dev-create-skill/scripts/package_skill.py <path-to-skill> [output-directory]` only after schema sync, validation, and trigger checks are clean enough for handoff.
</how_to_use>

<constraints>
- Do not use deprecated frontmatter keys or invent new contract fields without updating the local schema, validator, and examples together.
- Do not leave vague verbs such as `improve`, `optimize`, or `handle` without concrete acceptance criteria or explicit outputs.
- Do not assume packages, tools, files, credentials, or permissions exist unless the skill explicitly verifies them.
- Do not cite non-authoritative sources when repo-local contract files or official vendor documentation are available.
- Do not reference scripts, resources, or assets that are absent, unused, or described unclearly.
- Do not hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/`.
- Keep skill-local paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>
- Run `.agent/skills/dev-create-skill/scripts/init_skill.py` to scaffold the minimal skill directory and optional folders.
- Run `.agent/skills/dev-create-skill/scripts/sync_schema_mirrors.py` to refresh `resources/schema/<schema-id>/` from canonical `.agent/schemas/` definitions.
- Run `.agent/skills/dev-create-skill/scripts/quick_validate.py` to detect structural errors and quality warnings before packaging.
- Run `.agent/skills/dev-create-skill/scripts/package_skill.py` to build a clean `.skill` archive after validation passes.
- Read `.agent/skills/dev-create-skill/resources/workflows.md` to author observable decision branches and validation loops instead of unverifiable internal reasoning instructions.
- Read `.agent/skills/dev-create-skill/resources/output-patterns.md` to preserve Antigravity artifact and output expectations when the new skill emits structured files.
- Read `.agent/skills/dev-create-skill/resources/schema/skill/skill.d.ts` to confirm the active frontmatter and XML block contract.
- Read `.agent/skills/dev-create-skill/resources/schema/skill/README.md` to understand the canonical-versus-vendored schema governance model.
- Read `.agent/skills/dev-create-skill/directory_structure.md` to choose the smallest correct scaffold shape before adding optional folders.
</resources_reference>

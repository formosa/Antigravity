---
name: asset-skill
version: 3.3.0
description: Authors or refines Antigravity-compatible skills with explicit trigger boundaries, root README lifecycle governance, vendored schema mirrors, generated skills-index maintenance, and validation-first packaging hygiene. Use when the task is to scaffold a new skill or standardize an existing skill folder, including runtime-routed owner skills, artifact-centric owner skills, foundational `core-*` contracts, and routing contracts. Do not use for creating workflows, schemas, or ordinary project features outside the skill contract.
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
   - If the target skill will own an asset family, read the shared owner-skill pattern, mirror its governance split, and add a dedicated governance rule only when the documented owner-rule criteria are met.
   - If that dedicated governance rule will govern one stable plural asset directory plus its generated category index, name the rule `<plural-directory>-governance`.
   - Do not generalize the plural collection-governance naming pattern to ordinary non-directory rules or to asset-family naming families such as `asset-*`, `artifact-*`, `core-*`, or `*-router`.
   - If the target skill will be the direct-route owner contract for a reusable `rule`, `skill`, or `workflow` directory, classify it as a `Runtime-Routed Owner Skill` and name it `asset-<asset-family>`.
   - If the target skill will own one governed artifact family end to end, classify it as an `Artifact-Centric Owner` and prefer `artifact-<artifact-family>`.
   - If the target artifact family already has a schema-declared canonical owner name that intentionally differs from the schema directory id, preserve the canonical owner name. For the `issues-tracker` schema, prefer `artifact-issue-tracker`.
   - If the target skill will own a foundational cross-cutting governance surface such as canonical schema authoring, classify it as a `Foundational Core Contract` and prefer `core-<capability>`.
   - If the target skill is primarily an orchestration or routing contract, prefer a `*-router` name.
   - If the target skill is a router, keep it outside the `Runtime-Routed Owner Skill`, `Artifact-Centric Owner`, and `Foundational Core Contract` families unless the shared owner-skill pattern explicitly says otherwise.
3. Scaffold the base skill directory with `python .agent/skills/asset-skill/scripts/init_skill.py <skill-name> --path <output-directory>` and add opt-in flags only for the directories or examples you actually need.
4. Write the target `SKILL.md`:
   - make `description` explicit about what the skill does, when it should trigger, and when it should not
   - use `<when_to_use>` to add positive triggers, exclusions, and concrete example prompts
   - use `<how_to_use>` to define ordered actions, required inputs, expected outputs, and verification
   - use `<constraints>` to state hard boundaries and anti-patterns
   - use `<resources_reference>` to list each file with whether it should be read or run, and why
5. Author the root `README.md` so it contains exactly `<document_purpose>`, `<authority_order>`, `<schema_relationships>`, and `<modification_history>`, and make the latest history row match the `SKILL.md` version.
6. Add only the files the skill will actually use, then ensure every referenced path exists and uses repo-relative forward-slash notation.
7. Sync vendored schema mirrors with `python .agent/skills/asset-skill/scripts/sync_schema_mirrors.py <path-to-skill>` so `resources/schema/<schema-id>/` reflects the canonical `.agent/schemas/` directories before validation or packaging.
8. Validate with `python .agent/skills/asset-skill/scripts/quick_validate.py <path-to-skill>`. Resolve all structural errors, any schema-mirror drift, and any stale `.agent/skills/index.md` findings before proceeding.
9. Regenerate `.agent/skills/index.md` with `python .agent/skills/asset-skill/scripts/update_index.py` whenever any skill inventory, routing description, or owned skill package changes.
10. Trigger-test the finished skill with at least one prompt that should invoke it and one adjacent prompt that should not. Refine the description or exclusions until routing is predictable.
11. Package with `python .agent/skills/asset-skill/scripts/package_skill.py <path-to-skill> [output-directory]` only after schema sync, skills-index regeneration, validation, and trigger checks are clean enough for handoff.
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

- Run `.agent/skills/asset-skill/scripts/init_skill.py` to scaffold the minimal skill directory and optional folders.
- Run `.agent/skills/asset-skill/scripts/sync_schema_mirrors.py` to refresh `resources/schema/<schema-id>/` from canonical `.agent/schemas/` definitions.
- Run `.agent/skills/asset-skill/scripts/quick_validate.py` to detect structural errors and quality warnings before packaging.
- Run `.agent/skills/asset-skill/scripts/update_index.py` to regenerate `.agent/skills/index.md` after any skill inventory or routing-contract change.
- Run `.agent/skills/asset-skill/scripts/package_skill.py` to build a clean `.skill` archive after validation passes.
- Read `.agent/skills/asset-skill/resources/owner-skill-pattern.md` when the target skill will own a governed asset family and must align with the shared owner-skill lifecycle.
- Read `.agent/skills/asset-skill/resources/workflows.md` to author observable decision branches and validation loops instead of unverifiable internal reasoning instructions.
- Read `.agent/skills/asset-skill/resources/output-patterns.md` to preserve Antigravity artifact and output expectations when the new skill emits structured files.
- Read `.agent/skills/asset-skill/resources/schema/skill/skill.d.ts` to confirm the active frontmatter and XML block contract.
- Read `.agent/skills/asset-skill/resources/schema/skill/README.md` to understand the canonical-versus-vendored schema governance model.
- Read `.agent/skills/asset-skill/directory_structure.md` to choose the smallest correct scaffold shape before adding optional folders.
</resources_reference>

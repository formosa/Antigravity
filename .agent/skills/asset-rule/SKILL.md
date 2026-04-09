---
name: asset-rule
version: 2.1.2
description: Authors or refines Antigravity-compatible rule assets with explicit trigger boundaries, scaffold and validation tooling, and deterministic rules-index synchronization. Use when the task is to create, standardize, validate, or re-index a reusable rule under `.agent/rules/`. Do not use when the task is standalone canonical schema authoring, specialized rule-derived schema work such as `security-policy`, or ordinary project feature changes.
---

<when_to_use>

- Use when the user asks to create, scaffold, standardize, harden, or re-index a rule in `.agent/rules/`.
- Use when the task is to improve rule trigger wording, glob scope, verification steps, execution-tier hygiene, or rules-index alignment.
- Do not use when the request is to create or revise canonical `.d.ts` schemas, including standalone changes under `.agent/schemas/`.
- Do not use when the request is to define or revise a specialized rule-derived schema family such as `security-policy`, or to change ordinary project code outside `.agent/rules/`.
- Example prompt: "Create a new rule that enforces docs rebuild hygiene for generated files."
- Example prompt: "Standardize this existing rule so its trigger scope and verification steps are deterministic."
</when_to_use>

<how_to_use>

1. Gather 2-3 concrete requests the target rule must handle. Extract the trigger context, required frontmatter fields, expected rule behavior, and adjacent tasks the rule must reject.
2. Decide whether to scaffold or refine:
   - Run `python .agent/skills/asset-rule/scripts/init_rule.py <rule-name> [--path <output-directory>]` when creating a new rule.
   - Open the existing `.agent/rules/<rule-name>.md` when standardizing or tightening a live rule.
   - If the target rule governs one stable plural asset directory plus that directory's generated `index.md`, use the collection-scoped naming convention `<plural-directory>-governance` (for example: `rules-governance`, `schemas-governance`, `skills-governance`).
   - Do not apply the plural collection-governance naming pattern to ordinary non-directory rules.
3. Author the rule against the `rule` schema:
   - include YAML frontmatter with `version`, `description`, `trigger`, and `priority`
   - add `globs` only when `trigger` is `glob`
   - use `execution_tier: standard` unless a heavier non-LLM parallel workload is explicitly justified
   - encode rule behavior inside `<constraints>` and add `<verification_step>` when the rule needs explicit completion checks
4. Keep the rule narrow and role-appropriate:
   - target one coherent enforcement surface per rule
   - prefer concrete trigger phrases, file scopes, and verifiable constraints over broad guidance
   - do not mix rule authoring with standalone schema changes or specialized rule-derived schema design in the same pass
5. Validate with `python .agent/skills/asset-rule/scripts/quick_validate.py <rule-path-or-directory>`. Resolve structural failures before proceeding.
6. Update the rules directory index with `python .agent/skills/asset-rule/scripts/update_index.py` so `.agent/rules/index.md` stays aligned with the live rule set.
7. Trigger-test the finished rule with at least one prompt or file context that should invoke it and one adjacent context that should not. Refine the description, trigger, or glob scope until routing is predictable.
</how_to_use>

<constraints>
- Strict adherence to the `rule.d.ts` schema is REQUIRED.
- Provide explicit constraints. Do NOT leave vague rule goals such as "improve quality" or "optimize" without measurable expectations.
- Keep `trigger` and `globs` consistent: `globs` is required for `glob` rules and must be omitted for non-`glob` rules.
- Do NOT hallucinate scripts, files, or capabilities that do not exist in the repository.
- Do NOT hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/` instead.
- Keep rule-local paths repo-relative and written with forward slashes.
- Do NOT use this skill as a substitute for canonical schema authoring or for rule-derived schema families whose ownership remains elsewhere.
</constraints>

<resources_reference>

- Run `.agent/skills/asset-rule/scripts/init_rule.py` to scaffold a new rule from the canonical rule example.
- Run `.agent/skills/asset-rule/scripts/quick_validate.py` to detect rule-asset structural errors before handoff.
- Run `.agent/skills/asset-rule/scripts/update_index.py` to rebuild `.agent/rules/index.md` after rule changes.
- Read `.agent/skills/asset-skill/resources/owner-skill-pattern.md` to preserve the shared owner-skill lifecycle and governance model while keeping rule responsibilities role-appropriate.
- Read `resources/schema/rule/rule.d.ts` to verify the required rule frontmatter and XML block contract.
- Read `resources/schema/rule/example.md` to mirror the canonical rule structure and safe default trigger posture.
- Read `resources/schema/index/index.d.ts` to preserve the full-form rules-index contract used by `.agent/rules/index.md`.
- Read `resources/schema/index/example.md` to preserve section order, manifest shape, and authority-boundary wording in the rules index.
</resources_reference>

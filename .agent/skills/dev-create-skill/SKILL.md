---
name: dev-create-skill
version: 2.0.0
description: Scaffolds and finalizes Antigravity-compatible skills with deterministic structure and low-hallucination instruction design.
---

<when_to_use>
- The user asks to create a new custom skill.
- The user asks to scaffold or standardize existing skill format.
</when_to_use>

<how_to_use>
1. Confirm scope: trigger conditions, expected workflow, required scripts/resources.
2. Scaffold base structure:
   - `python .agent/skills/dev-create-skill/scripts/init_skill.py <skill-name> --path <output-directory>`
3. Implement `SKILL.md` with required XML blocks:
   - `<when_to_use>`
   - `<how_to_use>`
   - `<constraints>`
   - `<resources_reference>`
4. Add referenced assets/scripts and ensure links are valid.
5. Run quick validation:
   - `python .agent/skills/dev-create-skill/scripts/quick_validate.py <path-to-skill>`

Prefer concise, deterministic instructions over long narrative guidance.
</how_to_use>

<constraints>
- Do not use deprecated skill metadata fields.
- Do not leave ambiguous execution verbs (e.g., “improve”, “optimize”) without measurable criteria.
- Keep tool paths repository-relative.
</constraints>

<resources_reference>
- `.agent/skills/dev-create-skill/scripts/init_skill.py`
- `.agent/skills/dev-create-skill/scripts/package_skill.py`
- `.agent/skills/dev-create-skill/scripts/quick_validate.py`
- `.agent/skills/dev-create-skill/resources/workflows.md`
- `.agent/skills/dev-create-skill/resources/output-patterns.md`
- `.agent/skills/dev-create-skill/resources/schema/skill.d.ts`
</resources_reference>

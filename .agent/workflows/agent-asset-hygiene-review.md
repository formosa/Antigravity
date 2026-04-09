---
name: agent-asset-hygiene-review
version: 1.0.1
description: Reviews changed `.agent` assets, runs deterministic validators and generated-index refresh steps by asset family, and restores index and temp-workspace hygiene before handoff.
---

### steps

1. Inspect the current change set under `.agent/` and group the touched paths by family: schemas, skills, rules, workflows, scripts, tools, and temp-workspace state.
2. If any canonical schema changed under `.agent/schemas/`, run `python .agent/skills/core-schema/scripts/validate_schema.py --name <schema-id>` for each touched schema directory, then regenerate `.agent/schemas/index.md` with `python .agent/skills/core-schema/scripts/update_index.py`, then resync every affected skill mirror with `python .agent/skills/asset-skill/scripts/sync_schema_mirrors.py <skill-dir>`.
3. For each touched or mirror-affected skill directory under `.agent/skills/`, run `python .agent/skills/asset-skill/scripts/quick_validate.py <skill-dir>`, then regenerate `.agent/skills/index.md` with `python .agent/skills/asset-skill/scripts/update_index.py`.
4. Run `python .agent/scripts/tests/validate_env.py --config` after any settings, runtime-target, PowerShell-rule, or environment-validation change.
5. If any reusable rule assets changed under `.agent/rules/`, run `python .agent/skills/asset-rule/scripts/quick_validate.py <rule-path-or-.agent/rules>` and regenerate `.agent/rules/index.md` with `python .agent/skills/asset-rule/scripts/update_index.py`.
6. If any workflow assets changed under `.agent/workflows/`, run `python .agent/skills/asset-workflow/scripts/quick_validate.py <workflow-path>` for each touched workflow and regenerate `.agent/workflows/index.md` with `python .agent/skills/asset-workflow/scripts/update_index.py`.
7. If root scripts or script tests changed under `.agent/scripts/`, regenerate both governed script indexes with `python .agent/scripts/update_index.py`; if a docs rebuild surface changed, run `python .agent/scripts/rebuild_docs.py` and halt on any retained failure directory.
8. If any tool definitions changed under `.agent/tools/`, update `.agent/tools/index.md` so the manifest, implementation path, outputs, side effects, and safety notes match the live tool definitions exactly.
9. Finish with `pytest .agent/scripts/tests -q`, `pytest .agent/skills -q`, any touched skill-local `test_*.py` coverage not already included, then run `python .agent/scripts/cleanup_temp_assets.py` in dry-run mode and resolve any unexpected empty, stale, or retained-failure run directories before concluding the review.

### verification_plan

- Every changed asset family must pass its validator or targeted test command before dependent index, mirror-sync, or packaging work proceeds.
- Any regenerated index must mention only live assets and must reflect the current implementation or definition paths.
- `.agent/skills/index.md` must be regenerated from the live skill inventory whenever any skill or skill mirror changes.
- `validate_env.py --config` must pass before runtime-mode validation or handoff if the task changed runtime-target policy, PowerShell execution guidance, or workspace settings.
- Successful docs rebuilds must delete their managed temp directory; failed rebuilds must retain the directory with `retained-on-failure.txt`.
- The final dry-run temp audit must not report unexpected empty, stale, or retained-failure run directories.

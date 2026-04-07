---
name: agent-asset-hygiene-review
version: 1.0.0
description: Reviews changed `.agent` assets, runs the correct validators and tests by asset family, and restores index and temp-workspace hygiene before handoff.
---

### steps

1. Inspect the current change set under `.agent/` and group the touched paths by family: rules, skills, schemas, scripts, tools, workflows, and temp-workspace state.
2. If any reusable rule assets changed under `.agent/rules/`, run `python .agent/skills/asset-rule/scripts/quick_validate.py <rule-path-or-.agent/rules>` and regenerate `.agent/rules/index.md` with `python .agent/skills/asset-rule/scripts/update_index.py`.
3. For each touched skill directory under `.agent/skills/`, run `python .agent/skills/asset-skill/scripts/sync_schema_mirrors.py <skill-dir>`, then `python .agent/skills/asset-skill/scripts/quick_validate.py <skill-dir>`, then execute any local `test_*.py` coverage in that skill's `scripts/` folder.
4. If any canonical schema changed under `.agent/schemas/`, run `python .agent/skills/core-schema/scripts/validate_schema.py --name <schema-id>` for each touched schema directory and regenerate `.agent/schemas/index.md` with `python .agent/skills/core-schema/scripts/update_index.py`.
5. If root scripts or script tests changed under `.agent/scripts/`, regenerate both governed script indexes with `python .agent/scripts/update_index.py`; if a docs rebuild surface changed, run `python .agent/scripts/rebuild_docs.py` and halt on any retained failure directory.
6. If any tool definitions changed under `.agent/tools/`, update `.agent/tools/index.md` so the manifest, implementation path, outputs, side effects, and safety notes match the live tool definitions exactly.
7. If any workflow assets changed under `.agent/workflows/`, run `python .agent/skills/asset-workflow/scripts/quick_validate.py <workflow-path>` for each touched workflow and regenerate `.agent/workflows/index.md` with `python .agent/skills/asset-workflow/scripts/update_index.py`.
8. Finish with `pytest .agent/scripts/tests` plus the touched skill-local test files, then run `python .agent/scripts/cleanup_temp_assets.py` in dry-run mode and resolve any unexpected empty, stale, or retained-failure run directories before concluding the review.

### verification_plan

- Every changed asset family must pass its validator or targeted test command before dependent index or packaging work proceeds.
- Any regenerated index must mention only live assets and must reflect the current implementation or definition paths.
- Successful docs rebuilds must delete their managed temp directory; failed rebuilds must retain the directory with `retained-on-failure.txt`.
- The final dry-run temp audit must not report unexpected empty, stale, or retained-failure run directories.

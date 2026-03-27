# Resolution Report Format

This package documents the current Resolution Report contract used by
`agent-create-issue-report`.

## Canonical Profile

New reports must follow the `v6.1`-style canonical shape represented by:

- `.agent/assets/proposals/active/v6.2/DDR_v6.1_Issue-001.md` for lineage
- `.agent/skills/agent-create-issue-report/resources/report-template.md` for structure
- `.agent/skills/agent-create-issue-report/resources/schema/example.md` for a golden example

The canonical profile has these properties:

- YAML frontmatter includes `created`, `updated`, and conditional `resolved`
- `### Agent Context` is always a fenced YAML block synthesized from tracker data
- Exactly two options: `Option A` and `Option B`
- Required top-level sections:
  - `### 1. Validation Audit of ISSUE-XXX`
  - `### 2. Suggested Strategies for Optimal Resolution of ISSUE-XXX`
  - `### 3. Comparative Analysis and Recommended Strategy`
  - `### 4. Implementation Note`
- New reports should use repo-relative evidence paths with line spans

## Legacy Profiles

Historical `v4` and `v5` reports remain valid repository artifacts, but they are not the
generation target for new reports.

- `v4` lineage:
  - may include `Option C`
  - may end with `### 4. Independent Review Conclusion`
- `v5` lineage:
  - uses two options only
  - does not include `updated`, `resolved`, or `### 4. Implementation Note`

The validator supports these formats in `legacy` mode or `auto` mode so existing reports can
be classified and checked without being rewritten.

## Validation

Canonical validation:

```powershell
python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py .agent/skills/agent-create-issue-report/resources/schema/example.md --mode canonical
python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py .agent/assets/proposals/active/v6.2/DDR_v6.1_Issue-001.md --mode canonical
```

Legacy validation:

```powershell
python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py .agent/assets/proposals/processed/v4/DDR_v4_Issue-001.md --mode legacy
python .agent/skills/agent-create-issue-report/scripts/validate_issue_report.py .agent/assets/proposals/processed/v5/DDR_v5_Issue-001.md --mode legacy
```

## Design Basis

The current package follows a small-contract, validator-first approach:

- Precise skill descriptions drive routing.  
  Source: https://codelabs.developers.google.com/getting-started-with-antigravity-skills
- Critical instructions should be explicit, front-loaded, and validated after generation.  
  Source: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Small, relevant examples and consistent tagged structure improve reliability.  
  Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags
- Stable prompt prefixes and evaluation loops improve efficiency and iteration quality.  
  Sources:
  - https://developers.openai.com/api/docs/guides/prompting
  - https://developers.openai.com/api/docs/guides/prompt-caching
  - https://developers.openai.com/api/docs/guides/prompt-optimizer
- Formal contracts and post-generation validation improve interoperability.  
  Sources:
  - https://json-schema.org/overview/what-is-jsonschema
  - https://json-schema.org/understanding-json-schema

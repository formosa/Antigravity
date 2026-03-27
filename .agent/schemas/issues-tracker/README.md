# Issues Tracker Format

This package defines the current blank Issues Tracker contract used by
`agent-create-issues-tracker`.

## Canonical Profile

New trackers must follow the lean visible-metadata format represented by:

- `.agent/assets/proposals/active/v6.2/DDR_v6.1_Issues_Tracker.md` for structure lineage
- `.agent/schemas/issues-tracker/template.md` for blank initialization
- `.agent/schemas/issues-tracker/example.md` for the canonical initialized example

The canonical profile has these properties:

- No HTML parser header at the top of the file
- No per-issue `AGENT_CONTEXT` blocks
- Required sections:
  - `DOCUMENT METADATA`
  - `ISSUE SCHEMA`
  - `ISSUE REGISTRY`
  - `ISSUES`
  - `RESOLUTION WORKFLOW`
  - `APPENDIX: CROSS-ISSUE DEPENDENCY MAP`
- Blank initialization state:
  - `open_issues: 0`
  - `resolved_issues: 0`
  - zero `### ISSUE-` entries
  - exactly one empty registry row
  - footer counts equal `0 issues identified | 0 resolved`

## Legacy Profiles

Historical `v4` and `v5` trackers remain valid repository artifacts, but they are not the
generation target for new trackers.

- Legacy markers:
  - HTML `AGENT PARSING HEADER`
  - per-issue `AGENT_CONTEXT` blocks
- Historical references:
  - `.agent/assets/proposals/processed/v4/DDR_v4_Issues_Tracker.md`
  - `.agent/assets/proposals/processed/v5/DDR_v5_Issues_Tracker.md`

The validator supports these formats in `legacy` mode or `auto` mode so they can be
classified and checked without being rewritten.

## Validation

Canonical initialization validation:

```powershell
python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py .agent/schemas/issues-tracker/example.md --mode canonical
```

Legacy validation:

```powershell
python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py .agent/assets/proposals/processed/v4/DDR_v4_Issues_Tracker.md --mode legacy
python .agent/skills/agent-create-issues-tracker/scripts/validate_issues_tracker.py .agent/assets/proposals/processed/v5/DDR_v5_Issues_Tracker.md --mode legacy
```

## Design Basis

The current package follows a small-contract, validator-first approach:

- Precise skill descriptions drive routing.  
  Source: https://codelabs.developers.google.com/getting-started-with-antigravity-skills
- Static heavy text belongs in resource files, not the hot-path skill prompt.  
  Source: https://codelabs.developers.google.com/getting-started-with-antigravity-skills
- Clear structure, explicit parameters, and validate-after-generate checks improve reliability.  
  Source: https://ai.google.dev/gemini-api/docs/prompting-strategies
- Small, relevant examples and consistent XML/tag structure improve instruction following.  
  Source: https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags
- Stable prompt prefixes and evaluation loops improve efficiency and iteration quality.  
  Sources:
  - https://developers.openai.com/api/docs/guides/prompt-caching
  - https://developers.openai.com/api/docs/guides/prompting
  - https://developers.openai.com/api/docs/guides/prompt-optimizer
- Formal schema contracts and post-generation validation improve interoperability.  
  Sources:
  - https://json-schema.org/overview/what-is-jsonschema
  - https://json-schema.org/understanding-json-schema

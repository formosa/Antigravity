# Agent Create Issues Tracker Reference

## Scope

This skill initializes blank Issues Tracker artifacts only.

- It does not populate issue entries.
- It does not generate resolution reports.
- It does not replace `agent-create-issue-report`.

## Canonical Output Choice

New trackers should follow the lean visible-metadata profile represented by:

- `.agent/assets/proposals/active/v6.2/DDR_v6.1_Issues_Tracker.md` as the strongest current-format lineage sample
- `.agent/schemas/issues-tracker/template.md` as the blank initialization contract

Historical lineage files remain useful as references, but not as the generation target:

- `.agent/assets/proposals/processed/v4/DDR_v4_Issues_Tracker.md`
- `.agent/assets/proposals/processed/v5/DDR_v5_Issues_Tracker.md`

## Validation Contract

The validator is intentionally initialization-focused for the canonical format.

- Canonical mode checks:
  - required section headings
  - zero issue entries
  - exactly one empty registry row
  - zeroed metadata and footer counts
  - no unresolved placeholders
  - header and footer date/title coherence
- Legacy mode recognizes the historical `v4` and `v5` tracker styles so they can be checked
  without being rewritten.

## Internal Evidence

- The skill was introduced on `2026-03-02` and later simplified on `2026-03-27`.
- The shared template already moved toward the lean `v6.1` structure, but related docs still
  documented the heavier `v4`/`v5` parser-header model before this update.
- No repo-local Antigravity thread transcript store was found during review, so git history,
  prompt clips, and generated tracker artifacts were used as the execution evidence base.

## External References

- Google Codelabs, "Authoring Google Antigravity Skills"  
  https://codelabs.developers.google.com/getting-started-with-antigravity-skills
- Google AI for Developers, "Prompt design strategies"  
  https://ai.google.dev/gemini-api/docs/prompting-strategies
- Anthropic, "Claude prompting best practices"  
  https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices#structure-prompts-with-xml-tags
- OpenAI, "Prompt caching"  
  https://developers.openai.com/api/docs/guides/prompt-caching
- OpenAI, "Prompting"  
  https://developers.openai.com/api/docs/guides/prompting
- OpenAI, "Prompt optimizer"  
  https://developers.openai.com/api/docs/guides/prompt-optimizer
- OpenAI, "Safety in building agents"  
  https://developers.openai.com/api/docs/guides/agent-builder-safety
- OpenAI, "Using GPT-5.4"  
  https://developers.openai.com/api/docs/guides/latest-model
- JSON Schema overview  
  https://json-schema.org/overview/what-is-jsonschema
- JSON Schema reference  
  https://json-schema.org/understanding-json-schema

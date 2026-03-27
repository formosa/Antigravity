# Skill Contract Notes

This folder documents the current `SKILL.md` contract for
`agent-create-issues-tracker`.

## Current Frontmatter

Use only:

- `name`
- `description`

Do not add `version`, `scope`, `priority`, or other router metadata. The repository's
skill validator rejects unsupported frontmatter keys.

## Current Body Blocks

The skill should expose:

- `<when_to_use>`
- `<how_to_use>`
- `<constraints>`
- `<resources_reference>`

## Package Boundaries

- The tracker output contract lives in `.agent/schemas/issues-tracker/`
- The validation entrypoint lives in `../../scripts/validate_issues_tracker.py`
- This skill remains blank-initialization only; issue population and issue-report generation
  are separate concerns

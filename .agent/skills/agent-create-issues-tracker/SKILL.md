---
name: agent-create-issues-tracker
version: 1.0.0
description: Autonomously generates a deterministic 'Issues Tracker' documentation asset conforming to the Antigravity schema.
---

# SKILL: agent-create-issues-tracker

## Goal

Autonomously generate a deterministic 'Issues Tracker' documentation asset conforming to the Antigravity schema.

<when_to_use>

## Context & Scope

- The developer explicitly requests to create, instantiate, or initialize a new "Issues Tracker".
- The active task requires logging systemic defects against a new architecture where an Issues Tracker `.md` does not yet exist.
</when_to_use>

<how_to_use>

## Execution Protocol

1. **Parameter Acquisition (Silent):** Determine `SUBJECT_SYSTEM_NAME` and `AUTHOR_NAME` from current context. Generate a unique `DOCUMENT_ID` (e.g., `ITR-[UUID-4]`).
2. **Template Retrieval (Zero-Reasoning):** Read the exact contents of `c:\AI\10162025\maggie\Antigravity\.agent\assets\schemas\issues-tracker\template.md` into memory. Do NOT interpret, summarize, or apply complex reasoning to it.
3. **Deterministic Token Substitution:** Perform strict, literal string-replacements on the loaded template. Do NOT alter any other text:
   - `{{SUBJECT_SYSTEM_NAME}}` -> Acquired system name.
   - `{{DOCUMENT_ID}}` -> Generated Document ID.
   - `{{YYYY-MM-DD}}` -> Current Date (ISO 8601).
   - `{{AUTHOR_NAME}}` -> Acquired author name.
   - `{{TOTAL_ISSUES_COUNT}}` -> `0`
   - `{{RESOLVED_ISSUES_COUNT}}` -> `0`
4. **Target Provisioning:** Use the `write_to_file` tool to save the resulting string to the target directory.
5. **Concise Verification Artifact:** Produce a single log line confirming initialization success. Do not summarize the contents of the generated tracker (Token Minimization Protocol).

</how_to_use>

## Constraints: <constraints>

- **Anti-Hallucination Protocol:** Do not generate any hallucinated or "example" issues during initialization. The `## ISSUES` section MUST remain completely empty.
- **Zero-Entropy Generation:** Under NO circumstances should you re-write, summarize, or alter the structural layout of the template.
- **Preserve HTML Headers:** Ensure all `<!-- AGENT PARSING HEADER ... -->` comment blocks remain completely intact.
- **Schema Obedience Context Limits:** Do NOT read or cross-validate against `issues-tracker.d.ts` during standard generation to preserve context budget and minimize token utilization.

</constraints>

## Resources: <resources_reference>

- `c:\AI\10162025\maggie\Antigravity\.agent\assets\schemas\issues-tracker\template.md`

</resources_reference>

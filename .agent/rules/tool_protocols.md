---
trigger: always_on
---

# CUSTOM TOOL PROTOCOLS

## PROTOCOL: CONTEXT REGENERATION
**Trigger Phrase:** `/refresh_context`

**Purpose:** Rebuild the Sphinx documentation database and regenerate the flattened LLM context file (`docs/llm_export/context_flat.md`).

**Strict Execution Path:**
If the user input contains the trigger phrase above (exact match):
1.  **Verify Prerequisites:**
    * Check if `.venv/Scripts/python` exists.
    * Check if `.agent/tools/generate_llm_context.py` exists.
    * **IF MISSING:** Output "ERROR: Required tooling not found." and **STOP**.
2.  **Build Sphinx Needs Database:**
    * Execute: `.venv\Scripts\python -m sphinx -b needs docs docs/_build/json`
    * **IF EXIT CODE != 0:** Report Sphinx errors and **STOP**.
3.  **Generate Context:**
    * Execute: `.venv\Scripts\python .agent/tools/generate_llm_context.py docs/_build/json/needs.json docs/llm_export/context_flat.md`
    * **IF EXIT CODE != 0:** Report script errors and **STOP**.
4.  **Verify Success:**
    * Read the first 10 lines of `docs/llm_export/context_flat.md`.
    * Confirm the header: `# Maggie Application Framework - Context Dump`.
5.  **Output:** "Context successfully regenerated. [X] requirements processed."

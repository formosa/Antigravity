---
name: util-python-strip-comments
version: 1.0.2
description: Surgically removes all docstrings and code comments from a targeted Python file while preserving execution logic, formatting, and indentation. Use when the task is to strip non-executable Python comments or docstrings from a specific file. Do not use when the request targets non-Python files or requires manual semantic refactoring.
---

<when_to_use>

- The user requests to clean, sanitize, or strip comments and docstrings from a targeted Python (`.py`) script.
- The user asks to remove non-executable content from Python files while preserving formatting.
- Do not use this skill when the request targets non-Python files or requires hand-edited logic changes beyond comment removal.
- Example prompt: "Strip comments and docstrings from tools/sample.py."
- Example prompt: "Preview comment stripping for scripts/build.py without overwriting the file."
</when_to_use>

<how_to_use>

1. **Context Verification (Silent):**
   - Verify that the target Python file exists at the specified path.
   - Guardrails: NEVER run this skill on files inside `.venv/` or `site-packages/`. NEVER run this on the Agent's own script tools (`.agent/scripts/`) unless explicitly requested.

2. **Execution:**
   - Mandatory Backup: Create a backup copy of the target file in `.sandbox/` before executing the clean operation.
   - Run the sanitization script on the targeted python file using the included script. Do not try to manually parse the python code.
   - Run command: `python .agent/skills/util-python-strip-comments/scripts/strip_comments.py <target_file>`
   - To preview changes without destructive action, use the `--dry-run` flag: `python .agent/skills/util-python-strip-comments/scripts/strip_comments.py <target_file> --dry-run`
   - Review the exit code: Code `0` indicates SUCCESS (Syntax verified, comments removed). Code `1` indicates ERROR (Aborted, syntax check failed, File untouched).

3. **Artifact Generation:**
   - Output the terminal result to the user to confirm the sanitization was successful. Provide a brief summary of the file state.
</how_to_use>

<constraints>
- **Must use the script**. Do not attempt to strip comments manually using IDE edits or regex replacements, as it leads to file corruption.
- Destructive tool. The execution overwrites the target file immediately unless `--dry-run` is used. Always ensure the backup is created.
- The script preserves Shebangs (`#!/...`) and Encoding Headers (`# -*-...`) on lines 1-2. It removes all other comments (including `# type: ignore`) and docstrings.
</constraints>

<resources_reference>

- Run `.agent/skills/util-python-strip-comments/scripts/strip_comments.py` to strip comments and docstrings from the target Python file.
</resources_reference>

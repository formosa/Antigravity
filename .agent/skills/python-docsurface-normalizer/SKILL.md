---
name: python-docsurface-normalizer
version: 1.1.1
description: "Populate or normalize semantically dense NumPy-style docstrings and meaningful code comments in one or more explicitly named Python files using deterministic analysis, grouped preservation gating, and AST-safe verification. Use when the task is to document existing Python code without changing runtime behavior. Do not use when the request is a directory sweep, non-Python edit, or general refactor."
---

<when_to_use>

- Use when the user asks to populate, rewrite, normalize, or standardize docstrings and code comments in one or more explicit Python files.
- Use when the request calls for NumPy-style docstrings, agent-optimized Python documentation, comment preservation review, or comment/docstring stripping before rewrite.
- Do not use when the task is a directory-wide sweep, a non-Python change, a schema or skill contract edit, or a broader code refactor beyond documentation surfaces.
- Example prompt: "Populate NumPy-style docstrings and meaningful comments in `src/config_loader.py` and preserve existing comments if they carry useful semantics."
- Example prompt: "Normalize the docstrings in `tools/build.py`, strip stale comments first, and keep runtime behavior unchanged."
</when_to_use>

<how_to_use>

1. Resolve explicit targets before doing any mutation:
   - Accept only explicitly named `.py` files.
   - Reject directory inputs, glob-style sweep requests, and non-Python targets.
   - Hard-exclude targets under `.archive/`, `.venv/`, `__pycache__/`, `.agent/.temp/`, packaged `.skill` surfaces, and any `resources/schema/` mirror path.
2. Read `resources/aonds-c1-python-docs.md` before generating or rewriting any documentation text:
   - Treat it as the semantic contract for module docstrings, class docstrings, function/method docstrings, and meaningful code comments.
   - Use the helper scripts only for deterministic analysis, stripping, and AST-equivalence checks. Do not treat them as the documentation author.
3. Create a temp snapshot boundary before the first edit:
   - Create one managed temp run directory under `.agent/.temp/` using a timestamp-first task-specific name such as `YYYYMMDD-HHMMSS-python-docsurface-normalizer/`.
   - If a same-second collision occurs, append `-01`, `-02`, and so on to the directory name.
   - Copy every target file into that run directory before editing.
   - Delete the run directory on success. Retain it only on failure and add `retained-on-failure.txt` per `.agent/rules/agent-temp-artifact-hygiene.md`.
4. Analyze all targets first with `scripts/analyze_python_docs.py`:
   - Run the analyzer across the full target set before touching any file.
   - Use `--json` when a structured grouped summary is easier to reason over.
   - Halt immediately if any target is ineligible or has `parse_ok: false`.
5. Apply one grouped preservation gate for the run:
   - If no target reports `preserve_sensitive: true`, proceed without asking.
   - If any target reports `preserve_sensitive: true`, stop once and ask the user which run-wide mode to apply:
     - `preserve`: retain existing non-directive docstrings/comments and adapt them for technical accuracy plus AONDS-C1 alignment.
     - `strip`: remove existing non-directive docstrings/comments first, then repopulate them.
     - `abort`: stop with no file edits.
   - Never use NumPy formatting style as a provenance test. Existing well-structured NumPy docstrings may still be human-authored.
6. Preserve directive and tooling comments in both modes:
   - Keep shebangs, encoding headers, and operative pragmas such as `noqa`, `type: ignore`, `pragma: no cover`, `pyright`, `pylint`, `ruff`, `fmt:`, and `isort:` untouched.
   - In `strip` mode, use `scripts/strip_comments.py <file> --write` only after the grouped user decision is explicit.
7. Rewrite files sequentially, not as one bulk batch:
   - Process one target file at a time.
   - Modify only docstrings and comments unless the user separately asks for code changes.
   - Keep signatures and runtime behavior stable.
8. Run AST-equivalence validation after each rewritten file:
   - Compare the snapshot copy against the modified file with `scripts/compare_ast.py <snapshot> <modified>`.
   - If the comparison fails, restore the original file from the temp snapshot and halt the run.
9. Finish with bounded verification:
   - Re-read the modified file to confirm the docstrings/comments reflect the actual implementation.
   - Report the exact files changed and whether the run used `preserve` or `strip`.
   - Do not package this skill as a `.skill` archive unless the user explicitly asks for packaging.
</how_to_use>

<constraints>
- Do not widen scope from explicit file targets to directory recursion or repo-wide discovery in v1.
- Do not strip or rewrite directive/tooling comments.
- Do not treat comment style, docstring density, or NumPy formatting as evidence that existing documentation is machine-generated.
- Do not proceed when any target is ineligible, unreadable, or syntactically invalid.
- Do not allow AST comparison failures to pass as warnings; restore from the snapshot copy and halt.
- Do not modify code logic, signatures, imports, or control flow unless the user separately changes the task.
- Do not hand-edit vendored schema mirrors under `resources/schema/`; refresh them from `.agent/schemas/` instead.
- Keep skill-local paths repo-relative and written with forward slashes.
</constraints>

<resources_reference>

- Read `resources/aonds-c1-python-docs.md` to apply the full AONDS-C1 documentation-generation contract during rewrite.
- Run `scripts/analyze_python_docs.py` to classify target eligibility, parseability, existing docstrings/comments, and grouped preservation sensitivity before any edits.
- Run `scripts/strip_comments.py` only when the user selects `strip`; it removes non-directive docstrings/comments while preserving directive/tooling comments.
- Run `scripts/compare_ast.py` after each rewritten file to prove the code structure did not change beyond docstrings/comments.
- Read `.agent/rules/agent-temp-artifact-hygiene.md` to keep temp snapshots inside a managed run directory and clean them up correctly.
- Read `resources/schema/skill/skill.d.ts` to confirm the required frontmatter and XML block contract before changing this skill again.
</resources_reference>

---
type: workflow
name: "Document Script (Numpy-style)"
slug: /document_script
description: "Orchestrator. Applies comprehensive Numpy-style docstrings. Features: Shadow Volume, Knowledge Recall, and Artifact Reporting."
mode: autonomous
inputs:
  - name: target_file
    type: file_path
    description: "Path to the Python script (e.g., src/utils/audit.py)"
    required: true
context:
  - ".agent/assets/numpy_style_doc_example.py"
  - "{{inputs.target_file}}"
  - ".agent/knowledge/sources/constraints/isp_numpy_docstrings.md"
outputs:
  - name: documented_file
    type: string
  - name: coverage_report
    type: string
on_finish: "suggest_followup: /rebuild_docs"
---

# Workflow: Document Script (Numpy-style)

## Phase 1: Infrastructure & Knowledge Retrieval
**@tech_lead**: Initialize Shadow Volume and Recall Context.
1.  **Shadow Volume Initialization**:
    * **Execute**:
        ```bash
        python -c "import os; dirs=['.agent/.shadow/{{$executionId}}/artifacts', '.agent/.shadow/{{$executionId}}/temp']; [os.makedirs(d, exist_ok=True) for d in dirs];"
        ```
    * **Set Variables**:
        * `SHADOW_ROOT`: `.agent/.shadow/{{$executionId}}`
        * `ARTIFACTS`: `{{SHADOW_ROOT}}/artifacts`
        * `TEMP`: `{{SHADOW_ROOT}}/temp`

2.  **Knowledge Recall**:
    * **Goal**: Check for historical context or caveats for this specific file.
    * **Directive**: `@knowledge search "Application Notes for {{inputs.target_file}}"`
    * **Output**: Save findings to `{{TEMP}}/legacy_notes.md`.

3.  **Mirroring**:
    * **Execute**: `python -c "import shutil; shutil.copy('${workspaceFolder}/{{inputs.target_file}}', '${workspaceFolder}/{{TEMP}}/original.py')"`

## Phase 2: Generative Intelligence (Attempt 1)
**@tech_lead**: You are the Fiduciary of Code Integrity.
**Context**:
* Reference Style: `.agent/assets/numpy_style_doc_example.py`
* Legacy Notes: `{{TEMP}}/legacy_notes.md`

**Task**: Generate `${workspaceFolder}/{{TEMP}}/modified.py` based on `original.py`.
**Constraints**:
1.  **AST Invariance**: Logic must be identical.
2.  **Artifact Generation**: Create `{{ARTIFACTS}}/plan_summary.md` listing functions to document.

## Phase 3: The "Fail-Fast" Verification Chain (Attempt 1)
**@tech_lead**: Execute serial verification.
1.  **Check 1: Syntax**:
    * `python -m py_compile {{TEMP}}/modified.py` (Stop if fail)

2.  **Check 2: AST Integrity**:
    * Run tool: `/ast_compare`
      * `original_file`: `"${workspaceFolder}/{{TEMP}}/original.py"`
      * `modified_file`: `"${workspaceFolder}/{{TEMP}}/modified.py"`

3.  **Check 3: Coverage Gate (Weaponized)**:
    * **Goal**: Enforce 100% documentation coverage.
    * **Execute**:
        ```bash
        python -c "import ast, json, sys; t=ast.parse(open('{{TEMP}}/modified.py').read()); f={n.name for n in ast.walk(t) if isinstance(n, ast.FunctionDef)}; d={n.name for n in ast.walk(t) if isinstance(n, ast.FunctionDef) and ast.get_docstring(n)}; missing=list(f-d); print(json.dumps({'total':len(f), 'documented':len(d), 'missing': missing})); sys.exit(1) if missing else sys.exit(0)" > {{ARTIFACTS}}/coverage.json
        ```

## Phase 4: Recovery Controller (Retry Logic)
**@tech_lead**: Evaluate Phase 3 results.

**IF Phase 3 Success:**
* **Action**: Proceed to "Deployment" block below.

**IF Phase 3 Failure (Syntax OR AST OR Coverage):**
* **Action**: Initiate Single Retry Loop.
    1.  **Reset**:
        * Respond: "⚠️ Attempt 1 Failed. Resetting Shadow Volume for Retry 1/1."
        * `python -c "import shutil; shutil.copy('${workspaceFolder}/{{TEMP}}/original.py', '${workspaceFolder}/{{TEMP}}/modified.py')"` (Revert to clean slate)
    2.  **Regenerate (Attempt 2)**:
        * **@tech_lead**: Read `{{ARTIFACTS}}/coverage.json` (if available) or AST logs. Re-apply docstrings to `{{TEMP}}/modified.py`, fixing the previous error.
    3.  **Verify (Attempt 2)**:
        * Run **Check 1** (Syntax).
        * Run **Check 2** (`/ast_compare`).
        * Run **Check 3** (Coverage Gate).
    4.  **Final Decision**:
        * **IF Success**: Proceed to "Deployment".
        * **IF Failure**:
            * Respond: "⛔ CRITICAL FAILURE: Retry exhausted. System state unchanged. Check `{{ARTIFACTS}}` for logs."
            * **ABORT WORKFLOW**.

## Deployment (Success State)
**@tech_lead**: Only executed if Verification passes (Attempt 1 or 2).
1.  **Atomic Swap**:
    * `python -c "import shutil; shutil.move('${workspaceFolder}/{{TEMP}}/modified.py', '${workspaceFolder}/{{inputs.target_file}}');"`
2.  **Knowledge Crystallization**:
    * `@knowledge save "Application Notes {{inputs.target_file}}" --content-file "{{ARTIFACTS}}/plan_summary.md"`
3.  **Cleanup**:
    * `python -c "import shutil; shutil.rmtree('${workspaceFolder}/{{SHADOW_ROOT}}', ignore_errors=True)"`
    * Respond: "✅ Documentation complete. Coverage report saved to Knowledge Base."

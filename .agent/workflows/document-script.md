---
type: workflow
name: "Document Script (Numpy-style)"
slug: /document-script
description: "Orchestrator. Applies comprehensive Numpy-style docstrings to a targeted Python file. Enforces strict AST verification to ensure zero logic alteration."
mode: autonomous
inputs:
  - name: target_file
    type: file_path
    description: "Path to the Python script (e.g., src/utils/audit.py)"
    required: true
context:
  - ".agent/workflows/assets/numpy-style-doc-example.py"
  - "{{inputs.target_file}}"
---

# Workflow: Document Script (Numpy-style)

## Phase 1: Infrastructure & Safety
**@system**: Initialize the secure environment.
1.  **Sandboxing**:
    * Run tool: `/generate_uuid`
    * Set variable `SANDBOX_ID` from output.
    * Set variable `SANDBOX_DIR` to `.agent/.sandbox/document-script-{{SANDBOX_ID}}`.

2.  **Pre-Flight Syntax Check**:
    * Execute command:
        ```powershell
        & "${workspaceFolder}/.venv/Scripts/python.exe" -m py_compile "${workspaceFolder}/{{inputs.target_file}}"
        ```
    * *Constraint*: If this command fails, **ABORT WORKFLOW** immediately.

3.  **Staging (Atomic Backup)**:
    * Execute command:
        ```powershell
        New-Item -ItemType Directory -Force -Path "${workspaceFolder}/{{SANDBOX_DIR}}"
        Copy-Item "${workspaceFolder}/{{inputs.target_file}}" "${workspaceFolder}/{{SANDBOX_DIR}}/original.py"
        ```

## Phase 2: Generative Intelligence
**@coder**: You are the Fiduciary of Code Integrity.
**Task**: Read `${workspaceFolder}/{{SANDBOX_DIR}}/original.py`. Generate a fully documented version and save it to `${workspaceFolder}/{{SANDBOX_DIR}}/modified.py`.

**Strict Constraints:**
1.  **AST Invariance**: Logic, variable names, and operation order must remain IDENTICAL.
2.  **Style**: Apply **Numpy-style** docstrings strictly matching the `numpy-style-doc-example.py` in your context.
3.  **Legacy Preservation**: Merge existing "Application Notes" into the new `Notes` or `See Also` sections. Do not delete technical insights.

**Required Schema:**
* **Modules/Classes/Methods/Exceptions**: Summary + applicable sections (Parameters, Returns, Raises, etc.).
* **Type Hints**: MUST be included in the `Parameters` docstring section.

## Phase 3: Gatekeeper Verification
**@system**: Verify AST integrity.
1.  Run tool: `/ast_compare`
    * `original_file`: `"${workspaceFolder}/{{SANDBOX_DIR}}/original.py"`
    * `modified_file`: `"${workspaceFolder}/{{SANDBOX_DIR}}/modified.py"`

## Phase 4: Final Loop (Auto-Remediation)
**@coder**: Analyze the result of Phase 3.

**IF Exit Code == 0 (Success):**
* **@system**:
    ```powershell
    Copy-Item "${workspaceFolder}/{{SANDBOX_DIR}}/modified.py" "${workspaceFolder}/{{inputs.target_file}}" -Force
    Remove-Item "${workspaceFolder}/{{SANDBOX_DIR}}" -Recurse -Force
    ```
* Respond: "✅ Success: Docstrings applied and verified. Sandbox cleaned."

**IF Exit Code == 1 (Logic Mismatch):**
* **Action**: You have ONE attempt to fix this.
    1.  Read the diff from the AST tool.
    2.  Rewrite `${workspaceFolder}/{{SANDBOX_DIR}}/modified.py` to fix the logic error while keeping the docs.
    3.  Run tool `/ast_compare` again.
    4.  **IF Success**: Perform the deployment commands from the "Success" block above.
    5.  **IF Failure**:
        * Respond: "⛔ CRITICAL FAILURE: Logic alteration detected. Unsafe file preserved at `{{SANDBOX_DIR}}/modified.py`."
        * **DO NOT** overwrite the user's file.

**IF Exit Code == 2 (System Error):**
* Respond: "⚠️ System Error during AST verification. Process halted."

---
type: workflow
name: "Update Documentation Spec"
slug: /update_documentation_spec
description: "Process for updating the Maggie Design Specifications (Sphinx-Needs)."
mode: interactive
inputs: []
context:
  - "docs/llm_export/context_flat.md"
  - "@design_lead"
on_finish: "suggest_followup: /rebuild_docs"
---

This workflow defines the strict protocol for adding or modifying design specifications (Requirements, Specs, Architecture, etc.) in the Sphinx-Needs system. Adherence ensures data integrity, traceability, and valid build outputs.

# 1. Analysis & ID Strategy
1.  **Source of Truth (READ ONLY):**
    *   ALWAYS read `docs/llm_export/context_flat.md` first to understand the current system state, relationships, and parents.
    *   Do **NOT** attempt to edit the `.html` or `.md` files directly. These are build artifacts.
2.  **Edit Targets (WRITE):**
    *   Updates must ONLY be made to the `docs/**/*.rst` source files:
        *   `01_brd/brd.rst` (Business Goals)
        *   `02_nfr/nfr.rst` (Constraints)
        *   `03_fsd/fsd.rst` (Features/Behavior)
        *   `04_sad/sad.rst` (Structure/Patterns)
        *   `05_icd/icd.rst` (Data/Schemas)
        *   `06_tdd/tdd.rst` (Classes/Functions)
        *   `07_isp/isp.rst` (Implementation Prompts)
2.  **Determine IDs:**
    *   Find the next available ID in the sequence (e.g., if `FSD-10.2` exists, use `FSD-10.3`).
    *   **Atomic Convention:** If refining an existing item, use dot-notation (e.g., child of `SAD-1` is `SAD-1.1`).
3.  **Traceability:**
    *   Identify the **Parent ID** (e.g., new FSD must link to a BRD or NFR).

# 2. Update Specification (RST)
Edit the target `.rst` file. Use the following template:

```rst
.. <type>:: <Title Summary>
   :id: <ID>
   :links: <PARENT_ID>
   :status: open

   <Detailed Description Text>

   .. mermaid::

      graph TD
         A[Node] --> B[Node]
```

*   **Valid Types:** `brd`, `nfr`, `fsd`, `sad`, `icd`, `tdd`, `isp`.
*   **Visualization:** Prefer `.. mermaid::` blocks over ASCII art for complex relationships (Architecture/Flows).
    *   **Strict Syntax:** ALWAYS quote node labels (e.g., `Node["Node Label"]`).
    *   **Layout:** Use `graph LR` for process flows to maximize readability.
    *   **Style:** Use rounded corners (`rx:5,ry:5`) and semantic colors (Blue=Core, Orange=Service, Green=Sink).
    *   **Directive:** Ensure a blank line exists between `.. mermaid::` and the graph definition.
*   **ID Regex:** Must match `^[A-Z0-9\-\.]+$` (No spaces, use dashes or dots).

# 3. Compile & Validate (The Build)
// turbo
Execute the Sphinx build to validate links and syntax.
```powershell
.venv\Scripts\python -m sphinx -b html docs docs/_build/html
```

**Validation Check:**
*   If the output contains `WARNING:`, **STOP**.
*   Fix the issue (usually a broken link or duplicate ID).
*   Re-run until the build is clean.

# 4. Regenerate LLM Context
// turbo
Once the build is clean, regenerate the flattened context file for the Agent.
```powershell
.venv\Scripts\python .agent/tools/generate_llm_context.py docs/_build/json/needs.json docs/llm_export/context_flat.md
```

# 5. Final Verification
1.  Read `docs/llm_export/context_flat.md`.
2.  Verify the new item appears in the text and has the correct `-> LINK` pointers.

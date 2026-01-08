---
name: "Traceability Audit"
slug: /traceability_audit
description: "Detailed routine for conducting a precise internal traceability tag audit."
mode: autonomous
inputs: []
context:
  - "docs/llm_export/context_flat.md"
  - "@design_lead"
on_finish: "suggest_task: Remediation Plan"
---

This workflow defines the process for validating documentation integrity, tag inventory accuracy, and design logic consistency.

# 1. Inventory & Tag Scan
1.  **Scan for IDs:**
    *   Find all occurrences of `:id: <TYPE>-<NUM>` in `docs/**/*.rst`.
    *   Compare counts against `reconciliation_manifest.rst` in each folder.
2.  **Verify Append-Only:**
    *   Ensure no IDs have been deleted or skipped in the sequence.
    *   Check for duplicates (e.g., TDD-2.6).

# 2. Traceability (Link) Validation
1.  **Check Outgoing Links:**
    *   For each item, verify `:links: <PARENT_ID>` exists and points to a valid ID.
2.  **Verify Causal Hierarchy:**
    *   BRD -> NFR (Constraint)
    *   NFR -> FSD (Specification)
    *   FSD -> SAD (Architecture)
    *   SAD -> ICD (Contract)
    *   ICD -> TDD (Blueprint)
    *   TDD -> ISP (Prompt)
3.  **Detect Orphans:**
    *   Identify any item missing a required parent link (The Orphan Rule).

# 3. Terminology & Logic Audit
1.  **Glossary Compliance:**
    *   Verify all descriptions use terms defined in `docs/00_glossary/terms.rst`.
    *   Flag non-compliant terms (e.g., using "Manager" instead of "Core Process").
2.  **Lateral Dependency Check:**
    *   Ensure items do not link to sibling items (Same level in hierarchy).
3.  **Atomicity Check:**
    *   Ensure each item (ICD/TDD/ISP) is atomic and does not conflate concerns.

# 4. Report & Reconciliation
1.  **Generate Report:**
    *   List all broken links, duplicates, orphans, and terminology violations.
2.  **Update Manifests:**
    *   If issues found, set `:integrity_status: DIRTY` in the relevant section's `reconciliation_manifest.rst`.
    *   List specific issues in `:pending_items:`.
3.  **Correction:**
    *   Fix identified issues in source RST files.
    *   Once fixed, update status back to `CLEAN`.

// turbo
# 5. Build & Export
1.  Run the Sphinx build to verify final syntax.
    ```powershell
    .venv\Scripts\python -m sphinx -b html docs docs/_build/html
    ```
2.  Regenerate the LLM context.
    ```powershell
    .venv\Scripts\python .agent/scripts/generate_llm_context.py docs/_build/json/needs.json docs/llm_export/context_flat.md
    ```

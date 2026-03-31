---
task: "Repair the DDR v6.3 reference manual against the v6.3 YAML SSOT while preserving the existing inline-style documentation pattern."
model: "gemini-3.1-pro"
version: "1.0.0"
# HUMAN CONTEXT: This plan is approved for execution. Scope is markdown-only and
# document-only: repair `ddr_ref_manual_v6.3.md`, do not modify the SSOT YAML
# pair, do not add a validator script, and do not regenerate the PDF in this
# pass.
---

<objective>
Produce a corrected, renderer-consistent version of `.agent/assets/proposals/active/v6.3/ddr_ref_manual_v6.3.md` that is fully aligned with `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml` and `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml`. The execution must fix the audited manual defects already identified in the approved plan: incomplete CSS/class coverage for semantic badges and labels, exact-value drift in metadata and note surfaces, under-modeled reconciliation-manifest and advisory behavior, imprecise authority-basis selectors, and any Mermaid figure that weakens or omits machine-significant content. The pass must preserve the repo's inline-style markdown convention, keep scope limited to the reference manual, and leave the SSOT YAML and PDF artifact untouched.
</objective>

<phases>
- phase_id: "PHASE_1_CORRECTION_LEDGER"
  objectives: ["Map every manual section to the authoritative YAML/schema source surfaces", "Turn the approved audit findings into an execution ledger with exact repair targets"]
  task_references: ["DOC-RM-001", "DOC-RM-002", "DOC-RM-003"]
  entry_criteria: ["The active v6.3 manual, schema, and system-definition files are readable", "The approved implementation plan is present"]
  exit_criteria: ["Every section in the manual has a mapped SSOT basis", "All previously identified issues are translated into concrete edit targets before prose changes begin"]
  assigned_model: "gemini-3.1-pro"
- phase_id: "PHASE_2_PRESENTATION_AND_SELECTOR_REPAIR"
  objectives: ["Repair the inline CSS/class contract so all rendered semantics have real definitions", "Normalize authority-basis references to valid, unambiguous source selectors"]
  task_references: ["DOC-RM-004", "DOC-RM-005", "DOC-RM-006"]
  entry_criteria: ["PHASE_1_CORRECTION_LEDGER complete"]
  exit_criteria: ["Every used `.ddr-*` class is defined in the style block", "No authority-basis callout relies on pseudo-path notation"]
  assigned_model: "gemini-3.1-pro"
- phase_id: "PHASE_3_SSOT_FIDELITY_REMEDIATION"
  objectives: ["Repair all machine-significant wording drift in core sections", "Restore omitted manifest, ARE, and extension semantics where the manual currently compresses the source too aggressively"]
  task_references: ["DOC-RM-007", "DOC-RM-008", "DOC-RM-009", "DOC-RM-010"]
  entry_criteria: ["PHASE_2_PRESENTATION_AND_SELECTOR_REPAIR complete"]
  exit_criteria: ["Sections 2, 7, 8, and 10 are textually aligned with the SSOT on exact-value and machine-significant surfaces", "No known approved-audit issue remains unresolved in the markdown"]
  assigned_model: "gemini-3.1-pro"
- phase_id: "PHASE_4_DIAGRAM_AND_APPENDIX_RECONCILIATION"
  objectives: ["Reconcile all Mermaid figures with the repaired prose/tables", "Ensure appendices, counts, crosswalks, and quick references remain accurate after the core repairs"]
  task_references: ["DOC-RM-011", "DOC-RM-012", "DOC-RM-013"]
  entry_criteria: ["PHASE_3_SSOT_FIDELITY_REMEDIATION complete"]
  exit_criteria: ["Each Mermaid figure is either source-faithful or removed/simplified", "Appendices and study aids no longer contradict the repaired core sections"]
  assigned_model: "gemini-3.1-pro"
</phases>

<atomic_steps>

1. Create an execution ledger that maps each major manual section (`1` through `10`) to the exact YAML/schema surfaces that govern it, and list the already-audited defects under the owning section before modifying the markdown.
2. Inspect the top `<style>` block and enumerate every `.ddr-*` class actually used in the manual; add concrete definitions for every missing semantic surface, label, status, verification, mode, constraint, and edge class rather than inventing new class names.
3. Preserve the existing inline-style markdown pattern used by this repo, but normalize it so badges and labels share one coherent visual system and no rendered element depends on an undefined selector.
4. Repair Section `2.1` so exact-value metadata surfaces match the authoritative YAML verbatim where precision matters, especially `project.name` and `system_metadata.single_source_of_truth`.
5. Review Sections `3` through `6` for any condensed wording that drops machine-significant qualifiers; keep summaries concise, but restore exact conditions whenever a paraphrase changes the operational meaning of rules, guards, invariants, or citations.
6. Rewrite every `Authority basis` callout to use valid source references. For list-based YAML surfaces, use selector wording such as `operations.core_operations[name=SUPERSEDE]` instead of pseudo-object paths like `operations.core_operations.SUPERSEDE`.
7. Repair Section `7.3` so the reconciliation-manifest narrative explicitly models both `pending_items` and `extension_advisories`, and so the manifest schema description matches the authoritative structure and later CLEAN-state logic.
8. Reconcile Section `7.5` and related quick-reference text so advisory disposition, pending-item handling, and semantic-gap handling are internally consistent and do not imply that pending items are the only manifest-level blockers.
9. Repair Section `8.3` so ARE candidate-pool semantics reflect the authoritative checkpoint, visibility, and promotion behavior without dropping machine-significant details.
10. Repair Sections `8.4` and `8.5` so E5 and E7 notes match the SSOT exactly where the current manual weakens or alters intent, including E5 annotation-boundary wording, checkpoint payload semantics, and the E7 forward-reference advisory semantics.
11. Review all Mermaid figures in Sections `1` through `9`; if a figure omits a surface the adjacent prose treats as authoritative, redraw it to match the repaired content. If a figure adds no explanatory value after the repair, simplify or remove it instead of preserving decorative duplication.
12. Keep Mermaid usage inside the manual's declared stable subset; do not introduce renderer-specific syntax while repairing figures.
13. Recompute and verify Appendix `10.4` counts against the YAML pair after all content edits, then update Appendix `10.5` source crosswalk rows wherever repaired sections now expose fuller SSOT coverage.
14. Re-read Appendices `10.6` through `10.11` after the core repairs and update any quick-reference, pro-tip, or Q&A text that still reflects the pre-repair wording.
15. Perform a final markdown integrity pass: balanced HTML tags, balanced code fences, valid section numbering, consistent heading text, and a table of contents that still points to the repaired section names.
16. Leave `.agent/assets/proposals/active/v6.3/ddr_system_v6.3.yaml`, `.agent/assets/proposals/active/v6.3/ddr_node_schema_v6.3.yaml`, and `.agent/assets/proposals/active/v6.3/ddr_ref_manual_v6.3.pdf` unchanged throughout the pass.
</atomic_steps>

<verification>
1. Verify every used `.ddr-*` class in `ddr_ref_manual_v6.3.md` is defined in the top style block and that no class definition remains unused in a way that suggests stale design drift.
2. Verify the repaired metadata table in Section `2.1` matches the authoritative YAML values exactly for `project`, `system_metadata`, and `errata_log`.
3. Verify all cited rule IDs, invariant IDs, extension IDs, operation names, guard IDs, and tier IDs still match the SSOT after the prose edits.
4. Verify every `Authority basis` callout points to a real schema/spec surface or an explicit selector over a real list-based surface.
5. Verify Section `7.3` now covers both manifest pending items and extension advisory handling, and that Section `7.5` CLEAN logic uses the same terminology.
6. Verify Section `8` now preserves the authoritative E5 and E7 note semantics without introducing new interpretation beyond the SSOT.
7. Verify each Mermaid figure still matches its adjacent table or prose after the edits, and that no diagram contradicts the repaired section.
8. Verify Appendix `10.4` counts match the schema/spec-derived totals for top-level properties, rules, operations, extensions, guards, nodes, and errata entries.
9. Verify Appendix `10.5` crosswalk rows still point to the correct repaired sections and do not reference a section that no longer carries the claimed content.
10. Verify quick-reference, pro-tip, and Q&A sections do not reintroduce the repaired inaccuracies through shorthand restatements.
11. Verify HTML tags, fenced code blocks, and markdown tables remain structurally balanced and readable after the edit pass.
12. Verify the YAML SSOT pair and the PDF companion artifact remain byte-for-byte untouched in scope terms, with the markdown manual as the only modified deliverable.
</verification>

<risks_and_mitigations>

- **Risk:** The executor repairs visible prose but misses secondary drift in appendices, quick references, or Q&A sections.
  **Mitigation:** Require a deliberate Appendix `10.4` through `10.11` reconciliation step after all core edits, not before.

- **Risk:** Styling is "fixed" by adding ad hoc classes or redesigning the document away from the repo's current inline-style convention.
  **Mitigation:** Preserve the existing `ddr-*` naming scheme and repair missing definitions instead of introducing a new styling system.

- **Risk:** Authority-basis references remain human-readable but technically imprecise, leaving the manual harder to audit later.
  **Mitigation:** Normalize all list-member references to explicit selector syntax and reject pseudo-object paths during the final review.

- **Risk:** ARE and reconciliation-manifest sections are summarized too aggressively and lose machine-significant qualifiers again.
  **Mitigation:** Treat Sections `7` and `8` as exactness-critical surfaces and prefer SSOT-faithful wording over editorial compression in those areas.

- **Risk:** Mermaid figures become inconsistent with repaired prose or keep legacy omissions because they were reviewed too early.
  **Mitigation:** Perform figure review only after prose and tables are stable, and allow removal or simplification when a figure no longer improves comprehension.

- **Risk:** Scope expands into SSOT YAML edits, PDF export, or new tooling.
  **Mitigation:** Enforce the approved scope boundary explicitly in the artifact and final verification: markdown-only, document-only, no validator, no PDF regeneration.
</risks_and_mitigations>

---
task: Repair DDR v6.3 Canonical Specification Markdown Parity and Presentation
model: gemini-3.1-pro
version: 1.0.0
---

# DDR v6.3 Canonical Specification Repair

## Issue Matrix

| Concern ID | Issue of Concern | Target Location | Authority Surface | Repair Action | Verification Gate |
| --- | --- | --- | --- | --- | --- |
| IOC-01 | Title block and opening authority note imply a competing SSOT instead of a YAML-first authority hierarchy. | `DDR System(v6.3).md` opening metadata block and authority note | `ddr_system_v6.3.yaml.system_metadata.single_source_of_truth`, `ddr_ref_manual_v6.3.md §10.5` | Rewrite the opening block so the Markdown is the canonical human-readable rendering of the authoritative YAML pair and explicitly states conflict precedence. | Manual spot-check of opening block plus `audit.py` coverage check for authority text and root metadata fields. |
| IOC-02 | Root/profile machine contract is underexposed in the canonical Markdown. | New preamble/root-contract section near the top of `DDR System(v6.3).md` | `ddr_node_schema_v6.3.yaml` top-level `document_profile`, `project`, `active_tiers`, `allOf` branches | Add compact root contract tables covering `ddr_version`, `document_profile`, `project`, canonical `active_tiers`, profile branching, and required system-definition surfaces. | `audit.py` checks for required root/profile coverage phrases and section presence. |
| IOC-03 | Critical schema-side constructs are absent or only implicitly documented. | `§3.1`, `§3.8`, `§9`, new appendix crosswalk | `ParentCitation`, lifecycle status transitions and guards, rule-ID families, reserved extension shadow-key blocking | Add compact source-derived coverage for `ParentCitation`, lifecycle guard/transition authority, rule-ID typing, and extension-annotation restrictions without altering existing major numbering. | `audit.py` checks for `ParentCitation`, lifecycle guards, rule-ID families, and reserved shadow-key language. |
| IOC-04 | Navigation and reading flow are weak for a 1,100+ line spec. | Top of document, section intros, appendix area | Canonical Markdown only | Add a table of contents, short lead-in sentences for dense sections, a root-contract quick reference, and a YAML-surface-to-section crosswalk appendix. | Manual spot-check of TOC, lead-ins, quick-reference tables, and appendix crosswalk. |
| IOC-05 | Mermaid coverage is too thin and current diagrams lack explicit accessibility metadata policy. | Existing architecture diagram plus new diagrams near related sections | `brainstorm.md §8.2` Mermaid rules | Replace the single-diagram approach with a stable-only Mermaid suite and require `accTitle` and `accDescr` on every block. | `audit.py` checks every Mermaid block for `accTitle` and `accDescr`. |

<objective>
Repair the DDR v6.3 canonical Markdown specification so it stays aligned with the authoritative YAML pair, exposes the missing v6.3 machine-contract surfaces, improves navigation and auditability, and upgrades Mermaid coverage/accessibility without changing any public YAML or schema interfaces.
</objective>

<phases>

### PH-01 Baseline and Traceability

- Capture the execution scope and lock the no-YAML-mutation boundary.
- Map each identified Markdown concern to a concrete YAML or schema authority surface.
- Preserve all existing major section numbers already referenced by the YAML pair, especially `§3.1` through `§3.8`.

### PH-02 Canonical Markdown Repair

- Rewrite the opening authority model and expand the root metadata surface.
- Add TOC, root-contract quick reference, compact schema-surface inserts, and appendix crosswalk material.
- Introduce the stable-only Mermaid suite with nearby authoritative prose/tables.

### PH-03 Audit Hardening and Validation

- Extend `audit.py` so it checks Markdown parity coverage, Mermaid accessibility metadata, and crosswalk completeness.
- Run YAML schema validation, Markdown parity audit, and manual spot checks in the required order.
- Leave a final verification summary tied to the repaired surfaces.

</phases>

<atomic_steps>

1. Create this implementation artifact in `.agent/plans/` and record the execution boundary.
2. Rewrite the canonical Markdown opening block to establish YAML-first authority precedence.
3. Add a root-contract preamble covering `ddr_version`, `document_profile`, project coupling, and `system_definition` required surfaces.
4. Add a table of contents near the top and short lead-in sentences ahead of dense major sections.
5. Insert compact `ParentCitation` coverage and lifecycle quick-reference coverage without renumbering existing `§3.1` through `§3.8`.
6. Expand the schema-validation surface discussion to include rule-ID family closure and reserved extension shadow-key blocking.
7. Add a small stable-only Mermaid suite: authority hierarchy, profile branching, Express unbundle flow, lifecycle state machine, and updated architecture diagram.
8. Add an appendix mapping YAML/schema surfaces to Markdown sections.
9. Extend `audit.py` to verify metadata/root coverage, rule coverage, Mermaid accessibility metadata, and crosswalk completeness.
10. Run validation in the required order and record any failures as blocking.

</atomic_steps>

<verification>

1. Confirm no edits were made to `ddr_system_v6.3.yaml`, `ddr_node_schema_v6.3.yaml`, or `ddr_ref_manual_v6.3.md`.
2. Validate `ddr_system_v6.3.yaml` against `ddr_node_schema_v6.3.yaml` successfully.
3. Run the extended `audit.py` and require a clean parity result.
4. Manually inspect the title block, `document_profile` coverage, lifecycle section, ARE profile section, appendix crosswalk, and every Mermaid diagram.
5. Treat any mismatch between YAML section references and preserved Markdown section numbering as a hard failure.

</verification>

<risks_and_mitigations>
The highest risk is accidentally creating a second interpretation layer that drifts from the YAML authorities or renumbering sections already referenced by the YAML pair. Mitigate by using source-derived wording for high-precision statements, limiting new numbered insertions to preamble/additive subsection forms, validating all authoritative rule IDs remain present, and treating numbering drift or Mermaid accessibility omissions as blocking failures.
</risks_and_mitigations>

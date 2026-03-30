# DDR System v6.3 Reference Manual Enhancement Implementation Plan

## Summary

This plan defines a conservative enhancement pass for:

- `ddr_ref_manual_v6.3.md`

The target outcome is a structurally improved reference manual that is easier to enter and navigate without changing its authority model, section coverage, or factual scope.

This audited version also closes the main weakness in the prior draft: it now protects the full v6.3 system-definition surface and the Section `9` schema branches explicitly, rather than relying on broad summary language alone.

Normative validation baseline:

- `ddr_system_v6.3.yaml`
- `ddr_node_schema_v6.3.yaml`

Presentation cross-check only:

- `DDR System(v6.3).md`

## Decision Locks

- Treat the YAML pair as the normative SSOT for all decisions in this plan.
- Preserve the current manual as a reference artifact, not a tutorial or worked-example guide.
- Preserve the existing `1-10` section numbering and current anchor scheme; do not convert the manual to Sonnet-style chapter numbering.
- Do not rename existing H2 or H3 headings; use additive lead-ins, routing tables, and cross-reference lines instead of anchor-affecting heading rewrites.
- Preserve the current authoritative coverage footprint: source basis, overview/design philosophy, core model, tier reference, lifecycle/operations, consumption modes, reconciliation/CLEAN, extensions/ARE, schema contract, appendices.
- Preserve the dedicated schema section, authoritative-counts appendix, and final source crosswalk.
- Preserve the current low-diagram discipline; do not exceed the existing four Mermaid diagrams.
- Do not introduce new normative DDR facts, new rules, new examples beyond source-native examples, or new business-context claims.
- Preserve source-native examples only: representative topology nodes, canonical `active_tiers` variants, lifecycle transitions, Express Mode groups, manifest item types, extension entries, and scoring profiles already grounded in the YAML pair.

## Protected Source Surface Matrix

The enhancement pass is additive only. Every protected surface below must remain present and clearly discoverable after implementation.

### System-definition surfaces

| Source surface | Current manual coverage | Preservation rule |
| --- | --- | --- |
| `project`, `system_metadata` | Sections `1.2`, `2.1`, `2.2`, `2.3` | Keep current source-basis and metadata coverage intact; improvements may clarify orientation, not remove metadata detail. |
| `errata_log` | Sections `2.4`, `10.4` | Preserve explicit errata-state coverage in both overview and appendix form. |
| `axioms` | Section `3.1` | Preserve the full axiom lookup table and its direct source-derived framing. |
| `node_schema_fields` | Sections `3.5`, `9.3` | Preserve both the conceptual node-format discussion and schema-surface lookup. |
| `edge_type_definitions` | Section `3.7` | Preserve dedicated edge-type treatment as a current-state reference surface. |
| `dag_invariants` | Section `3.9` | Preserve the invariant lookup table as a standalone reference unit. |
| `node_id_format` | Section `3.6` | Preserve node-ID coverage as a standalone structural rule surface. |
| `citation_rules` | Section `3.8` | Preserve dedicated citation-rule coverage and `ParentCitation` linkage. |
| `nodes`, `tier_definitions` | Sections `3.4`, `4.1-4.9` | Preserve representative topology coverage and full tier-by-tier reference coverage. |

### Operational, extension, and appendix surfaces

| Source surface | Current manual coverage | Preservation rule |
| --- | --- | --- |
| `consumption_modes` | Section `6.1` | Preserve both declared modes and their purpose split. |
| `express_mode.description`, `groups`, `unbundle_determinism_rule`, `deferred_fragment_handling` | Sections `6.2-6.4` | Preserve the four groups, deterministic unbundling rules, and deferred-fragment handling as distinct lookup surfaces. |
| `constraint_precedence` including `constraint_classes`, `physical_constraint_rule`, `physical_constraint_escalation` | Sections `7.1-7.2` | Preserve the physical-vs-logical constraint treatment and escalation rules explicitly. |
| `operations.core_operations` | Section `5.4` | Preserve the canonical operation table as a standalone lookup surface. |
| `operations.dirty_flag_triggers`, `dirty_flag_notes`, `dirty_classification`, `supersede_dirty_behavior` | Section `5.5` | Preserve DIRTY behavior as a dedicated subsection; do not collapse it into generic lifecycle prose. |
| `operations.resolution_workflow`, `conflict_resolution_protocol`, `semantic_consistency_rules` | Sections `5.4`, `5.6`, `7.5` | Preserve workflow, conflict handling, and semantic-consistency review visibility. |
| `operations.reconciliation_manifest_tracks`, `reconciliation_manifest_schema` | Section `7.3` | Preserve both manifest track inventory and manifest item schema detail. |
| `extension_system`, `extension_catalog`, `are_scoring_profiles` | Sections `8.1-8.5` | Preserve extension architecture, catalog entries, candidate-pool behavior, and ARE profiles as separate surfaces. |
| `compliance_checklist` | Sections `7.4-7.5` | Preserve compliance categories and CLEAN-state logic. |
| `glossary`, `version_history`, `tier_migration` | Sections `10.1-10.3` | Preserve all three appendices separately; do not merge them. |
| Derived audit surfaces: authoritative counts and source crosswalk | Sections `10.4-10.5` | Preserve both appendices because they are now part of the baseline manual’s integrity model. |

### Schema surfaces already surfaced by the current manual

| Source surface | Current manual coverage | Preservation rule |
| --- | --- | --- |
| Schema root: `document_profile` branching and `system_definition` required surface | Sections `3.2`, `9.1` | Preserve explicit profile branching and authoritative-root requirements. |
| Schema root: `active_tiers` canonical variants | Sections `3.3`, `9.2` | Preserve the four canonical ordered variants. |
| Schema `$defs.DdrNode` | Sections `3.5`, `9.3` | Preserve field-level coverage of the node contract. |
| Schema `$defs.ParentCitation` | Sections `3.8`, `9.4` | Preserve typed-parent citation coverage as its own schema surface. |
| Schema express-specific rules including `project_instance_express` obligations and `ExpressModeGroup` | Sections `6.2-6.4`, `9.5` | Preserve express-profile obligations and the closed group system. |
| Schema extension/ARE rules including `ExtensionEntry`, `ScoringProfile`, and activation-state typing | Sections `8.3-8.5`, `9.6` | Preserve the schema-side treatment of extension and ARE structures. |
| Schema lifecycle rules including `StatusTransition`, `GuardDefinition`, `StatusEnum`, and guard references | Sections `5.2-5.3`, `9.7` | Preserve lifecycle schema detail separately from narrative lifecycle explanation. |

## Implementation Safety Rules

- Treat every approved enhancement as an additive presentation layer over the existing manual; do not use any enhancement as justification to collapse or merge source-derived tables.
- Do not delete, merge, or rename Appendix sections `10.1` through `10.5`.
- Do not move legacy terminology into Sections `1` through `9`.
- Do not replace existing source-derived tables with prose summaries unless the table is being preserved and the prose is strictly introductory.
- Do not add a new diagram. If a visual needs clarification, improve surrounding prose rather than expanding the diagram surface.
- If any enhancement conflicts with a protected source surface in the matrix above, the enhancement loses and must be skipped.

## Approved Enhancements

| ID | Change | Classification | Exact action | Source inspiration |
| --- | --- | --- | --- | --- |
| `EH-1` | Add macro-navigation above the existing TOC | `structure only` | Insert a `Manual Map` block between the opening authority paragraph and the existing TOC. Group the current sections as: `Part I - Authority and Orientation (Sections 1-2)`, `Part II - Core Model and Tiers (Sections 3-4)`, `Part III - Operations, Modes, and Reconciliation (Sections 5-7)`, `Part IV - Extensions and Validation Surface (Sections 8-9)`, `Part V - Appendices and Crosswalk (Section 10)`. | `Sonnet` |
| `EH-2` | Tighten reader-entry guidance | `manual-local context` | Replace the current single `How to use this manual` lookup table with a role/task matrix that includes: `New reader`, `Tier author/reviewer`, `Validator/tool author`, `Extension implementer`, `Audit/history reader`. Keep all routing targets within the current section numbering. | `ChatGPT`, `Sonnet` |
| `EH-3` | Add section-purpose lead-ins | `manual-local context` | Add a one-paragraph lead-in immediately under each H2 section heading from Sections `1` through `10`. Each lead-in must state what authority surface the section covers and what adjacent section handles the next level of detail. Keep each lead-in to `1-2` sentences. | `Sonnet`, `Gemini` |
| `EH-4` | Add standardized cross-reference cues | `manual-local context` | Add a final flat line at the end of Sections `3` through `9` in the form `See also: Section X, Section Y, Section Z.` Use these fixed mappings: `3 -> 4, 5, 9`; `4 -> 3, 5, 7`; `5 -> 6, 7, 9`; `6 -> 5, 9`; `7 -> 5, 9, 10`; `8 -> 9, 10`; `9 -> 3, 5, 6, 8`. | `ChatGPT`, `Sonnet` |
| `EH-5` | Sharpen authority wording at the front | `source-derived clarification` | Keep the existing opening authority text, but tighten the distinction so the opening explicitly says the manual is source-derived from the semantic system definition and the machine-contract schema, with the YAML pair controlling on divergence. Do not add any new authority sources. | `Codex` |
| `EH-6` | Preserve appendix boundary discipline | `source-derived clarification` | Insert one short historical-scope note immediately before Section `10.2`, explicitly applying to Sections `10.2-10.3`: legacy tier names, removed operations, and migration mappings in those appendices are historical vocabulary only and are not current-state DDR terms. | Baseline, reinforced by `Sonnet` and `Codex` drift observations |

## Explicit Non-Goals

- No rewrite-from-scratch pass
- No new chapter system
- No expansion into business/industry motivation sections
- No scenario library
- No worked-example appendix
- No anti-pattern chapter
- No extra Mermaid diagrams
- No frontmatter
- No image metadata
- No image references
- No inline payloads

## Rejected Ideas

| Rejected idea | Why it is rejected |
| --- | --- |
| Add an executive overview or business-context chapter ahead of the source-basis opening | Not required by the YAML-led authority surface and would expand the manual beyond reference scope |
| Add tutorial scenarios throughout the manual | Would dilute lookup density and increase drift pressure |
| Add separate anti-pattern or failure-mode chapters | Useful in a tutorial, but out of scope for a strict reference enhancement pass |
| Adopt Codex frontmatter or image metadata | Direct artifact-hygiene regression |
| Adopt Kimi inline media or export-style content | Direct artifact-hygiene regression |
| Adopt Sonnet-scale diagram volume or chapter sprawl | Maintenance-heavy and unnecessary for the current baseline |
| Reintroduce legacy terms into current-state sections | Conflicts with the baseline's clean appendix quarantine |

## Implementation Sequence

1. Update the opening block to preserve current authority statements while clarifying the semantic-authority vs machine-contract distinction.
2. Record the current H2/H3 heading set, Appendix `10.1-10.5` structure, and Mermaid count (`4`) as immutable edit constraints.
3. Build a preservation checklist from the Protected Source Surface Matrix and the current manual’s `10.5` source crosswalk before making text edits.
4. Insert the new `Manual Map` block above the existing TOC.
5. Replace the current Section `1.3` routing table with the role/task matrix defined in `EH-2`.
6. Add one short lead-in paragraph to each H2 section from `1` through `10`.
7. Add the fixed `See also` lines to Sections `3` through `9`.
8. Insert the historical-scope note immediately before Section `10.2`.
9. Verify that no existing section is removed, renumbered, renamed, or materially collapsed.
10. Verify that every protected source surface remains discoverable in the same section family or a strictly clearer additive placement.
11. Verify that the existing four Mermaid diagrams remain the ceiling and that no image references are introduced.

## Acceptance Criteria

- The only target file for the enhancement pass is `ddr_ref_manual_v6.3.md`.
- The manual still covers every protected source surface named in the Protected Source Surface Matrix.
- Section numbering remains `1-10`.
- Existing H2 and H3 headings remain unchanged, so the current TOC and crosswalk anchors continue to function.
- Sections `2.3`, `2.4`, `9.1-9.7`, `10.4`, and `10.5` remain present.
- Section `9` remains the dedicated schema and machine-validation surface.
- Section `6` still documents the four Express Mode groups and both unbundling rule surfaces.
- Section `5` still exposes the full operational surface, including `8` core operations, `5` DIRTY triggers, `5` manifest tracks, `3` manifest item types, `12` status transitions, and `9` guard definitions.
- Section `8` still exposes the extension architecture, `9` extension catalog entries, and `3` ARE scoring profiles.
- Sections `10.2` and `10.3` remain distinct historical appendices, and Sections `10.4` and `10.5` remain intact.
- No new normative DDR claims are introduced.
- No frontmatter, external visuals, or inline payloads appear in the updated manual.
- Diagram count remains at or below the current four Mermaid blocks.
- Historical terms remain confined to version-history and migration context.

## Second-Pass SSOT Review

The plan was reviewed against the YAML-led authority surface to confirm that the proposed changes are structural or manual-local only.

| Critical authority surface | Plan impact | Result |
| --- | --- | --- |
| Root and metadata surfaces: `project`, `system_metadata`, `errata_log` | Preserved; approved changes only add navigation and framing around Sections `1.2`, `2.1-2.4`, and `10.4` | `Pass` |
| Core structural rule surfaces: `axioms`, `node_schema_fields`, `edge_type_definitions`, `dag_invariants`, `node_id_format`, `citation_rules` | Preserved; no approved change removes or renames Sections `3.1`, `3.5-3.9`, or the related schema subsections | `Pass` |
| Topology and tier-definition surfaces: representative `nodes`, `tier_definitions`, canonical `active_tiers` variants | Preserved; Sections `3.3-3.4` and `4.1-4.9` remain in place | `Pass` |
| Consumption-mode surfaces: `consumption_modes` and full `express_mode` contract including `groups`, determinism, and deferred-fragment handling | Preserved; Section `6` scope is unchanged and remains a dedicated mode/unbundling surface | `Pass` |
| Constraint-precedence surfaces including physical constraint escalation | Preserved; Section `7.1-7.2` remains intact and additive framing does not alter precedence content | `Pass` |
| Core operations surface: `core_operations` plus removed-operation note | Preserved; Section `5.4` remains a dedicated operation lookup surface | `Pass` |
| DIRTY, resolution, and reconciliation surfaces: `dirty_flag_triggers`, `dirty_flag_notes`, `dirty_classification`, `supersede_dirty_behavior`, `resolution_workflow`, `conflict_resolution_protocol`, `semantic_consistency_rules`, `reconciliation_manifest_tracks`, `reconciliation_manifest_schema` | Preserved; Sections `5.5`, `5.6`, `7.3`, and `7.5` remain explicit protected surfaces | `Pass` |
| Extension and ARE surfaces: `extension_system`, `extension_catalog`, `are_scoring_profiles` | Preserved; Section `8` remains intact and is not being tutorialized or collapsed | `Pass` |
| Compliance and appendix surfaces: `compliance_checklist`, `glossary`, `version_history`, `tier_migration`, authoritative counts, source crosswalk | Preserved; Sections `7.4-7.5` and `10.1-10.5` remain intact, with added history-boundary clarification only | `Pass` |
| Schema root branching: `document_profile`, `system_definition` required surface, and `active_tiers` closure | Preserved; Sections `3.2`, `3.3`, `9.1`, and `9.2` remain mandatory | `Pass` |
| Schema node and citation definitions: `$defs.DdrNode`, `$defs.ParentCitation` | Preserved; Sections `9.3-9.4` remain explicit and uncollapsed | `Pass` |
| Schema express, extension, and lifecycle definitions: `ExpressModeGroup`, `ExtensionEntry`, `ScoringProfile`, `StatusTransition`, `GuardDefinition`, status and guard enums | Preserved; Sections `9.5-9.7` remain explicit, and the plan now names them as protected surfaces | `Pass` |

Markdown-spec cross-check result:

- `DDR System(v6.3).md` does not require any override to this plan.
- It supports the current section-family structure and does not justify weakening the YAML-led authority model.

## Execution Notes

- This plan intentionally improves readability without changing the manual's factual contract.
- If any planned wording change would require inventing a new DDR explanation not already grounded in the current manual and YAML pair, the change must be dropped rather than improvised.
- The enhancement pass should be treated as a presentation and navigation refinement, not a content-expansion project.

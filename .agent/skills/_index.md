# DDR System Skills Registry

> **Context:** This index defines atomic capabilities for the AI Agent functioning within the Antigravity IDE.
> **Usage:** Select skills based on "Category" logic or "Trigger" keywords in user prompts.
> **Constraint:** Maintain strict adherence to DDR (Dynamic Documentation Requirements) protocols.

## 1. Core Classification & Routing

*Primary function: Ingestion analysis and routing logic.*

### `tier_classifier`

- **Function:** Analyzes unstructured fragments.
- **Action:** Assigns tier (BRD/NFR/FSD/SAD/ICD/TDD/ISP) via decision tree/scoring.
- **Inputs:** Raw text, partial requirements.

### `ambiguity_resolver`

- **Function:** resolving classification ties.
- **Action:** Applies weighted scoring (10 factors) and abstraction hierarchy rules.
- **Trigger:** Multi-tier match detected.

---

## 2. Vertical Abstraction

*Primary function: Hierarchical requirement generation and link maintenance.*

### `parent_synthesizer`

- **Function:** Upstream generation.
- **Action:** Abstracts orphan child specs upward to create missing parent requirements.
- **Constraint:** Must preserve traceability chains.

### `child_decomposer`

- **Function:** Downstream generation.
- **Action:** Breaks high-level reqs into concrete specs, extracting constraints/vectors.
- **Constraint:** Must maintain parent citations.

### `sibling_expander`

- **Function:** Horizontal generation.
- **Action:** Identifies isolated tags; generates parallel concerns at same abstraction level.
- **Output:** Sibling tags with shared parent citations.

---

## 3. Traceability & Validation

*Primary function: Graph integrity and link verification.*

### `chain_validator`

- **Function:** Full-graph audit.
- **Action:** Validates trace from tag to BRD root.
- **Detects:** Orphans, cycles, forward references, broken chains.

### `impact_analyzer`

- **Function:** Change management.
- **Action:** Builds transitive dependency graphs upon parent modification.
- **Output:** List of downstream citations requiring review.

### `orphan_detective`

- **Function:** Gap detection.
- **Action:** Scans for missing parent citations.
- **Priority:** Queue for abstraction protocols or deletion.

---

## 4. Constraint Enforcement

*Primary function: Rule governance and immutable logic.*

### `tag_immutability_guard`

- **Function:** ID protection.
- **Action:** Blocks ID mutation, re-sequencing, or recycling.
- **Scope:** All operations.

### `citation_mandate_enforcer`

- **Function:** Link enforcement.
- **Action:** Enforces `:links:` directive presence for all non-BRD tags.

### `sibling_prohibition_enforcer`

- **Function:** Structure enforcement.
- **Action:** Blocks peer-level citations within same tier block (vertical-only trace).

### `tier_content_validator`

- **Function:** Content rules.
- **Action:** Enforces specific tier constraints (e.g., BRD=agnostic, NFR=numeric, ISP=stub-only).

---

## 5. Reconciliation & Integrity

*Primary function: State management and manifest sync.*

### `dirty_flag_manager`

- **Function:** Status tracking.
- **Action:** Manages `DIRTY` status in reconciliation manifests during modifications.

### `inventory_synchronizer`

- **Function:** Count maintenance.
- **Action:** Reconciles section text against manifest records (counts/inventory).

### `manifest_generator`

- **Function:** Metadata creation.
- **Action:** Writes blocks with `section_id`, `integrity_status`, `timestamp`, `tag_count`, `pending_items`.

---

## 6. Document Generation

*Primary function: Formatting and output syntax.*

### `rst_directive_formatter`

- **Function:** Sphinx/RST output.
- **Action:** Generates Sphinx-Needs directives with correct syntax/fields.

### `numpy_docstring_generator`

- **Function:** Python ISP output.
- **Action:** Creates stubs with Numpy-style docstrings (Parameters, Returns, Implements).

### `schema_documenter`

- **Function:** ICD output.
- **Action:** Formats data contracts as YAML/JSON schemas with inline trace comments.

---

## 7. Workflow Orchestration

*Primary function: Task sequencing and routing.*

### `tier_specialist_router`

- **Function:** Role delegation.
- **Action:** Routes tasks to sub-skills (e.g., BRD Strategist, NFR Enforcer).

### `end_to_end_feature_generator`

- **Function:** Macro workflow.
- **Action:** Orchestrates generation from BRD -> ISP across all 7 tiers.

### `reconciliation_orchestrator`

- **Function:** Cleanup workflow.
- **Action:** Sequences impact analysis -> validation -> constraints -> sync.

---

## 8. Knowledge Source Management

*Primary function: Context and vocabulary management.*

### `knowledge_source_author`

- **Function:** File creation.
- **Action:** Creates files using canonical templates (concept/protocol/constraint/pattern).

### `glossary_enforcer`

- **Function:** Terminology check.
- **Action:** Validates nouns against controlled vocabulary; flags undefined terms.

### `cross_reference_linker`

- **Function:** Meta-linking.
- **Action:** Manages `requires:` and `related:` frontmatter fields.

---

## 9. Quality Assurance

*Primary function: Static analysis and diagram verification.*

### `block_atomic_validator`

- **Function:** Hierarchy check.
- **Action:** Ensures Block tags (TIER-N) precede Atomic tags (TIER-N.M).

### `ascii_diagram_enforcer`

- **Function:** Visual requirement.
- **Action:** Verifies SAD sections contain mandatory ASCII topology diagrams.

### `metric_measurability_checker`

- **Function:** Clarity check.
- **Action:** Scans BRD/NFR for subjective terms; ensures numeric targets/units exist.

### `md060-strict-aligner`

- **Function:** Table Alignment.
- **Action:** Repairs MD060 violations by deterministically reformatting markdown tables via Python script.

---

## 10. Migration & Transformation

*Primary function: Legacy handling and ID generation.*

### `legacy_doc_classifier`

- **Function:** Retrofitting.
- **Action:** Assigns tiers and confidence scores to existing unstructured docs.

### `tag_id_minter`

- **Function:** ID creation.
- **Action:** Generates next ID via prefix conventions; ensures no recycling.

### `citation_repair_assistant`

- **Function:** Healing.
- **Action:** Suggests parent candidates via semantic similarity and hierarchy rules.

---

## 11. Reporting & Analytics

*Primary function: Visibility and status reporting.*

### `compliance_reporter`

- **Function:** Audit output.
- **Action:** Reports violations, orphans, dirty sections, and mismatches.

### `traceability_visualizer`

- **Function:** Graph output.
- **Action:** Renders tree/graph from ISP back to BRD.

### `coverage_analyzer`

- **Function:** Gap analysis.
- **Action:** Identifies missing tier coverage (e.g., FSD without SAD).

---

## 12. Planning & Strategy

*Primary function: User-guided execution planning.*

### `planning_instructions`

- **Function:** Implementation Planning.
- **Action:** Generates hallucination-resistant implementation plans via research and validation.
- **Trigger:** `@Implementation_Plan`

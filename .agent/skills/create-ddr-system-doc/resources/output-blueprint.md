<document_purpose>
Define the canonical Markdown section layout for DDR System documentation generated from DDR schema/specification YAML inputs.
</document_purpose>

<required_sections>

- `# DDR System Specification v<ddr_version>`
- `## 1. Design Philosophy`
- `## 2. Foundational Axioms`
- `## 3. DAG Internal Model`
- `## 4. Consumption Modes`
- `## 5. Tier Specifications`
- `## 6. Constraint Precedence`
- `## 7. Atomic Operations Protocol`
- `## 8. Extension System`
- `## 9. Extension Catalog`
- `## 10. Architecture Diagram`
- `## 11. Compliance Checklist`
- `## Glossary`
- `## Appendix A: Version History`
- `## Appendix B: Legacy Tier Migration`
</required_sections>

<section_mapping>

- `system_metadata.design_philosophy`, `changes_from_prior`, `errata_log` -> Section 1
- `axioms` -> Section 2
- `node_schema_fields`, `edge_type_definitions`, `nodes`, `dag_invariants`, `node_id_format`, `citation_rules`, `lifecycle` -> Section 3
- `consumption_modes`, `express_mode` -> Section 4
- `tier_definitions` -> Section 5
- `constraint_precedence` -> Section 6
- `operations` -> Section 7
- `extension_system` -> Section 8
- `extension_catalog`, `are_scoring_profiles` -> Section 9
- `nodes`, `extension_catalog` -> Section 10
- `compliance_checklist` -> Section 11
- `glossary` -> Glossary
- `version_history` -> Appendix A
- `tier_migration` -> Appendix B
</section_mapping>

<output_contract>

- Include a Mermaid diagram in Section 10.
- Include one subsection per tier in Section 5 and one subsection per extension in Section 9.
- Validate the final document against the source spec before returning success.
</output_contract>

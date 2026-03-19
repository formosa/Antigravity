<document_purpose>
This resource file contains domain knowledge and quality standards referenced by the Agent Create Issue Report skill during resolution strategy formulation and comparative analysis.
</document_purpose>

<domain_rules>

## Resolution Report Quality Standards

1. **Evidence-First Auditing:** Every claim in the Validation Audit section must cite a specific file path and quoted content from the project. Ungrounded claims are prohibited.
2. **Distinct Strategy Requirement:** Option A and Option B must represent fundamentally different design decisions — not parametric variants of the same approach. A useful heuristic: if one option could be derived from the other by changing a single configuration value, they are too similar.
3. **Citation Integrity:** External citations must reference real, published standards or documentation. Preferred sources:
   - ISO/IEC standards (e.g., ISO 9001, ISO/IEC 25010, IEC 62443)
   - IEEE standards and vocabularies (e.g., IEEE 830, IEEE 29148)
   - IETF RFCs
   - Official vendor documentation (e.g., Google, Microsoft, OWASP)
   - SOC 2 Trust Services Criteria
   - Peer-reviewed publications from ACM, IEEE Xplore, or arXiv
4. **Endorsement Objectivity:** The recommended option must be justified against measurable criteria (e.g., breaking change count, migration cost, backwards compatibility, compliance coverage). Subjective preferences ("feels cleaner") are insufficient.

## Tradeoff Dimensions for Comparative Analysis

When evaluating resolution strategies, consider these standard dimensions as candidates for comparison. Select 2–4 that are most relevant to the specific issue:

- **Breaking Change Scope:** Does the option require a major version bump, schema migration, or topology change?
- **Backwards Compatibility:** Can existing project files be parsed without modification after the change?
- **Implementation Complexity:** How many files, schemas, or rules must be modified?
- **Compliance Readiness:** Does the option satisfy or improve alignment with external regulatory standards?
- **Determinism Impact:** Does the option improve or degrade the system's ability to produce mechanically verifiable outputs?
- **Axiom Alignment:** Does the option honor or conflict with the subject system's stated design axioms?
- **Topological Entropy:** Does the option increase, decrease, or maintain the graph/schema complexity?
- **Extension Isolation:** Does the option keep changes within optional extensions, or does it modify the core?

</domain_rules>

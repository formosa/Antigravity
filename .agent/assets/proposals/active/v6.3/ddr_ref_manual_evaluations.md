# DDR v6.3 Reference Manual Draft Evaluations

## Purpose

This artifact is an adversarial review of the five previously generated DDR System v6.3 reference manual drafts. It exists to decide what can be reused for organization and reference design, and what must be rejected to keep the replacement manual faithful to the authoritative v6.3 source set:

- `ddr_system_v6.3.yaml`
- `ddr_node_schema_v6.3.yaml`

The drafts are not treated as factual authorities. They are evaluated only against the YAML specification and schema.

## Rubric

Scores use a 1-5 scale, where higher is better. For `Drift risk`, `5` means low risk of reintroducing superseded or unsupported concepts.

Severity labels:

- `Critical`: source contradiction, fabricated behavior, or artifact contamination severe enough to disqualify direct reuse
- `Major`: missing authoritative surface, materially misleading emphasis, or weak schema/lifecycle precision
- `Minor`: organization, style, or usability inefficiency that does not by itself invalidate the draft

Evaluation dimensions:

- `Factual fidelity`: how consistently the draft aligns with the v6.3 YAML authority
- `Coverage completeness`: how much of the authoritative v6.3 surface is actually documented
- `Schema/lifecycle precision`: how well the draft captures `document_profile`, schema conditionals, lifecycle transitions, guards, and machine constraints
- `Reference usability`: how effective the draft is as a lookup manual rather than a tutorial
- `Drift risk`: how safely the draft avoids overstating removed, historical, or merely illustrative concepts

## Authority Baseline

The replacement manual must cover, at minimum, the authoritative v6.3 surface below:

| Surface | Count / shape |
| --- | --- |
| Top-level specification sections | 26 |
| Top-level schema properties | 26 |
| `document_profile` values | 3 |
| Canonical `active_tiers` variants | 4 |
| Axioms | 7 |
| Edge types | 4 |
| Node schema fields | 13 |
| Citation rules | 7 |
| DAG invariants | 8 |
| Tier definitions | 9 |
| Canonical operations | 8 |
| Consumption modes | 2 |
| Express Mode groups | 4 |
| Extension catalog entries | 9 |
| ARE scoring profiles | 3 |
| Compliance checklist categories | 3 |
| Glossary entries | 14 |
| Version history entries | 10 |
| Representative topology nodes | 9 |
| Lifecycle status transitions | 12 |
| Lifecycle guard definitions | 9 |

## Score Matrix

| Draft | Factual fidelity | Coverage completeness | Schema/lifecycle precision | Reference usability | Drift risk | Decision |
| --- | ---: | ---: | ---: | ---: | ---: | --- |
| ChatGPT | 3 | 3 | 2 | 4 | 3 | Adapt |
| Codex | 4 | 4 | 4 | 4 | 3 | Adapt |
| Gemini | 2 | 1 | 1 | 2 | 2 | Reject |
| Kimi | 2 | 2 | 1 | 1 | 1 | Reject |
| Sonnet | 4 | 5 | 3 | 4 | 2 | Adapt |

## Draft-by-Draft Review

### ChatGPT Draft

**Assessment**

The ChatGPT draft is a solid tutorial-shaped manual with a practical section order. It explains the system well enough for a new reader, but it does not meet the threshold for a source-complete v6.3 reference artifact.

**Findings**

- `Major`: The draft does not surface the schema's profile branching as a first-class v6.3 concept. `document_profile`, `project_instance_express`, and the conditional express-profile requirements are absent from the manual's reference surface.
- `Major`: Lifecycle discussion is descriptive, but the draft does not treat `lifecycle.status_transitions` as the sole authority and does not provide a complete lookup surface for the nine guard definitions.
- `Major`: The draft is weak on authoritative appendices and machine-contract coverage. It does not adequately document errata state, version history, tier migration, or the schema conditionals that distinguish `system_definition` from project-instance artifacts.
- `Minor`: The document uses many explanatory and scenario sections relative to reference tables, which slows lookup when the reader already knows DDR vocabulary and needs exact v6.3 mechanics.

**Reusable patterns**

- Clear practical section ordering around topology, operations, compliance, and failure modes
- Good separation between edge types, citation rules, lifecycle, and extension material
- Strong instinct for "why this matters" framing after each technical area

**Patterns to reject**

- Tutorial weight that exceeds reference weight
- Scenario volume not directly tied to source-native examples
- Missing schema/lifecycle lookup tables

**Decision**

`Adapt`

Keep the broad table-of-contents strategy and some of the practical lookup sequencing. Replace the prose body with tighter source-derived tables and appendices.

### Codex Draft

**Assessment**

The Codex draft is the strongest starting point for authority framing and schema-aware reference design. It has the best instincts for separating semantic authority from machine-contract authority, but it still violates the replacement artifact requirements and needs heavy cleanup.

**Findings**

- `Major`: The file contains frontmatter and `image_prompt_sources`, which are incompatible with the requested plain-Markdown, source-only reference manual.
- `Major`: The draft depends on external and generated visual material rather than keeping the artifact self-contained. The replacement manual must not carry external image metadata or non-authoritative visual baggage.
- `Minor`: The draft is still too tutorialized in places, with many "authoring guidance" and "illustrative scenario" blocks that expand beyond strict reference needs.
- `Minor`: Historical and migration terminology such as `ORL`, `HIL`, `TDL`, `CRR`, and `fork-join` appears often enough that the replacement manual must quarantine those terms to the version-history and migration appendices to avoid interpretive drift.

**Reusable patterns**

- Explicit "semantic authority vs machine-contract authority" framing
- Strong schema/lifecycle coverage
- Good rule-table orientation and appendix mindset
- Practical grouping of extensions, ARE, and schema validation concerns

**Patterns to reject**

- Frontmatter
- External image references and image prompt metadata
- Excess scenario volume and diagram count
- Broad distribution of legacy terminology outside clearly historical sections

**Decision**

`Adapt`

Reuse the authority model, schema emphasis, and lookup-friendly grouping. Strip non-source metadata, reduce explanatory bulk, and constrain historical terminology to appendices.

### Gemini Draft

**Assessment**

The Gemini draft is too incomplete to serve as a viable source for the replacement manual. It captures high-level DDR ideas but misses most of the v6.3 machine and operational surface.

**Findings**

- `Major`: Coverage stops after axioms, DAG architecture, edge types, node format, topology, and invariants. Most authoritative v6.3 sections are missing: lifecycle, operations, consumption modes, Express Mode, constraint precedence, extensions, ARE profiles, compliance, glossary, version history, tier migration, and schema contract detail.
- `Major`: The draft does not document key v6.3 precision points such as `document_profile`, `constraint_origin`, `prior_status`, `extension_annotations`, `status_transitions`, guard definitions, or the E5 `scoring_profile` requirement.
- `Minor`: The artifact behaves more like a short conceptual explainer than a reference manual.

**Reusable patterns**

- Concise axiom summaries
- Minimalist framing for topology and edge semantics

**Patterns to reject**

- Incomplete chapter scope
- Absence of appendices and machine-contract documentation
- Reliance on examples in place of comprehensive rule coverage

**Decision**

`Reject`

The document is too incomplete to guide the replacement manual beyond a few stylistic cues for concise axiom summaries.

### Kimi Draft

**Assessment**

The Kimi draft has broad apparent scope, but its artifact hygiene and schema precision are poor enough to make it unsuitable as a direct template for the replacement manual.

**Findings**

- `Critical`: The document contains a massive inline base64 image payload, which contaminates the artifact and makes it unsuitable as a clean reference manual source.
- `Major`: Despite broad topical reach, the draft does not provide reliable v6.3 machine-contract coverage for `document_profile`, express-profile constraints, lifecycle guards, schema conditionals, or the closed status-transition model.
- `Major`: Reference usability is weak because the document is extremely large, noisy, and not shaped around clean lookup surfaces.
- `Minor`: Legacy terminology appears frequently enough to create drift pressure unless tightly quarantined to historical appendices.

**Reusable patterns**

- Broad section coverage across tiers, operations, extensions, and compliance
- Useful instinct to keep tier-by-tier and extension-catalog material visible

**Patterns to reject**

- Embedded non-reference artifacts such as base64 image payloads
- Oversized prose without a clean lookup model
- Weak schema/lifecycle precision

**Decision**

`Reject`

The draft is too noisy and too weak on v6.3 machine precision to serve as a safe foundation.

### Sonnet Draft

**Assessment**

The Sonnet draft has the strongest information architecture. Its part/chapter organization is the best template for a comprehensive reference manual, but its prose mass and drift exposure are too high for direct reuse.

**Findings**

- `Major`: The draft contains a large amount of hypothetical scenario material and explanatory elaboration. That makes the document readable, but it dilutes the distinction between authoritative reference and illustrative teaching.
- `Major`: Historical concepts such as `ORL`, `HIL`, `TDL`, `RELOCATE`, and prior fork-join structures appear frequently. Those concepts are legitimate only in version-history, migration, and design-decision context; the replacement manual must keep them there.
- `Major`: Schema and lifecycle precision is not consistently surfaced as dedicated lookup tables. The draft is chapter-rich but weaker than it should be on schema branch visibility, guard lookup, and conditional machine rules.
- `Minor`: Twenty-six Mermaid diagrams oversaturate the manual and create unnecessary maintenance surface.

**Reusable patterns**

- Best overall part/chapter navigation model
- Good separation between context, graph architecture, tier reference, operations, extension system, and appendices
- Strong instinct to keep the glossary, version history, and migration material in appendices

**Patterns to reject**

- High scenario density
- Very high diagram count
- Broad distribution of historical terminology outside explicitly historical sections

**Decision**

`Adapt`

Use Sonnet's macro-structure as the organizational backbone, but replace its prose body with tighter source-derived reference content and a much smaller diagram surface.

## Reusable Patterns to Keep

- From Codex: source-authority framing, schema-aware organization, lifecycle and machine-contract emphasis
- From Sonnet: part/chapter navigation, appendix discipline, clear separation of reference domains
- From ChatGPT: practical lookup sections around citation rules, operations, compliance, and failure modes
- Across the stronger drafts: explicit tables for rules, transitions, and extension catalog entries

## Patterns to Reject

- Any frontmatter, image prompt metadata, embedded images, or base64 payloads
- Any claim that is not directly supportable by the two authoritative YAML files
- Scenario-heavy tutorial content as the dominant mode of explanation
- Historical terminology distributed across current-state sections instead of confined to appendices
- Excess diagram count that obscures the authoritative reference surface

## Resulting Design Decisions for the Replacement Manual

- Use plain Markdown only. No frontmatter, external images, inline image payloads, or image prompt metadata.
- Treat `ddr_system_v6.3.yaml` and `ddr_node_schema_v6.3.yaml` as the only factual sources.
- Use Sonnet's large-scale part/chapter organization, but use Codex's authority/schema framing inside the chapters.
- Prefer tables for enumerations, rule sets, transitions, schema restrictions, and catalog entries.
- Use only source-native examples: representative nodes, canonical `active_tiers` variants, lifecycle transitions, Express Mode groups, extension entries, manifest item types, and scoring profiles.
- Limit Mermaid to exactly four diagrams: canonical topology, lifecycle state machine, Express Mode grouping/unbundle flow, and extension overlay with ARE candidate pool.
- Quarantine legacy terms such as `ORL`, `HIL`, `TDL`, `CRR`, `RELOCATE`, and prior fork-join structures to version-history, migration, or explicit design-decision context only.
- Add a final `Source Crosswalk` appendix so every authoritative source section and key schema branch maps to a specific section of the new manual.

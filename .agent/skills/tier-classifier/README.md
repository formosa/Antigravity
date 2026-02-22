# Tier Classifier Skill

**Version**: 1.0.0
**Category**: DDR System Migration
**Model**: Claude Sonnet 4

## Overview

The Tier Classifier skill analyzes unstructured information fragments and assigns them to the correct tier in the seven-tier DDR (Development Documentation Roadmap) hierarchy. It uses a sequential decision tree for clear cases and a multi-factor scoring matrix for ambiguous classifications.

## Capabilities

- ✅ Sequential decision tree classification (Q1-Q7)
- ✅ Multi-factor scoring for ambiguous fragments
- ✅ Tier-specific constraint validation
- ✅ Parent citation synthesis
- ✅ RST directive generation
- ✅ Confidence scoring with semantic validation
- ✅ Cross-tier decomposition detection
- ✅ Violation detection and correction suggestions

## Tier Hierarchy

| Tier    | Layer      | Question       | Output                       |
| :------ | :--------- | :------------- | :--------------------------- |
| **BRD** | Context    | Why build?     | Business value, stakeholders |
| **NFR** | Boundaries | What limits?   | Numeric constraints, SLAs    |
| **FSD** | Behavior   | What does it?  | User-facing capabilities     |
| **SAD** | Structure  | How organized? | Architectural patterns       |
| **ICD** | Contracts  | What shapes?   | Data schemas                 |
| **TDD** | Blueprints | What classes?  | Component structure          |
| **ISP** | Prompts    | What stubs?    | Code skeletons               |

## Usage

### Basic Classification

```json
{
  "fragment": "Enable hands-free voice interaction with response times under 1 second",
  "output_format": "rst"
}
```

### With Context

```json
{
  "fragment": "Log rotation every 50MB with 30-day retention",
  "context": {
    "existing_tags": ["BRD-3.5", "NFR-7"],
    "parent_candidates": ["BRD-3.5"]
  },
  "output_format": "report"
}
```

## Output Schema

```json
{
  "tier": "NFR",
  "confidence": 0.85,
  "reasoning": {
    "decision_path": [...],
    "scores": {...},
    "factors_detected": [...]
  },
  "parent_citations": ["BRD-3.5"],
  "formatted_output": ".. nfr:: ...",
  "validation_warnings": []
}
```

## Classification Algorithm

### Phase 1: Decision Tree

1. Q1: Business justification? → BRD
2. Q2: Constraints/limits? → NFR
3. Q3: System behavior? → FSD
4. Q4: Architecture/structure? → SAD
5. Q5: Data schemas? → ICD
6. Q6: Class structure? → TDD
7. Q7: Code stubs? → ISP

### Phase 2: Scoring Matrix (if ambiguous)

- 10 classification factors with tier-specific weights
- Sum scores per tier, highest wins
- Tie-breaker: favor higher abstraction

### Phase 3: Validation

- Tier-specific constraint checks
- Citation requirement validation
- Format/syntax verification

## Examples

See `examples/` directory:

- `brd_example.md` - Business requirements
- `nfr_example.md` - Performance constraints
- `ambiguous_example.md` - Scoring matrix demonstration
- `edge_cases.md` - Boundary conditions

## Knowledge Sources

- `tier_definitions.json` - Tier characteristics, rules, examples
- `classification_factors.json` - 10-factor scoring weights
- `validation_rules.json` - Constraint enforcement patterns

## Performance

- **Avg Tokens**: ~2,500 per classification
- **Cache Enabled**: Yes (knowledge sources, decision tree)
- **Confidence Threshold**: 0.7 (below triggers human review)

## Integration Points

### Upstream Skills

- `glossary_enforcer` - Validates controlled vocabulary
- `legacy_doc_classifier` - Bulk classification of existing docs

### Downstream Skills

- `parent_synthesizer` - Creates missing parent tags
- `rst_directive_formatter` - Enhanced RST generation
- `chain_validator` - Traceability verification

## Limitations

- Requires well-formed input (complete sentences/phrases)
- Cannot classify fragments outside DDR scope
- Confidence degrades with very short inputs (< 10 words)
- Cross-tier synthesis requires manual decomposition approval

## Testing

Run test suites:

```bash
python -m pytest tests/test_decision_tree.json
python -m pytest tests/test_scoring.json
python -m pytest tests/test_validation.json
```

## Version History

- **1.0.0** (2026-01-22): Initial release with full decision tree and scoring matrix
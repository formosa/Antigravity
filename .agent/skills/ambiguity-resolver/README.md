# DDR Ambiguity Resolver - Claude Skill

> **Version**: 1.0.0
> **Compatibility**: Google Antigravity IDE v1.16.5+
> **Model**: Claude Sonnet 4.5

## Overview

The **Ambiguity Resolver** is a Claude Skill that resolves ambiguous DDR tier classifications using multi-factor scoring when information fragments match multiple tiers. It implements the complete scoring protocol from `classification-scoring.md` with tie-breaker rules and contextual validation.

## Features

✅ **10-Factor Scoring Matrix** - Analyzes fragments across all classification dimensions
✅ **Tie-Breaker Logic** - Applies abstraction hierarchy when scores are equal
✅ **Contextual Validation** - Verifies semantic fit, parent availability, downstream feasibility
✅ **Confidence Scoring** - Calculates 0-1 confidence based on margin and validation
✅ **Batch Processing** - Classify multiple fragments efficiently
✅ **Structured Output** - JSON/RST directive formats for integration

## Installation

### For Antigravity IDE

1. **Copy skill to workspace**:

   ```bash
   cp -r ambiguity_resolver/ ~/.antigravity/skills/
   ```

2. **Verify installation**:

   ```bash
   antigravity skill list | grep ambiguity_resolver
   ```

3. **Enable in project**:

   ```yaml
   # .antigravity/config.yaml
   skills:
     - ambiguity_resolver
   ```

### For Standalone Use

```bash
pip install -r requirements.txt
python examples/basic_usage.py
```

## Quick Start

### Basic Usage

```python
from ambiguity_resolver import resolve_ambiguity

fragment = "System must aggregate all log messages into a single file with automatic rotation every 50MB"

result = resolve_ambiguity(
    fragment=fragment,
    candidate_tiers=["NFR", "ICD"],
    output_format="detailed"
)

print(f"Assigned Tier: {result['assigned_tier']}")
print(f"Confidence: {result['confidence']}")
print(result['reasoning'])
```

### Antigravity IDE Integration

Within the IDE, activate via:

- **Command**: `Ctrl+Shift+P` → "Resolve Tier Ambiguity"
- **Inline**: Select fragment, right-click → "DDR: Classify"
- **Pattern**: Type "resolve tier ambiguity" in chat

## Classification Protocol

### The 10 Factors

| Factor | Description | High Score Tiers |
|:-------|:------------|:-----------------|
| Numeric Metrics | < 1s, 50MB, 99.9% | NFR (3), ICD (2) |
| Hardware Reference | CPU, GPU, VRAM | NFR (3), SAD (1) |
| User Behavior | Interaction, workflow | FSD (3), BRD (2) |
| Pattern Names | Hub-and-Spoke, DEALER | SAD (3), TDD (1) |
| Schema Definition | JSON/YAML structures | ICD (3), ISP (1) |
| Class Names | PascalCase identifiers | TDD (3), ISP (2) |
| Executable Code | def, class, import | ISP (3) |
| Modal Keywords | MUST, SHALL, SHOULD | NFR (3), FSD (2) |
| Rationale | Because, enables, justifies | BRD (3), SAD (3) |
| Technology-Agnostic | No specific libs/tools | BRD (3), FSD (2) |

### Scoring Steps

1. **Factor Detection** - Analyze fragment for all 10 factors
2. **Score Calculation** - Sum weighted scores per tier
3. **Tie-Breaking** - Select highest abstraction if tied
4. **Validation** - Verify semantic fit and feasibility
5. **Confidence** - Calculate based on margin + validation

### Tie-Breaker Hierarchy

```
BRD > NFR > FSD > SAD > ICD > TDD > ISP
 ↑                                   ↓
Higher Abstraction      Lower Abstraction
```

## Configuration

### Scoring Weights

Customize in `config/scoring_weights.yaml`:

```yaml
numeric_metrics:
  BRD: 1
  NFR: 3
  FSD: 1
  # ... etc
```

### Validation Rules

Adjust in `config/validation_rules.yaml`:

```yaml
BRD:
  must_be_agnostic: true
  must_have_rationale: true
NFR:
  must_have_numeric: true
  # ... etc
```

## Output Formats

### Detailed (Default)

```json
{
  "assigned_tier": "NFR",
  "confidence": 0.823,
  "scores": {
    "BRD": 6,
    "NFR": 7,
    "FSD": 4,
    "ICD": 5
  },
  "factors_detected": {
    "numeric_metrics": "yes",
    "modal_keywords": "yes",
    "technology_agnostic": "yes"
  },
  "tie_breaker_applied": false,
  "validation_passed": true,
  "validation_notes": [
    "Semantic fit for NFR validated",
    "Parent BRD tags available for citation: 12 tags"
  ],
  "reasoning": "..."
}
```

### Summary

```json
{
  "assigned_tier": "NFR",
  "confidence": 0.823,
  "validation_passed": true
}
```

### RST Directive

```rst
.. nfr:: System must aggregate all log messages into a single file with automatic rotation every 50MB
   :id: NFR-<next>
   :links: BRD-<parent>

   # Classification confidence: 0.823
   # Factors: numeric_metrics, modal_keywords, technology_agnostic
```

## Examples

### Example 1: Clear Classification

**Fragment**: "System must respond within 1 second average latency"

**Result**:

- **Tier**: NFR
- **Confidence**: 0.91
- **Key Factors**: numeric_metrics (yes), modal_keywords (yes)
- **Reasoning**: Clear numeric constraint with modality

### Example 2: Ambiguous (Tie-Breaker)

**Fragment**: "Centralized logging enables debugging across components"

**Result**:

- **Tier**: BRD (tie-breaker applied)
- **Confidence**: 0.68
- **Scores**: BRD=6, NFR=5, FSD=5
- **Reasoning**: Tie between BRD/NFR/FSD; higher abstraction wins

### Example 3: Low Confidence

**Fragment**: "Process handles messages"

**Result**:

- **Tier**: FSD
- **Confidence**: 0.42
- **Flag**: Manual review recommended
- **Reasoning**: Insufficient specificity; limited factors detected

## Testing

```bash
# Run all tests
pytest tests/

# Run specific test suite
pytest tests/test_scoring.py -v

# Run with coverage
pytest --cov=src tests/
```

## Troubleshooting

### Issue: Low Confidence Scores

**Cause**: Fragment lacks clear tier indicators
**Solution**: Add specific factors (metrics, patterns, rationale)

### Issue: Unexpected Tier Assignment

**Cause**: Dominant factor outweighs intent
**Solution**: Review scoring weights in config; adjust if needed

### Issue: Validation Failures

**Cause**: Missing parent tags or constraint violations
**Solution**: Ensure parent tiers exist; check tier-specific constraints

## API Reference

See [`docs/api_reference.md`](docs/api_reference.md) for complete API documentation.

## Contributing

Contributions welcome! See contribution guidelines in the DDR system repository.

## License

MIT License - See LICENSE file for details.

## References

- **DDR Documentation**: `classification-scoring.md`, `tier-hierarchy.md`
- **Antigravity IDE Docs**: <https://docs.antigravity.dev/skills>
- **Issue Tracker**: <https://github.com/ddr-system/skills/issues>

---

**Maintained by**: DDR System Team
**Last Updated**: 2026-01-16
**Skill Version**: 1.0.0

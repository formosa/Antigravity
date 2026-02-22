# Changelog

All notable changes to the DDR Ambiguity Resolver skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2026-01-16

### Added

#### Core Features

- **10-Factor Scoring Matrix** - Complete implementation of classification-scoring.md protocol
  - Numeric metrics detection (< 1s, 50MB, 99.9%)
  - Hardware reference detection (CPU, GPU, VRAM)
  - User behavior identification
  - Architectural pattern recognition
  - Schema definition detection
  - Class name identification (PascalCase)
  - Executable code detection
  - RFC 2119 modal keywords (MUST, SHALL, SHOULD, MAY)
  - Rationale/justification extraction
  - Technology-agnostic language validation

- **Tie-Breaker Logic** - Abstraction hierarchy rules (BRD > NFR > FSD > SAD > ICD > TDD > ISP)
- **Contextual Validation** - Three-phase validation:
  - Semantic fit validation
  - Parent availability checking
  - Downstream feasibility assessment

- **Confidence Scoring** - 0-1 confidence calculation based on:
  - Score margin between winner and runner-up
  - Absolute score magnitude
  - Validation results
  - Tie-breaker usage

#### Integration

- **Antigravity IDE v1.16.5+ Integration**
  - Command palette integration
  - Context menu integration
  - Keyboard shortcuts (Ctrl+Shift+R / Cmd+Shift+R)
  - Natural language triggers
  - Inline annotation support
  - Side panel visualization

- **Output Formats**
  - Detailed JSON output
  - Summary JSON output
  - RST directive generation
  - Formatted text reports

- **Context Injection**
  - Automatic workspace tag scanning (BRD-*, NFR-*, etc.)
  - Citation extraction
  - Project domain awareness

#### Developer Features

- **Batch Processing** - Efficient multi-fragment classification
- **Configurable Weights** - YAML-based scoring matrix customization
- **Comprehensive Logging** - Debug, info, warning, error levels
- **Structured Output Schema** - JSON Schema validation
- **Type Hints** - Full Python type annotation

#### Testing & Documentation

- **Unit Tests** - Comprehensive test suite for all 10 factors
- **Integration Tests** - End-to-end workflow validation
- **Usage Examples** - 6 detailed examples covering common scenarios
- **API Reference** - Complete documentation of all public interfaces
- **Troubleshooting Guide** - Common issues and solutions

### Implementation Details

#### Architecture

- **Modular Design** - Separate concerns: scoring, validation, hierarchy
- **Enum-Based Tiers** - Type-safe tier representation
- **Dataclass Results** - Structured classification results
- **Factory Pattern** - Configurable resolver initialization

#### Performance

- **Efficient Regex** - Optimized pattern matching for factor detection
- **Lazy Loading** - Config loaded on first use
- **Caching Support** - Fragment hash-based result caching
- **Batch Optimization** - Single-pass analysis for multiple fragments

#### Compliance

- **DDR Meta-Standard Alignment** - Implements classification-scoring.md exactly
- **Numpy Docstring Convention** - All functions fully documented
- **Sphinx-Needs Compatible** - RST output format matches DDR standards
- **RFC 2119 Compliance** - Modal keyword detection follows RFC 2119

### Dependencies

#### Runtime

- Python >= 3.10
- PyYAML >= 6.0
- Claude Sonnet 4.5 (via Antigravity IDE)

#### Development

- pytest >= 7.4.0
- pytest-cov >= 4.1.0
- black >= 23.0.0
- mypy >= 1.5.0

### Configuration Files

- `config/scoring_weights.yaml` - 10-factor tier weights
- `config/tier_hierarchy.yaml` - Valid parent-child relationships
- `config/validation_rules.yaml` - Tier-specific validation criteria
- `.antigravity/metadata.json` - IDE integration settings

### Known Limitations

1. **Maximum Fragment Length**: 2000 characters (configurable)
2. **No Memory Across Invocations**: Each classification is stateless
3. **English Language Only**: Factor detection optimized for English text
4. **Regex-Based Detection**: May have false positives/negatives on edge cases

### Compatibility

- **Antigravity IDE**: v1.16.5 or higher
- **Python**: 3.10, 3.11, 3.12
- **Claude Model**: Sonnet 4.5 (recommended)
- **Operating Systems**: macOS, Linux, Windows

### Migration Notes

This is the initial release. No migration required.

### Contributors

- DDR System Team - Initial implementation

---

## [Unreleased]

### Planned for v1.1.0

- [ ] Multi-language support (Spanish, French, German)
- [ ] Machine learning-based factor detection
- [ ] Visual factor visualization in side panel
- [ ] Undo/redo classification history
- [ ] Export results to CSV/JSON files
- [ ] Integration with other DDR skills (tier_classifier, chain_validator)

### Under Consideration

- [ ] Custom factor definitions
- [ ] User-defined scoring weights
- [ ] Interactive confidence threshold adjustment
- [ ] Real-time classification as you type
- [ ] AI-suggested parent tag citations

---

## Version History

| Version | Release Date | Major Changes |
|:--------|:-------------|:--------------|
| 1.0.0   | 2026-01-16   | Initial release |

---

**Note**: For detailed changes and bug fixes, see the [commit history](https://github.com/ddr-system/skills/commits/main/ambiguity_resolver).

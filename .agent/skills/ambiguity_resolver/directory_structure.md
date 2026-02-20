# Directory Structure: ambiguity_resolver/

```plaintext
    .agent/skills/ambiguity_resolver/
    ├── skill.yaml                           # Skill manifest for Antigravity IDE
    ├── README.md                            # Skill documentation
    ├── CHANGELOG.md                         # Version history
    ├── .antigravity/
    │   ├── metadata.json                    # IDE integration metadata
    │   └── context_windows.yaml             # Context injection configuration
    ├── src/
    │   ├── __init__.py
    │   ├── resolver.py                      # Core ambiguity resolution logic
    │   ├── scoring_matrix.py                # 10-factor scoring implementation
    │   ├── validators.py                    # Contextual validation rules
    │   ├── tier_rules.py                    # Tier-specific characteristics
    │   └── utils.py                         # Helper functions
    ├── config/
    │   ├── scoring_weights.yaml             # Factor weights per tier
    │   ├── tier_hierarchy.yaml              # Tier precedence rules
    │   └── validation_rules.yaml            # Contextual validation criteria
    ├── prompts/
    │   ├── system.txt                       # System prompt for Claude
    │   ├── analysis_template.txt            # Fragment analysis template
    │   └── output_schema.json               # Structured output specification
    ├── knowledge/
    │   ├── tier_concepts.md                 # Tier definitions reference
    │   ├── factor_guide.md                  # Factor identification guide
    │   └── examples/                        # Worked classification examples
    │       ├── example_001_logging.md
    │       ├── example_002_latency.md
    │       └── example_003_topology.md
    ├── tests/
    │   ├── __init__.py
    │   ├── test_scoring.py                  # Scoring logic tests
    │   ├── test_validation.py               # Validation tests
    │   ├── test_integration.py              # End-to-end tests
    │   └── fixtures/
    │       ├── fragments.yaml               # Test input fragments
    │       └── expected_results.yaml        # Expected classifications
    ├── docs/
    │   ├── integration_guide.md             # Antigravity IDE integration
    │   ├── api_reference.md                 # Skill API documentation
    │   └── troubleshooting.md               # Common issues and solutions
    └── examples/
        ├── basic_usage.py                   # Simple usage example
        ├── batch_classification.py          # Batch processing example
        └── interactive_demo.py              # Interactive demonstration

```

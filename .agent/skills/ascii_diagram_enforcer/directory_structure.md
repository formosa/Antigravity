# Directory Structure: ascii_diagram_enforcer

```plaintext

.agent/skills/ascii_diagram_enforcer/
├── skill.yaml                          # Skill manifest for Antigravity IDE
├── README.md                           # Skill documentation
├── src/
│   ├── __init__.py                     # Package initialization
│   ├── enforcer.py                     # Core enforcement logic
│   ├── diagram_detector.py             # ASCII diagram pattern matching
│   ├── sad_parser.py                   # SAD-tier RST directive parser
│   └── validators.py                   # Validation rule implementations
├── config/
│   ├── diagram_patterns.yaml           # ASCII diagram validation rules
│   └── error_messages.yaml             # Standardized error templates
├── tests/
│   ├── __init__.py
│   ├── test_enforcer.py                # Unit tests for enforcer
│   ├── test_diagram_detector.py        # Diagram detection tests
│   ├── fixtures/
│   │   ├── valid_sad_section.rst       # Valid SAD example
│   │   ├── invalid_sad_missing_diagram.rst
│   │   └── invalid_sad_malformed_diagram.rst
│   └── test_data/
│       └── sample_diagrams.txt         # Collection of valid ASCII patterns
├── hooks/
│   ├── pre_save.py                     # Pre-save validation hook
│   ├── on_demand.py                    # Manual invocation hook
│   └── reconciliation.py               # Integration with reconciliation system
├── docs/
│   ├── architecture.md                 # Skill architecture documentation
│   ├── usage.md                        # User guide
│   └── api.md                          # API reference
└── integration/
    ├── antigravity_plugin.py           # Antigravity IDE plugin interface
    └── ddr_bridge.py                   # Bridge to DDR reconciliation system

```

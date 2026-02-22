# Directory Structure: block_atomic_validator

```plaintext
.agent/skills/block-atomic-validator/
├── README.md
├── skill_manifest.yaml
├── pyproject.toml
├── src/
│   └── block_atomic_validator/
│       ├── __init__.py
│       ├── core/
│       │   ├── __init__.py
│       │   ├── validator.py
│       │   ├── parser.py
│       │   └── models.py
│       ├── rules/
│       │   ├── __init__.py
│       │   ├── ordering_rule.py
│       │   ├── citation_rule.py
│       │   └── consistency_rule.py
│       ├── reporters/
│       │   ├── __init__.py
│       │   ├── console_reporter.py
│       │   └── ide_reporter.py
│       └── utils/
│           ├── __init__.py
│           ├── rst_utils.py
│           └── tag_utils.py
├── tests/
│   ├── __init__.py
│   ├── fixtures/
│   │   ├── valid_brd.rst
│   │   ├── valid_fsd.rst
│   │   ├── invalid_ordering.rst
│   │   └── invalid_citation.rst
│   ├── test_validator.py
│   ├── test_parser.py
│   └── test_rules.py
├── docs/
│   ├── integration_guide.md
│   ├── rule_specifications.md
│   └── examples.md
└── antigravity_hooks/
    ├── __init__.py
    ├── skill_entrypoint.py
    └── ide_integration.py

```

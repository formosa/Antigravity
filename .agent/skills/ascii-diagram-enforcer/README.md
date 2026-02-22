# ASCII Diagram Enforcer Skill

> **Version**: 1.0.0
> **Antigravity IDE Compatibility**: 1.16.5+
> **DDR Tier**: SAD (System Architecture Document)

## Overview

The ASCII Diagram Enforcer is a validation skill for the DDR (Development Documentation Roadmap) System that ensures all SAD-tier (System Architecture Document) sections include mandatory ASCII topology diagrams. This skill integrates with Antigravity IDE to provide real-time validation, inline annotations, and automated quality checks.

### Purpose

Per DDR System specifications, **every SAD block-level tag MUST include an ASCII diagram** illustrating architectural patterns, process topology, or system structure. This skill automatically enforces this requirement through:

- **Real-time validation** as you type
- **Pre-save blocking** (optional strict mode)
- **Quick-fix suggestions** for violations
- **Reconciliation manifest integration** for DIRTY flag management

---

## Features

### Core Validation

- ✅ **Mandatory Diagram Detection**: Ensures every SAD block tag has an accompanying ASCII diagram
- ✅ **Quality Validation**: Checks diagram structure, component relationships, and clarity
- ✅ **Multi-Style Support**: Recognizes box-and-arrow, hierarchical, and network topology diagrams
- ✅ **Character Recognition**: Validates use of standard ASCII/Unicode box drawing characters

### IDE Integration

- 🔴 **Inline Annotations**: Error/warning underlines in editor
- 🚦 **Gutter Icons**: Visual indicators for violations
- ⚡ **Quick Fixes**: One-click remediation actions
- 🔧 **Commands**: Manual validation and template insertion
- 🚫 **Pre-Save Blocking**: Prevents saving invalid documents (strict mode)

### Reconciliation Integration

- 📋 **DIRTY Flag Management**: Automatically updates reconciliation manifests
- 📊 **Violation Reporting**: Generates pending items for reconciliation system
- 🔄 **Impact Analysis**: Tracks diagram violations across documentation hierarchy

---

## Installation

### Prerequisites

- Antigravity IDE 1.16.5 or higher
- DDR Core Skill (>=2.0.0)
- RST Parser Skill (>=1.5.0)

### Install via Antigravity Marketplace

```bash
antigravity skill install ascii_diagram_enforcer
```

### Manual Installation

1. Clone repository:

   ```bash
   git clone https://github.com/ddr-system/ascii-diagram-enforcer.git
   cd ascii-diagram-enforcer
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Link to Antigravity:

   ```bash
   antigravity skill link .
   ```

4. Restart Antigravity IDE

---

## Configuration

Edit `skill.yaml` or configure via IDE settings:

### Basic Settings

```yaml
configuration:
  strict_mode: true              # Block save on ERROR violations
  min_diagram_lines: 3           # Minimum lines for valid diagram
  auto_flag_dirty: true          # Update reconciliation manifests
  violation_severity: "ERROR"    # Default severity level
```

### Advanced Settings

```yaml
configuration:
  allowed_diagram_styles:
    - box_and_arrow
    - hierarchical
    - network_topology

  validation_rules:
    - rule_id: "SAD-DIAGRAM-001"
      severity: "ERROR"            # Mandatory diagram rule
    - rule_id: "SAD-DIAGRAM-002"
      severity: "WARNING"          # Character recognition
```

---

## Usage

### Real-Time Validation

The skill automatically validates SAD-tier files as you edit them. Violations appear as:

- **Red underlines** for ERROR-level issues
- **Yellow underlines** for WARNING-level issues
- **Gutter icons** (🔴 error, 🟡 warning)

### Manual Validation

Trigger validation manually:

- **Command Palette**: `DDR: Validate ASCII Diagrams`
- **Keyboard Shortcut**: `Ctrl+Shift+D`

### Inserting Diagram Templates

Quick-insert a diagram template:

- **Command Palette**: `DDR: Insert ASCII Diagram Template`
- **Keyboard Shortcut**: `Ctrl+Alt+D`

### Quick Fixes

Click on violations to see available quick fixes:

1. **Insert Diagram Template** (for missing diagrams)
2. **View Example Diagrams** (for guidance)
3. **Fix Character Usage** (for unrecognized characters)

---

## Validation Rules

### Rule SAD-DIAGRAM-001 (ERROR)

**Every SAD block-level tag must have ASCII diagram**

❌ **Invalid**:

```rst
.. sad:: Hub-and-Spoke Architecture
   :id: SAD-1
   :links: FSD-1

(No diagram present)
```

✅ **Valid**:

```rst
.. sad:: Hub-and-Spoke Architecture
   :id: SAD-1
   :links: FSD-1

+-------------+     +-------------+     +-------------+
|     UI      | --> |    Core     | <-- |   Runtime   |
+-------------+     +-------------+     +-------------+
```

---

### Rule SAD-DIAGRAM-002 (WARNING)

**ASCII diagrams must use recognized box characters**

Standard characters:

- ASCII: `+ - | / \`
- Unicode: `┌ ┐ └ ┘ ─ │ ├ ┤ ┬ ┴ ┼`
- Arrows: `< > ^ v ← → ↑ ↓ ↔`

❌ **Invalid**:

```
[Core] ===> [UI]   # Using brackets instead of boxes
```

✅ **Valid**:

```
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
```

---

### Rule SAD-DIAGRAM-003 (ERROR)

**Diagrams must show component relationships**

Requirements:

- Minimum 2 components (boxes)
- Minimum 1 connection (arrow/line)

❌ **Invalid**:

```
+------+
| Core |     # Isolated component, no relationships
+------+
```

✅ **Valid**:

```
+------+     +------+
| Core | --> |  UI  |     # Shows relationship
+------+     +------+
```

---

### Rule SAD-DIAGRAM-004 (WARNING)

**Minimum 3 lines for structural clarity**

❌ **Invalid** (too simple):

```
Core --> UI
```

✅ **Valid** (structured):

```
+------+     +------+
| Core | --> |  UI  |
+------+     +------+
```

---

## Diagram Examples

### Box-and-Arrow Style

```
+---------------+          +------------------+          +-----------------+
|  UI (DEALER)  | <------> |   Core (ROUTER)  | <------> | Runtime (DEALER)|
+---------------+          +------------------+          +-----------------+
                                   |
                                   v
                           +------------------+
                           | Audio (DEALER)   |
                           +------------------+
```

### Hierarchical Style

```
                    +--------+
                    |  Core  |
                    +--------+
                    /    |    \
                   /     |     \
            +-----+   +-----+   +-----+
            | UI  |   | Audio|  | Runtime|
            +-----+   +-----+   +-----+
```

### Network Topology

```
    ┌─────────┐
    │   UI    │◄────┐
    └────┬────┘     │
         │          │
         ▼          │
    ┌─────────┐    │
    │  Core   │────┤
    └────┬────┘    │
         │         │
         ▼         │
    ┌─────────┐   │
    │ Runtime │───┘
    └─────────┘
```

---

## Integration with DDR System

### Reconciliation Manifests

When violations are detected, the skill automatically updates reconciliation manifests:

```rst
.. reconciliation_manifest:
   :section_id: sad-root
   :integrity_status: "DIRTY"
   :timestamp: "2026-02-20"
   :pending_items: [
     {
       "target_tag": "SAD-1",
       "source_trigger": "ascii_diagram_enforcer validation",
       "issue_type": "CONSTRAINT_VIOLATION",
       "description": "Missing mandatory ASCII diagram"
     }
   ]
```

### Traceability Chain

Diagram violations maintain full DDR traceability:

```
ASCII Diagram Violation → SAD-1 → FSD-1 → BRD-2
```

---

## API Reference

### Python API

```python
from ascii_diagram_enforcer.src.enforcer import ASCIIDiagramEnforcer

# Initialize enforcer
enforcer = ASCIIDiagramEnforcer(
    strict_mode=True,
    min_diagram_lines=3,
    auto_flag_dirty=True
)

# Validate section
content = read_file('docs/04_sad/architecture.rst')
result = enforcer.validate_section(content, 'sad-root')

# Check results
if not result.is_valid:
    print(f"Found {len(result.violations)} violations")
    for violation in result.violations:
        print(f"  [{violation.severity}] {violation.description}")
```

### Antigravity Plugin API

```python
from antigravity.plugin import get_plugin

# Access plugin instance
plugin = get_plugin('ascii_diagram_enforcer')

# Trigger validation
doc = context.get_active_document()
result = plugin._validate_document(doc)
```

---

## Troubleshooting

### Issue: Validation not triggering

**Solution**: Ensure document is in `docs/04_sad/` directory and has `.rst` or `.md` extension.

### Issue: False positives for valid diagrams

**Solution**: Check that diagram uses recognized box characters. Run `DDR: View Example Diagrams` to see valid patterns.

### Issue: Cannot save document (strict mode)

**Solution**: Fix ERROR-level violations or temporarily disable strict mode in settings:

```yaml
configuration:
  strict_mode: false
```

---

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Building from Source

```bash
python setup.py build
```

### Contributing

1. Fork the repository
2. Create feature branch: `git checkout -b feature/my-feature`
3. Run tests: `pytest`
4. Submit pull request

---

## License

MIT License - See LICENSE file for details

---

## Support

- **Issues**: <https://github.com/ddr-system/ascii-diagram-enforcer/issues>
- **Documentation**: <https://ddr-system.readthedocs.io>
- **Community**: <https://discord.gg/ddr-system>

---

## Changelog

### v1.0.0 (2026-02-20)

- Initial release
- Core validation engine
- Antigravity IDE integration
- Real-time validation
- Quick fix support
- Reconciliation manifest integration

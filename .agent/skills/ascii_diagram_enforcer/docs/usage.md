# ASCII Diagram Enforcer - Usage Guide

> **Skill Version**: 1.0.0
> **Target Users**: DDR System practitioners, technical writers, architects

## Quick Start

### 5-Minute Setup

1. **Install the skill** (if not already installed):

   ```bash
   antigravity skill install ascii_diagram_enforcer
   ```

2. **Open a SAD document**:
   - Navigate to `docs/04_sad/architecture.rst` (or any SAD file)

3. **Add a SAD tag**:

   ```rst
   .. sad:: My Architecture
      :id: SAD-1
      :links: FSD-1
   ```

4. **Insert a diagram** (Ctrl+Alt+D):

   ```
   +--------+     +--------+
   | Core   | --> |  UI    |
   +--------+     +--------+
   ```

5. **Validate** (Ctrl+Shift+D):
   - ✓ Green checkmark = compliant
   - ✗ Red error = violations

---

## Core Workflows

### Workflow 1: Creating a New SAD Section

**Scenario**: You're documenting a new architectural pattern

**Steps**:

1. **Create SAD file** in `docs/04_sad/`:

   ```bash
   touch docs/04_sad/message_routing.rst
   ```

2. **Add section header**:

   ```rst
   ==================================
   Message Routing Architecture
   ==================================
   ```

3. **Add SAD directive**:

   ```rst
   .. sad:: Hub-and-Spoke Routing
      :id: SAD-1
      :links: FSD-1
   ```

4. **Insert diagram template** (Ctrl+Alt+D):
   - Default template appears at cursor
   - Customize boxes and connections

5. **Validate in real-time**:
   - Yellow/red underlines appear immediately
   - Hover for violation details
   - Click quick fix to resolve

6. **Save** (Ctrl+S):
   - Strict mode: blocked if ERROR violations
   - Non-strict: warning notification only

---

### Workflow 2: Fixing Validation Errors

**Scenario**: You opened a SAD file with missing diagrams

**Steps**:

1. **Observe violations**:
   - Red underlines on SAD tags
   - 🔴 Error icons in gutter
   - Status bar: "✗ 3 violation(s)"

2. **View detailed report** (Ctrl+Shift+D):
   - Opens validation panel
   - Lists all violations with line numbers
   - Shows suggested fixes

3. **Fix each violation**:

   **Option A: Quick Fix**
   - Click violation → "Insert ASCII Diagram Template"
   - Customize template for your architecture

   **Option B: Manual**
   - Position cursor after SAD directive
   - Insert diagram:

     ```
     +------+     +------+
     | A    | --> | B    |
     +------+     +------+
     ```

   **Option C: Copy Example**
   - Command: "DDR: View ASCII Diagram Examples"
   - Find matching pattern
   - Copy and adapt

4. **Verify fix**:
   - Violations clear automatically
   - Green checkmark appears

5. **Save** (Ctrl+S):
   - Now allowed in strict mode

---

### Workflow 3: Understanding Validation Rules

**Rule SAD-DIAGRAM-001: Missing Diagram** (ERROR)

```rst
❌ INVALID:
.. sad:: Architecture
   :id: SAD-1
   :links: FSD-1

(No diagram)

✅ VALID:
.. sad:: Architecture
   :id: SAD-1
   :links: FSD-1

+------+     +------+
| Core | --> |  UI  |
+------+     +------+
```

**Rule SAD-DIAGRAM-002: Unrecognized Characters** (WARNING)

```rst
❌ AVOID:
[Core] ===> [UI]           # Brackets not standard

✅ CORRECT:
+------+     +------+
| Core | --> |  UI  |      # Standard box characters
+------+     +------+
```

**Rule SAD-DIAGRAM-003: Missing Relationships** (ERROR)

```rst
❌ INVALID:
+------+
| Core |                   # Isolated component
+------+

✅ VALID:
+------+     +------+
| Core | --> |  UI  |      # Shows relationship
+------+     +------+
```

**Rule SAD-DIAGRAM-004: Insufficient Clarity** (WARNING)

```rst
❌ TOO SIMPLE:
Core --> UI                # Only 1 line

✅ BETTER:
+------+     +------+
| Core | --> |  UI  |      # Structured boxes
+------+     +------+
```

---

## Keyboard Shortcuts

| Action | Shortcut | Description |
|:-------|:---------|:------------|
| Validate Diagrams | `Ctrl+Shift+D` | Run manual validation |
| Insert Template | `Ctrl+Alt+D` | Insert diagram boilerplate |
| View Examples | (command palette) | Open reference library |
| Quick Fix | `Ctrl+.` | Apply suggested fix |
| Go to Next Error | `F8` | Jump to next violation |

---

## Configuration

### Accessing Settings

1. **Via IDE**: Antigravity → Preferences → Skills → ASCII Diagram Enforcer
2. **Via File**: Edit `skill.yaml` in skill directory

### Key Configuration Options

```yaml
configuration:
  # Block save on ERROR violations
  strict_mode: true

  # Minimum diagram height
  min_diagram_lines: 3

  # Auto-update reconciliation manifests
  auto_flag_dirty: true

  # Violation severity
  violation_severity: "ERROR"

  # Allowed diagram styles
  allowed_diagram_styles:
    - box_and_arrow
    - hierarchical
    - network_topology
```

### Configuration Scenarios

**Scenario: Drafting Mode**

```yaml
strict_mode: false           # Don't block saves
violation_severity: "WARNING" # Downgrade all to warnings
```

**Scenario: Compliance Mode**

```yaml
strict_mode: true            # Block saves on errors
auto_flag_dirty: true        # Update manifests automatically
```

---

## Diagram Style Guide

### Box-and-Arrow (Most Common)

**Use for**: Process flows, service communication

```
+----------+     +----------+     +----------+
| Frontend | --> | Backend  | --> | Database |
+----------+     +----------+     +----------+
```

### Hierarchical (Tree)

**Use for**: Component hierarchies, org charts

```
        +--------+
        |  Root  |
        +--------+
        /         \
   +-----+      +-----+
   | Left|      |Right|
   +-----+      +-----+
```

### Network Topology (Mesh)

**Use for**: Distributed systems, peer networks

```
  +---+       +---+
  | A |-------| B |
  +---+       +---+
    |   \   /   |
    |    \ /    |
  +---+   X   +---+
  | D |-------| C |
  +---+       +---+
```

### Unicode Variants

**Use for**: Enhanced visual clarity

```
┌─────────┐     ┌─────────┐
│  Client │ ──> │  Server │
└─────────┘     └─────────┘
```

---

## Advanced Usage

### Working with Atomic Tags

**Atomic tags (SAD-N.M) inherit diagram requirements:**

```rst
.. sad:: Architecture Overview
   :id: SAD-1
   :links: FSD-1

+--------+
| System |      # Block diagram required
+--------+

.. sad:: Detail Point 1
   :id: SAD-1.1
   :links: SAD-1

Additional detail text.  # No diagram needed (inherits)

.. sad:: Detail Point 2
   :id: SAD-1.2
   :links: SAD-1

More detail text.        # No diagram needed (inherits)
```

### Multi-Diagram Sections

**Multiple block tags = multiple diagrams:**

```rst
.. sad:: High-Level Topology
   :id: SAD-1
   :links: FSD-1

+------+     +------+     +------+
| UI   | --> | Core | <-- | RT   |
+------+     +------+     +------+

.. sad:: Detailed Message Flow
   :id: SAD-2
   :links: FSD-2

Client          Core          Server
+-----+        +-----+        +-----+
|     | -----> | Q   | -----> |     |
+-----+        +-----+        +-----+
```

### Batch Validation

**Validate multiple files:**

```python
from ascii_diagram_enforcer.hooks.on_demand import validate_multiple_files

paths = [
    'docs/04_sad/architecture.rst',
    'docs/04_sad/topology.rst',
    'docs/04_sad/integration.rst'
]

results = validate_multiple_files(paths, context)
print(f"Valid: {results['valid_files']}")
print(f"Invalid: {results['invalid_files']}")
```

---

## Troubleshooting

### Problem: "Validation not triggering"

**Symptoms**: No underlines, gutter icons, or status updates

**Solutions**:

1. Verify file is in `docs/04_sad/` directory
2. Check file extension is `.rst` or `.md`
3. Ensure skill is activated (check Antigravity status bar)
4. Restart IDE if recently installed

### Problem: "False positive for valid diagram"

**Symptoms**: Error on diagram that looks correct

**Solutions**:

1. Check box characters: use `+` `-` `|` not `[` `]` `{` `}`
2. Ensure diagram is 3+ lines
3. Verify arrows between components (`-->`, not just spaces)
4. Add component labels inside boxes

### Problem: "Cannot save in strict mode"

**Symptoms**: Save blocked with error dialog

**Solutions**:

**Option 1: Fix violations**

- Use quick fixes (Ctrl+.)
- Insert diagram templates
- View validation report for details

**Option 2: Temporarily disable strict mode**

- Command: "DDR: Toggle Strict Mode"
- Settings: Set `strict_mode: false`

**Option 3: Save anyway (not recommended)**

- Disable skill temporarily
- Fix violations after save

### Problem: "Too many warnings"

**Symptoms**: Warnings about character usage, clarity, etc.

**Solutions**:

- Warnings are advisory only (don't block saves)
- Address warnings for quality improvement
- Lower priority than ERROR violations
- Can be ignored during drafting

---

## Best Practices

### 1. Diagram Early

✅ **Do**: Add diagrams as you write SAD sections
❌ **Don't**: Defer diagramming until the end

### 2. Keep Diagrams Simple

✅ **Do**: Focus on key architectural relationships
❌ **Don't**: Overload diagrams with every detail

### 3. Use Consistent Style

✅ **Do**: Pick one box character style per project
❌ **Don't**: Mix ASCII and Unicode inconsistently

### 4. Label Components

✅ **Do**: Put descriptive names in boxes
❌ **Don't**: Use generic labels like "A", "B", "C"

### 5. Align with FSD

✅ **Do**: Diagram should illustrate cited FSD behaviors
❌ **Don't**: Diagram unrelated architecture

---

## Integration with DDR Workflow

### Phase 1: Requirements (BRD/NFR/FSD)

- Define features and constraints
- **No diagrams yet** (not SAD tier)

### Phase 2: Architecture (SAD) ← YOU ARE HERE

- Create SAD sections
- **Add ASCII diagrams** (enforced by this skill)
- Illustrate system structure

### Phase 3: Design (ICD/TDD)

- Define interfaces and classes
- Cite SAD tags (including diagrammed architecture)

### Phase 4: Implementation (ISP)

- Generate code stubs
- Trace back through SAD to BRD

---

## Getting Help

### In-IDE Help

- **Command Palette**: "DDR: Help" → ASCII Diagram Enforcer
- **Hover Tooltips**: Hover over violations for quick info
- **Example Library**: "DDR: View ASCII Diagram Examples"

### Documentation

- **This Guide**: `docs/usage.md`
- **Architecture**: `docs/architecture.md`
- **API Reference**: `docs/api.md`

### Community Support

- **GitHub Issues**: <https://github.com/ddr-system/ascii-diagram-enforcer/issues>
- **DDR Discord**: <https://discord.gg/ddr-system>
- **Documentation**: <https://ddr-system.readthedocs.io>

---

## Appendix: Complete Example

```rst
====================================
Message Routing Architecture (SAD)
====================================

.. sad:: Hub-and-Spoke IPC Topology
   :id: SAD-1
   :links: FSD-1

The system uses a central Core process as a ROUTER hub, with all
peripheral services as DEALER clients. This enables centralized
message routing and request/response correlation.

**Topology:**

::

   +----------------+          +------------------+          +-----------------+
   |   UI Service   |          |   Core Process   |          | Runtime Service |
   |   (DEALER)     | <------> |     (ROUTER)     | <------> |    (DEALER)     |
   +----------------+          +------------------+          +-----------------+
                                        |
                                        |
                                +--------------+
                                |     Audio    |
                                |   (DEALER)   |
                                +--------------+

.. sad:: Non-Blocking I/O Strategy
   :id: SAD-1.1
   :links: SAD-1

Each DEALER service uses non-blocking sockets with internal queue buffering
to prevent blocking on send operations.

(No diagram needed - atomic tag inherits from SAD-1)


.. reconciliation_manifest:
   :section_id: "sad-message-routing"
   :integrity_status: "CLEAN"
   :timestamp: "2026-02-20"
   :tag_count: 2
   :tag_inventory: ["SAD-1", "SAD-1.1"]
   :pending_items: []
```

---

**Next Steps**: See [API Reference](api.md) for programmatic usage.

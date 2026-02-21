# ASCII Diagram Enforcer - Architecture Documentation

> **Version**: 1.0.0
> **Last Updated**: 2026-02-20

## Table of Contents

- [System Overview](#system-overview)
- [Component Architecture](#component-architecture)
- [Data Flow](#data-flow)
- [Integration Points](#integration-points)
- [Design Decisions](#design-decisions)

---

## System Overview

The ASCII Diagram Enforcer is a modular validation skill for the DDR (Development Documentation Roadmap) System. It enforces mandatory ASCII topology diagrams in SAD-tier (System Architecture Document) documentation through real-time IDE integration and automated quality checks.

### Core Purpose

**Enforce DDR Constraint**: Every SAD block-level tag (format: `SAD-N`) MUST include an ASCII diagram illustrating architectural patterns, component relationships, or system structure.

### Design Philosophy

1. **Separation of Concerns**: Detection, parsing, validation, and enforcement are independent modules
2. **Graceful Degradation**: Works standalone or integrates with full DDR ecosystem
3. **Non-Blocking by Default**: Warnings don't prevent work; errors require resolution in strict mode
4. **Developer-Friendly**: Clear feedback, quick fixes, and helpful examples

---

## Component Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Antigravity IDE Plugin                      │
│         (antigravity_plugin.py)                         │
│  • Event handling (open/change/save)                    │
│  • UI integration (annotations, gutter icons)           │
│  • Command registration                                 │
└────────────────┬────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────┐
│           Core Enforcer (enforcer.py)                   │
│  • Orchestrates validation workflow                     │
│  • Manages sub-component lifecycle                      │
│  • Generates reports and results                        │
└─────┬───────────────┬───────────────┬───────────────────┘
      │               │               │
      v               v               v
┌──────────┐   ┌──────────┐   ┌──────────┐
│ Diagram  │   │   SAD    │   │ Diagram  │
│ Detector │   │  Parser  │   │Validator │
└──────────┘   └──────────┘   └──────────┘
│              │              │
│ • Pattern    │ • RST        │ • Quality  │
│   matching   │   parsing    │   rules    │
│ • Style      │ • Tag        │ • Character│
│   classification│ extraction │   validation│
│ • Confidence │ • Citation   │ • Structural│
│   scoring    │   parsing    │   checks   │
└──────────┘   └──────────┘   └──────────┘
      │               │               │
      v               v               v
┌─────────────────────────────────────────────────────────┐
│                    Hooks Layer                           │
│  ┌────────────┐  ┌────────────┐  ┌─────────────────┐   │
│  │ Pre-Save   │  │ On-Demand  │  │ Reconciliation  │   │
│  │ Validation │  │ Validation │  │  Integration    │   │
│  └────────────┘  └────────────┘  └─────────────────┘   │
└─────────────────────────────────────────────────────────┘
                 │
                 v
┌─────────────────────────────────────────────────────────┐
│         DDR System Integration (ddr_bridge.py)          │
│  • Traceability chain validation                        │
│  • Cross-tier impact analysis                           │
│  • Manifest synchronization                             │
└─────────────────────────────────────────────────────────┘
```

---

## Component Details

### 1. Diagram Detector

**Responsibility**: Identify ASCII diagrams in document content

**Algorithm**:

1. Line-by-line scanning for box/arrow characters
2. Region extraction (consecutive diagram lines)
3. Style classification (box-and-arrow, hierarchical, network)
4. Confidence scoring (multi-factor 0.0-1.0 scale)

**Confidence Factors**:

- Box character density (30% weight)
- Arrow/connector presence (20% weight)
- Alignment consistency (25% weight)
- Style coherence (25% weight)

**Supported Styles**:

- **Box-and-Arrow**: Rectangular boxes with directional arrows
- **Hierarchical**: Tree-like parent-child structures
- **Network Topology**: Mesh of interconnected nodes

### 2. SAD Parser

**Responsibility**: Extract SAD tags from RST directives

**Parsing Strategy**:

```python
Pattern: .. sad:: <title>
         :id: <TAG-ID>
         :links: <PARENT-IDS>
```

**Tag Levels**:

- **Block**: `SAD-N` format (require diagrams)
- **Atomic**: `SAD-N.M` format (inherit from parent)

**Validation**:

- Tag ID format compliance
- Citation hierarchy rules
- Parent tag existence

### 3. Diagram Validator

**Responsibility**: Assess diagram quality

**Validation Rules**:

| Rule ID | Check | Severity |
|:--------|:------|:---------|
| SAD-DIAGRAM-001 | Diagram exists | ERROR |
| SAD-DIAGRAM-002 | Recognized characters | WARNING |
| SAD-DIAGRAM-003 | Component relationships | ERROR |
| SAD-DIAGRAM-004 | Structural clarity | WARNING |

**Quality Metrics**:

- Minimum 2 components (boxes)
- Minimum 1 connection (arrow/line)
- Minimum 3 lines for structure
- Component labels present

### 4. Core Enforcer

**Responsibility**: Orchestrate validation workflow

**Workflow**:

```
1. Parse SAD tags
2. Filter block-level tags
3. Detect ASCII diagrams
4. Associate diagrams to tags
5. Validate each block tag
6. Generate violation report
7. Update reconciliation manifest
```

**Result Structure**:

```python
ValidationResult:
  - section_id: str
  - is_valid: bool
  - violations: List[Violation]
  - sad_tags_found: int
  - diagrams_found: int
  - missing_diagrams: Set[str]
```

---

## Data Flow

### Real-Time Validation Flow

```
User Types in Editor
        |
        v
Document Changed Event (debounced 500ms)
        |
        v
Plugin Handler (on_document_changed)
        |
        v
Enforcer.validate_section()
        |
        +----> SAD Parser: Extract tags
        |
        +----> Diagram Detector: Find diagrams
        |
        +----> Association: Match diagrams to tags
        |
        +----> Validator: Check quality
        |
        v
ValidationResult
        |
        +----> Update Annotations (red/yellow underlines)
        |
        +----> Update Gutter Icons (error/warning)
        |
        +----> Update Status Bar
```

### Pre-Save Validation Flow

```
User Saves (Ctrl+S)
        |
        v
Pre-Save Hook (pre_save.py)
        |
        v
Enforcer.validate_section()
        |
        v
Check Strict Mode + Error Count
        |
        +----> Errors & Strict = TRUE
        |           |
        |           v
        |      Block Save + Show Dialog
        |
        +----> No Errors or Strict = FALSE
                    |
                    v
               Allow Save
```

### Reconciliation Integration Flow

```
Validation Complete (violations found)
        |
        v
Reconciliation Hook
        |
        v
Parse Existing Manifest
        |
        v
Update Fields:
  - integrity_status: "DIRTY"
  - timestamp: <current date>
  - pending_items: [violations...]
        |
        v
Replace Manifest in Document
        |
        v
Optionally Trigger DDR Bridge
        |
        v
Sync with Manifest Manager Skill
```

---

## Integration Points

### 1. Antigravity IDE

**Plugin Interface**:

- `SkillPlugin` base class
- Event handlers: `on_activate`, `on_document_opened`, `on_document_changed`, `on_before_save`
- Command registration
- UI components: annotations, gutter icons, panels

**Communication**:

- Plugin ↔ Enforcer: Direct method calls
- UI updates: Context methods (`show_error`, `show_panel`, etc.)

### 2. DDR Core Skill

**Optional Integration**:

- Traceability chain validation
- Impact analysis (find downstream TDD/ISP citations)
- Cross-tier consistency checks

**Graceful Degradation**:

- Works standalone without DDR Core
- Full features require DDR Core >=2.0.0

### 3. Manifest Manager Skill

**Optional Integration**:

- Centralized manifest tracking
- Cross-document integrity
- Automated reconciliation passes

### 4. File System

**Read Operations**:

- Document content (via IDE)
- Configuration files (YAML)
- Test fixtures

**Write Operations**:

- Updated document content (manifest changes)
- Validation reports (IDE panels)

---

## Design Decisions

### 1. Why Multi-Component Architecture?

**Decision**: Separate detector, parser, validator rather than monolithic enforcer

**Rationale**:

- **Testability**: Each component independently testable
- **Reusability**: Detector/parser usable by other skills
- **Maintainability**: Clear boundaries for bug fixes
- **Extensibility**: Easy to add new diagram styles or rules

### 2. Why Confidence Scoring?

**Decision**: Multi-factor weighted scoring vs. binary detection

**Rationale**:

- ASCII diagrams are inherently ambiguous
- Avoid false positives (plain text with +/- characters)
- Allow quality spectrum (perfect vs. acceptable diagrams)
- Configurable threshold for strictness tuning

### 3. Why Separate Block vs. Atomic Tags?

**Decision**: Only block tags require diagrams

**Rationale**:

- Atomic tags provide additional detail within parent scope
- Requiring diagrams for every atomic tag = excessive burden
- Parent block diagram covers architectural scope
- Aligns with DDR hierarchical principles

### 4. Why Hooks Layer?

**Decision**: Separate hook modules vs. inline in plugin

**Rationale**:

- **Modularity**: Each hook independently developable
- **Clarity**: Hook logic separated from plugin boilerplate
- **Testability**: Hooks testable without full IDE context
- **Reusability**: Hooks usable in CLI or other contexts

### 5. Why Two Severity Levels?

**Decision**: ERROR (blocking) vs. WARNING (advisory)

**Rationale**:

- **Developer experience**: Don't block on minor quality issues
- **Compliance**: Block on mandatory requirements (missing diagrams)
- **Flexibility**: Strict mode for compliance, relaxed for drafting
- **Prioritization**: Clear signal of what must be fixed

### 6. Why Debounced Real-Time Validation?

**Decision**: 500ms debounce on document changes

**Rationale**:

- **Performance**: Avoid validation on every keystroke
- **User experience**: No lag during rapid typing
- **Efficiency**: Batch changes before validation
- **Standard practice**: Common IDE pattern

### 7. Why Reconciliation Manifest Integration?

**Decision**: Auto-update manifests vs. manual reconciliation

**Rationale**:

- **DDR Compliance**: Manifests are required by DDR System
- **Traceability**: Violations tracked in DIRTY flags
- **Automation**: Reduce manual reconciliation burden
- **Consistency**: Uniform violation tracking across tiers

---

## Performance Characteristics

### Time Complexity

| Operation | Complexity | Notes |
|:----------|:-----------|:------|
| Parse SAD tags | O(n) | n = document lines |
| Detect diagrams | O(n) | Linear scan |
| Validate tag | O(1) | Per-tag constant |
| Full validation | O(n + m) | n = lines, m = tags |

### Space Complexity

| Component | Memory Usage |
|:----------|:-------------|
| Document content | O(n) - single copy |
| Parsed tags | O(m) - minimal metadata |
| Diagrams | O(d) - diagram count |
| Violations | O(v) - violation count |

### Optimization Strategies

1. **Early termination**: Stop scanning when diagram found
2. **Caching**: Store validation results per document
3. **Incremental**: Only re-validate changed sections (future)
4. **Lazy loading**: Load fixtures/examples on demand

---

## Security Considerations

### Input Validation

- **Document content**: No arbitrary code execution
- **Tag IDs**: Regex validation before processing
- **Configuration**: YAML safe loading only

### File System Access

- **Read-only**: No destructive file operations
- **Sandboxed**: Limited to project docs directory
- **Validated paths**: Check tier directory structure

### External Communication

- **No network**: Entirely local validation
- **No telemetry**: No data sent to external services
- **Privacy**: Document content never leaves IDE

---

## Future Enhancements

### Planned Features

1. **Auto-fix**: Automatically insert diagram templates
2. **Diagram diff**: Visual comparison of diagram changes
3. **Style detection**: Learn project-specific diagram conventions
4. **Batch validation**: Validate entire SAD directory
5. **Incremental validation**: Only re-check changed tags

### Research Areas

1. **Machine learning**: Train model on valid diagrams
2. **Natural language**: Generate diagrams from prose descriptions
3. **Graph analysis**: Verify diagram matches cited FSD behaviors
4. **Visualization**: Render ASCII diagrams as SVG/PNG

---

## References

- DDR System Specification: `ddr_meta_standard.txt`
- Tier SAD Definition: `concepts/tier_sad.md`
- Antigravity Plugin API: Antigravity IDE 1.16.5 documentation
- Box Drawing Characters: Unicode Standard Annex #11

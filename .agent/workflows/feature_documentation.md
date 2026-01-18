---
type: workflow
name: "Complete Feature Documentation"
slug: /complete_feature
description: "Full 9-stage DDR workflow: Classify → BRD → NFR → FSD → SAD → ICD → TDD → ISP → Validate"
mode: autonomous
inputs:
  - name: feature_description
    type: string
    description: "Natural language description of the feature"
    required: true
  - name: skip_tiers
    type: array
    description: "Optional tiers to skip (e.g., ['NFR'] if no quality constraints)"
    required: false
context:
  - ".agent/knowledge/sources/patterns/worked_example_feature.md"
  - ".agent/knowledge/sources/concepts/tier_hierarchy.md"
  - ".agent/knowledge/sources/protocols/classification_decision_tree.md"
outputs:
  - name: tag_chain
    type: object
    description: "Map of tier → tag_id for all created tags"
  - name: validation_report
    type: string
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Complete Feature Documentation

## Stage 1: Classification

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/classify_information.py" --input "{{inputs.feature_description}}"
```

---

## Stage 2: BRD Creation

**@brd_strategist**: Draft business requirement.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier BRD --title "{{feature_title}}" --description "{{brd_content}}"
```

---

## Stage 3: NFR Extraction

**@nfr_enforcer**: Extract non-functional constraints.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier NFR --parent "{{brd_id}}" --title "{{nfr_title}}"
```

---

## Stage 4: FSD Definition

**@fsd_analyst**: Define feature behavior.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier FSD --parent "{{brd_id}}" --title "{{fsd_title}}"
```

---

## Stage 5: SAD Architecture

**@sad_architect**: Design component topology.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier SAD --parent "{{fsd_id}}" --title "{{sad_title}}"
```

---

## Stage 6: ICD Interfaces

**@icd_dataengineer**: Specify interface contracts.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier ICD --parent "{{sad_id}}" --title "{{icd_title}}"
```

---

## Stage 7: TDD Design

**@tdd_designer**: Document technical design.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier TDD --parent "{{icd_id}}" --title "{{tdd_title}}"
```

---

## Stage 8: ISP Generation

**@isp_codegenerator**: Generate implementation stub.

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier ISP --parent "{{tdd_id}}" --title "{{isp_title}}"
```

---

## Stage 9: Validation

// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/generate_traceability_report.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json" --format summary
```

---
type: workflow
name: "Document Feature (BRD→ISP)"
slug: /document_feature
description: "Complete seven-tier documentation workflow from Business Requirements to Implementation Stubs."
mode: autonomous
inputs:
  - name: feature_description
    type: string
    description: "Natural language description of the feature to document"
    required: true
context:
  - ".agent/knowledge/sources/patterns/worked_example_feature.md"
  - ".agent/knowledge/sources/protocols/classification_decision_tree.md"
outputs:
  - name: brd_id
    type: string
  - name: tier_ids
    type: object
    description: "Map of tier to tag IDs created"
on_finish: "suggest_followup: /audit_traceability"
---

# Workflow: Document Feature (BRD→ISP)

## Phase 1: Classification
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/classify_information.py" --input "{{inputs.feature_description}}"
```

## Phase 2: Tier Cascade
// turbo
### 2.1 Create BRD
**@brd_strategist**: Draft business requirement.
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier BRD --title "{{feature_title}}"
```

### 2.2 Create NFR
**@nfr_enforcer**: Extract non-functional constraints.
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/create_tag.py" --tier NFR --parent "{{brd_id}}"
```

### 2.3 Create FSD
**@fsd_analyst**: Define feature behavior.

### 2.4 Create SAD
**@sad_architect**: Design architecture.

### 2.5 Create ICD
**@icd_dataengineer**: Specify interfaces.

### 2.6 Create TDD
**@tdd_designer**: Document technical design.

### 2.7 Create ISP
**@isp_codegenerator**: Generate implementation stub.

## Phase 3: Validation
// turbo
```powershell
& "${workspaceFolder}/.venv/Scripts/python" "${workspaceFolder}/.agent/scripts/generate_traceability_report.py" --needs-json "${workspaceFolder}/docs/_build/json/needs.json" --format summary
```

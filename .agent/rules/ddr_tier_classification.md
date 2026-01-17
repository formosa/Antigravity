---
type: rule
name: "DDR Tier Classification"
globs:
  - "docs/**/*.rst"
priority: 50
trigger:
  - "classify"
  - "tier"
  - "documentation"
severity: mandatory
description: "Always classify information by tier before processing using the DDR decision tree."
---
# DDR Tier Classification Rule

## Rule Statement

**Before any documentation task, apply the classification decision tree to determine the correct tier.**

## Decision Tree

1. **Q1: WHY?** Business value, ROI, market need?
   - YES → **BRD** | NO → Continue

2. **Q2: LIMITS?** Constraints, SLAs, hardware specs?
   - YES → **NFR** | NO → Continue

3. **Q3: WHAT?** Capabilities, features, user interactions?
   - YES → **FSD** | NO → Continue

4. **Q4: HOW?** Architectural patterns, process topology?
   - YES → **SAD** | NO → Continue

5. **Q5: SCHEMA?** Data formats, message structures?
   - YES → **ICD** | NO → Continue

6. **Q6: CLASS?** Class structure, methods, dependencies?
   - YES → **TDD** | NO → **ISP**

## Enforcement

| Result | Next Action |
|:-------|:------------|
| Clear tier match | Create tag in appropriate tier |
| Ambiguous | Use scoring matrix |
| No match | Decompose fragment |
| Mixed-tier content | Split into separate tags |

## References

- Knowledge: `protocols/classification_decision_tree.md`
- Knowledge: `protocols/classification_scoring.md`
- Source: DDR Meta-Standard §4.1, §4.2

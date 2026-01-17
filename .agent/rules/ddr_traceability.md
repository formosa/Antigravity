---
type: rule
name: "DDR Traceability Rules"
globs:
  - "docs/**/*.rst"
priority: 50
trigger:
  - "traceability"
  - "audit"
  - "validation"
severity: mandatory
description: "Enforces DDR hierarchy, citation, and anti-drift rules on Sphinx-Needs documentation."
---

# DDR Traceability Rules

Validate documentation integrity via /validate_ddr before committing document changes. This rule defines the validation constraints for Sphinx-Needs documentation based on the DDR meta-standard.

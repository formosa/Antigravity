---
type: rule
name: "Immutable Assets Protection"
globs:
  - ".agent/assets/**/*"
priority: 100
trigger:
  - "edit"
  - "update"
  - "modify"
  - "delete"
  - "overwrite"
severity: mandatory
description: "The .agent/assets/ directory contains strict project standards and reference schemas. These files are READ-ONLY. You are strictly forbidden from editing, modifying, overwriting, or deleting any file in this directory. EXCEPTION: If a user request specifically requires changes to these files, you must HALT execution, list the specific files to be changed, and explicitly ask the user for approval before proceeding."
---

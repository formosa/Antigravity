$targetRoot = ".\"
$agentRoot = Join-Path $targetRoot ".agent"

# Define directories
$directories = @(
    "config", "evals", "plans", "rules", "schemas", "scripts", "skills", "tools", "workflows", ".temp"
)

foreach ($dir in $directories) {
    $path = Join-Path $agentRoot $dir
    if (-not (Test-Path $path)) {
        New-Item -ItemType Directory -Path $path -Force | Out-Null
        Write-Host "Created directory: $path"
    }
}

# Define file templates
$files = @{}

# 1. Rules Governance
$files["rules\rules-governance.md"] = @"
---
name: "rules-governance"
description: "Glob-scoped collection governance rule for the .agent/rules/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/rules/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Scope Boundary: This rule governs only assets under `.agent/rules/`.
2. Rule Frontmatter Contract: Rule assets MUST satisfy the YAML frontmatter requirements (`name`, `version`, `description`, `trigger`, `priority`).
3. Rule Body Fencing: Rule assets MUST wrap all body content inside a non-empty `<constraints>` block and MAY include a `<verification_step>` block.
</constraints>

<verification_step>
Confirm all rules conform to the basic frontmatter and body fencing requirements.
</verification_step>
"@

# 2. Skills Governance
$files["rules\skills-governance.md"] = @"
---
name: "skills-governance"
description: "Glob-scoped collection governance rule for the .agent/skills/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/skills/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Root README Update Required: When any file under `.agent/skills/<skill-name>/` changes, update that skill's root `README.md`.
2. Version Synchronization: The changed skill's `SKILL.md` version MUST be incremented in the same task.
3. Schema Ownership: Skill-local schema mirrors are read-only.
</constraints>

<verification_step>
Before finishing any task that changes files under `.agent/skills/`, verify the updated root `README.md` and semantic version matches.
</verification_step>
"@

# 3. Schemas Governance
$files["rules\schemas-governance.md"] = @"
---
name: "schemas-governance"
description: "Glob-scoped collection governance rule for the .agent/schemas/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/schemas/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Definition Contract: Schema files MUST be standard valid format (e.g. `d.ts`, `json`).
2. Version Bumps: Changes require a version bump in the `README.md`.
</constraints>

<verification_step>
Verify schema structural validity before concluding tasks.
</verification_step>
"@

# 4. Workflows Governance
$files["rules\workflows-governance.md"] = @"
---
name: "workflows-governance"
description: "Glob-scoped collection governance rule for the .agent/workflows/ directory."
version: "1.0.0"
trigger: "glob"
globs: ".agent/workflows/**"
priority: "critical"
execution_tier: "standard"
---

<constraints>
1. Workflow format: MUST be markdown based with clear numbered steps.
2. Step triggers: Steps that can be auto-executed should be marked with `// turbo` if safe.
</constraints>

<verification_step>
Verify that workflows use clear explicit directives.
</verification_step>
"@

# 5. Skill Schema
$files["schemas\skill\skill.d.ts"] = @"
// Base Skill Asset Configuration Schema
interface SkillDefinition {
    frontmatter: {
        name?: string;
        version: string;
        description: string;
    };
    body_content: {
        when_to_use: string;
        how_to_use: string;
        constraints: string;
        resources_reference: string;
    };
}
"@
$files["schemas\skill\README.md"] = @"
# Skill Schema

## Description
This directory contains the canonical schemas and definitions for `Skill` assets in this repository.

## Modification History
| Date       | Version | Changes                      |
|------------|---------|------------------------------|
| $(Get-Date -Format "yyyy-MM-dd") | 1.0.0   | Initial base initialization. |
"@

# 6. Rule Schema
$files["schemas\rule\rule.d.ts"] = @"
// Base Rule Asset Configuration Schema
interface RuleDefinition {
    frontmatter: {
        name?: string;
        version: string;
        description: string;
        trigger: "glob" | "regex" | "always" | "never" | "event";
        globs?: string | string[];
        priority: "critical" | "high" | "standard" | "low";
        execution_tier?: "standard" | "heavy";
    };
    body_content: {
        constraints: string;
        verification_step?: string;
    };
}
"@
$files["schemas\rule\README.md"] = @"
# Rule Schema

## Description
This directory contains the canonical schemas and definitions for `Rule` assets in this repository.

## Modification History
| Date       | Version | Changes                      |
|------------|---------|------------------------------|
| $(Get-Date -Format "yyyy-MM-dd") | 1.0.0   | Initial base initialization. |
"@

# 7. Workflow Schema
$files["schemas\workflow\workflow.d.ts"] = @"
// Base Workflow Asset Configuration Schema
interface WorkflowDefinition {
    frontmatter: {
        name?: string;
        version: string;
        description: string;
    };
    body_content: {
        steps: string;
    };
}
"@
$files["schemas\workflow\README.md"] = @"
# Workflow Schema

## Description
This directory contains the canonical schemas and definitions for `Workflow` assets in this repository.

## Modification History
| Date       | Version | Changes                      |
|------------|---------|------------------------------|
| $(Get-Date -Format "yyyy-MM-dd") | 1.0.0   | Initial base initialization. |
"@

# 8. Base Skill: asset-skill
$files["skills\asset-skill\SKILL.md"] = @"
---
name: "asset-skill"
version: "1.0.0"
description: "Authors or refines compatible skills with explicit trigger boundaries and standard layouts."
---

<when_to_use>
- Creating a new skill asset.
- Modifying an existing skill asset's core capabilities.
</when_to_use>

<how_to_use>
1. Understand the goal of the new skill.
2. Scaffold a new folder in `.agent/skills/<skill-name>`.
3. Create the `SKILL.md` satisfying the canonical schema.
4. Create the `README.md` to track modification history.
</how_to_use>

<constraints>
- MUST strictly follow `skill.d.ts` schema.
- MUST define clear, bounded usage guidelines.
</constraints>

<resources_reference>
- `.agent/schemas/skill/skill.d.ts` (Read to understand skill structure requirements).
</resources_reference>
"@

$files["skills\asset-skill\README.md"] = @"
# asset-skill

## Modification History
| Date       | Version | Changes                      |
|------------|---------|------------------------------|
| $(Get-Date -Format "yyyy-MM-dd") | 1.0.0   | Initial base initialization. |
"@

# 9. Base Skill: asset-rule
$files["skills\asset-rule\SKILL.md"] = @"
---
name: "asset-rule"
version: "1.0.0"
description: "Authors or refines compatible rule assets with explicit trigger boundaries."
---

<when_to_use>
- Creating a new governance rule.
- Modifying an existing rule.
</when_to_use>

<how_to_use>
1. Identify the need for the rule.
2. Create the file in `.agent/rules/<rule-name>.md`.
3. Fill out the YAML frontmatter and `<constraints>`.
</how_to_use>

<constraints>
- MUST strictly follow `rule.d.ts` schema.
</constraints>

<resources_reference>
- `.agent/schemas/rule/rule.d.ts` (Read to understand rule structure requirements).
</resources_reference>
"@

$files["skills\asset-rule\README.md"] = @"
# asset-rule

## Modification History
| Date       | Version | Changes                      |
|------------|---------|------------------------------|
| $(Get-Date -Format "yyyy-MM-dd") | 1.0.0   | Initial base initialization. |
"@

# Write files to disk
foreach ($entry in $files.GetEnumerator()) {
    $filePath = Join-Path $agentRoot $entry.Key
    $dirPath = Split-Path $filePath -Parent
    
    if (-not (Test-Path $dirPath)) {
        New-Item -ItemType Directory -Path $dirPath -Force | Out-Null
    }
    
    if (-not (Test-Path $filePath)) {
        Set-Content -Path $filePath -Value $entry.Value
        Write-Host "Created file: $filePath"
    } else {
        Write-Host "File already exists, skipping: $filePath"
    }
}

Write-Host ""
Write-Host "Agent Assets scaffold initialization complete!"

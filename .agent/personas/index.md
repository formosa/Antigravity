# Agent Personas Index

> Master registry of all specialized agent personas.
>
> **Total Personas**: 17
>
> **Content Strategy**: [`persona-content-strategy.md`](../knowledge/sources/patterns/persona-content-strategy.md)
>
> **Parent**: [`.agent/`](..)

## Quick Lookup

| File                                                 | Handle                  | Purpose                                                                |
| :--------------------------------------------------- | :---------------------- | :--------------------------------------------------------------------- |
| [consultant.mdc](consultant.mdc)                     | `@consultant`           | Optimization-focused design & implementation advisor                   |
| [design-lead.mdc](design-lead.mdc)                   | `@design_lead`          | Adversarial design architect for documentation integrity               |
| [tech-lead.mdc](tech-lead.mdc)                       | `@tech_lead`            | Skeptical development environment architect                            |
| [ddr-orchestrator.mdc](ddr-orchestrator.mdc)         | `@ddr_orchestrator`     | Master DDR orchestrator; routes tasks to tier specialists              |
| [brd-strategist.mdc](brd-strategist.mdc)             | `@brd_strategist`       | Strategic business analyst for BRD tier content                        |
| [nfr-enforcer.mdc](nfr-enforcer.mdc)                 | `@nfr_enforcer`         | Non-functional requirements specialist; enforces numeric constraints   |
| [fsd-analyst.mdc](fsd-analyst.mdc)                   | `@fsd_analyst`          | Feature specification analyst; translates business intent to behavior  |
| [sad-architect.mdc](sad-architect.mdc)               | `@sad_architect`        | System architecture specialist; defines topology and patterns          |
| [icd-dataengineer.mdc](icd-dataengineer.mdc)         | `@icd_dataengineer`     | Interface contracts specialist; defines immutable data shapes          |
| [tdd-designer.mdc](tdd-designer.mdc)                 | `@tdd_designer`         | Technical design specialist; blueprints component structure            |
| [isp-codegenerator.mdc](isp-codegenerator.mdc)       | `@isp_codegenerator`    | Python stub generator with Numpy-style docstrings and traceability     |
| [antipattern-scanner.mdc](antipattern-scanner.mdc)   | `@antipattern_scanner`  | Enforces DDR architectural boundaries via pattern matching             |
| [orphan-detective.mdc](orphan-detective.mdc)         | `@orphan_detective`     | Graph topology validation via strict citation matrices                 |
| [traceability-auditor.mdc](traceability-auditor.mdc) | `@traceability_auditor` | Cross-tier chain validation; detects orphans, cycles, and broken links |
| [manifest-manager.mdc](manifest-manager.mdc)         | `@manifest_manager`     | Reconciliation manifest and inventory synchronization                  |
| [migration-assistant.mdc](migration-assistant.mdc)   | `@migration_assistant`  | Safe deprecation, versioning, and refactoring workflows                |
| [tag-reconciler.mdc](tag-reconciler.mdc)             | `@tag_reconciler`       | Dirty-flag propagation and conflict resolution                         |

---

## By Category

### Leadership & Advisory (3)

| File                               | Handle         | Content Strategy   | Purpose                                                  |
| :--------------------------------- | :------------- | :----------------- | :------------------------------------------------------- |
| [consultant.mdc](consultant.mdc)   | `@consultant`  | Refs-only          | Optimization-focused design & implementation advisor     |
| [design-lead.mdc](design-lead.mdc) | `@design_lead` | Refs-only          | Adversarial design architect for documentation integrity |
| [tech-lead.mdc](tech-lead.mdc)     | `@tech_lead`   | Refs-only          | Skeptical development environment architect              |

---

### Orchestration (1)

| File                                         | Handle              | Content Strategy   | Purpose                                                   |
| :------------------------------------------- | :------------------ | :----------------- | :-------------------------------------------------------- |
| [ddr-orchestrator.mdc](ddr-orchestrator.mdc) | `@ddr_orchestrator` | Refs-only          | Master DDR orchestrator; routes tasks to tier specialists |

---

### Tier Specialists (7)

| File                                           | Handle               | Tier   | Content Strategy   | Purpose                                                               |
| :--------------------------------------------- | :------------------- | :----- | :----------------- | :-------------------------------------------------------------------- |
| [brd-strategist.mdc](brd-strategist.mdc)       | `@brd_strategist`    | BRD    | Refs-only          | Strategic business analyst for BRD tier content                       |
| [nfr-enforcer.mdc](nfr-enforcer.mdc)           | `@nfr_enforcer`      | NFR    | Refs-only          | Non-functional requirements specialist; enforces numeric constraints  |
| [fsd-analyst.mdc](fsd-analyst.mdc)             | `@fsd_analyst`       | FSD    | Refs-only          | Feature specification analyst; translates business intent to behavior |
| [sad-architect.mdc](sad-architect.mdc)         | `@sad_architect`     | SAD    | Refs-only          | System architecture specialist; defines topology and patterns         |
| [icd-dataengineer.mdc](icd-dataengineer.mdc)   | `@icd_dataengineer`  | ICD    | Refs-only          | Interface contracts specialist; defines immutable data shapes         |
| [tdd-designer.mdc](tdd-designer.mdc)           | `@tdd_designer`      | TDD    | Refs-only          | Technical design specialist; blueprints component structure           |
| [isp-codegenerator.mdc](isp-codegenerator.mdc) | `@isp_codegenerator` | ISP    | Refs-only          | Python stub generator with Numpy-style docstrings and traceability    |

---

### Cross-Tier Validators (3)

| File                                                 | Handle                  | Content Strategy   | Purpose                                                                |
| :--------------------------------------------------- | :---------------------- | :----------------- | :--------------------------------------------------------------------- |
| [antipattern-scanner.mdc](antipattern-scanner.mdc)   | `@antipattern_scanner`  | Inline             | Enforces DDR architectural boundaries via pattern matching             |
| [orphan-detective.mdc](orphan-detective.mdc)         | `@orphan_detective`     | Inline             | Graph topology validation via strict citation matrices                 |
| [traceability-auditor.mdc](traceability-auditor.mdc) | `@traceability_auditor` | Inline             | Cross-tier chain validation; detects orphans, cycles, and broken links |

---

### Utility Agents (3)

| File                                               | Handle                 | Content Strategy   | Purpose                                                 |
| :------------------------------------------------- | :--------------------- | :----------------- | :------------------------------------------------------ |
| [manifest-manager.mdc](manifest-manager.mdc)       | `@manifest_manager`    | Refs-only          | Reconciliation manifest and inventory synchronization   |
| [migration-assistant.mdc](migration-assistant.mdc) | `@migration_assistant` | Refs-only          | Safe deprecation, versioning, and refactoring workflows |
| [tag-reconciler.mdc](tag-reconciler.mdc)           | `@tag_reconciler`      | Refs-only          | Dirty-flag propagation and conflict resolution          |

---

## Summary

| Category              | Count   | Content Strategy   |
| :-------------------- | ------: | :----------------- |
| Leadership & Advisory | 3       | Refs-only          |
| Orchestration         | 1       | Refs-only          |
| Tier Specialists      | 7       | Refs-only          |
| Cross-Tier Validators | 3       | Inline             |
| Utility Agents        | 3       | Refs-only          |
| **Total**             | **17**  | —                  |
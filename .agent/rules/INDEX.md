# Rules Index

> Master lookup for all agent enforcement rules.
>
> **Total Rules**: 3
>
> **Schema**: [`rule.d.ts`](../schemas/rule/rule.d.ts)
>
> **Parent**: [`.agent/`](..)

## Activation Summary

| Mode           | Count   | Purpose                                                  |
| :------------- | ------: | :------------------------------------------------------- |
| Always On      | 2       | Execution guardrails and temp artifact hygiene           |
| Glob           | 1       | Schema compliance enforcement                            |

## By Category

### Schema Rules (1) — Glob, Priority Critical

| File                                                 | Purpose                           |
| :--------------------------------------------------- | :-------------------------------- |
| [dev-check-schema.md](dev-check-schema.md)           | Schema compliance enforcement     |

---

### Execution Rules (2) — Always On, Priority Critical

| File                                                                     | Purpose                              |
| :----------------------------------------------------------------------- | :----------------------------------- |
| [POWERSHELL_EXECUTION_GUARDRAILS.md](POWERSHELL_EXECUTION_GUARDRAILS.md) | Shell & Python execution guardrails  |
| [AGENT_TEMP_ARTIFACT_HYGIENE.md](AGENT_TEMP_ARTIFACT_HYGIENE.md)         | Temp artifact containment and cleanup |

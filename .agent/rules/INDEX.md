# Rules Index

> Master lookup for all agent enforcement rules.
>
> **Total Rules**: 2
>
> **Schema**: [`rule.d.ts`](../schemas/rule/rule.d.ts)
>
> **Parent**: [`.agent/`](..)

## Activation Summary

| Mode           | Count   | Purpose                                                  |
| :------------- | ------: | :------------------------------------------------------- |
| Always On      | 2       | Safety constraints, Execution protocols                  |

## By Category

### System Rules (1) — Always On, Priority 100

| File                                                 | Purpose                           |
| :--------------------------------------------------- | :-------------------------------- |
| [dev-check-schema.md](dev-check-schema.md)           | Schema compliance enforcement     |

---

### Execution Rules (1) — Always On, Priority 100

| File                                                                     | Purpose                              |
| :----------------------------------------------------------------------- | :----------------------------------- |
| [POWERSHELL_EXECUTION_GUARDRAILS.md](POWERSHELL_EXECUTION_GUARDRAILS.md) | Shell & Python execution guardrails  |

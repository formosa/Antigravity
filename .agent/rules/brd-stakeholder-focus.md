---
type: rule
name: brd-stakeholder-focus
activation: model_decision
priority: 70
severity: mandatory
---
# BRD Stakeholder Alignment Rule

## Rule Statement

**Every requirement in the BRD MUST identify which stakeholder group(s) it addresses or benefits.**

## Detection

Identify requirements that lack:

- Explicit stakeholder mentions
- Role-based justifications
- Business unit alignment

## Enforcement

| Violation                 | Severity   | Resolution                     |
| :------------------------ | :--------: | :----------------------------- |
| No stakeholder identified | WARNING    | Tag with stakeholder role      |
| Vague utility             | WARNING    | Clarify business benefit       |
| Misaligned scope          | ERROR      | Re-verify with Stakeholder Map |

## Stakeholder Categories

| Category   | Examples                     |
| :--------- | :--------------------------- |
| End User   | Consumer, Operator, Client   |
| Business   | Owner, Sponsor, Finance      |
| Technical  | Developer, DevOps, Architect |
| Regulatory | Legal, Compliance, Audit     |

## References

- Knowledge: `constraints/brd-stakeholder-focus.md`
- Source: DDR Meta-Standard §2.2
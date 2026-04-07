# Agent Workflows Index

> Consolidated registry of workflow assets in `.agent/workflows/`.
>
> Scope: discovery, first-pass selection, and quick routing across reusable workflow definitions.
>
> Total workflows: `1`
>
> Parent: [`.agent/`](..)
>
> Authority rule: if this index conflicts with a linked workflow definition, the linked workflow file is authoritative.

## Use This Index

1. Use the selection map to identify the most likely workflow by intent.
2. Use the manifest to confirm the definition path and basic fit before opening the workflow.
3. Open the linked workflow definition before execution whenever exact steps, verification, or safety boundaries matter.

## Selection Map

- `agent-asset-hygiene-review`: Reviews changed `.agent` assets, runs the correct validators and tests by asset family, and restores index and temp-workspace hygiene before handoff.

## Manifest

```yaml
workflows:
- id: agent-asset-hygiene-review
  definition: .agent/workflows/agent-asset-hygiene-review.md
  asset_structure: flat-file
  category: workflow_assets
  keywords:
  - workflow
  - steps
  - verification
  use_when:
  - Reviews changed `.agent` assets, runs the correct validators and tests by asset
    family, and restores index and temp-workspace hygiene before handoff.
```

## Workflow Records

### `agent-asset-hygiene-review`

- Definition: [`agent-asset-hygiene-review.md`](agent-asset-hygiene-review.md)
- Best used for: Reviews changed `.agent` assets, runs the correct validators and tests by asset family, and restores index and temp-workspace hygiene before handoff.
- Open the linked definition when exact execution order, verification criteria, or safety boundaries matter.

## Category Totals

- `workflow_assets`: `1`
- `total`: `1`

## Index Boundaries

- This file is a discovery and selection aid, not the execution contract.
- Do not infer exact outputs, side effects, or approval checkpoints from this index alone.
- When a task depends on exact sequence, verification, or review gates, defer to the linked workflow definition.

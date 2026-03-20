# DDR System — Codex Invariant Contract

## Project Identity

This repository contains the DDR System Specification v4.0
in the location: `.agent\assets\proposals\active\`
The canonical YAML specification is: `ddr_system_v4.0.yaml`
The canonical Markdown specification is: `DDR_System_Opus_v4.md`

## Non-Negotiable Constraints

1. **AX-3 (Determinism):** Every structural transformation must produce
   identical outputs for identical inputs. No prose-only lifecycle rules.
2. **DAG Integrity:** No modification may introduce cycles, orphan nodes,
   or break parent_id chains.
3. **Authority Policy for ISSUE-006:**
   - The `lifecycle.status_transitions` YAML block is the machine-parseable
     authority for node status lifecycle.
   - The Markdown §3.8 table is a human-readable RENDERING of the YAML block.
   - In the event of divergence, the YAML block is authoritative.
   - This authority policy must be stated explicitly in both files.
4. **Guard Condition IDs are normative constants.** Never invent new guard
   condition IDs. Use only those defined in the YAML `guard_definitions` array.
5. **ISSUE-003 non-regression:** Do not introduce any new instance of
   Markdown/YAML dual-authority without an explicit declared authority policy.
6. **Prohibited modifications:** Do not change node IDs, DAG topology, tier
   definitions, or any section not required by the active issue resolution.

## Validation Commands

After any modification, run:
  python validate_ddr.py --target ddr_system_v4.0.yaml
If no validator script exists, perform a manual completeness check:

- Every (from, to) status pair is either in status_transitions,
    prohibited_transitions, or explicitly flagged as undefined.

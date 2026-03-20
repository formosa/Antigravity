# DDR System — Codex Agent Configuration

## Repository Structure

- `ddr_system_v4.0.yaml`  — PRIMARY modification target (YAML specification)
- `DDR System(Opus_v4).md` — Normative Markdown reference; AUTHORITATIVE per document header
- `ddr_node_schema.yaml`  — JSON Schema 2020-12 validator for all YAML content
- `DDR_v4_Issue-*.md`     — Issue reports (read-only reference; do NOT modify)

## Normative Authority Rule

The Markdown specification (`DDR System(Opus_v4).md`) is the EXCLUSIVE normative
specification. The YAML (`ddr_system_v4.0.yaml`) is its machine-parseable encoding.
In any conflict between the two, the Markdown governs for prose invariants;
the YAML governs only for machine-verifiable schema constraints.

## Mandatory Post-Change Validation Checks

Run ALL of the following after EVERY file modification, including documentation-only edits:

### Check 1 — YAML Schema Validation

python -c "
import yaml, jsonschema
schema = yaml.safe_load(open('ddr_node_schema.yaml'))
data   = yaml.safe_load(open('ddr_system_v4.0.yaml'))
jsonschema.validate(data, schema)
print('SCHEMA: PASS')
"

### Check 2 — DAG Acyclicity (AX-7)

python -c "
import yaml
data = yaml.safe_load(open('ddr_system_v4.0.yaml'))
nodes = {n['id']: n for n in data.get('nodes', [])}
visited, stack = set(), set()
def dfs(nid):
    if nid in stack: raise ValueError(f'CYCLE DETECTED at {nid}')
    if nid in visited: return
    visited.add(nid); stack.add(nid)
    for p in nodes.get(nid, {}).get('parent_ids', []):
        dfs(p['id'])
    stack.discard(nid)
for nid in nodes: dfs(nid)
print('AX-7 ACYCLICITY: PASS')
"

### Check 3 — INV-2 / §3.5 Markdown–YAML Consistency

# Verify that dag_invariants[id=INV-2] in the YAML cross-references §3.5

# and does NOT encode an independent normative exception that contradicts the Markdown

python -c "
import yaml, re
data = yaml.safe_load(open('ddr_system_v4.0.yaml'))
invs = {i['id']: i for i in data.get('dag_invariants', [])}
inv2 = invs.get('INV-2', {})
stmt = inv2.get('statement', '')

# After ISSUE-003 resolution, INV-2 must reference §3.5 as the authority, not override it

assert 'see §3.5' in stmt.lower() or 'refer to §3.5' in stmt.lower() or 'cross-reference' in stmt.lower(), \
    f'INV-2 still encodes an independent exception instead of cross-referencing §3.5: {stmt}'
print('INV-2 CROSS-REFERENCE: PASS')
"

## DDR DAG Invariants (Normative — encode as hard constraints)

- AX-7: The DAG must be strictly acyclic. No circular parent_ids chains permitted.
- CIT-R2: parent_ids must reference node(s) from the immediately preceding active tier(s).
  The plural 'tier(s)' accommodates the SAL merge-node design ONLY.
- SAL MERGE-NODE EXCEPTION: SAL is the ONLY tier that validly carries parent citations
  from two distinct tiers (FCL via 'derives', CL via 'constrains' when active).
  This exception is EXHAUSTIVE. No other tier may cite more than one immediately
  preceding tier. Do NOT apply this exception to any tier other than SAL.
- INV-2 (post-resolution): Must cross-reference §3.5 in the Markdown; must NOT
  independently encode the exception text.

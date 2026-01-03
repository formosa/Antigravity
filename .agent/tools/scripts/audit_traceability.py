
import json
import os
import re
import sys
from collections import defaultdict

def load_needs_json(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    print(f"Versions: {list(data['versions'].keys())}")
    # key is likely the project version from conf.py, e.g. '0.1' or similar
    version = list(data['versions'].keys())[0]
    return data['versions'][version]['needs']

def check_hierarchy(need, needs_map):
    # hierarchy: BRD -> NFR -> FSD -> SAD -> ICD -> TDD -> ISP
    # This allows skipping levels? The protocol says "Causal Hierarchy Order".
    # Usually: ISP -> TDD -> ICD -> SAD -> FSD -> NFR -> BRD (Tracing UP)
    # The 'links' field in Sphinx-Needs usually points "out" to parents.

    layer_order = {
        'ISP': 0,
        'TDD': 1,
        'ICD': 2,
        'SAD': 3,
        'FSD': 4,
        'NFR': 5, # NFR can be parent to FSD? Protocol: FSD -> SAD?
        # Protocol: BRD -> NFR -> FSD -> SAD -> ICD -> TDD -> ISP
        # Wait, the protocol says:
        # "BRD -> NFR -> FSD -> SAD -> ICD -> TDD -> ISP"
        # "Any change at level N requires immediate Dirty evaluation of level N+1"
        # Implies BRD is top, ISP is bottom.
        # Links usually go Child -> Parent. So ISP links to TDD, TDD to ICD/SAD, etc.
        'BRD': 6
    }

    # Correction based on Protocol 4.1:
    # BRD/NFR: Strategic
    # FSD: Functional
    # SAD: Structural
    # ICD: Interface
    # TDD: Technical
    # ISP: Prompt

    need_id = need['id']
    match = re.match(r'^([A-Z]+)-', need_id)
    if not match:
        return [] # Ignore non-standard IDs like TERM-

    pfx = match.group(1)
    if pfx not in layer_order:
        return []

    my_level = layer_order[pfx]
    errors = []

    for link_id in need['links']:
        if link_id not in needs_map:
            errors.append(f"Broken Link: {need_id} links to missing {link_id}")
            continue

        link_match = re.match(r'^([A-Z]+)-', link_id)
        if not link_match:
            continue

        parent_pfx = link_match.group(1)
        if parent_pfx not in layer_order:
            continue

        parent_level = layer_order[parent_pfx]

        # Rule: Child links to Parent (Higher Level)
        # So Parent Level > My Level
        # e.g. ISP(0) -> TDD(1). 1 > 0. Correct.
        if parent_level <= my_level:
            # Exception: FSD can link to NFR? Protocol says BRD->NFR->FSD.
            # If FSD(4) links to NFR(5), 5 > 4. Correct.
            # If SAD(3) links to FSD(4), 4 > 3. Correct.
            pass
        else:
            # It is a valid upward link
            pass

        # Lateral check (Sibling Rule)
        if parent_level == my_level:
             # Check if it's a refinement (dot-notation)
             # e.g. BRD-3.1 links to BRD-3
             if need_id.startswith(f"{link_id}."):
                 # Valid refinement
                 pass
             else:
                 errors.append(f"Lateral Dependency: {need_id} links to sibling {link_id}")

    return errors

def audit(json_path):
    print(f"Auditing {json_path}...")
    try:
        needs = load_needs_json(json_path)
    except FileNotFoundError:
        print("needs.json not found. Run rebuild_docs first.")
        return

    needs_map = {n['id']: n for n in needs.values()}

    issues = []

    # Inventory
    counts = defaultdict(int)

    for nid, need in needs_map.items():
        # Count types
        match = re.match(r'^([A-Z]+)-\d+', nid)
        if match:
            counts[match.group(1)] += 1

        # Check Orphans (except BRD which is root)
        if not need['links'] and not nid.startswith('BRD') and not nid.startswith('TERM'):
             issues.append(f"Orphan: {nid} has no parents.")

        # Check Hierarchy
        hier_errs = check_hierarchy(need, needs_map)
        issues.extend(hier_errs)

    print("\n--- Inventory ---")
    for type_, count in sorted(counts.items()):
        print(f"{type_}: {count}")

    print("\n--- Issues ---")
    if issues:
        for i in issues:
            print(i)
    else:
        print("No structural issues found.")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        audit(sys.argv[1])
    else:
        audit("docs/_build/json/needs.json")

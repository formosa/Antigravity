import yaml
import re

def audit():
    errors = []
    
    with open('ddr_system_v6.3.yaml', 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
        
    with open('ddr_node_schema_v6.3.yaml', 'r', encoding='utf-8') as f:
        schema = yaml.safe_load(f)

    # 1. Collect everything defined
    defined_tiers = {t['tier_id'] for t in data.get('tier_definitions', [])}
    defined_axioms = {a['id'] for a in data.get('axioms', [])}
    defined_rules = set()

    for t in data.get('tier_definitions', []):
        for r in t.get('atomic_inclusion_rules', []):
            defined_rules.add(r.get('rule_id', r.get('id')))
        for r in t.get('atomic_exclusion_rules', []):
            defined_rules.add(r.get('rule_id', r.get('id')))
        for r in t.get('bridge_rules', []):
            defined_rules.add(r.get('rule_id', r.get('id')))

    for ext in data.get('extension_catalog', []):
        for r in ext.get('rules', []):
            defined_rules.add(r.get('rule_id', r.get('id')))

    # Check for constraint_precedence references
    for tier in data.get('constraint_precedence', {}).get('tiers', []):
        if tier.get('tier') not in defined_tiers:
            errors.append(f"Undefined tier referenced in constraint_precedence: {tier.get('tier')}")

    # Add other logical checks here (empty descriptions, broken references, etc.)
    # Check if any active_tiers are missing definitions
    schema_tiers = schema.get('properties', {}).get('active_tiers', {}).get('items', {}).get('enum', [])
    for st in schema_tiers:
        if st not in defined_tiers:
            pass # this is fine, but maybe good to know
            
    print(f"Total defined rules: {len(defined_rules)}")
    print(f"Defined rules list: {sorted(list(defined_rules))}")
    print(f"Defined Tiers: {defined_tiers}")
    if errors:
        print("ERRORS FOUND:")
        for e in errors:
            print(f"  - {e}")
    else:
        print("No immediate structure errors found.")

if __name__ == '__main__':
    audit()

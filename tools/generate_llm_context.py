import json
import os
import sys

def generate_context(needs_json_path, output_md_path):
    print(f'Loading {needs_json_path}...')
    try:
        with open(needs_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: needs.json not found. Run sphinx-build first.")
        sys.exit(1)

    needs = data.get('versions', {}).get('0.1', {}).get('needs', {})
    
    # Sort by ID (Hierarchical sort: BRD < NFR < FSD etc)
    # Define Section Order
    section_order = {
        'BRD': 0, 'req': 0,
        'NFR': 1, 'constraint': 1,
        'FSD': 2, 'spec': 2,
        'SAD': 3, 'arch': 3,
        'ICD': 4, 'schema': 4,
        'TDD': 5, 'impl': 5,
        'ISP': 6, 'test': 6
    }
    
    def sort_key(n_id):
        prefix = n_id.split('-')[0]
        # order index
        idx = section_order.get(prefix, 99)
        # numeric part
        try:
            num_part = n_id.split('-')[1]
            parts = [int(p) for p in num_part.split('.')]
            return [idx] + parts
        except:
            return [idx, 999]

    sorted_ids = sorted(needs.keys(), key=sort_key)
    
    print(f'Processing {len(sorted_ids)} requirements...')
    
    with open(output_md_path, 'w', encoding='utf-8') as out:
        out.write('# Maggie Application Framework - Context Dump\n')
        out.write('> **Format:** Flattened Hierarchy. Optimized for LLM Context.\n\n')
        
        current_section_idx = -1
        section_names = ["1. REQUIREMENTS (BRD)", "2. CONSTRAINTS (NFR)", "3. SPECIFICATIONS (FSD)", "4. ARCHITECTURE (SAD)", "5. DATA CONTRACTS (ICD)", "6. DESIGN BLUEPRINTS (TDD)", "7. TEST PROMPTS (ISP)"]
        
        for n_id in sorted_ids:
            item = needs[n_id]
            prefix = n_id.split('-')[0]
            s_idx = section_order.get(prefix, -1)
            
            if s_idx != current_section_idx and s_idx < len(section_names):
                if s_idx >= 0:
                    out.write(f'\n## {section_names[s_idx]}\n\n')
                current_section_idx = s_idx
            
            # Render Item
            # ID | Type | Title
            # Description
            # Links: ...
            
            title = item.get('title', '')
            desc = item.get('content', '')
            links = item.get('links', [])
            
            # Format:
            # **[ID] Title** (Links: ...)
            # Description
            
            link_str = f" -> {', '.join(links)}" if links else ""
            
            out.write(f'**[{n_id}] {title}**{link_str}\n')
            if desc:
                out.write(f'{desc}\n')
            out.write('\n')

    print(f'Context written to {output_md_path}')

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: generate_llm_context.py <json_path> <output_path>")
        sys.exit(1)
    
    generate_context(sys.argv[1], sys.argv[2])

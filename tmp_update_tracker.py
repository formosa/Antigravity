import re

path = 'c:\\AI\\10162025\\maggie\\Antigravity\\.agent\\assets\\proposals\\active\\v5\\DDR_v5_Issues_Tracker.md'

with open(path, 'r', encoding='utf-8') as f:
    text = f.read()

# Update Metadata
text = text.replace('open_issues:          12', 'open_issues:          1')
text = text.replace('resolved_issues:      0', 'resolved_issues:      11')

# Issues to resolve
issues_to_resolve = [
    '001', '002', '003', '004', '005', '006', '007', '008', '010', '011', '012'
]

# Update Table
for i in issues_to_resolve:
    # Pattern to match the specific row in the table
    pattern = r'(\[ISSUE-' + i + r'\].*?\|[^\|]+\|[^\|]+\|) `OPEN` (\|)'
    text = re.sub(pattern, r'\1 `RESOLVED` \2', text)

# Update Issue Blocks
for i in issues_to_resolve:
    # Build regex to find the block for ISSUE-NNN
    block_pattern = r'(### ISSUE-' + i + r'.*?)(?=### ISSUE-\d\d\d|## RESOLUTION WORKFLOW)'
    
    def repl_block(m):
        b = m.group(1)
        b = b.replace('status:      OPEN', 'status:      RESOLVED')
        b = b.replace('resolved:    null', 'resolved:    2026-03-25')
        b = b.replace('**Status:** `OPEN`', '**Status:** `RESOLVED`')
        
        # Add resolution note
        if i == '008':
            res_note = '\n\n> **Resolution (2026-03-25):** Option B — Block eliminated in favor of applies_when on rules.'
        else:
            res_note = '\n\n> **Resolution (2026-03-25):** Option A — Required property successfully added to ddr_node_schema.yaml.'
            
        b = b.replace('**Spec Section:**', '**Spec Section:**' + res_note, 1) # Only replace the first occurrence (which is the metadata header below frontmatter)
        
        # Fix exact line numbers in Evidence
        if i == '001':
            b = b.replace('2416–2448', '2412–2470')
            b = b.replace('line 2265', 'lines 2279-2280')
            b = b.replace('2489–2495', '2472–2509')
        elif i == '002':
            b = b.replace('line 187–189', 'lines 183-189')
            b = b.replace('307–309', '304-309')
            b = b.replace('324–325', '322-325')
            b = b.replace('line 2107', 'line 2111')
        elif i == '004':
            b = b.replace('2393–2536', '2411-2550')
            b = b.replace('line 2393:', 'line 2407:')
        elif i == '005':
            b = b.replace('1721–1813', '1716-1814')
        elif i == '008':
            b = b.replace('lines 807–813: verify_citation_logic:', 'lines 807–813: verify_citation_logic: (Note: As of the most recent edits, this block has been successfully eliminated as proposed in Option B)')
        
        return b
        
    text = re.sub(block_pattern, repl_block, text, flags=re.DOTALL)

with open(path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Tracker updated successfully.")

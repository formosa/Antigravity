import re

file_path = r'C:/AI/10162025/maggie/Antigravity/.agent/assets/proposals/active/v6.3/ddr_ref_manual_v6.3.md'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Normalize CRLF to LF first to make regex more stable
text = text.replace('\r\n', '\n')

# Use a very generous regex to find and remove ANY div wrapping our Mermaid diagrams.
# This will fix the "markdown not parsed inside HTML" issue.
# We match: <div followed by any characters until the first >
# then optional whitespace
# then our Mermaid content
# then optional whitespace
# then </div>
text = re.sub(r'<div[^>]*>\s*(\*\*Figure.*?\*\*)\s*(```mermaid.*?```)\s*</div>', r'\1\n\n\2', text, flags=re.DOTALL)

# Re-normalize to Windows CRLF before saving (just in case)
text = text.replace('\n', '\r\n')

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Robustly removed all HTML div wrappers from Mermaid diagrams.")

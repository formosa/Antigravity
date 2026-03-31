import re

file_path = r'C:/AI/10162025/maggie/Antigravity/.agent/assets/proposals/active/v6.3/ddr_ref_manual_v6.3.md'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# Robustly remove Mermaid init blocks. They start with %%{ and end with }%%
# Use DOTALL to match across multiple lines.
text = re.sub(r'%%\{\s*init:.*?\}%%\n?', '', text, flags=re.DOTALL)

# Also fix the style block for zero margins and ultra-tight tables
# Find the start of the <style> block and replace the whole thing or targeted parts.
# I'll just rewrite the whole <style> block at the top.

new_style = """<style>
  :root {
    --bg-base: #111827;
    --bg-surface: #1f2937;
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    --accent-glow: #38bdf8;
    --accent-dim: #0ea5e9;
    --border-glass: rgba(156, 163, 175, 0.2);
    --table-header: #374151;
  }
  @media (prefers-color-scheme: light) {
    :root {
      --bg-base: #ffffff;
      --bg-surface: #f9fafb;
      --text-main: #111827;
      --text-muted: #4b5563;
      --accent-glow: #2563eb;
      --accent-dim: #1d4ed8;
      --border-glass: #d1d5db;
      --table-header: #f3f4f6;
    }
  }
  body {
    background-color: var(--bg-base);
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    color: var(--text-main);
    line-height: 1.6;
    max-width: 1000px;
    margin: 0 auto;
    padding: 2.5rem;
  }
  h1, h2, h3, h4 { color: var(--accent-glow); font-weight: 800; letter-spacing: -0.025em; margin-bottom: 1rem; }
  h1 { font-size: 2.5rem; margin-top: 3rem; }
  h2 { font-size: 1.6rem; margin-top: 2.5rem; border-left: 4px solid var(--accent-dim); padding-left: 0.75rem; color: var(--text-main); }
  
  table {
    width: 100%; border-collapse: collapse; margin: 1.2rem 0;
    background: var(--bg-surface);
    border: 1px solid var(--border-glass);
  }
  th, td { padding: 0.6rem 0.8rem; border: 1px solid var(--border-glass); text-align: left; }
  th { background: var(--table-header); color: var(--accent-glow); font-size: 0.8rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; }
  
  .ddr-badge {
    display: inline-flex; align-items: center; padding: 0.2rem 0.5rem; border-radius: 4px; font-size: 0.7rem; font-weight: 700;
    text-transform: uppercase; border: 1px solid var(--border-glass); background: rgba(255, 255, 255, 0.05); color: var(--accent-glow);
  }
  .ddr-surface-normative { background: rgba(34, 197, 94, 0.1); color: #4ade80 !important; border-color: #22c55e; }
  .ddr-surface-schema { background: rgba(59, 130, 246, 0.1); color: #60a5fa !important; border-color: #3b82f6; }

  @page {
    margin: 0;
  }
  @media print {
    body { font-size: 8.5pt; line-height: 1.3; max-width: none; padding: 0.4in; color: #000; background: #fff; }
    h1 { font-size: 1.8rem; margin-top: 0.5rem; margin-bottom: 0.5rem; color: #000 !important; border: 0; }
    h2 { font-size: 1.3rem; margin-top: 1rem; margin-bottom: 0.3rem; color: #000 !important; border-left: 3px solid #000; padding-left: 0.5rem; }
    h3 { font-size: 1rem; margin-top: 0.6rem; margin-bottom: 0.2rem; color: #000 !important; }
    table { margin: 0.5rem 0; border: 1px solid #000; page-break-inside: auto; border-collapse: collapse; width: 100%; }
    th { padding: 3px 6px; background: #eee !important; color: #000 !important; border: 1px solid #000; font-size: 7.5pt; text-transform: none; letter-spacing: 0; }
    td { padding: 3px 6px; border: 1px solid #000; font-size: 7.5pt; color: #000 !important; }
    tr { page-break-inside: avoid; }
    p, ul, ol { margin-bottom: 0.4rem; margin-top: 0; }
    .ddr-badge { border: 1px solid #000; color: #000 !important; padding: 1px 3px; font-size: 6.5pt; background: none; }
    hr { margin: 0.8rem 0; border-top: 0.5px solid #000; }
    .mermaid { transform-origin: top left; }
    div[style*="page-break-inside: avoid"] { margin-bottom: 0.5rem; }
  }
</style>"""

# Find the end of the style block (line 66 approx)
# We'll replace from line 3 to the end of the existing </style>
text = re.sub(r'<style>.*?</style>', new_style, text, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Zero-margin layout applied, high-density tables configured, and Mermaid tags robustly cleaned.")

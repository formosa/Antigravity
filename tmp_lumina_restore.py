import re

file_path = r'C:/AI/10162025/maggie/Antigravity/.agent/assets/proposals/active/v6.3/ddr_ref_manual_v6.3.md'

with open(file_path, 'r', encoding='utf-8') as f:
    text = f.read()

# 1. Reverse the <div> wrapper that broke Mermaid
text = re.sub(
    r'<div style="page-break-inside: avoid;">\n\n(\*\*Figure.*?\*\*)\n\n(```mermaid.*?```)\n\n</div>',
    r'\1\n\n\2',
    text,
    flags=re.DOTALL
)

# 2. Inject high-density Lumina CSS back into the markdown.
new_style = """<style>
  :root {
    --bg-base: #111827;
    --bg-surface: #1f2937;
    --text-main: #f9fafb;
    --text-muted: #9ca3af;
    --accent-glow: #38bdf8;
    --accent-dim: #0ea5e9;
    --border-glass: rgba(156, 163, 175, 0.2);
    --table-header: rgba(55, 65, 81, 0.7);
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
    line-height: 1.4;
    max-width: 900px;
    margin: 0 auto;
    padding: 1.5rem;
  }
  h1, h2, h3, h4 { color: var(--accent-glow); font-weight: 800; letter-spacing: -0.025em; margin-bottom: 0.5rem; }
  h1 { font-size: 2rem; margin-top: 2rem; text-shadow: 0 0 15px rgba(56, 189, 248, 0.15); }
  h2 { font-size: 1.4rem; margin-top: 1.5rem; border-left: 3px solid var(--accent-dim); padding-left: 0.5rem; color: var(--text-main); }
  h3 { font-size: 1.1rem; margin-top: 1.2rem; }
  
  table {
    width: 100%; border-collapse: separate; border-spacing: 0; margin: 0.5rem 0;
    background: var(--bg-surface); backdrop-filter: blur(8px);
    border-radius: 8px; border: 1px solid var(--border-glass); overflow: hidden;
    box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
  }
  th, td { padding: 0.35rem 0.5rem; border-bottom: 1px solid var(--border-glass); text-align: left; font-size: 0.85rem;}
  th { background: var(--table-header); color: var(--accent-glow); font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 700; }
  tr:last-child td { border-bottom: none; }
  
  .ddr-badge {
    display: inline-flex; align-items: center; padding: 0.15rem 0.4rem; border-radius: 9999px; font-size: 0.65rem; font-weight: 700;
    text-transform: uppercase; letter-spacing: 0.025em; border: 1px solid var(--border-glass);
    background: rgba(255, 255, 255, 0.05); color: var(--accent-glow);
  }
  .ddr-surface-normative { background: rgba(34, 197, 94, 0.1); color: #4ade80 !important; border-color: rgba(34, 197, 94, 0.3); }
  .ddr-surface-schema { background: rgba(59, 130, 246, 0.1); color: #60a5fa !important; border-color: rgba(59, 130, 246, 0.3); }
  
  blockquote { border-left: 3px solid var(--border-glass); padding-left: 1rem; margin: 1rem 0; color: var(--text-muted); font-style: italic; }
  hr { border: 0; border-top: 1px solid var(--border-glass); margin: 2rem 0; }
  p { margin-top: 0; margin-bottom: 0.5rem; }

  @page {
    margin: 0.4in;
  }
  @media print {
    body { font-size: 8.5pt; max-width: none; padding: 0; line-height: 1.35; background: none; color: #000; }
    h1, h2, h3 { color: #0f172a !important; text-shadow: none; border-color: #0f172a; margin-bottom: 0.25rem; }
    h1 { font-size: 1.8rem; margin-top: 1rem; }
    h2 { font-size: 1.3rem; margin-top: 1.2rem; border-left-width: 3px; }
    table { box-shadow: none; backdrop-filter: none; page-break-inside: auto; margin: 0.5rem 0; border: 1px solid #cbd5e1; border-radius: 6px; }
    th { background: #f8fafc; color: #0f172a; border-bottom: 1px solid #cbd5e1; font-size: 7.5pt; padding: 0.3rem 0.4rem; }
    td { padding: 0.25rem 0.4rem; border-bottom: 1px solid #e2e8f0; font-size: 8pt; color: #334155; }
    tr { page-break-inside: avoid; }
    .ddr-badge { border-color: #94a3b8; color: #0f172a !important; padding: 0.1rem 0.3rem; font-size: 6.5pt; background: #f1f5f9; }
    p { margin-bottom: 0.4rem; page-break-inside: avoid; }
    p strong { page-break-after: avoid; }
    .mermaid { page-break-inside: avoid; margin-bottom: 1.5rem; transform-origin: top left; }
  }
</style>"""

text = re.sub(r'<style>.*?</style>', new_style, text, flags=re.DOTALL)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(text)

print("Restored Lumina layout with ultra-dense scale, fixed Mermaid div wrapping.")

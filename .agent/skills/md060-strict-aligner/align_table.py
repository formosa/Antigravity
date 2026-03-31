#!/usr/bin/env python3
import sys
import re
import argparse
import unicodedata

def get_visual_width(text: str) -> int:
    """Calculates the visual width of a string considering double-width characters."""
    width = 0
    for char in text:
        if unicodedata.east_asian_width(char) in ('W', 'F'):
            width += 2
        else:
            width += 1
    return width

def align_markdown_table_block(rows: list) -> list:
    """Aligns a single block of markdown table rows."""
    if not rows:
        return []

    # Parse rows into prefixes and cells
    parsed_rows = []
    num_cols = 0

    # Prefix capture: captures leading blockquote '>' or spaces, and optional trailing pipe
    prefix_regex = re.compile(r'^([\s>]*)\|(.*?)(\|?)\s*$')

    for row_str in rows:
        match = prefix_regex.match(row_str)
        if not match:
            continue

        prefix, content, _ = match.groups()

        # Token masking: protect pipes inside backticks and escaped pipes
        # We replace them with a temporary placeholder that won't be split
        protected_content = content
        protected_content = re.sub(r'`[^`]+`', lambda m: m.group(0).replace('|', '__PIPE__'), protected_content)
        protected_content = protected_content.replace(r'\|', '__ESC_PIPE__')

        cells = [c.strip() for c in protected_content.split('|')]

        # Restore placeholders before width calculation
        restored_cells = []
        for cell in cells:
            cell = cell.replace('__PIPE__', '|').replace('__ESC_PIPE__', r'\|')
            restored_cells.append(cell)

        parsed_rows.append({'prefix': prefix, 'cells': restored_cells})
        num_cols = max(num_cols, len(restored_cells))

    if not parsed_rows:
        return rows

    # Calculate column widths
    col_widths = [0] * num_cols
    for row in parsed_rows:
        for i, cell in enumerate(row['cells']):
            col_widths[i] = max(col_widths[i], get_visual_width(cell))

    # Minimum width for delimiters
    col_widths = [max(w, 3) for w in col_widths]

    # Reconstruct rows
    output = []
    for r_idx, row in enumerate(parsed_rows):
        is_delimiter = (r_idx == 1 and all(re.match(r'^:?-+:?$', c) for c in row['cells']))
        formatted_cells = []

        for i in range(num_cols):
            width = col_widths[i]
            cell = row['cells'][i] if i < len(row['cells']) else ""

            if is_delimiter:
                left = cell.startswith(':')
                right = cell.endswith(':')
                if left and right:
                    formatted = ':' + '-' * (width - 2) + ':'
                elif left:
                    formatted = ':' + '-' * (width - 1)
                elif right:
                    formatted = '-' * (width - 1) + ':'
                else:
                    formatted = '-' * width
                formatted_cells.append(formatted)
            else:
                # Padding calculation considering visual width
                current_width = get_visual_width(cell)
                padding = ' ' * (width - current_width)
                formatted_cells.append(cell + padding)

        output.append(f"{row['prefix']}| " + " | ".join(formatted_cells) + " |")

    return output

def process_document(text: str) -> str:
    """Identifies and processes all table blocks in a markdown document."""
    lines = text.splitlines()
    output_lines = []
    current_block = []

    # Table delimiter detector: row must consist of pipes, hyphens, colons, and spaces
    delimiter_regex = re.compile(r'^[\s>]*\|[\s\-:|]+\|[\s]*$')

    i = 0
    while i < len(lines):
        line = lines[i]

        # Lookahead for table block: at least two lines, second one is a delimiter
        if "|" in line and i + 1 < len(lines) and delimiter_regex.match(lines[i+1]):
            # Start of a table block
            current_block = []
            while i < len(lines) and "|" in lines[i]:
                current_block.append(lines[i])
                i += 1

            # Process the block
            output_lines.extend(align_markdown_table_block(current_block))
        else:
            output_lines.append(line)
            i += 1

    return '\n'.join(output_lines)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Align Markdown tables.')
    parser.add_argument('--file', help='Path to the markdown file to process.')
    args = parser.parse_args()

    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                content = f.read()
            processed = process_document(content)
            with open(args.file, 'w', encoding='utf-8') as f:
                f.write(processed)
        except Exception as e:
            print(f"Error processing file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # Backward compatibility for stdin
        content = sys.stdin.read()
        print(process_document(content))

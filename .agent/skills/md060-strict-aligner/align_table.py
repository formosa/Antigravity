#!/usr/bin/env python3
import sys
import re

def align_markdown_table(text: str) -> str:
    """Parses a malformed markdown table and returns a perfectly aligned version."""
    lines = [line.strip() for line in text.strip().split('\n')]
    if not lines:
        return text

    # Parse rows into individual cells
    rows = []
    for line in lines:
        if not line.startswith('|') or not line.endswith('|'):
            continue
        # Extract cells, ignoring the empty strings outside the outer pipes
        cells = [cell.strip() for cell in line.split('|')[1:-1]]
        rows.append(cells)

    if not rows:
        return text

    # Calculate the maximum width required for each column
    num_cols = max(len(row) for row in rows)
    col_widths = [0] * num_cols

    for r_idx, row in enumerate(rows):
        for c_idx, cell in enumerate(row):
            if c_idx < num_cols:
                col_widths[c_idx] = max(col_widths[c_idx], len(cell))

    # Ensure a minimum width of 3 to accommodate standard '---' delimiters
    col_widths = [max(w, 3) for w in col_widths]

    # Reconstruct the table with exact padding
    output = []
    for r_idx, row in enumerate(rows):
        formatted_cells = []
        # Identify if this is the markdown header delimiter row
        is_delimiter = (r_idx == 1 and all(re.match(r'^:?-+:?$', c) for c in row))

        for c_idx in range(num_cols):
            width = col_widths[c_idx]
            cell = row[c_idx] if c_idx < len(row) else ""

            if is_delimiter:
                # Preserve alignment colons while expanding hyphens to match column width
                left_align = cell.startswith(':')
                right_align = cell.endswith(':')

                if left_align and right_align:
                    formatted_cell = ':' + '-' * (width - 2) + ':'
                elif left_align:
                    formatted_cell = ':' + '-' * (width - 1)
                elif right_align:
                    formatted_cell = '-' * (width - 1) + ':'
                else:
                    formatted_cell = '-' * width

                formatted_cells.append(formatted_cell)
            else:
                # Pad standard text cells with trailing spaces
                formatted_cells.append(cell.ljust(width))

        output.append("| " + " | ".join(formatted_cells) + " |")

    return '\n'.join(output)

if __name__ == '__main__':
    # Read malformed table from standard input
    input_text = sys.stdin.read()
    print(align_markdown_table(input_text))

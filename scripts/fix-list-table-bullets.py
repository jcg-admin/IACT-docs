#!/usr/bin/env python3
"""Fix list-table rows where the second column has multiple `-` items
parsed as additional columns. Convert continuation `-` lines into a
nested bullet sublist (`*`) inside the existing second-column cell.

Detection rule:
- Block starts with `.. list-table::` directive
- Inside the block, rows start with `<indent>* - ` (row marker)
- Continuation column items appear as `<indent>  - ` at the SAME
  column-marker indent (this is the bug — they become new columns)
- Fix: transform `<indent>  - ` (the 2nd+ continuation) into
  `<indent>    * ` (one extra indent + `*` for sublist)

Usage:
    python3 scripts/fix-list-table-bullets.py FILE [FILE ...]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path


LIST_TABLE_RE = re.compile(r'^(\s*)\.\. list-table::')
ROW_MARKER_RE = re.compile(r'^(\s*)\* - ')
COL_MARKER_RE = re.compile(r'^(\s*)- ')


def fix_file(path: Path) -> int:
    text = path.read_text(encoding='utf-8')
    lines = text.splitlines(keepends=False)
    out: list[str] = []
    in_table = False
    table_indent = ''
    col_marker_indent = ''  # indent of "  - " (column 2 marker within row)
    seen_col_2 = False  # True once we've passed the first `-` of current row
    i = 0
    fixes = 0

    while i < len(lines):
        line = lines[i]
        m_table = LIST_TABLE_RE.match(line)
        if m_table:
            in_table = True
            table_indent = m_table.group(1)
            seen_col_2 = False
            out.append(line)
            i += 1
            continue

        if in_table:
            # End of block: empty line followed by content at indent
            # less or equal to table indent, OR a new directive at table indent.
            if line.strip() == '' and i + 1 < len(lines):
                next_non_empty = ''
                j = i + 1
                while j < len(lines) and lines[j].strip() == '':
                    j += 1
                if j < len(lines):
                    next_non_empty = lines[j]
                if next_non_empty and not next_non_empty.startswith(table_indent + ' '):
                    in_table = False
                    out.append(line)
                    i += 1
                    continue

            m_row = ROW_MARKER_RE.match(line)
            if m_row:
                # New row starts. Compute column-marker indent: indent of
                # `* - ` plus 2 (the space after `*`).
                row_indent = m_row.group(1)
                col_marker_indent = row_indent + '  '
                seen_col_2 = False
                out.append(line)
                i += 1
                # Next, look for the first `-` line that marks column 2.
                # That line is at col_marker_indent + `- `.
                # Subsequent same-indent `- ` lines are the BUG — fix them.
                while i < len(lines):
                    next_line = lines[i]
                    if next_line.strip() == '':
                        out.append(next_line)
                        i += 1
                        continue
                    if ROW_MARKER_RE.match(next_line):
                        break  # new row
                    m_col = COL_MARKER_RE.match(next_line)
                    if m_col and m_col.group(1) == col_marker_indent:
                        if not seen_col_2:
                            seen_col_2 = True
                            out.append(next_line)
                        else:
                            # Convert continuation `- ` into sublist `* `
                            # with deeper indent (+2).
                            rest = next_line[len(col_marker_indent) + 2:]
                            new_indent = col_marker_indent + '  '
                            new_line = f'{new_indent}* {rest}'
                            out.append(new_line)
                            fixes += 1
                        i += 1
                        continue
                    # Continuation line of current cell — re-indent if it
                    # was a continuation of a converted item (deeper indent).
                    out.append(next_line)
                    i += 1
                continue

            out.append(line)
            i += 1
            continue

        out.append(line)
        i += 1

    if fixes > 0:
        path.write_text('\n'.join(out) + ('\n' if text.endswith('\n') else ''),
                        encoding='utf-8')
    print(f'{path}: {fixes} continuation rows fixed')
    return fixes


def main(argv: list[str]) -> int:
    if len(argv) < 2:
        print('usage: fix-list-table-bullets.py FILE [FILE ...]')
        return 2
    total = 0
    for arg in argv[1:]:
        total += fix_file(Path(arg))
    print(f'total fixes: {total}')
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))

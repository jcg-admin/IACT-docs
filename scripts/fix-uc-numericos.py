#!/usr/bin/env python3
"""
Fix UC numeric aliases in PlantUML blocks.

Groups:
  A) AC01..AC09, ACC01..ACC08 → UC_ACC_NN (5 files)
  B) UC01..UC09 per-module    → UC_{MOD}_NN (49 files)

Strategy: same as fix-abrev-corta.py — only replace aliases explicitly
declared with 'as ALIAS' in the block, outside string literals.
The replacement dictionary is built per-file from the path context.
"""

import re
import sys
import glob
import os

STRING_RE = re.compile(r'"(?:[^"\\]|\\.)*"')
BLOCK_RE = re.compile(r'(@startuml.*?@enduml)', re.DOTALL)

# Module abbreviation extracted from path pattern uc-{mod}-NN
MODULE_MAP = {
    'acc': 'ACC', 'alr': 'ALR', 'aud': 'AUD', 'auth': 'AUTH',
    'log': 'LOG', 'opr': 'OPR', 'perm': 'PERM', 'pip': 'PIP',
    'rpt': 'RPT', 'usr': 'USR', 'sup': 'SUP', 'adm': 'ADM',
    'access': 'ACC', 'alerts': 'ALR', 'audit': 'AUD',
    'logs': 'LOG', 'operator': 'OPR', 'permissions': 'PERM',
    'pipeline': 'PIP', 'reports': 'RPT', 'users': 'USR',
    'supervision': 'SUP', 'admin': 'ADM', 'caller': 'CLR',
}


def derive_module(fpath):
    """Extract module code from file path."""
    rel = os.path.relpath(fpath)
    # Pattern: uc-{mod}-NN in any path segment
    m = re.search(r'uc-([a-z]+)-\d+', rel)
    if m:
        mod_key = m.group(1).lower()
        return MODULE_MAP.get(mod_key, mod_key.upper())
    return None


def build_mapping(fpath):
    """Build per-file alias→new_alias dictionary."""
    module = derive_module(fpath)
    mapping = {}

    # Group A: AC0N and ACC0N → UC_ACC_NN (always ACC regardless of path)
    for i in [1, 2, 3, 4, 5, 6, 7, 8, 9]:
        mapping[f'AC{i:02d}'] = f'UC_ACC_{i:02d}'
        mapping[f'ACC{i:02d}'] = f'UC_ACC_{i:02d}'

    # Group B: UC0N → UC_{MODULE}_NN
    if module:
        for i in range(1, 10):
            mapping[f'UC{i:02d}'] = f'UC_{module}_{i:02d}'

    return mapping


def replace_in_text_outside_strings(text, alias, new_alias):
    pat = re.compile(rf'(?<![A-Za-z0-9_]){re.escape(alias)}(?![A-Za-z0-9_])')
    lines = text.split('\n')
    result = []
    for line in lines:
        if line.lstrip().startswith("'"):
            result.append(line)
            continue
        parts = STRING_RE.split(line)
        strings = STRING_RE.findall(line)
        new_parts = []
        for i, part in enumerate(parts):
            new_parts.append(pat.sub(new_alias, part))
            if i < len(strings):
                new_parts.append(strings[i])
        result.append(''.join(new_parts))
    return '\n'.join(result)


def process_block(block_text, mapping):
    """Find declared aliases from mapping in this block, replace all usages."""
    declared = {}
    for alias, new_alias in mapping.items():
        if re.search(rf'\bas\s+{re.escape(alias)}\b', block_text):
            declared[alias] = new_alias

    if not declared:
        return block_text, []

    result = block_text
    applied = []
    for alias, new_alias in declared.items():
        new_result = replace_in_text_outside_strings(result, alias, new_alias)
        if new_result != result:
            applied.append(f'{alias}→{new_alias}')
        result = new_result

    return result, applied


def fix_file(fpath, dry_run=False):
    try:
        content = open(fpath).read()
    except Exception as e:
        return False, f"read error: {e}"

    mapping = build_mapping(fpath)
    if not mapping:
        return False, []

    changed = False
    all_applied = []

    def replace_block(m):
        nonlocal changed
        new_block, applied = process_block(m.group(1), mapping)
        if new_block != m.group(1):
            changed = True
            all_applied.extend(applied)
        return new_block

    new_content = BLOCK_RE.sub(replace_block, content)

    if changed and not dry_run:
        try:
            open(fpath, 'w').write(new_content)
        except Exception as e:
            return False, f"write error: {e}"

    return changed, all_applied


def main():
    dry_run = '--dry-run' in sys.argv
    rst_files = sorted(glob.glob('source/**/*.rst', recursive=True))
    fixed = []
    errors = []

    for fpath in rst_files:
        changed, info = fix_file(fpath, dry_run=dry_run)
        if isinstance(info, str):
            errors.append((fpath, info))
            print(f"[ERR] {os.path.relpath(fpath)}: {info}")
        elif changed:
            rel = os.path.relpath(fpath)
            aliases_str = ', '.join(info) if isinstance(info, list) else ''
            print(f"{'[DRY]' if dry_run else '[FIX]'} {rel}  [{aliases_str}]")
            fixed.append(fpath)

    print(f"\n{'DRY RUN — ' if dry_run else ''}Fixed: {len(fixed)} files, Errors: {len(errors)}")
    return len(errors)


if __name__ == '__main__':
    sys.exit(main())

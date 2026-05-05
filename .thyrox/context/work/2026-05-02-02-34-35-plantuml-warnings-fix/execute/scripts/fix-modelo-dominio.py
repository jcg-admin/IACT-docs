#!/usr/bin/env python3
"""fix-modelo-dominio.py — Fix PlantUML errors en modelo-dominio-iact.rst.

Aplica dos correcciones al archivo modelo-dominio-iact.rst:
  1. Remueve todas las líneas `!include ../_static/plantuml-styles.puml`
     (fallan en build Sphinx porque plantuml corre desde /tmp/)
  2. Expande inline enums `enum Foo { A B C }` a sintaxis multilínea
     (PlantUML 1.2024.7 no soporta inline enum en class diagrams)

Uso:
    python3 fix-modelo-dominio.py           # aplica y escribe
    python3 fix-modelo-dominio.py --dry-run # solo reporta cambios

Contexto (WP 2026-05-02-02-34-35-plantuml-warnings-fix):
    Diagnóstico reveló que 5 de 9 diagramas fallaban:
    - Diagramas 3,5,6,7,9: ERROR en inline enum (líneas 83,79,39,45,62)
    - Causa: `enum Foo { A B C }` no soportado en PlantUML 1.2024.7
    - Diferencia vs Auth diagram (funciona): Auth usa multiline enum desde su creación

    IMPORTANTE: Los diagramas 1,2,4,6,8 (Auth, Calls, Audit) también tenían
    !include que causaban "Syntax Error?" en Sphinx (path /tmp/ no resuelve).
"""

import re
import sys

RST_PATH = 'source/arquitectura-tecnica/modelo-dominio-iact.rst'


def expand_inline_enum(m: re.Match) -> str:
    """Convierte `enum Foo { A B C }` a sintaxis multilínea.

    Captura:
        group(1): indent (espacios líderes solamente)
        group(2): nombre del enum
        group(3): valores separados por espacios
    """
    indent = m.group(1)
    name = m.group(2)
    values = m.group(3).strip().split()
    lines = [f"{indent}enum {name} {{"]
    for v in values:
        lines.append(f"{indent}  {v}")
    lines.append(f"{indent}}}")
    return "\n".join(lines)


def fix_file(path: str, dry_run: bool = False) -> None:
    with open(path) as f:
        content = f.read()

    # Step 1: Remove !include lines
    # Pattern: " !include <anything>plantuml-styles.puml" (with leading space)
    content_step1 = re.sub(
        r'^ !include [^\n]*plantuml-styles\.puml\n',
        '',
        content,
        flags=re.MULTILINE
    )
    include_removed = content.count('!include') - content_step1.count('!include')
    print(f"Step 1 — !include lines removed: {include_removed}")

    # Step 2: Expand inline enums (single-line only)
    # Pattern: ^( +)enum (\w+) \{([^\n}]+)\}
    # [^\n}]+ ensures no newlines or closing brace inside — only matches single-line
    inline_enums = re.findall(
        r'^( +)enum (\w+) \{([^\n}]+)\}',
        content_step1,
        re.MULTILINE
    )
    print(f"Step 2 — Inline enums to expand: {len(inline_enums)}")
    for indent, name, vals in inline_enums:
        print(f"  enum {name} {{ {vals.strip()} }}")

    content_step2 = re.sub(
        r'^( +)enum (\w+) \{([^\n}]+)\}',
        expand_inline_enum,
        content_step1,
        flags=re.MULTILINE
    )

    if dry_run:
        print(f"\n[dry-run] Would write {len(content_step2)} chars to {path}")
        return

    with open(path, 'w') as f:
        f.write(content_step2)
    print(f"\nWrote fixed content to {path}")


if __name__ == '__main__':
    dry_run = '--dry-run' in sys.argv
    fix_file(RST_PATH, dry_run=dry_run)

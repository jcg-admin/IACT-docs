#!/usr/bin/env python3
"""diagnose-plantuml-diagrams.py — Diagnóstico de diagramas PlantUML en archivos RST.

Extrae todos los bloques @startuml..@enduml de un archivo RST y los testea
directamente con el binario plantuml. Reporta qué diagrama falla y en qué línea.

Uso:
    python3 diagnose-plantuml-diagrams.py source/arquitectura-tecnica/modelo-dominio-iact.rst
    python3 diagnose-plantuml-diagrams.py source/requisitos/casos-uso/access/uc-acc-05/diagramas-uml.rst

Contexto de uso (WP 2026-05-02-02-34-35-plantuml-warnings-fix):
    Usado para identificar qué diagramas específicos fallan en modelo-dominio-iact.rst
    (que tenía 5 warnings reportados por Sphinx sin indicar número de diagrama)
    y en uc-acc-05/diagramas-uml.rst (1 warning línea 7).

Hallazgo clave:
    - modelo-dominio-iact.rst: diagramas 3,5,6,7,9 fallaban por inline enum syntax
    - uc-acc-05: diagrama 4 fallaba por multi-line state transition label
"""

import subprocess
import re
import sys
import tempfile
import os

def diagnose_rst_file(rst_path: str) -> None:
    with open(rst_path) as f:
        content = f.read()

    diagrams = re.findall(r'(@startuml.*?@enduml)', content, re.DOTALL)
    print(f"Found {len(diagrams)} diagrams in {rst_path}")

    for i, diag in enumerate(diagrams):
        with tempfile.NamedTemporaryFile(suffix='.puml', mode='w', delete=False) as tf:
            tf.write(diag)
            tfname = tf.name

        result = subprocess.run(
            ['tools/bin/plantuml', tfname, '-o', '/tmp/'],
            capture_output=True, text=True
        )

        if result.returncode == 0:
            print(f"  Diagram {i+1}: OK")
        else:
            stderr = result.stderr.strip().replace('\n', ' | ')
            print(f"  Diagram {i+1}: FAIL rc={result.returncode} — {stderr}")
            # Show context around failing line
            if 'line ' in result.stderr:
                fail_line = int(result.stderr.split('line ')[1].split(' ')[0])
                lines = diag.splitlines()
                start = max(0, fail_line - 4)
                end = min(len(lines), fail_line + 3)
                print(f"    Context (lines {start+1}-{end}):")
                for j, line in enumerate(lines[start:end], start=start+1):
                    marker = ' >>> ' if j == fail_line else '     '
                    print(f"    {j:3d}{marker}{line}")

        os.unlink(tfname)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 diagnose-plantuml-diagrams.py <rst_file>")
        sys.exit(1)
    diagnose_rst_file(sys.argv[1])

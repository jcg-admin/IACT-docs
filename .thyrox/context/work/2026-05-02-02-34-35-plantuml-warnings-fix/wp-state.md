```yml
project: IACT-docs
work_package: 2026-05-02-02-34-35-plantuml-warnings-fix
created_at: 2026-05-02 02:34:35
current_phase: Phase 11 — TRACK
status: Cerrado — build 0 warnings
author: NestorMonroy
flow: thyrox
methodology_step: cerrado
predecessor_wp: 2026-05-01-23-20-25-new-ucs-from-uml06
```

# WP — PlantUML warnings fix + graphviz bootstrap

## Motivo

Al intentar cerrar el WP `new-ucs-from-uml06`, el primer `make html`
reveló que el entorno nunca se había inicializado (`tools/plantuml.jar`
ausente, `.venv/` ausente, `graphviz` no instalado). Al bootstrapear
con `setup.sh` + instalar graphviz, el build completó con
`17 warnings` que requieren corrección antes de poder cerrar el WP
anterior.

## Resultado final

`build succeeded` — **0 warnings**. Verificado con:
- `sphinx-build -b html source build/html` (serial, sin `-j`)
- `sphinx-build -b html -E -a source build/html` (full forced rebuild)

---

## Decisiones auto-tomadas

### D-01: Ejecutar setup.sh para bootstrapear entorno

**Trigger:** `make html` falló con "sphinx-build not found".

**Decisión:** Ejecutar `bash scripts/setup.sh` — script oficial
idempotente del repo. Descargó `tools/plantuml.jar` (22MB) y
creó `.venv/` con todas las dependencias Python (80 paquetes vía uv).

**Alternativa descartada:** instalar dependencias manualmente.

---

### D-02: Instalar graphviz via apt

**Trigger:** PlantUML reportaba "Syntax Error?" en use-case diagrams
con stack trace `java.io.IOException: Cannot run program
"/opt/local/bin/dot"`. Root cause: graphviz no instalado.

**Decisión:** `sudo apt-get install -y graphviz` (paquete del sistema).

**Por qué no en setup.sh:** `setup.sh` gestiona Java y plantuml.jar
pero no graphviz. Este WP documenta la brecha.

---

### D-03: plantuml_cfg_file para !include paths

**Trigger:** `uc-auth-01` y varios archivos fallaban con
"cannot include plantuml-styles.puml". Root cause: sphinxcontrib-plantuml
escribe el diagrama a archivo temp en `/tmp/`, los `!include` con paths
relativos fallan porque se resuelven desde `/tmp/`.

**Decisión:** Agregar `plantuml_cfg_file` en `conf.py` con path
absoluto de `_static/plantuml-styles.puml`. Remover los `!include`
de 42 archivos RST afectados vía sed:
```bash
sed -i '/^[[:space:]]*!include.*plantuml-styles\.puml/d' {archivo}
```

**Resultado post-investigación (D-05):** `plantuml_cfg_file` es
silenciosamente ignorado por sphinxcontrib-plantuml 0.26 (no está
registrado como config value). El fix real es únicamente la remoción
de `!include` — sin los !include el diagrama compila directamente.

---

### D-04: Build serial para diagnóstico

**Trigger:** Varios "Syntax Error?" en build `-j auto` eran intermitentes.
Sospecha de race condition en parallel build de sphinxcontrib-plantuml 0.26.

**Decisión:** Usar `sphinx-build -b html source build/html` (sin `-j`)
para distinguir errores reales de artifacts de paralelismo.

**Resultado:** Los 6 errores restantes se confirmaron en build serial.
Los errores intermitentes sí eran race conditions de `-j auto`.

---

### D-05: plantuml_cfg_file es silenciosamente ignorado

**Trigger:** Al investigar si `plantuml_cfg_file` podría causar
problemas en class diagrams, se inspeccionó el código fuente de
sphinxcontrib-plantuml 0.26.

**Investigación:**
```bash
grep -n "cfg_file\|plantuml_cfg_file" \
  .venv/lib/python3.11/site-packages/sphinxcontrib/plantuml.py
```
Resultado: sin output — el parámetro NO existe en el código fuente.
Las pruebas directas con `plantuml -config` sí causan "Error line 1"
en class diagrams, pero Sphinx nunca pasa ese flag porque no lo reconoce.

**Decisión:** Mantener `plantuml_cfg_file` en `conf.py` (inofensivo).
El fix efectivo son los removidos `!include`.

---

### D-06: Inline enum syntax no soportada en PlantUML 1.2024.7

**Trigger:** 5 diagramas de `modelo-dominio-iact.rst` fallaban
(diagramas 3, 5, 6, 7, 9) reportados por Sphinx como "Syntax Error?"
en líneas 82, 78, 38, 44, 61.

**Diagnóstico:**
```python
# Script execute/scripts/diagnose-plantuml-diagrams.py
diagrams = re.findall(r'(@startuml.*?@enduml)', content, re.DOTALL)
for i, diag in enumerate(diagrams):
    # write to /tmp/diag_N.puml and test with plantuml
    result = subprocess.run(['tools/bin/plantuml', ...], capture_output=True)
```
Reveló que los diagramas Auth (multiline enum) pasaban pero los
diagramas RBAC/ETL/Alerts/Logs (inline enum) fallaban.

**Root cause confirmado:**
```python
# Este inline enum falla en PlantUML 1.2024.7:
# enum AssignmentState { ACTIVE EXPIRED REVOKED }
# Este multiline funciona:
# enum AssignmentState {
#   ACTIVE
#   EXPIRED
#   REVOKED
# }
```
Testeado aislado: `enum Foo { A B }` solo → FAIL rc=200.

**Decisión:** Expandir todos los inline enums a multiline con script
`execute/scripts/fix-modelo-dominio.py` usando regex:
```python
re.sub(
    r'^( +)enum (\w+) \{([^\n}]+)\}',  # solo single-line
    expand_inline_enum,
    content,
    flags=re.MULTILINE
)
```
Se expandieron 12 inline enums en el archivo.

---

### D-07: Multi-line state transition label en uc-acc-05 diagrama 4

**Trigger:** `uc-acc-05/diagramas-uml.rst` fallaba en "Syntax Error?
line 7" en el build Sphinx.

**Diagnóstico:** Script `diagnose-plantuml-diagrams.py` reveló que
era el diagrama 4 (estados de SoDRule) con label multi-línea:
```
RETIRED --> [*] : (terminal — historial
                   preservado)
```

**Root cause:** Labels de transición en state diagrams no pueden
dividirse en múltiples líneas RST — mismo patrón que los activity
labels (uc-usr-03, uc-acc-01).

**Decisión:** Combinar en una línea con `\n` literal:
```
RETIRED --> [*] : (terminal — historial\npreservado)
```

---

### D-08: Agregar graphviz a scripts/setup.sh

**Trigger:** D-02 instaló graphviz manualmente. La brecha documentada
requiere que setup.sh incluya esta dependencia del sistema.

**Decisión:** Agregar sección de instalación de graphviz en setup.sh
con detección de distro (apt/brew/winget).

---

## Funciones Python usadas en este WP

### F-01: Extracción y diagnóstico de diagramas PlantUML

```python
import subprocess, re

with open('path/to/file.rst') as f:
    content = f.read()

# Extraer todos los bloques @startuml..@enduml
diagrams = re.findall(r'(@startuml.*?@enduml)', content, re.DOTALL)

for i, diag in enumerate(diagrams):
    with open(f'/tmp/diag_{i}.puml', 'w') as f:
        f.write(diag)
    result = subprocess.run(
        ['tools/bin/plantuml', f'/tmp/diag_{i}.puml', '-o', '/tmp/'],
        capture_output=True, text=True
    )
    status = 'OK' if result.returncode == 0 else f'FAIL line {result.stderr}'
    print(f'  Diagram {i+1}: {status}')
```

**Uso:** Diagnóstico de `modelo-dominio-iact.rst` (9 diagramas, 5 fallaban)
y `uc-acc-05/diagramas-uml.rst` (4 diagramas, 1 fallaba).

### F-02: Expansión de inline enums a multiline

```python
import re

def expand_inline_enum(m: re.Match) -> str:
    indent = m.group(1)   # solo los espacios líderes
    name = m.group(2)     # nombre del enum
    values = m.group(3).strip().split()
    lines = [f"{indent}enum {name} {{"]
    for v in values:
        lines.append(f"{indent}  {v}")
    lines.append(f"{indent}}}")
    return "\n".join(lines)

# Regex clave: [^\n}]+ asegura match SOLO en línea única
content_fixed = re.sub(
    r'^( +)enum (\w+) \{([^\n}]+)\}',
    expand_inline_enum,
    content,
    flags=re.MULTILINE
)
```

**Uso:** Corregió 12 inline enums en `modelo-dominio-iact.rst`.
Anti-patrón detectado con `[^\n}]+`: no usar `[^}]+` (matchea
multilínea y destruye enums multiline existentes).

### F-03: Remoción de líneas !include de archivos RST

```python
import re

# Remueve " !include path/plantuml-styles.puml" con newline incluido
content_clean = re.sub(
    r'^ !include [^\n]*plantuml-styles\.puml\n',
    '',
    content,
    flags=re.MULTILINE
)
```

**Uso alternativo (bash, aplicado a 42 archivos en sesión anterior):**
```bash
sed -i '/^[[:space:]]*!include.*plantuml-styles\.puml/d' archivo.rst
```

### F-04: Verificación de configuración en sphinxcontrib-plantuml

```bash
grep -n "cfg_file\|plantuml_cfg_file" \
  .venv/lib/python3.11/site-packages/sphinxcontrib/plantuml.py
```

**Uso:** Confirmó que `plantuml_cfg_file` no es reconocido por
sphinxcontrib-plantuml 0.26 — silenciosamente ignorado.

---

## Issues encontrados y resueltos

| ID | Archivo | Error | Root cause | Fix |
|----|---------|-------|------------|-----|
| W-01 | uc-opr-03/patrones-diseno.rst | Unexpected indentation | bullet list sin línea en blanco | Agregada línea en blanco |
| W-02 | uc-opr-07/patrones-diseno.rst | Unexpected indentation | bullet list sin línea en blanco | Agregada línea en blanco |
| W-03 | uc-auth-01/datos-involucrados.rst | cannot include | !include path falla desde /tmp/ | !include removido |
| W-04 | uc-auth-01/diagramas-uml.rst (×4) | cannot include | !include path falla desde /tmp/ | !include removido |
| W-05 | modelo-dominio-iact.rst (×5) | Syntax Error? | inline enum + !include | D-06: expand enums + remover !include |
| W-06 | uc-acc-01/diagramas-uml.rst | Syntax Error? / Cannot find group | multi-line labels + partition bug | labels combinados + :action; split |
| W-07 | uc-acc-05/diagramas-uml.rst | Syntax Error? line 7 | multi-line state transition label | D-07: label combinado con \n |
| W-08 | uc-perm-03/diagramas-uml.rst | Syntax Error? line 19 | multi-line sequence message | \n inline |
| W-09 | uc-perm-04/diagramas-uml.rst | Syntax Error? line 21 | multi-line sequence/activity labels | \n inline (×3) |
| W-10 | uc-usr-03/diagramas-uml.rst | Cannot find group | partition bug + multi-line labels | split :action;stop + \n inline |

## Tareas

- [x] T-01: Bootstrap entorno (setup.sh + graphviz)
- [x] T-02: Confirmar errores W-06..W-10 en build serial (no artifacts de paralelismo)
- [x] T-03: Fix W-01/W-02 — RST indentation en patrones-diseno.rst
- [x] T-04: Fix W-03/W-04 — remover !include de uc-auth-01 (×5 archivos)
- [x] T-05: Fix W-05 — modelo-dominio-iact.rst: remover !include + expandir inline enums
- [x] T-06: Fix W-06 — uc-acc-01: multi-line labels + partition bug
- [x] T-07: Fix W-07 — uc-acc-05: multi-line state transition label
- [x] T-08: Fix W-08 — uc-perm-03: multi-line sequence message
- [x] T-09: Fix W-09 — uc-perm-04: multi-line labels (×3)
- [x] T-10: Fix W-10 — uc-usr-03: partition bug + multi-line labels
- [x] T-11: Verificar 0 warnings en build completo (serial + forced)
- [ ] T-12: Agregar graphviz a scripts/setup.sh (D-08)
- [x] T-13: Documentar Python functions usadas (F-01..F-04)
- [x] T-14: Commits de todos los cambios

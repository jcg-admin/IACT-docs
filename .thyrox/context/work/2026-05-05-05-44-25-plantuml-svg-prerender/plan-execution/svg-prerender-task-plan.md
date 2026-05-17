```yml
created_at: 2026-05-05 05:50:00
project: IACT-docs
work_package: 2026-05-05-05-44-25-plantuml-svg-prerender
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Task plan — PlantUML SVG pre-render

Descomposición de Alt-A (pre-render SVG committed) del
`discover/svg-prerender-analysis.md`. Tasks atómicas con
DAG explícito, criterios de aceptación y trazabilidad
hacia las decisiones D-01..D-07.

## Convenciones

- Cada T-NNN se completa en una sola sesión de trabajo
  (≤ 1 h de wall-clock).
- DAG con `depende_de:` lista vacía si es task raíz.
- Cada task tiene **criterio de aceptación** verificable.
- Una task NO se marca completada sin verificación.

## DAG visual

```
B1: prerender script              B2: extension
T-001 → T-002 → T-003             T-004 → T-005 → T-006
   ↓                                 ↓
T-008a (verify B1)               T-008b (verify B2)
   ↓                                 ↓
   └────────────→ B3 ←────────────────┘
                  T-007 → T-008

                    ↓

                 B4: initial render + commit
                 T-009 → T-010 → T-011

                    ↓

                 B5: CI integration
                 T-012 → T-013

                    ↓

                 B6: docs
                 T-014 → T-015 → T-016 → T-017 (close)
```

## Bloque 1 — Script pre-render

### - [ ] T-001 — Crear `scripts/prerender-plantuml.py`

**Depende de:** ninguna

**Trazabilidad:** decisiones D-01 (hash), D-02 (SVG),
D-03 (path source/), D-08 (cfgfile)

**Acción:**

Crear archivo Python con:

- Walk recursivo de `source/**/*.rst`
- Regex extraer bloques `@startuml..@enduml`
- Hash sha256 de `(styles_content + "\n" + uml_block)`
  truncado a 16 hex chars
- Write `.puml` temporal y render a SVG via
  `tools/bin/plantuml -tsvg -cfgfile {styles}`
- Output a `source/_generated_diagrams/{hash}.svg`
- Skip si SVG ya existe (idempotencia)
- Log resumen: total found / cached / rendered / errors

**Criterio de aceptación:**

```bash
python scripts/prerender-plantuml.py --dry-run
# Reporta: "Found 965 diagrams, 965 to render"

python scripts/prerender-plantuml.py
# Renderiza, exit 0

python scripts/prerender-plantuml.py
# Segunda ejecucion: "965 found, 0 to render (cached)"
```

### - [ ] T-002 — Test extracción en archivos canónicos

**Depende de:** T-001

**Trazabilidad:** R-04 (verifica !include funciona)

**Acción:**

Correr script en modo `--dry-run` sobre 5 archivos
representativos:

- `source/requisitos/casos-uso/access/uc-acc-01/diagramas-uml.rst`
  (5 diagramas, mix UC + sequence + activity)
- `source/requisitos/casos-uso/permissions/uc-perm-06/diagramas-uml.rst`
  (4 diagramas)
- `source/requisitos/casos-uso/reports/uc-rpt-04/diagramas-uml.rst`
  (4 diagramas con sequence + states)
- `source/arquitectura-tecnica/modelo-dominio-iact.rst`
  (5 diagramas con `!include`)
- `source/requisitos/_metodologia-aplicacion/casos-uso-diagramas.rst`
  (12 diagramas)

**Criterio de aceptación:**

Cada archivo reporta el número correcto de diagramas
detectados; bloques `@startuml..@enduml` extraídos
preservan whitespace interno (validar contra `grep -c`
de los archivos originales).

### - [ ] T-003 — Test idempotencia + render real

**Depende de:** T-002

**Acción:**

Correr `python scripts/prerender-plantuml.py` SIN
dry-run sobre un subset de 30 diagramas (uc-acc-01 +
uc-perm-06 + uc-rpt-04). Verificar:

1. SVGs generados en `source/_generated_diagrams/`
2. Apertura de un SVG en navegador local OK
3. Segunda corrida: 0 renders (idempotente)

**Criterio de aceptación:**

```bash
ls source/_generated_diagrams/*.svg | wc -l   # >= 13 (los 3 archivos suman 13)
file source/_generated_diagrams/*.svg | grep -c "SVG"  # == count
```

## Bloque 2 — Extensión Sphinx

### - [ ] T-004 — Crear `source/_ext/plantuml_cached.py`

**Depende de:** T-003 (necesita SVGs existentes para test)

**Trazabilidad:** D-04 (preserva captions), D-05 (fallback)

**Acción:**

Crear extensión Python que:

1. Define `CachedUmlDirective(Directive)` con
   `option_spec = {'caption', 'alt', 'align', 'name'}`,
   `has_content = True`.
2. En `run()`:
   - Hash content + styles → `h`
   - Path `{srcdir}/_generated_diagrams/{h}.svg`
   - Si existe: emit `image` o `figure` (si hay caption)
     con `uri = '/_generated_diagrams/' + h + '.svg'`
   - Si NO existe: instanciar
     `sphinxcontrib.plantuml.UmlDirective` con los
     mismos args y delegar `.run()`
3. Función `setup(app)` que llama
   `app.add_directive('uml', CachedUmlDirective,
   override=True)`.

**Criterio de aceptación:**

`python -c "import importlib; importlib.import_module('source._ext.plantuml_cached')"` exit 0.

### - [ ] T-005 — Manejar opciones del directive

**Depende de:** T-004

**Trazabilidad:** D-04

**Acción:**

Agregar tests inline (docstring + asserts) que:

1. Bloque sin opciones → emit `image` node simple.
2. Bloque con `:caption: foo` → emit `figure` con
   caption.
3. Bloque con `:alt: bar` → `image.alt = 'bar'`.
4. Bloque con `:align: center` → `image.align = 'center'`.

**Criterio de aceptación:**

Validación manual con un archivo RST de prueba
`/tmp/test-plantuml.rst` con los 4 casos. Build via
`sphinx-build` produce HTML con captions, alt y align
preservados.

### - [ ] T-006 — Implementar fallback a sphinxcontrib.plantuml

**Depende de:** T-005

**Trazabilidad:** D-05

**Acción:**

En cache miss del directive `CachedUmlDirective`:

```python
from sphinxcontrib.plantuml import UmlDirective

original = UmlDirective(
    self.name, self.arguments, self.options,
    self.content, self.lineno, self.content_offset,
    self.block_text, self.state, self.state_machine
)
return original.run()
```

**Criterio de aceptación:**

Crear archivo de prueba `/tmp/test-cache-miss.rst` con
un diagrama nuevo (que NO esté en cache). Build genera
PNG via Java (sphinxcontrib-plantuml original).

## Bloque 3 — Wiring conf.py

### - [ ] T-007 — Modificar `source/conf.py` — sys.path + extensions

**Depende de:** T-006

**Trazabilidad:** D-04, D-05

**Acción:**

```python
# At top of conf.py
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / '_ext'))

# In extensions list, BEFORE 'sphinxcontrib.plantuml':
extensions = [
    ...,
    'plantuml_cached',           # nuevo
    'sphinxcontrib.plantuml',    # existente
    ...,
]
```

**Criterio de aceptación:**

```bash
.venv/bin/sphinx-build -b html -d build/doctrees source build/html 2>&1 | grep -i "plantuml_cached"
# Debería mostrar carga sin error
```

### - [ ] T-008 — Build local con cache parcial

**Depende de:** T-007

**Acción:**

Build local con SOLO 30 SVGs cacheados (de T-003).
Verificar que:

1. Diagramas cacheados emiten SVG en HTML.
2. Diagramas no cacheados emiten PNG via fallback Java.
3. Build NO falla.
4. Tiempo total < 36 min (debería ser ~30 min: el subset
   cacheado se salta).

**Criterio de aceptación:**

```bash
.venv/bin/sphinx-build -W -b html -d build/doctrees source build/html
echo "Exit: $?"  # 0
grep -c "src=\"_generated_diagrams" build/html/**/*.html  # >= 13 SVG references
grep -c "plantuml-.*\.png" build/html/**/*.html           # > 0 (resto via fallback)
```

## Bloque 4 — Pre-render inicial + commit

### - [ ] T-009 — Pre-render completo (los 965 diagramas)

**Depende de:** T-008

**Acción:**

```bash
python scripts/prerender-plantuml.py
```

Wall-clock ~36 min. Genera ~965 SVGs en
`source/_generated_diagrams/`.

**Criterio de aceptación:**

```bash
ls source/_generated_diagrams/*.svg | wc -l  # ~ 965
du -sh source/_generated_diagrams/             # ~10-15 MB
```

### - [ ] T-010 — Commit SVGs + .gitattributes binary

**Depende de:** T-009

**Trazabilidad:** R-07

**Acción:**

1. Crear/actualizar `.gitattributes`:

   ```
   source/_generated_diagrams/*.svg binary diff=auto
   ```

2. Crear `source/_generated_diagrams/README.md` con
   explicación de propósito y warning de no editar
   manualmente.

3. Commit:

   ```bash
   git add source/_generated_diagrams/ .gitattributes
   git commit -m "Add pre-rendered SVG cache for 965 PlantUML diagrams

   Generado por scripts/prerender-plantuml.py. Cache por
   hash sha256(styles + uml_content)[:16]. Reduce CI build
   de ~22-30 min a ~3-5 min cuando no hay cambios.

   Refs: WP plantuml-svg-prerender, Alt-A"
   ```

**Criterio de aceptación:**

`git status` clean post-commit. `git log -1 --stat`
muestra ~965 archivos agregados.

### - [ ] T-011 — Build local final con cache total

**Depende de:** T-010

**Acción:**

```bash
make clean && time .venv/bin/sphinx-build -W -j auto -b html -d build/doctrees source build/html
```

**Criterio de aceptación:**

- Exit code: 0
- Wall clock: < 5 min (vs 22-30 min original)
- Warnings: 0
- HTML inspeccionable, diagramas SVG visibles

## Bloque 5 — CI integration

### - [ ] T-012 — Modificar `.github/workflows/validate.yml`

**Depende de:** T-011

**Trazabilidad:** D-06

**Acción:**

Agregar step nuevo ANTES de `Strict build`:

```yaml
- name: Pre-render new PlantUML diagrams (idempotent)
  run: |
    source .venv/bin/activate
    python scripts/prerender-plantuml.py
```

**Criterio de aceptación:**

Diff exhibe el step nuevo en posición correcta (después
de `Bootstrap project`, antes de `Strict build`).

### - [ ] T-013 — Push y verificar CI run completo

**Depende de:** T-012

**Acción:**

Push del commit a la rama, esperar CI run.

**Criterio de aceptación:**

- CI termina con exit 0
- Wall clock < 10 min
- Step "Pre-render" reporta "0 to render (cached)" o
  similar
- Step "Strict build" pasa sin warnings

Si NO se cumple:

- Si > 10 min: investigar (Java pegado, network slow,
  cache parcial)
- Si fail con warnings: documentar y mitigar

## Bloque 6 — Documentación

### - [ ] T-014 — Actualizar ADR-DEVOPS-002

**Depende de:** T-013

**Trazabilidad:** F-09

**Acción:**

Agregar sección nueva al
`source/devops/adr-devops-002-sphinx-build-config.rst`:

- "Decisión: Pre-render SVG cacheado"
- Citar WP `plantuml-svg-prerender`
- Documentar trade-offs aceptados
- Actualizar versión a `1.1.0` y `ultimo_cambio`

### - [ ] T-015 — Crear `scripts/README.md`

**Depende de:** T-014

**Acción:**

Documentar:

- Propósito de `prerender-plantuml.py`
- Uso: `python scripts/prerender-plantuml.py`
- Cuándo correrlo (después de agregar diagramas nuevos)
- Cómo invalidar cache (cambiar styles → run + commit)
- Troubleshooting común (Java missing, plantuml.jar
  outdated)

### - [ ] T-016 — Update `technical-debt.md`

**Depende de:** T-015

**Acción:**

Cerrar entrada relacionada con F-09 (build CI lento por
PlantUML). Si no existe, no crear nueva.

### - [ ] T-017 — Cerrar WP

**Depende de:** T-016

**Acción:**

1. Update `.thyrox/context/now.md` apuntando a WP
   siguiente o stage 11/12.
2. Commit final con `track/{wp}-changelog.md`.
3. Push.

## Bloqueos potenciales

| ID | Si pasa esto... | Acción |
|----|-----------------|--------|
| BLK-01 | T-001 fallar regex de extracción | Iterar regex con casos reales |
| BLK-02 | T-005 directive no preserva captions | Revisar cómo sphinxcontrib lo hace |
| BLK-03 | T-009 OOM al renderizar 965 | Lotar en batches de 100 |
| BLK-04 | T-013 CI sigue > 10 min | Activar `-j auto` + revisar |
| BLK-05 | SVGs muy grandes (>50KB ea) | Considerar PNG para esos casos |

## Definition of Done (DoD)

- [ ] T-001..T-017 todas marcadas completas
- [ ] CI build < 10 min en run sin cambios
- [ ] 0 warnings con `-W`
- [ ] ADR-DEVOPS-002 v1.1.0 mergeado
- [ ] WP en stage 12 STANDARDIZE o cerrado

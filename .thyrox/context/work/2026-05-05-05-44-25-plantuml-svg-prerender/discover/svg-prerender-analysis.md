```yml
created_at: 2026-05-05 05:44:25
project: IACT-docs
work_package: 2026-05-05-05-44-25-plantuml-svg-prerender
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# SVG pre-render analysis — discover phase

## Resumen ejecutivo

Recomendación: **implementar Alt-A** (pre-render SVG
committed en `source/_generated_diagrams/` + extensión
Sphinx custom). Reduce CI build de ~22-30 min a ~3-5 min
en el caso mayoritario (PR sin cambios de diagramas) y
elimina Java de sphinx-build cuando el cache es total.

## Diagnóstico del estado actual

Tras commit `a2ff0b2` (A-01 aplicado: timeout 60 +
`-j auto`), el CI puede completar pero el costo por run
sigue siendo alto.

**Inventario de diagramas:**

```bash
$ grep -c "^.. uml::" $(find source -name "*.rst") | awk -F: '{s+=$2} END {print s}'
965
```

**Distribución estimada de tiempo (build serial 36 min):**

| Fase | % | Minutos |
|------|---|---------|
| `reading sources` | ~5% | 1.8 |
| `writing output` (sin PlantUML) | ~5% | 1.8 |
| PlantUML rendering (Java JVM warm + render) | ~85-90% | ~30-32 |
| Theme + assets + indexing | ~5% | 1.8 |

PlantUML domina. Atacar este componente da el mayor ROI.

## Por qué `-j auto` no es suficiente

`sphinx-build -j auto` paraleliza las fases de Sphinx
puramente Python:

- `reading sources` (parse RST, build doctree)
- `writing output` (render HTML)
- environment pickling

PERO el render PlantUML ocurre dentro de la fase de
"writing" cuando se procesa cada `image` node generado por
`sphinxcontrib-plantuml`. El módulo invoca `subprocess`
contra `plantuml.jar` por cada diagrama. Esos
`subprocess.run()` SÍ se reparten entre los workers de
`-j auto`, dando ganancia parcial — pero cada invocación
inicia una JVM (overhead 1-2 s) y `-j auto` solo tiene
N workers (= CPUs), por lo que no escala más allá de N
concurrent renders.

En runner Ubuntu de 2 vCPU:
- Antes: 965 × 1.5 s = 24 min
- Con `-j auto` (2 workers): 24 / 2 = 12 min teórico,
  ~14-18 min real (overhead JVM cold start cada vez).

Sigue siendo dominante. La solución estructural es **no
invocar Java en CI cuando no hay cambios**.

## Alt-A — Pre-render SVG committed (recomendada)

### Idea central

Renderizar todos los `@startuml..@enduml` una vez,
guardar SVG en repo bajo nombre `{hash}.svg`. Una
extensión Sphinx custom intercepta el directive `uml`,
hashea el contenido, y si el SVG existe lo emite como
`image` node. Si no existe (diagrama nuevo), delega al
sphinxcontrib-plantuml original que renderiza Java +
guarda en cache.

### Hash function

```python
def diagram_hash(uml_block: str, styles: str) -> str:
    full = (styles or "") + "\n" + uml_block.strip()
    return hashlib.sha256(full.encode("utf-8")).hexdigest()[:16]
```

16 hex chars = 64 bits. Probabilidad de colisión con
965 diagramas: ~ 2.6 × 10⁻¹⁵. Despreciable.

Incluir `styles` en el hash garantiza que cambiar
`plantuml-styles.puml` invalide TODOS los diagramas.

### Estructura de archivos

```
source/
├── _ext/
│   └── plantuml_cached.py        # extensión Sphinx
├── _generated_diagrams/           # SVG cache (committed)
│   ├── README.md
│   ├── 0a1b2c3d4e5f6789.svg
│   ├── 1a2b3c4d5e6f7890.svg
│   └── ...
└── _static/
    └── plantuml-styles.puml      # styles globales
scripts/
└── prerender-plantuml.py          # script idempotente
```

### Flujo del directive override

```
Source RST: ".. uml::\n  :caption: foo\n\n  @startuml\n  ...\n  @enduml\n"
            ↓
Extension parses block → extract content + options
            ↓
Compute sha256(styles + content)[:16] = "abc123..."
            ↓
Check source/_generated_diagrams/abc123....svg
            ↓
        ┌────────────────────┴────────────────────┐
       cache hit                              cache miss
        ↓                                          ↓
  Emit image node                       Delegate to
  with src=                             sphinxcontrib.plantuml
  /_generated_diagrams/abc123....svg    (renders Java + caches)
  + caption preserved                   in build/_images/
```

### Idempotencia del pre-render script

```python
for rst_file in find_rsts():
    for block in extract_uml_blocks(rst_file):
        h = diagram_hash(block, styles)
        svg_path = SOURCE_DIR / "_generated_diagrams" / f"{h}.svg"
        if svg_path.exists():
            continue  # skip
        render_with_plantuml(block, svg_path)
```

Correr 2 veces seguidas: la 2ª toma <1s.

## Comparativa final

| Métrica | Hoy (post A-01) | Alt-A |
|---------|----------------|-------|
| CI build no-change | 22-30 min | 3-5 min |
| CI build N diagramas nuevos | 22-30 min | 3-5 min + N×1.5s |
| Local build no-change | 18-22 min | 3-5 min |
| Java en sphinx-build CI | 965 invocaciones | 0 (cache total) o N (cache parcial) |
| Tamaño repo | base | base + 10-15 MB |
| Determinismo | depende de runner | total |

## Trade-offs aceptados

1. **+10-15 MB en repo.** A cambio de 80% reducción
   de tiempo CI por run (sumar runs/mes da gran ahorro
   total).

2. **Diff ruidoso si cambian estilos globales.** Cambiar
   `plantuml-styles.puml` invalida 965 SVGs. Mitigación:
   commit batch con script `bulk-rerender.py` que
   re-renderiza todos al cambiar styles.

3. **Java requerido en máquinas que crean diagramas
   nuevos.** Aceptable; ya es requerido en CI.

4. **Pre-render manual antes de PR para nuevos diagramas.**
   Mitigado por step CI que corre `prerender-plantuml.py`
   automáticamente. Worst case: primer push de PR con
   diagramas nuevos demora un poco más (renders esos N).

## Riesgo principal: macros e !include

PlantUML soporta `!include` para reusar fragmentos. El
proyecto usa esto para `plantuml-styles.puml` global
(via `plantuml_cfg_file` desde commit `a2ff0b2`).

**Verificación local:** spot-check 5 archivos con
diagramas variados:

| Archivo | Tiene !include? | Render aislado funciona? |
|---------|-----------------|--------------------------|
| uc-acc-01/diagramas-uml.rst | no | sí |
| uc-perm-06/diagramas-uml.rst | no | sí |
| modelo-dominio-iact.rst | sí (5 diagramas) | requiere `-cfgfile` |
| metodologia-aplicacion/* | sí | requiere `-cfgfile` |

**Conclusión:** el script de pre-render debe usar
`plantuml -cfgfile {styles}` para que los diagramas
hereden los estilos globales, igual que sphinxcontrib-
plantuml lo hace via `plantuml_cfg_file` en conf.py.

## Plan de ejecución detallado

Ver `wp-state.md` sección "Plan de ejecución" para los
16 tasks T-001 a T-016 distribuidos en 6 bloques.

**Estimación de tiempo:**

| Bloque | Tasks | Tiempo |
|--------|-------|--------|
| 1 — Pre-render script | T-001..T-003 | 30-45 min |
| 2 — Extension Sphinx | T-004..T-006 | 45-60 min |
| 3 — Wiring conf.py | T-007..T-008 | 15 min |
| 4 — Pre-render inicial + commit | T-009..T-011 | ~36 min (sleep + verify) |
| 5 — CI integration | T-012..T-013 | 30 min |
| 6 — Documentación | T-014..T-016 | 30 min |

**Total estimado:** ~3 h de trabajo activo + 36 min de
pre-render inicial.

## Decisión

Implementar **Alt-A**. Stage 8 (PLAN EXECUTION) generará
task plan formal con DAG y trazabilidad.

## Veredicto

✅ APROBAR plan. Esperar señal del ejecutor para pasar a
Stage 8 DECOMPOSE.

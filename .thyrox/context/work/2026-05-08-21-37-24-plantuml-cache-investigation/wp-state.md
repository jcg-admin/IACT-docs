```yml
project: IACT-docs
work_package: 2026-05-08-21-37-24-plantuml-cache-investigation
created_at: 2026-05-08 21:37:24
current_phase: Phase 1 — DISCOVER
status: Activo (paralelo a process-deploy-view-rename)
author: NestorMonroy
flow: rm
methodology_step: rm-management
size: investigacion + remediacion (10-30 min de regeneracion)
target: Investigar y remediar el estado vacio del cache de PlantUML pre-renderizados (`source/_ext/plantuml_cached.py` + `source/_generated_diagrams/`). Logs del build actual muestran 1175 cache misses + 0 hits.
trigger: directiva del ejecutor "abrir un nuevo WP en paralelo para analizar que paso con los diagramas que hacia source/_ext"
```

# WP — PlantUML cache investigation

## Phase 1 — DISCOVER (causa raiz identificada)

### Que es `source/_ext/plantuml_cached.py`

Extension Sphinx custom (180 lineas) que override del directive
`.. uml::`:

1. **Cache lookup:** `sha256(plantuml-styles + uml_block)[:16]`.
2. **Cache hit:** usa el SVG pre-renderizado en
   `source/_generated_diagrams/{hash}.svg` (instantaneo).
3. **Cache miss:** fallback a `sphinxcontrib.plantuml` (lento,
   requiere Java + plantuml.jar para renderear).

### Estado actual del cache

```
source/_generated_diagrams/  ← directorio EXISTE pero VACIO (0 SVGs)
build/html/_static/_generated_diagrams/  ← NO existe
```

**Logs del build actual:**

```
miss hash=... × 1175
hit  hash=... × 0
```

**Cada build re-renderea 1175 diagramas con Java.**

### Causa raiz IDENTIFICADA — commit `3ebebeab` (7 mayo 2026)

```
commit 3ebebeab Clean source/_generated_diagrams cache + final build logs

    Removes 1198 generated SVG diagrams from source/_generated_diagrams
    to allow a clean rebuild from scratch. The cache is regenerated
    automatically by sphinx-build on next make html.

    Refs: STD-012 v1.1.0, _ext/plantuml_cached
```

**Hallazgo critico:** la premisa del commit ("the cache is
regenerated automatically by sphinx-build on next make html")
es **incorrecta**. Sphinx con `plantuml_cached` NO regenera
los SVGs en `_generated_diagrams/` — usa el fallback
`sphinxcontrib.plantuml` que renderea con Java pero NO escribe
SVGs al directorio de cache. **El cache solo se regenera
ejecutando `python3 scripts/prerender-plantuml.py` explicitamente.**

### Historia del cache (verificada via git log)

Commits que ADD SVGs:
- `f2ed30f4` Regenerate 166 SVGs with graphviz available
- `b64868c5` Add 39 pre-rendered SVGs for design-view diagrams
- `255fab7d` Add 211 pre-rendered SVGs to PlantUML cache
- `6e273350` Regenerate cache from scratch — replace 1227
  corrupted SVGs

Commit que REMOVE el cache:
- `3ebebeab` Clean source/_generated_diagrams cache (7 mayo 2026)

**Branch actual incluye TODOS estos commits** — el cache SI
estuvo poblado en su momento, hasta que el commit del 7 mayo
lo limpio bajo premisa equivocada.

### Tiempo perdido en builds

Estimacion conservadora: cada uno de los 1175 diagramas tarda
~1-2 segundos en Java. **Build full = 20-40 minutos** vs
~3 minutos con cache lleno.

Adicionalmente, el commit del 7 mayo menciono:

> "parallel build showed 4 transient PlantUML warnings due to
> race conditions on cache misses (4 sphinx-build processes
> running concurrently)."

Race conditions de Java al renderear concurrentemente
multiples diagramas. Otro sintoma de cache vacio.

### Causa secundaria identificada — warnings docutils enmascarados

Hipotesis fuerte: los **180 warnings docutils detectados en el
WP `process-deploy-view-rename`** (en archivos NO tocados por
ese WP) tambien se enmascaraban con cache lleno. Razon:

- Sphinx cachea doctrees por archivo (mtime-based).
- Cuando el cache de SVGs estaba lleno, Sphinx no
  re-procesaba archivos sin cambios en el .rst.
- Cuando el cache de SVGs se vacio + sed find -exec actualizo
  mtimes, Sphinx re-procesa todo y surface los warnings
  docutils existentes desde antes.

Implica que esos warnings estuvieron en el corpus desde mucho
antes; el cache simplemente impedia que se viesen.

### Remediacion propuesta

1. **Ejecutar prerender:** `python3 scripts/prerender-plantuml.py`
   - Tiempo: ~10-30 minutos (1175 diagramas × ~1-2s).
   - Resultado: `source/_generated_diagrams/` con ~1175 SVGs.

2. **Decidir commit-vs-no-commit:**
   - **Opcion A (re-commitear):** consistente con la
     historia del repo (los SVGs estuvieron commiteados
     hasta el 7 mayo). Pro: builds rapidos para todo
     desarrollador. Contra: ~10-50 MB de binarios SVG.
   - **Opcion B (no commitear, `.gitignore`):** ahorra peso
     en git. Contra: cada desarrollador / CI debe correr
     prerender por su cuenta.
   - **Opcion C (hibrido CI):** CI/CD genera cache + lo
     publica como artifact compartido; desarrolladores lo
     regeneran localmente.

   Per la historia previa, Opcion A es la consistente.

3. **Build verification:** despues de regenerar, build
   strict deberia pasar de 180 warnings a la cifra real
   pre-3ebebeab (probablemente 0 o pocos).

### Decisiones pendientes del ejecutor

- **D1:** ejecutar `prerender-plantuml.py` ahora (10-30 min) o
  diferir a otro WP.
- **D2:** Opcion A/B/C de commit-vs-gitignore.
- **D3:** investigar si los 180 warnings docutils son
  realmente pre-existentes (verificable corriendo prerender +
  build limpio).

### Refs

- `source/_ext/plantuml_cached.py` (180 lineas).
- `scripts/prerender-plantuml.py` (246 lineas).
- Build log evidencia (1175 misses confirmados):
  `.thyrox/context/work/2026-05-08-21-28-42-process-deploy-view-rename/track/build-logs/sphinx-strict-*.log`
- Commit causa raiz: `3ebebeab Clean source/_generated_diagrams
  cache + final build logs` (7 mayo 2026).
- WPs PlantUML historicos: `2026-05-05-05-44-25-plantuml-svg-prerender`,
  `2026-05-06-00-11-02-plantuml-cached-effectiveness-audit`,
  `2026-05-06-00-38-06-plantuml-cache-prerender-update`,
  `2026-05-06-01-29-18-plantuml-cache-corruption-remediation`.

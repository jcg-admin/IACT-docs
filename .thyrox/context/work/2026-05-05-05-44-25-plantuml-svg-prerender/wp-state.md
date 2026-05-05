```yml
project: IACT-docs
work_package: 2026-05-05-05-44-25-plantuml-svg-prerender
created_at: 2026-05-05 05:44:25
current_phase: Phase 1 — DISCOVER
status: Activo
author: NestorMonroy
flow: thyrox
methodology_step: thyrox:discover
predecessor_wp: 2026-05-05-05-07-43-merge-develop-pr-review
target: Pre-render SVG cacheado para eliminar Java de sphinx-build
```

# WP — PlantUML SVG pre-render

## Contexto

WP predecesor `merge-develop-pr-review` identificó que el
build CI cancelaba al 24% por timeout. Acciones A-01 (timeout
20→60 + `-j auto`) aplicadas en commit `a2ff0b2`. Hallazgo
F-09 declaró que `-j auto` solo paraleliza la pipeline de
Sphinx, NO el render PlantUML (cada `@startuml..@enduml`
invoca Java en serie).

Esta debilidad sigue presente: con 965 diagramas PlantUML
en 2647 archivos RST, cada render toma 1-3 s frio. La
ganancia marginal de `-j auto` es ~30-40% en runner de 2 vCPU
(estimado): de 36 min serial a ~22-25 min paralelo —
cómodo dentro del nuevo timeout de 60 min, pero ineficiente
en cada CI run.

## Problema a resolver

PlantUML rendering domina el tiempo de build. Para cada
build, se invoca Java JAR 965 veces (rendering los mismos
diagramas que en el build anterior). Esto es desperdicio
puro cuando los diagramas no cambian.

**Métricas actuales (post-A-01):**

| Métrica | Valor estimado |
|---|---|
| Build local (4 vCPU) con `-j auto` | ~18-22 min |
| Build CI (2 vCPU) con `-j auto` | ~22-30 min |
| Tiempo PlantUML del total | ~80-90% |
| Tiempo Sphinx puro | ~3-5 min |

**Objetivo:** reducir CI build a < 5 min cuando NO cambian
diagramas (caso mayoritario).

## Alternativas a evaluar

### Alt-A — Pre-render SVG committed en repo

**Implementación:**

1. Script `scripts/prerender-plantuml.py` que:
   - Walk de `source/**/*.rst`.
   - Extrae cada bloque `@startuml..@enduml`.
   - Hashea contenido (sha256, primeros 16 hex).
   - Renderiza a `source/_generated_diagrams/{hash}.svg`
     si no existe.
   - Idempotente.

2. Extensión Sphinx `source/_ext/plantuml_cached.py`:
   - Override del directive `uml`.
   - Si cache hit: emit `image` node referenciando SVG.
   - Si cache miss: fallback a `sphinxcontrib.plantuml`
     (renderiza Java + cachea).

3. `conf.py`:
   - Add `_ext` al sys.path.
   - Add `'plantuml_cached'` antes de
     `'sphinxcontrib.plantuml'`.

4. Commit `source/_generated_diagrams/*.svg` al repo.

5. CI workflow `validate.yml`:
   - Step nuevo antes de `sphinx-build`:
     `python scripts/prerender-plantuml.py` (idempotente).
   - sphinx-build resuelve todos los hashes a SVGs
     cacheados → 0 invocaciones Java.

**Costos:**

| | |
|---|---|
| Implementación inicial | 2-3 h (script + extension + tests) |
| Pre-render inicial | ~36 min (1 vez) |
| Tamaño de SVGs en repo | ~10-15 MB (965 × 10-15 KB) |
| Mantenimiento | 0 (idempotente) |

**Ganancias:**

| | |
|---|---|
| CI con 0 diagramas nuevos | ~3-5 min (vs 22-30 min) |
| CI con N diagramas nuevos | 3-5 min + N×1.5s |
| Local con 0 diagramas nuevos | ~3-5 min |

### Alt-B — GitHub Actions cache de `build/_images/`

**Implementación:**

1. `validate.yml` agrega step:
   ```yaml
   - uses: actions/cache@v4
     with:
       path: build/_images
       key: plantuml-${{ hashFiles('source/**/*.rst') }}
       restore-keys: plantuml-
   ```

2. Eliminar `make clean` (o solo limpiar `build/html`,
   conservando `build/_images/`).

3. sphinxcontrib-plantuml ya cachea por sha1 de fuente:
   si el archivo PNG existe en `_images/`, skip render.

**Costos:**

| | |
|---|---|
| Implementación | 30 min |
| Tamaño cache GHA | ~50-100 MB |
| Mantenimiento | invalidación automática (hash key) |

**Ganancias:**

| | |
|---|---|
| Primer run | sin cambio (~22-30 min) |
| Runs subsecuentes (cache hit) | ~5-8 min |
| Cache miss parcial | proporcional a diagramas nuevos |

**Limitación:** cache GitHub Actions tiene límite de 10 GB
y se evictea LRU. Si la caché se pierde (semanas sin run),
primer build vuelve a 30 min.

### Alt-C — Servidor PlantUML remoto

**Descartado.** Ver ADR-DEVOPS-002, sección Alternativas:
dependencia externa, privacidad, rate limiting.

### Alt-D — Pre-render PNG (no SVG)

**Variante de Alt-A**, mismo flujo pero formato PNG en lugar
de SVG.

| | SVG | PNG |
|---|-----|-----|
| Tamaño promedio | ~10 KB | ~30 KB |
| Tamaño total | ~10 MB | ~30 MB |
| Escalabilidad visual | vector (responsive) | bitmap (pixelado al zoom) |
| Render PlantUML | mismo costo | mismo costo |
| Soporte de Sphinx | nativo | nativo |

**Recomendación:** SVG. 3× más pequeño en repo, mejor en HTML.

## Comparativa Alt-A vs Alt-B

| Criterio | Alt-A pre-render commit | Alt-B GHA cache |
|----------|-------------------------|-----------------|
| Implementación | 2-3 h | 30 min |
| CI build sin cambios | 3-5 min | 5-8 min |
| Determinismo | total | depende de cache GHA |
| Tamaño repo | +10-15 MB | 0 |
| Tamaño cache GHA | 0 | 50-100 MB |
| Visibilidad de diagramas en PR | sí (SVG diff/preview) | no |
| Build local | 3-5 min siempre | 22-30 min |
| Java requerido en CI | NO (tras pre-render) | sí (pero skip cache hit) |
| Auditoría | sí (commits muestran cambios) | parcial |

**Recomendación:** Alt-A.

Razones:
- Determinismo total (no depende de eviction de GHA cache).
- Build local también se beneficia (no solo CI).
- Diagramas son auditables en commits y PRs.
- Java solo necesario en pre-render local cuando hay
  diagramas nuevos.
- Trade-off de +10-15 MB en repo es aceptable.

## Decisiones de diseño Alt-A

### D-01: Hash basado en contenido del bloque + estilos

**Hash input:**

```
sha256(plantuml_styles.puml content + "\n" + uml_block_content)[:16]
```

Incluir el archivo de estilos garantiza re-render cuando
cambian estilos globales.

### D-02: Formato output SVG

Razones en Alt-D arriba.

### D-03: Path en source tree, no en build

`source/_generated_diagrams/` en lugar de
`build/_generated_diagrams/`.

- Sobrevive `make clean`.
- Se puede commitear.
- Sphinx `_static`-style accessible.

### D-04: Extensión preserva captions y options

El override del directive lee `:caption:`, `:alt:`,
`:align:`, `:name:` y los re-emite en el `image`/`figure`
node. Sin pérdida de metadata.

### D-05: Cache miss = fallback automático

Si el hash no existe (diagrama nuevo en una PR), la
extensión delega a `sphinxcontrib.plantuml` para render
inline. No falla. El pre-render script + commit posterior
limpia esto.

### D-06: CI step pre-render automático

Antes de `sphinx-build`, agregar:

```yaml
- name: Pre-render new PlantUML diagrams
  run: python scripts/prerender-plantuml.py
```

Garantiza cache poblado para diagramas nuevos sin
intervención manual.

### D-07: Pre-commit hook (opcional)

Hook git pre-commit que detecta `@startuml` nuevos en
diff y corre `prerender-plantuml.py` automáticamente.
Diferido a iteración posterior.

## Riesgos identificados

| ID | Riesgo | Severidad | Mitigación |
|----|--------|-----------|-----------|
| R-01 | Hash collisions | bajísima (sha256/16 hex = 2^64) | improbable; aceptable |
| R-02 | SVG no renderiza idéntico al PNG en algunos viewers | bajo | Sphinx + Furo theme soportan SVG nativamente |
| R-03 | Repo crece 10-15 MB | bajo | aceptable vs ahorro CI |
| R-04 | Diagramas con macros / `!include` | medio | el pre-render usa `!include` igual que sphinx; styles via `plantuml_cfg_file` |
| R-05 | Diagramas con caracteres no-ASCII en hash | nulo | sha256 acepta bytes |
| R-06 | Olvido de pre-render local antes de PR | bajo | CI step lo corre automáticamente |
| R-07 | Repo grande de SVGs binarios genera diffs ruidosos | medio | `.gitattributes` marca SVGs como `binary` para evitar diff text |
| R-08 | Estilos de PlantUML ausentes en diagramas extraídos | medio | `plantuml_cfg_file` global aplica al pre-render como en sphinx |

## Plan de ejecución (DECOMPOSE → EXECUTE)

### Stage 8 — Plan execution (T-NNN tasks)

**Bloque 1: Infraestructura del pre-render**

- T-001 Crear `scripts/prerender-plantuml.py` (Python).
- T-002 Verificar que extrae correctamente bloques de UCs
  conocidos (uc-acc-01, uc-perm-06, uc-rpt-04).
- T-003 Test idempotencia (correr 2 veces, debe no
  re-renderizar).

**Bloque 2: Extension Sphinx**

- T-004 Crear `source/_ext/plantuml_cached.py` con override
  del `uml` directive.
- T-005 Manejar `:caption:`, `:alt:`, `:align:`, `:name:`.
- T-006 Fallback a sphinxcontrib.plantuml en cache miss.

**Bloque 3: Wiring**

- T-007 Modificar `conf.py`: add `_ext` a sys.path.
- T-008 Add `'plantuml_cached'` a extensions ANTES de
  `'sphinxcontrib.plantuml'`.

**Bloque 4: Pre-render inicial**

- T-009 Run `scripts/prerender-plantuml.py` localmente
  hasta cubrir 965 diagramas.
- T-010 Commit `source/_generated_diagrams/*.svg`.
- T-011 Verificar build local: tiempo y warnings.

**Bloque 5: CI integration**

- T-012 Modificar `.github/workflows/validate.yml` para
  correr pre-render antes de sphinx-build.
- T-013 Push y verificar CI completa en < 10 min.

**Bloque 6: Documentación**

- T-014 Actualizar `ADR-DEVOPS-002` con la nueva decisión
  de pre-render.
- T-015 Crear `scripts/README.md` con instrucciones de
  uso del pre-render.
- T-016 `.gitattributes`: marcar SVGs en
  `_generated_diagrams/` como binary.

### Exit conditions (DoD)

- [ ] CI build < 10 min en runs sin cambios de diagramas
- [ ] CI build < 25 min en runs con N diagramas nuevos
- [ ] 0 warnings en build local con `-W`
- [ ] 0 invocaciones Java en sphinx-build cuando hay
      cache hit total
- [ ] ADR-DEVOPS-002 actualizado con la decisión
- [ ] Pre-render script idempotente y testeado

## Output esperado

`discover/svg-prerender-analysis.md` (este archivo) con:

- Análisis comparativo Alt-A vs Alt-B
- Decisión: Alt-A SVG committed
- Plan de ejecución T-001..T-016
- Trade-offs documentados
- Riesgos y mitigaciones

Próximo paso: aprobación de la estrategia → proceder a
DECOMPOSE (Stage 8) y EXECUTE (Stage 10).

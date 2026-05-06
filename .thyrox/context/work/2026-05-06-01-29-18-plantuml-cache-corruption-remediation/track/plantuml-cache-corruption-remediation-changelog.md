```yml
created_at: 2026-05-06 02:35:00
project: IACT-docs
work_package: 2026-05-06-01-29-18-plantuml-cache-corruption-remediation
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — PlantUML Cache Corruption Remediation

## Resumen

| Metrica | Antes | Despues |
|---|---|---|
| SVGs con "Syntax Error?" | 1227 / 1438 (85%) | **0 / 1157 (0%)** |
| SVGs valid | 211 | **1157** |
| Cache misses en strict build | 188 (predecessor) → 3 (despues fix) | **3** (residuales) |
| Build strict EXIT | 0 (falso positivo: extension no validaba) | **0 (real)** |
| Build strict warnings | 0 (mismo) | **0** |

## Trabajo realizado

### Phase 1 DISCOVER

Verificacion exhaustiva post-cierre del WP plantuml-cache-prerender-update
revelo que **1227 de 1438 SVGs** en el cache contenian
"Syntax Error?" como placeholder, generados por el commit
`e7bffe08` ("WIP — PlantUML pre-render infra") con el bug
`-cfgfile` que solo se arreglo hoy.

La extension `plantuml_cached.py` solo valida existencia, no
contenido — por eso el build "succeeded" todo este tiempo
mientras ~85% del HTML mostraba placeholders en lugar de
diagramas reales.

### Phase 10 EXECUTE

1. Borrado de los 1227 SVGs corruptos (preservando los 211
   GOOD del WP previo).
2. Re-corrida del prerender con los fixes ya aplicados:
   - `-cfgfile` removido (commit `f10631c7`).
   - `@startuml NAME` strip (commit `06ca12be`).
   - graphviz disponible.
3. Verificacion: 0 SVGs con "Syntax Error".
4. Build strict de verificacion: EXIT=0, 0 warnings.

### Phase 11 TRACK

- Numbers post-prerender: 945 rendered + 217 cached (los 211
  GOOD + 6 que sobrevivieron) + 3 errores.
- Numbers post-build: EXIT=0, 0 warnings, 3 cache misses
  (los known residuales).
- Cierre formal.

## Added

- Este changelog.
- `execute/build-logs/prerender-regeneration-2026-05-06T01-35-35.log`.
- `execute/build-logs/sphinx-strict-final-2026-05-06T02-06-34.log`.

## Changed

- 945 SVGs hash-named regenerados con contenido valido (eran
  placeholders "Syntax Error?").
- 1 SVG legacy descriptive `UC-BACK-001-login-usuario.svg`
  reemplazado con render valido del diagrama (era placeholder
  desde commit `e7bffe08`).

## Removed

- 281 SVGs corruptos eliminados — sus diagramas fuente ya no
  existen en source (cambios desde `e7bffe08`). Incluye 14 SVGs
  legacy descriptive (IACT-Architecture, UC-BACK-001-gestion-
  usuarios, etc.) que tampoco tienen referencias activas.

## Aceptado / no fixeado

### 3 cache misses residuales

- `base-cognitiva/_uml/uml-12-diagramas-componentes/una-pagina-web-con-un-applet-java`
- `base-cognitiva/plantuml-guide/ejemplos/test-component-diagram`
- `base-cognitiva/plantuml-guide/ejemplos/test-uc-diagram`

Hipotesis: hash discrepancy entre prerender y runtime. Investigar
en WP separado si se desea cache 100%.

### 3 errores residuales del prerender

- `std-012-tipos-de-diagramas-uml.rst #3, #4`: `@startuml` dentro
  de `.. code:: text` (ejemplos de docs).
- `adr-gob-002-plantuml-para-diagramas.rst #1`: idem.

Mejora futura: parser explicito de `.. uml::` directives en
lugar de regex naive de `@startuml..@enduml`.

## Verified

- 1157 SVGs en cache, 0 con "Syntax Error".
- Build strict post-regeneration: EXIT=0, 0 warnings.
- Working tree clean, commits pusheados.
- WP siguio R-1, R-2, R-2.1 de `.claude/rules/long-running-commands.md`:
  prerender y build con `nohup ... & disown` (no run_in_background),
  monitor con `tail -f --pid=$PID` (auto-cierra en muerte del PID).

## Status de promocion a CHANGELOG.md raiz

Aplica al merge a main. La regeneracion del cache es un cambio
sustantivo: ~85% de los diagramas del HTML pasaran de mostrar
placeholders a mostrar el diagrama real.

## WPs sucesores derivados

1. `prerender-script-uml-directive-parser` — reemplazar regex
   naive por parser de `.. uml::` directives (low priority).
2. `prerender-cache-runtime-hash-debug` — investigar las 3
   hash discrepancies entre prerender y runtime (low priority).

## Refs

- WP que destapo el problema: `2026-05-06-00-38-06-plantuml-cache-prerender-update`.
- Causa original: commit `e7bffe08` (WIP — PlantUML pre-render
  infra) que introdujo los 1227 SVGs corruptos.
- Fixes del script aplicados: commits `f10631c7` (cfgfile),
  `06ca12be` (NAME strip).
- Regla operacional seguida: `.claude/rules/long-running-commands.md`
  R-1, R-2, R-2.1, R-2.2.
- Build log: `execute/build-logs/sphinx-strict-final-2026-05-06T02-06-34.log`.
- Commit principal: `6e273350` (regeneracion masiva).

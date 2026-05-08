```yml
project: IACT-docs
work_package: 2026-05-06-01-29-18-plantuml-cache-corruption-remediation
created_at: 2026-05-06 01:29:18
closed_at: 2026-05-06 02:35:00
current_phase: Phase 11 — TRACK/EVALUATE
status: Cerrado
final_cache_state: "1157 SVGs, 0 con Syntax Error"
build_strict_clean: true
build_strict_log: execute/build-logs/sphinx-strict-final-2026-05-06T02-06-34.log
final_misses: 3
author: NestorMonroy
flow: rm
methodology_step: rm-management
target: Regenerar los 1227 SVGs corruptos en source/_generated_diagrams/ que fueron creados con el bug -cfgfile (placeholders "Syntax Error?" en lugar de diagramas reales). Verificar que los 1438 SVGs finales no contengan "Syntax Error".
predecessor_wp: 2026-05-06-00-38-06-plantuml-cache-prerender-update
```

# WP — PlantUML Cache Corruption Remediation

## Trigger

Tras cerrar `plantuml-cache-prerender-update`, una verificacion mas
exhaustiva del cache revelo que **1227 de 1438 SVGs contienen
"Syntax Error?"** como placeholder. Eran los SVGs originales del
commit `e7bffe08` ("WIP — PlantUML pre-render infra"), generados
con el bug `-cfgfile` desde la creacion inicial del cache.

El extension `plantuml_cached.py` solo verifica la existencia del
archivo SVG, no su contenido. Por eso el build "succeeded" sin
warnings, pero el HTML rendido muestra "Syntax Error?" placeholders
en lugar de los diagramas reales en ~85% de los archivos.

## Estado actual

| Metrica | Valor |
|---|---|
| Total SVGs en cache | 1438 |
| BAD (con "Syntax Error?") | 1227 |
| GOOD (los 211 del WP previo) | 211 |
| % corrupto | 85.3% |
| Build strict | EXIT=0 (falso positivo: extension no valida contenido) |
| HTML output afectado | ~1227 diagramas mostrando placeholder en lugar del diagrama real |

## Causa raiz

Bug `-cfgfile` en `scripts/prerender-plantuml.py` (ya arreglado en
commit `f10631c7` del WP plantuml-cache-prerender-update). Los 1227
SVGs originales fueron creados antes de ese fix.

## Plan

### Phase 10 EXECUTE

1. Borrar los 1227 SVGs BAD (preservar los 211 GOOD).
2. Re-correr `scripts/prerender-plantuml.py` (con los 2 fixes ya
   aplicados: sin `-cfgfile` + strip `@startuml NAME`).
3. Verificar todos los nuevos sean GOOD (0 con "Syntax Error").
4. Build strict de verificacion final.
5. Commit + push.

### Phase 11 TRACK

- Documentar regeneracion completa.
- Cierre formal.

## Pre-conditions

- ✅ scripts/prerender-plantuml.py con los 2 fixes aplicados
  (verificado: commits `f10631c7` y `06ca12be`).
- ✅ graphviz instalado (`/usr/bin/dot`).
- ✅ Java 21 disponible.
- ✅ Working tree clean (sin cambios pendientes).

## Estimacion

- Borrado de 1227 SVGs: <1 min.
- Re-prerender: ~5-10 min (1438 diagramas; los previos sin styles
  serializan ~5s c/u).
- Verificacion: <1 min.
- Build strict: ~5-30 min (variable per overhead Sphinx HTML).
- **Total: 15-45 min wall-clock.**

Per R-1..R-5 de `.claude/rules/long-running-commands.md`: todos los
comandos en background detached, monitor con grep line-buffered.

## Riesgos

- **R-01**: El prerender puede generar errores residuales en
  diagramas con sintaxis no estandar. Mitigacion: aceptar
  mismos 4 known issues del WP previo (3 hash discrepancies
  runtime + 1 falso positivo en `.. code:: text`).
- **R-02**: La regeneracion masiva produce un commit grande
  (~1227 archivos). Mitigacion: commit atomico con mensaje
  Tim Pope claro explicando que son regeneraciones, no nuevos
  artefactos.
- **R-03**: Cambios en `plantuml-styles.puml` desde el WP previo
  invalidarian los 211 GOOD tambien. Mitigacion: verificar
  `git log -- source/_static/plantuml-styles.puml` desde
  `255fab7d` y, si cambio, regenerar tambien los 211.

## Stopping points

- **SP-01** (gate humano): aprobar bootstrap + plan.
- **SP-02** (gate tecnico): regeneracion completa, 0 SVGs
  con "Syntax Error".
- **SP-03** (gate tecnico): build strict EXIT=0, 0 warnings,
  ≤3 cache misses (los known residuales del WP previo).

## Anatomia del WP

```
2026-05-06-01-29-18-plantuml-cache-corruption-remediation/
├── wp-state.md
├── execute/
│   └── build-logs/
│       ├── prerender-regeneration-{ISO}.log
│       └── sphinx-strict-post-regen-{ISO}.log
└── track/
    └── plantuml-cache-corruption-remediation-changelog.md
```

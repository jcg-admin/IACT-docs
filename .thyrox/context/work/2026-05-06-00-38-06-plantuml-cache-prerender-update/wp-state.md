```yml
project: IACT-docs
work_package: 2026-05-06-00-38-06-plantuml-cache-prerender-update
created_at: 2026-05-06 00:38:06
current_phase: Phase 10 — EXECUTE
status: Activo
author: NestorMonroy
flow: rm
methodology_step: rm-management
target: Eliminar la causa raiz de builds lentos detectada en WP plantuml-cached-effectiveness-audit. Correr scripts/prerender-plantuml.py para llevar el cache de SVGs PlantUML del 83.2% al ~100%. Verificar build strict siguiente con 0 misses.
predecessors:
  - 2026-05-06-00-11-02-plantuml-cached-effectiveness-audit (registro la necesidad)
  - 2026-05-06-00-31-12-api-socket-error-investigation (registro la M-4 mitigacion de fondo)
size: micro (DISCOVER → EXECUTE → TRACK)
sp01_decisions:
  - dry_run_count: 212 diagramas missing (de 1165 totales, 953 cacheados)
  - estimacion_tiempo: 212 × 5-10s = ~20-35 min wall-clock
  - modo_ejecucion: background con monitor (per R-1..R-2 del WP api-socket-error)
```

# WP — PlantUML Cache Prerender Update

## Trigger

WPs sucesores `plantuml-cached-effectiveness-audit` (cerrado early-close)
y `api-socket-error-investigation` registraron este WP como mitigacion
de fondo: el cache PlantUML al 83.2% causa builds de ~20 min, lo que
dispara `cli_sse_liveness_timeout` (transporte SSE).

## Objetivo

Llevar `source/_generated_diagrams/` al 100% de cobertura de los
diagramas en `source/**/*.rst`.

## Pre-conditions verificadas

- ✅ `scripts/prerender-plantuml.py` existe y es ejecutable (Python 3.11).
- ✅ `tools/bin/plantuml` wrapper existe.
- ✅ Java 21 disponible (`openjdk version 21.0.10`).
- ✅ Dry-run ejecutado: 212 missing / 1165 totales / 953 cacheados.

## Plan

### Phase 10 EXECUTE

1. Lanzar prerender en background detached (no foreground per L-08
   y R-1 del api-socket-error WP).
2. Monitor con grep line-buffered para outcome (per R-2).
3. Persistir log en `execute/build-logs/prerender-{ISO}.log`.
4. Tras completar prerender: relanzar build strict en background.
5. Verificar 0 misses en build strict log.

### Phase 11 TRACK

- Documentar conteos pre/post (cached/rendered/errors).
- Verificar build strict times (esperado: <5 min vs ~20 min anterior).
- Cierre formal.

## Stopping points

- **SP-01**: dry-run aprobado (212 diagramas, ~30 min estimado). ✅
- **SP-02**: prerender complete sin errores fatales.
- **SP-03**: build strict siguiente con 0 misses + warnings.

## Anatomia esperada

```
2026-05-06-00-38-06-plantuml-cache-prerender-update/
├── wp-state.md                                       ← este
├── execute/
│   └── build-logs/
│       ├── prerender-{ISO}.log
│       └── sphinx-strict-post-prerender-{ISO}.log
└── track/
    └── plantuml-cache-prerender-update-changelog.md
```

## Riesgos

- **R-01**: 212 diagramas a renderizar puede dar errores en algunos
  bloques mal formados. Mitigacion: el script reporta errores
  individuales sin abortar; revisar al final.
- **R-02**: Wall-clock total puede exceder 30 min, durante los cuales
  no se puede esperar foreground. Mitigacion: detached + monitor
  per R-1..R-2 del api-socket-error WP.
- **R-03**: Cambios en `plantuml-styles.puml` invalidarian el cache
  completo. Verificar que el archivo no haya cambiado durante este
  WP.

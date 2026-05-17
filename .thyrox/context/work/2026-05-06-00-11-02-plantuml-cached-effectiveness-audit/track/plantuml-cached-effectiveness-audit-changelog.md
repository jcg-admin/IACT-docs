```yml
created_at: 2026-05-06 00:30:00
project: IACT-docs
work_package: 2026-05-06-00-11-02-plantuml-cached-effectiveness-audit
phase: Phase 11 — TRACK/EVALUATE (early-close)
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — PlantUML Cached Effectiveness Audit (early-close)

WP cerrado en early-close: la pregunta del trigger
("por que no estamos usando `source/_ext/plantuml_cached.py`") quedo
resuelta en Phase 1 DISCOVER con evidencia objetiva del build log
del WP predecesor. No se requirieron fases adicionales.

## Hallazgo principal

El cache **SI se usa**, no es un caso de "no se usa". Evidencia:

| Metrica | Valor | Fuente |
|---|---|---|
| `plantuml_cached` cargado en conf.py | si | `source/conf.py:44` |
| SVGs en `source/_generated_diagrams/` | 1227 | `ls` |
| Directivas `.. uml::` totales en source | 1119 | `grep -rE "^\.\. uml::"` |
| Cache misses en build de WP predecesor | 188 | log strict 2026-05-05T23-37-04 |
| **Hit rate** | **83.2%** | calculo |

La percepcion de "no se usa" se debe al impacto observable de los
188 misses (~10s c/u con Java + PlantUML = ~30 min wall-clock),
que dilato el strict build a ~15-20 minutos y disparo socket
timeout en sesion previa.

## Causa raiz

Los 188 misses corresponden, en gran medida, a los ~99 archivos
nuevos creados en el WP predecesor `use-case-view-uml07-standalone-pass`
(83 uml-07 standalone + 16 domain-model), que nunca pasaron por
`scripts/prerender-plantuml.py`. El cache funciona pero esta stale.

## Recomendacion (no-bloqueante para este WP)

Crear WP sucesor `plantuml-cache-prerender-update` con:

1. Correr `scripts/prerender-plantuml.py` sobre los 99 archivos
   nuevos para llevar hit rate a ~100%.
2. Verificar build strict siguiente con 0 misses.
3. Documentar en `.claude/rules/build-logs.md` o equivalente: tras
   batch generation de diagramas, correr prerender como SP-03
   estandar antes de sphinx strict.

## Added

- `wp-state.md` con hallazgo de Phase 1 DISCOVER + cierre formal.
- Este changelog.

## Changed / Fixed / Removed

- N/A — WP de pura investigacion, sin cambios al codigo o docs.

## Aceptado / no fixeado

- **No remediar el cache stale en este WP**. La remediacion (correr
  prerender + verificar) es scope de un WP sucesor enfocado.
- **No documentar guideline en `.claude/rules/`**. Esa
  estandarizacion va en el WP sucesor, no en este (que es
  diagnostic-only).

## Status de promocion a CHANGELOG.md raiz

No aplica — WP de investigacion sin cambios productivos.

## WPs sucesores derivados

1. `plantuml-cache-prerender-update` — correr prerender + verificar
   hit rate 100% + estandarizar workflow.

## Refs

- Predecesor: `2026-05-05-20-28-12-use-case-view-uml07-standalone-pass`.
- Build log de evidencia: `.thyrox/context/work/2026-05-05-20-28-12-use-case-view-uml07-standalone-pass/execute/build-logs/sphinx-strict-final-2026-05-05T23-37-04.log`.
- Extension auditada: `source/_ext/plantuml_cached.py`.
- Prerender script: `scripts/prerender-plantuml.py`.

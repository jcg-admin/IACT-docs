```yml
created_at: 2026-05-05 23:05:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — Use Case View UML-07 Standalone Pass

Formato Keep a Changelog. Promoción a `CHANGELOG.md` raíz: NO en este
WP — el merge se hace a `feature/solve-problem-docs` vía
`feature/cnst-033-uml-conformance`. La promoción a CHANGELOG raíz
ocurrirá cuando llegue el merge a `main` con bump de versión.

## Added

### Use Case View — 83 archivos uml-07 standalone

Por módulo (13 módulos):

- `access/` — 7 archivos (uc-acc-01..09, sin 06 y 07).
- `admin/` — 3 archivos (uc-adm-01..03).
- `alerts/` — 5 archivos (uc-alr-01..05).
- `audit/` — 4 archivos (uc-aud-01..04).
- `auth/` — 5 archivos (uc-auth-01..05).
- `caller/` — 5 archivos (uc-cli-01..05).
- `logs/` — 7 archivos (uc-log-01..07).
- `operator/` — 10 archivos (uc-opr-01..10).
- `permissions/` — 10 archivos (uc-perm-01..10).
- `pipeline/` — 4 archivos (uc-pip-01..04).
- `reports/` — 16 archivos (uc-rpt-01..04, 07..17 + uc-inc-rpt-01).
- `supervision/` — 3 archivos (uc-sup-01..03).
- `users/` — 4 archivos (uc-usr-01..04).

Convenciones aplicadas:

- Naming auto-explicativo: `uc-XXX-NN-<slug-descriptivo>.rst`.
- STD-011 aliases: `alias = label exacto`, sin abreviar.
- Funciones RBAC como actores (P-15), no roles.
- `<<sistema>>` para entidades del domain-model con nombre canónico.
- BR-006: sin `<|--` entre actores (NIST RBAC Flat).
- R-01..R-12 de uml-07 conformance.

### Domain-model — 16 archivos nuevos

9 clases:
- `authorization-guard.rst`
- `blacklisted-token.rst`
- `internal-message.rst`
- `pipeline-execution-repo.rst`
- `metrics-cache.rst`
- `idempotency-policy.rst`
- `expiration-policy.rst`
- `password-generator.rst`
- `effective-permissions-aggregator.rst`

5 repos canónicos:
- `user-repo.rst`
- `function-repo.rst`
- `function-group-repo.rst`
- `separation-rule-repo.rst`
- `access-group-repo.rst`

2 patterns documentales:
- `specification-pattern.rst`
- `strategy-pattern.rst`

### Module index updates — 13 archivos

Cada `use-case-view/<mod>/index.rst` actualizado con sección
`UC standalone uml-07` apuntando al nuevo archivo standalone vía
toctree.

### Scripts y herramientas

- `scripts/validate-uml07-standalone.sh` — auditor con checks
  C-01..C-08 (R-01..R-12 + BR-006 + STD-011 + R-12 codenames).

### Artefactos del WP

- `discover/use-case-view-uml07-standalone-pass-analysis.md` —
  análisis Phase 1.
- `discover/uml07-canonical-rules-annex.md` — reglas R-01..R-11
  + STD-011 + STD-012.
- `analyze/actor-vocabulary-analysis.md` — Phase 3.
- `analyze/domain-model-completion-analysis.md` — gap analysis
  domain-model.
- `strategy/use-case-view-uml07-standalone-pass-solution-strategy.md`.
- `plan/use-case-view-uml07-standalone-pass-plan.md`.
- `plan-execution/use-case-view-uml07-standalone-pass-task-plan.md`.
- `execute/build-logs/*.log` — logs ISO 8601 (sphinx strict +
  PlantUML pre-render).
- `track/audit-report-2026-05-05T21-55-01.md` — audit report 0
  violaciones.
- `track/coverage-analysis.md` — cobertura UV vs CU + R-07
  exception.
- `track/use-case-view-uml07-standalone-pass-lessons-learned.md` —
  L-08..L-14.
- `use-case-view-uml07-standalone-pass-risk-register.md`.

## Changed

### `reports/index.rst`

- Toctree entry renombrado: `uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento`
  → `uc-inc-rpt-01-resolver-segmento` (eliminó prefijo duplicado).

### 33 archivos uml-07 standalone — fix título overline

Overlines/underlines extendidos de 30 (o 46/48) a 60 `=` para
compatibilidad con Sphinx strict `-W`. El em-dash en los títulos
hizo que la longitud calculada fuera incorrecta. Archivos afectados
listados en commit `b4c4bbd0`.

## Fixed

- **F-01 — `uc-inc-rpt-01` naming bug**: archivo
  `uc-inc-rpt-01-uc-inc-rpt-01-resolver-segmento.rst` renombrado a
  `uc-inc-rpt-01-resolver-segmento.rst` (commit `414bd1f5`).
- **F-02 — Sphinx strict 33 warnings**: títulos con em-dash y
  overline corto resueltos (commit `b4c4bbd0`).

## Removed

- N/A — el WP es aditivo (creación de 83 + 16 nuevos archivos +
  updates de index).

## Aceptado / no fixeado

### Excepción a R-07 — `uc-inc-rpt-01` mantiene archivo standalone

R-07 ("UC included nunca solo, sin archivo standalone") se mantiene
como regla por defecto. Para `uc-inc-rpt-01` se documenta excepción
formal con 4 criterios de justificación (5+ pasos validación,
3 actores externos, CNST-008 crítico, reutilización transversal en
16 UC_RPT_*). Detalle en `track/coverage-analysis.md` sección
"Excepción formal a R-07".

### Cross-refs reverse (CU → UV) — 0/83

Out of scope del WP. Documentado en lessons-learned L-10. Follow-up:
WP `casos-uso-reverse-xref-pass`.

### Phase 9 PILOT formal — sustituido por audit script

WP saltó SP-02 formal (5 sample UCs revisados manualmente) y usó
`scripts/validate-uml07-standalone.sh` con 0 violaciones. L-12
documenta el trade-off: audit cubre sintaxis pero no semántica
profunda.

### Phase 12 STANDARDIZE — saltado

WP de tamaño mediano-grande, escalabilidad permite saltar
STANDARDIZE. Patrones reutilizables documentados implícitamente en
`scripts/validate-uml07-standalone.sh` y en plantillas reusables ya
inferibles del corpus de 83 archivos.

## Verified (clean state)

- ✅ 83/83 archivos uml-07 standalone creados.
- ✅ 16 archivos domain-model nuevos con cross-refs canónicos.
- ✅ 13 module index actualizados.
- ✅ Audit script: 0 violaciones C-01..C-08.
- ✅ Cobertura forward UV → CU: 100% (83/83).
- ✅ Conteos por módulo idénticos en ambos lados.
- ✅ Build strict `-W` 0 warnings (post-fix títulos, commit
  `b4c4bbd0`, log
  `execute/build-logs/sphinx-strict-final-2026-05-05T23-37-04.log`).
- ✅ R-07 excepción documentada formalmente.

## Status de promoción a CHANGELOG.md raíz

**No aplica en este WP**. La promoción a `CHANGELOG.md` raíz
ocurrirá cuando `feature/solve-problem-docs` se mergee a `develop`
y luego a `main` con bump de versión. Las entradas de este WP
formarán parte de ese release.

## WPs sucesores derivados

1. `casos-uso-reverse-xref-pass` — agregar xref reverse CU → UV
   en 83 archivos (L-10, prioridad media).
2. `uml07-template-strict-validation` — gate de template antes
   de batch generation (L-08, prioridad baja).
3. `casos-uso-format-normalization` — uniformar formato FA-/EX-
   en `casos-uso/` (H-1, prioridad baja).
4. `uml07-audit-semantic-extension` — añadir checks C-09..C-12
   semánticos al audit (H-2, prioridad baja).

## Refs

- WP predecesor: `2026-05-05-14-49-16-use-case-view-uml07-rebuild`
  (cerrado, scope drift documentado en lessons L-01..L-07 heredadas).
- Branch: `feature/cnst-033-uml-conformance`.
- Commits clave: `b4c4bbd0` (fix títulos), `414bd1f5` (rename
  uc-inc-rpt-01).
- Normativa: STD-008, STD-011, STD-012, BR-006, CNST-005, CNST-033,
  P-15.
- Referencias externas: uml-07 R-01..R-12 (`source/base-cognitiva/_uml/`).

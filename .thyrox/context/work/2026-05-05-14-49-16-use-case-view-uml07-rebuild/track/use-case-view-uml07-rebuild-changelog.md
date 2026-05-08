```yml
created_at: 2026-05-05 20:28:12
project: IACT-docs
work_package: 2026-05-05-14-49-16-use-case-view-uml07-rebuild
phase: Phase 11 — TRACK/EVALUATE
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# WP Changelog — `use-case-view-uml07-rebuild`

Formato Keep a Changelog. Promoción a `CHANGELOG.md` raíz se hace al merge a `main` con bump de versión.

## Added

- 53 archivos `casos-uso/<mod>/<uc>/diagramas-uml/diagrama-de-caso-de-uso.rst` con
  diagramas UML reales (no stubs), por módulo:
  - admin: uc-adm-01..03 (3)
  - permissions: uc-perm-01..03 (3)
  - audit: uc-aud-01..04 (4)
  - pipeline: uc-pip-01..04 (4)
  - alerts: uc-alr-01..05 (5)
  - caller: uc-cli-01..05 (5)
  - supervision: uc-sup-01..03 (3)
  - reports: uc-inc-rpt-01, uc-rpt-10..17 (9)
  - logs: uc-log-01..07 (7)
  - operator: uc-opr-01..10 (10)
- Sección `.. seealso::` con `:doc:` cross-refs a domain-model en los 53 archivos
  (≈250 cross-refs totales, 1-9 por archivo).
- `.claude/rules/build-logs.md` — convención ISO 8601 + WP path para logs de build.
- `.claude/rules/git-flow.md` — política de branching feature/<wp> → solve-problem-docs.
- `find-uc-stubs.sh` — detector de stubs pendientes con marcador `TODO (use-case-view-uml07-rebuild Nivel A)`.
- `discover/decisions-log.md` — registro de D-01..D-09 con alternativas descartadas.
- `discover/inventory.json` — inventario machine-readable de 83 UCs (predecesor + actualización).
- 3 build logs históricos en formato ISO 8601:
  - `sphinx-strict-pr14-2026-05-05T16-50-32.log` (5 warnings — race condition)
  - `sphinx-strict-postfix-2026-05-05T17-19-47.log` (73 warnings — build limpio)
  - `sphinx-strict-stubs-2026-05-05T17-34-03.log` (53 toctree warnings — pre toctree fix)
- Build logs Level A:
  - `sphinx-strict-leveA-admin-2026-05-05T17-39-55.log` (post admin module)
  - `sphinx-strict-leveA-completo-2026-05-05T19-22-00.log` (final, 0 warnings)
- 12 toctree updates en `casos-uso/<uc>/diagramas-uml/index.rst` para incluir
  `diagrama-de-caso-de-uso` (53 entradas nuevas).

## Changed

- `casos-uso/logs/uc-log-02/diagramas-uml/`:
  - `componentes-etl-log.rst` → `componentes-pipeline-log.rst` (rename + title).
  - `secuencia-de-consulta-etl-log.rst` → `secuencia-de-consulta-pipeline-log.rst`.
- `domain-model/exceptional-permission-repo.rst:95-97`: refs `uc-acc-06/uc-acc-07` →
  `uc-perm-03/uc-perm-04` (UCs reales que existen).
- `domain-model/permission-cache.rst:125`: ref `uc-acc-06` → `uc-perm-03`.
- `use-case-view/admin/index.rst`: 5 refs cortas (`uc-access`/`uc-permissions`/`uc-audit`)
  → paths absolutos a `/arquitectura-tecnica/use-case-view/{module}/index`.

## Fixed

- 73 warnings de strict build sphinx → 0 warnings (CI PR #14 verde).
- 4 warnings `toc.not_readable` + `toc.not_included` por rename ETL→Pipeline incompleto
  (commit `405751c1`).
- 53 warnings `ref.doc` forward refs a `diagrama-de-caso-de-uso` faltantes (commit `cdd9a2da`).
- 53 warnings `toc.not_included` por stubs huérfanos en toctrees (commit `972a4f77`).
- 7 warnings de typography `Title underline/overline too short` (varios archivos).
- 5 refs rotas en `use-case-view/admin/index.rst`.
- 3 refs forward inválidas en `domain-model/` apuntando a UCs inexistentes.

## Removed

- N/A (ningún archivo eliminado en este WP).

## Aceptado / no fixeado

- **TD-N1 — Vocabulario PlantUML interno en uc-log-02**: las 2 archivos renombradas
  (componentes-pipeline-log, secuencia-de-consulta-pipeline-log) aún contienen
  `ETLScheduler`, `sp_etl_maestro`, `/logs/etl/`, `ETLLogEndpoint` en su PlantUML
  interno. Decidido aceptar como deuda — refleja implementación real, requiere
  decisión arquitectónica separada para CNST-033 §8.2 (HTTP routes + SP names).
- **TD-N2 — Funcion RBAC desalineada en pipeline UC specs**: `informacion-general.rst`
  de UC_PIP_01..04 declara `view_etl_supervision` etc. mientras que
  `actores-precondiciones.rst` usa la forma rename-compliant `view_pipeline_status`.
  Los diagramas UML usan la forma compliant; metadata pendiente de barrer en WP futuro.

## Status de promoción a `CHANGELOG.md` raíz

**Pendiente** — esperando merge de PR #14 a `feature/solve-problem-docs` y luego
escalado a `develop` y `main`. NO se promueve aún. Las entradas relevantes para
`CHANGELOG.md` raíz (cuando llegue el bump de versión) son las de "Added" y "Changed"
sobre `casos-uso/` y "Added" sobre `.claude/rules/`.

## WPs sucesores derivados

1. `2026-05-05-20-28-12-use-case-view-uml07-standalone-pass` — retoma el target
   original (83 archivos uml-07 standalone en use-case-view/).
2. `domain-model-completion-pass` (futuro) — crear ~18 clases faltantes en
   domain-model (AuthorizationGuard, ThrottlePolicy, TransactionManager, etc.).
3. `domain-model-method-augmentation-pass` (futuro) — agregar ~30 métodos a
   clases existentes (PermissionService.check_bulk_with_cache, etc.).
4. `casos-uso-cnst-033-vocabulary-cleanup-pass` (futuro) — barrer TD-N1 + TD-N2.

## Refs

- PR #14: https://github.com/jcg-admin/IACT-docs/pull/14
- HEAD final del WP: `43823a51` (Cross-link 53 UC diagrams with domain-model entities)
- Build logs: `discover/build-logs/` (5 logs en formato ISO 8601)
- Decisions log: `discover/decisions-log.md` (D-01..D-09)
- Lessons learned: `track/use-case-view-uml07-rebuild-lessons-learned.md` (L-01..L-07)

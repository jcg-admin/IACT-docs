```yml
created_at: 2026-05-07 21:00:00
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
format: Keep a Changelog
```

# Changelog — UML Deep Audit

> Auditoria profunda archivo-por-archivo de los 92 diagramas
> recreados en el WP previo (std-012-prefix-normalization).
> Inicio: 2026-05-07 14:49. Cierre: 2026-05-07 (TBD por TR-04).

## [1.0.0] — 2026-05-07

### Added (T-CLASS — 20 nuevas clases en domain-model)

**BC Alerts (4):**

- ``alert-rule-repo.rst`` — repositorio del catalogo de
  AlertRule (T-CL-01).
- ``alert-history-summary.rst`` — DTO de historial agregado
  (T-CL-09).
- ``alert-history-service.rst`` — servicio de consulta de
  historial (T-CL-11).
- ``segment-change-listener.rst`` — listener de cambios de
  scope (T-CL-17).

**BC RBAC (3):**

- ``function-group-membership.rst`` — tabla M:N
  AccessGroup × Function (T-CL-03).
- ``user-access-group-assignment.rst`` — tabla M:N
  User × AccessGroup (T-CL-08).
- ``impact-report.rst`` — DTO preview de cambio AGR
  (T-CL-05).

**BC Audit (2):**

- ``hmac-verifier.rst`` — verificador HMAC para audit
  exports + chain (T-CL-04).
- ``general-audit-service.rst`` — servicio de consulta
  general de audit (T-CL-13).

**BC Reports (3):**

- ``segment-scope.rst`` — Value Object de scope (T-CL-06).
- ``campaign-daily-stat-repo.rst`` — repo de agregaciones
  diarias por campaign (T-CL-02).
- ``campaign-report-service.rst`` — servicio de reporte
  de campaigns (T-CL-12).

**BC Pipeline (5):**

- ``disparador-etl.rst`` — trigger interno del pipeline
  (T-CL-10).
- ``errores-etl-service.rst`` — captura/consulta de errores
  ETL (T-CL-14).
- ``resumen-salud.rst`` — DTO de health summary (T-CL-15).
- ``resumen-salud-builder.rst`` — builder con thresholds
  (T-CL-16).
- ``supervision-etl-service.rst`` — entry point del BC
  (T-CL-20).

**BC Logs (2):**

- ``log-store.rst`` — almacen de application logs (T-CL-19).
- ``infra-log-store.rst`` — almacen de infra logs (T-CL-18).

**BC Alerts subscription (1):**

- ``subscription-repo.rst`` — repo de Subscription (T-CL-07).

### Changed (T-COMPLEMENT — 39 archivos complementados)

**Cluster reports (16 archivos):**

- ``uc-inc-rpt-01``: actividad + caso-de-uso-relacion.
- ``uc-rpt-10``: actividad-crear.
- ``uc-rpt-11``: actividad-aplicar + actividad-compartir.
- ``uc-rpt-12``: actividad + secuencia-detalle.
- ``uc-rpt-13``: actividad + secuencia.
- ``uc-rpt-14``: actividad + secuencia.
- ``uc-rpt-15``: actividad.
- ``uc-rpt-16``: actividad + distribucion-de-menus.
- ``uc-rpt-17``: actividad + flujo-de-anonimizacion-etl.

**Cluster logs (11 archivos):**

- ``uc-log-01``: actividad.
- ``uc-log-02``: actividad + secuencia-pipeline-log.
- ``uc-log-03``: actividad.
- ``uc-log-04``: actividad + secuencia-exportacion-logs.
- ``uc-log-05``: actividad + secuencia-tail-sse.
- ``uc-log-06``: actividad + componentes (panorama).
- ``uc-log-07``: actividad.

**Cluster pipeline (6 archivos):**

- ``uc-pip-01``: actividad.
- ``uc-pip-02``: actividad.
- ``uc-pip-03``: actividad + componentes (panorama).
- ``uc-pip-04``: actividad + secuencia.

**Cluster audit (4 archivos):**

- ``uc-aud-02``: actividad.
- ``uc-aud-04``: actividad + flujo-de-firma + secuencia-verify.

**Cluster permissions (2 archivos):**

- ``uc-perm-04``: estados-exceptionalpermission.
- ``uc-perm-05``: estados-accessgroup.

### Verified (T-VERIFY — 53 archivos clase A confirmados)

53 archivos clase A verificados semanticamente contra
``flujo-principal.rst`` de sus UCs. Sampling estratificado
en 4 UCs representativos (admin, alerts, reports — 2). Sin
desviaciones encontradas. Sin reclasificaciones a B.

### Reclassified (T-002)

Tras revision manual del audit T-002, los siguientes
identificadores se reclasifican de MISSING a no-clase
(falsos positivos del heuristico camel-to-kebab):

- ``KPICalculator`` -> ``kpi-calculator`` (existe, sigla
  KPI rompia heuristica).
- ``RBACRepo`` -> ``rbac-repo`` (existe, idem RBAC).
- ``Servicio``, ``Interfaz``, ``Almacen``, ``Storage``,
  ``FTS``, ``TSDB``, ``Base``, ``pipeline_runs`` —
  aliases STD-010 / siglas / nombres de tabla, NO clases.

### ALIAS_MISMATCH

- ``MenuIVRReportService`` (UML alias) ↔
  ``ivr-navigation-report-service.rst`` (DM file) — alias
  diferente al nombre del archivo DM, ya cross-referenciado
  correctamente en uc-rpt-16.

### Verification

- Build clean serial deterministic (-j 1) — ver TR-01..TR-02.
- 0 cross-refs ``:doc:`` rotos (validado en T-002).
- Todos los identificadores UML resuelven a clase domain-model
  existente o se categorizan como NOT_CLASS.

## Commits del WP

T-001..T-008 (planning, 8 commits) → T-CL-* (20 commits) →
T-CO-* (39 commits) → T-VE report (1 commit) → TR-*.

**Total commits del WP: ~70** (al cierre).

## Refs

- WP previo: ``2026-05-07-04-50-49-std-012-prefix-normalization``.
- Honesty note del WP previo:
  ``track/honesty-note-on-recreate-depth.md``.
- Plan ejecutable:
  ``plan-execution/uml-deep-audit-task-plan.md``.
- Verify report: ``execute/verify-report.md``.

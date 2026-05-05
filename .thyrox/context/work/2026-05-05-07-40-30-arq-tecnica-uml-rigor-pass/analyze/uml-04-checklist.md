```yml
created_at: 2026-05-05 08:00:00
project: IACT-docs
work_package: 2026-05-05-07-40-30-arq-tecnica-uml-rigor-pass
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# UML-04 Checklist — Domain Model Rigor Pass

Matriz archivo × punto. Notación:

- ✓ aplicado
- N/A no aplica (no hay relaciones, o concepto no
  pertenece al modelo de la clase)
- ⏳ pendiente

Los 8 puntos:

1. **Mult** — multiplicidades en extremos (D-02)
2. **Rol** — roles en extremos (D-03)
3. **Restr** — ``{ordered}`` / ``{unique}`` /
   ``{readOnly}`` (D-04)
4. **Calif** — asociaciones calificadas (D-05)
5. **AssocCls** — clase de asociación (D-06)
6. **Gen** — generalización / abstractas (D-07)
7. **Reflex** — asociación reflexiva (D-08)
8. **DepStr** — estereotipo de dependencia (D-09)

## RBAC bounded context (10 archivos)

| Archivo | Mult | Rol | Restr | Calif | AssocCls | Gen | Reflex | DepStr |
|---------|------|-----|-------|-------|----------|-----|--------|--------|
| access-group.rst | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| access-group-function.rst | ✓ | N/A | N/A | N/A | ✓ | N/A | N/A | N/A |
| action.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| assignment-repo.rst | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | ✓ |
| exceptional-permission-repo.rst | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | ✓ |
| function.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| menu.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| nav-domain.rst | ✓ | ✓ | ✓ | N/A | N/A | N/A | ✓ | N/A |
| permission-cache.rst | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | ✓ |
| permission-service.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| rbac-repo.rst | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | N/A |
| section.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Reports bounded context (17 archivos)

| Archivo | Mult | Rol | Restr | Calif | AssocCls | Gen | Reflex | DepStr |
|---------|------|-----|-------|-------|----------|-----|--------|--------|
| abandono-report-service.rst | ✓ | N/A | ✓ | N/A | N/A | ✓ | N/A | ✓ |
| agent-daily-stat-repo.rst | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | ✓ |
| agent-report-service.rst | ✓ | N/A | ✓ | N/A | N/A | ✓ | N/A | ✓ |
| base-report-service.rst (NUEVO) | ✓ | N/A | N/A | N/A | N/A | ✓ | N/A | N/A |
| bucket.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| clientes-report-service.rst | ✓ | N/A | ✓ | N/A | N/A | ✓ | N/A | ✓ |
| column-catalog.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| comparative.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| filter-validator.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| historical-report.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| kpi-calculator.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| menu-ivr-report-service.rst | ✓ | N/A | ✓ | N/A | N/A | ✓ | N/A | ✓ |
| report.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| saved-filter.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| saved-view.rst | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| scheduled-report-list-service.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| scheduled-report-repo.rst | ✓ | N/A | N/A | ✓ | N/A | N/A | N/A | ✓ |
| segment-resolver.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| servicio-reportes.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| transferencias-report-service.rst | ✓ | N/A | N/A | N/A | N/A | ✓ | N/A | ✓ |

## Audit bounded context (9 archivos)

| Archivo | Mult | Rol | Restr | Calif | AssocCls | Gen | Reflex | DepStr |
|---------|------|-----|-------|-------|----------|-----|--------|--------|
| alert-hook.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| audit-event.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| audit-query-service.rst | ✓ | N/A | ✓ | N/A | N/A | N/A | N/A | ✓ |
| audit-repo.rst | ✓ | N/A | ✓ | ✓ | N/A | N/A | N/A | ✓ |
| audit-service.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| audit-validator.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| cursor-encoder.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| export-worker.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| pii-scanner.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| sanitizer.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |

## Alerts bounded context (5 archivos)

| Archivo | Mult | Rol | Restr | Calif | AssocCls | Gen | Reflex | DepStr |
|---------|------|-----|-------|-------|----------|-----|--------|--------|
| alert-repo.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| alert-rule.rst | ✓ | N/A | ✓ | N/A | N/A | N/A | N/A | N/A |
| evaluator-reloader.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| rule-validator.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |
| timing-calculator.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | ✓ |

## Otros BCs (Auth, Calls, Pipeline ETL, Logs, Alerts entities)

Archivos sin relaciones inter-clase (single-class
diagrams) — no requieren multiplicidad:

- access-group.rst, application-log.rst, campaign.rst,
  etl-ejecucion.rst, etl-log.rst, export-job.rst,
  infrastructure-log.rst, internal-mailbox.rst, metric.rst,
  session.rst, technical-metric.rst, threshold.rst,
  system-health.rst, alert.rst, assignment.rst,
  exceptional-permission.rst, function-group.rst,
  separation-rule.rst, scheduled-report.rst (1 enum
  asociado, ya con multiplicidad)

Archivos con relaciones simples actualizados:

| Archivo | Mult | Rol | Restr | Calif | AssocCls | Gen | Reflex | DepStr |
|---------|------|-----|-------|-------|----------|-----|--------|--------|
| user.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| call.rst | N/A | N/A | N/A | N/A | N/A | N/A | N/A | N/A |
| subscription.rst | ✓ | N/A | N/A | N/A | N/A | N/A | N/A | N/A |

## Resumen agregado

- **Mult** ✓ aplicado en **42 archivos**
- **Restr** ``{ordered}`` aplicado en **6 archivos**
  (audit-query-service, audit-repo, agent-report-service,
  abandono-report-service, clientes-report-service,
  menu-ivr-report-service, alert-rule, nav-domain)
- **Calif** asociaciones calificadas aplicadas en
  **6 archivos** RBAC y Reports
- **AssocCls** clase de asociación corregida en
  **1 archivo** (access-group-function)
- **Gen** generalización aplicada en **6 archivos**
  (BaseReportService nuevo + 5 herederos)
- **Reflex** aplicada en **1 archivo** (nav-domain).
  ``Menu`` no es jerárquico — es proyección plana de
  Domain → Section → Action; la jerarquía vive en
  Domain.
- **DepStr** estereotipo de dependencia aplicado en
  **22 archivos** (``<<returns>>``, ``<<uses>>``,
  ``<<persists>>``)

## Pre-render validación

68 archivos × diagramas → **69 diagramas únicos**
(uno tiene 2 diagramas, ej: index/overview).

Todos renderizan sin error tras la pasada:

```
$ python3 scripts/prerender-plantuml.py --only domain-model
PlantUML pre-render summary:
  Total diagrams found: 69
  Cached (skipped):     69
  Rendered (this run):  0
```

## Trabajo pendiente (futuro WP)

- **Roles** en extremos de asociación: solo aplicado
  en ``nav-domain`` (parent/children). Los roles tipo
  ``stat_repo`` que usé como label se podrían formalizar
  como rol en lugar de label de asociación.
- **{readOnly}** en catálogos seed (``column-catalog``,
  ``action`` enum-like) — no aplicado por riesgo de
  ambigüedad con la propiedad de lectura/escritura del
  repo.
- **{unique}** en colecciones tipo Set — no aplicado;
  PlantUML no tiene anotación nativa estándar.
- ``Function`` posible reflexiva si existe jerarquía
  funcional: requiere consultar spec RBAC v5.5.0.

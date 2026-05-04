```yml
created_at: 2026-05-04 22:00:00
project: THYROX
work_package: 2026-05-04-20-13-29-domain-model-per-class
phase: Phase 11 — TRACK
author: NestorMonroy
status: Aprobado
version: 1.0.0
```

# Inventario de Clases Pendientes de Desarrollo

Clases identificadas en `source/requisitos/casos-uso/` que tienen stubs
en `domain-model/` (`:estado: Pendiente`, versión `0.1.0`). Cada una
requiere un WP dedicado para desarrollar atributos canónicos, enums,
relaciones completas y constraints.

## BC RBAC — 8 clases pendientes

| Clase | Archivo | Métodos conocidos | Fuente UC |
|-------|---------|-------------------|-----------|
| AccessGroupFunction | `access-group-function.rst` | — | uc-perm-05, uc-acc-04 |
| Action | `action.rst` | — | uc-perm-08 |
| AssignmentRepo | `assignment-repo.rst` | find_active_agrs_with_function | uc-perm-07 |
| ExceptionalPermissionRepo | `exceptional-permission-repo.rst` | find_active_revoke, find_active_grant | uc-perm-07 |
| Menu | `menu.rst` | — | uc-perm-08 |
| NavDomain | `nav-domain.rst` | — | uc-perm-08 |
| PermissionCache | `permission-cache.rst` | get, set, invalidate | uc-perm-07 |
| PermissionService | `permission-service.rst` | check, check_bulk | uc-perm-07 |
| RBACRepo | `rbac-repo.rst` | get_did_assignments, is_global_admin | uc-inc-rpt-01 |
| RuleValidator | `rule-validator.rst` | validate | uc-alr-01 |
| Section | `section.rst` | — | uc-perm-08 |

## BC Alerts — 5 clases pendientes

| Clase | Archivo | Métodos conocidos | Fuente UC |
|-------|---------|-------------------|-----------|
| AlertRule | `alert-rule.rst` | — | uc-alr-01 |
| AlertRepo | `alert-repo.rst` | query_history | uc-alr-04 |
| EvaluatorReloader | `evaluator-reloader.rst` | reload | uc-alr-01 |
| RuleValidator | `rule-validator.rst` | validate | uc-alr-01 |
| TimingCalculator | `timing-calculator.rst` | compute_ttak, compute_ttar | uc-alr-04 |

## BC Audit — 10 clases pendientes

| Clase | Archivo | Métodos conocidos | Fuente UC |
|-------|---------|-------------------|-----------|
| AlertHook | `alert-hook.rst` | on_commit | uc-perm-09 |
| AuditQueryService | `audit-query-service.rst` | list, get, aggregate, export | uc-perm-10 |
| AuditRepo | `audit-repo.rst` | query, get_by_id, aggregate | uc-perm-09, uc-perm-10 |
| AuditService | `audit-service.rst` | emit, emit_batch | uc-perm-09 |
| AuditValidator | `audit-validator.rst` | validate | uc-perm-09 |
| CursorEncoder | `cursor-encoder.rst` | encode, decode | uc-perm-10 |
| ExportWorker | `export-worker.rst` | enqueue, process | uc-perm-10 |
| PIIScanner | `pii-scanner.rst` | scan | uc-perm-09 |
| Sanitizer | `sanitizer.rst` | truncate, sanitize | uc-perm-09, uc-perm-10 |

## BC Reports — 22 clases pendientes

| Clase | Archivo | Métodos conocidos | Fuente UC |
|-------|---------|-------------------|-----------|
| AbandonoReportService | `abandono-report-service.rst` | get | uc-rpt-13 |
| AgentDailyStatRepo | `agent-daily-stat-repo.rst` | aggregate_by_agent, stream_by_agent | uc-rpt-12 |
| AgentReportService | `agent-report-service.rst` | list, detail | uc-rpt-12 |
| Bucket | `bucket.rst` | — | uc-rpt-03 |
| ClientesReportService | `clientes-report-service.rst` | get | uc-rpt-17 |
| ColumnCatalog | `column-catalog.rst` | list_for, exists | uc-rpt-10 |
| Comparative | `comparative.rst` | — | uc-rpt-03 |
| FilterValidator | `filter-validator.rst` | validate | uc-rpt-09 |
| HistoricalReport | `historical-report.rst` | — | uc-rpt-03 |
| KPICalculator | `kpi-calculator.rst` | derive_agent_kpis | uc-rpt-12, uc-rpt-14 |
| MenuIVRReportService | `menu-ivr-report-service.rst` | get | uc-rpt-16 |
| SavedFilter | `saved-filter.rst` | — | uc-rpt-09 |
| ScheduledReportListService | `scheduled-report-list-service.rst` | list, detail, runs | uc-rpt-08 |
| ScheduledReportRepo | `scheduled-report-repo.rst` | list_by_actor, get, list_runs | uc-rpt-08 |
| SegmentResolver | `segment-resolver.rst` | resolve | uc-rpt-13, uc-rpt-15, uc-rpt-16, uc-rpt-17 |
| ServicioReportes | `servicio-reportes.rst` | llamadas_abandonadas, menu_redirigidos, clientes, centros_transferencia | uc-rpt-13, uc-rpt-15, uc-rpt-16, uc-rpt-17 |
| TransferenciasReportService | `transferencias-report-service.rst` | get | uc-rpt-15 |

## Resumen

| BC | Clases pendientes |
|----|------------------|
| RBAC | 11 |
| Alerts | 5 |
| Audit | 9 |
| Reports | 17 |
| **Total** | **41** |

## Criterio de desarrollo para WP futuro

Para cada clase, el WP de desarrollo debe producir:

1. Atributos canónicos con tipos (UUID, String, DateTime, etc.)
2. Métodos con permisos RBAC (`<<function_code>>`)
3. Enums propios si aplica
4. Relaciones con otras clases del mismo BC
5. Constraints activos (BR-NNN, CNST-NNN)
6. `seealso` a los archivos relacionados
7. Bump de versión `0.1.0 → 1.0.0` y cambio de `:estado: Pendiente → Vigente`

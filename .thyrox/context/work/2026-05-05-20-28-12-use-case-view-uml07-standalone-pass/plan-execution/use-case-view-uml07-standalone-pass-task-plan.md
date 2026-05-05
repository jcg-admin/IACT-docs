```yml
created_at: 2026-05-05 21:15:00
project: IACT-docs
work_package: 2026-05-05-20-28-12-use-case-view-uml07-standalone-pass
phase: Phase 8 — PLAN EXECUTION
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Task Plan — `use-case-view-uml07-standalone-pass`

> 115 tareas atómicas T-001..T-115 distribuidas en 6 etapas.
> Marcar `[x]` al completar.

## Etapa 1 — Domain-model nuevas clases (14 archivos)

- [ ] **T-001** Crear `domain-model/authorization-guard.rst` (RBAC, 10 UCs)
- [ ] **T-002** Crear `domain-model/blacklisted-token.rst` (Auth, 5 UCs)
- [ ] **T-003** Crear `domain-model/internal-message.rst` (Mailbox, 4 UCs)
- [ ] **T-004** Crear `domain-model/pipeline-execution-repo.rst` (Pipeline, 4 UCs)
- [ ] **T-005** Crear `domain-model/metrics-cache.rst` (CrossCutting, 4 UCs)
- [ ] **T-006** Crear `domain-model/idempotency-policy.rst` (CrossCutting, 3 UCs)
- [ ] **T-007** Crear `domain-model/expiration-policy.rst` (RBAC/Auth, 2 UCs)
- [ ] **T-008** Crear `domain-model/password-generator.rst` (Auth/Users, 2 UCs)
- [ ] **T-009** Crear `domain-model/effective-permissions-aggregator.rst` (RBAC, 1 UC)
- [ ] **T-010** Crear `domain-model/user-repo.rst` (RBAC)
- [ ] **T-011** Crear `domain-model/function-repo.rst` (RBAC)
- [ ] **T-012** Crear `domain-model/function-group-repo.rst` (RBAC)
- [ ] **T-013** Crear `domain-model/separation-rule-repo.rst` (RBAC)
- [ ] **T-014** Crear `domain-model/access-group-repo.rst` (RBAC)
- [ ] **T-VAL-1A** Build strict local 0 warnings sobre los 14 nuevos
- [ ] **T-VAL-1B** Update `domain-model/index.rst` toctree con los 14 nuevos
- [ ] **T-COM-1** Commit Etapa 1 + push

## Etapa 2 — Patterns documentales (2 archivos)

- [ ] **T-015** Crear `domain-model/specification-pattern.rst` con lista CriticalFunctionSpec, LastHolderSpec, etc.
- [ ] **T-016** Crear `domain-model/strategy-pattern.rst` con lista NotifyOnAssignStrategy, NotifyOnRevokeStrategy, etc.
- [ ] **T-VAL-2A** Update `domain-model/index.rst` con los 2 patterns
- [ ] **T-VAL-2B** Build strict local 0 warnings
- [ ] **T-COM-2** Commit Etapa 2 + push

## Etapa 3 — SP-02 PILOT (5 sample uml-07)

- [ ] **T-017** `use-case-view/admin/uc-adm-01-gestionar-ciclo-de-vida-de-reglas-sod.rst` (multi-invoker)
- [ ] **T-018** `use-case-view/operator/uc-opr-02-atender-llamada-entrante.rst` (caller externo)
- [ ] **T-019** `use-case-view/reports/uc-rpt-12-reporte-de-agentes.rst` (UC_INC_RPT_01 included)
- [ ] **T-020** `use-case-view/supervision/uc-sup-01-monitorear-llamada-whisper.rst` (P-39 reforzado)
- [ ] **T-021** `use-case-view/audit/uc-aud-03-exportar-auditoria-async.rst` (ExportWorker async)
- [ ] **T-VAL-3A** Build strict local 0 warnings sobre los 5 sample
- [ ] **T-VAL-3B** Audit script verifica R-01..R-12 + BR-006 sobre los 5 sample
- [ ] **T-COM-3** Commit Etapa 3 + push
- [ ] **🛑 SP-02** Ejecutor revisa los 5 sample y aprueba pattern antes de propagar

## Etapa 4 — Generación masiva por módulo (78 uml-07 restantes)

### Etapa 4.1 — admin (2 restantes)

- [ ] **T-022** `use-case-view/admin/uc-adm-02-gestionar-catalogo-de-funciones.rst`
- [ ] **T-023** `use-case-view/admin/uc-adm-03-gestionar-catalogo-de-agrupadores-del-sistema.rst`
- [ ] **T-VAL-4A** Build strict + audit script para admin
- [ ] **T-COM-4A** Commit + push admin

### Etapa 4.2 — permissions (10)

- [ ] **T-024** `use-case-view/permissions/uc-perm-01-asignar-grupo-a-usuario.rst`
- [ ] **T-025** `use-case-view/permissions/uc-perm-02-revocar-grupo-a-usuario.rst`
- [ ] **T-026** `use-case-view/permissions/uc-perm-03-conceder-permiso-excepcional.rst`
- [ ] **T-027** `use-case-view/permissions/uc-perm-04-revocar-permiso-excepcional.rst`
- [ ] **T-028** `use-case-view/permissions/uc-perm-05-gestionar-grupos.rst` (slug exacto se confirma con casos-uso index)
- [ ] **T-029** `use-case-view/permissions/uc-perm-06-componer-grupo-de-funciones.rst`
- [ ] **T-030** `use-case-view/permissions/uc-perm-07-verificar-permiso.rst`
- [ ] **T-031** `use-case-view/permissions/uc-perm-08-consultar-permisos.rst`
- [ ] **T-032** `use-case-view/permissions/uc-perm-09-ver-historico.rst`
- [ ] **T-033** `use-case-view/permissions/uc-perm-10-consultar-auditoria-rbac.rst`
- [ ] **T-VAL-4B** Build strict + audit script para permissions
- [ ] **T-COM-4B** Commit + push permissions

### Etapa 4.3 — users (4)

- [ ] **T-034** `use-case-view/users/uc-usr-01-crear-usuario.rst`
- [ ] **T-035** `use-case-view/users/uc-usr-02-modificar-usuario.rst`
- [ ] **T-036** `use-case-view/users/uc-usr-03-desactivar-usuario.rst`
- [ ] **T-037** `use-case-view/users/uc-usr-04-consultar-usuarios.rst`
- [ ] **T-VAL-4C** Build + audit
- [ ] **T-COM-4C** Commit + push users

### Etapa 4.4 — auth (5)

- [ ] **T-038** `use-case-view/auth/uc-auth-01-iniciar-sesion.rst`
- [ ] **T-039** `use-case-view/auth/uc-auth-02-cerrar-sesion.rst`
- [ ] **T-040** `use-case-view/auth/uc-auth-03-recuperar-contrasena.rst`
- [ ] **T-041** `use-case-view/auth/uc-auth-04-cambiar-contrasena.rst`
- [ ] **T-042** `use-case-view/auth/uc-auth-05-renovar-token.rst`
- [ ] **T-VAL-4D** Build + audit
- [ ] **T-COM-4D** Commit + push auth

### Etapa 4.5 — access (7)

- [ ] **T-043** `use-case-view/access/uc-acc-01-asignar-funciones.rst`
- [ ] **T-044** `use-case-view/access/uc-acc-02-revocar-funciones.rst`
- [ ] **T-045** `use-case-view/access/uc-acc-03-consultar-permisos-efectivos.rst`
- [ ] **T-046** `use-case-view/access/uc-acc-04-asignar-agrupador.rst`
- [ ] **T-047** `use-case-view/access/uc-acc-05-ver-reglas-sod.rst`
- [ ] **T-048** `use-case-view/access/uc-acc-08-permiso-temporal.rst`
- [ ] **T-049** `use-case-view/access/uc-acc-09-vencimiento-permisos.rst`
- [ ] **T-VAL-4E** Build + audit
- [ ] **T-COM-4E** Commit + push access

### Etapa 4.6 — audit (3 restantes — uc-aud-03 ya en pilot)

- [ ] **T-050** `use-case-view/audit/uc-aud-01-consultar-auditoria-general.rst`
- [ ] **T-051** `use-case-view/audit/uc-aud-02-buscar-auditoria.rst`
- [ ] **T-052** `use-case-view/audit/uc-aud-04-generar-reporte-compliance.rst`
- [ ] **T-VAL-4F** Build + audit
- [ ] **T-COM-4F** Commit + push audit

### Etapa 4.7 — alerts (5)

- [ ] **T-053** `use-case-view/alerts/uc-alr-01-configurar-umbrales-de-alertas.rst`
- [ ] **T-054** `use-case-view/alerts/uc-alr-02-ver-alertas-activas.rst`
- [ ] **T-055** `use-case-view/alerts/uc-alr-03-reconocer-alerta.rst`
- [ ] **T-056** `use-case-view/alerts/uc-alr-04-ver-historial-de-alertas.rst`
- [ ] **T-057** `use-case-view/alerts/uc-alr-05-gestionar-suscripciones.rst`
- [ ] **T-VAL-4G** Build + audit
- [ ] **T-COM-4G** Commit + push alerts

### Etapa 4.8 — pipeline (4)

- [ ] **T-058** `use-case-view/pipeline/uc-pip-01-supervisar-pipeline.rst`
- [ ] **T-059** `use-case-view/pipeline/uc-pip-02-consultar-errores.rst`
- [ ] **T-060** `use-case-view/pipeline/uc-pip-03-consultar-disponibilidad-de-datos.rst`
- [ ] **T-061** `use-case-view/pipeline/uc-pip-04-solicitar-reintento-de-pipeline.rst`
- [ ] **T-VAL-4H** Build + audit
- [ ] **T-COM-4H** Commit + push pipeline

### Etapa 4.9 — caller (5)

- [ ] **T-062** `use-case-view/caller/uc-cli-01-iniciar-llamada-al-call-center.rst`
- [ ] **T-063** `use-case-view/caller/uc-cli-02-navegar-ivr.rst`
- [ ] **T-064** `use-case-view/caller/uc-cli-03-esperar-en-cola.rst`
- [ ] **T-065** `use-case-view/caller/uc-cli-04-solicitar-callback.rst`
- [ ] **T-066** `use-case-view/caller/uc-cli-05-calificar-atencion-post-call.rst`
- [ ] **T-VAL-4I** Build + audit
- [ ] **T-COM-4I** Commit + push caller

### Etapa 4.10 — supervision (2 restantes — uc-sup-01 ya en pilot)

- [ ] **T-067** `use-case-view/supervision/uc-sup-02-barge-in-en-llamada.rst`
- [ ] **T-068** `use-case-view/supervision/uc-sup-03-mensaje-broadcast-al-equipo.rst`
- [ ] **T-VAL-4J** Build + audit
- [ ] **T-COM-4J** Commit + push supervision

### Etapa 4.11 — logs (7)

- [ ] **T-069** `use-case-view/logs/uc-log-01-consultar-logs-del-sistema.rst`
- [ ] **T-070** `use-case-view/logs/uc-log-02-consultar-logs-del-pipeline.rst`
- [ ] **T-071** `use-case-view/logs/uc-log-03-buscar-logs.rst`
- [ ] **T-072** `use-case-view/logs/uc-log-04-exportar-logs.rst`
- [ ] **T-073** `use-case-view/logs/uc-log-05-ver-logs-de-infraestructura.rst`
- [ ] **T-074** `use-case-view/logs/uc-log-06-ver-estado-del-sistema.rst`
- [ ] **T-075** `use-case-view/logs/uc-log-07-ver-metricas-tecnicas.rst`
- [ ] **T-VAL-4K** Build + audit
- [ ] **T-COM-4K** Commit + push logs

### Etapa 4.12 — operator (10 — uc-opr-02 ya en pilot)

- [ ] **T-076** `use-case-view/operator/uc-opr-01-cambiar-estado-del-agente.rst`
- [ ] **T-077** `use-case-view/operator/uc-opr-03-realizar-llamada-saliente.rst`
- [ ] **T-078** `use-case-view/operator/uc-opr-04-hold-unhold-llamada.rst`
- [ ] **T-079** `use-case-view/operator/uc-opr-05-transferir-llamada.rst`
- [ ] **T-080** `use-case-view/operator/uc-opr-06-ingresar-disposition.rst`
- [ ] **T-081** `use-case-view/operator/uc-opr-07-solicitar-break-pausa.rst`
- [ ] **T-082** `use-case-view/operator/uc-opr-08-ver-propio-dashboard.rst`
- [ ] **T-083** `use-case-view/operator/uc-opr-09-ver-propio-historial-de-llamadas.rst`
- [ ] **T-084** `use-case-view/operator/uc-opr-10-leer-buzon-interno.rst`
- [ ] **T-VAL-4L** Build + audit
- [ ] **T-COM-4L** Commit + push operator

### Etapa 4.13 — reports (16 — uc-rpt-12 ya en pilot)

- [ ] **T-085** `use-case-view/reports/uc-inc-rpt-01-resolver-segmento.rst`
- [ ] **T-086** `use-case-view/reports/uc-rpt-01-ver-dashboard-ivr.rst`
- [ ] **T-087** `use-case-view/reports/uc-rpt-02-ver-dashboard-call-center.rst`
- [ ] **T-088** `use-case-view/reports/uc-rpt-03-comparar-periodos.rst`
- [ ] **T-089** `use-case-view/reports/uc-rpt-04-exportar-reporte.rst`
- [ ] **T-090** `use-case-view/reports/uc-rpt-07-listar-reportes-programados.rst`
- [ ] **T-091** `use-case-view/reports/uc-rpt-08-programar-reporte-recurrente.rst`
- [ ] **T-092** `use-case-view/reports/uc-rpt-09-aplicar-filtros.rst`
- [ ] **T-093** `use-case-view/reports/uc-rpt-10-guardar-vista.rst`
- [ ] **T-094** `use-case-view/reports/uc-rpt-11-compartir-reporte.rst`
- [ ] **T-095** `use-case-view/reports/uc-rpt-13-reporte-de-colas.rst`
- [ ] **T-096** `use-case-view/reports/uc-rpt-14-reporte-de-campanas.rst`
- [ ] **T-097** `use-case-view/reports/uc-rpt-15-reporte-de-transferencias.rst`
- [ ] **T-098** `use-case-view/reports/uc-rpt-16-reporte-de-menus-ivr.rst`
- [ ] **T-099** `use-case-view/reports/uc-rpt-17-reporte-de-clientes-unicos.rst`
- [ ] **T-VAL-4M** Build + audit
- [ ] **T-COM-4M** Commit + push reports

> **Slug verificación:** los slugs exactos de cada UC se toman de
> `discover/inventory.json::target` field.

## Etapa 5 — Module index updates (13 archivos)

- [ ] **T-101** `use-case-view/access/index.rst` — xref a uc-acc-* nuevos
- [ ] **T-102** `use-case-view/admin/index.rst` — xref
- [ ] **T-103** `use-case-view/alerts/index.rst` — xref
- [ ] **T-104** `use-case-view/audit/index.rst` — xref
- [ ] **T-105** `use-case-view/auth/index.rst` — xref
- [ ] **T-106** `use-case-view/caller/index.rst` — xref
- [ ] **T-107** `use-case-view/logs/index.rst` — xref
- [ ] **T-108** `use-case-view/operator/index.rst` — xref
- [ ] **T-109** `use-case-view/permissions/index.rst` — xref
- [ ] **T-110** `use-case-view/pipeline/index.rst` — xref
- [ ] **T-111** `use-case-view/reports/index.rst` — xref
- [ ] **T-112** `use-case-view/supervision/index.rst` — xref
- [ ] **T-113** `use-case-view/users/index.rst` — xref
- [ ] **T-VAL-5A** Build strict + audit final
- [ ] **T-COM-5** Commit + push module index updates

## Etapa 6 — Audit script + final build

- [ ] **T-114** Crear `scripts/validate-uml07-standalone.sh` con checks R-01..R-12 + BR-006
- [ ] **T-VAL-6A** `bash scripts/validate-uml07-standalone.sh` con 0 violaciones
- [ ] **T-115** Build strict final + reporte cobertura `:doc:` cross-refs
- [ ] **T-COM-6** Commit + push audit script + final

## DAG resumido

```
Etapa 1 (T-001..T-014) → T-VAL-1A → T-VAL-1B → T-COM-1
                                      │
                                      ▼
Etapa 2 (T-015..T-016) → T-VAL-2A,B → T-COM-2
                                      │
                                      ▼
Etapa 3 (T-017..T-021) → T-VAL-3A,B → T-COM-3 → 🛑 SP-02
                                      │
                                      ▼ (post-aprobación)
Etapa 4 (T-022..T-099, 78 tasks)      por módulo
                                      cada módulo: VAL + COM
                                      │
                                      ▼
Etapa 5 (T-101..T-113) → T-VAL-5A → T-COM-5
                                      │
                                      ▼
Etapa 6 (T-114, T-115) → T-VAL-6A → T-COM-6 → 🛑 SP-04
                                      │
                                      ▼
                               Phase 11 TRACK
```

## Trazabilidad

| Task | Solution Strategy section | Riesgo mitigado |
|---|---|---|
| T-001..T-014 | KI-1 + Etapa 1 | R-11 (lista cerrada) |
| T-015..T-016 | KI-4 | (patterns) |
| T-017..T-021 | Etapa 3 | R-08 (PlantUML pilot) |
| T-022..T-099 | Etapa 4 | R-03 (effort por chunks) |
| T-101..T-113 | Etapa 5 | R-06 (build break en index) |
| T-114, T-115 | Etapa 6 | (audit) |

## Métricas de progreso

| Etapa | Tasks | Estado |
|---|---|---|
| 1 | 17 | pending |
| 2 | 5 | pending |
| 3 | 9 (incluye SP-02) | pending |
| 4 | ~91 (78 tasks + ~13 vals/coms) | pending |
| 5 | 15 | pending |
| 6 | 4 | pending |
| **TOTAL** | **~141 tasks** | 0% |

## Próximo paso

Phase 10 EXECUTE — ejecutar T-001 (primera clase domain-model: AuthorizationGuard) tras
gate humano de Phase 8 → 10.

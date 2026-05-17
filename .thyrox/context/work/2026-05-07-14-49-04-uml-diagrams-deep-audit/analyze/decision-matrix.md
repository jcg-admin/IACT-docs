```yml
created_at: 2026-05-07 19:39:28
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-004 Consolidated Decision Matrix
```

# T-004 — Matriz consolidada de decisiones

> Consolida T-001 (inventario), T-002 (cobertura DM),
> T-003 (UML-07 scoring) en una matriz unica por archivo
> con: clase, ejes faltantes, dependencias de clases nuevas,
> y orden de ejecucion sugerido.

## 1. Reclasificacion de identificadores MISSING

Tras revisar T-002, los siguientes identificadores que aparecieron
como MISSING son **falsos positivos** (aliases STD-010, genericos,
siglas) y se reclasifican a NOT_CLASS:

- `Almacen` — generico/alias/sigla (no requiere stub)
- `Base` — generico/alias/sigla (no requiere stub)
- `FTS` — generico/alias/sigla (no requiere stub)
- `Interfaz` — generico/alias/sigla (no requiere stub)
- `RBACRepo` — generico/alias/sigla (no requiere stub)
- `Servicio` — generico/alias/sigla (no requiere stub)
- `Storage` — generico/alias/sigla (no requiere stub)
- `TSDB` — generico/alias/sigla (no requiere stub)
- `pipeline_runs` — generico/alias/sigla (no requiere stub)

**Identificadores realmente MISSING (candidatos a clase nueva): 22**

| # | Identificador | Candidato kebab-case |
|---|---|---|
| 1 | `AlertHistoryService` | alert-history-service, alerthistoryservice |
| 2 | `AlertHistorySummary` | alert-history-summary, alerthistorysummary |
| 3 | `AlertRuleRepo` | alert-rule-repo, alertrulerepo |
| 4 | `CampaignDailyStatRepo` | campaign-daily-stat-repo, campaigndailystatrepo |
| 5 | `CampaignReportService` | campaignreportservice, campaign-report-service |
| 6 | `DisparadorETL` | disparadoretl, disparador-e-t-l |
| 7 | `ErroresETLService` | errores-e-t-l-service, erroresetlservice |
| 8 | `FunctionGroupMembership` | function-group-membership, functiongroupmembership |
| 9 | `GeneralAuditService` | general-audit-service, generalauditservice |
| 10 | `HmacVerifier` | hmacverifier, hmac-verifier |
| 11 | `ImpactReport` | impact-report, impactreport |
| 12 | `InfraLogStore` | infralogstore, infra-log-store |
| 13 | `KPICalculator` | k-p-i-calculator, kpicalculator |
| 14 | `LogStore` | logstore, log-store |
| 15 | `MenuIVRReportService` | menu-i-v-r-report-service, menuivrreportservice |
| 16 | `ResumenSalud` | resumen-salud, resumensalud |
| 17 | `ResumenSaludBuilder` | resumensaludbuilder, resumen-salud-builder |
| 18 | `SegmentChangeListener` | segmentchangelistener, segment-change-listener |
| 19 | `SegmentScope` | segment-scope, segmentscope |
| 20 | `SubscriptionRepo` | subscriptionrepo, subscription-repo |
| 21 | `SupervisionETLService` | supervision-e-t-l-service, supervisionetlservice |
| 22 | `UserAccessGroupAssignment` | user-access-group-assignment, useraccessgroupassignment |

## 2. Distribucion final A/B/C

| Clase | Archivos | Accion |
|---|---|---|
| **A** | 53 | Verificar (con re-eval semantica vs flujo-principal) |
| **B** | 39 | Complementar (anadir ejes faltantes) |
| **C** | 0 | Recrear desde cero |
| **Total** | 92 | |

## 3. Dependencias archivo -> clases nuevas

**20 archivos** referencian al menos una clase
nueva (TRUE_MISSING). Estos archivos NO pueden complementarse hasta
que la clase exista en domain-model (T-CLASS antes que T-COMPLEMENT).

| # | Archivo | Clase | Deps en clases nuevas |
|---|---|---|---|
| 1 | `requisitos/casos-uso/access/uc-acc-04/diagramas-uml/diagrama-de-agr-como-agregacion.rst` | **A** | `FunctionGroupMembership`, `UserAccessGroupAssignment` |
| 2 | `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-impacto.rst` | **A** | `ImpactReport` |
| 3 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst` | **A** | `AlertRuleRepo` |
| 4 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-clases.rst` | **A** | `AlertHistoryService`, `AlertHistorySummary` |
| 5 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-clases.rst` | **A** | `SegmentChangeListener`, `SubscriptionRepo` |
| 6 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst` | **A** | `GeneralAuditService` |
| 7 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-secuencia-verify.rst` | **B** | `HmacVerifier` |
| 8 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-pipeline.rst` | **A** | `LogStore` |
| 9 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-tail-sse.rst` | **A** | `LogStore` |
| 10 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-componentes-export.rst` | **A** | `LogStore` |
| 11 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-secuencia-exportacion-logs.rst` | **B** | `LogStore` |
| 12 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-pipeline-infraestructura.rst` | **A** | `InfraLogStore` |
| 13 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-secuencia-tail-sse.rst` | **B** | `InfraLogStore` |
| 14 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst` | **A** | `ResumenSalud`, `ResumenSaludBuilder`, `SupervisionETLService` |
| 15 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst` | **A** | `ErroresETLService` |
| 16 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-secuencia.rst` | **B** | `DisparadorETL` |
| 17 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-clases.rst` | **A** | `SegmentScope` |
| 18 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-clases.rst` | **A** | `KPICalculator` |
| 19 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-clases.rst` | **A** | `CampaignDailyStatRepo`, `CampaignReportService`, `KPICalculator` |
| 20 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-clases.rst` | **A** | `MenuIVRReportService` |

## 4. Orden T-COMPLEMENT (cluster por riesgo)

Decision del ejecutor: cluster reports primero (mas superficial,
16 complementos), luego logs (11), luego resto alfabetico.

**39 archivos** en orden de procesamiento:

| Orden | Archivo | Cluster | Tipo | Ejes faltantes | Deps clases nuevas |
|---|---|---|---|---|---|
| 1 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 2 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso-relacion-de-inclusion.rst` | reports | caso-de-uso-relacion | extension, generalizacion, comprension_dominio | — |
| 3 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-actividad-crear.rst` | reports | otro(actividad-crear) | comprension_dominio | — |
| 4 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-aplicar.rst` | reports | otro(actividad-aplicar) | comprension_dominio | — |
| 5 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-compartir.rst` | reports | otro(actividad-compartir) | comprension_dominio | — |
| 6 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 7 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-secuencia-detalle.rst` | reports | otro(secuencia-detalle) | comprension_dominio | — |
| 8 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 9 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-secuencia.rst` | reports | secuencia | comprension_dominio | — |
| 10 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 11 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-secuencia.rst` | reports | secuencia | comprension_dominio | — |
| 12 | `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 13 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 14 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-distribucion-de-menus.rst` | reports | otro(distribucion-de-menus) | comprension_dominio | — |
| 15 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-actividad.rst` | reports | actividad | comprension_dominio | — |
| 16 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-flujo-de-anonimizacion-etl.rst` | reports | otro(flujo-de-anonimizacion-etl) | comprension_dominio | — |
| 17 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 18 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 19 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-secuencia-pipeline-log.rst` | logs | otro(secuencia-pipeline-log) | comprension_dominio | — |
| 20 | `requisitos/casos-uso/logs/uc-log-03/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 21 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 22 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-secuencia-exportacion-logs.rst` | logs | otro(secuencia-exportacion-logs) | comprension_dominio | `LogStore` |
| 23 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 24 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-secuencia-tail-sse.rst` | logs | otro(secuencia-tail-sse) | comprension_dominio | `InfraLogStore` |
| 25 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 26 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-componentes.rst` | logs | componentes | panorama | — |
| 27 | `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-actividad.rst` | logs | actividad | comprension_dominio | — |
| 28 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-actividad.rst` | audit | actividad | comprension_dominio | — |
| 29 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-actividad.rst` | audit | actividad | comprension_dominio | — |
| 30 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-flujo-de-firma.rst` | audit | otro(flujo-de-firma) | comprension_dominio | — |
| 31 | `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-secuencia-verify.rst` | audit | otro(secuencia-verify) | comprension_dominio | `HmacVerifier` |
| 32 | `requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-estados-exceptionalpermission.rst` | permissions | estados | comprension_dominio | — |
| 33 | `requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-estados-accessgroup.rst` | permissions | estados | comprension_dominio | — |
| 34 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst` | pipeline | actividad | comprension_dominio | — |
| 35 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-actividad.rst` | pipeline | actividad | comprension_dominio | — |
| 36 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-actividad.rst` | pipeline | actividad | comprension_dominio | — |
| 37 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-componentes.rst` | pipeline | componentes | panorama | — |
| 38 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-actividad.rst` | pipeline | actividad | comprension_dominio | — |
| 39 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-secuencia.rst` | pipeline | secuencia | comprension_dominio | `DisparadorETL` |

## 5. Orden T-VERIFY (cluster por riesgo)

Decision del ejecutor: re-evaluacion semantica archivo por archivo
contra `flujo-principal.rst` del UC. Criterio binario: el diagrama
refleja fielmente el flujo? Si si -> queda A. Si no -> reclasifica a B.

**53 archivos** en orden de procesamiento:

| Orden | Archivo | Cluster | Tipo | Score | Deps clases nuevas |
|---|---|---|---|---|---|
| 1 | `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | `SegmentScope` |
| 2 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | — |
| 3 | `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-estados-saved-view.rst` | reports | estados | 2/2 | — |
| 4 | `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-estados-share.rst` | reports | estados | 2/2 | — |
| 5 | `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | `KPICalculator` |
| 6 | `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | — |
| 7 | `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | `CampaignDailyStatRepo`, `CampaignReportService`, `KPICalculator` |
| 8 | `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | — |
| 9 | `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | `MenuIVRReportService` |
| 10 | `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-clases.rst` | reports | clases | 2/2 | — |
| 11 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-pipeline.rst` | logs | otro(pipeline) | 2/2 | `LogStore` |
| 12 | `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-tail-sse.rst` | logs | otro(tail-sse) | 2/2 | `LogStore` |
| 13 | `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-componentes-pipeline-log.rst` | logs | otro(componentes-pipeline-log) | 2/2 | — |
| 14 | `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-componentes-export.rst` | logs | otro(componentes-export) | 2/2 | `LogStore` |
| 15 | `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-pipeline-infraestructura.rst` | logs | otro(pipeline-infraestructura) | 2/2 | `InfraLogStore` |
| 16 | `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-estados-overall.rst` | logs | estados | 2/2 | — |
| 17 | `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-pipeline-metricas.rst` | logs | otro(pipeline-metricas) | 2/2 | — |
| 18 | `requisitos/casos-uso/access/uc-acc-04/diagramas-uml/diagrama-de-agr-como-agregacion.rst` | access | otro(agr-como-agregacion) | 2/2 | `FunctionGroupMembership`, `UserAccessGroupAssignment` |
| 19 | `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-actividad.rst` | admin | actividad | 2/2 | — |
| 20 | `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst` | admin | estados | 2/2 | — |
| 21 | `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-actividad.rst` | admin | actividad | 2/2 | — |
| 22 | `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-estados-funcion.rst` | admin | estados | 2/2 | — |
| 23 | `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-actividad.rst` | admin | actividad | 2/2 | — |
| 24 | `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-impacto.rst` | admin | otro(impacto) | 2/2 | `ImpactReport` |
| 25 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-actividad.rst` | alerts | actividad | 2/2 | — |
| 26 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst` | alerts | clases | 2/2 | `AlertRuleRepo` |
| 27 | `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-estados-regla.rst` | alerts | estados | 2/2 | — |
| 28 | `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-actividad.rst` | alerts | actividad | 2/2 | — |
| 29 | `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-estados-alerta.rst` | alerts | estados | 2/2 | — |
| 30 | `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-secuencia.rst` | alerts | secuencia | 2/2 | — |
| 31 | `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-actividad.rst` | alerts | actividad | 2/2 | — |
| 32 | `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-estados-transicion.rst` | alerts | estados | 2/2 | — |
| 33 | `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-secuencia.rst` | alerts | secuencia | 2/2 | — |
| 34 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-actividad.rst` | alerts | actividad | 2/2 | — |
| 35 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-clases.rst` | alerts | clases | 2/2 | `AlertHistoryService`, `AlertHistorySummary` |
| 36 | `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-secuencia.rst` | alerts | secuencia | 2/2 | — |
| 37 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-actividad.rst` | alerts | actividad | 2/2 | — |
| 38 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-clases.rst` | alerts | clases | 2/2 | `SegmentChangeListener`, `SubscriptionRepo` |
| 39 | `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-estados-subscription.rst` | alerts | estados | 2/2 | — |
| 40 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-actividad.rst` | audit | actividad | 2/2 | — |
| 41 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst` | audit | clases | 2/2 | `GeneralAuditService` |
| 42 | `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-secuencia.rst` | audit | secuencia | 2/2 | — |
| 43 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-componentes-fts.rst` | audit | otro(componentes-fts) | 2/2 | — |
| 44 | `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-secuencia.rst` | audit | secuencia | 2/2 | — |
| 45 | `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-actividad.rst` | audit | actividad | 2/2 | — |
| 46 | `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-estados-export-job.rst` | audit | estados | 2/2 | — |
| 47 | `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-secuencia.rst` | audit | secuencia | 2/2 | — |
| 48 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst` | pipeline | clases | 2/2 | `ResumenSalud`, `ResumenSaludBuilder`, `SupervisionETLService` |
| 49 | `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-estados-ejecucion-etl.rst` | pipeline | estados | 2/2 | — |
| 50 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst` | pipeline | clases | 2/2 | `ErroresETLService` |
| 51 | `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-secuencia.rst` | pipeline | secuencia | 2/2 | — |
| 52 | `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-estados-frescura-datos.rst` | pipeline | estados | 2/2 | — |
| 53 | `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-estados-reintento.rst` | pipeline | estados | 2/2 | — |

## 6. Resumen ejecutivo del esfuerzo

| Bloque | Cantidad | Estimacion |
|---|---|---|
| T-CLASS (clases nuevas en DM) | 22 | 15-30 min/clase = 5-10 h |
| T-COMPLEMENT (clase B) | 39 | 15-25 min/archivo = 10-16 h |
| T-VERIFY semantico (clase A) | 53 | 5-10 min/archivo = 4-9 h |
| T-RECREATE (clase C) | 0 | — |
| TRACK (cierre WP) | 4 tareas | 1-2 h |
| **Total tareas atomicas** | **~118** | **~20-37 h** |

## 7. Proximos pasos

- T-005: catalogo detallado de las clases nuevas con sus stubs.
- T-006: patrones UML-07 obligatorios por categoria de UC.
- T-007: DAG con orden total (T-CLASS -> T-COMPLEMENT -> T-VERIFY).
- T-008: task-plan ejecutable con T-NNN secuenciados.

## Refs

- T-001: `discover/inventory-recreated-files.md`
- T-002: `analyze/coverage/domain-model-coverage.md`
- T-003: `analyze/uml07-conformance/uml07-scoring.md`

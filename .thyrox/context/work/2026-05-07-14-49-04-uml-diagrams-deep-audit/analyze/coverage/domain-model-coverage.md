```yml
created_at: 2026-05-07 15:52:40
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 3 — ANALYZE
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-002 Coverage Audit
```

# T-002 — Auditoría de cobertura domain-model + cross-refs

> Verificación mecánica de:
> 1. Cada identificador UML del inventario T-001 contra
>    `source/arquitectura-tecnica/domain-model/*.rst`.
> 2. Cada `:doc:` ref de los 92 archivos contra el filesystem.

## 1. Resumen

- Identificadores UML únicos analizados: **55**
- Clases existentes en domain-model: **88**
- Identificadores categorizados como NOT_CLASS (actor/alias/genérico): **2**
- Identificadores con clase EXISTS en domain-model: **22**
- Identificadores **MISSING** en domain-model (candidatos a stub): **31**

- Cross-refs `:doc:` totales auditados: **214**
- Cross-refs **rotos**: **0**

## 2. Identificadores UML — clasificación

| Identificador UML | #Apariciones | Status | Match / Candidatos |
|---|---|---|---|
| `Servicio` | 17 | **MISSING** | servicio |
| `AuditService` | 8 | **EXISTS** | audit-service |
| `SegmentResolver` | 6 | **EXISTS** | segment-resolver |
| `AlertRepo` | 4 | **EXISTS** | alert-repo |
| `LogStore` | 4 | **MISSING** | logstore, log-store |
| `PipelineExecutionRepo` | 4 | **EXISTS** | pipeline-execution-repo |
| `Interfaz` | 3 | **MISSING** | interfaz |
| `AuditRepo` | 3 | **EXISTS** | audit-repo |
| `PiiScanner` | 3 | **EXISTS** | pii-scanner |
| `Base` | 3 | **MISSING** | base |
| `EvaluatorReloader` | 2 | **EXISTS** | evaluator-reloader |
| `TimingCalculator` | 2 | **EXISTS** | timing-calculator |
| `CursorEncoder` | 2 | **EXISTS** | cursor-encoder |
| `ExportWorker` | 2 | **NOT_CLASS** | actor/alias/genérico |
| `InternalMailbox` | 2 | **NOT_CLASS** | actor/alias/genérico |
| `pipeline_runs` | 2 | **MISSING** | pipeline_runs |
| `InfraLogStore` | 2 | **MISSING** | infralogstore, infra-log-store |
| `AgentReportService` | 2 | **EXISTS** | agent-report-service |
| `KPICalculator` | 2 | **MISSING** | k-p-i-calculator, kpicalculator |
| `AccessGroup` | 1 | **EXISTS** | access-group |
| `Function` | 1 | **EXISTS** | function |
| `FunctionGroupMembership` | 1 | **MISSING** | function-group-membership, functiongroupmembership |
| `User` | 1 | **EXISTS** | user |
| `UserAccessGroupAssignment` | 1 | **MISSING** | user-access-group-assignment, useraccessgroupassignment |
| `Almacen` | 1 | **MISSING** | almacen |
| `ImpactReport` | 1 | **MISSING** | impact-report, impactreport |
| `AlertRule` | 1 | **EXISTS** | alert-rule |
| `AlertRuleRepo` | 1 | **MISSING** | alert-rule-repo, alertrulerepo |
| `RuleValidator` | 1 | **EXISTS** | rule-validator |
| `AlertHistoryService` | 1 | **MISSING** | alert-history-service, alerthistoryservice |
| `AlertHistorySummary` | 1 | **MISSING** | alert-history-summary, alerthistorysummary |
| `SegmentChangeListener` | 1 | **MISSING** | segmentchangelistener, segment-change-listener |
| `Subscription` | 1 | **EXISTS** | subscription |
| `SubscriptionRepo` | 1 | **MISSING** | subscriptionrepo, subscription-repo |
| `GeneralAuditService` | 1 | **MISSING** | general-audit-service, generalauditservice |
| `FTS` | 1 | **MISSING** | f-t-s, fts |
| `HmacVerifier` | 1 | **MISSING** | hmacverifier, hmac-verifier |
| `Storage` | 1 | **MISSING** | storage |
| `TSDB` | 1 | **MISSING** | tsdb, t-s-d-b |
| `ResumenSalud` | 1 | **MISSING** | resumen-salud, resumensalud |
| `ResumenSaludBuilder` | 1 | **MISSING** | resumensaludbuilder, resumen-salud-builder |
| `SupervisionETLService` | 1 | **MISSING** | supervision-e-t-l-service, supervisionetlservice |
| `ErroresETLService` | 1 | **MISSING** | errores-e-t-l-service, erroresetlservice |
| `DisparadorETL` | 1 | **MISSING** | disparadoretl, disparador-e-t-l |
| `RBACRepo` | 1 | **MISSING** | r-b-a-c-repo, rbacrepo |
| `SegmentScope` | 1 | **MISSING** | segment-scope, segmentscope |
| `ColumnCatalog` | 1 | **EXISTS** | column-catalog |
| `SavedView` | 1 | **EXISTS** | saved-view |
| `AgentDailyStatRepo` | 1 | **EXISTS** | agent-daily-stat-repo |
| `AbandonmentReportService` | 1 | **EXISTS** | abandonment-report-service |
| `CampaignDailyStatRepo` | 1 | **MISSING** | campaign-daily-stat-repo, campaigndailystatrepo |
| `CampaignReportService` | 1 | **MISSING** | campaignreportservice, campaign-report-service |
| `TransferReportService` | 1 | **EXISTS** | transfer-report-service |
| `MenuIVRReportService` | 1 | **MISSING** | menu-i-v-r-report-service, menuivrreportservice |
| `CallerReportService` | 1 | **EXISTS** | caller-report-service |

## 3. Identificadores MISSING — candidatos a clase nueva en domain-model (31)

> Cada uno requiere decisión en T-005:
> (a) crear stub en domain-model, (b) reclasificar a NOT_CLASS
> (es alias/actor genérico), (c) renombrar al canónico ya existente.

| # | Identificador | #Apariciones | Candidatos kebab-case probados |
|---|---|---|---|
| 1 | `Servicio` | 17 | servicio |
| 2 | `LogStore` | 4 | logstore, log-store |
| 3 | `Interfaz` | 3 | interfaz |
| 4 | `Base` | 3 | base |
| 5 | `pipeline_runs` | 2 | pipeline_runs |
| 6 | `InfraLogStore` | 2 | infralogstore, infra-log-store |
| 7 | `KPICalculator` | 2 | k-p-i-calculator, kpicalculator |
| 8 | `FunctionGroupMembership` | 1 | function-group-membership, functiongroupmembership |
| 9 | `UserAccessGroupAssignment` | 1 | user-access-group-assignment, useraccessgroupassignment |
| 10 | `Almacen` | 1 | almacen |
| 11 | `ImpactReport` | 1 | impact-report, impactreport |
| 12 | `AlertRuleRepo` | 1 | alert-rule-repo, alertrulerepo |
| 13 | `AlertHistoryService` | 1 | alert-history-service, alerthistoryservice |
| 14 | `AlertHistorySummary` | 1 | alert-history-summary, alerthistorysummary |
| 15 | `SegmentChangeListener` | 1 | segmentchangelistener, segment-change-listener |
| 16 | `SubscriptionRepo` | 1 | subscriptionrepo, subscription-repo |
| 17 | `GeneralAuditService` | 1 | general-audit-service, generalauditservice |
| 18 | `FTS` | 1 | f-t-s, fts |
| 19 | `HmacVerifier` | 1 | hmacverifier, hmac-verifier |
| 20 | `Storage` | 1 | storage |
| 21 | `TSDB` | 1 | tsdb, t-s-d-b |
| 22 | `ResumenSalud` | 1 | resumen-salud, resumensalud |
| 23 | `ResumenSaludBuilder` | 1 | resumensaludbuilder, resumen-salud-builder |
| 24 | `SupervisionETLService` | 1 | supervision-e-t-l-service, supervisionetlservice |
| 25 | `ErroresETLService` | 1 | errores-e-t-l-service, erroresetlservice |
| 26 | `DisparadorETL` | 1 | disparadoretl, disparador-e-t-l |
| 27 | `RBACRepo` | 1 | r-b-a-c-repo, rbacrepo |
| 28 | `SegmentScope` | 1 | segment-scope, segmentscope |
| 29 | `CampaignDailyStatRepo` | 1 | campaign-daily-stat-repo, campaigndailystatrepo |
| 30 | `CampaignReportService` | 1 | campaignreportservice, campaign-report-service |
| 31 | `MenuIVRReportService` | 1 | menu-i-v-r-report-service, menuivrreportservice |

## 4. Cross-refs `:doc:` rotos

Ningún cross-ref roto detectado.

## 5. Archivos con cross-refs rotos (0)

## 6. Catálogo completo de domain-model existente

**88 clases** en `source/arquitectura-tecnica/domain-model/`:

- `abandonment-report-service`
- `access-group`
- `access-group-function`
- `access-group-repo`
- `action`
- `agent-daily-stat-repo`
- `agent-report-service`
- `alert`
- `alert-hook`
- `alert-repo`
- `alert-rule`
- `application-log`
- `assignment`
- `assignment-repo`
- `audit-event`
- `audit-query-service`
- `audit-repo`
- `audit-service`
- `audit-validator`
- `authorization-guard`
- `base-report-service`
- `blacklisted-token`
- `bucket`
- `call`
- `caller-report-service`
- `campaign`
- `column-catalog`
- `comparative`
- `cursor-encoder`
- `effective-permissions-aggregator`
- `evaluator-reloader`
- `exceptional-permission`
- `exceptional-permission-repo`
- `expiration-policy`
- `export-job`
- `export-worker`
- `filter-validator`
- `function`
- `function-group`
- `function-group-repo`
- `function-repo`
- `historical-report`
- `idempotency-policy`
- `infrastructure-log`
- `internal-mailbox`
- `internal-message`
- `ivr-navigation-report-service`
- `kpi-calculator`
- `menu`
- `menu-item`
- `menu-item-repo`
- `menu-lifecycle-service`
- `metric`
- `metrics-cache`
- `nav-domain`
- `overview`
- `password-generator`
- `permission-cache`
- `permission-service`
- `pii-scanner`
- `pipeline-execution`
- `pipeline-execution-repo`
- `pipeline-log`
- `rbac-repo`
- `report`
- `rule-validator`
- `sanitizer`
- `saved-filter`
- `saved-view`
- `scheduled-report`
- `scheduled-report-list-service`
- `scheduled-report-repo`
- `section`
- `segment-resolver`
- `separation-rule`
- `separation-rule-repo`
- `session`
- `specification-pattern`
- `strategy-pattern`
- `subscription`
- `system-health`
- `technical-metric`
- `threshold`
- `timing-calculator`
- `transfer-report-service`
- `user`
- `user-capability-resolver`
- `user-repo`

## Refs

- T-001: `discover/inventory-recreated-files.md`
- T-005 (siguiente): catálogo de stubs de clase a crear
- Domain-model: `source/arquitectura-tecnica/domain-model/`

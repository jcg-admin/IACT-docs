```yml
created_at: 2026-05-07 16:00:00
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-005 New Classes Catalog
```

# T-005 — Catalogo de clases nuevas en domain-model

> Catalogo detallado de las clases que requieren stub en
> `source/arquitectura-tecnica/domain-model/`. Cada entrada
> incluye: archivo a crear, UCs consumidores, proposito,
> atributos minimos, metodos, relaciones.

## 1. Reclasificaciones tras lectura mas profunda

Tras leer los diagramas-de-clases consumidores y verificar
manualmente el catalogo domain-model, se reclasifican los
siguientes identificadores que aparecian como MISSING en T-002:

### EXISTS (mover a "ya cubierto")

| Identificador UML | Domain-model existente | Razon |
|---|---|---|
| `KPICalculator` | `kpi-calculator.rst` | Heuristica camel-to-kebab fallaba con siglas (KPI -> k-p-i en lugar de kpi). Existe. |
| `RBACRepo` | `rbac-repo.rst` | Mismo problema con sigla RBAC. Existe. |

### ALIAS_MISMATCH (no requiere stub, pero el archivo consumidor debe corregirse)

| Identificador UML | Domain-model real | Accion en T-COMPLEMENT |
|---|---|---|
| `MenuIVRReportService` | `ivr-navigation-report-service.rst` | Renombrar alias UML a `IVRNavigationReportService` o anadir alias en el archivo del DM. |

## 2. Clases nuevas confirmadas (20)

| # | Nombre clase | Archivo a crear | UCs consumidores |
|---|---|---|---|
| 1 | `AlertHistoryService` | `alert-history-service.rst` | uc-alr-04 |
| 2 | `AlertHistorySummary` | `alert-history-summary.rst` | uc-alr-04 |
| 3 | `AlertRuleRepo` | `alert-rule-repo.rst` | uc-alr-01 |
| 4 | `CampaignDailyStatRepo` | `campaign-daily-stat-repo.rst` | uc-rpt-14 |
| 5 | `CampaignReportService` | `campaign-report-service.rst` | uc-rpt-14 |
| 6 | `DisparadorETL` | `disparador-etl.rst` | uc-pip-04 |
| 7 | `ErroresETLService` | `errores-etl-service.rst` | uc-pip-02 |
| 8 | `FunctionGroupMembership` | `function-group-membership.rst` | uc-acc-04 |
| 9 | `GeneralAuditService` | `general-audit-service.rst` | uc-aud-01 |
| 10 | `HmacVerifier` | `hmac-verifier.rst` | uc-aud-04 |
| 11 | `ImpactReport` | `impact-report.rst` | uc-adm-03 |
| 12 | `InfraLogStore` | `infra-log-store.rst` | uc-log-05 |
| 13 | `LogStore` | `log-store.rst` | uc-log-01, uc-log-04 |
| 14 | `ResumenSalud` | `resumen-salud.rst` | uc-pip-01 |
| 15 | `ResumenSaludBuilder` | `resumen-salud-builder.rst` | uc-pip-01 |
| 16 | `SegmentChangeListener` | `segment-change-listener.rst` | uc-alr-05 |
| 17 | `SegmentScope` | `segment-scope.rst` | uc-inc-rpt-01 |
| 18 | `SubscriptionRepo` | `subscription-repo.rst` | uc-alr-05 |
| 19 | `SupervisionETLService` | `supervision-etl-service.rst` | uc-pip-01 |
| 20 | `UserAccessGroupAssignment` | `user-access-group-assignment.rst` | uc-acc-04 |

## 3. Stubs detallados

### 3.1 `alert-history-service.rst`

- **Proposito:** Servicio de aplicacion que consulta el historial
  de alertas disparadas, agregando por regla, severidad y rango
  temporal. Distinto de `alert-service` (gestion de reglas).
- **Atributos:** ninguno (servicio sin estado).
- **Metodos:**
  - `get_history(filters, range) : list[AlertEvent]`
  - `summarize(range) : AlertHistorySummary`
- **Relaciones:**
  - `AlertHistoryService --> AlertRepo : queries`
  - `AlertHistoryService --> AuditService : emits read event`
- **UC consumidor:** uc-alr-04.

### 3.2 `alert-history-summary.rst`

- **Proposito:** DTO/Value Object que agrega contadores de
  alertas por severidad y regla en un rango temporal.
- **Atributos:**
  - `range: TemporalRange`
  - `total: int`
  - `by_severity: dict[str, int]`
  - `by_rule: dict[str, int]`
- **Metodos:** ninguno (inmutable).
- **Relaciones:** producido por `AlertHistoryService`.

### 3.3 `alert-rule-repo.rst`

- **Proposito:** Repository especifico para AlertRule. Existe
  `alert-repo` (alertas disparadas) y `alert-rule` (entidad regla),
  pero falta el repo de AlertRule.
- **Atributos:** ninguno.
- **Metodos:**
  - `get(id) : AlertRule`
  - `list_active() : list[AlertRule]`
  - `save(rule) : None`
- **Relaciones:** maneja entidad `AlertRule`.

### 3.4 `campaign-daily-stat-repo.rst`

- **Proposito:** Repository de estadisticas diarias por campaign,
  paralelo a `agent-daily-stat-repo`.
- **Atributos:** ninguno.
- **Metodos:**
  - `aggregate(campaign_id, range) : list[DailyStat]`
  - `top_n(range, n) : list[DailyStat]`
- **Relaciones:** maneja entidad agregada `Campaign × dia`.

### 3.5 `campaign-report-service.rst`

- **Proposito:** Servicio de aplicacion que genera reportes de
  performance de campaigns (asistencia, conversion, etc.).
- **Metodos:**
  - `generate(campaign_id, range, vista) : CampaignReport`
- **Relaciones:**
  - `--> CampaignDailyStatRepo : queries`
  - `--> KPICalculator : computes metrics`
  - `--> SegmentResolver : filters by audience`

### 3.6 `disparador-etl.rst`

- **Proposito:** Trigger interno del pipeline ETL de supervision.
  Vocabulario STD-010 (canonico en lugar de "Trigger" tecnico).
- **Atributos:**
  - `cron: str` (expresion programada)
  - `scope: ETLScope`
- **Metodos:**
  - `trigger() : ETLRun`

### 3.7 `errores-etl-service.rst`

- **Proposito:** Servicio que captura, persiste y consulta errores
  ocurridos durante runs ETL del pipeline de supervision.
- **Metodos:**
  - `record(run_id, error)`
  - `query(filters) : list[ETLError]`

### 3.8 `function-group-membership.rst`

- **Proposito:** Tabla intermedia M:N entre `Function` y
  `FunctionGroup`, parte del catalogo RBAC v5.6.x. Equivalente a
  `assignment` para el otro extremo del modelo.
- **Atributos:**
  - `function_id: FK`
  - `function_group_id: FK`
  - `role: str` (owner/member)
- **Metodos:** ninguno (entidad pura).
- **Relaciones:**
  - `--> Function`
  - `--> FunctionGroup`

### 3.9 `general-audit-service.rst`

- **Proposito:** Servicio que provee consulta general de audit
  events con paginacion cursor + sanitizacion PII. Distinto de
  `audit-query-service` (filtrado especifico) y `audit-service`
  (escritura).
- **Metodos:**
  - `query(filters, cursor) : AuditQueryResult`
- **Relaciones:**
  - `--> AuditRepo : queries`
  - `--> CursorEncoder : paginates`
  - `--> PiiScanner : sanitizes`
  - `--> AuditService : emits meta-audit`

### 3.10 `hmac-verifier.rst`

- **Proposito:** Verificador HMAC para integridad de cadenas de
  audit log (chain hashing). Usado en uc-aud-04.
- **Metodos:**
  - `verify(event_id) : VerifyResult`
  - `verify_chain(from_id, to_id) : ChainVerifyResult`

### 3.11 `impact-report.rst`

- **Proposito:** Reporte de impacto generado en uc-adm-03 al
  modificar una FunctionGroup. Lista las funciones afectadas y
  los users que perderian acceso.
- **Atributos:**
  - `function_group_id: FK`
  - `affected_functions: list[FK]`
  - `affected_users_count: int`
- **Metodos:** ninguno (DTO).

### 3.12 `infra-log-store.rst`

- **Proposito:** Almacen de logs de infraestructura (procesos
  internos: workers, schedulers, healthchecks). Distinto de
  `log-store` (logs de aplicacion) y `infrastructure-log` (entidad).
- **Metodos:**
  - `append(infra_log)`
  - `tail(filters, limit) : list[InfrastructureLog]`

### 3.13 `log-store.rst`

- **Proposito:** Almacen append-only de logs de aplicacion.
  Abstrae la persistencia (TSDB, Storage) sin acoplarse a una
  tecnologia concreta.
- **Metodos:**
  - `append(log_entry)`
  - `query(filters, range, cursor) : list[ApplicationLog]`
  - `tail_sse(filters) : Stream[ApplicationLog]`

### 3.14 `resumen-salud.rst`

- **Proposito:** DTO que agrega el estado de salud del pipeline:
  runs activos, errores, lag, ultimo exito. Vocabulario STD-010.
- **Atributos:**
  - `runs_activos: int`
  - `errores_recientes: int`
  - `lag_segundos: int`
  - `ultimo_exito: datetime`
  - `estado: HealthStatus` (verde/amarillo/rojo)

### 3.15 `resumen-salud-builder.rst`

- **Proposito:** Builder que ensambla un `ResumenSalud` consultando
  varias fuentes (pipeline-runs, agent-stats, etc.).
- **Metodos:**
  - `build() : ResumenSalud`

### 3.16 `segment-change-listener.rst`

- **Proposito:** Listener de eventos de cambio en `SegmentScope`
  (alta/baja/modificacion de un segmento). Re-evalua suscripciones
  de alerta afectadas.
- **Metodos:**
  - `on_segment_change(event)`

### 3.17 `segment-scope.rst`

- **Proposito:** Value Object que representa el alcance de un
  segmento (queue/skill/depto). Distinto de `segment-resolver`
  (servicio).
- **Atributos:**
  - `kind: str` (queue/skill/dept/all)
  - `ref: str` (id del recurso)

### 3.18 `subscription-repo.rst`

- **Proposito:** Repository de `Subscription` (entidad existente).
- **Metodos:**
  - `get(id) : Subscription`
  - `list_for_user(user_id) : list[Subscription]`
  - `list_for_segment(segment_id) : list[Subscription]`

### 3.19 `supervision-etl-service.rst`

- **Proposito:** Servicio principal del pipeline ETL de supervision.
  Coordina extraccion, transformacion y carga del estado de los
  pipelines monitoreados.
- **Metodos:**
  - `run() : ETLRun`
  - `get_state() : ResumenSalud`
- **Relaciones:**
  - `--> DisparadorETL`
  - `--> ResumenSaludBuilder`
  - `--> ErroresETLService`

### 3.20 `user-access-group-assignment.rst`

- **Proposito:** Tabla intermedia M:N entre `User` y `AccessGroup`,
  parte del catalogo RBAC v5.6.x. Es el lado complementario de
  `function-group-membership`.
- **Atributos:**
  - `user_id: FK`
  - `access_group_id: FK`
  - `assigned_at: datetime`
- **Relaciones:**
  - `--> User`
  - `--> AccessGroup`

## 4. Plantilla minima de stub

Cada T-CLASS-* sigue esta plantilla:

```rst
.. _domain-model-{kebab-name}:

{Nombre Clase} ({tipo})
=======================

.. meta::
 :artefacto: DM_{NOMBRE}
 :tipo: Domain Model — {Servicio|Entidad|Repository|DTO}
 :dominio: arquitectura_tecnica
 :estado: Borrador
 :version: 1.0.0

Proposito
---------

{2-3 lineas describiendo el rol de la clase en el dominio}.

.. uml::
 :caption: {Nombre Clase}.

 @startuml
 class {NombreClase} {
   + metodo_1(param) : ReturnType
   + metodo_2() : ReturnType
 }
 @enduml

Atributos
---------

- {atributo}: tipo — descripcion.

Metodos
-------

- {metodo}: param -> return — descripcion.

Relaciones
----------

- ``-->`` {OtraClase} — naturaleza relacion.

Consumidores
------------

- :doc:`/requisitos/casos-uso/{cluster}/{uc}/index`.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/{clase-relacionada}`.
```

## 5. Estimacion de esfuerzo T-CLASS

- 20 clases nuevas × ~15-20 min/clase = 5-7 h.
- Riesgo: clases con relaciones cruzadas (ResumenSalud +
  ResumenSaludBuilder + SupervisionETLService) requieren
  coordinacion en orden de creacion.

## 6. Orden sugerido de creacion T-CLASS

Por dependencia interna (clases base antes que servicios que las
referencian):

1. **Sin dependencias internas** (10): AlertRuleRepo,
   CampaignDailyStatRepo, FunctionGroupMembership, HmacVerifier,
   ImpactReport, SegmentScope, SubscriptionRepo,
   UserAccessGroupAssignment, AlertHistorySummary, DisparadorETL.
2. **Servicios dependientes** (10): AlertHistoryService (usa
   AlertHistorySummary), CampaignReportService (usa
   CampaignDailyStatRepo), GeneralAuditService, ErroresETLService,
   ResumenSalud, ResumenSaludBuilder (usa ResumenSalud),
   SegmentChangeListener (usa SegmentScope, SubscriptionRepo),
   InfraLogStore, LogStore, SupervisionETLService (usa
   ResumenSaludBuilder, DisparadorETL, ErroresETLService).

## Refs

- T-002: `analyze/coverage/domain-model-coverage.md`
- T-004: `analyze/decision-matrix.md`
- Catalogo RBAC: `source/normativa/restricciones/cnst-032-menu-dinamico-obligatorio.rst`
- Domain-model existente: `source/arquitectura-tecnica/domain-model/`

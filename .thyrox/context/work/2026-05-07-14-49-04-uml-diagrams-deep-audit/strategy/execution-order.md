```yml
created_at: 2026-05-07 16:45:00
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 5 — STRATEGY
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-007 Execution DAG
```

# T-007 — DAG de orden de ejecucion

> Define el orden total de tareas atomicas, respetando
> dependencias (clases nuevas antes que complementos que las
> referencian) y prioridades (cluster reports primero).

## 1. Reglas de ordenamiento

1. **T-CLASS antes que T-COMPLEMENT/T-VERIFY** que dependa de
   esa clase nueva.
2. **Dentro de T-CLASS**: clases base primero, servicios despues
   (DAG interno definido en T-005 §6).
3. **Dentro de T-COMPLEMENT**: cluster por riesgo
   (reports → logs → resto alfabetico).
4. **Dentro de T-VERIFY**: idem, mismo orden de cluster.
5. **T-COMPLEMENT y T-VERIFY pueden mezclarse por cluster**:
   completar todo un cluster (B + A) antes de pasar al siguiente.

## 2. Bloque T-CLASS — orden total (20 tareas)

### Lote 1: clases base sin dependencias internas (10)

| # | Clase | Archivo a crear |
|---|---|---|
| C-01 | AlertRuleRepo | alert-rule-repo.rst |
| C-02 | CampaignDailyStatRepo | campaign-daily-stat-repo.rst |
| C-03 | FunctionGroupMembership | function-group-membership.rst |
| C-04 | HmacVerifier | hmac-verifier.rst |
| C-05 | ImpactReport | impact-report.rst |
| C-06 | SegmentScope | segment-scope.rst |
| C-07 | SubscriptionRepo | subscription-repo.rst |
| C-08 | UserAccessGroupAssignment | user-access-group-assignment.rst |
| C-09 | AlertHistorySummary | alert-history-summary.rst |
| C-10 | DisparadorETL | disparador-etl.rst |

### Lote 2: servicios dependientes (10)

| # | Clase | Archivo a crear | Depende de |
|---|---|---|---|
| C-11 | AlertHistoryService | alert-history-service.rst | C-09 |
| C-12 | CampaignReportService | campaign-report-service.rst | C-02 |
| C-13 | GeneralAuditService | general-audit-service.rst | — |
| C-14 | ErroresETLService | errores-etl-service.rst | — |
| C-15 | ResumenSalud | resumen-salud.rst | — |
| C-16 | ResumenSaludBuilder | resumen-salud-builder.rst | C-15 |
| C-17 | SegmentChangeListener | segment-change-listener.rst | C-06, C-07 |
| C-18 | InfraLogStore | infra-log-store.rst | — |
| C-19 | LogStore | log-store.rst | — |
| C-20 | SupervisionETLService | supervision-etl-service.rst | C-10, C-14, C-16 |

## 3. Bloque T-COMPLEMENT (39 tareas)

Orden por cluster de riesgo (definido en T-004 §4):

### Cluster reports (16 tareas)

T-CO-01 ... T-CO-16 — archivos clase B del cluster reports.

### Cluster logs (11 tareas)

T-CO-17 ... T-CO-27 — archivos clase B del cluster logs.

### Cluster pipeline (6 tareas)

T-CO-28 ... T-CO-33 — archivos clase B del cluster pipeline.

### Cluster audit (4 tareas)

T-CO-34 ... T-CO-37 — archivos clase B del cluster audit.

### Cluster permissions (2 tareas)

T-CO-38, T-CO-39 — archivos clase B del cluster permissions.

(Lista detallada con paths exactos en T-008.)

## 4. Bloque T-VERIFY (53 tareas)

Mismo orden de cluster que T-COMPLEMENT pero con archivos clase A:

### Cluster reports (10)
T-VE-01 ... T-VE-10
### Cluster logs (7)
T-VE-11 ... T-VE-17
### Cluster pipeline (6)
T-VE-18 ... T-VE-23
### Cluster audit (8)
T-VE-24 ... T-VE-31
### Cluster permissions (0)
(no hay archivos clase A en este cluster)
### Cluster access (1)
T-VE-32
### Cluster admin (6)
T-VE-33 ... T-VE-38
### Cluster alerts (15)
T-VE-39 ... T-VE-53

## 5. Bloque TRACK (4 tareas)

| # | Tarea |
|---|---|
| TR-01 | Build clean serial deterministic (`make clean` + `sphinx-build -W -j 1`) |
| TR-02 | Verificar 0 warnings + 0 cross-refs rotos |
| TR-03 | Changelog + lessons learned |
| TR-04 | Cierre WP con post-mortem |

## 6. DAG global resumido

```
[T-CLASS lote 1: C-01..C-10] (paralelos, sin deps)
        |
        v
[T-CLASS lote 2: C-11..C-20] (sequenciales por deps internas)
        |
        v
[T-COMPLEMENT cluster reports] (16) + [T-VERIFY cluster reports] (10)
        |
        v
[T-COMPLEMENT cluster logs] (11) + [T-VERIFY cluster logs] (7)
        |
        v
[T-COMPLEMENT cluster pipeline] (6) + [T-VERIFY cluster pipeline] (6)
        |
        v
[T-COMPLEMENT cluster audit] (4) + [T-VERIFY cluster audit] (8)
        |
        v
[T-COMPLEMENT cluster permissions] (2) + [T-VERIFY cluster access] (1)
        |
        v
[T-VERIFY cluster admin] (6) + [T-VERIFY cluster alerts] (15)
        |
        v
[TR-01..TR-04: TRACK]
```

## 7. Total tareas atomicas

| Bloque | Tareas |
|---|---|
| T-CLASS | 20 |
| T-COMPLEMENT | 39 |
| T-VERIFY | 53 |
| TRACK | 4 |
| **Total** | **116** |

## 8. Estimacion total

| Bloque | Tiempo estimado |
|---|---|
| T-CLASS (20 × 15-20 min) | 5-7 h |
| T-COMPLEMENT (39 × 15-25 min) | 10-16 h |
| T-VERIFY (53 × 5-10 min) | 4-9 h |
| TRACK | 1-2 h |
| **Total** | **20-34 h** |

## Refs

- T-005: `strategy/new-classes-catalog.md`
- T-006: `strategy/uml07-patterns-by-category.md`
- T-008 (siguiente): task-plan ejecutable con T-NNN secuenciados

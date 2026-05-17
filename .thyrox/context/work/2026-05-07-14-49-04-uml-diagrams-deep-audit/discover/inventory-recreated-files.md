```yml
created_at: 2026-05-07 15:50:54
project: IACT-docs
work_package: 2026-05-07-14-49-04-uml-diagrams-deep-audit
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
type: T-001 Inventory
```

# T-001 — Inventario de los 92 archivos recreados

> Inventario exhaustivo extraído mecánicamente con
> `inventory-92.py` el 2026-05-07 15:50:54.
> Fuente: 92 archivos `diagrama-de-*.rst` agregados en
> commits `b057b049..7e4a6463` del WP previo
> `2026-05-07-04-50-49-std-012-prefix-normalization`.

## 1. Distribución por cluster

| Cluster | Archivos |
|---|---|
| access | 1 |
| admin | 6 |
| alerts | 15 |
| audit | 12 |
| logs | 18 |
| permissions | 2 |
| pipeline | 12 |
| reports | 26 |
| **Total** | **92** |

## 2. Distribución por tipo

| Tipo | Archivos |
|---|---|
| actividad | 30 |
| estados | 15 |
| clases | 14 |
| secuencia | 10 |
| componentes | 2 |
| otro(agr-como-agregacion) | 1 |
| otro(impacto) | 1 |
| otro(componentes-fts) | 1 |
| otro(flujo-de-firma) | 1 |
| otro(secuencia-verify) | 1 |
| otro(pipeline) | 1 |
| otro(tail-sse) | 1 |
| otro(componentes-pipeline-log) | 1 |
| otro(secuencia-pipeline-log) | 1 |
| otro(componentes-export) | 1 |
| otro(secuencia-exportacion-logs) | 1 |
| otro(pipeline-infraestructura) | 1 |
| otro(secuencia-tail-sse) | 1 |
| otro(pipeline-metricas) | 1 |
| caso-de-uso-relacion | 1 |
| otro(actividad-crear) | 1 |
| otro(actividad-aplicar) | 1 |
| otro(actividad-compartir) | 1 |
| otro(secuencia-detalle) | 1 |
| otro(distribucion-de-menus) | 1 |
| otro(flujo-de-anonimizacion-etl) | 1 |

## 3. Clases UML referenciadas (top 30)

> Identificadores que aparecen como `class`, `entity`, `component`, `participant`, etc.
> en bloques `@startuml..@enduml`. NO equivalen 1:1 a clases del domain-model —
> incluyen actores, componentes técnicos y aliases STD-011.

| # | Identificador | Apariciones |
|---|---|---|
| 1 | `Servicio` | 17 |
| 2 | `AuditService` | 8 |
| 3 | `SegmentResolver` | 6 |
| 4 | `AlertRepo` | 4 |
| 5 | `LogStore` | 4 |
| 6 | `PipelineExecutionRepo` | 4 |
| 7 | `Interfaz` | 3 |
| 8 | `AuditRepo` | 3 |
| 9 | `PiiScanner` | 3 |
| 10 | `Base` | 3 |
| 11 | `EvaluatorReloader` | 2 |
| 12 | `TimingCalculator` | 2 |
| 13 | `CursorEncoder` | 2 |
| 14 | `ExportWorker` | 2 |
| 15 | `InternalMailbox` | 2 |
| 16 | `pipeline_runs` | 2 |
| 17 | `InfraLogStore` | 2 |
| 18 | `AgentReportService` | 2 |
| 19 | `KPICalculator` | 2 |
| 20 | `AccessGroup` | 1 |
| 21 | `Function` | 1 |
| 22 | `FunctionGroupMembership` | 1 |
| 23 | `User` | 1 |
| 24 | `UserAccessGroupAssignment` | 1 |
| 25 | `Almacen` | 1 |
| 26 | `ImpactReport` | 1 |
| 27 | `AlertRule` | 1 |
| 28 | `AlertRuleRepo` | 1 |
| 29 | `RuleValidator` | 1 |
| 30 | `AlertHistoryService` | 1 |

**Total identificadores únicos:** 55

## 4. Cross-refs `:doc:` (top 30)

> Paths declarados en `.. seealso::`. T-002 verificará cuáles existen.

| # | Path | Apariciones |
|---|---|---|
| 1 | `diagrama-de-caso-de-uso` | 53 |
| 2 | `diagrama-de-secuencia` | 10 |
| 3 | `diagrama-de-clases` | 10 |
| 4 | `/arquitectura-tecnica/domain-model/alert` | 8 |
| 5 | `/arquitectura-tecnica/domain-model/pipeline-execution` | 6 |
| 6 | `/requisitos/reglas-negocio/br-009-bajas-logicas` | 5 |
| 7 | `/arquitectura-tecnica/domain-model/evaluator-reloader` | 4 |
| 8 | `/arquitectura-tecnica/domain-model/alert-repo` | 4 |
| 9 | `diagrama-de-actividad` | 4 |
| 10 | `/arquitectura-tecnica/domain-model/export-job` | 4 |
| 11 | `/arquitectura-tecnica/domain-model/function` | 3 |
| 12 | `/backend/adr-back-010-function-is-critical-governance` | 3 |
| 13 | `/arquitectura-tecnica/domain-model/alert-rule` | 3 |
| 14 | `/arquitectura-tecnica/domain-model/subscription` | 3 |
| 15 | `/arquitectura-tecnica/domain-model/audit-event` | 3 |
| 16 | `/arquitectura-tecnica/domain-model/pii-scanner` | 3 |
| 17 | `/arquitectura-tecnica/domain-model/pipeline-execution-repo` | 3 |
| 18 | `/arquitectura-tecnica/domain-model/saved-view` | 3 |
| 19 | `/arquitectura-tecnica/domain-model/access-group` | 2 |
| 20 | `/arquitectura-tecnica/domain-model/separation-rule` | 2 |
| 21 | `/requisitos/reglas-negocio/br-007-separacion-funciones-sod` | 2 |
| 22 | `/arquitectura-tecnica/domain-model/rule-validator` | 2 |
| 23 | `/arquitectura-tecnica/domain-model/audit-service` | 2 |
| 24 | `/arquitectura-tecnica/domain-model/timing-calculator` | 2 |
| 25 | `/arquitectura-tecnica/domain-model/cursor-encoder` | 2 |
| 26 | `/arquitectura-tecnica/domain-model/export-worker` | 2 |
| 27 | `/arquitectura-tecnica/domain-model/internal-mailbox` | 2 |
| 28 | `diagrama-de-flujo-de-firma` | 2 |
| 29 | `diagrama-de-secuencia-verify` | 2 |
| 30 | `/arquitectura-tecnica/domain-model/application-log` | 2 |

**Total `:doc:` refs únicos:** 82

## 5. Archivos sin caption (gap STD)

Todos los archivos tienen caption.

## 6. Archivos sin `.. seealso::` (gap cross-refs)

**2 archivos** sin bloque `.. seealso::`:

- `requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-estados-exceptionalpermission.rst`
- `requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-estados-accessgroup.rst`

## 7. Tabla maestra (92 filas)

| # | Cluster | UC | Tipo | Líneas | #Clases | #Actores | #Inc | #Ext | Cap | SeeAlso | #DocRefs |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | access | uc-acc-04 | otro(agr-como-agregacion) | 87 | 5 | 0 | 0 | 0 | Y | Y | 6 |
| 2 | admin | uc-adm-01 | actividad | 66 | 0 | 0 | 0 | 0 | Y | Y | 4 |
| 3 | admin | uc-adm-01 | estados | 40 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 4 | admin | uc-adm-02 | actividad | 67 | 0 | 0 | 0 | 0 | Y | Y | 5 |
| 5 | admin | uc-adm-02 | estados | 50 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 6 | admin | uc-adm-03 | actividad | 65 | 0 | 0 | 0 | 0 | Y | Y | 4 |
| 7 | admin | uc-adm-03 | otro(impacto) | 43 | 5 | 1 | 0 | 0 | Y | Y | 3 |
| 8 | alerts | uc-alr-01 | actividad | 47 | 0 | 0 | 0 | 0 | Y | Y | 4 |
| 9 | alerts | uc-alr-01 | clases | 49 | 4 | 0 | 0 | 0 | Y | Y | 4 |
| 10 | alerts | uc-alr-01 | estados | 41 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 11 | alerts | uc-alr-02 | actividad | 38 | 0 | 0 | 0 | 0 | Y | Y | 4 |
| 12 | alerts | uc-alr-02 | estados | 50 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 13 | alerts | uc-alr-02 | secuencia | 34 | 3 | 1 | 0 | 0 | Y | Y | 4 |
| 14 | alerts | uc-alr-03 | actividad | 59 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 15 | alerts | uc-alr-03 | estados | 31 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 16 | alerts | uc-alr-03 | secuencia | 35 | 3 | 1 | 0 | 0 | Y | Y | 4 |
| 17 | alerts | uc-alr-04 | actividad | 56 | 0 | 0 | 0 | 0 | Y | Y | 4 |
| 18 | alerts | uc-alr-04 | clases | 41 | 4 | 0 | 0 | 0 | Y | Y | 2 |
| 19 | alerts | uc-alr-04 | secuencia | 43 | 4 | 1 | 0 | 0 | Y | Y | 3 |
| 20 | alerts | uc-alr-05 | actividad | 45 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 21 | alerts | uc-alr-05 | clases | 43 | 3 | 0 | 0 | 0 | Y | Y | 1 |
| 22 | alerts | uc-alr-05 | estados | 36 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 23 | audit | uc-aud-01 | actividad | 44 | 0 | 0 | 0 | 0 | Y | Y | 4 |
| 24 | audit | uc-aud-01 | clases | 45 | 5 | 0 | 0 | 0 | Y | Y | 5 |
| 25 | audit | uc-aud-01 | secuencia | 41 | 5 | 1 | 0 | 0 | Y | Y | 2 |
| 26 | audit | uc-aud-02 | actividad | 44 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 27 | audit | uc-aud-02 | otro(componentes-fts) | 39 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 28 | audit | uc-aud-02 | secuencia | 36 | 4 | 1 | 0 | 0 | Y | Y | 3 |
| 29 | audit | uc-aud-03 | actividad | 49 | 0 | 0 | 0 | 0 | Y | Y | 5 |
| 30 | audit | uc-aud-03 | estados | 42 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 31 | audit | uc-aud-03 | secuencia | 42 | 5 | 1 | 0 | 0 | Y | Y | 3 |
| 32 | audit | uc-aud-04 | actividad | 53 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 33 | audit | uc-aud-04 | otro(flujo-de-firma) | 36 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 34 | audit | uc-aud-04 | otro(secuencia-verify) | 34 | 3 | 1 | 0 | 0 | Y | Y | 2 |
| 35 | logs | uc-log-01 | actividad | 36 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 36 | logs | uc-log-01 | otro(pipeline) | 31 | 1 | 0 | 0 | 0 | Y | Y | 2 |
| 37 | logs | uc-log-01 | otro(tail-sse) | 27 | 2 | 1 | 0 | 0 | Y | Y | 2 |
| 38 | logs | uc-log-02 | actividad | 32 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 39 | logs | uc-log-02 | otro(componentes-pipeline-log) | 26 | 1 | 1 | 0 | 0 | Y | Y | 1 |
| 40 | logs | uc-log-02 | otro(secuencia-pipeline-log) | 29 | 2 | 1 | 0 | 0 | Y | Y | 1 |
| 41 | logs | uc-log-03 | actividad | 37 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 42 | logs | uc-log-04 | actividad | 45 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 43 | logs | uc-log-04 | otro(componentes-export) | 29 | 1 | 1 | 0 | 0 | Y | Y | 2 |
| 44 | logs | uc-log-04 | otro(secuencia-exportacion-logs) | 35 | 5 | 1 | 0 | 0 | Y | Y | 1 |
| 45 | logs | uc-log-05 | actividad | 32 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 46 | logs | uc-log-05 | otro(pipeline-infraestructura) | 28 | 1 | 1 | 0 | 0 | Y | Y | 1 |
| 47 | logs | uc-log-05 | otro(secuencia-tail-sse) | 35 | 2 | 1 | 0 | 0 | Y | Y | 1 |
| 48 | logs | uc-log-06 | actividad | 47 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 49 | logs | uc-log-06 | componentes | 26 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 50 | logs | uc-log-06 | estados | 37 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 51 | logs | uc-log-07 | actividad | 37 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 52 | logs | uc-log-07 | otro(pipeline-metricas) | 30 | 1 | 0 | 0 | 0 | Y | Y | 1 |
| 53 | permissions | uc-perm-04 | estados | 20 | 0 | 0 | 0 | 0 | Y | N | 0 |
| 54 | permissions | uc-perm-05 | estados | 20 | 0 | 0 | 0 | 0 | Y | N | 0 |
| 55 | pipeline | uc-pip-01 | actividad | 30 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 56 | pipeline | uc-pip-01 | clases | 40 | 4 | 0 | 0 | 0 | Y | Y | 2 |
| 57 | pipeline | uc-pip-01 | estados | 27 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 58 | pipeline | uc-pip-02 | actividad | 30 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 59 | pipeline | uc-pip-02 | clases | 25 | 2 | 0 | 0 | 0 | Y | Y | 1 |
| 60 | pipeline | uc-pip-02 | secuencia | 26 | 2 | 1 | 0 | 0 | Y | Y | 2 |
| 61 | pipeline | uc-pip-03 | actividad | 36 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 62 | pipeline | uc-pip-03 | componentes | 22 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 63 | pipeline | uc-pip-03 | estados | 37 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 64 | pipeline | uc-pip-04 | actividad | 43 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 65 | pipeline | uc-pip-04 | estados | 32 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 66 | pipeline | uc-pip-04 | secuencia | 30 | 4 | 1 | 0 | 0 | Y | Y | 1 |
| 67 | reports | uc-inc-rpt-01 | actividad | 31 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 68 | reports | uc-inc-rpt-01 | caso-de-uso-relacion | 40 | 0 | 3 | 1 | 0 | Y | Y | 2 |
| 69 | reports | uc-inc-rpt-01 | clases | 35 | 3 | 0 | 0 | 0 | Y | Y | 2 |
| 70 | reports | uc-rpt-10 | otro(actividad-crear) | 42 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 71 | reports | uc-rpt-10 | clases | 34 | 2 | 0 | 0 | 0 | Y | Y | 2 |
| 72 | reports | uc-rpt-10 | estados | 29 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 73 | reports | uc-rpt-11 | otro(actividad-aplicar) | 37 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 74 | reports | uc-rpt-11 | otro(actividad-compartir) | 48 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 75 | reports | uc-rpt-11 | estados | 35 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 76 | reports | uc-rpt-12 | actividad | 43 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 77 | reports | uc-rpt-12 | clases | 34 | 3 | 0 | 0 | 0 | Y | Y | 3 |
| 78 | reports | uc-rpt-12 | otro(secuencia-detalle) | 31 | 4 | 1 | 0 | 0 | Y | Y | 1 |
| 79 | reports | uc-rpt-13 | actividad | 36 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 80 | reports | uc-rpt-13 | clases | 26 | 2 | 0 | 0 | 0 | Y | Y | 2 |
| 81 | reports | uc-rpt-13 | secuencia | 28 | 3 | 1 | 0 | 0 | Y | Y | 1 |
| 82 | reports | uc-rpt-14 | actividad | 36 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 83 | reports | uc-rpt-14 | clases | 31 | 3 | 0 | 0 | 0 | Y | Y | 1 |
| 84 | reports | uc-rpt-14 | secuencia | 25 | 2 | 1 | 0 | 0 | Y | Y | 1 |
| 85 | reports | uc-rpt-15 | actividad | 36 | 0 | 0 | 0 | 0 | Y | Y | 2 |
| 86 | reports | uc-rpt-15 | clases | 25 | 2 | 0 | 0 | 0 | Y | Y | 1 |
| 87 | reports | uc-rpt-16 | actividad | 42 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 88 | reports | uc-rpt-16 | clases | 25 | 2 | 0 | 0 | 0 | Y | Y | 1 |
| 89 | reports | uc-rpt-16 | otro(distribucion-de-menus) | 21 | 0 | 0 | 0 | 0 | Y | Y | 1 |
| 90 | reports | uc-rpt-17 | actividad | 36 | 0 | 0 | 0 | 0 | Y | Y | 3 |
| 91 | reports | uc-rpt-17 | clases | 25 | 2 | 0 | 0 | 0 | Y | Y | 1 |
| 92 | reports | uc-rpt-17 | otro(flujo-de-anonimizacion-etl) | 32 | 0 | 0 | 0 | 0 | Y | Y | 2 |

## 8. Detalle por archivo (clases + cross-refs)

### `requisitos/casos-uso/access/uc-acc-04/diagramas-uml/diagrama-de-agr-como-agregacion.rst`

- Tipo: **otro(agr-como-agregacion)** · Líneas: 87
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AccessGroup`, `Function`, `FunctionGroupMembership`, `User`, `UserAccessGroupAssignment`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/user`
  - `/arquitectura-tecnica/domain-model/assignment`
  - `/arquitectura-tecnica/domain-model/access-group`
  - `/arquitectura-tecnica/domain-model/access-group-function`
  - `/arquitectura-tecnica/domain-model/function`
  - `/backend/adr-back-010-function-is-critical-governance`

### `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 66
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/normativa/restricciones/cnst-030-reglas-de-separacion-de-funciones-sod`
  - `/arquitectura-tecnica/domain-model/separation-rule`
  - `/arquitectura-tecnica/domain-model/evaluator-reloader`

### `requisitos/casos-uso/admin/uc-adm-01/diagramas-uml/diagrama-de-estados-sod-rule.rst`

- Tipo: **estados** · Líneas: 40
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/separation-rule`
  - `/requisitos/reglas-negocio/br-007-separacion-funciones-sod`
  - `/requisitos/reglas-negocio/br-009-bajas-logicas`

### `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 67
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/normativa/estandares/std-008-naming-identificadores`
  - `/arquitectura-tecnica/domain-model/function`
  - `/arquitectura-tecnica/domain-model/permission-cache`
  - `/backend/adr-back-010-function-is-critical-governance`

### `requisitos/casos-uso/admin/uc-adm-02/diagramas-uml/diagrama-de-estados-funcion.rst`

- Tipo: **estados** · Líneas: 50
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/function`
  - `/requisitos/reglas-negocio/br-009-bajas-logicas`
  - `/backend/adr-back-010-function-is-critical-governance`

### `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 65
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/requisitos/reglas-negocio/br-007-separacion-funciones-sod`
  - `/arquitectura-tecnica/domain-model/function-group`
  - `/arquitectura-tecnica/domain-model/access-group`

### `requisitos/casos-uso/admin/uc-adm-03/diagramas-uml/diagrama-de-impacto.rst`

- Tipo: **otro(impacto)** · Líneas: 43
- Caption: sí · SeeAlso: sí
- Identificadores UML: `Almacen`, `EvaluatorReloader`, `ImpactReport`, `Interfaz`, `Servicio`
- Actores: `assign_functions_to_group`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/evaluator-reloader`
  - `/arquitectura-tecnica/domain-model/effective-permissions-aggregator`

### `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 47
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/alert-rule`
  - `/arquitectura-tecnica/domain-model/rule-validator`
  - `/arquitectura-tecnica/domain-model/evaluator-reloader`

### `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 49
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AlertRule`, `AlertRuleRepo`, `EvaluatorReloader`, `RuleValidator`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/alert-rule`
  - `/arquitectura-tecnica/domain-model/alert-repo`
  - `/arquitectura-tecnica/domain-model/rule-validator`
  - `/arquitectura-tecnica/domain-model/evaluator-reloader`

### `requisitos/casos-uso/alerts/uc-alr-01/diagramas-uml/diagrama-de-estados-regla.rst`

- Tipo: **estados** · Líneas: 41
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/alert-rule`
  - `/requisitos/reglas-negocio/br-009-bajas-logicas`

### `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 38
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `/arquitectura-tecnica/domain-model/alert`
  - `/arquitectura-tecnica/domain-model/alert-repo`

### `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-estados-alerta.rst`

- Tipo: **estados** · Líneas: 50
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/alert`
  - `/requisitos/casos-uso/alerts/uc-alr-03/index`

### `requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 34
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AlertRepo`, `Interfaz`, `Servicio`
- Actores: `view_alerts`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-actividad`
  - `/arquitectura-tecnica/domain-model/alert`
  - `/arquitectura-tecnica/domain-model/alert-repo`

### `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 59
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `/arquitectura-tecnica/domain-model/alert`

### `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-estados-transicion.rst`

- Tipo: **estados** · Líneas: 31
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/alert`
  - `/requisitos/casos-uso/alerts/uc-alr-02/diagramas-uml/diagrama-de-estados-alerta`

### `requisitos/casos-uso/alerts/uc-alr-03/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 35
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AlertRepo`, `AuditService`, `Servicio`
- Actores: `acknowledge_alert`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-actividad`
  - `/arquitectura-tecnica/domain-model/alert`
  - `/arquitectura-tecnica/domain-model/audit-service`

### `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 56
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `/arquitectura-tecnica/domain-model/alert`
  - `/arquitectura-tecnica/domain-model/timing-calculator`

### `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 41
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AlertHistoryService`, `AlertHistorySummary`, `AlertRepo`, `TimingCalculator`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/alert-repo`
  - `/arquitectura-tecnica/domain-model/timing-calculator`

### `requisitos/casos-uso/alerts/uc-alr-04/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 43
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AlertRepo`, `Interfaz`, `Servicio`, `TimingCalculator`
- Actores: `view_alert_history`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-actividad`
  - `/arquitectura-tecnica/domain-model/alert`

### `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 45
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/subscription`

### `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 43
- Caption: sí · SeeAlso: sí
- Identificadores UML: `SegmentChangeListener`, `Subscription`, `SubscriptionRepo`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/subscription`

### `requisitos/casos-uso/alerts/uc-alr-05/diagramas-uml/diagrama-de-estados-subscription.rst`

- Tipo: **estados** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/subscription`
  - `/requisitos/reglas-negocio/br-009-bajas-logicas`

### `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 44
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `/arquitectura-tecnica/domain-model/audit-event`
  - `/arquitectura-tecnica/domain-model/cursor-encoder`

### `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 45
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AuditRepo`, `AuditService`, `CursorEncoder`, `GeneralAuditService`, `PiiScanner`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/audit-event`
  - `/arquitectura-tecnica/domain-model/audit-query-service`
  - `/arquitectura-tecnica/domain-model/audit-repo`
  - `/arquitectura-tecnica/domain-model/cursor-encoder`
  - `/arquitectura-tecnica/domain-model/pii-scanner`

### `requisitos/casos-uso/audit/uc-aud-01/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 41
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AuditRepo`, `AuditService`, `CursorEncoder`, `PiiScanner`, `Servicio`
- Actores: `view_audit_log`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/audit-service`

### `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 44
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-componentes-fts`
  - `diagrama-de-secuencia`

### `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-componentes-fts.rst`

- Tipo: **otro(componentes-fts)** · Líneas: 39
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/audit-event`

### `requisitos/casos-uso/audit/uc-aud-02/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AuditService`, `FTS`, `PiiScanner`, `Servicio`
- Actores: `search_audit_log`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-actividad`
  - `/arquitectura-tecnica/domain-model/pii-scanner`

### `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 49
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `diagrama-de-estados-export-job`
  - `/arquitectura-tecnica/domain-model/export-job`
  - `/arquitectura-tecnica/domain-model/export-worker`

### `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-estados-export-job.rst`

- Tipo: **estados** · Líneas: 42
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/export-job`
  - `/arquitectura-tecnica/domain-model/export-worker`

### `requisitos/casos-uso/audit/uc-aud-03/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 42
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AuditRepo`, `AuditService`, `ExportWorker`, `InternalMailbox`, `Servicio`
- Actores: `export_audit_log`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/export-job`
  - `/arquitectura-tecnica/domain-model/internal-mailbox`

### `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 53
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-flujo-de-firma`
  - `diagrama-de-secuencia-verify`

### `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-flujo-de-firma.rst`

- Tipo: **otro(flujo-de-firma)** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia-verify`

### `requisitos/casos-uso/audit/uc-aud-04/diagramas-uml/diagrama-de-secuencia-verify.rst`

- Tipo: **otro(secuencia-verify)** · Líneas: 34
- Caption: sí · SeeAlso: sí
- Identificadores UML: `HmacVerifier`, `Servicio`, `Storage`
- Actores: `verify_audit_report`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-flujo-de-firma`

### `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-pipeline`
  - `diagrama-de-tail-sse`

### `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-pipeline.rst`

- Tipo: **otro(pipeline)** · Líneas: 31
- Caption: sí · SeeAlso: sí
- Identificadores UML: `LogStore`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/application-log`
  - `/arquitectura-tecnica/domain-model/pii-scanner`

### `requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-tail-sse.rst`

- Tipo: **otro(tail-sse)** · Líneas: 27
- Caption: sí · SeeAlso: sí
- Identificadores UML: `LogStore`, `Servicio`
- Actores: `view_application_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/application-log`

### `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 32
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-componentes-pipeline-log`
  - `diagrama-de-secuencia-pipeline-log`

### `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-componentes-pipeline-log.rst`

- Tipo: **otro(componentes-pipeline-log)** · Líneas: 26
- Caption: sí · SeeAlso: sí
- Identificadores UML: `pipeline_runs`
- Actores: `view_pipeline_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution`

### `requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-secuencia-pipeline-log.rst`

- Tipo: **otro(secuencia-pipeline-log)** · Líneas: 29
- Caption: sí · SeeAlso: sí
- Identificadores UML: `Servicio`, `pipeline_runs`
- Actores: `view_pipeline_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/logs/uc-log-03/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 37
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/requisitos/casos-uso/audit/uc-aud-02/index`

### `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 45
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-componentes-export`
  - `diagrama-de-secuencia-exportacion-logs`

### `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-componentes-export.rst`

- Tipo: **otro(componentes-export)** · Líneas: 29
- Caption: sí · SeeAlso: sí
- Identificadores UML: `LogStore`
- Actores: `export_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/export-job`
  - `/arquitectura-tecnica/domain-model/internal-mailbox`

### `requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-secuencia-exportacion-logs.rst`

- Tipo: **otro(secuencia-exportacion-logs)** · Líneas: 35
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AuditService`, `ExportWorker`, `InternalMailbox`, `LogStore`, `Servicio`
- Actores: `export_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 32
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-pipeline-infraestructura`
  - `diagrama-de-secuencia-tail-sse`

### `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-pipeline-infraestructura.rst`

- Tipo: **otro(pipeline-infraestructura)** · Líneas: 28
- Caption: sí · SeeAlso: sí
- Identificadores UML: `InfraLogStore`
- Actores: `view_infrastructure_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/infrastructure-log`

### `requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-secuencia-tail-sse.rst`

- Tipo: **otro(secuencia-tail-sse)** · Líneas: 35
- Caption: sí · SeeAlso: sí
- Identificadores UML: `InfraLogStore`, `Servicio`
- Actores: `view_infrastructure_logs`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 47
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-componentes`
  - `diagrama-de-estados-overall`

### `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-componentes.rst`

- Tipo: **componentes** · Líneas: 26
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/system-health`

### `requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-estados-overall.rst`

- Tipo: **estados** · Líneas: 37
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/system-health`

### `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 37
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-pipeline-metricas`

### `requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-pipeline-metricas.rst`

- Tipo: **otro(pipeline-metricas)** · Líneas: 30
- Caption: sí · SeeAlso: sí
- Identificadores UML: `TSDB`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/technical-metric`

### `requisitos/casos-uso/permissions/uc-perm-04/diagramas-uml/diagrama-de-estados-exceptionalpermission.rst`

- Tipo: **estados** · Líneas: 20
- Caption: sí · SeeAlso: NO
- Includes: 0 · Extends: 0

### `requisitos/casos-uso/permissions/uc-perm-05/diagramas-uml/diagrama-de-estados-accessgroup.rst`

- Tipo: **estados** · Líneas: 20
- Caption: sí · SeeAlso: NO
- Includes: 0 · Extends: 0

### `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 30
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-estados-ejecucion-etl`

### `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 40
- Caption: sí · SeeAlso: sí
- Identificadores UML: `PipelineExecutionRepo`, `ResumenSalud`, `ResumenSaludBuilder`, `SupervisionETLService`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution`
  - `/arquitectura-tecnica/domain-model/pipeline-execution-repo`

### `requisitos/casos-uso/pipeline/uc-pip-01/diagramas-uml/diagrama-de-estados-ejecucion-etl.rst`

- Tipo: **estados** · Líneas: 27
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution`

### `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 30
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `diagrama-de-clases`

### `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 25
- Caption: sí · SeeAlso: sí
- Identificadores UML: `ErroresETLService`, `PipelineExecutionRepo`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution-repo`

### `requisitos/casos-uso/pipeline/uc-pip-02/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 26
- Caption: sí · SeeAlso: sí
- Identificadores UML: `PipelineExecutionRepo`, `Servicio`
- Actores: `view_pipeline_errors`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/arquitectura-tecnica/domain-model/pipeline-execution`

### `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-componentes`
  - `diagrama-de-estados-frescura-datos`

### `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-componentes.rst`

- Tipo: **componentes** · Líneas: 22
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution-repo`

### `requisitos/casos-uso/pipeline/uc-pip-03/diagramas-uml/diagrama-de-estados-frescura-datos.rst`

- Tipo: **estados** · Líneas: 37
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution`

### `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 43
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-secuencia`
  - `diagrama-de-estados-reintento`

### `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-estados-reintento.rst`

- Tipo: **estados** · Líneas: 32
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/pipeline-execution`

### `requisitos/casos-uso/pipeline/uc-pip-04/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 30
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AuditService`, `DisparadorETL`, `PipelineExecutionRepo`, `Servicio`
- Actores: `request_pipeline_retry`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 31
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso-relacion-de-inclusion`
  - `diagrama-de-clases`
  - `/requisitos/reglas-negocio/br-012-usuario-segmento-unico`

### `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-caso-de-uso-relacion-de-inclusion.rst`

- Tipo: **caso-de-uso-relacion** · Líneas: 40
- Caption: sí · SeeAlso: sí
- Actores: `RBACRepo`, `SegmentResolver`, `view_reports`
- Includes: 1 · Extends: 0
- `:doc:` refs:
  - `/requisitos/casos-uso/reports/uc-inc-rpt-01/index`
  - `/requisitos/reglas-negocio/br-012-usuario-segmento-unico`

### `requisitos/casos-uso/reports/uc-inc-rpt-01/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 35
- Caption: sí · SeeAlso: sí
- Identificadores UML: `RBACRepo`, `SegmentResolver`, `SegmentScope`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/segment-resolver`
  - `/arquitectura-tecnica/domain-model/rbac-repo`

### `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-actividad-crear.rst`

- Tipo: **otro(actividad-crear)** · Líneas: 42
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-estados-saved-view`

### `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 34
- Caption: sí · SeeAlso: sí
- Identificadores UML: `ColumnCatalog`, `SavedView`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/saved-view`
  - `/arquitectura-tecnica/domain-model/column-catalog`

### `requisitos/casos-uso/reports/uc-rpt-10/diagramas-uml/diagrama-de-estados-saved-view.rst`

- Tipo: **estados** · Líneas: 29
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/saved-view`
  - `/requisitos/reglas-negocio/br-009-bajas-logicas`

### `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-aplicar.rst`

- Tipo: **otro(actividad-aplicar)** · Líneas: 37
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-actividad-compartir`
  - `diagrama-de-estados-share`

### `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-actividad-compartir.rst`

- Tipo: **otro(actividad-compartir)** · Líneas: 48
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-estados-share`

### `requisitos/casos-uso/reports/uc-rpt-11/diagramas-uml/diagrama-de-estados-share.rst`

- Tipo: **estados** · Líneas: 35
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/saved-view`

### `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 43
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-secuencia-detalle`

### `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 34
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AgentDailyStatRepo`, `AgentReportService`, `KPICalculator`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/agent-report-service`
  - `/arquitectura-tecnica/domain-model/agent-daily-stat-repo`
  - `/arquitectura-tecnica/domain-model/kpi-calculator`

### `requisitos/casos-uso/reports/uc-rpt-12/diagramas-uml/diagrama-de-secuencia-detalle.rst`

- Tipo: **otro(secuencia-detalle)** · Líneas: 31
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AgentReportService`, `AuditService`, `Base`, `Servicio`
- Actores: `view_reports`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-secuencia`

### `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 26
- Caption: sí · SeeAlso: sí
- Identificadores UML: `AbandonmentReportService`, `SegmentResolver`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/abandonment-report-service`
  - `/arquitectura-tecnica/domain-model/segment-resolver`

### `requisitos/casos-uso/reports/uc-rpt-13/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 28
- Caption: sí · SeeAlso: sí
- Identificadores UML: `Base`, `SegmentResolver`, `Servicio`
- Actores: `view_reports`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-secuencia`

### `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 31
- Caption: sí · SeeAlso: sí
- Identificadores UML: `CampaignDailyStatRepo`, `CampaignReportService`, `KPICalculator`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/kpi-calculator`

### `requisitos/casos-uso/reports/uc-rpt-14/diagramas-uml/diagrama-de-secuencia.rst`

- Tipo: **secuencia** · Líneas: 25
- Caption: sí · SeeAlso: sí
- Identificadores UML: `Base`, `Servicio`
- Actores: `view_reports`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`

### `requisitos/casos-uso/reports/uc-rpt-15/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 25
- Caption: sí · SeeAlso: sí
- Identificadores UML: `SegmentResolver`, `TransferReportService`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/transfer-report-service`

### `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 42
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-distribucion-de-menus`

### `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 25
- Caption: sí · SeeAlso: sí
- Identificadores UML: `MenuIVRReportService`, `SegmentResolver`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/ivr-navigation-report-service`

### `requisitos/casos-uso/reports/uc-rpt-16/diagramas-uml/diagrama-de-distribucion-de-menus.rst`

- Tipo: **otro(distribucion-de-menus)** · Líneas: 21
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`

### `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-actividad.rst`

- Tipo: **actividad** · Líneas: 36
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `diagrama-de-clases`
  - `diagrama-de-flujo-de-anonimizacion-etl`

### `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-clases.rst`

- Tipo: **clases** · Líneas: 25
- Caption: sí · SeeAlso: sí
- Identificadores UML: `CallerReportService`, `SegmentResolver`
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `/arquitectura-tecnica/domain-model/caller-report-service`

### `requisitos/casos-uso/reports/uc-rpt-17/diagramas-uml/diagrama-de-flujo-de-anonimizacion-etl.rst`

- Tipo: **otro(flujo-de-anonimizacion-etl)** · Líneas: 32
- Caption: sí · SeeAlso: sí
- Includes: 0 · Extends: 0
- `:doc:` refs:
  - `diagrama-de-caso-de-uso`
  - `/requisitos/reglas-negocio/br-020-clasificacion-datos`

## 9. Próximos pasos

- T-002: verificar cada cross-ref `:doc:` y cada identificador
  UML que parezca clase del domain-model contra
  `source/arquitectura-tecnica/domain-model/`.
- T-003: scoring UML-07 archivo-por-archivo.
- T-004: matriz consolidada con clasificación A/B/C.

## Refs

- WP previo: `2026-05-07-04-50-49-std-012-prefix-normalization`.
- Honesty note: `track/honesty-note-on-recreate-depth.md` en WP previo.
- Material UML-07: `source/base-cognitiva/_uml/uml-07-diagramas-casos-uso/`.
- Domain-model: `source/arquitectura-tecnica/domain-model/`.

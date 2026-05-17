```yml
created_at: 2026-05-02 09:54:55
project: IACT-docs
work_package: 2026-05-02-09-54-55-source-corrections-pipeline
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# DISCOVER — Correcciones source/ pipeline

Gap analysis entre la documentación publicada en `source/` y la
arquitectura real descubierta en el WP anterior
`2026-05-02-07-12-32-pipeline-uc-deepening`.

---

## Contexto: arquitectura REAL (PROVEN desde WP previo)

| Componente | Realidad |
|---|---|
| Motor de DB | **MariaDB 10.1.48** — sin window functions (CNST-ETL-007) |
| Tablas fuente | `tbl_historico_tN_YYYY` — quarterly, sin índices, read-only |
| Tablas destino ETL | `base_ivr_detalle` + `base_ivr_clientes` — en MariaDB |
| ETL | Stored Procedures: `sp_etl_maestro`, `sp_etl_base_detalle`, `sp_etl_base_clientes` |
| Patrón ETL | TRUNCATE + INSERT (no upsert, no Python classes) |
| Reporting | 7 SPs read-only: `sp_rpt_centros_transferencia`, `sp_rpt_llamadas_abandonadas`, `sp_rpt_menu_redirigidos`, `sp_rpt_clientes`, `sp_rpt_centros_xsegmento`, `sp_rpt_menu_centro`, `sp_rpt_cMENU_ERROR` |
| Segmentos | `nacional_A` (DID 19028031), `nacional_B` (DID 19020001), `Puebla` (DID 19020084) |
| Sentinel cMenu vacío | `'VACIO'` (D-24 — convención unificada) |
| Definición abandono | `menu IN ('VACIO','cliente_colgo','SinOpcion_Cabecera')` (D-21) |
| Django y ETL | Django **NO ejecuta el ETL** — llama solo `sp_rpt_*` (read) vía `CALL` |

---

## Gap 1 — `source/databases/etl-pipeline.rst`

**Estado:** CRÍTICO — describe arquitectura completamente diferente.

| Claim en source/ | Realidad | Severidad |
|---|---|---|
| ETL en Python: `etl/extractors/`, `etl/transformers/`, `etl/loaders/` | ETL en SQL SPs en MariaDB | CRÍTICA |
| Modelo `ETLRun` con `rows_processed`, `bytes_processed` | No existe `ETLRun` — el ETL es `CALL sp_etl_maestro(...)` | CRÍTICA |
| Compatible con Airflow/Prefect/custom | MariaDB SPs solamente. Scheduler externo solo lanza el CALL | ALTA |
| "Calcula métricas derivadas (tasa abandono, TMO, etc.)" en transformer | El SP agrega conteos de filas, no calcula tasas — las tasas las calcula el SP de reporte al momento | MEDIA |
| Frecuencia 6-12h (CNST_008) — correcto en concepto | Correcto — frecuencia aplica, ventana 02:00-04:00 correcta | OK |

**Corrección requerida:** Reescribir las secciones 2 (Etapas) y 3+ para
describir el flujo SP-based real. Conservar CNST_008 y la restricción de
ventana horaria.

---

## Gap 2 — `source/databases/modelo-dual.rst`

**Estado:** PARCIALMENTE INCORRECTO.

| Claim en source/ | Realidad | Severidad |
|---|---|---|
| "BD PostgreSQL (IACT Analytics)" como destino del ETL | Las tablas analíticas (`base_ivr_*`) están en **MariaDB**, no PostgreSQL | CRÍTICA |
| "Tablas analíticas derivadas del ETL" en PostgreSQL | `base_ivr_detalle` y `base_ivr_clientes` son tablas MariaDB | CRÍTICA |
| "BD MySQL (IVR Operacional) — solo lectura" | Correcto | OK |
| CNST_007 (read-only) | Correcto | OK |
| `IVRRouter` Django router | Conceptualmente correcto, pero el target es MariaDB no MySQL | MEDIA |

**Nota de aclaración:** PostgreSQL puede existir para tablas **operacionales**
de Django (usuarios, RBAC, sesiones, alertas). La dualidad real es:
- **MariaDB (cliente):** `tbl_historico_*` (fuente) + `base_ivr_*` (agregados ETL) + SPs
- **PostgreSQL (IACT):** tablas operacionales Django (`auth_user`, RBAC, `audit_log`, alertas, etc.)

El ETL NO transfiere datos a PostgreSQL. Django lee reportes IVR directamente
desde MariaDB vía `CALL sp_rpt_*`.

---

## Gap 3 — `source/arquitectura-tecnica/modulos/vis-reports/componentes.rst`

**Estado:** INCORRECTO — modelo de datos inventado.

| Claim en source/ | Realidad | Severidad |
|---|---|---|
| Modelo Django `DailyMetrics` con `date`, `center_code`, `service_code`, etc. | No existe `DailyMetrics` — datos vienen de `sp_rpt_*` en MariaDB | CRÍTICA |
| `apps.analytics` — "Modelos de métricas, repositorios de consulta" | No hay modelos ORM de métricas — son CALL a SPs | ALTA |
| `unique_together = ['date', 'center_code', 'service_code']` | No aplica — no hay tabla Django para esto | ALTA |
| `GET /api/v1/reports/quarterly` | Endpoint puede existir pero llama `CALL sp_rpt_centros_transferencia(...)` | MEDIA |

**Corrección requerida:** Reemplazar el modelo Django con la descripción real
de cómo Django llama SPs de reporte en MariaDB y serializa el resultado.

---

## Gap 4 — `source/requisitos/reglas-negocio/br-016-tasa-abandono.rst`

**Estado:** INCOMPLETO — la fórmula abstracta es correcta pero falta la
implementación concreta.

| Claim en source/ | Realidad | Severidad |
|---|---|---|
| `tasa_abandono = (llamadas_abandonadas / llamadas_recibidas) * 100` | Correcto a nivel conceptual | OK |
| `llamadas_abandonadas`: "el cliente colgó antes de ser atendido" | Implementación real: `menu IN ('VACIO','cliente_colgo','SinOpcion_Cabecera')` (D-21) | GAP (enriquecimiento) |
| Sin mención de `cliente_colgo` vs `VACIO` vs `SinOpcion_Cabecera` | El SP actual solo cuenta `VACIO` (~8-9%). Con definición completa: ~27-28% | GAP SIGNIFICATIVO |
| Thresholds 5% / 10% | Estos umbrales son incompatibles con la realidad: el SP actual reporta 8-9% (sub-conteo). Con definición real el valor típico es 27-28%, invalidando los umbrales. | ALTA |

**Corrección requerida:** Agregar sección "Implementación en sistema IVR IACT"
con los tres tipos de abandono (VACIO / cliente_colgo / SinOpcion_Cabecera)
y recalibrar los umbrales operativos a la realidad del IVR.

---

## Gap 5 — `source/requisitos/casos-uso/pipeline/uc-pip-01..04/`

**Estado:** CONCEPTUALMENTE VÁLIDO, implementación incorrecta.

Los UCs describen monitoreo de ETL (salud, errores, disponibilidad, reintentos).
El **concepto es correcto** — IACT necesita estas capacidades.
El **mecanismo de implementación** descrito es incorrecto.

| Claim en UCs | Realidad | Severidad |
|---|---|---|
| `PipelineRun` entity con `started_at`, `completed_at`, `rows_processed` | No existe este modelo. El ETL es `CALL sp_etl_maestro(...)` — el tracking requiere una tabla MariaDB de logs del SP, no un modelo Django | ALTA |
| `ETLError` entity con stack trace sanitizado | No existe. Los errores del SP se propagan al caller (Django o cron job) | ALTA |
| "Compatible con Airflow/Prefect/custom" | Solo MariaDB SPs. El scheduler externo solo lanza el CALL | ALTA |
| Flujos conceptuales (dashboard health, error drill-down, retry) | Válidos en concepto — solo cambia la implementación | OK conceptual |

**Decisión de corrección:** Los UCs no necesitan reescritura conceptual completa.
Solo las secciones `datos-involucrados.rst` e `implementacion-tecnica.rst`
de cada UC necesitan actualizarse para reflejar el mecanismo SP-based.

---

## Archivos que NO necesitan corrección (pipeline scope)

| Archivo | Razón |
|---|---|
| `uc-pip-01..04/informacion-general.rst` | Objetivo del UC correcto |
| `uc-pip-01..04/flujo-principal.rst` | Flujo correcto a nivel de actor/sistema |
| `uc-pip-01..04/criterios-aceptacion.rst` | Criterios independientes de implementación |
| `uc-pip-01..04/testing.rst` | Tests independientes de implementación |
| `etl-pipeline.rst` sección CNST_008 | Restricción de frecuencia correcta |
| `modelo-dual.rst` sección 1 (MySQL fuente) | Correcto |
| `modelo-dual.rst` CNST_007 | Correcto |

---

## Orden de trabajo recomendado

El criterio es: mayor severidad primero, archivos con dependencias antes
de los que dependen de ellos.

| Prioridad | Archivo | Cambio principal |
|---|---|---|
| 1 | `databases/modelo-dual.rst` | Corregir BD destino ETL: MariaDB, no PostgreSQL |
| 2 | `databases/etl-pipeline.rst` | Reescribir secciones 2-4: SPs en lugar de Python classes |
| 3 | `vis-reports/componentes.rst` | Reemplazar DailyMetrics por sp_rpt_* pattern |
| 4 | `br-016-tasa-abandono.rst` | Agregar implementación real (VACIO+cliente_colgo+SinOpcion_Cabecera), recalibrar umbrales |
| 5 | `uc-pip-01..04/datos-involucrados.rst` | Actualizar entidades a tablas/SPs reales |
| 6 | `uc-pip-01..04/implementacion-tecnica.rst` | Actualizar a mecanismo SP-based |

Total: ~10 archivos a editar.

---

## Preguntas que quedan abiertas antes de editar

Estas preguntas afectan el contenido de las correcciones:

| # | Pregunta | Afecta a |
|---|---|---|
| Q-01 | ¿Existe realmente una BD PostgreSQL para tablas operacionales de Django (users, RBAC, audit_log)? | `modelo-dual.rst` — si sí existe, la dualidad es correcta pero el rol de PostgreSQL cambia |
| Q-02 | ¿Hay una tabla de tracking de runs del ETL en MariaDB? ¿O el SP no registra inicio/fin/filas procesadas? | `uc-pip-01` datos-involucrados — sin tabla de tracking, el UC de monitoring necesita ser rediseñado |
| Q-03 | ¿Los umbrales operativos de BR-016 (5%/10%) son valores de negocio reales o fueron inventados? | `br-016-tasa-abandono.rst` — si son reales, deben revisarse contra el nuevo denominador |

**Estrategia:** Responder Q-01 y Q-02 antes de editar `modelo-dual.rst` y
`uc-pip-01/datos-involucrados.rst`. Q-03 puede responderse con los datos
reales: ~27-28% actual vs umbrales 5/10% → los umbrales están calibrados
para otro tipo de call center (muy bajo volumen de abandono), no para IACT.

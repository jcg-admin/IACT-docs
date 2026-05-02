```yml
created_at: 2026-05-02 07:47:25
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Corrección de Arquitectura ETL — MySQL-internal vs Python+PostgreSQL

> **HALLAZGO CRÍTICO:** La arquitectura ETL documentada actualmente en `source/` es
> incorrecta. Este documento registra la arquitectura real y el plan de corrección.

---

## 1. Divergencia entre documentado y real (PROVEN)

### Arquitectura documentada actualmente en source/ (INCORRECTA)

```
MySQL IVR (cliente)
    ↓ SELECT (Python extractors)
Python ETL (django-crontab / Celery Beat)
    ↓ INSERT/UPSERT
PostgreSQL Analytics (IACT)
    ↓ SELECT (Django ORM)
Django app → reportes
```

**Archivos con esta arquitectura incorrecta:**
- `source/databases/etl-pipeline.rst` — menciona "BD PostgreSQL Analytics", `etl/extractors/`, `etl/transformers/`, `etl/loaders/`
- `source/normativa/restricciones/cnst-008-*.rst` — menciona `django-crontab`, `django-crontab`, modelo `ETLRun`
- `source/arquitectura-tecnica/modulos/etl-monitoring/componentes.rst` — modelo `ETLExecution` como modelo Django
- `source/requisitos/reglas-negocio/br-002-etl-batch-nocturno.rst` — menciona Celery Beat, "Base Analytics"
- `source/normativa/estandares/plantillas/tpl-etl-job-etl-job.rst` — template Python para ETL jobs

### Arquitectura real (PROVEN — confirmada por el equipo)

```
MySQL IVR (cliente)
    tbl_historico_t1_2025
    tbl_historico_t2_2025
    tbl_historico_t3_2025
    tbl_historico_tN_YYYY ...
         ↓
    MySQL ETL interno
    (Stored Procedures + Functions + Events/Jobs + Triggers)
         ↓ limpieza + transformación + aggregación
    MySQL — tablas limpias por reporte
    (una tabla por tipo de reporte)
         ↓ SELECT solo
Django app
    → lee ÚNICAMENTE de las tablas limpias
    → módulo de monitoreo observa si el ETL MySQL ejecutó correctamente
```

---

## 2. Componentes del ETL MySQL (PROVEN — confirmado por equipo)

| Componente MySQL | Propósito |
|---|---|
| **Stored Procedures (SP)** | Lógica principal de limpieza y transformación de datos |
| **Functions** | Funciones de apoyo: `fn_es_dia_habil()`, `fn_agregar_dias_habiles()`, `fn_contar_dias_habiles()`, normalización `cDID_Centro_Transferencia`, etc. |
| **Events / Jobs** | Scheduler interno MySQL — dispara los SPs en ventana programada |
| **Triggers** | Posiblemente para mantener integridad en tablas limpias |
| **Tablas limpias** | Una tabla por tipo de reporte — destino final del ETL |

---

## 3. Rol de Django (PROVEN — confirmado por equipo)

**Django hace DOS cosas relacionadas con el ETL:**

1. **Consumo de datos** — Lee ÚNICAMENTE las tablas limpias MySQL para servir reportes.
   No conecta a PostgreSQL. No ejecuta el ETL. Solo SELECT.

2. **Módulo de monitoreo** — Observa si el ETL MySQL se ejecutó correctamente.
   Esto implica que Django necesita acceso a algún mecanismo de tracking del ETL:
   - ¿Una tabla de log en MySQL que los SPs actualizan?
   - ¿MySQL `information_schema` o `performance_schema`?
   - ¿Una tabla `etl_executions` que el SP popula al inicio/fin de cada run?

**INFERRED:** El módulo de monitoreo de Django leerá una tabla de tracking del ETL
(e.g. `etl_executions` o similar) que los Stored Procedures populan.

---

## 4. Impacto en documentación existente

### 4.1 Archivos que deben ser reescritos (BREAKING CHANGE)

| Archivo | Problema | Corrección requerida |
|---|---|---|
| `source/databases/etl-pipeline.rst` | Dice "PostgreSQL Analytics", extractors/transformers/loaders Python | Reescribir para MySQL-internal SPs + tablas limpias |
| `source/normativa/restricciones/cnst-008-*.rst` | Menciona `django-crontab`, `ETLRun` Python | Actualizar: scheduler es MySQL Events, tracking es tabla MySQL |
| `source/arquitectura-tecnica/modulos/etl-monitoring/componentes.rst` | `ETLExecution` como modelo Django | Cambiar: Django lee tabla MySQL de tracking, no modelo propio |
| `source/requisitos/reglas-negocio/br-002-etl-batch-nocturno.rst` | Menciona Celery Beat, "Base Analytics" | Corregir: MySQL Event scheduler, tablas limpias MySQL |
| `source/normativa/estandares/plantillas/tpl-etl-job-etl-job.rst` | Template Python para ETL | Cambiar a template SP MySQL |

### 4.2 Nuevas restricciones (CNST) que deben crearse

| ID sugerido | Enunciado |
|---|---|
| `CNST-ETL-001` | El ETL se ejecuta EXCLUSIVAMENTE dentro de MySQL mediante Stored Procedures, Functions y Events. No existe un proceso Python ETL externo. |
| `CNST-ETL-002` | Django lee ÚNICAMENTE de las tablas limpias MySQL. No ejecuta ninguna transformación de datos. |
| `CNST-ETL-003` | Existe una tabla por tipo de reporte (clean table). Su estructura es estable para el consumo por Django. |
| `CNST-ETL-004` | El monitoreo del ETL se realiza leyendo la tabla de tracking del ETL en MySQL. |

### 4.3 Nuevos documentos que deben crearse

| Documento | Contenido |
|---|---|
| `source/databases/mysql-ivr-schema.rst` | Schema real: `tbl_historico_tN_YYYY`, columnas reales, funciones de BD |
| `source/databases/mysql-clean-tables.rst` | Catálogo de tablas limpias por reporte, su estructura y el SP que las genera |
| `source/databases/mysql-etl-sp-catalog.rst` | Catálogo de SPs y funciones del ETL, parámetros, frecuencia |
| `source/arquitectura-tecnica/modulos/etl-monitoring/etl-tracking-table.rst` | Schema de la tabla de tracking que los SPs actualizan |

---

## 5. Modelo de datos real para el módulo de monitoreo (INFERRED)

Si Django va a mostrar si el ETL se ejecutó correctamente, necesita leer algo
de MySQL. El modelo más natural es una tabla de tracking que los SPs populan:

```sql
-- Tabla propuesta (a confirmar con equipo)
CREATE TABLE etl_executions (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    job_name        VARCHAR(100),        -- nombre del SP/proceso
    quarter_name    VARCHAR(10),         -- 'Q01_25', 'Q02_25', etc.
    started_at      DATETIME,
    finished_at     DATETIME,
    status          ENUM('RUNNING','SUCCESS','FAILED'),
    records_source  INT DEFAULT 0,       -- rows leídas de tbl_historico_*
    records_clean   INT DEFAULT 0,       -- rows insertadas en tabla limpia
    error_message   TEXT,
    executed_by     VARCHAR(100)         -- 'EVENT:etl_q1_nightly' o 'MANUAL:admin'
);
```

Django leerá esta tabla via un modelo mapeado (read-only), sin ORM write access.

**Los modelos `ETLExecution` y `DataAvailability` actuales en Django** pueden mantenerse
como modelos Python que mapean a esta tabla MySQL — pero la tabla es owned por MySQL,
no creada por Django migrations.

---

## 6. Patrón "tabla limpia por reporte" (PROVEN)

El equipo confirmó: **una tabla limpia por tipo de reporte.**

Implicaciones:
- Los UCs de reportes consultan una tabla MySQL específica, no una query compleja sobre raw data
- El SP del ETL genera/regenera esa tabla limpia (TRUNCATE + INSERT o UPSERT)
- Django solo necesita hacer `SELECT * FROM rpt_transfer_menu_opcion WHERE ...`
- La query compleja (con los CASE WHEN de normalización) está encapsulada en el SP, no en Django

Ejemplo de naming para tablas limpias (INFERRED — pendiente confirmación):

| SP origen | Tabla limpia | Reporte que sirve |
|---|---|---|
| `sp_etl_transfer_menu_opcion` | `rpt_transfer_menu_opcion` | Análisis transfer/menu/opción |
| `sp_etl_clientes_unicos` | `rpt_clientes_unicos` | Clientes únicos por DID y trimestre |
| `sp_etl_llamadas_abandonadas` | `rpt_llamadas_abandonadas` | Llamadas abandonadas por menú |
| `sp_etl_centros_transferencia` | `rpt_centros_transferencia` | Centros de transferencia con métricas |

---

## 7. Correcciones de CNST existentes

### CNST-008 (actual: "Sincronización ETL 6-12 horas")

La restricción de frecuencia sigue siendo válida, pero el mecanismo cambia:

| Aspecto | Documentado (incorrecto) | Real |
|---|---|---|
| Mecanismo scheduler | `django-crontab` / Celery Beat | MySQL Events / MySQL Event Scheduler |
| Proceso ETL | Python (`etl/extractors/`) | MySQL Stored Procedures |
| Tracking | Modelo `ETLRun` Django | Tabla `etl_executions` MySQL (read-only para Django) |
| Destino | PostgreSQL Analytics | Tablas limpias MySQL |
| Herramientas prohibidas | Debezium, WebSockets, CDC | Igual — sigue prohibido |

### CNST-006 y CNST-007 (BD Dual)

**CNST-006** (arquitectura BD dual) y **CNST-007** (IVR read-only) mencionan dos BDs
separadas. Con la nueva arquitectura:
- Solo hay UNA BD MySQL (no dos BDs separadas)
- La restricción de "solo lectura en IVR" aplica a los SPs del ETL sobre `tbl_historico_*`
- Las tablas limpias están en la misma instancia MySQL pero son owned por IACT

---

## 8. Preguntas abiertas (requieren confirmación del equipo)

| # | Pregunta | Impacto |
|---|---|---|
| P-01 | ¿Hay una tabla de tracking del ETL? ¿Qué nombre tiene? ¿Qué columnas? | Define el modelo Django de monitoreo |
| P-02 | ¿Las tablas limpias siguen el naming `rpt_*`? ¿O tienen otra convención? | Define los modelos Django y las queries |
| P-03 | ¿Los Events/Jobs MySQL son diarios o por trimestre? ¿Se disparan manualmente? | Define BR_002 corrección |
| P-04 | ¿Los SPs hacen TRUNCATE+INSERT o UPSERT en tablas limpias? | Implica idempotencia en UC_PIP_04 |
| P-05 | ¿Las tablas limpias incluyen `quarter_name` ('Q01_25') para filtrar? | Define queries de reportes en Django |
| P-06 | ¿Django puede triggear manualmente un SP? (UC_PIP_04: solicitar reintento) | Define el flujo de "retry" |
| P-07 | ¿Hay una base de datos IACT separada de la base IVR del cliente, aunque ambas sean MySQL? | Crítico para CNST-006/007 |

---

## 9. Orden de acciones en source/ (INFERRED — para siguiente fase)

Prioridad de correcciones una vez confirmadas las preguntas P-01..P-07:

1. **Actualizar `source/databases/etl-pipeline.rst`** — reescribir para MySQL-internal
2. **Crear `source/databases/mysql-ivr-schema.rst`** — schema real `tbl_historico_*`
3. **Crear `source/databases/mysql-clean-tables.rst`** — catálogo tablas limpias
4. **Actualizar CNST-008** — mecanismo correcto (MySQL Events, no django-crontab)
5. **Actualizar CNST-006/007** — arquitectura single-MySQL o dual-MySQL (confirmar P-07)
6. **Actualizar BR_002** — Celery → MySQL Event Scheduler
7. **Actualizar `etl-monitoring/componentes.rst`** — modelos Django read-only desde MySQL
8. **Crear `source/databases/mysql-etl-sp-catalog.rst`** — catálogo de SPs
9. **Deepen UC_PIP_01..04** con arquitectura correcta

---

## 10. Lo que NO cambia con esta corrección

- El **módulo de monitoreo existe** — Django sí muestra estado del ETL (UC_PIP_01..04 siguen siendo válidos en concepto)
- La **restricción de frecuencia** 6-12h sigue siendo válida
- Los **datos IVR son read-only** para el sistema (aunque el ETL corre en MySQL, los SPs solo leen `tbl_historico_*` y escriben en tablas limpias propias)
- La **latencia de datos** (6-12h) sigue siendo una restricción para reportes
- Los **4 UCs del pipeline** siguen siendo necesarios — solo cambia qué tecnología monitorean

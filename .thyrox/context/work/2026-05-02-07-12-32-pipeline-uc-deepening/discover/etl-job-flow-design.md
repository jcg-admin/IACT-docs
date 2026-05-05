```yml
created_at: 2026-05-02 08:44:41
updated_at: 2026-05-02 15:00:00
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 2.4.0
```

# Diagrama de Flujo del Proceso ETL — IACT

## Sistema IACT: Procesamiento y Carga de Datos del IVR

---

## Información del Documento

| Aspecto | Detalle |
|---|---|
| **Proyecto** | IACT-2025-001 |
| **Proceso** | ETL MySQL-interno: SPs + Events + Triggers |
| **Tecnología** | **MariaDB 10.1.48** — Stored Procedures + MySQL Event Scheduler |
| **Restricción SQL** | MariaDB 10.1.48 no tiene window functions — usar subconsultas (CNST-ETL-007). **Actualización de MariaDB fuera de scope.** |
| **Restricción SQL** | Tabla fuente es dinámica — requiere PREPARE/EXECUTE (CNST-ETL-008) |
| **Carga diaria** | Solo quarter actual — calculado con YEAR()/QUARTER() (D-20, D-22) |
| **Carga histórica** | `sp_etl_historico(year, quarter_num)` — ejecución manual una sola vez |
| **Frecuencia** | Diaria (02:00 AM) — D-08 |
| **Restricción crítica** | Solo lectura en tablas IVR — CNST-ETL-001, CNST-ETL-002 |
| **Sin índices en fuente** | `tbl_historico_*` NO tienen índices — CNST-ETL-005 |
| **Tablas destino** | 2 tablas base con índices (D-18) — `base_ivr_detalle` + `base_ivr_clientes` |
| **Reportes** | SPs de reporte llamados por Django bajo demanda (D-19) |

### DIDs de segmentos (valores únicos y correctos)

| Variable | DID | Segmento |
|---|---|---|
| Puebla | `19020084` | Centro Puebla |
| Nacional A | `19028031` | Centro Nacional (línea A) |
| Nacional B | `19020001` | Centro Nacional (línea B) |

> **Regla obligatoria:** Todo filtro sobre `cDID_800Transfer` incluye los 3 DIDs
> en un solo `WHERE IN (19020084, 19028031, 19020001)`. Nunca omitir uno.

---

## Por qué 2 tablas base en lugar de 7 tablas de reporte

### El problema: millones de registros + sin índices

```
tbl_historico_t3_2025
  ~14M filas, sin índices (CNST-ETL-005)
       │
       │  Full table scan INEVITABLE en cada lectura
       │  Tiempo estimado: 5-20 minutos por scan
       │
       ▼
  Diseño anterior (7 tablas rpt_*):
  7 SPs de ETL × 1 scan cada uno = 7 scans nocturnos
  → mismos millones de registros procesados 7 veces

  Diseño nuevo (2 tablas base):
  1 SP de ETL × 1 scan = 1 scan nocturno
  → millones de registros procesados 1 sola vez
```

### La separación que resuelve el problema

```
ETL nocturno (caro — se paga una vez por noche):
  tbl_historico_* (~14M filas, sin índice)
       │
       │  1 scan  →  GROUP BY de 14M filas
       │              resultado: miles de filas
       ▼
  base_ivr_detalle  (miles de filas, CON índices)
  base_ivr_clientes (filas mínimas, CON índices)
       │
Reporte bajo demanda (barato — milisegundos):
       │  SELECT sobre miles de filas indexadas
       ▼
  sp_rpt_*(@quarter, @params)  →  Django  →  Usuario
```

### Ventajas del nuevo diseño

| Dimensión | 7 tablas rpt_* | 2 tablas base |
|---|---|---|
| Scans de `tbl_historico_*` por noche | 7 scans | 1 scan |
| Nuevo reporte necesario | Nuevo ETL SP + nueva tabla + datos | Solo nuevo SP de reporte |
| Django lee | Tabla directamente (schema coupling) | Result set del SP (desacoplado) |
| Parámetros dinámicos | No — tabla estática | Sí — SP recibe @quarter, @segmento, etc. |
| Duplicación de datos | Alta — mismos datos en N tablas | Ninguna — fuente única |

---

## Arquitectura general

```
EVENT: evt_etl_diario  (diariamente 02:00 AM — D-08)
  └── CALL sp_etl_maestro()
        │
        ├── CALL sp_etl_base_detalle(@quarter, @inicio, @fin)
        │     └── 1 scan tbl_historico_tN_YYYY
        │         → DELETE + INSERT base_ivr_detalle
        │
        └── CALL sp_etl_base_clientes(@quarter, @inicio, @fin)
              └── 1 scan tbl_historico_tN_YYYY (COUNT DISTINCT)
                  → DELETE + INSERT base_ivr_clientes

SPs de reporte (llamados por Django bajo demanda — D-19):
  sp_rpt_centros_transferencia(@quarter, @segmento)
  sp_rpt_menu_centro(@quarter, @segmento)
  sp_rpt_llamadas_abandonadas(@quarter)
  sp_rpt_cMENU_ERROR(@quarter)
  sp_rpt_colgadas(@quarter)
  sp_rpt_menu_redirigidos(@quarter)
  sp_rpt_clientes_unicos(@quarter)
```

### Separación ETL SPs vs Reporting SPs

| Tipo | Nombre | Quién lo llama | Operación |
|---|---|---|---|
| **ETL SP** | `sp_etl_base_*` | MySQL Event (nocturno) | Lee `tbl_historico_*` → escribe tablas base |
| **Reporting SP** | `sp_rpt_*` | Django (bajo demanda) | Lee tablas base → retorna result set |

> D-09 aplica SOLO a ETL SPs — Django no puede disparar el ETL.
> Los Reporting SPs son read-only y Django los llama libremente.

---

## Tablas base — schemas

### base_ivr_detalle

Grain: una fila por combinación única de
`(quarter_name, fecha_mes, segmento, centro_transferencia, menu, opcion)`.

Contiene todas las métricas aditivas (COUNT, SUM).
Fuente para todos los reportes excepto `sp_rpt_clientes_unicos`.

```sql
CREATE TABLE base_ivr_detalle (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name          VARCHAR(10)   NOT NULL,  -- 'Q01_25','Q02_25','Q03_25'
    fecha                 VARCHAR(6)    NOT NULL,  -- YYYYMM: '202507'
    segmento              VARCHAR(20)   NOT NULL,  -- 'Puebla','nacional_A','nacional_B'
    centro_transferencia  VARCHAR(100)  NOT NULL,  -- normalizado: DID, 'CASO_NULL',
                                                   -- 'CASO_ERROR_CEROS','CLIENTE_COLGO'
    menu                  VARCHAR(100)  NOT NULL,  -- normalizado: nombre literal o 'VACIO'
    opcion                VARCHAR(100)  NOT NULL,  -- normalizado: nombre, 'SIN_OPCION'
    total_llamadas        INT           NOT NULL DEFAULT 0,
    misma_linea           INT           NOT NULL DEFAULT 0,  -- cTelefono_Origen = Digitado
    linea_diferente       INT           NOT NULL DEFAULT 0,
    no_digito_telefono    INT           NOT NULL DEFAULT 0,  -- cTelefono_Digitado IS NULL

    INDEX idx_quarter           (quarter_name),
    INDEX idx_quarter_fecha     (quarter_name, fecha),
    INDEX idx_quarter_segmento  (quarter_name, segmento),
    INDEX idx_quarter_menu      (quarter_name, menu),
    INDEX idx_quarter_centro    (quarter_name, centro_transferencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### base_ivr_clientes

Separada de `base_ivr_detalle` porque `COUNT(DISTINCT cTelefono_Digitado)` es
**no aditivo** — no puede derivarse sumando filas de `base_ivr_detalle`.
Requiere su propio scan sobre la fuente.

```sql
CREATE TABLE base_ivr_clientes (
    id               INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name     VARCHAR(10)  NOT NULL,  -- 'Q01_25','Q02_25','Q03_25'
    segmento         VARCHAR(20)  NOT NULL,  -- 'Puebla','nacional_A','nacional_B'
    clientes_unicos  INT          NOT NULL DEFAULT 0,

    INDEX idx_quarter           (quarter_name),
    INDEX idx_quarter_segmento  (quarter_name, segmento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Sentinels de calidad de datos (valores canonizados)

| Sentinel / Valor especial | Condición de origen en `tbl_historico_*` | Columna en tabla base | Nota |
|---|---|---|---|
| `'CASO_NULL'` | `cDID_Centro_Transferencia` IS NULL o vacío | `centro_transferencia` | — |
| `'CASO_ERROR_CEROS'` | `cDID_Centro_Transferencia REGEXP '^0+$'` | `centro_transferencia` | — |
| `'CLIENTE_COLGO'` | `cDID_Centro_Transferencia = 'cliente_colgo'` | `centro_transferencia` | Llamada terminada por cliente |
| `'VACIO'` | `cMenu IS NULL` / `TRIM(cMenu) = ''` / `cMenu = 'sin cMenu'` | `menu` | Generado por ETL. Mismo valor usado por el script de análisis histórico — convención unificada (D-24). |
| `'SIN_OPCION'` | `cOpcion IS NULL` o vacío | `opcion` | — |
| `'Desborde_Cabecera'` | `cMenu = 'Desborde_Cabecera'` (valor literal) | `menu` | **NO es sentinel** — valor válido. Indica enrutamiento por `cEtiquetacliente` (BR-ROUTING-002). No se normaliza. |

**Nota NK90 (BR-ROUTING-001):** Cuando `LENGTH(cDID_Centro_Transferencia) > 10`,
los últimos 10 dígitos son `cTelefono_Digitado` concatenado por la infraestructura
NK90 (en migración a IPVR). El VDN real = `LEFT(..., LENGTH - 10)`. Esta
normalización es permanente para datos históricos.

---

## D-23 — "Total Nacional" en SPs de reporte requiere unión de nacional_A + nacional_B

**Decisión:** Los SPs de reporte que muestren métricas "Nacional" como entidad
consolidada DEBEN filtrar `WHERE segmento IN ('nacional_A', 'nacional_B')` y sumar.
Nunca filtrar por un solo segmento cuando se quiere el total Nacional.

**Razón:** Nacional tiene dos líneas físicas separadas con DIDs distintos:
- `nacional_A` — DID 19028031 (línea principal, volumen dominante)
- `nacional_B` — DID 19020001 (línea secundaria)

Ambas se almacenan como filas independientes en `base_ivr_detalle`. Para reportes
consolidados, el SP debe agregarlas. Los SPs que muestran por segmento individual
(`sp_rpt_centros_transferencia`, `sp_rpt_menu_centro`) reciben `@segmento` como
parámetro — si el usuario pide "Nacional" la capa Django debe pasar
`@segmento = 'Nacional'` y el SP traducirlo al filtro correcto:

```sql
-- CORRECTO — Total Nacional consolidado
WHERE quarter_name = @quarter
  AND segmento IN ('nacional_A', 'nacional_B')

-- INCORRECTO — solo una línea, volúmenes incompletos
WHERE quarter_name = @quarter
  AND segmento = 'nacional_A'
```

**Impacto en los 7 SPs de reporte:**

| SP | Impacto de D-23 |
|---|---|
| `sp_rpt_centros_transferencia` | `@segmento = 'Nacional'` → `IN ('nacional_A','nacional_B')` |
| `sp_rpt_menu_centro` | Ídem |
| `sp_rpt_llamadas_abandonadas` | No usa `@segmento` — afecta si se filtra implícitamente |
| `sp_rpt_cMENU_ERROR` | Sin filtro segmento — sin impacto directo |
| `sp_rpt_colgadas` | Sin filtro segmento — sin impacto directo |
| `sp_rpt_menu_redirigidos` | `@segmento` → ídem |
| `sp_rpt_clientes_unicos` | `nacional_A + nacional_B` en `base_ivr_clientes` — sumar ambas filas |

**Nota de proporciones observadas (Q2-Q3 2025):**
- `nacional_A` domina (~93-99% del volumen Nacional)
- `nacional_B` es residual en Q03_25 Sep 2025 (~95K vs ~8.8M de nacional_A)

---

## Flujo general del proceso

```
┌──────────────────────────────────────────────────────┐
│           INICIO DEL JOB (MySQL Event Scheduler)     │
│           evt_etl_diario → CALL sp_etl_maestro()     │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 1: VALIDACIONES INICIALES                      │
├──────────────────────────────────────────────────────┤
│  • ¿Hay otro Job ejecutándose?                       │
│    SI: registrar SKIP y salir                        │
│    NO: continuar                                     │
│  • Determinar quarter activo por CURDATE()           │
│  • Registrar inicio en job_execution_log             │
│    (status = 'RUNNING')                              │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 2: DETERMINAR QUARTER Y TABLA FUENTE (D-20)    │
├──────────────────────────────────────────────────────┤
│  Cálculo dinámico — funciona para cualquier año.     │
│  Solo se reprocesa el quarter ACTIVO.                │
│                                                      │
│  v_year    = YEAR(CURDATE())      -- ej: 2026        │
│  v_qnum    = QUARTER(CURDATE())   -- ej: 2           │
│  v_quarter = 'Q02_26'                                │
│  v_table   = 'tbl_historico_t2_2026'                 │
│  v_inicio  = '2026-04-01'                            │
│  v_fin     = '2026-06-30'                            │
│                                                      │
│  Quarters pasados: sp_etl_historico(year, qnum)      │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 3: sp_etl_base_detalle                         │
│  (1 scan completo — el más costoso)                  │
├──────────────────────────────────────────────────────┤
│  START TRANSACTION;                                  │
│                                                      │
│  DELETE FROM base_ivr_detalle                        │
│  WHERE quarter_name = @quarter;                      │
│                                                      │
│  INSERT INTO base_ivr_detalle                        │
│    (quarter_name, fecha, segmento,                   │
│     centro_transferencia, menu, opcion,              │
│     total_llamadas, misma_linea,                     │
│     linea_diferente, no_digito_telefono)             │
│  SELECT                                              │
│    @quarter,                                         │
│    DATE_FORMAT(dFecha, '%Y%m'),     -- YYYYMM        │
│    CASE cDID_800Transfer                             │
│      WHEN 19020084 THEN 'Puebla'                     │
│      WHEN 19028031 THEN 'nacional_A'                 │
│      WHEN 19020001 THEN 'nacional_B'                 │
│    END,                                              │
│    -- Normalización cDID_Centro_Transferencia:       │
│    CASE                                              │
│      WHEN TRIM(cDID_Centro_Transferencia) IS NULL    │
│        OR TRIM(cDID_Centro_Transferencia) = ''       │
│        THEN 'CASO_NULL'                              │
│      WHEN cDID_Centro_Transferencia                  │
│        = 'cliente_colgo' THEN 'CLIENTE_COLGO'        │
│      WHEN cDID_Centro_Transferencia                  │
│        REGEXP '^0+$' THEN 'CASO_ERROR_CEROS'         │
│      WHEN LENGTH(cDID_Centro_Transferencia) > 10     │
│        THEN LEFT(cDID_Centro_Transferencia,          │
│             LENGTH(cDID_Centro_Transferencia) - 10)  │
│      ELSE cDID_Centro_Transferencia                  │
│    END,                                              │
│    -- Normalización cMenu:                           │
│    CASE                                              │
│      WHEN cMenu IS NULL              THEN 'VACIO'    │
│      WHEN TRIM(cMenu) = ''           THEN 'VACIO'    │
│      WHEN cMenu = 'sin cMenu'        THEN 'VACIO'    │
│      ELSE cMenu                                      │
│    END,                                              │
│    -- Normalización cOpcion:                         │
│    COALESCE(NULLIF(TRIM(cOpcion),''),'SIN_OPCION'),  │
│    COUNT(*),                                         │
│    SUM(cTelefono_Origen = cTelefono_Digitado),       │
│    SUM(cTelefono_Origen != cTelefono_Digitado),      │
│    SUM(cTelefono_Digitado IS NULL)                   │
│  FROM tbl_historico_tN_YYYY   -- tabla dinámica      │
│  WHERE dFecha BETWEEN @inicio AND @fin               │
│    AND cDID_800Transfer IN                           │
│        (19020084, 19028031, 19020001)                 │
│  GROUP BY 2,3,4,5,6;          -- miles de filas      │
│                                                      │
│  COMMIT;  -- fallo → ROLLBACK automático             │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 4: sp_etl_base_clientes                        │
│  (2do scan — COUNT DISTINCT no aditivo)              │
├──────────────────────────────────────────────────────┤
│  START TRANSACTION;                                  │
│                                                      │
│  DELETE FROM base_ivr_clientes                       │
│  WHERE quarter_name = @quarter;                      │
│                                                      │
│  INSERT INTO base_ivr_clientes                       │
│    (quarter_name, segmento, clientes_unicos)         │
│  SELECT                                              │
│    @quarter,                                         │
│    CASE cDID_800Transfer                             │
│      WHEN 19020084 THEN 'Puebla'                     │
│      WHEN 19028031 THEN 'nacional_A'                 │
│      WHEN 19020001 THEN 'nacional_B'                 │
│    END,                                              │
│    COUNT(DISTINCT cTelefono_Digitado)                │
│  FROM tbl_historico_tN_YYYY                          │
│  WHERE dFecha BETWEEN @inicio AND @fin               │
│    AND cDID_800Transfer IN                           │
│        (19020084, 19028031, 19020001)                 │
│  GROUP BY 2;                  -- 3 filas resultado   │
│                                                      │
│  COMMIT;                                             │
└──────────────────────────────────────────────────────┘
                            ↓
                   ¿Ambos SPs exitosos?
                            ↓
                NO ─────────────────────┐
                │                       ↓
               SÍ            ┌──────────────────────┐
                │             │  MANEJO DE ERROR     │
                ↓             │  • ROLLBACK (auto)   │
┌──────────────────────────┐  │  • status = 'FAILED' │
│  PASO 5: VALIDACIÓN      │  │  • Datos anteriores  │
├──────────────────────────┤  │    conservados       │
│  • COUNT(*) en           │  │  • INSERT INTO       │
│    base_ivr_detalle      │  │    internal_messages │
│    WHERE quarter = @q    │  └──────────────────────┘
│    debe ser > 0          │
│  • COUNT(*) en           │
│    base_ivr_clientes     │
│    WHERE quarter = @q    │
│    debe ser 3 filas       │
│  • Si discrepancia:      │
│    status = 'PARTIAL'    │
└──────────────────────────┘
                ↓
┌──────────────────────────────────────────────────────┐
│  PASO 6: ACTUALIZAR CONTROL                          │
├──────────────────────────────────────────────────────┤
│  UPDATE job_execution_log                            │
│  SET status = 'SUCCESS', end_time = NOW(),           │
│      records_extracted = @count_raw,                 │
│      records_loaded    = @count_base                 │
│  WHERE execution_id = @exec_id;                      │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 7: NOTIFICACIÓN (buzón interno)                │
├──────────────────────────────────────────────────────┤
│  INSERT INTO internal_messages ...                   │
│  ✅ Solo buzón interno                               │
│  ❌ NO email (D-09, BR-087)                          │
│  ❌ Django NO dispara este SP (D-09)                 │
└──────────────────────────────────────────────────────┘
                            ↓
                       FIN DEL JOB
```

---

## SPs de reporte — llamados por Django

Todos read-only sobre `base_ivr_detalle` y `base_ivr_clientes`.
Django llama estos SPs bajo demanda para servir cada vista de reporte.

```sql
-- sp_rpt_clientes_unicos(@quarter)
SELECT quarter_name, segmento, clientes_unicos
FROM   base_ivr_clientes
WHERE  quarter_name = @quarter
ORDER BY segmento;

-- sp_rpt_centros_transferencia(@quarter, @segmento)
-- NOTA: MariaDB 10.1 no tiene window functions. Porcentaje se calcula
-- via subconsulta correlacionada en lugar de OVER(PARTITION BY).
SELECT
    t.fecha,
    t.segmento,
    t.centro_transferencia,
    t.menu,
    t.opcion,
    t.total_llamadas,
    ROUND(t.total_llamadas /
          (SELECT SUM(t2.total_llamadas)
           FROM   base_ivr_detalle t2
           WHERE  t2.quarter_name = t.quarter_name
             AND  t2.fecha        = t.fecha
             AND  t2.segmento     = t.segmento)
          * 100, 7)                  AS porcentaje,
    t.misma_linea,
    t.linea_diferente,
    t.no_digito_telefono
FROM   base_ivr_detalle t
WHERE  t.quarter_name = @quarter
  AND  t.segmento     = @segmento
ORDER BY t.fecha, t.total_llamadas DESC;

-- sp_rpt_llamadas_abandonadas(@quarter)
SELECT
    quarter_name,
    menu,
    SUM(total_llamadas)                                         AS total_llamadas,
    SUM(CASE WHEN menu IN ('VACIO','cliente_colgo','SinOpcion_Cabecera')
             THEN total_llamadas ELSE 0 END)                   AS abandono,
    ROUND(
        SUM(CASE WHEN menu IN ('VACIO','cliente_colgo','SinOpcion_Cabecera')
                 THEN total_llamadas ELSE 0 END)
        / NULLIF(SUM(total_llamadas), 0) * 100, 2)             AS pct_abandono
FROM   base_ivr_detalle
WHERE  quarter_name = @quarter
GROUP BY quarter_name, menu;

-- sp_rpt_cMENU_ERROR(@quarter)
SELECT quarter_name, menu, SUM(total_llamadas) AS total
FROM   base_ivr_detalle
WHERE  quarter_name = @quarter
  AND  menu REGEXP '^[0-9]+'
GROUP BY quarter_name, menu
ORDER BY total DESC;

-- sp_rpt_colgadas(@quarter)
SELECT quarter_name, menu, opcion, SUM(total_llamadas) AS total_llamadas
FROM   base_ivr_detalle
WHERE  quarter_name = @quarter
  AND  centro_transferencia = 'CLIENTE_COLGO'
GROUP BY quarter_name, menu, opcion
ORDER BY total_llamadas DESC;

-- sp_rpt_menu_centro(@quarter, @segmento)
-- NOTA: MariaDB 10.1 no tiene window functions. El total por centro se
-- obtiene con JOIN a subconsulta en lugar de OVER(PARTITION BY).
SELECT
    t.segmento,
    t.centro_transferencia,
    t.menu,
    t.opcion,
    SUM(t.total_llamadas)   AS ejecuciones,
    ROUND(SUM(t.total_llamadas) /
          tot.total_centro * 100, 2) AS pct_dentro_centro
FROM   base_ivr_detalle t
JOIN   (SELECT centro_transferencia,
               SUM(total_llamadas) AS total_centro
        FROM   base_ivr_detalle
        WHERE  quarter_name = @quarter
          AND  segmento     = @segmento
        GROUP BY centro_transferencia) tot
       ON tot.centro_transferencia = t.centro_transferencia
WHERE  t.quarter_name = @quarter
  AND  t.segmento     = @segmento
GROUP BY t.segmento, t.centro_transferencia, t.menu, t.opcion
ORDER BY t.centro_transferencia, ejecuciones DESC;

-- sp_rpt_menu_redirigidos(@quarter)
-- Estructura pendiente de confirmar con el equipo (P-13)
SELECT quarter_name, menu, centro_transferencia,
       SUM(total_llamadas) AS total_llamadas
FROM   base_ivr_detalle
WHERE  quarter_name = @quarter
  AND  centro_transferencia NOT IN
       ('CASO_NULL','CASO_ERROR_CEROS','VACIO')
GROUP BY quarter_name, menu, centro_transferencia
ORDER BY total_llamadas DESC;
```

---

## Cómo Django llama los SPs de reporte

```python
# Django — llamada a SP de reporte (read-only)
from django.db import connections

def get_reporte_centros(quarter_name, segmento):
    with connections['mysql_ivr'].cursor() as cursor:
        cursor.callproc('sp_rpt_centros_transferencia',
                        [quarter_name, segmento])
        columns = [col[0] for col in cursor.description]
        rows    = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]
```

Django recibe un result set — no tiene acoplamiento al schema de `base_ivr_detalle`.
Si el SP cambia internamente (nuevo cálculo, nueva columna), Django solo ve el nuevo result set.

---

## Programación del ETL

```sql
-- Habilitar el scheduler de eventos
SET GLOBAL event_scheduler = ON;

-- Evento maestro: diariamente a las 02:00 AM
CREATE EVENT IF NOT EXISTS evt_etl_diario
ON SCHEDULE EVERY 1 DAY
STARTS '2025-09-01 02:00:00'
ON COMPLETION PRESERVE
ENABLE
COMMENT 'ETL diario IVR → base_ivr_*. D-08.'
DO
    CALL sp_etl_maestro();
```

---

## Tablas de control

### job_execution_log

```sql
CREATE TABLE job_execution_log (
    execution_id       INT AUTO_INCREMENT PRIMARY KEY,
    job_name           VARCHAR(100)  NOT NULL,
    quarter_name       VARCHAR(10)   NOT NULL,
    start_time         DATETIME      NOT NULL,
    end_time           DATETIME,
    status             ENUM('RUNNING','SUCCESS','FAILED','PARTIAL','SKIP') NOT NULL,
    records_extracted  INT           DEFAULT 0,   -- COUNT(*) de tbl_historico_*
    records_loaded     INT           DEFAULT 0,   -- filas en base_ivr_detalle
    error_message      TEXT,
    created_at         TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_job_status  (job_name, status),
    INDEX idx_quarter     (quarter_name),
    INDEX idx_start_time  (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### job_config

```sql
CREATE TABLE job_config (
    config_id          INT AUTO_INCREMENT PRIMARY KEY,
    job_name           VARCHAR(100)  NOT NULL UNIQUE,
    is_enabled         BOOLEAN       DEFAULT TRUE,
    timeout_seconds    INT           DEFAULT 300,
    notify_on_success  BOOLEAN       DEFAULT TRUE,
    notify_on_failure  BOOLEAN       DEFAULT TRUE,
    updated_at         TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
                       ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

INSERT INTO job_config (job_name) VALUES
    ('sp_etl_base_detalle'),
    ('sp_etl_base_clientes');
```

---

## Esqueleto del SP maestro

El maestro calcula el quarter y el nombre de tabla **dinámicamente** a partir de
`YEAR(CURDATE())` y `QUARTER(CURDATE())` — funciona para cualquier año sin
modificación. Se elimina el ELSEIF hardcodeado por año.

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_maestro()
sp_etl_maestro: BEGIN
    DECLARE v_exec_id    INT;
    DECLARE v_year       INT;
    DECLARE v_year_short CHAR(2);
    DECLARE v_qnum       TINYINT;
    DECLARE v_quarter    VARCHAR(10);
    DECLARE v_table      VARCHAR(50);
    DECLARE v_inicio     DATE;
    DECLARE v_fin        DATE;

    -- Calcular quarter activo — válido para cualquier año (D-20)
    SET v_year       = YEAR(CURDATE());
    SET v_year_short = RIGHT(v_year, 2);
    SET v_qnum       = QUARTER(CURDATE());  -- 1..4
    -- Ejemplos: 'Q02_26', 'Q04_27'
    SET v_quarter    = CONCAT('Q', LPAD(v_qnum, 2, '0'), '_', v_year_short);
    -- Ejemplos: 'tbl_historico_t2_2026', 'tbl_historico_t4_2027'
    SET v_table      = CONCAT('tbl_historico_t', v_qnum, '_', v_year);

    -- Rango de fechas estándar (trimestres calendario)
    CASE v_qnum
        WHEN 1 THEN SET v_inicio = CONCAT(v_year,'-01-01');
                    SET v_fin    = CONCAT(v_year,'-03-31');
        WHEN 2 THEN SET v_inicio = CONCAT(v_year,'-04-01');
                    SET v_fin    = CONCAT(v_year,'-06-30');
        WHEN 3 THEN SET v_inicio = CONCAT(v_year,'-07-01');
                    SET v_fin    = CONCAT(v_year,'-09-30');
        WHEN 4 THEN SET v_inicio = CONCAT(v_year,'-10-01');
                    SET v_fin    = CONCAT(v_year,'-12-31');
    END CASE;

    -- Verificar concurrencia
    IF EXISTS (
        SELECT 1 FROM job_execution_log
        WHERE  status = 'RUNNING'
          AND  start_time >= DATE_SUB(NOW(), INTERVAL 6 HOUR)
    ) THEN
        INSERT INTO job_execution_log
            (job_name, quarter_name, start_time, status, error_message)
        VALUES ('sp_etl_maestro', v_quarter, NOW(), 'SKIP',
                'Job anterior aún activo');
        LEAVE sp_etl_maestro;
    END IF;

    -- Registrar inicio
    INSERT INTO job_execution_log
        (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_maestro', v_quarter, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    -- Pasar nombre de tabla dinámico a los SPs ETL (D-21)
    CALL sp_etl_base_detalle(v_quarter, v_inicio, v_fin, v_table);
    CALL sp_etl_base_clientes(v_quarter, v_inicio, v_fin, v_table);

    -- Registrar éxito
    UPDATE job_execution_log
    SET    status = 'SUCCESS', end_time = NOW()
    WHERE  execution_id = v_exec_id;

    -- Notificación buzón interno
    INSERT INTO internal_messages
        (recipient_user_id, subject, body, message_type, created_at)
    SELECT user_id,
           CONCAT('ETL completado — ', v_quarter),
           CONCAT('base_ivr_* actualizadas. Quarter: ', v_quarter,
                  '. Tabla fuente: ', v_table),
           'system', NOW()
    FROM   users WHERE role = 'SYSTEM_ADMIN';

END$$

DELIMITER ;
```

---

## Esqueleto de SP ETL — sp_etl_base_detalle

El SP recibe el nombre de tabla como parámetro `p_table`. Como MariaDB 10.1 no
permite usar una variable como identificador de tabla directamente, se usa
`PREPARE/EXECUTE` con SQL dinámico (CNST-ETL-008).

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_base_detalle(
    IN p_quarter  VARCHAR(10),  -- 'Q02_26'
    IN p_inicio   DATE,         -- '2026-04-01'
    IN p_fin      DATE,         -- '2026-06-30'
    IN p_table    VARCHAR(50)   -- 'tbl_historico_t2_2026'
)
BEGIN
    DECLARE v_exec_id      INT;
    DECLARE v_count_loaded INT DEFAULT 0;

    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        UPDATE job_execution_log
        SET    status = 'FAILED', end_time = NOW(),
               error_message = CONCAT('SQLEXCEPTION — tabla: ', p_table)
        WHERE  execution_id = v_exec_id;
        INSERT INTO internal_messages
            (recipient_user_id, subject, body, message_type, created_at)
        SELECT user_id, 'ERROR ETL — base_ivr_detalle',
               CONCAT('Falló ETL para ', p_quarter, ', tabla: ', p_table),
               'alert', NOW()
        FROM   users WHERE role = 'SYSTEM_ADMIN';
    END;

    INSERT INTO job_execution_log
        (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_base_detalle', p_quarter, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    START TRANSACTION;

        DELETE FROM base_ivr_detalle
        WHERE  quarter_name = p_quarter;

        -- PREPARE/EXECUTE requerido: el nombre de tabla es dinámico (CNST-ETL-008)
        -- p_quarter/p_inicio/p_fin vienen de lógica interna — no hay riesgo de inyección
        SET @sql = CONCAT('
            INSERT INTO base_ivr_detalle
                (quarter_name, fecha, segmento, centro_transferencia,
                 menu, opcion, total_llamadas, misma_linea,
                 linea_diferente, no_digito_telefono)
            SELECT
                ''', p_quarter, ''',
                DATE_FORMAT(dFecha, ''%Y%m''),
                CASE cDID_800Transfer
                    WHEN 19020084 THEN ''Puebla''
                    WHEN 19028031 THEN ''nacional_A''
                    WHEN 19020001 THEN ''nacional_B''
                END,
                CASE
                    WHEN TRIM(cDID_Centro_Transferencia) IS NULL
                      OR TRIM(cDID_Centro_Transferencia) = ''''
                        THEN ''CASO_NULL''
                    WHEN cDID_Centro_Transferencia = ''cliente_colgo''
                        THEN ''CLIENTE_COLGO''
                    WHEN cDID_Centro_Transferencia REGEXP ''^0+$''
                        THEN ''CASO_ERROR_CEROS''
                    WHEN LENGTH(cDID_Centro_Transferencia) > 10
                        THEN LEFT(cDID_Centro_Transferencia,
                             LENGTH(cDID_Centro_Transferencia) - 10)
                    ELSE cDID_Centro_Transferencia
                END,
                CASE
                    WHEN cMenu IS NULL         THEN ''VACIO''
                    WHEN TRIM(cMenu) = ''''    THEN ''VACIO''
                    WHEN cMenu = ''sin cMenu'' THEN ''VACIO''
                    ELSE cMenu
                END,
                COALESCE(NULLIF(TRIM(cOpcion), ''''), ''SIN_OPCION''),
                COUNT(*),
                SUM(cTelefono_Origen = cTelefono_Digitado),
                SUM(cTelefono_Origen != cTelefono_Digitado),
                SUM(cTelefono_Digitado IS NULL)
            FROM ', p_table, '
            WHERE  dFecha BETWEEN ''', p_inicio, ''' AND ''', p_fin, '''
              AND  cDID_800Transfer IN (19020084, 19028031, 19020001)
            GROUP BY 2, 3, 4, 5, 6
        ');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

    COMMIT;

    SET v_count_loaded = (
        SELECT COUNT(*) FROM base_ivr_detalle
        WHERE  quarter_name = p_quarter
    );

    UPDATE job_execution_log
    SET    status         = IF(v_count_loaded > 0, 'SUCCESS', 'PARTIAL'),
           end_time       = NOW(),
           records_loaded = v_count_loaded
    WHERE  execution_id = v_exec_id;

END$$

DELIMITER ;
```

---

## SP para carga histórica — sp_etl_historico

Carga quarters pasados bajo demanda. El Event Scheduler solo procesa el quarter
actual (D-22). Los quarters históricos (2025, años futuros ya cerrados) se cargan
con este SP ejecutado manualmente una sola vez.

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_historico(
    IN p_year        INT,       -- año completo: 2025, 2026
    IN p_quarter_num TINYINT    -- 1..4
)
BEGIN
    DECLARE v_quarter VARCHAR(10);
    DECLARE v_table   VARCHAR(50);
    DECLARE v_inicio  DATE;
    DECLARE v_fin     DATE;

    SET v_quarter = CONCAT('Q', LPAD(p_quarter_num, 2, '0'), '_', RIGHT(p_year, 2));
    SET v_table   = CONCAT('tbl_historico_t', p_quarter_num, '_', p_year);

    CASE p_quarter_num
        WHEN 1 THEN SET v_inicio = CONCAT(p_year,'-01-01');
                    SET v_fin    = CONCAT(p_year,'-03-31');
        WHEN 2 THEN SET v_inicio = CONCAT(p_year,'-04-01');
                    SET v_fin    = CONCAT(p_year,'-06-30');
        WHEN 3 THEN SET v_inicio = CONCAT(p_year,'-07-01');
                    SET v_fin    = CONCAT(p_year,'-09-30');
        WHEN 4 THEN SET v_inicio = CONCAT(p_year,'-10-01');
                    SET v_fin    = CONCAT(p_year,'-12-31');
    END CASE;

    CALL sp_etl_base_detalle(v_quarter, v_inicio, v_fin, v_table);
    CALL sp_etl_base_clientes(v_quarter, v_inicio, v_fin, v_table);
END$$

DELIMITER ;

-- Carga inicial de datos históricos 2025:
-- CALL sp_etl_historico(2025, 1);  -- Q01_25 (tbl_historico_t1_2025)
-- CALL sp_etl_historico(2025, 2);  -- Q02_25 (tbl_historico_t2_2025)
-- CALL sp_etl_historico(2025, 3);  -- Q03_25 (tbl_historico_t3_2025)
-- CALL sp_etl_historico(2025, 4);  -- Q04_25 (tbl_historico_t4_2025)
```

---

## Manejo de errores

| Error | Acción | Notificación |
|---|---|---|
| SQLEXCEPTION | EXIT HANDLER → ROLLBACK → status='FAILED' | `internal_messages` → SYSTEM_ADMIN |
| Count cargado = 0 | COMMIT, status='PARTIAL' | `internal_messages` → SYSTEM_ADMIN |
| Job ya activo | Salir, status='SKIP' | Solo log en `job_execution_log` |
| Quarter no configurado | Salir, status='FAILED' | Solo log en `job_execution_log` |

**Retries:** No hay retry automático. Si un SP falla, los datos del quarter anterior
se conservan intactos en `base_ivr_*` (ROLLBACK los protege). El Event retomará
automáticamente al día siguiente.

---

## Métricas y monitoreo (para UC_PIP_01..03)

```sql
-- Últimas 10 ejecuciones
SELECT
    job_name,
    quarter_name,
    start_time,
    end_time,
    TIMESTAMPDIFF(MINUTE, start_time, end_time) AS duracion_min,
    status,
    records_extracted,
    records_loaded,
    error_message
FROM   job_execution_log
ORDER BY start_time DESC
LIMIT 10;

-- Estado actual de base_ivr_* por quarter (UC_PIP_03 — disponibilidad)
SELECT
    quarter_name,
    MAX(end_time)                                             AS ultima_actualizacion,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)      AS runs_exitosos,
    SUM(CASE WHEN status = 'FAILED'  THEN 1 ELSE 0 END)      AS runs_fallidos
FROM   job_execution_log
WHERE  job_name IN ('sp_etl_base_detalle','sp_etl_base_clientes')
GROUP BY quarter_name
ORDER BY quarter_name;

-- Estadísticas de la semana (UC_PIP_01 — panel monitoreo)
SELECT
    DATE(start_time)                                          AS fecha,
    COUNT(*)                                                  AS ejecuciones,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)      AS exitosas,
    SUM(CASE WHEN status = 'FAILED'  THEN 1 ELSE 0 END)      AS fallidas,
    AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time))          AS promedio_min
FROM   job_execution_log
WHERE  start_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(start_time)
ORDER BY fecha DESC;
```

---

## Pendientes de confirmar con el equipo

| # | Pregunta | Impacto |
|---|---|---|
| P-13 | ¿`sp_rpt_menu_redirigidos` usa `base_ivr_detalle` o necesita columnas de `llamadas_QN` (etiquetas, nidMQ)? | Si usa `llamadas_QN`, requiere un 3er scan en el ETL |
| P-14 | ¿`sp_rpt_colgadas` agrupa solo por menu+opcion o hay más dimensiones? | Schema de la query del SP |
| G-28 | ¿`llamadas_cmenu` (cDID, trimestre, cMenu, total) es un reporte derivado de `base_ivr_detalle` o necesita tabla propia? | Si es derivado, no requiere cambios en el ETL |

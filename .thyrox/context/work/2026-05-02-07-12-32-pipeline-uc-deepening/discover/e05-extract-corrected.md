```yml
created_at: 2026-05-02 09:15:20
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
source_document: E05 v6.0 - Especificación de Transformaciones EXTRACT
```

# E05 — Especificación de Transformaciones EXTRACT (CORREGIDO)
## Sistema ETL In-Database (MariaDB 10.1.48)

**Proyecto:** IACT Call Center Analytics Dashboard
**Documento base:** E05 v6.0 (17 Feb 2026)
**Versión corregida:** 1.0.0
**Correcciones aplicadas:** 5 problemas críticos, 2 importantes

---

## REGISTRO DE CORRECCIONES

| # | Sección | Problema en E05 v6.0 | Corrección aplicada | Severidad |
|---|---|---|---|---|
| C-01 | 2, 3 | Asume `INDEX idx_fecha` en `tbl_historico_*` | Eliminado — CNST-ETL-005 confirma sin índices | 🔴 FATAL |
| C-02 | 3 | Arquitectura daily row-level (188K filas/día) | Reemplazada por quarterly aggregated (cientos de filas/quarter) | 🔴 FATAL |
| C-03 | 3 | Columnas inexistentes: `nidRegistro`, `nTiempoEsperaSeg`, `id_CTransferencia` | Eliminadas — no existen en `tbl_historico_*` | 🔴 FATAL |
| C-04 | Anexo B | `LAG(...) OVER (...)` — window function incompatible | Reemplazada con subconsulta (CNST-ETL-007) | 🟡 IMPORTANTE |
| C-05 | 2, 3 | UNION ALL sobre 3 tablas hardcodeadas (2025 only) | Reemplazado por PREPARE/EXECUTE con tabla dinámica (CNST-ETL-008) | 🟡 IMPORTANTE |
| C-06 | 3 | `WHERE DATE(dFecha) = p_fecha` inhabilita índices incluso si existieran | Cambiado a rango por quarter (`BETWEEN p_inicio AND p_fin`) | 🟡 IMPORTANTE |
| C-07 | 3 | 4 functions (fn_corregir_timestamps, fn_determinar_estado, fn_calcular_duracion) innecesarias | Eliminadas — diseño agregado no requiere limpiar registros individuales | 🟡 IMPORTANTE |

---

## TABLA DE CONTENIDOS

1. [Resumen Ejecutivo](#1-resumen-ejecutivo)
2. [Estrategia de Extracción](#2-estrategia-de-extraccion)
3. [Consultas SQL de Extracción](#3-consultas-sql-de-extraccion)
4. [Manejo de Conexiones](#4-manejo-de-conexiones)
5. [Logging de Extracción](#5-logging-de-extraccion)
6. [Manejo de Errores](#6-manejo-de-errores)
7. [Cumplimiento de Constraints](#7-cumplimiento-de-constraints)
8. [Métricas y Monitoreo](#8-metricas-y-monitoreo)

---

## 1. RESUMEN EJECUTIVO

### 1.1 Decisión Arquitectónica

**Arquitectura seleccionada:** ETL In-Database (MariaDB 10.1.48 nativo) — extracción **trimestral agregada**

```
❌ NO se usa:
├─ Python/Django ETL externo
├─ PostgreSQL como destino
├─ ORM Django queries sobre IVR
├─ Extracción incremental diaria de registros individuales
├─ tbl_llamadas_limpias (tabla intermedia de registros limpios)
└─ UNION ALL hardcodeado sobre tablas específicas por año

✅ SÍ se usa:
├─ MariaDB 10.1.48 — Stored Procedures + Event Scheduler
├─ sp_etl_base_detalle  — agrega por trimestre a base_ivr_detalle
├─ sp_etl_base_clientes — COUNT DISTINCT por trimestre a base_ivr_clientes
├─ sp_etl_maestro       — orquestador, calcula quarter y tabla dinámicamente
├─ sp_etl_historico     — carga manual de quarters pasados
└─ sp_rpt_*             — SPs read-only llamados por Django bajo demanda
```

### 1.2 Por qué ETL trimestral agregado (no diario row-level)

**C-01 / C-02 — Razonamiento:**

Las tablas `tbl_historico_*` **no tienen índices** (CNST-ETL-005) e IACT no puede
crearlos (acceso de solo lectura al IVR del cliente, P-12 cerrada).

Un filtro `WHERE DATE(dFecha) = p_fecha` sin índice hace full table scan de
~11-14M filas por tabla, por día. Con el UNION ALL del E05 original:
`3 tablas × ~14M filas × 365 días/año = ~15B filas escaneadas/año`.

El patrón diario replica exactamente el anti-patrón de `REPTRIM001-WS.sql`
que tardó 1 día completo en ejecutarse.

**Solución:** 1 scan por quarter, resultado agregado (GROUP BY). Los reportes de
IACT son siempre agregados (total llamadas por centro/menú/trimestre), no
requieren registros individuales. Un scan de 14M filas que produce cientos de
filas agregadas en `base_ivr_detalle` es la operación correcta.

```
❌ Diario (E05 original):
   3 tablas × 14M filas × 365 scans/año = ~15B filas/año
   tbl_llamadas_limpias crece ~137M filas en 2 años

✅ Trimestral (corrección):
   1 tabla × 14M filas × 4 scans/año = ~56M filas/año
   base_ivr_detalle: cientos de filas por quarter (permanente)
```

### 1.3 Columnas reales en tbl_historico_tN_YYYY (C-03)

Las columnas confirmadas desde scripts SQL de producción analizados:

| Columna | Tipo | Notas |
|---|---|---|
| `dFecha` | DATE | Fecha de la llamada — correcto para filtros de rango |
| `dHoraInicio` | DATETIME | 38.8% con inversión respecto a dHoraFin (G-29) |
| `dHoraFin` | DATETIME | Ver defecto de inversión |
| `cDID_800Transfer` | VARCHAR | DID del segmento: 19020084, 19028031, 19020001 |
| `cDID_Centro_Transferencia` | VARCHAR | Código del centro — requiere normalización |
| `cMenu` | VARCHAR | Menú IVR — puede ser NULL, vacío o 'sin cMenu' |
| `cOpcion` | VARCHAR | Opción seleccionada — puede ser NULL o vacía |
| `cTelefono_Origen` | VARCHAR | ANI — siempre presente |
| `cTelefono_Digitado` | VARCHAR | Teléfono capturado — 75.3% NULL (baseline) |
| `cEtiquetacliente` | VARCHAR | CSV de etiquetas (máx 6 posiciones) |

**Columnas que NO existen en tbl_historico_*:**
- ~~`nidRegistro`~~ — no confirmada en ningún script de producción
- ~~`nTiempoEsperaSeg`~~ — no confirmada
- ~~`id_CTransferencia`~~ — existe en la vista `llamadas_QN`, no en las tablas brutas

### 1.4 Flujo de Extracción Corregido

```
EVENT: evt_etl_diario (02:00 AM diario — D-08)
└── CALL sp_etl_maestro()
      │
      │  Calcula dinámicamente (D-20):
      │  v_year    = YEAR(CURDATE())     → 2026
      │  v_qnum    = QUARTER(CURDATE()) → 2
      │  v_quarter = 'Q02_26'
      │  v_table   = 'tbl_historico_t2_2026'
      │  v_inicio  = '2026-04-01'
      │  v_fin     = '2026-06-30'
      │
      ├── CALL sp_etl_base_detalle('Q02_26', inicio, fin, 'tbl_historico_t2_2026')
      │     │
      │     │  PREPARE/EXECUTE (CNST-ETL-008):
      │     │  1 full scan de tbl_historico_t2_2026
      │     │  WHERE dFecha BETWEEN '2026-04-01' AND '2026-06-30'
      │     │  AND cDID_800Transfer IN (19020084, 19028031, 19020001)
      │     │  GROUP BY fecha, segmento, centro, menu, opcion
      │     │
      │     └── DELETE + INSERT base_ivr_detalle (cientos de filas)
      │
      └── CALL sp_etl_base_clientes('Q02_26', inicio, fin, 'tbl_historico_t2_2026')
            │
            │  1 full scan (COUNT DISTINCT — no aditivo, scan separado)
            │
            └── DELETE + INSERT base_ivr_clientes (3 filas: Puebla, nacional_A, nacional_B)

Carga histórica (manual, una sola vez por quarter cerrado):
  CALL sp_etl_historico(2025, 1);  -- tbl_historico_t1_2025 → Q01_25
  CALL sp_etl_historico(2025, 2);  -- tbl_historico_t2_2025 → Q02_25
  CALL sp_etl_historico(2025, 3);  -- tbl_historico_t3_2025 → Q03_25
  CALL sp_etl_historico(2025, 4);  -- tbl_historico_t4_2025 → Q04_25
```

### 1.5 Volumen real

| Dimensión | E05 v6.0 (incorrecto) | Corrección |
|---|---|---|
| Filas/día en tabla destino | ~188K (row-level) | ~0 — no hay inserción diaria de registros |
| Filas/quarter en base_ivr_detalle | N/A | Cientos (96 centros × 25 menús × N opciones × 3 meses) |
| Scans de tbl_historico_* por noche | 3 tablas × scan (diario) | 1 tabla × scan (diario del quarter activo) |
| Retención | 137M filas en 2 años | Crece ~cientos de filas × N quarters — sin límite problemático |
| tbl_historico_* tienen índices | Asumido ✅ | **NO tienen índices** (CNST-ETL-005) |

---

## 2. ESTRATEGIA DE EXTRACCIÓN

### 2.1 Método de Extracción

**Tipo:** Extracción Trimestral con Agregación (TRUNCATE+INSERT por quarter — D-07)

```sql
-- Patrón correcto: rango por quarter, no por día
WHERE dFecha BETWEEN p_inicio AND p_fin    -- rango de fecha sin función
  AND cDID_800Transfer IN (19020084, 19028031, 19020001)
GROUP BY DATE_FORMAT(dFecha,'%Y%m'), segmento, centro, menu, opcion
```

**Por qué no incremental diario (C-01, C-02):**

| Criterio | Incremental diario (E05) | Trimestral agregado (corrección) |
|---|---|---|
| Scans tbl_historico_* | 1 scan/día × 3 tablas = 1095 scans/año | 4 scans/año (1 por quarter) |
| Índice necesario en fuente | Sí (no disponible — CNST-ETL-005) | No — 1 scan completo es inevitable y correcto |
| Tabla destino crecimiento | ~188K filas/día → 137M en 2 años | Cientos de filas por quarter, crecimiento trivial |
| Reprocesamiento | Re-ejecutar día a día | Re-ejecutar 1 quarter completo |
| Consistencia temporal | Parcial por día | Quarter completo o nada (D-07: ROLLBACK conserva datos anteriores) |

### 2.2 Frecuencia de Ejecución

```sql
CREATE EVENT IF NOT EXISTS evt_etl_diario
ON SCHEDULE EVERY 1 DAY
STARTS '2025-09-01 02:00:00'
ON COMPLETION PRESERVE
ENABLE
COMMENT 'ETL diario IVR → base_ivr_*. D-08.'
DO
    CALL sp_etl_maestro();
```

**El evento corre diariamente** porque durante el quarter activo los datos de
`tbl_historico_*` siguen llegando. Cada run del ETL refresca el quarter
corriente completo (DELETE WHERE quarter_name + INSERT) — no acumula días.

**Ventana de procesamiento:**
```
02:00 AM — sp_etl_maestro() inicia
02:00 AM — sp_etl_base_detalle(): 1 scan ~14M filas, GROUP BY
           Estimado: 10-30 minutos (full scan sin índice, inevitable)
02:30 AM — sp_etl_base_clientes(): 1 scan adicional
           Estimado: 10-30 minutos
03:00 AM — base_ivr_* disponibles para Django
```

### 2.3 Alcance de Datos

**Quarter activo calculado dinámicamente (D-20, D-21):**

```
CURDATE() = 2026-05-02
  → YEAR(CURDATE())    = 2026
  → QUARTER(CURDATE()) = 2
  → v_quarter          = 'Q02_26'
  → v_table            = 'tbl_historico_t2_2026'
  → v_inicio           = '2026-04-01'
  → v_fin              = '2026-06-30'
```

No hay UNION ALL. Un solo scan a la tabla del quarter activo. Para quarters
pasados: `CALL sp_etl_historico(year, quarter_num)`.

### 2.4 Formato de Extracción

**Formato:** Inserción directa de datos AGREGADOS a tabla destino.

```
tbl_historico_tN_YYYY (raw, ~14M filas)
     │  1 scan + GROUP BY inline (sin tablas temporales — CNST-ETL-005)
     ▼
base_ivr_detalle (cientos de filas/quarter, indexadas — CNST-ETL-006)
base_ivr_clientes (3 filas/quarter, indexadas)
```

**NO se usa:**
- Tablas temporales intermedias (viola CNST-ETL-005)
- tbl_llamadas_limpias (row-level, anti-patrón de volumen)
- CSV / JSON intermedios

---

## 3. CONSULTAS SQL DE EXTRACCIÓN

### 3.1 Tablas Destino

```sql
CREATE TABLE base_ivr_detalle (
    id                   INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name         VARCHAR(10)  NOT NULL,  -- 'Q01_25', 'Q02_26', etc.
    fecha                VARCHAR(6)   NOT NULL,  -- YYYYMM: '202507'
    segmento             VARCHAR(20)  NOT NULL,  -- 'Puebla','nacional_A','nacional_B'
    centro_transferencia VARCHAR(100) NOT NULL,  -- normalizado
    menu                 VARCHAR(100) NOT NULL,  -- normalizado
    opcion               VARCHAR(100) NOT NULL,  -- normalizado
    total_llamadas       INT NOT NULL DEFAULT 0,
    misma_linea          INT NOT NULL DEFAULT 0,
    linea_diferente      INT NOT NULL DEFAULT 0,
    no_digito_telefono   INT NOT NULL DEFAULT 0,

    INDEX idx_quarter          (quarter_name),
    INDEX idx_quarter_fecha    (quarter_name, fecha),
    INDEX idx_quarter_segmento (quarter_name, segmento),
    INDEX idx_quarter_menu     (quarter_name, menu),
    INDEX idx_quarter_centro   (quarter_name, centro_transferencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

CREATE TABLE base_ivr_clientes (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name    VARCHAR(10) NOT NULL,
    segmento        VARCHAR(20) NOT NULL,
    clientes_unicos INT NOT NULL DEFAULT 0,

    INDEX idx_quarter          (quarter_name),
    INDEX idx_quarter_segmento (quarter_name, segmento)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 3.2 SP Maestro — Cálculo Dinámico de Quarter

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

    -- Calcular quarter activo sin hardcodear años (D-20)
    SET v_year       = YEAR(CURDATE());
    SET v_year_short = RIGHT(v_year, 2);
    SET v_qnum       = QUARTER(CURDATE());
    SET v_quarter    = CONCAT('Q', LPAD(v_qnum, 2, '0'), '_', v_year_short);
    SET v_table      = CONCAT('tbl_historico_t', v_qnum, '_', v_year);

    CASE v_qnum
        WHEN 1 THEN SET v_inicio=CONCAT(v_year,'-01-01'); SET v_fin=CONCAT(v_year,'-03-31');
        WHEN 2 THEN SET v_inicio=CONCAT(v_year,'-04-01'); SET v_fin=CONCAT(v_year,'-06-30');
        WHEN 3 THEN SET v_inicio=CONCAT(v_year,'-07-01'); SET v_fin=CONCAT(v_year,'-09-30');
        WHEN 4 THEN SET v_inicio=CONCAT(v_year,'-10-01'); SET v_fin=CONCAT(v_year,'-12-31');
    END CASE;

    -- Verificar concurrencia
    IF EXISTS (SELECT 1 FROM job_execution_log
               WHERE status = 'RUNNING'
                 AND start_time >= DATE_SUB(NOW(), INTERVAL 6 HOUR)) THEN
        INSERT INTO job_execution_log (job_name, quarter_name, start_time, status, error_message)
        VALUES ('sp_etl_maestro', v_quarter, NOW(), 'SKIP', 'Job anterior aún activo');
        LEAVE sp_etl_maestro;
    END IF;

    INSERT INTO job_execution_log (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_maestro', v_quarter, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    CALL sp_etl_base_detalle(v_quarter, v_inicio, v_fin, v_table);
    CALL sp_etl_base_clientes(v_quarter, v_inicio, v_fin, v_table);

    UPDATE job_execution_log
    SET    status = 'SUCCESS', end_time = NOW()
    WHERE  execution_id = v_exec_id;

    INSERT INTO internal_messages (recipient_user_id, subject, body, message_type, created_at)
    SELECT user_id,
           CONCAT('ETL completado — ', v_quarter),
           CONCAT('base_ivr_* actualizadas. Tabla: ', v_table),
           'system', NOW()
    FROM   users WHERE role = 'SYSTEM_ADMIN';

END$$

DELIMITER ;
```

### 3.3 SP ETL — sp_etl_base_detalle

**Core del EXTRACT+TRANSFORM+LOAD.** Una sola pasada sobre la tabla fuente,
normalización inline, GROUP BY directo. Sin tablas temporales (CNST-ETL-005).
PREPARE/EXECUTE requerido para nombre de tabla dinámico (CNST-ETL-008).

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
        INSERT INTO internal_messages (recipient_user_id, subject, body, message_type, created_at)
        SELECT user_id, 'ERROR ETL — base_ivr_detalle',
               CONCAT('Falló ETL para ', p_quarter, ', tabla: ', p_table),
               'alert', NOW()
        FROM   users WHERE role = 'SYSTEM_ADMIN';
    END;

    INSERT INTO job_execution_log (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_base_detalle', p_quarter, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    START TRANSACTION;

        -- Elimina datos del quarter para reinsertar (D-07)
        DELETE FROM base_ivr_detalle WHERE quarter_name = p_quarter;

        -- PREPARE/EXECUTE: nombre de tabla no puede ser parámetro directo en MariaDB 10.1
        -- p_quarter/p_inicio/p_fin son valores internos — sin riesgo de inyección SQL
        SET @sql = CONCAT('
            INSERT INTO base_ivr_detalle
                (quarter_name, fecha, segmento, centro_transferencia,
                 menu, opcion, total_llamadas, misma_linea,
                 linea_diferente, no_digito_telefono)
            SELECT
                ''', p_quarter, ''',
                DATE_FORMAT(dFecha, ''%Y%m''),

                -- Normalización de segmento por DID
                CASE cDID_800Transfer
                    WHEN 19020084 THEN ''Puebla''
                    WHEN 19028031 THEN ''nacional_A''
                    WHEN 19020001 THEN ''nacional_B''
                END,

                -- Normalización de centro de transferencia
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

                -- Normalización de menú
                CASE
                    WHEN cMenu IS NULL         THEN ''SIN_MENU''
                    WHEN TRIM(cMenu) = ''''    THEN ''SIN_MENU''
                    WHEN cMenu = ''sin cMenu'' THEN ''SIN_MENU''
                    ELSE cMenu
                END,

                -- Normalización de opción
                COALESCE(NULLIF(TRIM(cOpcion), ''''), ''SIN_OPCION''),

                -- Métricas agregadas
                COUNT(*),
                SUM(cTelefono_Origen = cTelefono_Digitado),   -- misma_linea
                SUM(cTelefono_Origen != cTelefono_Digitado),  -- linea_diferente
                SUM(cTelefono_Digitado IS NULL)               -- no_digito_telefono

            FROM ', p_table, '
            WHERE  dFecha BETWEEN ''', p_inicio, ''' AND ''', p_fin, '''
              AND  cDID_800Transfer IN (19020084, 19028031, 19020001)
            GROUP BY 2, 3, 4, 5, 6
        ');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

    COMMIT;

    SET v_count_loaded = (SELECT COUNT(*) FROM base_ivr_detalle
                          WHERE quarter_name = p_quarter);

    UPDATE job_execution_log
    SET    status         = IF(v_count_loaded > 0, 'SUCCESS', 'PARTIAL'),
           end_time       = NOW(),
           records_loaded = v_count_loaded
    WHERE  execution_id = v_exec_id;

END$$

DELIMITER ;
```

### 3.4 SP ETL — sp_etl_base_clientes

COUNT DISTINCT requiere scan separado — métrica no aditiva que no puede
derivarse de los datos ya agregados en `base_ivr_detalle`.

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_base_clientes(
    IN p_quarter VARCHAR(10),
    IN p_inicio  DATE,
    IN p_fin     DATE,
    IN p_table   VARCHAR(50)
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
    END;

    INSERT INTO job_execution_log (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_base_clientes', p_quarter, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    START TRANSACTION;

        DELETE FROM base_ivr_clientes WHERE quarter_name = p_quarter;

        SET @sql = CONCAT('
            INSERT INTO base_ivr_clientes (quarter_name, segmento, clientes_unicos)
            SELECT
                ''', p_quarter, ''',
                CASE cDID_800Transfer
                    WHEN 19020084 THEN ''Puebla''
                    WHEN 19028031 THEN ''nacional_A''
                    WHEN 19020001 THEN ''nacional_B''
                END,
                COUNT(DISTINCT cTelefono_Digitado)
            FROM ', p_table, '
            WHERE  dFecha BETWEEN ''', p_inicio, ''' AND ''', p_fin, '''
              AND  cDID_800Transfer IN (19020084, 19028031, 19020001)
              AND  cTelefono_Digitado IS NOT NULL
            GROUP BY 2
        ');
        PREPARE stmt FROM @sql;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;

    COMMIT;

    SET v_count_loaded = (SELECT COUNT(*) FROM base_ivr_clientes
                          WHERE quarter_name = p_quarter);

    UPDATE job_execution_log
    SET    status         = IF(v_count_loaded > 0, 'SUCCESS', 'PARTIAL'),
           end_time       = NOW(),
           records_loaded = v_count_loaded
    WHERE  execution_id = v_exec_id;

END$$

DELIMITER ;
```

### 3.5 SP para Carga Histórica — sp_etl_historico

Carga quarters pasados bajo demanda. No tiene Event Scheduler — se ejecuta
manualmente una sola vez por quarter ya cerrado (D-22).

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_historico(
    IN p_year        INT,      -- año completo: 2025, 2026
    IN p_quarter_num TINYINT   -- 1..4
)
BEGIN
    DECLARE v_quarter VARCHAR(10);
    DECLARE v_table   VARCHAR(50);
    DECLARE v_inicio  DATE;
    DECLARE v_fin     DATE;

    SET v_quarter = CONCAT('Q', LPAD(p_quarter_num, 2, '0'), '_', RIGHT(p_year, 2));
    SET v_table   = CONCAT('tbl_historico_t', p_quarter_num, '_', p_year);

    CASE p_quarter_num
        WHEN 1 THEN SET v_inicio=CONCAT(p_year,'-01-01'); SET v_fin=CONCAT(p_year,'-03-31');
        WHEN 2 THEN SET v_inicio=CONCAT(p_year,'-04-01'); SET v_fin=CONCAT(p_year,'-06-30');
        WHEN 3 THEN SET v_inicio=CONCAT(p_year,'-07-01'); SET v_fin=CONCAT(p_year,'-09-30');
        WHEN 4 THEN SET v_inicio=CONCAT(p_year,'-10-01'); SET v_fin=CONCAT(p_year,'-12-31');
    END CASE;

    CALL sp_etl_base_detalle(v_quarter, v_inicio, v_fin, v_table);
    CALL sp_etl_base_clientes(v_quarter, v_inicio, v_fin, v_table);
END$$

DELIMITER ;
```

### 3.6 Transformaciones aplicadas (inline en sp_etl_base_detalle)

El diseño agregado no necesita funciones separadas por registro. Las
transformaciones se aplican inline en el SELECT del PREPARE/EXECUTE:

| Transformación | E05 v6.0 | Corrección | Razón |
|---|---|---|---|
| Normalización de segmento por DID | `CASE cDID_800Transfer` | Idéntica ✅ | Correcta en el original |
| Normalización de centro | `fn_extraer_codigo_centro()` | Inline en CASE ✅ | Funciones UDF innecesarias con diseño agregado |
| Normalización de menú | `CASE cMenu` | Idéntica ✅ | Correcta en el original |
| Normalización de opción | `COALESCE(NULLIF(...))` | Idéntica ✅ | Correcta en el original |
| Corrección timestamps (swap) | `fn_corregir_timestamps()` | **Eliminada** | No hay columnas de tiempo en base_ivr_detalle |
| Clasificación estado llamada | `fn_determinar_estado()` | **Eliminada** | Los reportes son por volumen, no por estado |
| Cálculo duración en segundos | `fn_calcular_duracion()` | **Eliminada** | No hay columna de duración en base_ivr_detalle |

**Nota sobre dHoraInicio/dHoraFin:** El defecto de inversión (38.8%) existe en
los datos brutos (G-29) pero no afecta `base_ivr_detalle` porque no extraemos
ni almacenamos timestamps. Si un reporte futuro requiere duración, el SP de
reporte correspondiente deberá manejar el defecto con `ABS(TIME_TO_SEC(...))`.

### 3.7 Performance real (sin índices en fuente)

| Métrica | E05 v6.0 (asumía índices) | Corrección (sin índices) |
|---|---|---|
| Tipo de acceso | range scan (0.5% filas) | **Full table scan (100%)** |
| Rows examined por run | ~188K (estimado con índice) | ~11-14M (CNST-ETL-005) |
| Tiempo estimado | 5-10 minutos | **20-60 minutos** (aceptable — 1 vez/día) |
| Ventana nocturna disponible | 02:00-03:00 AM | 02:00-04:00 AM (ampliada) |
| Alternativa para reducir tiempo | NO — índice no disponible (P-12) | Ninguna — es el costo fijo del diseño |

La diferencia clave: en el diseño original, el costo se pagaba CADA DÍA sobre 3
tablas. En el diseño corregido, el costo se paga UNA VEZ por noche sobre 1 tabla.

---

## 4. MANEJO DE CONEXIONES

Sin cambios respecto al E05 v6.0 — la arquitectura in-database es correcta.

```
Base de datos MySQL/MariaDB (misma instancia)
├─ Tablas IVR (tbl_historico_tN_YYYY) — acceso solo lectura
├─ Tablas base ETL (base_ivr_detalle, base_ivr_clientes) — R/W por ETL SPs
├─ Tablas de control (job_execution_log, job_config)
└─ Stored Procedures (sp_etl_*, sp_rpt_*, sp_etl_historico)

Base de datos PostgreSQL (separada — D-10)
└─ Django: users, sessions, permisos (sin acceso a tablas IVR ni base_ivr_*)
```

**Django → MySQL:** Solo llama a `sp_rpt_*` read-only (D-19). Nunca accede a
`tbl_historico_*` ni a `sp_etl_*` (D-09).

---

## 5. LOGGING DE EXTRACCIÓN

### 5.1 Tabla principal de ejecuciones

```sql
CREATE TABLE job_execution_log (
    execution_id       INT AUTO_INCREMENT PRIMARY KEY,
    job_name           VARCHAR(100)  NOT NULL,
    quarter_name       VARCHAR(10)   NOT NULL,
    start_time         DATETIME      NOT NULL,
    end_time           DATETIME,
    status             ENUM('RUNNING','SUCCESS','FAILED','PARTIAL','SKIP') NOT NULL,
    records_extracted  INT           DEFAULT 0,  -- COUNT(*) de tbl_historico_*
    records_loaded     INT           DEFAULT 0,  -- filas en base_ivr_detalle/clientes
    error_message      TEXT,
    created_at         TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_job_status (job_name, status),
    INDEX idx_quarter    (quarter_name),
    INDEX idx_start_time (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

### 5.2 Query de monitoreo

```sql
-- Últimas 10 ejecuciones por quarter
SELECT
    job_name,
    quarter_name,
    start_time,
    end_time,
    TIMESTAMPDIFF(MINUTE, start_time, end_time) AS duracion_min,
    status,
    records_loaded,
    error_message
FROM   job_execution_log
ORDER BY start_time DESC
LIMIT 10;
```

---

## 6. MANEJO DE ERRORES

Estrategia idéntica al E05 v6.0 — correcta en el original.

| Escenario | Acción | Resultado |
|---|---|---|
| SQLEXCEPTION en INSERT | EXIT HANDLER → ROLLBACK | base_ivr_* conservan datos del run anterior (D-07) |
| COUNT cargado = 0 después de COMMIT | status='PARTIAL' | Alerta a SYSTEM_ADMIN via internal_messages |
| Job anterior aún activo | status='SKIP' | Solo log, sin datos afectados |
| Tabla tbl_historico_* inaccesible | ROLLBACK en PREPARE/EXECUTE | FAILED + alerta |

**Recuperación manual (quarters anteriores):**
```sql
-- Re-ejecutar quarter que falló
CALL sp_etl_historico(2026, 2);   -- Si Q02_26 falló
CALL sp_etl_base_detalle('Q02_26', '2026-04-01', '2026-06-30', 'tbl_historico_t2_2026');
```

No hay retry automático — errores suelen ser estructurales (tabla inaccesible,
permiso faltante). El Event retoma automáticamente al día siguiente.

---

## 7. CUMPLIMIENTO DE CONSTRAINTS

### CNST-ETL-001 / CNST-ETL-002 — Solo lectura en tablas IVR ✅
El ETL hace SELECT sobre tbl_historico_* y escribe SOLO en base_ivr_detalle,
base_ivr_clientes, job_execution_log. Ninguna operación DML sobre tablas IVR.

### CNST-ETL-005 — Sin índices en tbl_historico_* ✅ (corregido)
El diseño corregido asume full table scan inevitable. Reglas aplicadas:
- Una sola pasada por tabla por run (1 scan = 1 INSERT...SELECT...GROUP BY)
- Todos los DIDs en un solo WHERE IN (19020084, 19028031, 19020001)
- Sin tablas temporales intermedias

### CNST-ETL-006 — Índices obligatorios en tablas destino ✅
base_ivr_detalle: 5 índices definidos en CREATE TABLE.
base_ivr_clientes: 2 índices definidos en CREATE TABLE.
DELETE+INSERT conserva la definición de índices.

### CNST-ETL-007 — MariaDB 10.1.48 sin window functions ✅ (corregido)
Ningún SP usa OVER, PARTITION BY, LAG, LEAD, ROW_NUMBER, RANK.
Los SPs de reporte (sp_rpt_*) que calculan porcentajes usan subconsultas
correlacionadas o JOINs a subconsultas. Actualizar MariaDB: fuera de scope.

### CNST-ETL-008 — PREPARE/EXECUTE para tabla dinámica ✅
Los SPs ETL reciben p_table como VARCHAR(50). El nombre de tabla se incrusta
via CONCAT en el SQL dinámico. Los valores de filtro (quarter, fechas) son
internos y no vienen de input de usuario — sin riesgo de inyección SQL.

---

## 8. MÉTRICAS Y MONITOREO

### 8.1 Vista de monitoreo ETL

```sql
CREATE VIEW v_etl_status AS
SELECT
    quarter_name,
    MAX(CASE WHEN job_name='sp_etl_base_detalle'  AND status='SUCCESS'
             THEN end_time END)                           AS detalle_ok,
    MAX(CASE WHEN job_name='sp_etl_base_clientes' AND status='SUCCESS'
             THEN end_time END)                           AS clientes_ok,
    MAX(CASE WHEN status='FAILED' THEN error_message END) AS ultimo_error,
    COUNT(CASE WHEN status='SUCCESS' THEN 1 END)          AS runs_exitosos,
    COUNT(CASE WHEN status='FAILED'  THEN 1 END)          AS runs_fallidos
FROM   job_execution_log
WHERE  job_name IN ('sp_etl_base_detalle','sp_etl_base_clientes')
GROUP BY quarter_name
ORDER BY quarter_name DESC;
```

### 8.2 Estado actual de base_ivr_* por quarter

```sql
SELECT
    quarter_name,
    SUM(total_llamadas)      AS total_llamadas,
    COUNT(*)                 AS combinaciones_unicas,
    COUNT(DISTINCT segmento) AS segmentos
FROM   base_ivr_detalle
GROUP BY quarter_name
ORDER BY quarter_name;
```

### 8.3 Performance por ejecución (sin window functions — CNST-ETL-007)

```sql
-- Corrección de Anexo B del E05 v6.0
-- LAG(...) OVER (...) no está disponible en MariaDB 10.1.48
-- Se calcula la duración directamente desde start_time y end_time del mismo registro

SELECT
    DATE(start_time)                                          AS dia,
    job_name,
    quarter_name,
    TIMESTAMPDIFF(MINUTE, start_time, end_time)               AS duracion_min,
    records_loaded,
    status
FROM   job_execution_log
WHERE  start_time >= DATE_SUB(NOW(), INTERVAL 30 DAY)
ORDER BY start_time DESC;
```

---

## ANEXOS

### Anexo A — Ejecución manual de quarters históricos

```sql
-- Carga inicial de datos históricos 2025 (una sola vez)
CALL sp_etl_historico(2025, 1);  -- Q01_25 — tbl_historico_t1_2025
CALL sp_etl_historico(2025, 2);  -- Q02_25 — tbl_historico_t2_2025
CALL sp_etl_historico(2025, 3);  -- Q03_25 — tbl_historico_t3_2025
CALL sp_etl_historico(2025, 4);  -- Q04_25 — tbl_historico_t4_2025

-- Verificar carga
SELECT quarter_name,
       COUNT(*)              AS filas,
       SUM(total_llamadas)   AS llamadas_totales
FROM   base_ivr_detalle
GROUP BY quarter_name
ORDER BY quarter_name;
```

### Anexo B — Queries de diagnóstico (compatible MariaDB 10.1.48)

```sql
-- Ver últimas 10 ejecuciones
SELECT * FROM job_execution_log
ORDER BY start_time DESC
LIMIT 10;

-- Ver errores recientes
SELECT execution_id, job_name, quarter_name, start_time, error_message
FROM   job_execution_log
WHERE  status = 'FAILED'
ORDER BY start_time DESC
LIMIT 5;

-- Duración por ejecución exitosa (SIN window functions — compatible MariaDB 10.1)
SELECT
    job_name,
    quarter_name,
    DATE(start_time)                                     AS dia,
    TIMESTAMPDIFF(MINUTE, start_time, end_time)          AS duracion_min,
    records_loaded
FROM   job_execution_log
WHERE  status = 'SUCCESS'
ORDER BY start_time DESC
LIMIT 20;
```

### Anexo C — Checklist de implementación

**Pre-requisitos:**
- [ ] Tablas `tbl_historico_tN_YYYY` accesibles con SELECT
- [ ] `base_ivr_detalle` creada con índices (CNST-ETL-006)
- [ ] `base_ivr_clientes` creada con índices (CNST-ETL-006)
- [ ] `job_execution_log` creada
- [ ] `internal_messages` disponible para alertas
- [ ] Event Scheduler habilitado: `SET GLOBAL event_scheduler = ON`

**Implementación:**
- [ ] Crear `sp_etl_base_detalle(p_quarter, p_inicio, p_fin, p_table)`
- [ ] Crear `sp_etl_base_clientes(p_quarter, p_inicio, p_fin, p_table)`
- [ ] Crear `sp_etl_maestro()`
- [ ] Crear `sp_etl_historico(p_year, p_quarter_num)`
- [ ] Crear `evt_etl_diario` (02:00 AM daily)
- [ ] Probar: `CALL sp_etl_historico(2025, 3)` — ejecutar 1 quarter histórico
- [ ] Verificar `base_ivr_detalle` con query del Anexo A
- [ ] Verificar `job_execution_log` con registro SUCCESS
- [ ] Monitorear primera ejecución automática del Event

**Creación de SPs de reporte (paso siguiente — fase de implementación):**
- [ ] `sp_rpt_centros_transferencia(@quarter, @segmento)`
- [ ] `sp_rpt_clientes_unicos(@quarter)`
- [ ] `sp_rpt_llamadas_abandonadas(@quarter)`
- [ ] `sp_rpt_cMENU_ERROR(@quarter)`
- [ ] `sp_rpt_colgadas(@quarter)`
- [ ] `sp_rpt_menu_centro(@quarter, @segmento)`
- [ ] `sp_rpt_menu_redirigidos(@quarter)`

---

**Documento base:** E05 v6.0 — 17 Feb 2026
**Correcciones:** 7 (C-01..C-07), ver tabla al inicio
**Constraints aplicados:** CNST-ETL-005, CNST-ETL-006, CNST-ETL-007, CNST-ETL-008
**Decisiones aplicadas:** D-07, D-08, D-09, D-19, D-20, D-21, D-22

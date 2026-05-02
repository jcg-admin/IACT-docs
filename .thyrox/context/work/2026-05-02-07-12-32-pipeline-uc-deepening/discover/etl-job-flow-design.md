```yml
created_at: 2026-05-02 08:44:41
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
version: 1.0.0
```

# Diagrama de Flujo del Proceso ETL — IACT

## Sistema IACT: Procesamiento y Carga de Datos del IVR

---

## Información del Documento

| Aspecto | Detalle |
|---|---|
| **Proyecto** | IACT-2025-001 |
| **Proceso** | ETL MySQL-interno: SPs + Events + Triggers |
| **Tecnología** | MariaDB — Stored Procedures + MySQL Event Scheduler |
| **Frecuencia** | Diaria (02:00 AM) — D-08 |
| **Restricción crítica** | Solo lectura en tablas IVR — CNST-ETL-001, CNST-ETL-002 |
| **Sin índices en fuente** | `tbl_historico_*` NO tienen índices — CNST-ETL-005 |
| **Tablas destino** | 7 tablas `rpt_*` con índices definidos — D-01, D-02, CNST-ETL-006 |

### DIDs de segmentos (valores únicos y correctos)

| Variable | DID | Segmento |
|---|---|---|
| `@DID_Puebla` | `19020084` | Centro Puebla |
| `@DID_NacionalA` | `19028031` | Centro Nacional (línea A) |
| `@DID_NacionalB` | `19020001` | Centro Nacional (línea B) |

> **Regla obligatoria:** Todo filtro sobre `cDID_800Transfer` debe incluir los 3 DIDs
> en un solo `WHERE IN (19020084, 19028031, 19020001)`. Nunca omitir uno.

---

## Arquitectura general: un SP por tabla rpt_* + SP maestro

```
EVENT: evt_etl_diario  (diariamente 02:00 AM — D-08)
  └── CALL sp_etl_maestro(@quarter_name, @fecha_inicio, @fecha_fin)
        │
        ├── CALL sp_etl_rpt_clientes_unicos(...)
        ├── CALL sp_etl_rpt_centros_transferencia(...)
        ├── CALL sp_etl_rpt_llamadas_abandonadas(...)
        ├── CALL sp_etl_rpt_colgadas(...)
        ├── CALL sp_etl_rpt_menu_centro(...)
        ├── CALL sp_etl_rpt_cMENU_ERROR(...)
        └── CALL sp_etl_rpt_menu_redirigidos(...)
```

**Principios de cada SP individual (CNST-ETL-005):**
- Una sola pasada sobre `tbl_historico_tN_YYYY` — sin queries secundarias sobre la misma tabla
- Los 3 DIDs siempre en un único `WHERE IN`
- Normalización y agregación en el mismo `SELECT` — sin tablas temporales de datos brutos
- Patrón atómico: `DELETE WHERE quarter_name + INSERT` dentro de transacción (D-07)

---

## Tablas de la fuente IVR (solo lectura)

| Tabla | Quarter | Rango de fechas |
|---|---|---|
| `tbl_historico_t1_2025` | Q01_25 | 2025-01-01 → 2025-03-31 |
| `tbl_historico_t2_2025` | Q02_25 | 2025-04-01 → 2025-06-30 |
| `tbl_historico_t3_2025` | Q03_25 | 2025-07-01 → 2025-09-30 |

**Columnas disponibles para el ETL:**

| Columna | Tipo | Uso en ETL |
|---|---|---|
| `dFecha` | DATE | Filtro por rango del quarter |
| `dHoraInicio` | DATETIME | Cálculo de duración (extraer con `TIME()`) |
| `dHoraFin` | DATETIME | Cálculo de duración — **con registros donde inicio > fin** |
| `cDID_800Transfer` | BIGINT | Filtro de segmento y dimensión de reporte |
| `cDID_Centro_Transferencia` | VARCHAR | Requiere normalización compleja (ver Paso 3) |
| `cMenu` | VARCHAR | NULLABLE — normalizar a sentinels |
| `cOpcion` | VARCHAR | NULLABLE — normalizar a sentinels |
| `cTelefono_Origen` | VARCHAR | Identidad del llamante |
| `cTelefono_Digitado` | VARCHAR | Teléfono ingresado por el usuario en el IVR |
| `cEtiquetacliente` | VARCHAR | Etiqueta individual (la vista agrega en CSV) |

> **ADVERTENCIA `dHoraInicio`/`dHoraFin`:** existen registros donde `dHoraInicio > dHoraFin`
> (datos invertidos). Al calcular duración, usar `ABS(TIME_TO_SEC(TIME(dHoraFin)) -
> TIME_TO_SEC(TIME(dHoraInicio)))` como workaround. Para llamadas que cruzan medianoche
> este workaround produce resultados incorrectos — es un defecto conocido de la fuente.

---

## Sentinels de calidad de datos (valores canonizados)

Estos son los valores exactos que deben aparecer en las tablas `rpt_*`:

| Sentinel | Condición de origen | Columnas que lo usan |
|---|---|---|
| `'CASO_NULL'` | Campo raw es NULL o cadena vacía | `centro_transferencia`, `menu`, `opcion` |
| `'CASO_ERROR_CEROS'` | `cDID_Centro_Transferencia REGEXP '^0+$'` | `centro_transferencia` |
| `'CLIENTE_COLGO'` | `cDID_Centro_Transferencia = 'cliente_colgo'` | `centro_transferencia` |
| `'VACIO'` | `TRIM(cMenu) = ''` o `TRIM(cOpcion) = ''` | `menu`, `opcion` |
| `'SIN_MENU'` | `cMenu IS NULL` o `cMenu = 'sin cMenu'` | `menu` |
| `'SIN_OPCION'` | `cOpcion IS NULL` | `opcion` |

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
│    SI: salir (no esperar — el Event dispara mañana)  │
│    NO: continuar                                     │
│  • Determinar quarter activo por CURDATE()           │
│  • Registrar inicio en job_execution_log             │
│    status = 'RUNNING'                                │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 2: DETERMINAR QUARTER Y TABLA FUENTE           │
├──────────────────────────────────────────────────────┤
│  Lógica basada en CURDATE():                         │
│                                                      │
│  IF CURDATE() BETWEEN '2025-01-01' AND '2025-03-31' │
│    SET @quarter = 'Q01_25'                           │
│    SET @tabla   = 'tbl_historico_t1_2025'            │
│    SET @inicio  = '2025-01-01'                       │
│    SET @fin     = '2025-03-31'                       │
│  ELSEIF CURDATE() BETWEEN '2025-04-01' AND '2025-06-30'│
│    SET @quarter = 'Q02_25'                           │
│    SET @tabla   = 'tbl_historico_t2_2025'            │
│    SET @inicio  = '2025-04-01'                       │
│    SET @fin     = '2025-06-30'                       │
│  ELSEIF CURDATE() BETWEEN '2025-07-01' AND '2025-09-30'│
│    SET @quarter = 'Q03_25'                           │
│    SET @tabla   = 'tbl_historico_t3_2025'            │
│    SET @inicio  = '2025-07-01'                       │
│    SET @fin     = '2025-09-30'                       │
│  END IF                                              │
│                                                      │
│  NOTA: Solo se reprocesa el quarter activo. Los      │
│  quarters anteriores ya están en rpt_* y no cambian. │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 3: EXTRACCIÓN + NORMALIZACIÓN (por SP)         │
├──────────────────────────────────────────────────────┤
│  Columnas extraídas de tbl_historico_tN_YYYY:        │
│    dFecha, dHoraInicio, dHoraFin,                    │
│    cDID_800Transfer,                                 │
│    cDID_Centro_Transferencia,                        │
│    cMenu, cOpcion,                                   │
│    cTelefono_Origen, cTelefono_Digitado              │
│                                                      │
│  Filtro obligatorio:                                 │
│    WHERE dFecha BETWEEN @inicio AND @fin             │
│      AND cDID_800Transfer IN                         │
│          (19020084, 19028031, 19020001)               │
│                                                      │
│  Normalización inline (en el mismo SELECT):          │
│                                                      │
│  A) cDID_Centro_Transferencia:                       │
│     CASE                                             │
│       WHEN TRIM(cDID_Centro_Transferencia) IS NULL   │
│         OR TRIM(cDID_Centro_Transferencia) = ''      │
│         THEN 'CASO_NULL'                             │
│       WHEN cDID_Centro_Transferencia                 │
│         = 'cliente_colgo'  THEN 'CLIENTE_COLGO'      │
│       WHEN cDID_Centro_Transferencia                 │
│         REGEXP '^0+$'      THEN 'CASO_ERROR_CEROS'   │
│       WHEN LENGTH(cDID_Centro_Transferencia) > 10    │
│         THEN LEFT(cDID_Centro_Transferencia,         │
│              LENGTH(cDID_Centro_Transferencia) - 10) │
│       ELSE cDID_Centro_Transferencia                 │
│     END AS centro_transferencia                      │
│                                                      │
│  B) cMenu:                                           │
│     CASE                                             │
│       WHEN cMenu IS NULL               THEN 'SIN_MENU'│
│       WHEN TRIM(cMenu) = ''            THEN 'SIN_MENU'│
│       WHEN cMenu = 'sin cMenu'         THEN 'SIN_MENU'│
│       ELSE cMenu                                     │
│     END AS menu                                      │
│                                                      │
│  C) cOpcion:                                         │
│     COALESCE(NULLIF(TRIM(cOpcion), ''), 'SIN_OPCION')│
│     AS opcion                                        │
│                                                      │
│  D) Segmento (label legible):                        │
│     CASE cDID_800Transfer                            │
│       WHEN 19020084 THEN 'Puebla'                    │
│       WHEN 19028031 THEN 'nacional_A'                │
│       WHEN 19020001 THEN 'nacional_B'                │
│     END AS segmento                                  │
│                                                      │
│  E) Campos derivados:                                │
│     (cTelefono_Origen = cTelefono_Digitado)          │
│       AS es_misma_linea                              │
│     (cTelefono_Digitado IS NOT NULL)                 │
│       AS tiene_telefono_digitado                     │
│                                                      │
│  Timeout: 300 segundos máximo por SP                 │
│  Registrar COUNT(*) leído                            │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 4: AGREGACIÓN (en el mismo SELECT del SP)      │
├──────────────────────────────────────────────────────┤
│  Sin tablas temporales de datos brutos (anti-patrón  │
│  documentado — CNST-ETL-005). La agregación ocurre   │
│  dentro del SELECT que va directo a INSERT.          │
│                                                      │
│  Por SP:                                             │
│  ─────────────────────────────────────────────────   │
│  sp_etl_rpt_clientes_unicos:                         │
│    GROUP BY quarter_name, cDID_800Transfer           │
│    COUNT(DISTINCT cTelefono_Digitado)                │
│    → ~3 filas por quarter                            │
│                                                      │
│  sp_etl_rpt_centros_transferencia:                   │
│    GROUP BY quarter_name, fecha(YYYYMM),             │
│             segmento, centro_transferencia,          │
│             menu, opcion                             │
│    COUNT(*), SUM(es_misma_linea),                    │
│    SUM(linea_diferente),                             │
│    SUM(no_digito_telefono),                          │
│    ROUND(COUNT(*) / total_quarter * 100, 7)          │
│    → cientos de filas por quarter                    │
│                                                      │
│  sp_etl_rpt_llamadas_abandonadas:                    │
│    Criterio: cMenu IS NULL OR TRIM(cMenu) = ''       │
│    GROUP BY quarter_name, menu                       │
│    COUNT(*) as total, SUM(abandono), %               │
│                                                      │
│  sp_etl_rpt_cMENU_ERROR:                             │
│    Criterio: cMenu REGEXP '^[0-9]+'                  │
│    GROUP BY quarter_name, cMenu                      │
│    COUNT(*)                                          │
│                                                      │
│  sp_etl_rpt_colgadas:                                │
│    Criterio: cliente colgó sin completar flujo       │
│    GROUP BY quarter_name, menu, opcion               │
│                                                      │
│  sp_etl_rpt_menu_centro:                             │
│    GROUP BY quarter_name, segmento,                  │
│             centro_transferencia, menu, opcion       │
│    COUNT(*), usuarios_unicos, distribución horaria   │
│                                                      │
│  sp_etl_rpt_menu_redirigidos:                        │
│    Usa columnas de vista llamadas_QN:                │
│    etiquetas, nidMQ, id_CTransferencia               │
└──────────────────────────────────────────────────────┘
                            ↓
                   ¿Agregación exitosa?
                            ↓
                   NO ──────────────────┐
                   │                    ↓
                   SÍ       ┌───────────────────────┐
                   ↓        │  MANEJO DE ERROR      │
┌──────────────────────────┐│  • ROLLBACK           │
│  PASO 5: CARGA ATÓMICA  ││  • status = 'FAILED'  │
│  (DELETE + INSERT)       ││  • Registrar error    │
├──────────────────────────┤│  • INSERT INTO        │
│  Para cada SP:           ││    internal_messages  │
│                          ││    (admin RBAC R016)  │
│  START TRANSACTION;      │└───────────────────────┘
│                          │          │
│  DELETE FROM rpt_<tabla> │          │
│  WHERE quarter_name      │          │
│    = @quarter_name;      │◄─────────┘
│                          │   (datos del run anterior
│  INSERT INTO rpt_<tabla> │    conservados en rpt_*)
│  SELECT                  │
│    @quarter_name,        │
│    ...columnas           │
│    ...agregaciones       │
│  FROM tbl_historico_tN   │
│  WHERE dFecha BETWEEN    │
│    @inicio AND @fin      │
│  AND cDID_800Transfer IN │
│    (19020084,19028031,   │
│     19020001)            │
│  GROUP BY ...;           │
│                          │
│  COMMIT;                 │
│                          │
│  Si hay error:           │
│  EXIT HANDLER →          │
│    ROLLBACK automático   │
│    (datos anteriores     │
│     conservados)         │
└──────────────────────────┘
                   ↓
┌──────────────────────────────────────────────────────┐
│  PASO 6: VALIDACIÓN DE RESULTADOS                    │
├──────────────────────────────────────────────────────┤
│  • Contar registros en rpt_* para @quarter_name      │
│  • Verificar que COUNT(*) > 0                        │
│  • Comparar totales: SUM(total_llamadas) en rpt_*    │
│    vs COUNT(*) extraído de tbl_historico_*           │
│  • Si discrepancia > 5%: status = 'PARTIAL'          │
│    y notificar al admin                              │
│  • Registrar records_extracted y records_loaded      │
│    en job_execution_log                              │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 7: ACTUALIZAR CONTROL                          │
├──────────────────────────────────────────────────────┤
│  UPDATE job_execution_log                            │
│  SET                                                 │
│    end_time            = NOW(),                      │
│    status              = 'SUCCESS',                  │
│    records_extracted   = @count_extracted,           │
│    records_loaded      = @count_loaded,              │
│    quarter_name        = @quarter_name               │
│  WHERE execution_id    = @exec_id;                   │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│  PASO 8: NOTIFICACIÓN (buzón interno)                │
├──────────────────────────────────────────────────────┤
│  INSERT INTO internal_messages                       │
│  (recipient_user_id, subject, body,                  │
│   message_type, created_at)                          │
│  SELECT user_id,                                     │
│    CONCAT('ETL completado — ', @quarter_name),       │
│    CONCAT('Registros cargados: ', @count_loaded),    │
│    'system', NOW()                                   │
│  FROM users WHERE role = 'SYSTEM_ADMIN';             │
│                                                      │
│  ✅ Solo buzón interno                               │
│  ❌ NO enviar email (D-09, BR-087)                   │
│  ❌ NO Django puede disparar ni reiniciar el ETL     │
└──────────────────────────────────────────────────────┘
                            ↓
┌──────────────────────────────────────────────────────┐
│                   FIN DEL JOB                        │
│       (Event Scheduler programa siguiente run        │
│        para mañana 02:00 AM automáticamente)         │
└──────────────────────────────────────────────────────┘
```

---

## Diagrama de decisiones

```
                  INICIO JOB
                      │
                      ▼
            ┌─────────────────┐
            │ ¿Job activo en  │
            │ este momento?   │
            └─────────────────┘
                │         │
               SÍ        NO
                │         │
                ▼         ▼
          [SALIR:       [CONTINUAR]
           log SKIP]        │
                            ▼
            ┌─────────────────┐
            │ Determinar      │
            │ quarter activo  │
            │ por CURDATE()   │
            └─────────────────┘
                            │
                            ▼
            ┌─────────────────┐
            │ Para cada SP    │◄────────────────────┐
            │ (7 tablas rpt_*)│                     │
            └─────────────────┘                     │
                            │                       │
                            ▼                       │
            ┌─────────────────┐                     │
            │ ¿SELECT+GROUP   │                     │
            │ BY exitoso?     │                     │
            └─────────────────┘                     │
                │         │                         │
               SÍ        NO                         │
                │         │                         │
                │         ▼                         │
                │    [ROLLBACK]                      │
                │    [status='FAILED']               │
                │    [Notificar admin]               │
                │    [Continuar con                  │
                │     siguiente SP]──────────────────┘
                │
                ▼
            ┌─────────────────┐
            │ ¿COUNT(*)       │
            │ cargado > 0?    │
            └─────────────────┘
                │         │
               SÍ        NO
                │         │
                │         ▼
                │    [status='PARTIAL']
                │    [Notificar admin]
                │         │
                ▼         │
         [Siguiente SP] ◄─┘
                │
    (todos los SPs completados)
                │
                ▼
       [ACTUALIZAR LOG MAESTRO]
                │
                ▼
          [NOTIFICAR]
                │
                ▼
             [FIN]
```

---

## Programación del Job

### EVENT en MariaDB

```sql
-- Habilitar el scheduler de eventos
SET GLOBAL event_scheduler = ON;

-- Crear evento maestro: diariamente a las 02:00 AM
CREATE EVENT IF NOT EXISTS evt_etl_diario
ON SCHEDULE EVERY 1 DAY
STARTS '2025-09-01 02:00:00'
ON COMPLETION PRESERVE
ENABLE
COMMENT 'ETL diario IVR → rpt_*. D-08.'
DO
  CALL sp_etl_maestro();
```

### Frecuencia de actualización por tabla rpt_*

Todas las tablas se procesan en el mismo run diario (D-08).
No hay tablas con frecuencia distinta — el ETL es atómico y uniforme.

| Tabla | Frecuencia | Ventana |
|---|---|---|
| `rpt_clientes_unicos` | Diaria | 02:00 AM |
| `rpt_centros_transferencia` | Diaria | 02:00 AM |
| `rpt_llamadas_abandonadas` | Diaria | 02:00 AM |
| `rpt_colgadas` | Diaria | 02:00 AM |
| `rpt_menu_centro` | Diaria | 02:00 AM |
| `rpt_cMENU_ERROR` | Diaria | 02:00 AM |
| `rpt_menu_redirigidos` | Diaria | 02:00 AM |

---

## Tablas de control

### job_execution_log

```sql
CREATE TABLE job_execution_log (
    execution_id       INT AUTO_INCREMENT PRIMARY KEY,
    job_name           VARCHAR(100)  NOT NULL,
    quarter_name       VARCHAR(10)   NOT NULL,         -- 'Q01_25', 'Q02_25', 'Q03_25'
    start_time         DATETIME      NOT NULL,
    end_time           DATETIME,
    status             ENUM('RUNNING','SUCCESS','FAILED','PARTIAL','SKIP') NOT NULL,
    records_extracted  INT           DEFAULT 0,        -- COUNT(*) de tbl_historico_*
    records_loaded     INT           DEFAULT 0,        -- COUNT(*) insertado en rpt_*
    error_message      TEXT,
    created_at         TIMESTAMP     DEFAULT CURRENT_TIMESTAMP,

    INDEX idx_job_status   (job_name, status),
    INDEX idx_quarter      (quarter_name),
    INDEX idx_start_time   (start_time)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

> **`SKIP`** se usa cuando el job detecta otro run activo y sale sin procesar.
> `records_extracted` refleja el COUNT(*) leído de `tbl_historico_*`.
> `records_loaded` refleja el COUNT(*) insertado en la tabla `rpt_*` correspondiente.

### job_config

```sql
CREATE TABLE job_config (
    config_id          INT AUTO_INCREMENT PRIMARY KEY,
    job_name           VARCHAR(100)  NOT NULL UNIQUE,
    is_enabled         BOOLEAN       DEFAULT TRUE,
    timeout_seconds    INT           DEFAULT 300,
    max_retries        INT           DEFAULT 0,       -- SPs no hacen retry automático
    notify_on_success  BOOLEAN       DEFAULT TRUE,
    notify_on_failure  BOOLEAN       DEFAULT TRUE,
    updated_at         TIMESTAMP     DEFAULT CURRENT_TIMESTAMP
                       ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Configuración inicial
INSERT INTO job_config (job_name, timeout_seconds) VALUES
  ('sp_etl_rpt_clientes_unicos',        300),
  ('sp_etl_rpt_centros_transferencia',  300),
  ('sp_etl_rpt_llamadas_abandonadas',   300),
  ('sp_etl_rpt_colgadas',               300),
  ('sp_etl_rpt_menu_centro',            300),
  ('sp_etl_rpt_cMENU_ERROR',            300),
  ('sp_etl_rpt_menu_redirigidos',       300);
```

---

## Esqueleto de SP maestro

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_maestro()
BEGIN
    DECLARE v_exec_id       INT;
    DECLARE v_quarter       VARCHAR(10);
    DECLARE v_inicio        DATE;
    DECLARE v_fin           DATE;
    DECLARE v_error_msg     TEXT DEFAULT '';

    -- Determinar quarter activo
    IF CURDATE() BETWEEN '2025-01-01' AND '2025-03-31' THEN
        SET v_quarter = 'Q01_25';
        SET v_inicio  = '2025-01-01';
        SET v_fin     = '2025-03-31';
    ELSEIF CURDATE() BETWEEN '2025-04-01' AND '2025-06-30' THEN
        SET v_quarter = 'Q02_25';
        SET v_inicio  = '2025-04-01';
        SET v_fin     = '2025-06-30';
    ELSEIF CURDATE() BETWEEN '2025-07-01' AND '2025-09-30' THEN
        SET v_quarter = 'Q03_25';
        SET v_inicio  = '2025-07-01';
        SET v_fin     = '2025-09-30';
    ELSE
        -- Quarter no configurado — registrar y salir
        INSERT INTO job_execution_log
            (job_name, quarter_name, start_time, status, error_message)
        VALUES ('sp_etl_maestro', 'UNKNOWN', NOW(), 'FAILED',
                'Quarter no configurado para la fecha actual');
        LEAVE sp_etl_maestro;  -- usar label para salir de SP
    END IF;

    -- Verificar concurrencia: ¿hay un run activo?
    IF EXISTS (
        SELECT 1 FROM job_execution_log
        WHERE status = 'RUNNING'
          AND start_time >= DATE_SUB(NOW(), INTERVAL 6 HOUR)
    ) THEN
        INSERT INTO job_execution_log
            (job_name, quarter_name, start_time, status, error_message)
        VALUES ('sp_etl_maestro', v_quarter, NOW(), 'SKIP',
                'Job anterior aún activo — ejecución omitida');
        LEAVE sp_etl_maestro;
    END IF;

    -- Registrar inicio
    INSERT INTO job_execution_log
        (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_maestro', v_quarter, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    -- Ejecutar cada SP de reporte (en orden de menor a mayor complejidad)
    CALL sp_etl_rpt_clientes_unicos(v_quarter, v_inicio, v_fin);
    CALL sp_etl_rpt_centros_transferencia(v_quarter, v_inicio, v_fin);
    CALL sp_etl_rpt_llamadas_abandonadas(v_quarter, v_inicio, v_fin);
    CALL sp_etl_rpt_colgadas(v_quarter, v_inicio, v_fin);
    CALL sp_etl_rpt_menu_centro(v_quarter, v_inicio, v_fin);
    CALL sp_etl_rpt_cMENU_ERROR(v_quarter, v_inicio, v_fin);
    CALL sp_etl_rpt_menu_redirigidos(v_quarter, v_inicio, v_fin);

    -- Registrar éxito
    UPDATE job_execution_log
    SET    status   = 'SUCCESS',
           end_time = NOW()
    WHERE  execution_id = v_exec_id;

    -- Notificar via buzón interno
    INSERT INTO internal_messages
        (recipient_user_id, subject, body, message_type, created_at)
    SELECT user_id,
           CONCAT('ETL completado — ', v_quarter),
           CONCAT('Procesamiento exitoso. Quarter: ', v_quarter,
                  '. Fin: ', NOW()),
           'system',
           NOW()
    FROM   users
    WHERE  role = 'SYSTEM_ADMIN';

END$$

DELIMITER ;
```

---

## Esqueleto de SP individual — ejemplo: rpt_clientes_unicos

```sql
DELIMITER $$

CREATE PROCEDURE sp_etl_rpt_clientes_unicos(
    IN p_quarter_name  VARCHAR(10),
    IN p_fecha_inicio  DATE,
    IN p_fecha_fin     DATE
)
BEGIN
    DECLARE v_exec_id          INT;
    DECLARE v_count_extracted  INT DEFAULT 0;
    DECLARE v_count_loaded     INT DEFAULT 0;
    DECLARE v_tabla_fuente     VARCHAR(50);

    -- Determinar tabla fuente según quarter
    SET v_tabla_fuente = CASE p_quarter_name
        WHEN 'Q01_25' THEN 'tbl_historico_t1_2025'
        WHEN 'Q02_25' THEN 'tbl_historico_t2_2025'
        WHEN 'Q03_25' THEN 'tbl_historico_t3_2025'
    END;

    -- Handler de errores: ROLLBACK + log + notificación
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        UPDATE job_execution_log
        SET    status        = 'FAILED',
               end_time      = NOW(),
               error_message = 'SQLEXCEPTION en sp_etl_rpt_clientes_unicos'
        WHERE  execution_id  = v_exec_id;

        INSERT INTO internal_messages
            (recipient_user_id, subject, body, message_type, created_at)
        SELECT user_id,
               'ERROR ETL — rpt_clientes_unicos',
               CONCAT('Falló el SP para ', p_quarter_name),
               'alert', NOW()
        FROM   users WHERE role = 'SYSTEM_ADMIN';
    END;

    -- Registrar inicio de este SP
    INSERT INTO job_execution_log
        (job_name, quarter_name, start_time, status)
    VALUES ('sp_etl_rpt_clientes_unicos', p_quarter_name, NOW(), 'RUNNING');
    SET v_exec_id = LAST_INSERT_ID();

    -- Contar registros fuente (para validación posterior)
    -- NOTA: este es un segundo scan — evaluar si el costo es aceptable.
    -- Alternativa: usar el COUNT de la inserción como proxy.
    SET v_count_extracted = (
        SELECT COUNT(*)
        FROM   tbl_historico_t1_2025      -- reemplazar dinámicamente por v_tabla_fuente
        WHERE  dFecha BETWEEN p_fecha_inicio AND p_fecha_fin
          AND  cDID_800Transfer IN (19020084, 19028031, 19020001)
    );

    -- Carga atómica: DELETE quarter + INSERT agregado (D-07)
    START TRANSACTION;

        DELETE FROM rpt_clientes_unicos
        WHERE  quarter_name = p_quarter_name;

        INSERT INTO rpt_clientes_unicos
            (quarter_name, cDID_800Transfer, clientes_unicos)
        SELECT
            p_quarter_name,
            cDID_800Transfer,
            COUNT(DISTINCT cTelefono_Digitado) AS clientes_unicos
        FROM   tbl_historico_t1_2025          -- reemplazar dinámicamente por v_tabla_fuente
        WHERE  dFecha BETWEEN p_fecha_inicio AND p_fecha_fin
          AND  cDID_800Transfer IN (19020084, 19028031, 19020001)
        GROUP BY cDID_800Transfer;

    COMMIT;

    -- Registrar registros cargados
    SET v_count_loaded = (
        SELECT COUNT(*) FROM rpt_clientes_unicos
        WHERE  quarter_name = p_quarter_name
    );

    -- Validar: si no se cargó nada, marcar como PARTIAL
    IF v_count_loaded = 0 THEN
        UPDATE job_execution_log
        SET    status             = 'PARTIAL',
               end_time           = NOW(),
               records_extracted  = v_count_extracted,
               records_loaded     = v_count_loaded,
               error_message      = 'Sin registros cargados — verificar datos fuente'
        WHERE  execution_id = v_exec_id;
    ELSE
        UPDATE job_execution_log
        SET    status             = 'SUCCESS',
               end_time           = NOW(),
               records_extracted  = v_count_extracted,
               records_loaded     = v_count_loaded
        WHERE  execution_id = v_exec_id;
    END IF;

END$$

DELIMITER ;
```

> **Nota sobre tablas dinámicas:** MySQL Stored Procedures no admiten nombres de tabla
> dinámicos en SQL estático. Para apuntar a `tbl_historico_t1_2025`, `t2_2025` o `t3_2025`
> según el quarter, se requiere `PREPARE` / `EXECUTE` con SQL dinámico, o un `CASE` que
> replique el SELECT para cada tabla. El esqueleto anterior asume tabla fija para simplificar
> la ilustración — la implementación real debe manejar esto.

---

## CREATE TABLE para las tablas rpt_* (CNST-ETL-006)

Patrón con índices obligatorios:

```sql
-- rpt_clientes_unicos
CREATE TABLE rpt_clientes_unicos (
    id                INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name      VARCHAR(10)   NOT NULL,
    cDID_800Transfer  VARCHAR(20)   NOT NULL,
    clientes_unicos   INT           NOT NULL DEFAULT 0,
    INDEX idx_quarter         (quarter_name),
    INDEX idx_quarter_did     (quarter_name, cDID_800Transfer)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rpt_centros_transferencia
CREATE TABLE rpt_centros_transferencia (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name          VARCHAR(10)    NOT NULL,
    fecha                 VARCHAR(6)     NOT NULL,  -- YYYYMM: '202501'
    segmento              VARCHAR(20)    NOT NULL,  -- 'Puebla','nacional_A','nacional_B'
    centro_transferencia  VARCHAR(100)   NOT NULL,
    menu                  VARCHAR(100)   NOT NULL,
    opcion                VARCHAR(100)   NOT NULL,
    total_llamadas        INT            NOT NULL DEFAULT 0,
    porcentaje            DECIMAL(15,7)  NOT NULL DEFAULT 0,
    misma_linea           INT            NOT NULL DEFAULT 0,
    linea_diferente       INT            NOT NULL DEFAULT 0,
    no_digito_telefono    INT            NOT NULL DEFAULT 0,
    INDEX idx_quarter             (quarter_name),
    INDEX idx_quarter_segmento    (quarter_name, segmento),
    INDEX idx_quarter_centro      (quarter_name, centro_transferencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rpt_llamadas_abandonadas
CREATE TABLE rpt_llamadas_abandonadas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name    VARCHAR(10)   NOT NULL,
    menu            VARCHAR(100)  NOT NULL,
    total_llamadas  INT           NOT NULL DEFAULT 0,
    abandono        INT           NOT NULL DEFAULT 0,
    pct_abandono    DECIMAL(5,2)  NOT NULL DEFAULT 0,
    INDEX idx_quarter      (quarter_name),
    INDEX idx_quarter_menu (quarter_name, menu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rpt_cMENU_ERROR
CREATE TABLE rpt_cMENU_ERROR (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name    VARCHAR(10)   NOT NULL,
    cMenu           VARCHAR(100)  NOT NULL,
    total           INT           NOT NULL DEFAULT 0,
    INDEX idx_quarter  (quarter_name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rpt_colgadas (estructura pendiente de confirmar con el equipo)
CREATE TABLE rpt_colgadas (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name    VARCHAR(10)   NOT NULL,
    menu            VARCHAR(100)  NOT NULL,
    opcion          VARCHAR(100)  NOT NULL,
    total_llamadas  INT           NOT NULL DEFAULT 0,
    INDEX idx_quarter      (quarter_name),
    INDEX idx_quarter_menu (quarter_name, menu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rpt_menu_centro (estructura pendiente de confirmar con el equipo)
CREATE TABLE rpt_menu_centro (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name          VARCHAR(10)   NOT NULL,
    segmento              VARCHAR(20)   NOT NULL,
    centro_transferencia  VARCHAR(100)  NOT NULL,
    menu                  VARCHAR(100)  NOT NULL,
    opcion                VARCHAR(100)  NOT NULL,
    ejecuciones           INT           NOT NULL DEFAULT 0,
    usuarios_unicos       INT           NOT NULL DEFAULT 0,
    ejecuciones_manana    INT           NOT NULL DEFAULT 0,
    ejecuciones_tarde     INT           NOT NULL DEFAULT 0,
    ejecuciones_noche     INT           NOT NULL DEFAULT 0,
    INDEX idx_quarter             (quarter_name),
    INDEX idx_quarter_segmento    (quarter_name, segmento),
    INDEX idx_quarter_menu_centro (quarter_name, menu, centro_transferencia)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- rpt_menu_redirigidos (estructura pendiente de confirmar con el equipo)
CREATE TABLE rpt_menu_redirigidos (
    id                    INT AUTO_INCREMENT PRIMARY KEY,
    quarter_name          VARCHAR(10)   NOT NULL,
    menu                  VARCHAR(100)  NOT NULL,
    centro_transferencia  VARCHAR(100)  NOT NULL,
    total_llamadas        INT           NOT NULL DEFAULT 0,
    INDEX idx_quarter      (quarter_name),
    INDEX idx_quarter_menu (quarter_name, menu)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## Manejo de errores — tipos y acciones

| Tipo de Error | Acción del SP | Notificación |
|---|---|---|
| **SQLEXCEPTION** | EXIT HANDLER → ROLLBACK → status='FAILED' | `internal_messages` al SYSTEM_ADMIN |
| **Count cargado = 0** | COMMIT, status='PARTIAL' | `internal_messages` al SYSTEM_ADMIN |
| **Job ya activo** | Salir sin procesar, status='SKIP' | Log en `job_execution_log` |
| **Quarter no configurado** | Salir, status='FAILED' | Log en `job_execution_log` |
| **Discrepancia fuente vs destino > 5%** | COMMIT, status='PARTIAL' | `internal_messages` al SYSTEM_ADMIN |

**Retries:** Los SPs no implementan retry automático. Si un SP falla:
1. El run diario marca el SP como FAILED en `job_execution_log`
2. Los datos del quarter anterior se conservan en `rpt_*` (ROLLBACK los protege)
3. Al día siguiente, el Event lo reintenta automáticamente
4. Si el admin requiere un reintento manual, debe ejecutar el SP directamente en MySQL
   — Django NO puede disparar SPs (D-09)

---

## Métricas y monitoreo

### KPIs del Job

| Métrica | Objetivo | Alerta si |
|---|---|---|
| Tiempo de ejecución total | < 60 minutos | > 120 minutos |
| Status del run | SUCCESS | FAILED o PARTIAL |
| Registros cargados por tabla | > 0 | = 0 (tabla vacía) |
| Tasa de éxito semanal | 100% | < 95% (5 de 7 días) |

### Queries de monitoreo (para Django — UC_PIP_01, UC_PIP_02, UC_PIP_03)

```sql
-- Ver últimas 10 ejecuciones
SELECT
    job_name,
    quarter_name,
    start_time,
    end_time,
    TIMESTAMPDIFF(MINUTE, start_time, end_time) AS duracion_minutos,
    status,
    records_extracted,
    records_loaded,
    error_message
FROM   job_execution_log
ORDER BY start_time DESC
LIMIT 10;

-- Estado del último run por SP
SELECT
    job_name,
    quarter_name,
    MAX(start_time)  AS ultimo_inicio,
    status,
    records_loaded
FROM   job_execution_log
WHERE  start_time >= DATE_SUB(NOW(), INTERVAL 48 HOUR)
GROUP BY job_name, quarter_name, status
ORDER BY job_name;

-- Disponibilidad de datos por quarter (UC_PIP_03)
SELECT
    quarter_name,
    COUNT(DISTINCT job_name)                                       AS sps_ejecutados,
    SUM(CASE WHEN status = 'SUCCESS'  THEN 1 ELSE 0 END)          AS exitosos,
    SUM(CASE WHEN status = 'FAILED'   THEN 1 ELSE 0 END)          AS fallidos,
    SUM(CASE WHEN status = 'PARTIAL'  THEN 1 ELSE 0 END)          AS parciales,
    MAX(end_time)                                                  AS ultima_actualizacion
FROM   job_execution_log
WHERE  status IN ('SUCCESS', 'FAILED', 'PARTIAL')
GROUP BY quarter_name
ORDER BY quarter_name;

-- Estadísticas de la semana (UC_PIP_01 — panel de monitoreo)
SELECT
    DATE(start_time)                                               AS fecha,
    COUNT(*)                                                       AS ejecuciones,
    SUM(CASE WHEN status = 'SUCCESS' THEN 1 ELSE 0 END)           AS exitosas,
    SUM(CASE WHEN status = 'FAILED'  THEN 1 ELSE 0 END)           AS fallidas,
    AVG(TIMESTAMPDIFF(MINUTE, start_time, end_time))               AS promedio_minutos,
    SUM(records_loaded)                                            AS total_registros_cargados
FROM   job_execution_log
WHERE  start_time >= DATE_SUB(NOW(), INTERVAL 7 DAY)
GROUP BY DATE(start_time)
ORDER BY fecha DESC;
```

---

## Pendientes de confirmar con el equipo

| # | Pregunta | Impacto |
|---|---|---|
| P-13 | ¿La tabla `rpt_menu_redirigidos` usa la vista `llamadas_QN` o directamente `tbl_historico_*`? | Diseño del SP |
| P-14 | ¿`rpt_colgadas` agrupa por menu+opcion o hay más dimensiones? | Schema de la tabla |
| P-15 | ¿`rpt_menu_centro` incluye distribución horaria (mañana/tarde/noche)? | Costo de compute + schema |
| G-28 | ¿`llamadas_cmenu` mapea a `rpt_menu_centro` o es una tabla separada del catálogo D-02? | Catálogo definitivo |

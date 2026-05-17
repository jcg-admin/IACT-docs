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
| **Events / Jobs** | Scheduler interno MySQL — dispara los SPs en ventana programada para poblar las tablas limpias |
| **Triggers** | Se crearán para mantener integridad en las tablas limpias una vez pobladas (PROVEN — confirmado por el equipo 2026-05-02) |
| **Tablas limpias** | Una tabla `rpt_*` por tipo de reporte — destino final del ETL (7 tablas en Scope 1) |

> **DECISIÓN CONFIRMADA (2026-05-02):** Todo el ETL ocurre en MySQL.
> Los triggers y jobs se crearán cuando se llenen las tablas limpias.
> No existe ningún componente Python ni proceso externo involucrado.

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

Naming de tablas limpias (PROVEN — confirmado por el equipo, 2026-05-02):

Prefijo `rpt_` confirmado. 7 tablas limpias para Scope 1:

| SP origen (INFERRED) | Tabla limpia (PROVEN) | Reporte que sirve |
|---|---|---|
| `sp_etl_menu_centro` | `rpt_menu_centro` | Análisis Transfer/Menú/Opción |
| `sp_etl_clientes_unicos` | `rpt_clientes_unicos` | Clientes únicos por DID y trimestre |
| `sp_etl_llamadas_abandonadas` | `rpt_llamadas_abandonadas` | Llamadas abandonadas por menú |
| `sp_etl_centros_transferencia` | `rpt_centros_transferencia` | Centros de transferencia con métricas |
| `sp_etl_colgadas` | `rpt_colgadas` | Análisis colgadas |
| `sp_etl_cMENU_ERROR` | `rpt_cMENU_ERROR` | Menús con número de teléfono (anomalías) |
| `sp_etl_menu_redirigidos` | `rpt_menu_redirigidos` | Menús que redirigen por centro (tabla separada) |

Nota: hay reportes futuros planificados (open clause) pero fuera de Scope 1.

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

### Resueltas

| # | Pregunta | Respuesta | Fecha |
|---|---|---|---|
| P-01 | ¿Hay tabla de tracking del ETL? | No existe aún. Solo existen `tbl_historico_tN_YYYY`. Las tablas limpias se crearán. | 2026-05-02 |
| P-02 | ¿Las tablas limpias usan prefijo `rpt_*`? | **Sí, prefijo `rpt_`** confirmado. 7 tablas: ver sección 6. | 2026-05-02 |
| P-03 | ¿Los Events/Jobs son diarios o por trimestre? | **Diarios.** El ETL corre cada día. | 2026-05-02 |
| P-04 | ¿TRUNCATE+INSERT o UPSERT? | **TRUNCATE+INSERT dentro de transacción.** ETL diario regenera el reporte completo. Si falla → ROLLBACK → tabla conserva datos del día anterior. | 2026-05-02 |
| P-05 | ¿Las tablas limpias incluyen `quarter_name`? | **Sí.** Columna `quarter_name` ('Q01_25', 'Q02_25', 'Q03_25') en todas las tablas limpias para filtrar por trimestre. | 2026-05-02 |
| P-06 | ¿Django puede triggear manualmente un SP? | **No.** Por el momento Django es solo monitoreo — no puede disparar ni reiniciar el ETL. UC_PIP_04 queda reducido a "solicitar reintento" como notificación, no como acción técnica. | 2026-05-02 |
| P-07 | ¿BD IACT separada de BD IVR? | **Misma instancia MySQL.** La única BD separada es PostgreSQL para la aplicación Django (datos de la app: usuarios, sesiones, permisos). | 2026-05-02 |

### Pendientes

Todas las preguntas P-01..P-07 están resueltas.

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

## 10. Funciones de utilidad MySQL confirmadas (PROVEN — de scripts SQL)

Además de las funciones ya documentadas, el equipo proporcionó funciones adicionales:

### 10.1 Catálogo completo de funciones

| Función | Firma | Propósito | Depende de |
|---|---|---|---|
| `fn_es_dia_habil` | `(p_fecha DATE) → BOOLEAN` | Verifica si la fecha es día hábil (lunes-viernes, no festivo) | Tabla `c_dias_festivos` |
| `fn_agregar_dias_habiles` | `(p_fecha_inicio DATE, p_dias INT) → DATE` | Suma o resta días hábiles a una fecha (incluye festivos) | `fn_es_dia_habil`, `c_dias_festivos` |
| `fn_contar_dias_habiles` | `(p_fecha_inicio DATE, p_fecha_fin DATE) → INT` | Cuenta días hábiles entre dos fechas | `fn_es_dia_habil` |
| `fn_extraer_etiqueta` | `(p_etiquetas TEXT, p_posicion INT) → VARCHAR(100)` | Extrae etiqueta por posición de string CSV separado por comas | — |
| `fn_contar_etiquetas` | `(p_etiquetas TEXT) → INT` | Cuenta el total de etiquetas en el CSV | — |
| `fn_actividad_usuario` | `(p_numero_entrada VARCHAR, p_fecha DATE) → TEXT` | Resumen de actividad de un número en una fecha (primera/última llamada + menú) | `llamadas_QN` |

### 10.2 Tabla de soporte: `c_dias_festivos` (PROVEN)

Tabla de catálogo de festivos usada por `fn_es_dia_habil` y `fn_agregar_dias_habiles`:

```sql
c_dias_festivos (
    fecha   DATE,
    activo  CHAR(1)   -- 'S' = es festivo, 'N' = no es festivo
)
```

### 10.3 Campo `etiquetas` — estructura interna (PROVEN)

El campo `etiquetas` en `llamadas_QN` es un CSV separado por comas.
Ejemplos reales del dataset:

```
'2L,ZMB,VSI,NVS,'
'2L,ZMB,SEG_14,'
'ZMB,WTS,'
'2L,ZMB,WTS,NOBOT,PR_MA,'
'ZMB,'
'1L,ZMB,VSI,'
```

Etiquetas identificadas: `1L`, `2L`, `ZMB`, `VSI`, `NVS`, `SEG_14`, `WTS`, `NOBOT`, `PR_MA`, `ML`, `DG`

Máximo de posiciones observado: 6 etiquetas (basado en datos de Q3 2025).

### 10.4 Patrón ETL confirmado: TRUNCATE+INSERT en transacción (D-07)

```sql
-- Patrón estándar para todos los SPs del ETL
START TRANSACTION;
TRUNCATE TABLE rpt_<nombre>;
INSERT INTO rpt_<nombre>
    SELECT ... FROM llamadas_QN WHERE quarter_name = 'QNN_YY';
COMMIT;
-- Si falla: ROLLBACK automático → tabla conserva datos del run anterior
```

---

## 11. Volumen de datos — brutos vs limpios (PROVEN — 2026-05-02)

Datos reales compartidos por el equipo en formato tabular.

### 11.1 Volumen de tablas brutas

| Fuente | Estimación |
|---|---|
| `tbl_historico_t1_2025` + `t2_2025` + `t3_2025` | **~34.1M llamadas** (Q01+Q02+Q03 2025) |
| Por trimestre | ~11–14M llamadas/trimestre |
| Por mes (estimado) | ~4–5M llamadas/mes |

Fuente: suma de `total_llamadas` del reporte `llamadas_cmenu` = 34,101,981.

### 11.2 Volumen de tablas limpias (tablas rpt_*)

Las tablas limpias almacenan datos **AGREGADOS**, no registros individuales:

| Tabla limpia | Filas Q01-Q03 2025 (PROVEN) |
|---|---|
| `rpt_clientes_unicos` | **8 filas** (tabla mínima — 2-3 filas/trimestre) |
| `rpt_centros_transferencia` | Cientos de filas por trimestre/segmento |
| `rpt_llamadas_cmenu` | ~20–30 filas por trimestre/segmento |
| Demás tablas rpt_* | Estimación: decenas a pocos miles de filas/quarter |

### 11.3 Implicación para D-07: TRUNCATE+INSERT — CONFIRMADO CORRECTO (PROVEN)

**Error de interpretación previa:** Preocupación de que TRUNCATE+INSERT sería
ineficiente para "millones de registros". Corrección: los millones de registros
están en `tbl_historico_*` (tablas brutas). Los SPs del ETL **leen** esas tablas
brutas, **agregan** los datos, y **escriben** los agregados en tablas limpias.

```
tbl_historico_* (~34M registros) → SP ETL (SELECT+GROUP BY) → rpt_* (~cientos filas)
```

TRUNCATE+INSERT sobre cientos de filas es trivialmente rápido (<1 segundo).
D-07 queda CONFIRMADO sin ninguna reserva técnica.

### 11.4 Calidad de datos en tablas limpias (PROVEN)

Los SPs del ETL materializan valores sentinel cuando los campos raw están
en estado inválido:

| Sentinel | Aparece en | Origen en tabla bruta |
|---|---|---|
| `CASO_ERROR_CEROS` | `centro_transferencia`, `menu`, `opcion` | `cDID_Centro_Transferencia = 0` o vacío |
| `CASO_NULL` | `centro_transferencia`, `menu`, `opcion` | campo raw = NULL |
| `VACIO` | `menu`, `opcion`, `cMenu` | campo raw = cadena vacía |
| `CLIENTE_COLGO` | `centro_transferencia` | cliente colgó antes de transferencia completa |

**Distribución de `CASO_ERROR_CEROS`:** aparece en Q02_25 y Q03_25, NO en Q01_25.
Esto es consistente con el problema documentado en `dHoraInicio`/`dHoraFin` de
`tbl_historico_t2_2025` y `t3_2025` (G-29 — ver `real-db-schema-analysis.md`).
El problema NO es en `dFecha` — esa columna funciona correctamente como DATE.

---

## 12. Anti-patrón de ETL documentado — REPTRIM001-WS.sql (PROVEN)

Script ad-hoc de agosto 2025 que tardó **1 día completo** en ejecutar.
Documenta el anti-patrón que los SPs de producción deben evitar.

### Anti-patrón:

```sql
-- MAL: materializar ~34M filas en tabla temporal, luego indexar
CREATE TEMPORARY TABLE temp ENGINE=InnoDB AS
SELECT ... FROM tbl_historico_t1_2025 UNION ALL t2 UNION ALL t3;

ALTER TABLE temp ADD INDEX idx_...;  -- reconstruir B-tree sobre 34M filas = lento
```

**Por qué es lento:**
- INSERT masivo de ~34M filas en InnoDB (escritura en disco)
- ALTER TABLE post-carga = O(N log N) sobre 34M filas
- **Full table scans CONFIRMADOS** — `tbl_historico_*` NO tienen índices (PROVEN,
  confirmado por el equipo 2026-05-02). Cada SELECT sobre estas tablas escanea
  la totalidad de ~11-14M filas/quarter sin reducción de I/O.

### Patrón correcto para los SPs de ETL:

```sql
-- BIEN: agregar en el SELECT, escribir solo el resultado en rpt_*
-- Resultado de GROUP BY = centenas de filas (no millones)

START TRANSACTION;
TRUNCATE TABLE rpt_clientes_unicos;
INSERT INTO rpt_clientes_unicos (trimestre, cDID_800Transfer, clientes_unicos)
SELECT 
    'Q01_25',
    cDID_800Transfer,
    COUNT(DISTINCT cTelefono_Digitado)
FROM tbl_historico_t1_2025
WHERE dFecha BETWEEN '2025-01-01' AND '2025-03-31'  -- ← fechas correctas
  AND cDID_800Transfer IN (19020084, 19028031, 19020001)  -- ← DIDs correctos
GROUP BY cDID_800Transfer;
COMMIT;
```

El INSERT escribe ~3 filas (una por DID) — no 11M.

### Bugs del script ad-hoc (a NO reproducir en SPs):

| Bug | Script | Correcto |
|---|---|---|
| `@ONacional02 = 1902001` | 7 dígitos (inválido) | `19020001` |
| `@ONacionalB` ausente en Q2/Q3 | solo Q1 tiene 3 DIDs | todos los quarters: 3 DIDs |
| `@Q1_inicio = '2025-02-01'` | falta enero | `'2025-01-01'` |
| `@Q3_fin = '2025-07-31'` | solo julio | `'2025-09-30'` |

---

## 13. Restricción CNST-ETL-005 — Sin índices en tablas brutas (PROVEN)

**Confirmado por el equipo (2026-05-02):** Las tablas `tbl_historico_tN_YYYY`
NO tienen ningún índice.

**CNST-ETL-005:** Todo acceso a `tbl_historico_tN_YYYY` desde los SPs del ETL
implica un full table scan sobre ~11-14M filas por trimestre. Esta es una
restricción arquitectónica conocida del sistema IVR del cliente — IACT no puede
agregar índices a estas tablas sin coordinación con el proveedor del IVR.

**Implicaciones de diseño obligatorias para los SPs:**

1. **Una sola pasada por tabla por run del ETL.** Nunca hacer N queries separadas
   sobre la misma `tbl_historico_*` en un mismo SP (N pasadas = N × 11-14M filas).

2. **Cubrir todos los DIDs en un solo `WHERE IN`** — no queries separadas por DID:
   ```sql
   -- CORRECTO: un scan, 3 DIDs
   WHERE cDID_800Transfer IN (19020084, 19028031, 19020001)
   
   -- INCORRECTO: 3 scans sobre la misma tabla
   WHERE cDID_800Transfer = 19020084  -- scan 1
   WHERE cDID_800Transfer = 19028031  -- scan 2
   WHERE cDID_800Transfer = 19020001  -- scan 3
   ```

3. **Agregar todo en un solo SELECT+GROUP BY.** El resultado son centenas de filas
   que se escriben directamente en la tabla limpia.

4. **Programar el ETL en ventana nocturna de mínima carga IVR** — los full table scans
   compiten con el I/O del sistema de grabación de llamadas en tiempo real.

5. **No materializar datos brutos en tablas temporales intermedias** — el anti-patrón
   de REPTRIM001-WS (que tardó 1 día) demuestra el costo de esta decisión.

**Estimación de tiempo de scan por tabla** (INFERRED — sin benchmark real):
- InnoDB full scan de ~11-14M filas: típicamente 30-120 segundos dependiendo del
  hardware y carga concurrente
- Con el patrón correcto (una sola query por tabla por SP): 3 scans totales por run
  (uno por `tbl_historico_t1`, `t2`, `t3`)

**P-12 (CERRADA — PROVEN, confirmado 2026-05-02):** No es posible. IACT solo tiene
acceso de lectura a las tablas del IVR. No puede agregar índices a `tbl_historico_*`
ni coordinar cambios de schema con el cliente del IVR.

**Compensación:** Los índices van en las tablas `rpt_*` que IACT crea y controla.
Ver CNST-ETL-006 a continuación.

---

### CNST-ETL-006 — Las tablas rpt_* DEBEN tener índices (PROVEN)

IACT crea y es dueño de las tablas `rpt_*`. Al ser las tablas que Django consulta
para servir reportes, deben tener índices apropiados definidos en el `CREATE TABLE`.

**Por qué TRUNCATE+INSERT NO destruye los índices:**
- `TRUNCATE` elimina todas las filas pero conserva la definición del índice
- El `INSERT` posterior reconstruye el índice sobre las nuevas filas (centenas de filas)
- Reconstruir un índice sobre centenas de filas es trivialmente rápido (<1 segundo)
- No se necesita `DROP INDEX` / `CREATE INDEX` durante el ETL

**Índices mínimos por tabla limpia:**

| Tabla | Índice recomendado | Justificación |
|---|---|---|
| `rpt_clientes_unicos` | `(trimestre)`, `(trimestre, cDID_800Transfer)` | Django filtra por trimestre y segmento |
| `rpt_centros_transferencia` | `(trimestre)`, `(trimestre, 800_transfer)` | Filtros primarios en reporting |
| `rpt_llamadas_abandonadas` | `(trimestre)`, `(trimestre, cMenu)` | Filtro por trimestre y menú |
| `rpt_cMENU_ERROR` | `(trimestre)` | Tabla pequeña, índice simple suficiente |
| `rpt_menu_centro` | `(trimestre)`, `(trimestre, 800_transfer, menu)` | Reporte más complejo |
| `rpt_colgadas` | `(trimestre)` | Estructura por definir |
| `rpt_menu_redirigidos` | `(trimestre)` | Estructura por definir |

**Patrón de CREATE TABLE para todas las tablas limpias:**
```sql
CREATE TABLE rpt_<nombre> (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    trimestre       VARCHAR(10)  NOT NULL,   -- 'Q01_25', 'Q02_25', 'Q03_25'
    ...columnas específicas del reporte...,
    INDEX idx_trimestre (trimestre),
    INDEX idx_trimestre_segment (trimestre, <columna_segmento>)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

---

## 14. Lo que NO cambia con esta corrección

- El **módulo de monitoreo existe** — Django sí muestra estado del ETL (UC_PIP_01..04 siguen siendo válidos en concepto)
- La **restricción de frecuencia** 6-12h sigue siendo válida
- Los **datos IVR son read-only** para el sistema (aunque el ETL corre en MySQL, los SPs solo leen `tbl_historico_*` y escriben en tablas limpias propias)
- La **latencia de datos** (6-12h) sigue siendo una restricción para reportes
- Los **4 UCs del pipeline** siguen siendo necesarios — solo cambia qué tecnología monitorean

```yml
created_at: 2026-05-02 07:35:00
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# IVR Schema Analysis — Tabla ivr_calls y flujo ETL trimestral

## Fuentes consultadas (PROVEN)

- `temp-holding/canonical/TPL_UC_Construccion_7_Pasos_1_3_0.rst` — queries SQL reales
- `temp-holding/canonical/TPL_BR_Decision_Tipo_1_3_0.rst` — queries de validación
- `temp-holding/canonical/PARTE_0_Contexto_Fundamentos_IACT_1_0_0.md` — UC reporte trimestral
- `temp-holding/canonical/PARTE_6_Casos_Practicos_Completos_IACT_1_0_0.md` — implementación Python

---

## 1. Estructura de la tabla ivr_calls (MySQL IVR)

**Hallazgo principal (PROVEN):** `ivr_calls` es **una sola tabla** en MySQL.
No existen tablas físicas separadas por trimestre. El "dividido por trimestre"
es un **particionamiento lógico** implementado con columnas `quarter` y `year`.

### Columnas confirmadas por queries reales

```sql
-- Query confirmada del template UC (TPL_UC_Construccion_7_Pasos_1_3_0.rst)
SELECT
    DATE_TRUNC('day', call_date)       AS dia,
    COUNT(*)                           AS total_llamadas,
    SUM(CASE WHEN status='COMPLETED' THEN 1 ELSE 0 END)  AS completadas,
    SUM(CASE WHEN status='ABANDONED' THEN 1 ELSE 0 END)  AS abandonadas,
    AVG(duration_seconds)              AS duracion_promedio
FROM ivr_calls
WHERE quarter = 'Q3'
  AND year    = 2024
  AND segment = 'OP'
GROUP BY DATE_TRUNC('day', call_date)
ORDER BY dia
```

| Columna | Tipo (inferido) | Descripción | Fuente |
|---|---|---|---|
| `quarter` | ENUM/VARCHAR | 'Q1','Q2','Q3','Q4' — partición lógica trimestral | Query SQL |
| `year` | INT | Año del trimestre (2024, 2025, ...) | Query SQL |
| `segment` | VARCHAR | Segmento de datos: 'OP', 'MG', etc. — aislamiento CNST-008 | Query SQL |
| `call_date` | DATE | Fecha de la llamada | Query SQL |
| `status` | ENUM/VARCHAR | 'COMPLETED', 'ABANDONED' (al menos) | Query SQL |
| `duration_seconds` | INT/NUMERIC | Duración de la llamada en segundos | Query SQL |
| `session_id` | FK → ivr_sessions | FK a tabla de sesiones IVR | PARTE_6 JOIN query |

### Tabla relacionada: ivr_sessions

```sql
-- Join confirmado (PARTE_6_Casos_Practicos)
SELECT COUNT(*) as record_count
FROM ivr_calls c
INNER JOIN ivr_sessions s ON c.session_id = s.session_id
WHERE c.call_date >= :start_date
  AND c.call_date < :end_date
  AND s.user_segment IN (:allowed_segments)
```

| Columna | Tipo (inferido) | Descripción |
|---|---|---|
| `session_id` | PK | Identificador de sesión IVR |
| `user_segment` | VARCHAR | Segmento del agente ('OP', 'MG', etc.) |

**Nota:** `segment` en `ivr_calls` y `user_segment` en `ivr_sessions` parecen
ser equivalentes — el segmento del agente que atendió la llamada.

---

## 2. Índice requerido (PROVEN)

```sql
-- Confirmado en PARTE_0 (performance notes)
INDEX (call_date, center_id, metric_type)
```

El índice cubre el patrón de consulta más frecuente: filtrar por
rango de fecha + centro + tipo de métrica.

Para el patrón `WHERE quarter = 'Q3' AND year = 2024`:
el índice sobre `(quarter, year, segment)` es el más eficiente
para las queries del ETL.

---

## 3. Implicación para el ETL (INFERRED)

### 3.1 Extract — unidad de extracción

El ETL extrae de `ivr_calls` en unidades de **trimestre + segmento**:

```sql
-- Patrón de extracción del ETL (inferido de queries confirmadas)
SELECT *
FROM ivr_calls
WHERE quarter = :quarter  -- 'Q1', 'Q2', 'Q3', 'Q4'
  AND year    = :year     -- 2024, 2025
  AND segment = :segment  -- 'OP', 'MG', ...
```

Esto explica por qué `ETLExecution` tiene campos `date_range_start`
y `date_range_end` — mapean a los límites del trimestre:
- Q1: 01-Ene → 31-Mar
- Q2: 01-Abr → 30-Jun
- Q3: 01-Jul → 30-Sep
- Q4: 01-Oct → 31-Dic

### 3.2 Transform — métricas derivadas calculadas

Por cada trimestre/segmento, el ETL calcula:

| Métrica | Fórmula | Fuente |
|---|---|---|
| `total_llamadas` | `COUNT(*)` | Query principal |
| `completadas` | `SUM(CASE WHEN status='COMPLETED' THEN 1 ELSE 0 END)` | Query principal |
| `abandonadas` | `SUM(CASE WHEN status='ABANDONED' THEN 1 ELSE 0 END)` | Query principal |
| `duracion_promedio` | `AVG(duration_seconds)` | Query principal |
| `tasa_abandono` | `(abandonadas / total_llamadas) * 100` | PARTE_6 / BR-IACT-053 |
| `tasa_abandono_ultima_hora` | query por `NOW() - INTERVAL '1 hour'` | PARTE_6 — alertas |

### 3.3 Load — destino en Analytics

Los datos transformados van a tablas en PostgreSQL Analytics.
Las referencias en los documentos mencionan:
- `analytics_calls` — tabla espejo/derivada de `ivr_calls` en Analytics
- `analytics_centers` — centros de contacto, con `center_id` y `segment_id`

```sql
-- Query de count sobre Analytics (no sobre IVR)
SELECT COUNT(*) as total_records
FROM analytics_calls ac
INNER JOIN analytics_centers ctr ON ac.center_id = ctr.center_id
WHERE ac.call_date BETWEEN :start_date AND :end_date
  AND ac.metric_type = :metric_type
  AND ctr.segment_id = :user_segment_id
```

Esto confirma que el ETL **transforma** la estructura de `ivr_calls` (con
`quarter`/`year` como partición lógica) en `analytics_calls` (con
`call_date`, `center_id`, `metric_type` como estructura analítica).

---

## 4. Implicación para DataAvailability (UC_PIP_03)

`DataAvailability` rastrea qué trimestres ya fueron procesados:

```python
# El period_type='TRIMESTRE' mapea directamente a quarter+year de ivr_calls
DataAvailability(
    period_type  = 'TRIMESTRE',
    period_value = 'Q3-2024',   # format: Q{n}-{year}
    status       = 'COMPLETO',  # COMPLETO | PARCIAL | FALTANTE
    record_count = 42380,       # rows procesadas
    last_updated = datetime(...)
)
```

UC_PIP_03 responde la pregunta: **"¿El trimestre Q3-2024 ya está disponible
en Analytics para los reportes?"**

Respuesta implica verificar que `ETLExecution` con `date_range_start` =
inicio de Q3-2024 y `status='SUCCESS'` existe.

---

## 5. Regla de negocio nueva derivada de este análisis

**BR-derivada (INFERRED — pendiente de formalizar):**

> El ETL DEBE procesar `ivr_calls` en unidades de trimestre completo.
> Un trimestre se considera DISPONIBLE en Analytics cuando el ETL
> completó exitosamente TODOS los `segment` activos para ese
> `quarter + year`. Si al menos un `segment` falla, el trimestre
> se marca `PARCIAL` en `DataAvailability`.

Esta regla NO existe documentada actualmente. Es un gap en la
especificación que debe añadirse al WP de deepening de UCs.

---

## 6. Gaps documentales identificados

| # | Gap | Impacto |
|---|---|---|
| G-01 | Schema completo de `ivr_calls` no está documentado en `source/` | Alto — cualquier UC que mencione la tabla usa datos de inferencia |
| G-02 | `analytics_calls` no tiene schema documentado | Alto — es la tabla de destino del ETL |
| G-03 | `analytics_centers` no está documentada | Medio |
| G-04 | La lógica de `PARCIAL` vs `COMPLETO` en DataAvailability no está especificada | Alto — UC_PIP_03 necesita esta lógica |
| G-05 | No hay BR formal para "trimestre completo = todos los segmentos" | Alto — es la condición de éxito del ETL |
| G-06 | El patrón de extracción por `quarter+year` no está en `databases/etl-pipeline.rst` | Medio |

---

## 7. Qué documentar en `source/databases/` como resultado de este WP

1. Añadir sección a `etl-pipeline.rst`: **"Estructura de extracción por trimestre"**
   — explicar el patrón `WHERE quarter = 'QN' AND year = YYYY`
2. Crear `source/databases/ivr-schema.rst`: schema de `ivr_calls` e `ivr_sessions`
   con todos los campos conocidos
3. Actualizar `DataAvailability` en `etl-monitoring/componentes.rst` con la
   lógica COMPLETO/PARCIAL/FALTANTE ligada a segmentos

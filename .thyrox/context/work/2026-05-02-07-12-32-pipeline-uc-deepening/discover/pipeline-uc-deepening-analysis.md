```yml
created_at: 2026-05-02 07:12:32
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# DISCOVER — Pipeline UC Deepening

## 1. Objetivo del WP

Profundizar los 4 UCs del módulo `MOD_Pipeline` al estándar de
benchmark (12 partes completas, ~2,000+ líneas por UC), partiendo
del inventario de lo que existe hoy y de todo el conocimiento
contextual del sistema ETL de IACT.

---

## 2. Lo que existe hoy

### 2.1 Archivos del módulo pipeline

**Ubicación:** `source/requisitos/casos-uso/pipeline/`

4 UCs × 13 archivos = 52 archivos RST.
**Total actual: 1,604 líneas** (promedio ~30 líneas/archivo).
El benchmark es ~2,000+ líneas *por UC*, no por archivo.

Estado de profundidad por UC:

| UC | Propósito | Líneas totales | Estado |
|---|---|---|---|
| UC_PIP_01 | Ver estado del pipeline (health, lag, throughput) | ~401 | Stub superficial |
| UC_PIP_02 | Ver errores ETL (diagnóstico, stack traces) | ~400 | Stub superficial |
| UC_PIP_03 | Consultar disponibilidad de datos por dataset/periodo | ~400 | Stub superficial |
| UC_PIP_04 | Solicitar reintento de pipeline fallado | ~403 | Stub superficial |

El archivo más largo individual es `uc-pip-04/diagramas-uml.rst` con 75 líneas.
Para referencia, UC_SUP_01 completado tiene ~2,200 líneas en sus partes 1-12.

---

## 3. Inventario de conocimiento contextual (fuentes)

### 3.1 Arquitectura del sistema ETL

**Fuente:** `source/databases/modelo-dual.rst`, `source/databases/etl-pipeline.rst`

**Modelo de datos dual (CNST-006, CNST-007):**
- **BD MySQL IVR** — propiedad del cliente, acceso SOLO LECTURA para IACT.
  Enforcement en 3 niveles: GRANT SELECT, Django `managed=False`, IVRRouter.
  Contenido: llamadas, agentes, colas, eventos IVR.
- **BD PostgreSQL Analytics** — propiedad IACT, read/write.
  Contenido: tablas analíticas derivadas del ETL + operacionales IACT
  (usuarios, sesiones, RBAC, alertas, audit log).

**Flujo ETL completo:**
```
BD MySQL IVR (cliente)
    │  EXTRACT (SELECT only)
    ▼
etl/extractors/        ← lee datos crudos de IVR
    │  TRANSFORM
    ▼
etl/transformers/      ← calcula métricas derivadas:
                          TMO, tasa abandono, throughput, etc.
    │  LOAD
    ▼
BD PostgreSQL Analytics ← INSERT / UPSERT
    │  TRACK
    ▼
ETLRun / ETLExecution  ← registra: inicio, fin, registros,
                          estado, errores, date_range
```

**Restricciones de frecuencia (CNST-008):**
- Ventana: 6 a 12 horas. NO menor a 6h, NO mayor a 12h.
- Ventana preferente: 02:00–04:00 hora local.
- Mecanismo: `django-crontab` / Celery Beat (BR-002: trigger a medianoche 00:00).
- Prohibido: Debezium, CDC, WebSockets, polling agresivo, triggers cross-DB.

### 3.2 Modelos de datos del ETL (fuente: etl-monitoring/componentes.rst)

**ETLExecution** (también referenciado como ETLRun en algunos docs — inconsistencia a resolver):
```python
class ETLExecution(models.Model):
    job_id           = CharField(max_length=50, unique=True)
    started_at       = DateTimeField
    finished_at      = DateTimeField(null=True)
    status           = CharField(choices=['RUNNING', 'SUCCESS', 'FAILED'])
    records_extracted   = IntegerField(default=0)
    records_transformed = IntegerField(default=0)
    records_loaded      = IntegerField(default=0)
    error_message    = TextField(null=True)
    date_range_start = DateField
    date_range_end   = DateField
```

**DataAvailability:**
```python
class DataAvailability(models.Model):
    period_type  = CharField  # TRIMESTRE, MES, DIA
    period_value = CharField  # Q1-2024, 2024-01, 2024-01-15
    status       = CharField  # COMPLETO, PARCIAL, FALTANTE
    record_count = IntegerField
    last_updated = DateTimeField
```

### 3.3 APIs expuestas (fuente: etl-monitoring/componentes.rst)

| Método | Endpoint | Descripción |
|---|---|---|
| GET | `/api/v1/etl/executions` | Listar ejecuciones |
| GET | `/api/v1/etl/executions/{id}` | Detalle de ejecución |
| GET | `/api/v1/etl/availability` | Disponibilidad por periodo |
| GET | `/api/v1/etl/quality-issues` | Incidencias de calidad |
| POST | `/api/v1/etl/retry/{id}` | Reintentar procesamiento |

### 3.4 Funciones RBAC canónicas

Del catálogo v5.5.0 (`modelo-rbac-iact/catalogo-funciones.rst`,
`grupos-funciones.rst` — AGR-009 `pipeline_admin_group`):

| ID | Nombre canónico | UC que lo requiere |
|---|---|---|
| PIP-001 | `view_pipeline_status` | UC_PIP_01 |
| PIP-002 | `view_pipeline_errors` | UC_PIP_02 |
| PIP-003 | `view_data_availability` | UC_PIP_03 |
| PIP-004 | `request_pipeline_retry` | UC_PIP_04 |

**⚠ INCONSISTENCIA DETECTADA:** Los stubs actuales de los UCs usan
nombres de función distintos a los canónicos:
- UC_PIP_01 stub: `view_etl_supervision` → debe ser `PIP-001 view_pipeline_status`
- UC_PIP_02 stub: `view_etl_errors` → debe ser `PIP-002 view_pipeline_errors`
- UC_PIP_03 stub: `view_data_availability` → ya correcto ✓ (PIP-003)
- UC_PIP_04 stub: `request_pipeline_retry` → ya correcto ✓ (PIP-004)

### 3.5 Restricciones aplicables

| CNST | Título | Impacto en pipeline |
|---|---|---|
| CNST-006 | BD dual | ETL es el único mecanismo de sincronización |
| CNST-007 | BD IVR solo lectura | Extract: solo SELECT sobre MySQL IVR |
| CNST-008 | ETL en ventana 6-12h | Frecuencia máxima y mínima del scheduler |
| CNST-009 | JWT obligatorio | Todos los endpoints de pipeline requieren auth |
| CNST-013 | Manejo de errores | UC_PIP_02: stack traces sanitizados |
| CNST-025 | Auditoría inmutable | UC_PIP_04: retry queda en AuditEvent |
| CNST-026 | Sin PII innecesaria | UC_PIP_02: stack traces pueden tener PII — sanitizar |

### 3.6 Reglas de negocio aplicables

| BR | Título | Impacto |
|---|---|---|
| BR-001 | Fuente Operacional Inmutable | IVR es read-only absoluto |
| BR-002 | ETL Batch Nocturno | Trigger programado a 00:00 diariamente |
| BR-009 | Bajas lógicas | En reproceso: marcar INACTIVE, no DELETE |

### 3.7 Dependencias del módulo (etl-monitoring/dependencias.rst)

**Depende de:**
- `arq-mod-001` (Auth) — requiere sesión autenticada
- `arq-mod-003` (RBAC) — verifica PIP-001..004

**Es requerido por:**
- `arq-mod-005` (Reportes/vis-reports) — consulta disponibilidad antes de mostrar datos
- `arq-mod-006` (Alertas) — genera alertas por fallos ETL

### 3.8 Runbook operacional (fuente: devops/runbooks/runbook-reprocesar-etl-fallido.rst)

El runbook de reproceso ETL documenta el flujo operacional completo de UC_PIP_04:
- Verificar estado actual (`/internal/etl/last-run`)
- Diagnosticar causa (logs JSON, systemd journal)
- Identificar rango a reprocesar
- Limpiar datos parciales con baja lógica (BR-009)
- Encolar reproceso vía API (`/internal/etl/reprocess`)
- Verificar post-reproceso (conteo filas, audit log)
- Escalación si falla 2 veces consecutivas

Esto es material directo para UC_PIP_04 partes 4-11.

### 3.9 Responsabilidades del módulo (etl-monitoring/responsabilidades.rst)

**PUEDE:**
- Listar ejecuciones ETL históricas
- Ver detalle (errores, métricas) — CNST-004 (datos sensibles)
- Consultar fechas/trimestres disponibles
- Listar incidencias de calidad de datos
- Reintentar transformación sobre datos ya extraídos

**NO PUEDE (violaciones de SoD):**
- Generar tablas/gráficos para usuario final → responsabilidad de MOD_Reports
- Exponer logs técnicos crudos → MOD_Logs
- Consultar BD IVR directamente (solo via ETL metadata)
- Definir reglas de seguridad → MOD_RBAC

### 3.10 Actor especial: Scheduler (UML-06 Actor Tiempo)

UC_PIP_01, UC_PIP_02, UC_PIP_03 tienen un actor implícito: el
**Scheduler** (Celery Beat / django-crontab) que dispara el ETL.
Según UML-06, esto es un **Actor Tiempo** — debe modelarse con el
estereotipo `<<actor>>` o con notación de reloj en el diagrama UC.
UC_PIP_04 tiene el Scheduler como actor secundario (el retry es
manual pero también puede ser programático post-fallo).

---

## 4. Inconsistencias identificadas (a resolver en este WP)

| # | Inconsistencia | Ubicación | Acción |
|---|---|---|---|
| I-01 | `ETLRun` vs `ETLExecution` — dos nombres para el mismo modelo | `etl-pipeline.rst`, `componentes.rst`, `cnst-008.rst` | Unificar en `ETLExecution` (más descriptivo) en los UCs |
| I-02 | UC_PIP_01 usa `view_etl_supervision` — no existe en RBAC | `uc-pip-01/informacion-general.rst` | Corregir a `PIP-001 view_pipeline_status` |
| I-03 | UC_PIP_02 usa `view_etl_errors` — no existe en RBAC | `uc-pip-02/informacion-general.rst` | Corregir a `PIP-002 view_pipeline_errors` |
| I-04 | `arq-mod-004/responsabilidades.rst` usa UC_051..055 (IDs legacy) | `etl-monitoring/responsabilidades.rst` | Actualizar a UC_PIP_01..04 |
| I-05 | `cnst-008.rst` referencia UC_025, UC_017 (IDs legacy) | `cnst-008.rst` sección 3.2 | Actualizar a UC_PIP_01..04, UC_RPT_* |
| I-06 | `br-002.rst` referencia AGR-009 y AGR-010 como "operador_etl" — no existe AGR-010 con ese nombre | `br-002.rst` sección 4.2 | AGR-009 = pipeline_admin_group (correcto), AGR-010 = system_admin_group |

---

## 5. Flujo del ETL y su relación con cada UC

```
[BR-002: 00:00 diario]
        │
        ▼
[Scheduler: Celery Beat]──────────────────────────────────────────────┐
        │                                                              │
        ▼                                                              │
[ETL Job START]   ← registra ETLExecution(status=RUNNING)             │
        │                                                              │
        ▼                                                              │
[EXTRACT: MySQL IVR]  ← CNST-007 solo lectura                         │
        │  falla?──────────────────────────────────────────────────────┤
        ▼                                                              │
[TRANSFORM: calcular métricas]                                        │
        │  falla?──────────────────────────────────────────────────────┤
        ▼                                                              │
[LOAD: PostgreSQL Analytics]  ← INSERT/UPSERT                        │
        │  falla?──────────────────────────────────────────────────────┤
        ▼                                                              │
[ETL Job END]   ← registra ETLExecution(status=SUCCESS/FAILED)        │
        │                                                              │
        ▼                                                         ▼   │
[DataAvailability.update()]  ← UC_PIP_03 lee esto    [ETLExecution.status=FAILED]
                                                              │
                                                              ▼
                                                     [UC_PIP_02: diagnóstico]
                                                              │
                                                              ▼
                                                     [UC_PIP_04: retry manual]
                                                        (PIP-004 RBAC)

[UC_PIP_01: dashboard salud]  ← lee ETLExecution en tiempo real
                                  (jobs running/completed/failed,
                                   lag, throughput)
```

**UC_PIP_01** — Dashboard de salud: vista de todas las ejecuciones, lag por source,
throughput, bytes procesados. Actor principal con PIP-001.

**UC_PIP_02** — Diagnóstico de errores: filtra ETLExecution con status=FAILED,
muestra stack traces sanitizados (CNST-013 + CNST-026), correlation IDs.
Actor principal con PIP-002.

**UC_PIP_03** — Disponibilidad por dataset: lee DataAvailability por período.
Responde la pregunta del usuario de reportes: "¿están listos los datos del Q1?"
Actor principal con PIP-003. **Actor secundario implícito: Scheduler** (dispara
actualización de DataAvailability).

**UC_PIP_04** — Retry manual: POST `/api/v1/etl/retry/{id}`. Operación sensitiva
con reason obligatoria, AuditEvent(ETL_RETRY_REQUESTED). Solo durante ventana
CNST-008 o por excepción aprobada. Actor principal con PIP-004.

---

## 6. Material por UC disponible para deepening

### UC_PIP_01 — Ver Estado Pipeline
- Flujo: GET con auth → PIP-001 → listar ETLExecution → métricas agregadas
- Datos: ETLExecution (todos los campos), métricas: lag = NOW()-last_success.finished_at
- Patrones: read-only query, paginación, filtros por status/date_range
- RNF: response ≤ 1s, datos frescos cada refresh, indicador "último ETL hace X horas"
- El runbook no cubre este UC directamente

### UC_PIP_02 — Ver Errores ETL
- Flujo: GET con auth → PIP-002 → ETLExecution(status=FAILED) → detalle + sanitización
- Datos: error_message, stack_trace (sanitizado), correlation_id, payload_muestra
- Restricción crítica: stack traces pueden contener PII — CNST-026 requiere sanitizar
- Patrones: data masking, structured error reporting

### UC_PIP_03 — Disponibilidad de Datos
- Flujo: GET con auth → PIP-003 → DataAvailability por dataset/período
- Datasets conocidos: CallSummary, AgentDailyStat, QueueDailyStat (y más)
- Datos: period_type (TRIMESTRE/MES/DIA), period_value, status (COMPLETO/PARCIAL/FALTANTE)
- **Dependencia crítica con MOD_Reports**: UC_PIP_03 es prereq de todos los reportes
  — el usuario de reportes consulta primero si los datos del período están disponibles
- UI obligatoria: mostrar timestamp de última actualización (CNST-008 §UI)

### UC_PIP_04 — Solicitar Reintento
- Flujo: POST con auth → PIP-004 → validar reason → ETLExecution(status=FAILED) →
  encolar retry → AuditEvent(ETL_RETRY_REQUESTED) → 202 Accepted
- Operación asíncrona: el retry NO es síncrono, retorna job_id para tracking
- Restricciones: solo sobre ETLExecution.status=FAILED, reason ≥ 20 chars,
  no puede iniciar si otro ETL está RUNNING sobre el mismo date_range
- Runbook: material detallado disponible para partes 4-11

---

## 7. Gap analysis (lo que falta construir)

Cada UC tiene 13 archivos (12 partes + index). Estado actual:

| Parte | UC_PIP_01 | UC_PIP_02 | UC_PIP_03 | UC_PIP_04 |
|---|---|---|---|---|
| 1 informacion-general | Stub (44L) | Stub (33L) | Stub (34L) | Stub (36L) |
| 2 actores-precondiciones | Stub (32L) | Stub (14L) | Stub (26L) | Stub (21L) |
| 3 flujo-principal | Stub (18L) | Stub (13L) | Stub (15L) | Stub (53L) |
| 4 flujos-alternos | Stub (36L) | Stub (35L) | Stub (30L) | Stub (40L) |
| 5 excepciones | Stub (22L) | Stub (23L) | Stub (22L) | Stub (28L) |
| 6 RNF | Stub (12L) | Stub (11L) | Stub (10L) | Stub (11L) |
| 7 datos-involucrados | Stub (30L) | Stub (29L) | Stub (22L) | Stub (17L) |
| 8 diagramas-uml | Stub (63L) | Stub (68L) | Stub (62L) | Stub (75L) |
| 9 criterios-aceptacion | Stub (28L) | Stub (26L) | Stub (29L) | Stub (33L) |
| 10 patrones-diseno | Stub (8L) | Stub (8L) | Stub (9L) | Stub (8L) |
| 11 implementacion-tecnica | Stub (21L) | Stub (18L) | Stub (19L) | Stub (51L) |
| 12 testing | Stub (37L) | Stub (33L) | Stub (36L) | Stub (50L) |

**Todas las 48 partes de los 4 UCs requieren expansión completa.**

---

## 8. Orden de trabajo recomendado

El orden refleja dependencias lógicas:

1. **UC_PIP_03** primero — es el UC más simple (solo lectura de disponibilidad)
   y es prerequisito de MOD_Reports. Establecer el patrón base.

2. **UC_PIP_01** segundo — dashboard de salud, lectura de ETLExecution.
   Construye sobre los modelos entendidos en UC_PIP_03.

3. **UC_PIP_02** tercero — diagnóstico de errores. Requiere comprender
   ETLExecution (de UC_PIP_01) + sanitización de PII.

4. **UC_PIP_04** último — retry operacional. El más complejo (async, audit,
   restricciones de ventana CNST-008, compensación). El runbook provee
   material detallado para las partes 4-11.

**Primero:** corregir inconsistencias I-01..I-06 antes de comenzar los UCs.

---

## 9. BReqs relacionados

| BReq | Título | Relación |
|---|---|---|
| BReq-005 | Integridad y Trazabilidad de Datos | UC_PIP_01..04 satisfacen observabilidad del ETL |
| BReq-006 | Operación Continua SLA | UC_PIP_01 muestra lag; UC_PIP_04 permite recovery |
| BReq-007 | Integración IVR Operacional | El ETL es el mecanismo de integración IVR→Analytics |

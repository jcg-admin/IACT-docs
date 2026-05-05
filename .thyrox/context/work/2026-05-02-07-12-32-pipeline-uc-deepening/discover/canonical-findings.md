```yml
created_at: 2026-05-02 07:25:31
project: IACT-docs
work_package: 2026-05-02-07-12-32-pipeline-uc-deepening
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Borrador
```

# Hallazgos Canónicos — PARTE_0, PARTE_6 y TPL files

Análisis exhaustivo de los archivos canónicos en `temp-holding/`.
Todos los hallazgos son **PROVEN** — extraídos verbatim de los documentos fuente.

## Fuentes analizadas

| Archivo | Líneas | Relevancia |
|---|---|---|
| `PARTE_0_Contexto_Fundamentos_IACT_1_0_0.md` | 2780 | Alta — arquitectura del sistema, módulos, CNST, actores, UC/FR/BR principales |
| `PARTE_6_Casos_Practicos_Completos_IACT_1_0_0.md` | 1307 | Alta — implementación Python, queries SQL, código de referencia |
| `TPL_UC_Construccion_7_Pasos_1_3_0.rst` | — | Alta — query principal ETL con `quarter`+`year` |
| `TPL_BR_Decision_Tipo_1_3_0.rst` | — | Alta — validaciones y queries de BR |

---

## 1. Módulos del sistema — catálogo completo (PROVEN)

De PARTE_0 sección 4.2:

| Módulo | Nombre | Descripción |
|---|---|---|
| `MOD_Auth` | Autenticación | Login/logout, sesiones, expiración, reset passwords |
| `MOD_Users` | Gestión de Usuarios | CRUD usuarios, perfiles, preferencias, estados |
| `MOD_Access` | Control de Acceso RBAC | Funciones atómicas, SoD, permisos temporales |
| `MOD_Pipeline` | ETL y Procesamiento | Extracción IVR → Transformación → Carga Analytics, 6-12h |
| `MOD_Reports` | Reportes y Analytics | Consultas consolidadas, exportación, aprobación grandes |
| `MOD_Alerts` | Alertas y Notificaciones | Umbrales dinámicos, notificaciones internas, logs alertas |
| `MOD_Audit` | Auditoría | Registro acciones, búsqueda, retención 7 años |
| `MOD_Logs` | Logs Técnicos | Logs aplicación, monitoreo errores, dashboards técnicos |

**Nota importante:** En PARTE_0 el módulo `MOD_Pipeline` ejecuta **cada 6-12 horas**
(consistente con CNST-003 y CNST-004).

---

## 2. Restricciones del sistema — lista completa (PROVEN)

De PARTE_0 sección 4.2:

| ID | Enunciado |
|---|---|
| `CNST-001` | NO envío de emails externos — solo notificaciones en buzón interno |
| `CNST-002` | Sesión única por usuario — cierre automático de sesión anterior |
| `CNST-003` | BD IVR solo lectura — datos con desfase 6-12h según ETL |
| `CNST-004` | ETL cada 6-12 horas — datos NO en tiempo real |
| `CNST-005` | Flat RBAC + SoD — 44 funciones atómicas, sin jerarquía; permisos temporales con justificación |
| `CNST-006` | Rango máximo 2 años — reportes limitados a 730 días |
| `CNST-007` | Límites de exportación — CSV:100K registros, Excel:50K, PDF:10K |
| `CNST-008` | Sesión expira 15 minutos — inactividad = logout automático |
| `CNST-009` | Auditoría obligatoria — todas las acciones se registran |
| `CNST-010` | Retención logs 7 años — cumplimiento normativo |

**⚠ Gap identificado (G-07):** En la documentación actual del proyecto, CNST-008 está
documentado como la restricción de ventana 6-12h del ETL. En PARTE_0, CNST-008 se
refiere a la expiración de sesión de 15 minutos. Hay una colisión de numeración que
debe resolverse.

---

## 3. Actores y Agrupadores RBAC (PROVEN)

De PARTE_0 sección 4.3:

| Agrupador | Nombre | Funciones típicas | Rol |
|---|---|---|---|
| `AGR-001` | `agr_operador` | 5-10 básicas | Consulta datos de su segmento, sin administración |
| `AGR-002` | `agr_analista` | 15-20 | Reportes avanzados, exportación de datos |
| `AGR-003` | `agr_supervisor` | 25-30 | Aprobación consultas grandes, gestión de equipo |
| `AGR-004` | `agr_admin_sistema` | 35-40 | Gestión usuarios, asignación funciones, configuración |
| `AGR-005` | `agr_auditor` | 5-8 específicas | Solo lectura de logs, sin modificación |

**Segmentos de datos confirmados:**

| Código | Nombre | Descripción |
|---|---|---|
| `OP` | Operativo | Centros de contacto operativos, métricas llamadas, clientes activos |
| `FI` | Financiero | Centros financieros, transacciones telefónicas, datos sensibles |
| `VT` | Ventas | Centros de ventas, métricas de conversión, campañas |
| `SP` | Soporte | Soporte técnico, tiempos de resolución, satisfacción |

**Nota:** En queries del ETL se usan solo `'OP'` y `'MG'` como `allowed_segments`.
`MG` no está documentado en esta taxonomía — posible gap G-08.

---

## 4. Business Rules principales (PROVEN)

De PARTE_0 secciones 2-4 y PARTE_6:

| ID | Tipo | Enunciado | Genera |
|---|---|---|---|
| `BR-IACT-001` | Definición | "Cliente activo" = llamada en últimos 30 días | Glosario |
| `BR-IACT-015` | Definición | "Función crítica" = `es_critica=TRUE` | Glosario |
| `BR-IACT-028` | Restricción | Consultas >10K registros requieren aprobación supervisor | UC-RPT-01 FA-1, UC-RPT-09 |
| `BR-IACT-031` | Desencadenador | Notificar usuario cuando sesión lleva 12 min inactiva | UC-AUTH-07 completo |
| `BR-IACT-046` | Inferencia | Marcar sesión EXPIRED si >15 min inactividad | FR-AUTH-08-02 directamente |
| `BR-IACT-053` | Cálculo | `promedio_duracion = SUM(duration>0) / COUNT(duration>0)` | FR-RPT-02-08, integrado en UC-RPT-01 |
| `BR-IACT-087` | Restricción | Usuario requiere `nivel_seguridad ≥ 3` para asignar funciones críticas | UC-ACC-01 precondición + FA-3 |
| `BR-IACT-091` | Inferencia | Clasificar horario como PEAK/OFF-PEAK | FR directo |
| `BR-IACT-104` | Desencadenador | Alerta cuando llamadas abandonadas >20% en última hora | UC-DASH-05 completo |
| `BR-IACT-105` | Cálculo | `tasa_abandono = (abandonadas / total) * 100` | FR-DASH-05-02, integrado en UC-DASH-05 |
| `BR-IACT-112` | Cálculo | Timeout 60 segundos para consultas de reportes | FR-RPT-01-06 |

**Business Requirements (BReq):**

| ID | Nombre | BRs que lo implementan |
|---|---|---|
| `BRQ-RPT-001` | Prevenir Sobrecarga Servidor Analytics | BR-028, BR-053, BR-112 |
| `BRQ-SEC-005` | Gestión seguridad sesiones | BR-031, BR-046 |
| `BRQ-SEC-008` | Nivel seguridad funciones críticas | BR-087 |

---

## 5. Módulo de Reportes — especificación completa (PROVEN)

### 5.1 UC-IACT-RPT-01: Consultar Reporte Trimestral

Actor principal: Analista de Negocio (AGR-003: `agr_supervisor`)
Actor secundario: Supervisor de Área (AGR-003)
Función RBAC: `RPT-001` (`ve_reportes`)
Prioridad: ALTA

**Restricciones aplicables:**
- CNST-003: Datos provienen de BD Analytics (desfase 6-12h según ETL)
- CNST-006: Rango máximo 2 años
- CNST-007: CSV:100K, Excel:50K, PDF:10K
- BR-IACT-028: Aprobación si >10,000 registros

**Precondiciones:**
1. Usuario autenticado
2. Función `RPT-001` (`ve_reportes`) asignada
3. Usuario pertenece a un segmento de datos válido
4. ETL ha ejecutado al menos una vez

**Flujo normal (12 pasos):**
1. Usuario selecciona "Reportes > Trimestral Consolidado"
2. Sistema valida función RPT-001
3. Sistema muestra formulario con filtros
4. Usuario selecciona trimestre, centro, métrica
5. Usuario hace click "Generar Reporte"
6. Sistema valida rango fecha ≤ 2 años (CNST-006)
7. Sistema ejecuta COUNT(*) en query (FR-RPT-01-07)
8. Sistema valida count ≤ 10,000 (BR-IACT-028)
9. Sistema aplica filtro segmento del usuario
10. Sistema ejecuta query en BD Analytics (timeout 60s)
11. Sistema renderiza tabla con resultados
12. Sistema audita acción (CNST-009)

**Flujos alternos:**
- FA-1: count > 10,000 → modal confirmación → crear request PENDIENTE_APROBACION → notificar supervisor → fin UC (continúa en UC-RPT-09)
- FA-2: sin RPT-001 → error → audita intento denegado
- FA-3: rango > 2 años → error campos en rojo
- FA-4: query retorna 0 registros → "No hay datos"

**Excepciones:**
- EX-1: timeout >60s → cancelar → nivel WARNING
- EX-2: error BD → log completo → nivel ERROR

**FR derivados (10):**
- `FR-RPT-01-01`: Validar función RBAC RPT-001
- `FR-RPT-01-02`: Renderizar formulario con filtros
- `FR-RPT-01-03`: Validar rango fecha ≤ 2 años
- `FR-RPT-01-04`: Ejecutar COUNT(*) antes de query principal
- `FR-RPT-01-05`: Aplicar filtro segmento automático
- `FR-RPT-01-06`: Ejecutar query con timeout 60s
- `FR-RPT-01-07`: Renderizar tabla paginada (50 filas/página)
- `FR-RPT-01-08`: Auditar evento en tabla auditoria
- `FR-RPT-01-09`: Crear request si count >10K
- `FR-RPT-01-10`: Notificar supervisor vía InternalMessage

### 5.2 UC-IACT-RPT-09: Aprobar/Rechazar Consulta Grande

Actor: Supervisor (AGR-003)
Precondición: Request en estado PENDIENTE_APROBACION
Paso 3: Supervisor aprueba/rechaza
Paso 5: Notifica analista

FR derivado:
- `FR-RPT-09-03`: Actualizar estado del request

### 5.3 FR-RPT-01-07: Calcular COUNT(*) — query completa (PROVEN)

```sql
SELECT COUNT(*) as total_records
FROM analytics_calls ac
INNER JOIN analytics_centers ctr ON ac.center_id = ctr.center_id
WHERE ac.call_date BETWEEN :start_date AND :end_date
  AND ac.metric_type = :metric_type
  AND ctr.segment_id = :user_segment_id
  [AND ac.center_id = :center_id]  -- Si filtro centro activo
```

**Performance:**
- Timeout: 5 segundos máximo
- Index requerido: `(call_date, center_id, metric_type)` en `analytics_calls`
- Caching: NO (datos cambian con cada ETL)

**Implementación Python confirmada:**
```python
# File: apps/reports/services.py
def calculate_query_count(filters: ReportFilters, user: User) -> int:
    """
    Implements: FR-RPT-01-07
    References: BR-IACT-028, BR-IACT-053
    """
    query = """
        SELECT COUNT(*) as total_records
        FROM analytics_calls ac
        INNER JOIN analytics_centers ctr 
          ON ac.center_id = ctr.center_id
        WHERE ac.call_date BETWEEN %s AND %s
          AND ac.metric_type = %s
          AND ctr.segment_id = %s
    """
    # SET statement_timeout = 5000 (5 seg)
```

### 5.4 FR-RPT-02-08: Calcular promedio duración — query (PROVEN)

```sql
SELECT 
    AVG(call_duration) as avg_duration
FROM analytics_calls
WHERE call_date BETWEEN :start AND :end
  AND call_duration > 0  -- Excluir abandonadas sin conexión
  AND segment_id = :user_segment
```

Validación:
- `avg_duration >= 0`
- `avg_duration <= 7200` (2 horas máximo físico)
- Redondeo: 2 decimales
- Unidad: segundos
- Si COUNT(duration>0) = 0: retornar NULL (no 0)

---

## 6. Módulo de Alertas — especificación (PROVEN)

### 6.1 UC-IACT-DASH-05: Alertar Llamadas Abandonadas Altas

Actor: Sistema (Scheduler)
Trigger: Cron job cada 5 minutos
BR-IACT-104: alerta si tasa abandono >20% en última hora

Flujo normal:
1. Sistema consulta llamadas última hora
2. Sistema calcula tasa abandono (BR-IACT-105)
3. Sistema valida si tasa > 20% (BR-IACT-104)
4. Sistema crea alerta con prioridad HIGH
5. Sistema actualiza dashboard (widget parpadea rojo)
6. Usuario ve alerta en tiempo real

### 6.2 FR-DASH-05-02: Calcular Tasa de Abandono — query (PROVEN)

```sql
SELECT 
    COUNT(CASE WHEN status='ABANDONED' THEN 1 END) as abandoned,
    COUNT(*) as total,
    (COUNT(CASE WHEN status='ABANDONED' THEN 1 END)::float / 
     NULLIF(COUNT(*), 0)) * 100 as rate
FROM ivr_calls
WHERE call_timestamp >= NOW() - INTERVAL '1 hour'
```

**Punto crítico:** Esta query corre sobre `ivr_calls` (MySQL IVR) directamente,
NO sobre `analytics_calls`. Confirma que las alertas son near-real-time desde
la fuente, mientras que los reportes usan el Analytics DB.

Timeout: 3 segundos
Logs: INFO con `rate` calculada
Tests: 0%, 15%, 25%

---

## 7. Schema de analytics_calls y analytics_centers (PROVEN)

Confirmado de FR-RPT-01-07 y FR-RPT-02-08:

### analytics_calls

| Columna | Tipo | Descripción | Fuente |
|---|---|---|---|
| `call_date` | DATE | Fecha de la llamada (para filtros de reporte) | FR-RPT-01-07 query |
| `center_id` | FK → analytics_centers | Centro de contacto | FR-RPT-01-07 JOIN |
| `metric_type` | VARCHAR | Tipo de métrica ('TOTAL_CALLS', etc.) | FR-RPT-01-07 WHERE |
| `call_duration` | INT/NUMERIC | Duración de llamada en segundos | FR-RPT-02-08 WHERE + AVG |

**Index requerido:** `(call_date, center_id, metric_type)`

### analytics_centers

| Columna | Tipo | Descripción | Fuente |
|---|---|---|---|
| `center_id` | PK | Identificador del centro | FR-RPT-01-07 JOIN ON |
| `segment_id` | VARCHAR | Segmento ('OP', 'FI', 'VT', 'SP') | FR-RPT-01-07 WHERE |

---

## 8. Módulo de Autenticación — especificación (PROVEN)

### UC-IACT-AUTH-07: Notificar Sesión por Expirar

Tipo: Desencadenador (BR-IACT-031)
Actor: Sistema (Scheduler/Background Job) + Usuario receptor
Trigger: Cron job cada 1 minuto
Timing: T+12min de inactividad → notificación

Paso 2 query (sesiones a notificar):
```sql
-- sessions con estado = 'ACTIVA' 
-- Y last_activity BETWEEN (NOW() - 13 min) AND (NOW() - 12 min)
```

Acción: Crea InternalMessage (CNST-001: NO email)
Notificación: "Su sesión expirará en 3 minutos por inactividad"

### UC-IACT-AUTH-08: Marcar Sesiones Expiradas

Tipo: Inferencia (BR-IACT-046)
Actor: Sistema únicamente
Query (FR-AUTH-08-02):
```sql
UPDATE user_sessions
SET estado = 'EXPIRED',
    expired_at = CURRENT_TIMESTAMP
WHERE estado = 'ACTIVA'
  AND last_activity < (CURRENT_TIMESTAMP - INTERVAL '15 minutes')
RETURNING session_id;
```

---

## 9. Módulo de Control de Acceso — especificación (PROVEN)

### UC-IACT-ACC-01: Asignar Funciones a Usuario

Precondición (BR-IACT-087):
- Si funciones a asignar incluyen críticas: usuario admin requiere `nivel_seguridad ≥ 3`

Paso 4: Sistema verifica cuáles funciones tienen `es_critica = TRUE`

FA-3: Si hay funciones críticas Y `nivel_admin < 3`:
```
4a. Error: "Nivel de seguridad insuficiente para asignar funciones críticas.
     Nivel requerido: 3. Nivel actual: X."
4b. Sistema lista funciones denegadas
4c. Regresa a selección de funciones
```

FR-ACC-01-04: `validate_security_level(user, functions) -> bool`

---

## 10. Trazabilidad bidireccional — matriz RTM (PROVEN)

De PARTE_0 sección 3.4:

| BR | BReq | UC | FR | Código | Test |
|---|---|---|---|---|---|
| BR-IACT-028 | BRQ-RPT-001 | UC-IACT-RPT-01 | FR-RPT-01-07 | `calculate_query_count()` | `test_count_over_10k()` |
| BR-IACT-028 | BRQ-RPT-001 | UC-IACT-RPT-01 | FR-RPT-01-09 | `create_approval_request()` | `test_approval_created()` |
| BR-IACT-028 | BRQ-RPT-001 | UC-IACT-RPT-09 | FR-RPT-09-03 | `update_request_status()` | `test_supervisor_approves()` |
| BR-IACT-031 | BRQ-SEC-005 | UC-IACT-AUTH-07 | FR-AUTH-07-02 | `get_expiring_sessions()` | `test_notification_sent()` |
| BR-IACT-031 | BRQ-SEC-005 | UC-IACT-AUTH-07 | FR-AUTH-07-03 | `create_internal_message()` | `test_message_created()` |
| BR-IACT-046 | BRQ-SEC-005 | UC-IACT-AUTH-08 | FR-AUTH-08-02 | `mark_sessions_expired()` | `test_session_marked()` |
| BR-IACT-087 | BRQ-SEC-008 | UC-IACT-ACC-01 | FR-ACC-01-04 | `validate_security_level()` | `test_level_insufficient()` |

---

## 11. Patrón ETL — diferenciación de fuentes de datos (PROVEN)

Hallazgo clave que emerge de las queries:

| Operación | Fuente de datos | Justificación |
|---|---|---|
| **Reportes trimestrales** | `analytics_calls` (PostgreSQL Analytics) | Datos agregados, acceso controlado por `segment_id` |
| **Alertas en tiempo real** | `ivr_calls` (MySQL IVR) | Near-real-time, query directa `NOW() - INTERVAL '1 hour'` |
| **Count ETL (FR-RPT-01-07)** | `analytics_calls` (PostgreSQL Analytics) | El count pre-ejecución usa el mismo DB que el query principal |

Esto confirma el flujo: MySQL IVR (fuente) → ETL → PostgreSQL Analytics (destino para reportes).
Las alertas son la excepción que apunta al origen directamente.

---

## 12. Gaps documentales identificados en canonico (INFERRED)

Complementando los G-01..G-06 del `ivr-schema-analysis.md`:

| # | Gap | Impacto |
|---|---|---|
| G-07 | Colisión de numeración CNST-008: en proyecto actual = ventana ETL 6-12h; en PARTE_0 = sesión expira 15 min | Alto — dos definiciones contradictorias del mismo ID |
| G-08 | Segmento `MG` (¿Management?) no está en taxonomía de segmentos de PARTE_0 (OP/FI/VT/SP) | Medio — queries del ETL usan `['OP', 'MG']` como allowed_segments |
| G-09 | `UC-IACT-RPT-02` (Consultar Promedio de Duración) no existe en `source/requisitos/casos-uso/reports/` | Alto — UC referenciado en PARTE_0 y PARTE_6, no creado |
| G-10 | `UC-IACT-RPT-09` (Aprobar/Rechazar Consulta Grande) no existe en source/ | Alto — complemento necesario de UC_RPT_01 |
| G-11 | `UC-IACT-DASH-05` (Alertar Llamadas Abandonadas) referenciado pero sin directorio `dashboard/` | Medio — ¿es MOD_Alerts o MOD_Dashboard? |
| G-12 | `analytics_calls.call_duration` columna — no documentada en schema de Analytics | Medio — usada en FR-RPT-02-08 |
| G-13 | `analytics_calls.metric_type` posibles valores no documentados (solo 'TOTAL_CALLS' visto) | Alto — afecta validación de formulario de reportes |
| G-14 | `UC-IACT-AUTH-07` y `UC-IACT-AUTH-08` existen en PARTE_0 pero no en source/requisitos/casos-uso/auth/ | Bajo (Scope 1) |
| G-15 | Función RBAC `RPT-001` (`ve_reportes`) y agrupador `AGR-003` (`agr_supervisor`) no aparecen en source/requisitos/rbac/ | Alto — son el actor principal de reports |

---

## 13. UCs canónicos que deben existir en source/ (INFERRED)

Los siguientes UCs están referenciados en PARTE_0/PARTE_6 y corresponden a módulos Scope 1:

### MOD_Reports (máxima prioridad)
- `UC-IACT-RPT-01`: Consultar Reporte Trimestral Consolidado
- `UC-IACT-RPT-02`: Consultar Promedio de Duración
- `UC-IACT-RPT-09`: Aprobar/Rechazar Consulta Grande (complemento de RPT-01)

### MOD_Alerts
- `UC-IACT-DASH-05`: Alertar Llamadas Abandonadas Altas (o equivalente en alerts/)

### MOD_Pipeline (directamente relevante para este WP)
- `UC_PIP_01..04`: Ya existen como stubs — deepening pendiente

### MOD_Auth
- `UC-IACT-AUTH-07`: Notificar Sesión por Expirar
- `UC-IACT-AUTH-08`: Marcar Sesiones Expiradas

---

## 14. Implicación para UC_RPT_01 (deepening futuro)

Cuando se profundice `UC_RPT_01` en source/, debe incorporar:

1. **FR-RPT-01-01 a FR-RPT-01-10** — los 10 FRs del canon
2. **CNST-006** explícito: validar rango ≤ 2 años (730 días)
3. **CNST-007** explícito: límites de exportación por formato
4. **CNST-003** explícito: nota de desfase 6-12h en precondiciones
5. **BR-IACT-028** en paso 8 (no solo mencionada)
6. **AGR-003** + **RPT-001** como función RBAC
7. **analytics_calls** como tabla de destino de reportes (no `ivr_calls`)
8. Query COUNT con `metric_type` y `segment_id` (no solo `quarter`/`year`)
9. Tabla de aprobaciones `requests` con estado `PENDIENTE_APROBACION`
10. Paginación de resultados: 50 filas/página

---

## 15. Código Python canónico de referencia

### calculate_query_count (PROVEN — PARTE_6 líneas 595-663)

```python
from django.db import connection
from django.utils import timezone
import logging

logger = logging.getLogger(__name__)

def calculate_query_count(query_params):
    """
    Implements: FR-RPT-01-07
    Derived from: UC-IACT-RPT-01 paso 5, BR-IACT-028
    """
    start_time = timezone.now()
    
    query = """
        SELECT COUNT(*) as record_count
        FROM ivr_calls c
        INNER JOIN ivr_sessions s ON c.session_id = s.session_id
        WHERE c.call_date >= %s
          AND c.call_date < %s
          AND s.user_segment IN %s
    """
    # ... timeout + logging + retorno
```

**Nota:** En PARTE_6 el count usa `ivr_calls + ivr_sessions` (fuente MySQL).
En PARTE_0/FR-RPT-01-07 el count usa `analytics_calls + analytics_centers` (Analytics DB).
Hay **inconsistencia entre PARTE_6 y PARTE_0** sobre qué BD usa el count.
Hipótesis INFERRED: PARTE_6 ilustra el patrón general; PARTE_0 muestra la implementación
real en el sistema (Analytics DB). El count debe correr sobre Analytics para ser consistente
con el query principal de reportes.

### calculate_abandon_rate (PROVEN — PARTE_6 líneas 956-967)

```python
# Query sobre ivr_calls (MySQL IVR) — para alertas en tiempo real
SELECT 
  COUNT(CASE WHEN status='ABANDONED' THEN 1 END) as abandoned,
  COUNT(*) as total,
  (COUNT(CASE WHEN status='ABANDONED' THEN 1 END)::float / 
   NULLIF(COUNT(*), 0)) * 100 as rate
FROM ivr_calls
WHERE call_timestamp >= NOW() - INTERVAL '1 hour'
```

---

## Resumen de hallazgos prioritarios para UC deepening

| Prioridad | Hallazgo | Acción |
|---|---|---|
| 1 | FR-RPT-01-01..10 son el canon de reports | Usar como base para source/requisitos/casos-uso/reports/ |
| 2 | `analytics_calls` usa `metric_type` como campo de filtro | Documentar en schema analytics |
| 3 | Count pre-ejecución timeout: 5s; query principal timeout: 60s | Especificar en UC_RPT_01 |
| 4 | Tasa abandono corre sobre `ivr_calls` directo (alertas ≠ reportes) | Distinguir claramente en UC_ALT/UC_PIP |
| 5 | CNST-007 define límites de exportación — no aparece en UC_RPT actual | Añadir al deepening |
| 6 | AGR-003 (`agr_supervisor`) es el actor principal de reports | Verificar en rbac/agrupadores.rst |
| 7 | `MG` segmento no documentado en taxonomía oficial | Resolver G-08 antes de deepening reports |
| 8 | G-07 colisión CNST-008 | Resolver ambigüedad de numeración |

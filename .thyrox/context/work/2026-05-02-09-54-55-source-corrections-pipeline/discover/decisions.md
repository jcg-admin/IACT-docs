```yml
created_at: 2026-05-02 10:30:00
project: IACT-docs
work_package: 2026-05-02-09-54-55-source-corrections-pipeline
phase: Phase 1 — DISCOVER
author: NestorMonroy
status: Aprobado
```

# Decisiones autónomas — source-corrections-pipeline

Decisiones tomadas durante la corrección de `source/` para reflejar
la arquitectura real del sistema IACT IVR pipeline.

---

## D-ETL-001 — Rol dual de MariaDB 10.1.48

**Decisión:** MariaDB 10.1.48 tiene DOS roles distintos en la arquitectura:

1. **IVR Fuente (read-only):** `tbl_historico_tN_YYYY` — propiedad del
   cliente, IACT solo tiene GRANT SELECT (CNST_007).
2. **IVR Analítica (read-write ETL):** `base_ivr_detalle`, `base_ivr_clientes`,
   `etl_runs` — propiedad de IACT dentro del mismo servidor MariaDB.
   El ETL escribe aquí vía SPs propios.

PostgreSQL existe exclusivamente para tablas operacionales de Django
(usuarios, sesiones, RBAC, alertas, audit log, configuraciones).

**Impacto:** `databases/modelo-dual.rst` se corrige para describir
TRES bases de datos lógicas en DOS servidores:
- MariaDB: fuente IVR (cliente) + analítica IVR (IACT)
- PostgreSQL: operacional IACT

---

## D-ETL-002 — Tabla etl_runs para tracking de ejecuciones

**Decisión:** Se agrega tabla `etl_runs` en MariaDB (propiedad IACT)
para registrar cada ejecución del ETL y habilitar UC_PIP_01/02/03.

**Esquema:**
```sql
CREATE TABLE etl_runs (
    id              INT AUTO_INCREMENT PRIMARY KEY,
    tabla_origen    VARCHAR(100) NOT NULL,
    trimestre       VARCHAR(20)  NOT NULL,   -- formato: Q3_25, Q1_25
    iniciado_en     DATETIME     NOT NULL,
    finalizado_en   DATETIME,
    estado          ENUM('en_ejecucion','exitoso','fallido')
                    DEFAULT 'en_ejecucion',
    registros_base  INT     DEFAULT 0,      -- filas en base_ivr_detalle post-ETL
    mensaje_error   TEXT,
    ejecutado_por   VARCHAR(100) DEFAULT 'scheduler',
    INDEX idx_estado_inicio (estado, iniciado_en DESC),
    INDEX idx_trimestre     (trimestre)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```

**Justificación:** Sin esta tabla, UC_PIP_01 (supervisar ETL) y
UC_PIP_02 (errores ETL) no tienen fuente de datos concreta. La tabla
vive en MariaDB (no en PostgreSQL) porque el ETL es todo-MariaDB y
es el proceso que la escribe.

---

## D-ETL-003 — Django trigger ETL via management command

**Decisión:** Django no ejecuta el ETL directamente. El ETL ocurre
así:
1. Cron/APScheduler llama `python manage.py run_etl` en la ventana
   02:00–04:00 (CNST_008).
2. El management command `run_etl` inserta en `etl_runs` (estado
   `en_ejecucion`), llama `CALL sp_etl_maestro(p_fecha)` en MariaDB,
   luego actualiza `etl_runs` con resultado.
3. Para reintentos manuales (UC_PIP_04): el AdminPipeline dispara
   `python manage.py run_etl --quarter Q3_25 --force` desde la
   interfaz de administración de IACT.
4. Para backfill histórico: `CALL sp_etl_historico(year, quarter_num)`.

**Consecuencia:** No hay `ETLRun` como modelo Django ORM. La fuente
de verdad de runs es `etl_runs` en MariaDB.

---

## D-ETL-004 — Django lee reportes via cursor.callproc()

**Decisión:** Las vistas Django de reportes IVR NO usan modelos ORM.
Usan `cursor.callproc()` sobre la conexión MariaDB:

```python
from django.db import connections

def get_centros_transferencia(quarter_name):
    with connections['ivr'].cursor() as cursor:
        cursor.callproc('sp_rpt_centros_transferencia', [quarter_name])
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]
```

**Consecuencia:** No existe `DailyMetrics` ni ningún modelo ORM para
datos IVR analíticos. El módulo `vis-reports` es una capa de
presentación sobre SPs de MariaDB.

---

## D-ETL-005 — Vocabulario de abstracción en UCs (soda machine)

**Decisión:** Los UCs (en `source/requisitos/`) usan terminología
abstracta que no expone la tecnología de implementación:

| Término en UC | Implementación real |
|---|---|
| Repositorio IVR | `tbl_historico_tN_YYYY` en MariaDB |
| Base Analítica IVR | `base_ivr_detalle` + `base_ivr_clientes` en MariaDB |
| Servicio ETL | `sp_etl_maestro` + SP auxiliares en MariaDB |
| Registro de Ejecuciones | Tabla `etl_runs` en MariaDB |
| Servicio de Reportes | Los 7 `sp_rpt_*` en MariaDB |
| Disparador ETL | Management command Django + APScheduler/cron |
| ETLEjecucion | Registro individual en `etl_runs` |
| EjecucionHistorica | `CALL sp_etl_historico(year, quarter)` |

En `source/arquitectura-tecnica/` SÍ se puede mencionar tecnología
concreta (MariaDB, stored procedures, cursor.callproc, etc.).

---

## D-ETL-006 — Implementación concreta de BR-016 (tasa de abandono)

**Decisión:** La implementación concreta de `llamadas_abandonadas`
en el sistema IACT IVR es:

```sql
WHERE menu IN ('VACIO', 'cliente_colgo', 'SinOpcion_Cabecera')
```

Tres tipos de abandono:
- `VACIO`: nunca llegó a un menú (cMenu vacío/NULL)
- `cliente_colgo`: llegó al menú y colgó explícitamente
- `SinOpcion_Cabecera`: llegó al menú pero no eligió opción

**El SP actual `sp_rpt_llamadas_abandonadas` solo cuenta `VACIO`**
(~8-9% del total). La implementación correcta con los tres tipos
da ~27-28% del total. El SP requiere corrección.

---

## D-ETL-007 — Recalibración de umbrales BR-016

**Decisión:** Los umbrales operativos de BR-016 (`< 5%` óptimo,
`5-10%` aceptable, `> 10%` crítico) son INCORRECTOS para el
sistema IVR IACT con la definición completa de abandono.

**Observación real Q3 2025:**
- Nacional A: ~27-28% de abandono (con definición completa)
- Puebla: ~27-30% de abandono

**Umbrales recalibrados:**
- `< 20%`: Óptimo — performance dentro de SLA
- `20-30%`: Aceptable — monitoreo recomendado
- `> 30%`: Crítico — requiere intervención inmediata

**Justificación:** Los umbrales 5%/10% corresponden a un call center
con alta tasa de resolución en menú IVR self-service. El IVR de
IACT tiene un perfil distinto con ~70-80% de llamadas que navegan
exitosamente y ~20-30% de abandono estructural.

---

## D-ETL-008 — UC_PIP_04 retry = sp_etl_historico

**Decisión:** El reintento de ETL (UC_PIP_04) usa
`sp_etl_historico(year, quarter_num)` para reprocesar un trimestre
completo. No hay retry granular a nivel de tabla fuente individual.

**Razonamiento:** El patrón TRUNCATE + INSERT hace idempotente el
reintento. Reprocesar el trimestre completo desde `tbl_historico_*`
garantiza consistencia de `base_ivr_detalle`.

---

## D-ETL-009 — Único trimestre disponible actualmente

**Decisión:** Solo existe `tbl_historico_t3_2025` como tabla fuente.
Toda la documentación que mencione "múltiples trimestres" o "Q1,
Q2, Q3" debe aclararse como el diseño para el estado final del
sistema. El estado actual tiene solo Q3 2025.

**Impacto en documentación:** Los UCs y la arquitectura técnica
describen el sistema completo (multi-quarter). El estado "solo Q3"
es un estado transitorio de arranque, no el diseño objetivo.

---

## D-ETL-010 — UC_INC_RPT_01: Resolver Segmento como <<include>> formal

**Decisión:** "Resolver Segmento del Usuario" es un comportamiento
compartido por TODOS los UCs de reportes (rpt-01..rpt-17). Se extrae
como UC formal `UC_INC_RPT_01` con relación `<<include>>` desde cada
UC de reporte.

**Pasos del UC:**
1. Leer los DIDs configurados para el usuario en RBAC.
2. Mapear cada DID a su segmento (`nacional_A`, `nacional_B`, `Puebla`).
3. Retornar la lista de segmentos accesibles (puede ser uno o todos).

**En ausencia de configuración de segmento:** el usuario ve todos
los segmentos (administrador / vista global).

**Justificación:** El principio soda machine (UML_06) establece
que los pasos comunes a múltiples UCs se extraen como UCs
independientes con `<<include>>`. Este comportamiento aparece
literalmente en todos los flujos de reporte como PASO 4.

---

---

## D-UML-001 — Actores en diagramas UML usan nombres de grupos RBAC (inglés)

**Decisión:** Los diagramas UML del sistema (diagramas-uml-sistema.rst,
arquitectura-sistema.rst) nombran los actores con los nombres de los
grupos RBAC en inglés (`report_viewer_group`, `quality_supervisor_group`,
`pipeline_admin_group`, `user_admin_group`, `auditor_group`), no con
títulos institucionales ("Administrador", "Analista de Datos",
"Supervisor de Operaciones").

**Justificación:** El RBAC del sistema es función-based (no role-based con
títulos). Los grupos RBAC son el identificador canónico del actor en el
sistema. Usar títulos institucionales desvincula los diagramas del modelo
de permisos real y crea ambigüedad.

**Impacto:** `arquitectura-sistema.rst` y `diagramas-uml-sistema.rst`
actualizados con grupos RBAC como actores.

---

## D-MENU-001 — Sistema de menú controlado por funciones RBAC

**Decisión:** Los ítems de menú visibles al usuario se determinan
exclusivamente por las funciones RBAC activas en el JWT del usuario.
Si el usuario no tiene la función requerida por un ítem de menú, ese
ítem NO se renderiza en el frontend (hide, not disable).

**Consecuencia:** No existe lógica de menú hardcodeada en el frontend.
El frontend recibe la lista de menú desde el backend en la respuesta de
autenticación.

---

## D-MENU-002 — Menú almacenado en tabla `iact_menu` (PostgreSQL)

**Decisión:** Los ítems de menú se almaceran en la tabla `iact_menu`
de PostgreSQL (base de datos operacional Django). Cada ítem referencia
una función RBAC (`required_function`) del catálogo `AccessFunction`.

**Esquema:**
```sql
CREATE TABLE iact_menu (
    id                SERIAL PRIMARY KEY,
    nombre            VARCHAR(100) NOT NULL UNIQUE,
    url               VARCHAR(200) NOT NULL,
    icono             VARCHAR(50),
    orden             INT DEFAULT 0,
    required_function VARCHAR(100) NOT NULL,
    modulo            VARCHAR(50) NOT NULL,
    activo            BOOLEAN DEFAULT TRUE
);
```

**Justificación:** PostgreSQL es la base de datos operacional de Django.
Los menús son configuración operacional que cambia con RBAC — pertenecen
al mismo espacio que `AccessGroup` y `AccessFunction`.

---

## D-MENU-003 — UC_MENU_01 incluido por UC_AUTH_01 post-JWT

**Decisión:** `UC_MENU_01` (Cargar Menu IACT) es un UC `<<include>>`
ejecutado automáticamente al final de `UC_AUTH_01` (Autenticar JWT),
después de generar el JWT con payload RBAC.

**Flujo:**
1. UC_AUTH_01 genera JWT con funciones RBAC.
2. UC_MENU_01 consulta `iact_menu WHERE required_function IN (funciones_usuario)`.
3. La lista de ítems de menú se incluye en la respuesta de autenticación.
4. El frontend almacena y renderiza solo los ítems recibidos.

**Justificación:** Centralizar la carga del menú en el momento de auth
elimina round-trips adicionales y garantiza consistencia entre funciones
RBAC y menú visible en toda la sesión.

---

## D-MENU-004 — Nueva función RBAC MGT-001: manage_menus

**Decisión:** Se crea la función RBAC `manage_menus` (ID: MGT-001) para
controlar el acceso a `UC_MENU_02` (Gestionar Menu IACT — CRUD sobre
`iact_menu`).

**Función:**
- **ID:** MGT-001
- **Nombre:** `manage_menus`
- **Descripción:** Crear, editar, desactivar y reordenar ítems de menú
  en la tabla `iact_menu`.
- **Asignada a:** `user_admin_group` (AGR-006)
- **SoD:** No hay restricción SoD para esta función.

**Justificación:** Los administradores de usuarios (AGR-006) son los
responsables naturales de la configuración de menús, ya que la
configuración de menú extiende la gestión de RBAC.

---

## D-MENU-005 — Módulo UC menus/ creado en casos-uso/

**Decisión:** Se crea el módulo `source/requisitos/casos-uso/menus/`
con dos UCs:

- `UC_MENU_01`: Cargar Menu IACT (<<include>> desde UC_AUTH_01)
- `UC_MENU_02`: Gestionar Menu IACT (actor: user_admin_group con manage_menus)

**Justificación:** El sistema de menú es un comportamiento funcional
relevante para la trazabilidad de RBAC y la experiencia de usuario. No
existía documentación de este comportamiento en `source/`. La omisión
dejaba un gap entre la arquitectura técnica (RBAC function-based) y los
requisitos documentados.

---

---

## D-FUNC-001 — Renombrar funciones RBAC del Pipeline ETL a inglés

**Decisión:** Las funciones RBAC del módulo Pipeline (PIP-*) estaban en
español. Se renombran a inglés para mantener consistencia con el resto
del catálogo de funciones.

**Mapeo de renombrado:**

| Anterior (español) | Nuevo (inglés) |
|---|---|
| `ver_estado_etl` | `view_etl_status` |
| `ver_errores_etl` | `view_etl_errors` |
| `ver_disponibilidad_datos` | `view_data_availability` |
| `reintentar_etl` | `retry_etl` |

**Justificación:** La convención del proyecto es que las funciones RBAC,
clases y atributos son en inglés; los comentarios en español. Las funciones
PIP eran la única excepción inconsistente en el catálogo.

**Impacto:** `matriz-dependencias-uc-iact.rst`, `uc-pip-*/actores-precondiciones.rst`,
`diagramas-uml-sistema.rst`, `diagramas-uc-por-modulo.rst`,
`arquitectura-sistema.rst`.

---

## D-MENU-006 — UC_PERM_08 ya cubre "Generar Menu Dinamico" — sin UC duplicado

**Decisión:** La funcionalidad de menú dinámico ya está documentada en
`UC_PERM_08 — Generar Menu Dinamico` (módulo MOD_Permissions). No se
crean UCs adicionales en un módulo separado `menus/`.

**Arquitectura correcta del menú:**
- Los ítems de menú vienen del catálogo de funciones (`FunctionRegistry`)
- Cada función RBAC tiene metadata de menú: `domain`, `section`, `label_es`,
  `label_en`, `icon`, `order`
- El menú se construye en `GET /api/me/menu/` filtrado por `effective_set`
  del usuario (UC_PERM_08)
- La función implícita es `view_own_navigation`
- El menú oculta opciones; la seguridad real está en UC_PERM_07 (decorators)

**Consecuencia:** D-MENU-001 a D-MENU-005 son parcialmente corregidas
por esta decisión. No se crea `iact_menu` como tabla separada.

---

## D-ETL-011 — Entidades de reportes IVR mapean a Base Analítica IVR

**Decisión:** Los UCs de reporte IVR (rpt-13, rpt-15, rpt-16, rpt-17)
referencian entidades ficticias (`QueueDailyStat`, `TransferEvent`,
`IVRSessionEvent`, `CallSummary`). La fuente real es la Base Analítica
IVR consultada vía Servicio de Reportes.

**Mapeo correcto:**

| UC | Entidad ficticia | SP real | Datos reales |
|---|---|---|---|
| UC_RPT_13 | QueueDailyStat | sp_rpt_llamadas_abandonadas | abandono por segmento en base_ivr_detalle |
| UC_RPT_15 | TransferEvent | sp_rpt_centros_transferencia + sp_rpt_centros_xsegmento | transferencias por centro y segmento |
| UC_RPT_16 | IVRSessionEvent | sp_rpt_menu_redirigidos + sp_rpt_menu_centro + sp_rpt_cMENU_ERROR | navegación de menús IVR |
| UC_RPT_17 | CallSummary | sp_rpt_clientes | clientes únicos en base_ivr_clientes |
| UC_RPT_01 | CallEvent/CallSummary | sp_rpt_centros_xsegmento | KPIs de transferencia por segmento |
| UC_RPT_03 | CallSummary/SegmentDimension | sp_rpt_centros_transferencia | histórico por centro |

**Consecuencia:** Los datos-involucrados de estos UCs se corrigen
para usar terminología abstracta alineada con D-ETL-005:
"Base Analítica IVR" en lugar de nombres de entidades ficticias.

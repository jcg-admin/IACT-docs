.. meta::
 :artefacto: AT_PIPELINE_ETL_IACT_INDEX
 :tipo: Indice — Pipeline ETL IVR Implementation Spec
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at-pipeline-etl-iact-index:

==================================================================
Pipeline ETL IVR — Especificacion de Implementacion (v2.1)
==================================================================

Especificacion **autoritativa** del pipeline ETL del sistema
IACT desde la fuente IVR del cliente (MariaDB) hasta los
endpoints Django REST Framework. Documenta los 6 niveles
arquitectonicos de la implementacion real con DDL, codigo
SQL, y codigo Python verificados.

.. note::

 **Reemplaza** dos documentos previos (informales,
 mantenidos como inputs de WP):

 - ``FLUJO-ETL-V2.md`` (arquitectura sin codigo)
 - ``FLUJO-ETL-COMPLETO.md`` (codigo v1 con nombres obsoletos)

 La v2.1 fusiona ambos con la implementacion actual.

Actores y scope funcional
==========================

El pipeline ETL es operado y supervisado por el rol
``PipelineAdmin`` (AGR-009 ``pipeline_admin_group``). Este
rol es distinto de otros dos roles que existen en el catalogo
RBAC del corpus pero estan **fuera de scope** del proyecto
IACT:

.. list-table::
 :widths: 24 32 24 20
 :header-rows: 1

 * - Rol
   - AGR / funciones
   - Dominio
   - Scope
 * - ``PipelineAdmin``
   - AGR-009 ``pipeline_admin_group`` —
     ``view_pipeline_status``, ``view_pipeline_errors``,
     ``request_pipeline_retry``
   - IT/ops — supervisa salud tecnica del ETL de datos IVR
   - **In scope** — UC_PIP_01..04
 * - ``Supervisor`` de agentes
   - AGR-003 ``quality_supervisor_group`` /
     AGR-012 ``call_center_supervisor_group`` —
     ``monitor_live_calls``, ``barge_in_calls``,
     ``broadcast_team_messages``
   - Call center — supervisa agentes en tiempo real
   - **Fuera de scope** (``MOD_Supervision``) —
     UC_SUP_01..03
 * - ``Operador`` / ``Agente``
   - ``MOD_Operator`` —
     ``manage_own_agent_state``, ``mailbox``, ...
   - Call center — operacion del agente telefonico
   - **Fuera de scope** (``MOD_Operator``) —
     UC_OPR_01..10

.. warning::

 La palabra ``Supervisor`` aparece en dos contextos
 incompatibles del corpus RBAC. **En este spec y en
 UC_PIP_01..04 todo "supervisor" se refiere a
 ``PipelineAdmin``** (IT/ops), nunca al ``Supervisor`` de
 call center (AGR-003 / AGR-012). El rename global del
 actor ``Supervisor`` a ``QualitySupervisor`` queda como
 WP futuro cuando se active ``MOD_Supervision``.

Cambios v1 → v2
================

.. list-table::
 :widths: 18 32 28 22
 :header-rows: 1

 * - Area
   - v1
   - v2
   - Por que
 * - G-29 (38.8% de registros con dHoraInicio > dHoraFin)
   - CASE inline en cada SP
   - ``fn_duracion_seg()``
   - Una sola version correcta
 * - NK90 / segmento / VACIO
   - CASE inline duplicado
   - ``fn_normalizar_centro()``,
     ``fn_did_segmento()``,
     ``fn_normalizar_menu()``
   - Cambio en un lugar afecta a todos
 * - Dias de semana
   - Pendiente del cliente
   - ``ivr_es_dia_semana()`` propias
   - Independencia del cliente — IVR opera 7 dias,
     criterio es lun-vie
 * - Procesamiento
   - DELETE+INSERT de todo el quarter
   - Por mes (chunks ~4M filas)
   - Undo log manejable en MariaDB 10.1
 * - Orquestacion
   - Un SP sin checkpoints
   - Pipeline con checkpoint por paso en
     ``job_execution_log``
   - Diagnostico preciso de fallos
 * - Crash MariaDB
   - ``etl_runs`` queda en ``en_ejecucion`` sin fin
   - Heartbeat Django + campo ``timeout_at``
   - Deteccion automatica de timeout en 30 min
 * - Dias de semana en reportes
   - Segundo scan a la fuente
   - Pre-computados en ETL (``llamadas_entre_semana``)
   - ``sp_rpt_centros_xsegmento`` sin scan adicional

Vista panoramica del pipeline
==============================

.. code-block:: text

   CLIENTE (solo lectura)          IACT — MariaDB mismo servidor
   ──────────────────────          ──────────────────────────────────────────────

   tbl_historico_t1_2025           DISPARO
   tbl_historico_t2_2025           evt_etl_diario (02:00 AM MySQL Event)
   tbl_historico_t3_2025           manage.py run_etl (APScheduler Django)
   tbl_historico_t4_2025               │
   tbl_historico_t1_2026               ▼
   tbl_historico_t2_2026           sp_etl_maestro()
            │                          │ checkpoint 'etl_base_detalle'
            └── scan mes a mes ──▶     ├── sp_etl_base_detalle() ──▶ base_ivr_detalle
            └── scan full quarter ──▶  ├── sp_etl_base_clientes() ──▶ base_ivr_clientes
                                       └── sp_etl_validar()
                                            │
                                       job_execution_log / etl_runs
                                            │
                                            ▼
                                     sp_rpt_centros_transferencia()
                                     sp_rpt_centros_xsegmento()
                                     sp_rpt_llamadas_abandonadas()  ◀── Django
                                     sp_rpt_menu_redirigidos()          cursor.callproc()
                                     sp_rpt_menu_centro()
                                     sp_rpt_cMENU_ERROR()
                                     sp_rpt_clientes()

Estructura de la spec
======================

La especificacion se organiza en 6 niveles arquitectonicos.
Cada archivo es independiente pero parte del flujo completo.

.. toctree::
 :maxdepth: 1
 :caption: Niveles del pipeline

 utility-functions
 triggers
 orchestration
 etl-procedures
 intermediate-tables
 report-procedures
 django-rest-integration
 legacy-comparison

Estado de los componentes
==========================

.. list-table::
 :widths: 12 32 30 26
 :header-rows: 1

 * - Capa
   - Componente
   - Tecnologia
   - Estado
 * - 0 Fuente
   - ``tbl_historico_tN_YYYY`` (6 tablas)
   - MariaDB cliente
   - Creadas + seed
 * - 0 Funciones
   - 7 funciones de utilidad
   - MariaDB FUNCTION
   - Desplegadas
 * - 1 Disparo
   - ``evt_etl_diario``
   - MySQL Event
   - Pendiente
 * - 1 Disparo
   - ``manage.py run_etl`` + heartbeat
   - Django
   - Pendiente
 * - 2 Orquestacion
   - ``sp_etl_maestro``
   - MariaDB SP
   - Desplegado
 * - 3 ETL
   - ``sp_etl_base_detalle``
   - MariaDB SP (PREPARE/EXECUTE)
   - Desplegado
 * - 3 ETL
   - ``sp_etl_base_clientes``
   - MariaDB SP (PREPARE/EXECUTE)
   - Desplegado
 * - 3 ETL
   - ``sp_etl_validar``
   - MariaDB SP
   - Desplegado
 * - 3 Backfill
   - ``sp_etl_historico``
   - MariaDB SP
   - Desplegado
 * - 4 Tablas
   - ``base_ivr_detalle``, ``base_ivr_clientes``
   - MariaDB IACT
   - Creadas
 * - 4 Control
   - ``job_execution_log``, ``etl_runs``,
     ``job_config``
   - MariaDB IACT
   - Creadas
 * - 5 Reportes
   - 7 SPs ``sp_rpt_*``
   - MariaDB SP
   - Desplegados
 * - 6 API
   - ``settings.py`` DATABASES dual
   - Django
   - Pendiente
 * - 6 API
   - ``services/ivr_reports.py``
   - Django
   - Pendiente
 * - 6 API
   - ``views/ivr_reports.py`` + ``urls.py``
   - Django REST
   - Pendiente
 * - 6 Scheduler
   - APScheduler + ``run_etl`` command
   - Django
   - Pendiente

Restricciones tecnicas que condicionan el diseño
==================================================

.. list-table::
 :widths: 18 50 32
 :header-rows: 1

 * - ID
   - Restriccion
   - Impacto
 * - CNST-ETL-001
   - Solo SELECT en ``tbl_historico_*``
   - No se crean indices en la fuente
 * - CNST-ETL-005
   - Sin indices en tablas fuente
   - Full scan obligatorio — chunks por mes para
     controlar undo log
 * - CNST-ETL-007
   - Produccion en MariaDB 10.1.48; sandbox en 10.11.14
   - Subconsultas correlacionadas en lugar de
     ``OVER(PARTITION BY)``; SPs sin window functions
 * - CNST-ETL-008
   - Nombre de tabla dinamico (``p_table``)
   - ``PREPARE/EXECUTE`` obligatorio en
     ``sp_etl_base_detalle`` y ``sp_etl_base_clientes``
 * - CNST-003
   - Intervalo minimo entre ejecuciones
   - ``job_config.min_intervalo_h = 6``
 * - ADR-BACK-012
   - Sin Redis/RabbitMQ
   - Heartbeat con ``threading.Thread`` en el
     management command
 * - IVR-7-dias
   - El IVR opera 7 dias / no aplica festivos
   - ``ivr_es_dia_semana`` = solo lun-vie, sin catalogo
     de festivos

Orden de implementacion
========================

.. code-block:: text

   PASO 1  funciones_utilidad.sql    — 7 funciones (Nivel 0)
   PASO 2  schema_base_ivr.sql       — 5 tablas (base_ivr_*, control)
   PASO 3  sp_etl_pipeline.sql       — 5 SPs ETL (Niveles 2 y 3)
   PASO 4  sp_rpt_reportes.sql       — 7 SPs reporte (Nivel 4)
   PASO 5  MySQL Event Scheduler     — evt_etl_diario (Nivel 1A)
   PASO 6  management command        — run_etl + heartbeat (Nivel 1B)
   PASO 7  sp_etl_historico          — carga de Q01_25..Q01_26
   PASO 8  Django REST               — settings + services + views + urls

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/index` —
   UCs del modulo pipeline (UC_PIP_01..04).
 - :doc:`/arquitectura-tecnica/design-view/pipeline/index` —
   estructura de diseño del modulo pipeline.
 - :doc:`/arquitectura-tecnica/implementation-view/pipeline/index` —
   capas API/service/repository/ORM del pipeline.
 - :doc:`/arquitectura-tecnica/modulos/etl-monitoring/index` —
   ARQ_MOD_004 perspectiva de monitoreo (no ejecucion).
 - :doc:`/arquitectura-tecnica/system-view/etl-execution-lifecycle` —
   FSM de ejecucion ETL.

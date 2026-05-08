.. meta::
 :artefacto: AT_PIPELINE_ETL_ORCHESTRATION
 :tipo: Especificacion de Implementacion — Nivel 2
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 2
 :estado: Aprobado
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_orchestration:

==============================================================
Nivel 2 — Orquestacion con checkpoints (sp_etl_maestro)
==============================================================

``sp_etl_maestro`` es el punto unico de entrada al pipeline ETL.
Coordina los SPs ETL (Nivel 3 — ver :doc:`etl-procedures`) con
checkpoints granulares en ``job_execution_log`` para diagnostico
preciso de fallos.

Cada paso del pipeline registra un checkpoint con su propio
``status``:

- ``RUNNING`` — paso en progreso.
- ``SUCCESS`` — paso completado correctamente.
- ``FAILED`` — paso fallo con error.
- ``PARTIAL`` — algunos sub-pasos OK, otros fallaron.
- ``SKIP`` — paso saltado por concurrencia previa.
- ``TIMEOUT`` — paso supero el tiempo limite.

----

DAG de niveles 0-5
===================

.. code-block:: text

   ┌─────────────────────────────────────────────────────────────────┐
   │  NIVEL 0 — Funciones de utilidad  (prerequisito de todo)        │
   │                                                                   │
   │  fn_did_segmento        fn_normalizar_menu    fn_duracion_seg    │
   │  fn_normalizar_centro   ivr_es_dia_semana     ivr_contar_dias_s  │
   │                         ivr_agregar_dias_s                       │
   └──────────────────────────────┬──────────────────────────────────┘
                                  │ usan
   ┌──────────────────────────────▼──────────────────────────────────┐
   │  NIVEL 1 — Disparo del ETL                                       │
   │  evt_etl_diario (MySQL Event 02:00 AM)                           │
   │  manage.py run_etl ──▶ INSERT etl_runs + heartbeat thread        │
   └──────────────────────────────┬──────────────────────────────────┘
                                  │
   ┌──────────────────────────────▼──────────────────────────────────┐
   │  NIVEL 2 — Orquestacion con checkpoints (sp_etl_maestro)        │
   │  checkpoint 'maestro'         → job_execution_log               │
   │  checkpoint 'etl_base_detalle'→ job_execution_log               │
   │  checkpoint 'etl_base_clientes'→ job_execution_log              │
   └───────────┬──────────────────────┬──────────────────────────────┘
               │                      │
   ┌───────────▼──────────┐ ┌─────────▼────────────┐
   │  NIVEL 3A            │ │  NIVEL 3B             │
   │  sp_etl_base_detalle │ │  sp_etl_base_clientes │
   │  Scan mes a mes      │ │  Scan full quarter    │
   │  GROUP BY grain      │ │  COUNT(DISTINCT)      │
   │  → base_ivr_detalle  │ │  → base_ivr_clientes  │
   └──────────────────────┘ └───────────────────────┘
               │                      │
   ┌───────────▼──────────────────────▼──────────────────────────────┐
   │  NIVEL 4 — SPs de reporte (read-only, milisegundos)              │
   │  7 SPs que leen base_ivr_detalle / base_ivr_clientes             │
   └──────────────────────────────┬──────────────────────────────────┘
                                  │ cursor.callproc()
   ┌──────────────────────────────▼──────────────────────────────────┐
   │  NIVEL 5 — Django REST Framework                                  │
   │  services/ivr_reports.py + views/ivr_reports.py + urls.py        │
   └─────────────────────────────────────────────────────────────────┘

----

Esqueleto de ``sp_etl_maestro``
=================================

.. code-block:: sql

   CREATE PROCEDURE sp_etl_maestro()
   maestro: BEGIN
       DECLARE v_quarter   VARCHAR(10);
       DECLARE v_table     VARCHAR(100);
       DECLARE v_inicio    DATE;
       DECLARE v_fin       DATE;
       DECLARE v_log_id    INT;
       DECLARE v_running   INT DEFAULT 0;

       -- 1. Detectar concurrencia (anti-overlap window 6h)
       SELECT COUNT(*) INTO v_running
       FROM job_execution_log
       WHERE job_name='etl_diario'
         AND status='RUNNING'
         AND start_time > DATE_SUB(NOW(), INTERVAL 6 HOUR);

       IF v_running > 0 THEN
           INSERT INTO job_execution_log
               (job_name, step_name, status, start_time, end_time, error_message)
           VALUES
               ('etl_diario', 'maestro', 'SKIP', NOW(), NOW(),
                'Anti-overlap: hay job RUNNING en las ultimas 6h');
           LEAVE maestro;
       END IF;

       -- 2. Calcular quarter actual y tabla fuente
       SET v_quarter = sp_quarter_actual();    -- helper que retorna 'Q02_26'
       SET v_table   = CONCAT('tbl_historico_t', SUBSTRING(v_quarter, 2, 2),
                              '_',  SUBSTRING(v_quarter, 5, 4));
       SET v_inicio  = sp_quarter_start(v_quarter);
       SET v_fin     = sp_quarter_end(v_quarter);

       -- 3. Insertar checkpoint MAESTRO
       INSERT INTO job_execution_log
           (job_name, quarter_name, step_name, tabla_origen,
            start_time, status)
       VALUES
           ('etl_diario', v_quarter, 'maestro', v_table, NOW(), 'RUNNING');
       SET v_log_id = LAST_INSERT_ID();

       -- 4. Llamar sp_etl_base_detalle con su propio checkpoint
       CALL sp_etl_base_detalle(v_quarter, v_inicio, v_fin, v_table,
                                _new_log_id_for_step('etl_base_detalle',
                                                     v_quarter, v_table));

       -- 5. Llamar sp_etl_base_clientes con su propio checkpoint
       CALL sp_etl_base_clientes(v_quarter, v_inicio, v_fin, v_table,
                                 _new_log_id_for_step('etl_base_clientes',
                                                      v_quarter, v_table));

       -- 6. Validacion
       CALL sp_etl_validar(v_quarter);

       -- 7. Cerrar checkpoint maestro como SUCCESS
       UPDATE job_execution_log
       SET status='SUCCESS', end_time=NOW()
       WHERE id = v_log_id;

   END maestro;

Notas:

- Si cualquiera de los SPs internos lanza una excepcion, el
  handler global del SP (no mostrado por brevedad) actualiza
  el checkpoint a ``FAILED`` con el mensaje de error.
- Los sub-pasos (``etl_base_detalle``, ``etl_base_clientes``)
  tienen sus propios ``log_id``; el SP maestro solo coordina
  el flujo y el checkpoint top-level.

----

Patron de checkpoints en ``job_execution_log``
================================================

Ejecucion exitosa
------------------

.. code-block:: text

   id  job_name    step_name           quarter  status   duracion_seg
   1   etl_diario  maestro             Q02_26   SUCCESS  318
   2   etl_diario  etl_base_detalle    Q02_26   SUCCESS  281
   3   etl_diario  etl_base_clientes   Q02_26   SUCCESS  34

Fallo en ``etl_base_detalle``
------------------------------

.. code-block:: text

   id  step_name           status   error_message
   1   maestro             FAILED   Fallo etl_base_detalle: Table doesn't exist
   2   etl_base_detalle    FAILED   Table 'tbl_historico_t2_2026' doesn't exist
   -- etl_base_clientes NO llega a correr
   -- se puede reintentar solo el paso fallido

PARTIAL — detalle OK, clientes falla
--------------------------------------

.. code-block:: text

   id  step_name           status   records_procesados
   1   maestro             PARTIAL  —
   2   etl_base_detalle    SUCCESS  12847
   3   etl_base_clientes   FAILED   0
   -- Solo 2 filas de 3 en base_ivr_clientes
   -- reintentar solo sp_etl_base_clientes

Esto permite:

- **Diagnostico preciso** sin grep en logs aplicativos.
- **Reintentar paso fallido** sin re-ejecutar el ETL completo.
- **Visualizacion en UI** (consume ``job_execution_log`` en
  endpoints de monitoring de ARQ_MOD_004).

----

Anti-overlap window
====================

``sp_etl_maestro`` consulta ``job_execution_log`` con
``status='RUNNING'`` en las ultimas 6 horas (configurable
via ``job_config.min_intervalo_h``). Si hay un job en
progreso, inserta una fila con ``status='SKIP'`` y retorna.

Esto previene:

- Ejecuciones concurrentes desde el Event Scheduler + el
  management command corriendo en simultaneo.
- Ejecuciones repetidas si el job nocturno se sobrelapa con
  un retry manual.

----

.. seealso::

 - :doc:`utility-functions` — funciones que usan los SPs ETL.
 - :doc:`triggers` — disparo del ETL (mecanismos A y B).
 - :doc:`etl-procedures` — SPs ETL invocados por el maestro.
 - :doc:`intermediate-tables` — DDL de ``job_execution_log``.
 - :doc:`/arquitectura-tecnica/design-view/pipeline/etl-execution-flow`
   — flujo ETL en la design view.
 - :doc:`/arquitectura-tecnica/design-view/pipeline/pipeline-execution-lifecycle`
   — FSM de PipelineExecution.

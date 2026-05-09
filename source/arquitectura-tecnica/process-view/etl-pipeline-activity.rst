.. meta::
 :artefacto: AT_PROC_ETL_PIPELINE_ACTIVITY
 :tipo: Diagrama Arquitectonico — Process View — Activity
 :dominio: arquitectura_tecnica
 :subdominio: ProcessView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_proc_etl_pipeline_activity:

============================================================
Process View — Pipeline ETL: flujo de actividades
============================================================

Diagrama de actividades del pipeline ETL — complementa
:doc:`etl-pipeline-concurrency` (vista de secuencia de
participantes) con la perspectiva del **flujo de control**:
decisiones de skip por intervalo minimo, fork de SPs ETL,
join, validacion y politica de retry.

.. uml::
 :caption: ProcessView ETL — flujo de actividades con decisiones, fork/join y retry.

 @startuml

 start

 :Disparo (MySQL Event 02:00 AM\nor manage.py run_etl);

 :Leer job_config.last_run_at;

 if (¿NOW() - last_run_at < 6h?\n(CNST-003)) then (si)
   :SKIP — registrar en
   job_execution_log
   (status=SKIP);
   stop
 else (no)
 endif

 :INSERT etl_runs
 (status='en_ejecucion',
 timeout_at=NOW()+30min);

 :Iniciar HeartbeatThread
 (60s tick → UPDATE
 etl_runs.heartbeat_at);

 partition "sp_etl_maestro (orquestador)" {
   :checkpoint
   etl_base_detalle
   (status=RUNNING);

   fork
     :CALL sp_etl_base_detalle
     (scan mes a mes);
   fork again
     :CALL sp_etl_base_clientes
     (scan full quarter);
   end fork

   :checkpoint base_*
   (status=SUCCESS);
 }

 :CALL sp_etl_validar;

 if (¿validaciones OK?) then (si)
   :UPDATE etl_runs
   (status='success',
   fin_at=NOW());
   :Detener heartbeat;
   stop
 else (no)
   :UPDATE etl_runs
   (status='failed',
   error_message);
   :checkpoint validar
   (status=FAILED);
   :Detener heartbeat;

   if (¿auto_retry habilitado\nAND retries < 3?) then (si)
     :Esperar backoff exponencial
     (5min, 15min, 45min);
     :Re-disparar pipeline;
     stop
   else (no)
     :Alerta operacional
     (audit_gap o pipeline_failed);
     stop
   endif
 endif

 @enduml

Decisiones modeladas
=====================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Decision
   - Detalle
 * - Skip por intervalo minimo
   - CNST-003: si hubo run hace menos de 6h, no se vuelve
     a disparar. Registra fila ``SKIP`` en
     ``job_execution_log`` para evidencia.
 * - Fork ETL
   - ``sp_etl_base_detalle`` y ``sp_etl_base_clientes``
     pueden ejecutarse en paralelo dentro del orquestador
     (no comparten tablas de output — uno escribe en
     ``base_ivr_detalle``, el otro en ``base_ivr_clientes``).
 * - Validacion gate
   - Si ``sp_etl_validar`` falla, el run se marca
     ``failed`` y NO se reintenta automaticamente — un
     fallo de validacion es de datos, no transitorio.
 * - Auto-retry
   - Solo aplica a fallos transitorios (timeouts,
     deadlock, conexion). Maximo 3 reintentos con backoff
     exponencial (5min, 15min, 45min).

----

.. seealso::

 - :doc:`etl-pipeline-concurrency` — secuencia de
   participantes (workers, queue, dispatcher).
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/orchestration` —
   ``sp_etl_maestro`` (implementacion).
 - :doc:`/arquitectura-tecnica/implementation-view/pipeline/etl-execution-binding` —
   binding del ejecutor (Django command + heartbeat).

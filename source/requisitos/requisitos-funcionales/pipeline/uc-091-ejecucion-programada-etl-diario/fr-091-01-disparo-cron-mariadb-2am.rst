.. meta::
 :artefacto: FR-091.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/pipeline
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-20
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-091-01:

==================================================================
FR-091.01: Disparo cron MariaDB del ETL nocturno (02:00 AM diario)
==================================================================

1. Identificacion
-----------------

* **ID:** FR-091.01
* **UC origen:** UC-091
* **Modulo:** MOD_Pipeline
* **Tipo:** Tarea programada (scheduled job)
* **Actor:** Sistema (MariaDB event_scheduler)

2. Especificacion
-----------------

**Declaracion:** el sistema DEBE ejecutar automaticamente el
pipeline ETL IVR cada dia a las 2:00 AM via ``evt_etl_diario``
EVENT de MariaDB, invocando ``sp_etl_maestro()``.

**Comportamiento implementado:**

* MariaDB EVENT ``evt_etl_diario`` con
  ``ON SCHEDULE EVERY 1 DAY STARTS '02:00:00'``.
* Cuerpo del event: ``DO CALL sp_etl_maestro();``.
* Requiere variable de sistema ``event_scheduler=ON``.
* Si ``job_config.is_enabled = FALSE`` para ``job_name =
  'etl_diario'``, ``sp_etl_maestro`` no procesa (control
  operacional FR-091.02).
* ``etl_runs`` registra cada corrida (status=en_ejecucion ->
  terminado/timeout/error).

3. Criterios de aceptacion
--------------------------

* CA-01: con ``event_scheduler=ON`` y ``job_config.is_enabled=
  TRUE``, a las 2:00 AM se crea row en ``etl_runs`` con
  ``trigger_source='mariadb_event'``.
* CA-02: con ``event_scheduler=OFF``, el EVENT no dispara
  (responsabilidad del operador del DB).
* CA-03: si una corrida supera ``job_config.timeout_seconds``,
  ``etl_runs.status`` transiciona a ``timeout`` (separado de
  esta FR; ver el pipeline timeout handler).
* CA-04: el EVENT es idempotente — no crea
  ejecuciones concurrentes si una previa esta ``en_ejecucion``
  (CTRL via ``min_intervalo_h`` en job_config).

4. Trazabilidad
---------------

* **Codigo DB:** ``provisioners/mariadb/objetos/jobs/evt_etl_diario.sql``
* **SP invocado:** ``provisioners/mariadb/objetos/sps/sp_etl_maestro.sql``
* **Origen historico:** T-081, HALLAZGOS-EVENT-SCHEDULER-2026-05-09.md
  H-081-04.
* **Tabla operacional:** ``etl_runs``, ``job_execution_log``.

5. Dependencias
---------------

* FR-091.02 (control operacional via job_config).
* UC_PIP_04 (reintentar pipeline manual — usa el mismo
  sp_etl_maestro).
* UC_PIP_01..03 (consumen ``etl_runs`` para mostrar estado).

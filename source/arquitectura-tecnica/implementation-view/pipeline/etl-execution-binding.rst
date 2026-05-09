.. meta::
 :artefacto: AT_IMPL_PATTERN_ETL_EXECUTION_BINDING
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_etl_execution_binding:

============================================================
Implementation View — ETL Execution Binding (Django + Cron)
============================================================

Patron de binding entre Django y el Servicio ETL (MariaDB
SPs). Documenta decisiones de implementacion no obvias —
``ADR-BACK-012`` (sin Redis/RabbitMQ/Celery) y CNST-003
(intervalo minimo entre ejecuciones).

Hay dos disparadores coexistentes:

1. **MySQL Event Scheduler** (``evt_etl_diario``) — primary,
   noche programada. NO requiere Django corriendo.
2. **Django mgmt command** (``manage.py run_etl``) — backup
   + control manual con observabilidad detallada (heartbeat).

Arquitectura del binding
=========================

.. uml::
 :caption: ETL execution binding — coexistencia MySQL Event + Django command.

 @startuml

 package "MariaDB" {
   component "evt_etl_diario\n(MySQL Event)" as MyEvt <<scheduler>>
   component "sp_etl_maestro" as SP <<sp>>
   component "etl_runs / job_execution_log" as Tables <<table>>
 }

 package "Django Host" {
   component "manage.py run_etl" as Cmd <<command>>
   component "APScheduler\n(BlockingScheduler)" as APS <<scheduler>>
   component "HeartbeatThread\n(threading.Thread)" as HB <<thread>>
   component "PipelineService" as Svc <<service>>
 }

 actor "cron de host" as Cron

 MyEvt --> SP : CALL sp_etl_maestro()\n(02:00 AM)
 SP --> Tables : INSERT/UPDATE
 SP --> Tables : checkpoint

 Cron --> Cmd : @daily o ad-hoc
 Cmd --> APS : start()
 APS --> Svc : trigger run
 Svc --> SP : cursor.callproc('sp_etl_maestro')
 Svc --> HB : start()
 HB --> Tables : UPDATE etl_runs.heartbeat_at\n(cada 60s)

 note right of HB
   ADR-BACK-012: sin Redis.
   Heartbeat con threading.Thread
   permite detectar timeout sin
   broker externo.
 end note

 note bottom of MyEvt
   CNST-003: si ya hay run en
   progreso (last_run_at < 6h),
   se hace SKIP (NO doble-trigger).
 end note

 @enduml

Mecanismo A — MySQL Event
==========================

.. code-block:: sql

   -- Definicion del Event
   CREATE EVENT IF NOT EXISTS evt_etl_diario
   ON SCHEDULE EVERY 1 DAY
   STARTS '2026-05-10 02:00:00'
   DO BEGIN
     IF (SELECT TIMESTAMPDIFF(HOUR, last_run_at, NOW())
         FROM job_config WHERE job_name = 'etl_diario') >= 6 THEN
       CALL sp_etl_maestro();
     END IF;
   END;

Pros: 0 dependencias Django runtime. Funciona aunque la app
caiga.

Cons: sin observabilidad granular — todo el log esta en
``job_execution_log`` (escrito por el SP).

Mecanismo B — Django mgmt command
==================================

.. code-block:: python

   # apps/pipeline/management/commands/run_etl.py
   class Command(BaseCommand):
       def handle(self, *args, **options):
           run_id = self._create_etl_run()

           # Heartbeat thread
           hb_stop = threading.Event()
           hb_thread = threading.Thread(
               target=self._heartbeat_loop,
               args=(run_id, hb_stop),
               daemon=True,
           )
           hb_thread.start()

           try:
               with connection.cursor() as cur:
                   cur.callproc('sp_etl_maestro')
               self._mark_success(run_id)
           except DatabaseError as e:
               self._mark_failed(run_id, str(e))
               raise
           finally:
               hb_stop.set()
               hb_thread.join(timeout=5)

       def _heartbeat_loop(self, run_id, stop_event):
           while not stop_event.wait(60):  # 60s tick
               ETLRunORM.objects.filter(id=run_id).update(
                   heartbeat_at=timezone.now()
               )

Pros: heartbeat -> deteccion automatica de timeout (housekeeping
detecta ``status=en_ejecucion AND heartbeat_at <
NOW() - 5min``).

Cons: requiere proceso Django activo durante todo el ETL.

Restricciones de implementacion
================================

- **R-ETL-EXEC-01:** los dos mecanismos NO deben dispararse
  simultaneamente. ``job_config.is_enabled`` per-job actua
  como flag de habilitacion. ``sp_etl_historico`` lo
  habilita/deshabilita en su ejecucion (ver
  :doc:`/arquitectura-tecnica/pipeline-etl-iact/etl-procedures`).
- **R-ETL-EXEC-02:** sin Celery/RabbitMQ (``ADR-BACK-012``).
  El heartbeat NO usa worker pool — es un thread directo del
  proceso del management command.
- **R-ETL-EXEC-03:** ``threading.Thread`` es daemon — si el
  proceso principal muere por OOM o SIGKILL, el heartbeat
  cesa, y el housekeeping detecta el timeout en <= 5 min.
- **R-ETL-EXEC-04:** ``cursor.callproc('sp_etl_maestro')`` es
  blocking — el management command no termina hasta que el
  SP retorna. Provisionar timeout adecuado en MariaDB para
  permitir el quarter completo (~30 min con cache lleno).

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Archivo
 * - run_etl command
   - ``apps/pipeline/management/commands/run_etl.py``
 * - APScheduler config
   - ``apps/pipeline/scheduler.py``
 * - HeartbeatThread
   - ``apps/pipeline/services/heartbeat.py``
 * - SP runner
   - ``apps/pipeline/services/sp_runner.py``
 * - MySQL Event DDL
   - ``apps/pipeline/sql/ddl/event_etl_diario.sql``

----

.. seealso::

 - :doc:`interaction-pattern` — flow de consulta del estado.
 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/triggers` —
   spec completa del binding (DDL del Event + management
   command).
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/orchestration` —
   ``sp_etl_maestro`` invocado por ambos mecanismos.

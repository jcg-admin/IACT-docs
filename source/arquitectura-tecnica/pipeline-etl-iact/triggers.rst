.. meta::
 :artefacto: AT_PIPELINE_ETL_TRIGGERS
 :tipo: Especificacion de Implementacion — Nivel 1
 :dominio: arquitectura_tecnica
 :subdominio: pipeline-etl-iact
 :nivel: 1
 :estado: pendiente-implementacion
 :version: 2.1.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_pipeline_etl_triggers:

==============================================================
Nivel 1 — Disparo del ETL
==============================================================

Dos mecanismos coexisten con roles distintos:

- **Mecanismo A:** ``evt_etl_diario`` (MySQL Event Scheduler) —
  produccion automatica nocturna sin intervencion humana.
- **Mecanismo B:** ``manage.py run_etl`` (Django management
  command) — control manual con observabilidad detallada en
  ``etl_runs`` + heartbeat de timeout.

Ambos mecanismos invocan ``sp_etl_maestro()`` (ver
:doc:`orchestration`). El SP maneja la concurrencia entre
ambos disparos via ``job_config.min_intervalo_h``.

.. note::

 **Estado:** ambos mecanismos son ``pendiente-implementacion``.
 El SP ``sp_etl_maestro`` y los SPs ETL si estan desplegados
 (ver :doc:`etl-procedures`); falta solo el disparo
 automatizado.

----

Mecanismo A — MySQL Event Scheduler
====================================

Programado a las 02:00 AM local. Corre sin intervencion
humana y NO registra en ``etl_runs`` — solo en
``job_execution_log`` (ver :doc:`intermediate-tables`).

.. code-block:: sql

   SET GLOBAL event_scheduler = ON;

   CREATE EVENT IF NOT EXISTS evt_etl_diario
   ON SCHEDULE EVERY 1 DAY
   STARTS CONCAT(CURDATE() + INTERVAL 1 DAY, ' 02:00:00')
   COMMENT 'ETL IVR nocturno — ejecuta sp_etl_maestro()'
   DO CALL sp_etl_maestro();

Caracteristicas:

- Sin retries automaticos; falla queda registrada en
  ``job_execution_log`` con ``status='FAILED'``.
- ``sp_etl_maestro`` maneja la concurrencia: si hay un job
  RUNNING en las ultimas 6 horas, inserta ``status='SKIP'``
  y sale.
- No requiere infraestructura externa (sin Redis, sin
  RabbitMQ — ADR-BACK-012).

----

Mecanismo B — Django management command
=========================================

Control manual con observabilidad. Inserta en ``etl_runs``
con ``timeout_at`` + ``estado='en_ejecucion'`` + thread de
heartbeat.

.. code-block:: python

   # management/commands/run_etl.py
   import threading
   from django.core.management.base import BaseCommand
   from django.db import connections


   class Command(BaseCommand):

       def add_arguments(self, parser):
           parser.add_argument('--quarter', type=str, default=None)
           parser.add_argument('--force',   action='store_true')

       def handle(self, *args, **options):
           quarter = options.get('quarter') or self._calcular_quarter_actual()

           # 1. Registrar inicio con timeout_at
           with connections['ivr'].cursor() as c:
               c.execute("""
                   INSERT INTO etl_runs
                       (trimestre, iniciado_en, timeout_at, estado, ejecutado_por)
                   VALUES (%s, NOW(), DATE_ADD(NOW(), INTERVAL 30 MINUTE),
                           'en_ejecucion', %s)
               """, [quarter, 'management_command'])
               run_id = c.lastrowid

           # 2. Heartbeat en thread paralelo (detecta timeout)
           stop_event = threading.Event()
           threading.Thread(
               target=self._heartbeat,
               args=(run_id, stop_event),
               daemon=True
           ).start()

           # 3. Ejecutar el ETL
           try:
               with connections['ivr'].cursor() as c:
                   c.callproc('sp_etl_maestro', [])
               self._update_run(run_id, 'exitoso')
           except Exception as e:
               self._update_run(run_id, 'fallido', str(e))
               raise
           finally:
               stop_event.set()

       def _heartbeat(self, run_id, stop_event):
           """Marca como timeout si el SP lleva mas de 30 min sin responder."""
           while not stop_event.wait(timeout=120):   # check cada 2 min
               try:
                   with connections['ivr'].cursor() as c:
                       c.execute("""
                           UPDATE etl_runs
                           SET estado='timeout',
                               finalizado_en=NOW(),
                               mensaje_error='Sin respuesta > 30 min'
                           WHERE id=%s
                             AND estado='en_ejecucion'
                             AND timeout_at < NOW()
                       """, [run_id])
               except Exception:
                   pass

       def _update_run(self, run_id, estado, error=None):
           with connections['ivr'].cursor() as c:
               c.execute("""
                   UPDATE etl_runs
                   SET estado=%s, finalizado_en=NOW(), mensaje_error=%s
                   WHERE id=%s
               """, [estado, error, run_id])

Caracteristicas:

- ``timeout_at`` permite deteccion automatica de jobs colgados.
- Heartbeat thread chequea cada 2 min; marca ``estado='timeout'``
  si el SP supera 30 min sin responder. Esto resuelve el
  problema de v1 donde un crash de MariaDB dejaba ``etl_runs``
  en ``en_ejecucion`` indefinidamente.
- Daemon thread (``daemon=True``) garantiza que termina cuando
  el comando termina.
- ``stop_event.set()`` en ``finally`` asegura cleanup explicito.

----

Coexistencia de ambos mecanismos
=================================

Los dos mecanismos pueden coexistir sin colisiones porque:

1. **``sp_etl_maestro``** verifica al inicio si hay otra
   ejecucion en progreso (consultando ``job_execution_log``
   con ``status='RUNNING'`` en las ultimas 6 horas — valor
   configurable en ``job_config.min_intervalo_h``).

2. Si la verificacion encuentra otra ejecucion activa, el
   SP inserta una fila con ``status='SKIP'`` en
   ``job_execution_log`` y retorna sin ejecutar el ETL.

3. Ambos mecanismos usan la misma deteccion → no hay duplicacion
   de cargas, no hay race conditions sobre las tablas
   ``base_ivr_*``.

Patron de uso esperado:

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Mecanismo
   - Cuando usar
 * - ``evt_etl_diario`` (Event)
   - Operacion normal — corre todas las noches a las 02:00
 * - ``manage.py run_etl``
   - Carga manual on-demand, backfill, debug, recuperacion
     post-falla

----

Carga historica inicial
========================

Para poblar quarters historicos se usa ``sp_etl_historico``
(ver :doc:`etl-procedures`) ejecutado manualmente uno a uno:

.. code-block:: sql

   -- Ejecutar una sola vez para poblar los quarters historicos.
   -- sp_etl_historico habilita temporalmente etl_historico en job_config,
   -- corre el ETL, y deshabilita el job al terminar.

   CALL sp_etl_historico(2025, 1);   -- Q01_25  ~11.6M filas reales  ~9 min
   CALL sp_etl_historico(2025, 2);   -- Q02_25  ~13.6M filas reales  ~10 min
   CALL sp_etl_historico(2025, 3);   -- Q03_25  ~11.5M filas reales  ~9 min
   CALL sp_etl_historico(2025, 4);   -- Q04_25  estimado             ~9 min
   CALL sp_etl_historico(2026, 1);   -- Q01_26  estimado             ~9 min
   -- Q02_26: evt_etl_diario lo maneja desde hoy
   -- Total backfill: ~47 min (5 quarters + pausas de 5s entre pasos)

----

.. seealso::

 - :doc:`utility-functions` — funciones SQL pre-requisito.
 - :doc:`orchestration` — ``sp_etl_maestro`` que recibe el
   disparo.
 - :doc:`intermediate-tables` — DDL de ``etl_runs``,
   ``job_execution_log``, ``job_config``.
 - :doc:`/arquitectura-tecnica/system-view/etl-execution-lifecycle`
   — FSM canonica de la ejecucion ETL.

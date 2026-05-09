.. meta::
 :artefacto: AT_IMPL_PATTERN_EVALUATOR_SCHEDULER
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_evaluator_scheduler:

============================================================
Implementation View — Evaluator Scheduler Binding
============================================================

Patron de scheduling del evaluator de alertas. Documenta la
decision de usar APScheduler in-process (``ADR-BACK-012``,
sin Celery) y restricciones operativas no obvias del tick
de 60 segundos.

Arquitectura
=============

.. uml::
 :caption: Evaluator scheduler — APScheduler in-process Django.

 @startuml

 component "Django app server\n(Gunicorn worker 1)" as App <<process>>
 component "EvaluatorScheduler\n(BackgroundScheduler)" as Sched <<scheduler>>
 component "EvaluatorJob" as Job <<job>>
 component "AlertService" as Svc <<service>>

 App --> Sched : on app ready()\nstart()
 Sched --> Job : trigger every 60s
 Job --> Svc : evaluate_all()

 note right of Sched
   ADR-BACK-012: sin Celery.
   APScheduler.BackgroundScheduler
   corre en el mismo proceso Python
   que el app server.
 end note

 note bottom of App
   IMPORTANTE: solo UN worker
   ejecuta el scheduler. Los demas
   workers solo sirven HTTP.
   Mecanismo: env var
   IACT_RUN_SCHEDULER=true en
   un solo Gunicorn worker.
 end note

 @enduml

Configuracion
==============

.. code-block:: python

   # apps/alerts/scheduler.py
   import os
   from apscheduler.schedulers.background import BackgroundScheduler
   from .jobs.evaluator import EvaluatorJob

   _scheduler: BackgroundScheduler | None = None

   def start_scheduler() -> None:
       global _scheduler
       if not os.getenv("IACT_RUN_SCHEDULER") == "true":
           return  # solo el worker designado lo arranca
       if _scheduler is not None:
           return  # idempotent

       _scheduler = BackgroundScheduler(daemon=True)
       _scheduler.add_job(
           EvaluatorJob().run,
           trigger="interval",
           seconds=60,
           id="alert_evaluator",
           max_instances=1,    # NO solapar evaluaciones
           coalesce=True,      # si pierde un tick, no acumula
       )
       _scheduler.start()

.. code-block:: python

   # apps/alerts/apps.py
   class AlertsConfig(AppConfig):
       def ready(self):
           from .scheduler import start_scheduler
           start_scheduler()

Restricciones de implementacion
================================

- **R-EVAL-01:** ``max_instances=1`` — si una evaluacion
  toma mas de 60s, el siguiente tick se descarta. NO se
  ejecutan evaluaciones en paralelo.
- **R-EVAL-02:** ``coalesce=True`` — si el scheduler estuvo
  pausado (e.g. restart del worker), al volver NO ejecuta
  todos los ticks acumulados; ejecuta solo uno.
- **R-EVAL-03:** ``IACT_RUN_SCHEDULER=true`` en EXACTAMENTE
  un Gunicorn worker. Asignar al worker 0 via
  ``--worker-tmp-dir`` + script de wrapper o via plugin
  Gunicorn que lee worker_id y settea el env.
- **R-EVAL-04:** sin Celery ni RabbitMQ
  (:doc:`/arquitectura-tecnica/deploy-view/standard-topology`).
  Si en el futuro se necesita scheduling distribuido (multi-host),
  este patron se reemplaza por un scheduler externo o por
  Celery beat — documentado como deuda en
  ``technical-debt.md``.
- **R-EVAL-05:** el evaluator job es **read-heavy**: lee de
  ``alert_rule`` (cache-able) y de la fuente de metrica
  (Prometheus o BD). Las inserciones a ``alert`` son
  esporadicas — el costo dominante es la lectura de
  metricas. Provisionar ``MetricSource`` con timeout
  agresivo (5s) para no bloquear el tick.

Manejo de fallos
=================

- Si el job falla con excepcion no atrapada, APScheduler
  emite un ``EVENT_JOB_ERROR``. Logger captura y registra.
  El siguiente tick (60s despues) intenta de nuevo.
- Si el proceso Django muere, APScheduler muere con el. Al
  reiniciar el worker designado, el scheduler arranca solo
  via ``ready()``.

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Archivo
 * - Scheduler bootstrap
   - ``apps/alerts/scheduler.py``
 * - EvaluatorJob
   - ``apps/alerts/jobs/evaluator.py``
 * - AlertService
   - ``apps/alerts/services/alert_service.py``
 * - Worker selection wrapper
   - ``ops/gunicorn/post_fork.py`` (settea
     IACT_RUN_SCHEDULER en worker 0)

----

.. seealso::

 - :doc:`interaction-pattern` — flow de evaluacion.
 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-evaluation-flow` —
   logica en DesignView.
 - :doc:`/arquitectura-tecnica/process-view/alert-evaluation-concurrency` —
   patron de concurrencia ProcessView.

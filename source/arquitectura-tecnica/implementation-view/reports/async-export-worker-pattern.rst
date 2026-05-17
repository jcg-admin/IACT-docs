.. meta::
 :artefacto: AT_IMPL_PATTERN_ASYNC_EXPORT_WORKER
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: reports
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_async_export_worker:

============================================================
Implementation View — Async Export Worker Pattern
============================================================

Patron de export asincrono para reportes grandes (CSV/XLSX
sobre quarters completos). Sin Celery (``ADR-BACK-012``),
con APScheduler in-process. Documenta restricciones no
obvias del worker que hacen viable el patron sin broker.

Por que async
==============

Los reportes con datos de un quarter (~hasta 13.6M filas
agregadas en ``base_ivr_detalle``) tardan minutos en
serializarse a XLSX. Hacer la generacion sincrona en el
request DRF dispara timeout SSE. Solucion: el endpoint crea
un ``ExportJob`` (con ``status=QUEUED``), un worker
in-process lo procesa en background, el cliente polling el
job para descargar.

Arquitectura
=============

.. uml::
 :caption: Async export — request -> ExportJob -> worker -> S3.

 @startuml

 actor User
 participant "ExportView\n(POST)" as View <<api>>
 participant "ExportService" as Svc <<service>>
 participant "ExportJobRepository" as Repo <<repository>>
 participant "ExportWorker\n(APScheduler tick 30s)" as Worker <<worker>>
 participant "SPRunner" as SP <<service>>
 participant "StorageGateway" as Storage <<gateway>>
 database PostgreSQL

 == 1) Request: encolar ==
 User -> View : POST /api/v1/reports/export/\n{report, quarter, format}
 View -> Svc : enqueue(...)
 Svc -> Repo : create(QUEUED)
 Repo -> PostgreSQL : INSERT INTO export_job
 Svc --> View : ExportJob{id, status=QUEUED}
 View --> User : HTTP 202 + {job_id}

 == 2) Worker tick ==
 Worker -> Repo : claim_oldest_queued(limit=1)
 note right
   atomic SELECT ... FOR UPDATE SKIP LOCKED
   + UPDATE status=PROCESSING
   evita doble-claim entre workers.
 end note
 Repo --> Worker : ExportJob | None

 alt job claimed
   Worker -> SP : callproc('sp_rpt_<X>', [quarter])
   SP --> Worker : rows
   Worker -> Worker : serialize(rows -> XLSX)
   Worker -> Storage : upload(blob, key=f"export/{job.id}.xlsx")
   Storage --> Worker : url + size
   Worker -> Repo : mark_done(job, url, size)
 end

 == 3) Polling ==
 User -> View : GET /api/v1/reports/export/{job_id}/
 View -> Repo : by_id(...)
 Repo --> View : ExportJob{status=DONE, url}
 View --> User : HTTP 200 + {status, download_url}

 @enduml

FSM del ExportJob
==================

.. uml::
 :caption: ExportJob FSM.

 @startuml
 [*] --> QUEUED : Service.enqueue()
 QUEUED --> PROCESSING : Worker.claim()
 PROCESSING --> DONE   : Worker.mark_done()
 PROCESSING --> FAILED : Worker.mark_failed()
 QUEUED --> CANCELLED  : User.cancel()
 DONE --> [*] : retencion 7d -> purga
 FAILED --> QUEUED : Worker.retry() (si attempts < 3)
 FAILED --> [*] : si attempts = 3
 CANCELLED --> [*]
 @enduml

Restricciones de implementacion
================================

- **R-EXP-01:** ``claim_oldest_queued`` usa ``SELECT ... FOR
  UPDATE SKIP LOCKED`` para soportar potencialmente multiples
  workers en el mismo host. **En produccion actual hay solo
  uno** (mismo mecanismo que ``IACT_RUN_SCHEDULER``), pero
  la query es defensiva.
- **R-EXP-02:** retries limitados a 3 con backoff
  exponencial (30s -> 120s -> 480s). Tras attempts=3 el job
  queda FAILED definitivo.
- **R-EXP-03:** archivos en ``StorageGateway`` con TTL = 7
  dias (configurable via ``settings.EXPORT_TTL_DAYS``).
  Housekeeping job purga archivos y registros expirados.
- **R-EXP-04:** sin Celery (``ADR-BACK-012``). Si se requiere
  scaling horizontal de workers, este patron necesita
  reemplazarse por Celery + RabbitMQ — documentado como
  deuda tecnica.
- **R-EXP-05:** el worker NO bloquea la generacion en una
  transaccion DB. La transaccion se cierra DESPUES del
  upload a Storage. Si el upload falla, el job queda en
  ``PROCESSING`` y el housekeeping lo recupera (timeout +
  retry).

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Archivo
 * - ExportView
   - ``apps/reports/api/views.py: ExportRequestView,
     ExportStatusView``
 * - ExportService
   - ``apps/reports/services/export_service.py``
 * - ExportWorker
   - ``apps/reports/jobs/export_worker.py``
 * - StorageGateway
   - ``apps/reports/gateways/storage_gateway.py``
 * - ExportJob ORM
   - ``apps/reports/models.py: ExportJobORM``

----

.. seealso::

 - :doc:`interaction-pattern` — flow sincrono.
 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/reports/async-export-flow` —
   flujo en DesignView.
 - :doc:`/arquitectura-tecnica/design-view/reports/export-job-lifecycle` —
   FSM de ``ExportJob``.

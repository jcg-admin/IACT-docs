.. meta::
 :artefacto: AT_IMPL_SEQ_PIPELINE
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_pipeline:

============================================================
Implementation View — MOD_Pipeline: Patron de Interaccion
============================================================

Secuencia para el flujo "consultar estado del pipeline ETL"
(UC_PIP_01) — el camino mas comun. Las views son thin
controllers que delegan en service + repository sobre
``etl_runs`` y ``job_execution_log``.

.. uml::
 :caption: MOD_Pipeline impl seq — view → service → repo (lectura).

 @startuml

 actor PipelineAdmin
 participant "PipelineStatusView\n(APIView)" as View <<api>>
 participant "PipelineService" as Service <<service>>
 participant "ETLRunRepository" as RunRepo <<repository>>
 participant "JobLogRepository" as LogRepo <<repository>>
 participant "ETLRunORM" as ORM <<orm>>
 database MariaDB

 PipelineAdmin -> View : GET /api/v1/etl/supervision/
 activate View

 View -> View : permission_classes\n[function_perm("view_pipeline_status")]

 View -> Service : get_summary()
 activate Service

 Service -> RunRepo : last_successful()
 activate RunRepo
 RunRepo -> ORM : ETLRunORM.objects\n.filter(status='success')\n.order_by('-end_time').first()
 ORM -> MariaDB : SELECT ... LIMIT 1
 MariaDB --> ORM
 ORM --> RunRepo
 RunRepo --> Service : ETLRun | None
 deactivate RunRepo

 Service -> RunRepo : count_last_24h_by_status()
 activate RunRepo
 RunRepo -> ORM : aggregate Count(*) GROUP BY status
 ORM --> RunRepo
 RunRepo --> Service : {success: N, failed: M}
 deactivate RunRepo

 Service -> LogRepo : current_running_step()
 activate LogRepo
 LogRepo -> ORM : JobExecutionLogORM.objects\n.filter(status='RUNNING').first()
 ORM --> LogRepo
 LogRepo --> Service : JobLog | None
 deactivate LogRepo

 Service --> View : SummaryDTO(\nestado_general,\nultima_ejecucion,\nen_curso,\ntotal_24h)
 deactivate Service

 View --> PipelineAdmin : HTTP 200 + JSON
 deactivate View

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View
   - ``apps/pipeline/api/views.py: PipelineStatusView,
     PipelineErrorsView, DataAvailabilityView,
     PipelineRetryView``
 * - Service
   - ``apps/pipeline/services/pipeline_service.py``
 * - Repositories
   - ``apps/pipeline/repositories/etl_run_repo.py``
     ``apps/pipeline/repositories/job_log_repo.py``
 * - ORM
   - ``apps/pipeline/models.py:
     ETLRunORM, JobExecutionLogORM, JobConfigORM``
 * - SP invokers
   - ``apps/pipeline/services/sp_runner.py`` —
     wrapper de ``cursor.callproc()`` para
     ``sp_etl_maestro``, ``sp_etl_historico``.

Distincion vs. el Servicio ETL
================================

El **Servicio ETL** real (los SPs ``sp_etl_*`` en MariaDB)
NO esta en este modulo Django. Vive en MariaDB y se invoca
via ``cursor.callproc()`` desde ``sp_runner``. El modulo
Django ``MOD_Pipeline`` es **el monitor** del Servicio ETL,
no el Servicio ETL en si.

----

Invariantes de implementacion
==============================

- **I-IMPL-PIP-01:** ningun view de este modulo escribe en
  ``base_ivr_*`` ni en ``tbl_historico_*``. Solo lee de
  ``etl_runs`` y ``job_execution_log``.
- **I-IMPL-PIP-02:** ``PipelineRetryView`` (UC_PIP_04) NO
  invoca el SP directamente — agenda un job y devuelve
  ``run_id``. El SP corre en background.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`etl-execution-binding` — patron de scheduling
   (Django mgmt cmd + APScheduler + heartbeat threading).
 - :doc:`/arquitectura-tecnica/pipeline-etl-iact/index` —
   spec de implementacion del Servicio ETL completo.
 - :doc:`/arquitectura-tecnica/design-view/pipeline/etl-execution-flow` —
   flujo en DesignView.

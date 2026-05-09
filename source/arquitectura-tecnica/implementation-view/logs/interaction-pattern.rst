.. meta::
 :artefacto: AT_IMPL_SEQ_LOGS
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: logs
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_logs:

============================================================
Implementation View — MOD_Logs: Patron de Interaccion
============================================================

Secuencias del modulo: (1) escritura via Django logging
handler, (2) consulta via REST y (3) job de retencion. Los
3 son simples — el modulo no tiene patrones transversales
no-obvios.

Escritura
==========

.. uml::
 :caption: MOD_Logs impl seq — write via Django LogHandler.

 @startuml

 participant "Cualquier modulo\n(logger.info(...))" as Caller
 participant "DjangoLogger" as Logger <<library>>
 participant "DBLogHandler" as Handler <<handler>>
 participant "LogRepository" as Repo <<repository>>
 participant "InfrastructureLogORM" as ORM <<orm>>
 database PostgreSQL

 Caller -> Logger : .info("event", extra={"key": "value"})
 activate Logger
 Logger -> Handler : emit(LogRecord)
 activate Handler

 Handler -> Handler : filter por level\n(>= settings.DB_LOG_LEVEL)
 alt level >= threshold
   Handler -> Repo : create(level, message, extra,\ntraceback?)
   activate Repo
   Repo -> ORM : InfrastructureLogORM.objects.create(...)
   ORM -> PostgreSQL : INSERT INTO infrastructure_log ...
   Repo --> Handler : Log
   deactivate Repo
 end
 deactivate Handler
 deactivate Logger

 @enduml

Consulta
=========

.. uml::
 :caption: MOD_Logs impl seq — query via REST.

 @startuml

 actor PipelineAdmin
 participant "LogQueryView\n(APIView)" as View <<api>>
 participant "LogService" as Svc <<service>>
 participant "LogRepository" as Repo <<repository>>
 database PostgreSQL

 PipelineAdmin -> View : GET /api/v1/logs/?level=ERROR&from=...&to=...
 activate View

 View -> View : permission_classes\n[function_perm("view_logs")]

 View -> Svc : query(filters)
 activate Svc
 Svc -> Repo : search(filters, limit=100, offset=0)
 activate Repo
 Repo -> PostgreSQL : SELECT * FROM infrastructure_log\nWHERE level = ? AND ...\nORDER BY id DESC LIMIT 100 OFFSET 0
 PostgreSQL --> Repo
 Repo --> Svc : list[Log] + count
 deactivate Repo
 Svc --> View : paginated result
 deactivate Svc

 View --> PipelineAdmin : HTTP 200 + JSON
 deactivate View

 @enduml

Job de retencion
=================

El job de retencion vive en
:doc:`/arquitectura-tecnica/design-view/logs/log-retention-flow`
(activity diagram). En implementacion se ejecuta como un
APScheduler tick diario (mismo mecanismo descrito en
:doc:`/arquitectura-tecnica/implementation-view/alerts/evaluator-scheduler-binding`),
con la diferencia de que el cron es ``@daily 03:30 AM`` y
no ``every 60s``.

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View
   - ``apps/logs/api/views.py: LogQueryView``
 * - Service
   - ``apps/logs/services/log_service.py``
 * - Repository
   - ``apps/logs/repositories/log_repo.py``
 * - DB log handler
   - ``apps/logs/handlers.py: DBLogHandler``
 * - Retention job
   - ``apps/logs/jobs/retention_job.py``

Invariantes de implementacion
==============================

- **I-IMPL-LOG-01:** ``DBLogHandler.emit`` es **fail-safe**:
  cualquier excepcion durante el INSERT se atrapa y se
  emite a stderr (formato fallback). Un bug en el handler
  NUNCA debe propagarse a la app que llamo ``logger.info``.
- **I-IMPL-LOG-02:** ``LogService.query`` aplica
  ``permission_classes`` en el view + filtrado por
  ``module`` opcional — el operador puede ver solo logs
  de modulos a los que tiene acceso (cross-modulo a
  MOD_Permissions).
- **I-IMPL-LOG-03:** la retencion respeta
  :doc:`/arquitectura-tecnica/design-view/logs/log-retention-flow`
  — ``CRITICAL`` y entries con ``preserve=TRUE`` no se
  purgan.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/logs/log-retention-flow` —
   politica de retencion en DesignView.
 - :doc:`/arquitectura-tecnica/implementation-view/audit/audit-capture-middleware-pattern` —
   distincion vs audit (MOD_Logs es operativo, MOD_Audit
   es regulatorio).

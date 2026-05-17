.. meta::
 :artefacto: AT_IMPL_SEQ_AUDIT
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_audit:

============================================================
Implementation View — MOD_Audit: Patron de Interaccion
============================================================

Secuencia de captura y persistencia de un ``AuditEvent``.
Hay dos caminos principales: captura **automatica** (via
middleware, transversal a todos los requests) y captura
**explicita** (services llamando ``AuditService.record``).

.. uml::
 :caption: MOD_Audit impl seq — captura via middleware + persist con hash chain.

 @startuml

 actor "Cualquier request" as Req
 participant "DRF View\n(modulo X)" as View
 participant "AuditMiddleware\n(MIDDLEWARE setting)" as MW <<middleware>>
 participant "AuditService" as Svc <<service>>
 participant "AuditEventRepository" as Repo <<repository>>
 participant "AuditEventORM" as ORM <<orm>>
 database PostgreSQL

 Req -> MW : process_request
 activate MW
 MW -> MW : record start_time, request_meta
 deactivate MW

 Req -> View : dispatch
 activate View
 View --> Req : response
 deactivate View

 Req -> MW : process_response
 activate MW
 alt path requiere audit\n(via decorator @audited\no PATTERN match)
   MW -> Svc : record(event_type, actor, target,\nrequest_meta, response_meta)
   activate Svc

   Svc -> Repo : last_hash()
   activate Repo
   Repo -> ORM : .order_by('-id').first()
   ORM --> Repo : prev | None
   Repo --> Svc : prev_hash | NULL
   deactivate Repo

   Svc -> Svc : compute hash(\nprev_hash + payload)
   Svc -> Repo : create(payload, hash, prev_hash)
   activate Repo
   Repo -> ORM : AuditEventORM.objects.create(...)
   ORM -> PostgreSQL : INSERT INTO audit_event ...
   PostgreSQL --> ORM
   ORM --> Repo : AuditEvent
   Repo --> Svc : AuditEvent
   deactivate Repo

   Svc --> MW : ok
   deactivate Svc
 end
 deactivate MW

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View (consulta)
   - ``apps/audit/api/views.py: AuditEventListView,
     AuditExportView``
 * - Middleware
   - ``apps/audit/middleware.py: AuditMiddleware``
 * - Service
   - ``apps/audit/services/audit_service.py``
 * - Repository
   - ``apps/audit/repositories/audit_event_repo.py``
 * - ORM
   - ``apps/audit/models.py: AuditEventORM``

Invariantes de implementacion
==============================

- **I-IMPL-AUD-01:** ``AuditEventORM`` no tiene metodo
  ``save()`` con UPDATE — solo ``create()``. El ORM se
  configura con
  ``Meta.permissions = []`` para que Django-admin no permita
  edicion.
- **I-IMPL-AUD-02:** el ``hash`` se computa con SHA-256 sobre
  el payload + ``prev_hash``. Si ``prev_hash`` es NULL (primer
  evento), se usa una constante ``GENESIS_HASH``.
- **I-IMPL-AUD-03:** el middleware NO consume excepciones de
  ``AuditService`` — si la persistencia del audit falla, el
  request normal sigue, pero se emite alerta inmediata
  (``audit gap``) y log de error.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`audit-capture-middleware-pattern` — patron del
   middleware (transversal a todos los modulos).
 - :doc:`/arquitectura-tecnica/design-view/audit/audit-event-lifecycle` —
   FSM en DesignView.

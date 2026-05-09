.. meta::
 :artefacto: AT_IMPL_PATTERN_AUDIT_CAPTURE_MIDDLEWARE
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: audit
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_audit_capture_middleware:

============================================================
Implementation View — Audit Capture Middleware (transversal)
============================================================

Patron transversal de captura automatica de eventos de
auditoria. Vive en MOD_Audit pero **se aplica a todos los
requests del corpus** via Django MIDDLEWARE setting.
Critico para CNST-025 (trazabilidad regulatoria).

Mecanismos de captura
======================

Hay tres mecanismos coexistentes:

1. **Implicit (path-based):** el middleware reconoce paths
   en una whitelist (``settings.AUDITED_PATHS``) y captura
   automaticamente.
2. **Decorator (@audited):** views especificas se marcan con
   un decorator que indica el ``event_type``.
3. **Explicit (service.record):** services internos invocan
   ``AuditService.record`` directamente cuando una operacion
   de dominio (no exposed via HTTP) requiere audit
   (e.g. ETL backfill manual).

.. uml::
 :caption: Pipeline de captura — middleware + decorator + explicit.

 @startuml

 participant Client
 participant "AuditMiddleware" as MW <<middleware>>
 participant "DRF View" as View
 participant "AuditService" as Svc <<service>>

 Client -> MW : request
 activate MW
 MW -> MW : process_request:\ncapture context (start_time,\nactor, ip, ua, path, method)
 MW -> View : dispatch
 activate View
 View --> MW : response
 deactivate View

 MW -> MW : process_response:\nevaluar reglas

 alt path en AUDITED_PATHS\nor view @audited
   MW -> Svc : record(event_type, ctx, response_meta)
   activate Svc
   Svc --> MW : ok
   deactivate Svc
 else sin match
   note right of MW: no audit emitido
 end

 MW --> Client : response
 deactivate MW

 @enduml

Implementacion del middleware
==============================

.. code-block:: python

   # apps/audit/middleware.py
   class AuditMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response
           self._audited_paths = set(settings.AUDITED_PATHS)

       def __call__(self, request):
           request._audit_ctx = self._capture_context(request)
           response = self.get_response(request)
           self._maybe_record(request, response)
           return response

       def _capture_context(self, request) -> dict:
           return {
               "start_time": timezone.now(),
               "actor": getattr(request.user, "id", None),
               "ip": _client_ip(request),
               "ua": request.META.get("HTTP_USER_AGENT", ""),
               "path": request.path,
               "method": request.method,
           }

       def _maybe_record(self, request, response) -> None:
           view_func = getattr(request, "_audit_view_func", None)
           audited_decorator = getattr(view_func, "_audited", None)

           event_type = None
           if audited_decorator:
               event_type = audited_decorator.event_type
           elif self._matches_implicit(request.path):
               event_type = self._implicit_event_type(request)

           if event_type is None:
               return

           try:
               audit_service.record(
                   event_type=event_type,
                   ctx=request._audit_ctx,
                   response_status=response.status_code,
               )
           except Exception:
               # NO swallow silently — alert + continue
               logger.exception("audit capture failed")
               _emit_audit_gap_alert(request._audit_ctx)

Decorator @audited
===================

.. code-block:: python

   # apps/audit/decorators.py
   def audited(event_type: str):
       def decorator(view_func):
           @wraps(view_func)
           def wrapper(request, *args, **kwargs):
               request._audit_view_func = view_func
               return view_func(request, *args, **kwargs)
           wrapper._audited = SimpleNamespace(event_type=event_type)
           return wrapper
       return decorator

Uso:

.. code-block:: python

   class AssignmentView(APIView):
       @audited("ACCESS_CHANGE")
       def post(self, request):
           ...

Restricciones de implementacion
================================

- **R-AUD-01:** ``MIDDLEWARE`` setting incluye
  ``apps.audit.middleware.AuditMiddleware`` **DESPUES** de
  ``AuthenticationMiddleware`` — el actor solo es conocible
  tras autenticacion.
- **R-AUD-02:** la persistencia es **best-effort** desde el
  punto de vista del request — un fallo en
  ``audit_service.record`` NO aborta el response, pero emite
  alerta operativa (``audit_gap``) que dispara investigacion.
  Trade-off: regulatoriamente preferible "no perder requests"
  vs. "no perder evento de audit"; el rule actual prioriza
  el primero porque CNST-025 acepta gaps si hay alerting.
- **R-AUD-03:** ``hash`` chain (SHA-256) computado en el
  service — el middleware NO toca hashing.
- **R-AUD-04:** payload no incluye request body crudo. Solo
  metadata: ``actor, ip, ua, path, method, status, target_id,
  event_type``. Esto evita PII en el log de audit
  (CNST-026: PII solo en log operativo, no en audit).

Path matching
==============

``settings.AUDITED_PATHS`` es una lista de patterns:

.. code-block:: python

   AUDITED_PATHS = [
       (r"^/api/v1/users/", "USER_CHANGE"),
       (r"^/api/v1/access/assignments/", "ACCESS_CHANGE"),
       (r"^/api/v1/permissions/groups/", "PERMISSION_CHANGE"),
       (r"^/api/v1/etl/.*/retry/$", "PIPELINE_CHANGE"),
       (r"^/api/v1/auth/login/$", "AUTH_LOGIN"),
       (r"^/api/v1/auth/logout/$", "AUTH_LOGOUT"),
   ]

Uso de regex permite cubrir endpoints sin requerir tocar el
codigo del view.

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 30 70
 :header-rows: 1

 * - Componente
   - Archivo
 * - Middleware
   - ``apps/audit/middleware.py``
 * - Decorator
   - ``apps/audit/decorators.py``
 * - Audit service
   - ``apps/audit/services/audit_service.py``
 * - Settings
   - ``config/settings/base.py: AUDITED_PATHS``
 * - Audit gap alert
   - ``apps/audit/alerts.py: _emit_audit_gap_alert``

----

.. seealso::

 - :doc:`interaction-pattern` — flow de captura.
 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/audit/audit-event-lifecycle` —
   FSM del evento.
 - :doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern` —
   uno de los productores principales de eventos.

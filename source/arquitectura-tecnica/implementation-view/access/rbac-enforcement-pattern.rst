.. meta::
 :artefacto: AT_IMPL_PATTERN_RBAC_ENFORCEMENT
 :tipo: Diagrama Arquitectonico — Implementation View — Pattern
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_impl_pattern_rbac_enforcement:

============================================================
Implementation View — Patron de RBAC Enforcement
============================================================

Patron transversal que aplica el control de acceso RBAC en
todas las views DRF del sistema IACT. Vive logicamente en
MOD_Access (define el patron) pero **lo consumen todos los
modulos**: pipeline, alerts, reports, etc.

El patron tiene 3 capas:

1. **JWT authentication** (Django middleware) — extrae el
   ``request.user`` del token.
2. **DRF permission class** (``HasFunctionPerm``) — valida
   que ``request.user`` tiene la ``Function`` requerida.
3. **In-method check** (``permissions_service.has(...)``) —
   verifica permisos a nivel de objeto cuando aplica
   (e.g. asignaciones limitadas a un segmento del usuario).

.. uml::
 :caption: RBAC enforcement — pipeline de 3 capas por request DRF.

 @startuml

 actor Client
 participant "DRF View" as View
 participant "JWTAuthentication" as JWT <<middleware>>
 participant "HasFunctionPerm\n(DRF perm class)" as Perm <<permission>>
 participant "PermissionsService" as PS <<service>>
 participant "Service de modulo\n(e.g. AccessService)" as Svc <<service>>

 Client -> View : request (JWT en Authorization header)
 activate View

 View -> JWT : authenticate(request)
 activate JWT
 JWT --> View : (request.user, jwt_claims)
 deactivate JWT

 View -> Perm : has_permission(request, view)
 activate Perm
 Perm -> PS : has(user, function_codename)
 activate PS
 note right of PS
   PermissionsService consulta
   cache en memoria (LRU + TTL)
   poblada por background job de
   sync. Hot path sin BD.
 end note
 PS --> Perm : True / False
 deactivate PS
 alt False
   Perm --> View : False
   View --> Client : HTTP 403 Forbidden
 else True
   Perm --> View : True
 end
 deactivate Perm

 View -> Svc : action(...)
 activate Svc
 opt object-level check
   Svc -> PS : has(user, codename, target=obj)
   PS --> Svc : True / False
   alt False
     Svc --> View : raise PermissionDenied
     View --> Client : HTTP 403
   end
 end
 Svc --> View : result
 deactivate Svc

 View --> Client : HTTP 200 + body
 deactivate View

 @enduml

----

Componentes del patron
=======================

DRF Permission classes (en ``apps/access/permissions.py``)
----------------------------------------------------------

.. code-block:: python

   class HasFunctionPerm(BasePermission):
       """Generica — usar via factory por function codename."""
       function_codename: str = ""

       def has_permission(self, request, view):
           if not request.user.is_authenticated:
               return False
           return permissions_service.has(
               user=request.user,
               codename=self.function_codename,
           )

   def function_perm(codename: str) -> type[BasePermission]:
       """Factory: produce subclase con codename concreto."""
       cls = type(
           f"HasFunc_{codename}",
           (HasFunctionPerm,),
           {"function_codename": codename},
       )
       return cls

Uso en cada view del corpus:

.. code-block:: python

   class AssignmentView(APIView):
       permission_classes = [function_perm("assign_functions_to_group")]

   class PipelineRetryView(APIView):
       permission_classes = [function_perm("request_pipeline_retry")]

PermissionsService cache (en
``apps/permissions/services/permissions_service.py``)
-----------------------------------------------------

- Backed by ``functools.lru_cache`` con TTL via
  ``cachetools.TTLCache``.
- Invalidacion: el ``AccessService`` llama
  ``permissions_service.invalidate(user_id)`` tras cualquier
  cambio en asignaciones.
- ADR-BACK-012 (sin Redis): el cache es **per-process**. En
  un setup multi-worker, cada worker tiene su copia. La
  invalidacion via signal Django se publica a todos los
  workers en el host (in-process); cross-host no aplica
  porque el deploy actual es single-host (ver
  :doc:`/arquitectura-tecnica/deploy-view/standard-topology`).

----

Reglas operativas
==================

- **R-RBAC-01:** ninguna view DRF puede omitir
  ``permission_classes``. Un linter (``apps/access/lint/
  check_views.py``) valida en CI que toda view tiene la
  declaracion.
- **R-RBAC-02:** el codename usado en
  ``function_perm("...")`` debe existir en el catalogo de
  ``Function`` (validado en migraciones).
- **R-RBAC-03:** los object-level checks (``Svc -> PS``)
  son obligatorios cuando la operacion lee/modifica datos
  segmentables (e.g. reportes filtrables por segmento del
  usuario).

----

.. seealso::

 - :doc:`interaction-pattern` — patron concreto en
   MOD_Access.
 - :doc:`layer-structure` — componentes del modulo.
 - :doc:`/arquitectura-tecnica/design-view/access/separation-check-flow` —
   flujo SoD que usa este patron.
 - :doc:`/arquitectura-tecnica/modulos/permissions/index` —
   modulo de resolucion del conjunto efectivo.

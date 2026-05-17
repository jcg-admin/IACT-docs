.. meta::
 :artefacto: AT_DM_CLASS_AUTHORIZATION_GUARD
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_authorization_guard:

==================
AuthorizationGuard
==================

Componente cross-cutting que verifica que el actor autenticado posee la
funcion RBAC requerida para invocar un endpoint o ejecutar una accion
del sistema. Es la frontera de control de acceso a nivel funcion (P-15
RBAC granular) — toda escritura/lectura sensible pasa por aqui antes
de llegar al servicio de negocio.

Consume la decision de ``PermissionService`` (que a su vez consulta
``PermissionCache``) y emite ``AuditEvent`` de tipo ``ACCESS_DENIED``
o ``AUTHORIZATION_OK`` segun resultado. Falla cerrada (deny by default)
cuando hay error tecnico (CNST-008 isolation).

.. uml::
 :caption: Clase AuthorizationGuard — verificacion de funcion RBAC.

 @startuml

 class AuthorizationGuard {
   - permission_service : PermissionService
   - audit_service : AuditService
   --
   + check(user_id : UUID, function_codename : String, ctx : Context) : Boolean
   + check_or_raise(user_id : UUID, function_codename : String, ctx : Context) : void
   + check_bulk(user_id : UUID, function_codenames : List<String>, ctx : Context) : Map<String, Boolean>
   + decide(request : Request) : AuthorizationDecision
 }

 class AuthorizationDecision {
   + allowed : Boolean
   + matched_function : String
   + reason : String
   + decided_at : DateTime
 }

 AuthorizationGuard --> PermissionService : consulta
 AuthorizationGuard --> AuditService     : emite
 AuthorizationGuard ..> AuthorizationDecision : produce

 note bottom of AuthorizationGuard
   CNST-008: fail-closed por default.
   BR-006 NIST RBAC Flat: verificacion
   sobre funcion canonica, no sobre rol.
   P-15: una funcion por request.
 end note

 @enduml

Trazabilidad a UCs
==================

AuthorizationGuard es referenciado por toda escritura/lectura sensible.
UCs que lo invocan explicitamente:

- :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` —
  verifica ``create_separation_rule``, ``update_separation_rule``,
  ``disable_separation_rule``, ``view_separation_rules``.
- :doc:`/requisitos/casos-uso/admin/uc-adm-02/index` —
  verifica funciones de catalogo de Function.
- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  verifica ``assign_functions_to_group``.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-03/index` —
  verifica ``grant_exceptional_permission``.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-04/index` —
  verifica ``revoke_exceptional_permission``.
- :doc:`/requisitos/casos-uso/access/uc-acc-01/index` —
  verifica ``assign_functions``.
- :doc:`/requisitos/casos-uso/access/uc-acc-02/index` —
  verifica ``revoke_functions``.
- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  verifica ``assign_function_groups``.
- :doc:`/requisitos/casos-uso/audit/uc-aud-03/index` —
  verifica ``export_audit_log``.
- :doc:`/requisitos/casos-uso/audit/uc-aud-04/index` —
  verifica ``generate_compliance_report``.

Relaciones
==========

- :doc:`permission-service` — fuente de la decision (consulta cache + RBAC).
- :doc:`permission-cache` — capa de cache consultada via PermissionService.
- :doc:`audit-service` — emisor de ``ACCESS_DENIED`` / ``AUTHORIZATION_OK``.
- :doc:`audit-event` — estructura del evento emitido.
- :doc:`session` — contexto del request (token JWT, user_id).

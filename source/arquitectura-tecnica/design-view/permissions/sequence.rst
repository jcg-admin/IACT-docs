.. meta::
 :artefacto: AT_DESIGN_SEQ_PERMISSIONS
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: permissions
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_permissions:

============================================================
Design View — MOD_Permissions: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Permissions: verificacion en
runtime de un permiso para un usuario y funcion. Es el patron
invocado en CADA operacion del sistema (gateway de autorizacion).

.. uml::
 :caption: MOD_Permissions — verify(user, function) en runtime.

 @startuml

 actor "verify_user_permission" as verify_user_permission
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PermissionService" as PermissionService <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "ExceptionalPermissionRepo" as ExceptionalPermissionRepo <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 verify_user_permission -> AuthorizationGuard : verify()
 activate AuthorizationGuard

 AuthorizationGuard -> PermissionService : check(user, function)
 activate PermissionService

 PermissionService -> PermissionCache : get(user)
 activate PermissionCache
 alt cache hit
   PermissionCache --> PermissionService : effective_set
 else cache miss
   PermissionCache --> PermissionService : null
   PermissionService -> EffectivePermissionsAggregator : compute(user)
   activate EffectivePermissionsAggregator
   EffectivePermissionsAggregator -> ExceptionalPermissionRepo : list(user)
   ExceptionalPermissionRepo --> EffectivePermissionsAggregator : exceptions
   EffectivePermissionsAggregator --> PermissionService : effective_set
   deactivate EffectivePermissionsAggregator
   PermissionService -> PermissionCache : put(user, set)
 end
 deactivate PermissionCache

 PermissionService --> AuthorizationGuard : grant|deny
 deactivate PermissionService

 AuthorizationGuard -> AuditService : emit(AuditEvent\nresult=grant|deny)
 AuditService --> AuthorizationGuard : OK
 AuthorizationGuard --> verify_user_permission : grant|deny
 deactivate AuthorizationGuard

 note right of EffectivePermissionsAggregator
   effective_set =
     UNION(assignments, exceptional_grants)
     - exceptional_revokes
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/permissions/class`
 - :doc:`/arquitectura-tecnica/use-case-view/permissions/index`
 - :doc:`/arquitectura-tecnica/design-view/permissions/activity`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/permission-service`
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache`
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator`
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`

.. meta::
 :artefacto: AT_UC_PERM_07_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _at_uc_perm_07_verificar_permiso_de_usuario:

============================================================
UC_PERM_07 — Verificar Permiso (consulta admin)
============================================================

Verifica si un User especifico tiene una funcion especifica. Tiene
dos modos: **interno** (otros UCs lo invocan via PermissionService —
no requiere RBAC adicional) y **admin** (consulta explicita via
endpoint, requiere ``view_assignments``). El modo admin emite audit
P-44 (consulta del sistema RBAC).

.. uml::
 :caption: UC_PERM_07 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_assignments" as view_assignments
 actor "Caller UC interno" as Caller_UC <<sistema>>
 actor "view_audit_log" as view_audit_log <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PermissionService" as PermissionService <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 rectangle "MOD_Permissions" {
   usecase "UC_PERM_07\nVerificar Permiso\nde Usuario\n.. extension points ..\nModoAdmin" as UC_PERM_07
   usecase "Verificar\nview_assignments\n(solo modo admin)" as VERIFICAR_AGR
   usecase "Lookup PermissionCache" as CACHE_LOOKUP
   usecase "Compute fallback\n(EffectivePermissions\nAggregator)" as COMPUTE
   usecase "Verificar funcion\nen effective_set" as VERIFICAR_FN
   usecase "Audit consulta\nP-44 (modo admin)" as AUDITAR
 }

 view_assignments --> UC_PERM_07
 Caller_UC --> UC_PERM_07

 UC_PERM_07 ..> CACHE_LOOKUP : <<include>>
 UC_PERM_07 ..> COMPUTE : <<include>>
 UC_PERM_07 ..> VERIFICAR_FN : <<include>>
 AUDITAR ..> UC_PERM_07 : <<extend>> (ModoAdmin)
 VERIFICAR_AGR ..> UC_PERM_07 : <<extend>> (ModoAdmin)

 CACHE_LOOKUP --> PermissionCache
 COMPUTE --> EffectivePermissionsAggregator
 VERIFICAR_FN --> PermissionService
 VERIFICAR_AGR --> AuthorizationGuard
 AUDITAR --> AuditService
 AuditService --> view_audit_log

 note bottom of UC_PERM_07
   Dos modos:
   - Interno: otros UCs invocan
     PermissionService directo
     (no RBAC, no audit).
   - Admin: endpoint explicito
     con view_assignments + audit P-44.
 end note

 note bottom of CACHE_LOOKUP
   Hot path: cache hit ratio alto.
   Compute fallback solo si miss
   o cache invalidada.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/permission-service` —
   servicio principal de verificacion.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   cache hot path.
 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   compute fallback.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   fuente de Assignment activos.
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` —
   fuente de ExceptionalPermission no vencidos.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_assignments en modo admin.
 - :doc:`/arquitectura-tecnica/domain-model/audit-service` —
   emisor (modo admin).
 - :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index` —
   spec textual.

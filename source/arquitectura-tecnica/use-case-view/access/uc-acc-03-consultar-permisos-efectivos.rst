.. meta::
 :artefacto: AT_UC_ACC_03_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: access
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_acc_03_consultar_permisos_efectivos:

================================================
UC_ACC_03 — Consultar Permisos Efectivos
================================================

Calcula el ``effective_set`` de funciones de un User combinando
``Assignment`` directos + ``Assignment`` AGR (expandidos) +
``ExceptionalPermission`` activos no vencidos. Read-only. ``view_assignments``
para consulta sobre otros Users; consulta sobre si mismo no requiere
RBAC adicional (auto al rol User).

.. uml::
 :caption: UC_ACC_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_assignments" as view_assignments
 actor "User propio" as User_propio <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "EffectivePermissionsAggregator" as EffectivePermissionsAggregator <<sistema>>
 actor "PermissionCache" as PermissionCache <<sistema>>
 actor "AssignmentRepo" as AssignmentRepo <<sistema>>
 actor "ExceptionalPermissionRepo" as ExceptionalPermissionRepo <<sistema>>
 actor "AccessGroup" as AccessGroup <<sistema>>

 rectangle "MOD_Access" {
   usecase "UC_ACC_03\nConsultar Permisos\nEfectivos\n.. extension points ..\nVerOtroUser" as UC_ACC_03
   usecase "Cache lookup" as CACHE_LOOKUP
   usecase "Compute effective_set\n(Assignments + AGRs +\nExceptionalPermissions)" as COMPUTE
   usecase "Filtrar por target_user_id" as FILTRAR_USER
   usecase "Verificar\nview_assignments\n(otro User)" as VERIFICAR_AGR
 }

 view_assignments --> UC_ACC_03
 User_propio --> UC_ACC_03

 UC_ACC_03 ..> CACHE_LOOKUP : <<include>>
 UC_ACC_03 ..> COMPUTE : <<include>>
 UC_ACC_03 ..> FILTRAR_USER : <<include>>
 VERIFICAR_AGR ..> UC_ACC_03 : <<extend>> (VerOtroUser)

 CACHE_LOOKUP --> PermissionCache
 COMPUTE --> EffectivePermissionsAggregator
 EffectivePermissionsAggregator --> AssignmentRepo
 EffectivePermissionsAggregator --> ExceptionalPermissionRepo
 EffectivePermissionsAggregator --> AccessGroup
 VERIFICAR_AGR --> AuthorizationGuard

 note bottom of UC_ACC_03
   Self-query: sin RBAC adicional
   (auto al rol User).
   Cross-User query: requiere
   view_assignments.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/effective-permissions-aggregator` —
   computa effective_set.
 - :doc:`/arquitectura-tecnica/domain-model/permission-cache` —
   hot path.
 - :doc:`/arquitectura-tecnica/domain-model/assignment-repo` —
   Assignments activos.
 - :doc:`/arquitectura-tecnica/domain-model/exceptional-permission-repo` —
   ExceptionalPermission no vencidos.
 - :doc:`/arquitectura-tecnica/domain-model/access-group` —
   AccessGroups asignados.
 - :doc:`/arquitectura-tecnica/domain-model/access-group-function` —
   funciones expandidas.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica view_assignments.
 - :doc:`/requisitos/casos-uso/access/uc-acc-03/index` —
   spec textual.

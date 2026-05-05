.. meta::
 :artefacto: AT_DM_CLASS_EFFECTIVE_PERMISSIONS_AGGREGATOR
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

.. _dm_class_effective_permissions_aggregator:

==============================
EffectivePermissionsAggregator
==============================

Computa el ``effective_set`` de funciones RBAC para un User combinando
todas las fuentes de permisos: ``Assignment`` activos sobre ``Function``
directos + ``Assignment`` sobre ``AccessGroup`` (expandidos a sus
funciones via ``AccessGroupFunction``) + ``ExceptionalPermission``
activos no vencidos. El resultado se cachea en ``PermissionCache``.

Es la pieza que materializa la P-15 RBAC granular: cada User tiene un
set canonico de funciones efectivas que ``PermissionService`` consulta
para autorizacion. Cuando cambia cualquier fuente (assignment nuevo,
revoke, ExceptionalPermission expirada), este aggregator recalcula y
publica el nuevo set.

.. uml::
 :caption: Clase EffectivePermissionsAggregator — computa effective_set.

 @startuml

 class EffectivePermissionsAggregator {
   - assignment_repo : AssignmentRepo
   - exceptional_repo : ExceptionalPermissionRepo
   - access_group_repo : AccessGroupRepo
   - permission_cache : PermissionCache
   --
   + compute(user_id : UUID) : EffectiveSet
   + compute_for_function(user_id : UUID, function : String) : Boolean
   + recompute_after_assign(user_id : UUID, assignment_id : UUID) : void
   + recompute_after_revoke(user_id : UUID, assignment_id : UUID) : void
   + recompute_after_expiry(user_id : UUID, exceptional_id : UUID) : void
 }

 class EffectiveSet {
   + user_id : UUID
   + functions : Set<String>
   + computed_at : DateTime
   + sources : List<PermissionSource>
 }

 enum PermissionSource {
   ASSIGNMENT_DIRECT
   ASSIGNMENT_AGR
   EXCEPTIONAL_PERMISSION
 }

 EffectivePermissionsAggregator --> EffectiveSet : produce
 EffectiveSet -- PermissionSource

 note bottom of EffectivePermissionsAggregator
   Materializa P-15 RBAC granular.
   Recompute cada vez que cambia
   assignment, AGR composition o
   ExceptionalPermission. Resultado
   cacheado en PermissionCache.
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que usan EffectivePermissionsAggregator (consultar/recomputar):

- :doc:`/requisitos/casos-uso/access/uc-acc-03/index` —
  consultar permisos efectivos: compute(user_id).

UCs que disparan recompute (escrituras):

- :doc:`/requisitos/casos-uso/access/uc-acc-01/index` —
  asignar funciones: recompute_after_assign.
- :doc:`/requisitos/casos-uso/access/uc-acc-02/index` —
  revocar funciones: recompute_after_revoke.
- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  asignar AGR: recompute (cascada por funciones del AGR).
- :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
  conceder permiso excepcional: recompute con source=EXCEPTIONAL.
- :doc:`/requisitos/casos-uso/access/uc-acc-09/index` —
  vencimiento: recompute_after_expiry.
- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  modificar AGR composition: recompute para todos los Users con AGR.

Relaciones
==========

- :doc:`assignment-repo` — fuente directa de Assignment activos.
- :doc:`assignment` — entity consumida en agregacion.
- :doc:`access-group-function` — expansion AGR → functions.
- :doc:`exceptional-permission-repo` — fuente de ExceptionalPermission no vencidos.
- :doc:`permission-cache` — cache donde se publica EffectiveSet.
- :doc:`permission-service` — consumidor del EffectiveSet.

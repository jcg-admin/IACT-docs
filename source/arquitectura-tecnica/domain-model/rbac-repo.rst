.. meta::
 :artefacto: AT_DM_CLASS_RBAC_REPO
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: RBAC
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_rbac_repo:

========
RBACRepo
========

Repositorio de consultas RBAC de alto nivel: provee
acceso optimizado a las relaciones que ``PermissionService``
necesita para resolver el ``effective_set`` de un usuario.

A diferencia de ``AssignmentRepo`` y
``ExceptionalPermissionRepo`` (que son CRUD por entidad),
``RBACRepo`` ofrece operaciones **agregadas** orientadas a
verificación rápida (e.g. devolver directamente el set de
``function_code`` resultante sin que el caller tenga que
unir múltiples queries).

.. uml::
 :caption: Clase RBACRepo — consultas agregadas para
           verificación RBAC.

 @startuml

 class RBACRepo {
   - assignment_repo : AssignmentRepo
   - exceptional_permission_repo : ExceptionalPermissionRepo
   --
   + get_active_function_codes(user_id : UUID) : Set<String>
   + get_active_assignments(user_id : UUID) : List<Assignment>
   + get_did_assignments(user_id : UUID) : List<String>
   + is_global_admin(user_id : UUID) : Boolean
   + get_users_with_function(function_code : String) : List<UUID>
   + get_users_in_access_group(access_group_id : UUID) : List<UUID>
 }

 class AssignmentRepo
 class ExceptionalPermissionRepo
 class Function

 RBACRepo "1" o-- "1" AssignmentRepo : aggregates
 RBACRepo "1" o-- "1" ExceptionalPermissionRepo : aggregates
 RBACRepo "1" -- "(user_id, function_code)" Function : resolves

 note right of RBACRepo
   Operaciones agregadas optimizadas
   para path critico de verificacion.
   No reemplaza CRUD por entidad —
   los repos especializados siguen
   siendo el punto de escritura.
 end note

 @enduml

Operaciones principales
=======================

- ``get_active_function_codes(user_id)`` — devuelve set
  de ``function_code`` efectivos para el usuario,
  combinando assignments + exceptional. Operación
  optimizada (single query con joins).
- ``get_active_assignments(user_id)`` — list de
  ``Assignment`` activos.
- ``get_did_assignments(user_id)`` — DIDs (Direct
  Inward Dialing) que el usuario puede usar para outbound;
  subset filtrado de assignments por convención de
  función.
- ``is_global_admin(user_id)`` — short circuit:
  ``global_admin`` ∈ effective_set.
- ``get_users_with_function(function_code)`` — consulta
  inversa: qué usuarios tienen una función. Útil para
  invalidación de cache cuando cambia ``Function``.
- ``get_users_in_access_group(access_group_id)`` —
  inverso de ``Assignment``: usuarios afectados al
  cambiar composición.

Restricciones aplicables
========================

- **CNST-031** — el repo aplica filtros temporales
  (``valid_from``, ``valid_until``) en assignments y
  exceptional permissions.
- **CNST-008** — segmentación: las consultas inversas
  (``get_users_with_function``) respetan el scope del
  invocador si se invocan desde contexto autenticado;
  cuando se invocan desde sistema (cache invalidation)
  no aplican filtro.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`
  — verificación.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-08/index`
  — menú dinámico.
- :doc:`/requisitos/casos-uso/access/uc-acc-03/index` —
  consultar permisos de un usuario.

Relaciones
==========

- Agregación con ``AssignmentRepo`` y
  ``ExceptionalPermissionRepo`` (delegación).
- Usado por ``PermissionService`` (lectura).

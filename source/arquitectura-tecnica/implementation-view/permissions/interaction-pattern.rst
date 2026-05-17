.. meta::
 :artefacto: AT_IMPL_SEQ_PERMISSIONS
 :tipo: Diagrama Arquitectonico — Implementation View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :modulo: permissions
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-09
 :ultimo_cambio: 2026-05-09
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_seq_permissions:

============================================================
Implementation View — MOD_Permissions: Patron de Interaccion
============================================================

Secuencia de "consultar permisos efectivos de un usuario"
(UC_PERM_01) — usado por el endpoint ``/api/v1/permissions/me/``
y consumido internamente por ``HasFunctionPerm`` (ver
:doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern`).

.. uml::
 :caption: MOD_Permissions impl seq — has(user, codename) hot path.

 @startuml

 actor Caller as "Caller\n(View / Permission class)"
 participant "PermissionsService" as PS <<service>>
 participant "EffectiveSetCache" as Cache <<cache>>
 participant "AssignmentRepository" as ARepo <<repository>>
 participant "FunctionRepository" as FRepo <<repository>>
 database PostgreSQL

 Caller -> PS : has(user, codename)
 activate PS

 PS -> Cache : get_or_compute(user.id)
 activate Cache
 alt cache hit (95%+ casos)
   Cache --> PS : EffectiveSet(set[str])
 else cache miss
   Cache -> PS : compute_effective_set(user.id)
   activate PS #DDDDDD
   PS -> ARepo : active_assignments_for(user.id)
   activate ARepo
   ARepo -> PostgreSQL : SELECT a.* FROM assignment a\nWHERE a.user_id = ?\nAND (a.valid_to IS NULL OR a.valid_to > now())
   PostgreSQL --> ARepo
   ARepo --> PS : list[Assignment]
   deactivate ARepo

   PS -> FRepo : functions_in_groups([group_ids])
   activate FRepo
   FRepo -> PostgreSQL : SELECT f.codename FROM function f\nJOIN group_function gf ...
   PostgreSQL --> FRepo
   FRepo --> PS : set[codename]
   deactivate FRepo

   PS --> Cache : EffectiveSet
   deactivate PS
   Cache --> PS : EffectiveSet
 end
 deactivate Cache

 PS --> Caller : codename in EffectiveSet
 deactivate PS

 @enduml

Mapeo a archivos del repo
==========================

.. list-table::
 :widths: 25 75
 :header-rows: 1

 * - Capa
   - Archivo
 * - View (consulta directa)
   - ``apps/permissions/api/views.py: MyPermissionsView,
     UserPermissionsView``
 * - Service
   - ``apps/permissions/services/permissions_service.py``
 * - Cache
   - ``apps/permissions/services/effective_set_cache.py``
 * - Repositories
   - ``apps/permissions/repositories/assignment_repo.py``
     ``apps/permissions/repositories/function_repo.py``

Invariantes de implementacion
==============================

- **I-IMPL-PERM-01:** ``PermissionsService.has`` es**read-only**
  — no escribe a BD. Toda mutacion ocurre en MOD_Access.
- **I-IMPL-PERM-02:** la consulta a ``Assignment`` filtra
  por ``valid_to`` server-side; el cache no incluye
  asignaciones expiradas.
- **I-IMPL-PERM-03:** sin recursion ni herencia de roles
  (CNST-005). El effective set es la **union directa** de
  funciones de los grupos asignados.

----

.. seealso::

 - :doc:`layer-structure` — paquetes del modulo.
 - :doc:`effective-set-cache-pattern` — patron del cache
   transversal (LRU + TTL + invalidation signals).
 - :doc:`/arquitectura-tecnica/design-view/permissions/effective-set-evaluation-flow` —
   flujo en DesignView.
 - :doc:`/arquitectura-tecnica/implementation-view/access/rbac-enforcement-pattern` —
   consumidor principal del cache.

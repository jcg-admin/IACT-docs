.. meta::
 :artefacto: AT_DM_CLASS_ASSIGNMENT_REPO
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

.. _dm_class_assignment_repo:

==============
AssignmentRepo
==============

Repositorio CRUD de ``Assignment`` (asignaciones de
``AccessGroup`` a usuarios). Es el punto único de
escritura para la relación U:N entre ``User`` y
``AccessGroup``.

Cada operación que modifica un ``Assignment`` debe
emitirse acompañada de un ``AuditEvent`` (responsabilidad
del servicio invocante, no del repo) y disparar
invalidación de ``PermissionCache`` para el usuario
afectado.

.. uml::
 :caption: Clase AssignmentRepo — CRUD de Assignment con
           soporte de queries por estado y temporalidad.

 @startuml

 class AssignmentRepo {
   - storage_backend : StorageBackend
   --
   + create(assignment : Assignment) : UUID
   + revoke(assignment_id : UUID, actor_user_id : UUID, reason : String) : Assignment
   + find_active_by_user(user_id : UUID) : List<Assignment>
   + find_by_access_group(access_group_id : UUID) : List<Assignment>
   + get_by_id(assignment_id : UUID) : Assignment
   + count_active(user_id : UUID) : Integer
   + exists_active(user_id : UUID, access_group_id : UUID) : Boolean
 }

 class Assignment
 class AssignmentFilters {
   + state : AssignmentState
   + valid_at : DateTime
 }

 AssignmentRepo "1" -- "(user_id, access_group_id)" Assignment : resolves
 AssignmentRepo "1" ..> "0..*" Assignment : <<persists>>
 AssignmentRepo "1" ..> "0..1" AssignmentFilters : <<uses>>

 note right of AssignmentRepo
   No hay operacion delete: revoke
   marca state=REVOKED y persiste
   reason + revoked_by per BR-009.
 end note

 @enduml

Operaciones principales
=======================

- ``create(assignment)`` — persiste nueva asignación.
  Devuelve ``assignment_id`` generado.
- ``revoke(assignment_id, actor, reason)`` — transición
  ``ACTIVE → REVOKED`` (no delete). Devuelve la
  ``Assignment`` actualizada.
- ``find_active_by_user(user_id)`` — query principal del
  path crítico de verificación; debe ser O(log n) con
  índice apropiado.
- ``find_by_access_group(access_group_id)`` — usuarios
  asignados a un grupo. Útil para invalidación de cache.
- ``exists_active(user_id, access_group_id)`` — short
  circuit booleano para evitar duplicados antes de
  ``create``.

Restricciones aplicables
========================

- **BR-009** — bajas lógicas: nunca DELETE.
- **CNST-031** rango temporal — los assignments con
  ``valid_until`` pasan a ``EXPIRED`` automáticamente
  vía job programado.
- **CNST-025** — toda creación o revocación se audita
  (responsabilidad del servicio invocante).

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  asignar agrupador (``create``).
- :doc:`/requisitos/casos-uso/access/uc-acc-08/index` —
  revocar agrupador (``revoke``).
- :doc:`/requisitos/casos-uso/access/uc-acc-03/index` —
  consultar permisos de usuario (``find_active_by_user``).

Relaciones
==========

- Persiste y consulta ``Assignment``.
- Usado por ``RBACRepo`` (delegación) y por servicios de
  asignación (escritura).

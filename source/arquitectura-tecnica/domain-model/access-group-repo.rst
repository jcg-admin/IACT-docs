.. meta::
 :artefacto: AT_DM_CLASS_ACCESS_GROUP_REPO
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

.. _dm_class_access_group_repo:

===============
AccessGroupRepo
===============

Repositorio CRUD de ``AccessGroup`` (instancias de agrupadores
asignables: AGR-001..012 del sistema mas grupos custom). Distinto de
``FunctionGroupRepo`` (catalogo de agrupadores tipados) — este repo
opera sobre las **instancias** que pueden ser asignadas a Users via
``Assignment.target_type=AccessGroup``.

Punto unico de escritura para crear/desactivar AccessGroup. BR-009
bajas logicas. CNST-008 isolation por segmento donde aplique.

.. uml::
 :caption: Clase AccessGroupRepo — CRUD de AccessGroup.

 @startuml

 class AccessGroupRepo {
   - storage_backend : StorageBackend
   --
   + create(group : AccessGroup) : UUID
   + get_by_id(group_id : UUID) : AccessGroup
   + get_by_code(code : String) : AccessGroup
   + find_active() : List<AccessGroup>
   + find_system() : List<AccessGroup>
   + find_assignable_by_segment(segment_code : String) : List<AccessGroup>
   + update(group_id : UUID, changes : Map) : AccessGroup
   + deactivate(group_id : UUID, actor_id : UUID, reason : String) : AccessGroup
   + exists_code(code : String) : Boolean
 }

 class AccessGroup

 AccessGroupRepo "1" --> "*" AccessGroup : gestiona

 note bottom of AccessGroupRepo
   BR-009 deactivate, no DELETE.
   AGR-001..012 son del sistema
   (no se pueden desactivar via
   este repo — usar UC_ADM_03).
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que escriben (crear/desactivar AGR):

- :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index` —
  gestionar grupos custom: create, update, deactivate.

UCs que leen:

- :doc:`/requisitos/casos-uso/access/uc-acc-04/index` —
  asignar AGR: get_by_id + validar AGR existe + ACTIVE.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-01/index` —
  vista PERM de UC_ACC_04: idem.
- :doc:`/requisitos/casos-uso/access/uc-acc-09/index` —
  vencimiento de agrupador: cron consume find_active.

Relaciones
==========

- :doc:`access-group` — entity gestionada.
- :doc:`function-group-repo` — gestiona la composicion (funciones del AGR).
- :doc:`access-group-function` — relacion M:N AccessGroup ↔ Function.
- :doc:`assignment-repo` — Assignment.target_type=AccessGroup referencia
  esta entity.
- :doc:`audit-service` — emite AGR_CREATED / DEACTIVATED.

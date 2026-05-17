.. meta::
 :artefacto: AT_DM_CLASS_FUNCTION_GROUP_REPO
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

.. _dm_class_function_group_repo:

=================
FunctionGroupRepo
=================

Repositorio CRUD de ``FunctionGroup`` (agrupadores predefinidos AGR-001
a AGR-012 marcados con ``is_system=True``, mas grupos custom creados
en UC_PERM_05 con ``is_system=False``). Es el punto unico de escritura
para gestionar la composicion de los agrupadores y disparar la
recalculacion del effective_set en cascada cuando cambian.

UC_ADM_03 modifica solo grupos del sistema (``is_system=True``);
UC_PERM_05 gestiona grupos custom. Este repo expone ambos paths con
filtros explicitos.

.. uml::
 :caption: Clase FunctionGroupRepo — CRUD de FunctionGroup.

 @startuml

 class FunctionGroupRepo {
   - storage_backend : StorageBackend
   --
   + create(function_group : FunctionGroup) : UUID
   + get_by_id(group_id : UUID) : FunctionGroup
   + get_by_name(name : String) : FunctionGroup
   + find_system() : List<FunctionGroup>
   + find_custom() : List<FunctionGroup>
   + find_active() : List<FunctionGroup>
   + add_function(group_id : UUID, function_id : UUID, actor_id : UUID) : void
   + remove_function(group_id : UUID, function_id : UUID, actor_id : UUID) : void
   + list_functions(group_id : UUID) : List<Function>
   + count_users_with_group(group_id : UUID) : Integer
 }

 class FunctionGroup

 FunctionGroupRepo "1" --> "*" FunctionGroup : gestiona

 note bottom of FunctionGroupRepo
   AGR-001..012: is_system=True
   (mutable solo por system_admin AGR-010).
   Grupos custom: is_system=False
   (UC_PERM_05).
   add/remove disparan recompute en
   cascada (effective_set de Users
   con el grupo asignado).
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que escriben:

- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  modificar AGR de sistema: add_function / remove_function con
  is_system=True validado.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index` —
  gestionar grupos custom: create / update con is_system=False.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index` —
  componer grupo: add_function / remove_function en custom.

UCs que leen:

- :doc:`/requisitos/casos-uso/permissions/uc-perm-05/index` —
  list custom groups.
- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  vista de impacto: count_users_with_group.

Relaciones
==========

- :doc:`function-group` — entity gestionada.
- :doc:`function` — funciones agrupadas.
- :doc:`access-group-function` — relacion M:N entre AGR y funciones.
- :doc:`assignment-repo` — count_users_with_group consulta este repo
  para vista de impacto.
- :doc:`effective-permissions-aggregator` — disparado por add/remove.
- :doc:`audit-service` — emite AGR_FUNCTION_ADDED / REMOVED.

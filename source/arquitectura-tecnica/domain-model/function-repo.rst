.. meta::
 :artefacto: AT_DM_CLASS_FUNCTION_REPO
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

.. _dm_class_function_repo:

============
FunctionRepo
============

Repositorio CRUD del catalogo de ``Function`` (funciones atomicas
RBAC). Punto unico de escritura. BR-009 bajas logicas:
desactivacion transita ``is_active`` a False, no DELETE — preserva
asignaciones historicas.

P-44 codename inmutable: tras creacion, ``codename`` no puede cambiar.
Solo ``description``, ``scope``, ``module`` e ``is_active`` son
editables en update. PermissionsEngine recarga catalogo activo al
cambio.

.. uml::
 :caption: Clase FunctionRepo — CRUD de Function con catalogo activo.

 @startuml

 class FunctionRepo {
   - storage_backend : StorageBackend
   --
   + create(function : Function) : UUID
   + get_by_id(function_id : UUID) : Function
   + get_by_codename(codename : String) : Function
   + find_by_module(module : String) : List<Function>
   + find_active() : List<Function>
   + update(function_id : UUID, changes : Map) : Function
   + deactivate(function_id : UUID, actor_id : UUID) : Function
   + count_active() : Integer
   + exists_codename(codename : String) : Boolean
 }

 class Function

 FunctionRepo "1" --> "*" Function : gestiona

 note bottom of FunctionRepo
   BR-009 bajas logicas.
   P-44 codename inmutable.
   exists_codename verifica unicidad
   en create (CNST-009 codename unique).
 end note

 @enduml

Trazabilidad a UCs
==================

UCs que escriben:

- :doc:`/requisitos/casos-uso/admin/uc-adm-02/index` —
  gestionar catalogo de funciones: create, update, deactivate.

UCs que leen:

- :doc:`/requisitos/casos-uso/admin/uc-adm-02/index` —
  view_functions: find_by_module + find_active.
- :doc:`/requisitos/casos-uso/admin/uc-adm-03/index` —
  validar funcion existe en catalogo: get_by_codename.
- :doc:`/requisitos/casos-uso/admin/uc-adm-01/index` —
  validar funciones de separacion existen en catalogo activo.

Relaciones
==========

- :doc:`function` — entity gestionada.
- :doc:`function-group-repo` — referencia funciones del AGR.
- :doc:`access-group-function` — tabla M:N que une funciones a AGRs.
- :doc:`permission-service` — consume catalogo activo via PermissionCache.
- :doc:`audit-service` — emite FUNCTION_*.

.. meta::
 :artefacto: AT_DM_CLASS_ACCESS_GROUP_FUNCTION
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

.. _dm_class_access_group_function:

===================
AccessGroupFunction
===================

Tabla pivote M:N entre ``AccessGroup`` y ``Function``.
Materializa qué funciones componen un grupo de acceso. Es
el corazón del modelo RBAC v5.5.0: el ``effective_set`` de
funciones de un usuario se calcula vía ``Assignment`` →
``AccessGroup`` → ``AccessGroupFunction`` → ``Function``.

La tabla pivote no tiene operaciones de negocio propias
(es estructural). Las operaciones que la modifican viven
en el servicio que gestiona la composición de
``AccessGroup`` (UC_PERM_06).

.. uml::
 :caption: AccessGroupFunction como **clase de
           asociación** entre AccessGroup y Function.

 @startuml

 class AccessGroup
 class Function
 class AccessGroupFunction {
   + added_at : DateTime
   + added_by : UUID
 }

 AccessGroup "1" -- "1..*" Function : grants
 (AccessGroup, Function) .. AccessGroupFunction

 note right of AccessGroupFunction
   Clase de asociacion (uml-04).
   PK compuesta (access_group_id,
   function_id) implicita en la
   asociacion. added_at/added_by
   para trazabilidad sin auditar.
 end note

 @enduml

Restricciones aplicables
========================

- PK compuesta ``(access_group_id, function_id)`` evita
  duplicados; un par solo puede aparecer una vez.
- **CNST-030** SoD — la composición debe respetar reglas
  de separación de funciones (validado en el servicio
  invocante, no en la entidad).
- **CNST-025** — cambios de composición auditados en
  ``AuditEvent`` con tipo
  ``ACCESS_GROUP_COMPOSITION_CHANGED``.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/permissions/uc-perm-06/index`
  — gestión de composición.
- :doc:`/requisitos/casos-uso/permissions/uc-perm-07/index`
  — verificación de permiso (lectura indirecta para
  resolver ``effective_set``).

Relaciones
==========

- Pertenece a un ``AccessGroup`` (asociación M:1).
- Referencia un ``Function`` (asociación M:1).
- No tiene operaciones de negocio propias; es entidad
  estructural.

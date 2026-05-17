.. meta::
 :artefacto: AT_IMPL_MOD_PERMISSIONS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_permissions:

==========================================
Implementation View — MOD_Permissions
==========================================

Componentes y paquetes de codigo del modulo de permisos RBAC.
Cubre ``FunctionGroup``, ``AccessGroup`` y ``ExceptionalPermission``
con validacion de rango temporal (CNST-031).

.. uml::
 :caption: Implementation View MOD_Permissions — componentes de permisos RBAC.

 @startuml

 package "MOD_Permissions" {
   component "FunctionGroupView\nAccessGroupView\nExceptionalPermView" as PermView <<api>>
   component "FunctionGroupSerializer\nExceptionalPermSerializer" as PermSerializer <<serializer>>
   component "PermissionService\ngestionar grupos y permisos\nvalidar CNST-031" as PermService <<service>>
   component "FunctionGroupRepository\nExceptionalPermRepository\nFunctionRepository" as PermRepo <<repository>>
   component "FunctionGroupORM\nExceptionalPermORM\nFunctionORM" as PermORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 PermView --> PermSerializer : valida
 PermView --> PermService : invoca
 PermService --> PermRepo : consulta / persiste
 PermRepo --> PermORM : mapea
 PermORM --> AlmacenDatos : SQL

 note right of PermService
   ExceptionalPermission{state:PermissionState}.
   CNST-031: validates granted_at < expires_at.
   FunctionGroup "*" -- "*" Function.
   AuditEvent{PERMISSION_GRANT/REVOKE} registrado.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/exceptional-permission`
 :doc:`/arquitectura-tecnica/domain-model/function-group`

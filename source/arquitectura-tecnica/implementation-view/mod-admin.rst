.. meta::
 :artefacto: AT_IMPL_MOD_ADMIN
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_admin:

==========================================
Implementation View — MOD_Admin
==========================================

Componentes y paquetes de codigo del modulo de administracion.
Cubre desactivacion de ``User`` (BR-009: INACTIVE, no DELETE),
revocacion en cascada de ``Assignment`` y auditoria de cambios.

.. uml::
 :caption: Implementation View MOD_Admin — componentes de administracion de usuarios.

 @startuml

 package "MOD_Admin" {
   component "AdminUserView\nDeactivateUserView\nListAdminView" as AdminView <<api>>
   component "AdminUserSerializer" as AdminSerializer <<serializer>>
   component "AdminService\ndesactivar User (BR-009)\nrevocar Assignments en cascada" as AdminService <<service>>
   component "UserRepository\nAssignmentRepository" as AdminRepo <<repository>>
   component "UserORM\nAssignmentORM" as AdminORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 AdminView --> AdminSerializer : valida
 AdminView --> AdminService : invoca
 AdminService --> AdminRepo : consulta / persiste
 AdminRepo --> AdminORM : mapea
 AdminORM --> AlmacenDatos : SQL

 note right of AdminService
   User.deactivate() → state=INACTIVE <<BR-009 v2.0.0>>.
   Assignment.revoke() en cascada por cada asignacion activa.
   AuditEvent{ACCESS_CHANGE} registrado por cada operacion.
   No DELETE — solo transicion de estado.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/domain-model/assignment`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`

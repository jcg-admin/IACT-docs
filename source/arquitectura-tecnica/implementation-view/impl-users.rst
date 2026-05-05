.. meta::
 :artefacto: AT_IMPL_MOD_USERS
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_users:

==========================================
Implementation View — MOD_Users
==========================================

Componentes y paquetes de codigo del modulo de gestion de identidad
de usuarios. Cubre creacion, modificacion, consulta y desactivacion
de ``User`` (BR-009: desactivar, no eliminar).

.. uml::
 :caption: Implementation View MOD_Users — componentes de gestion de usuarios.

 @startuml

 package "MOD_Users" {
   component "UserView\nCreateUserView\nDeactivateUserView\nListUserView" as UserView <<api>>
   component "UserSerializer\nCreateUserSerializer\nUserDetailSerializer" as UserSerializer <<serializer>>
   component "UserService\ngestionar ciclo de vida User\nvalidar unicidad username" as UserService <<service>>
   component "UserRepository" as UserRepo <<repository>>
   component "UserORM" as UserORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 UserView --> UserSerializer : valida
 UserView --> UserService : invoca
 UserService --> UserRepo : consulta / persiste
 UserRepo --> UserORM : mapea
 UserORM --> AlmacenDatos : SQL

 note right of UserService
   User{user_id:UUID, state:UserState}.
   BR-009 v2.0.0: User.deactivate()
   establece state=INACTIVE, no DELETE.
   AuditEvent{ACCESS_CHANGE} en toda modificacion.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`

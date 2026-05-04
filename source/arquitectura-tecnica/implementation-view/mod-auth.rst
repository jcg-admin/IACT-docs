.. meta::
 :artefacto: AT_IMPL_MOD_AUTH
 :tipo: Diagrama Arquitectonico — Implementation View
 :dominio: arquitectura_tecnica
 :subdominio: ImplementationView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_impl_mod_auth:

==========================================
Implementation View — MOD_Auth
==========================================

Componentes y paquetes de codigo del modulo de autenticacion.
Cubre login/logout, gestion de sesiones y recuperacion de contrasena.

.. uml::
 :caption: Implementation View MOD_Auth — componentes de autenticacion.

 @startuml

 package "MOD_Auth" {
   component "AuthView\nLoginView, LogoutView,\nSessionView" as AuthView <<api>>
   component "AuthSerializer\nLoginSerializer,\nTokenSerializer" as AuthSerializer <<serializer>>
   component "AuthService\nvalidar credenciales,\ncrear Session, emitir JWT" as AuthService <<service>>
   component "UserRepository\nSessionRepository" as AuthRepo <<repository>>
   component "UserORM\nSessionORM" as AuthORM <<orm>>
 }

 database "AlmacenDatos\n(PostgreSQL)" as AlmacenDatos

 AuthView --> AuthSerializer : valida
 AuthView --> AuthService : invoca
 AuthService --> AuthRepo : consulta / persiste
 AuthRepo --> AuthORM : mapea
 AuthORM --> AlmacenDatos : SQL

 note right of AuthService
   User.state:UserState validado antes de crear Session.
   Session{session_id:UUID, state:ACTIVE, expires_at}.
   AuditEvent{LOGIN} emitido en cada autenticacion.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/user`
 :doc:`/arquitectura-tecnica/domain-model/session`

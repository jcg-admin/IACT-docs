.. meta::
 :artefacto: AT_DESIGN_CLASS_USERS
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_users:

============================================================
Design View — MOD_Users: Estructura de Clases
============================================================

Modulo de **gestion del ciclo de vida de usuarios**: alta, baja
logica (BR-009), cambio de datos, reset de contrasena. Las
asignaciones RBAC se delegan a MOD_Access.

.. uml::
 :caption: MOD_Users — clases canonicas y relaciones internas.

 @startuml

 class User
 class Assignment
 class Session
 class UserRepo <<sistema>>
 class PasswordGenerator <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 User "1" -- "0..n" Assignment : tiene
 User "1" -- "0..n" Session : sesiones activas

 UserRepo ..> User : CRUD + bajas logicas
 PasswordGenerator ..> User : genera password inicial

 AuthorizationGuard ..> UserRepo : verify_function

 User ..> AuditService : create/update/disable

 note right of UserRepo
   BR-009: bajas logicas
   (state=DISABLED, no DELETE).
 end note

 @enduml

----

UCs cubiertos
==============

UC_USR_01..04 — crear usuario, actualizar, desactivar, reset
contrasena. Ver
:doc:`/arquitectura-tecnica/use-case-view/users/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/assignment`
 - :doc:`/arquitectura-tecnica/domain-model/session`
 - :doc:`/arquitectura-tecnica/domain-model/user-repo`
 - :doc:`/arquitectura-tecnica/domain-model/password-generator`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/users/index`
 - :doc:`/arquitectura-tecnica/design-view/users/sequence`

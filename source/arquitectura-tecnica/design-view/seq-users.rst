.. meta::
 :artefacto: AT_DESIGN_SEQ_USERS
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: users
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_users:

============================================================
Design View — MOD_Users: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Users: alta de un nuevo
``User`` con generacion automatica de password inicial via
``PasswordGenerator``, persistencia via ``UserRepo`` y emision
de AuditEvent.

.. uml::
 :caption: MOD_Users — alta de usuario con password generado.

 @startuml

 actor "create_user" as create_user
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PasswordGenerator" as PasswordGenerator <<sistema>>
 actor "UserRepo" as UserRepo <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 create_user -> AuthorizationGuard : verify()
 activate AuthorizationGuard
 AuthorizationGuard --> create_user : OK
 deactivate AuthorizationGuard

 create_user -> PasswordGenerator : generate()
 activate PasswordGenerator
 PasswordGenerator --> create_user : password_initial
 deactivate PasswordGenerator

 create_user -> UserRepo : create(User{...})
 activate UserRepo
 UserRepo --> create_user : User
 deactivate UserRepo

 create_user -> AuditService : emit(AuditEvent\ntype=user_created)
 activate AuditService
 AuditService --> create_user : OK
 deactivate AuditService

 note right of UserRepo
   BR-009: bajas son logicas
   (state=DISABLED, no DELETE).
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/class-users`
 - :doc:`/arquitectura-tecnica/use-case-view/users/index`
 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/user-repo`
 - :doc:`/arquitectura-tecnica/domain-model/password-generator`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`

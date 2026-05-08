.. meta::
 :artefacto: AT_DESIGN_SEQ_AUTH
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: auth
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_auth:

============================================================
Design View — MOD_Auth: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Auth: login con credenciales,
verificacion de IdempotencyPolicy, creacion de Session con TTL
de ExpirationPolicy, y emision de JWT.

.. uml::
 :caption: MOD_Auth — login con creacion de Session.

 @startuml

 actor "login" as login
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "User" as User <<sistema>>
 actor "IdempotencyPolicy" as IdempotencyPolicy <<sistema>>
 actor "ExpirationPolicy" as ExpirationPolicy <<sistema>>
 actor "Session" as Session <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 login -> User : verify_credentials()
 activate User
 User --> login : OK
 deactivate User

 login -> IdempotencyPolicy : check(request_id)
 activate IdempotencyPolicy
 IdempotencyPolicy --> login : not_duplicate
 deactivate IdempotencyPolicy

 login -> ExpirationPolicy : compute_ttl()
 activate ExpirationPolicy
 ExpirationPolicy --> login : ttl_seconds
 deactivate ExpirationPolicy

 login -> Session : create(user_id, ttl)
 activate Session
 Session --> login : Session{jwt, refresh}
 deactivate Session

 login -> AuditService : emit(AuditEvent\ntype=login)
 activate AuditService
 AuditService --> login : OK
 deactivate AuditService

 login --> AuthorizationGuard : Session disponible para verify futuros

 note right of Session
   P-44: codename inmutable.
   El JWT lleva user_id, no email.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/auth/class`
 - :doc:`/arquitectura-tecnica/design-view/auth/activity`
 - :doc:`/arquitectura-tecnica/design-view/auth/state`
 - :doc:`/arquitectura-tecnica/use-case-view/auth/index`
 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/session`
 - :doc:`/arquitectura-tecnica/domain-model/idempotency-policy`
 - :doc:`/arquitectura-tecnica/domain-model/expiration-policy`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`

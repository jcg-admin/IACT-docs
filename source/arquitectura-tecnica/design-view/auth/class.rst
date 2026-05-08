.. meta::
 :artefacto: AT_DESIGN_CLASS_AUTH
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_auth:

============================================================
Design View — MOD_Auth: Estructura de Clases
============================================================

Modulo **fundamental**: gestion de sesion, JWT, blacklist de
tokens, politicas de expiracion, recuperacion de contrasena.
Sin este modulo no se ejecuta ningun otro.

.. uml::
 :caption: MOD_Auth — clases canonicas y relaciones internas.

 @startuml

 class User
 class Session
 class BlacklistedToken
 class IdempotencyPolicy <<sistema>>
 class ExpirationPolicy <<sistema>>
 class PasswordGenerator <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 User "1" -- "0..n" Session
 BlacklistedToken --> Session : invalida
 ExpirationPolicy --> Session : aplica TTL
 IdempotencyPolicy ..> Session : evita re-uso

 PasswordGenerator ..> User : reset

 AuthorizationGuard ..> Session : valida activa
 AuthorizationGuard ..> BlacklistedToken : verifica
 AuthorizationGuard ..> ExpirationPolicy : check ttl

 Session ..> AuditService : login/logout
 BlacklistedToken ..> AuditService : on revoke
 PasswordGenerator ..> AuditService : on reset

 @enduml

----

UCs cubiertos
==============

UC_AUTH_01..05 — login, logout, recuperar contrasena, cambiar
contrasena, gestionar sesiones. Ver
:doc:`/arquitectura-tecnica/use-case-view/auth/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/user`
 - :doc:`/arquitectura-tecnica/domain-model/session`
 - :doc:`/arquitectura-tecnica/domain-model/blacklisted-token`
 - :doc:`/arquitectura-tecnica/domain-model/idempotency-policy`
 - :doc:`/arquitectura-tecnica/domain-model/expiration-policy`
 - :doc:`/arquitectura-tecnica/domain-model/password-generator`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/auth/index`
 - :doc:`/arquitectura-tecnica/design-view/auth/sequence`

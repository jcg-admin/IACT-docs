.. meta::
 :artefacto: AT_DESIGN_MOD_AUTH
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: auth
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_auth:

============================================================
Design View — MOD_Auth: Vista de Diseño
============================================================

Caja del modulo **MOD_Auth** (autenticacion + sesiones +
gateway de autorizacion runtime). Cubre login, logout,
recuperacion y cambio de password, gestion del ciclo de
vida de ``Session``, y verificacion de capabilities en cada
request via ``AuthorizationGuard``.

Materializa los UCs UC_AUTH_01..05 documentados en
:doc:`/arquitectura-tecnica/use-case-view/auth/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Auth — Session como entidad central + Guard
           runtime. Detalle de policies en :doc:`class`.

 @startuml

 package "MOD_Auth" {
   class Session <<entity>>
   class BlacklistedToken <<entity>>
   class AuthorizationGuard <<service>>
 }

 class User <<external>>
 class EffectivePermissionsAggregator <<external>>
 class AuditService <<external>>

 User "1" --> "0..*" Session : <<has>>
 BlacklistedToken --> Session : <<invalida>>

 AuthorizationGuard ..> Session : <<verify vigente>>
 AuthorizationGuard ..> EffectivePermissionsAggregator : <<resolve>>
 Session ..> AuditService : <<emite LOGIN/LOGOUT>>

 note bottom of Session
   Estado: ACTIVE / CLOSED.
   FSM canonica en :doc:`state`.
   Flujo JWT verify en :doc:`activity`.
 end note

 @enduml

Lectura del diagrama
====================

- **Entidad central:** ``Session`` representa la sesion
  vigente de un usuario. FSM ``ACTIVE → CLOSED`` (con
  ``close_reason``) en :doc:`state`.
- **AuthorizationGuard** es el gateway runtime: en cada
  request verifica que la sesion sigue vigente, que el
  refresh token no esta blacklisteado, y que el usuario
  tiene la capability requerida (delega al aggregator de
  permissions).
- **BlacklistedToken** invalida tokens de sesiones
  cerradas anticipadamente (logout, bloqueo administrativo,
  refresh revoke).
- Eventos de ``LOGIN_SUCCESS``, ``LOGIN_FAILED``,
  ``LOGOUT``, ``ACCOUNT_LOCKED`` se emiten al
  ``AuditService``.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/session` —
  Session entity.
- :doc:`/arquitectura-tecnica/domain-model/blacklisted-token`
  — BlacklistedToken.
- :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
  — AuthorizationGuard.
- :doc:`/arquitectura-tecnica/domain-model/expiration-policy`
  — ExpirationPolicy.
- :doc:`/arquitectura-tecnica/domain-model/idempotency-policy`
  — IdempotencyPolicy.
- :doc:`/arquitectura-tecnica/domain-model/password-generator`
  — PasswordGenerator (reset).
- :doc:`/arquitectura-tecnica/domain-model/user` — User.
- :doc:`/arquitectura-tecnica/domain-model/audit-service` —
  AuditService.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Auth

 class
 sequence
 state
 activity

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/auth/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/permissions/index` —
   resolver del effective_set invocado por el Guard.
 - :doc:`/arquitectura-tecnica/design-view/users/index` —
   modulo dueño de User.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.

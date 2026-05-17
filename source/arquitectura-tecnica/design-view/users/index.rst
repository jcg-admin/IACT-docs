.. meta::
 :artefacto: AT_DESIGN_MOD_USERS
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: users
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_users:

============================================================
Design View — MOD_Users: Vista de Diseño
============================================================

Caja del modulo **MOD_Users** (gestion de usuarios). Cubre
el ciclo de vida del User: creacion con onboarding,
modificacion administrativa, edicion self-service del
perfil propio, baja logica, bloqueo y desbloqueo.

Materializa los UCs UC_USR_01..07 documentados en
:doc:`/arquitectura-tecnica/use-case-view/users/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Users — entidad central User y servicios de
           ciclo de vida. Detalle interno en :doc:`bounded-context`.

 @startuml

 package "MOD_Users" {
   class User <<entity>>
   class UserOnboardingService <<service>>
 }

 class Assignment <<external>>
 class Session <<external>>
 class AuthorizationGuard <<external>>
 class AuditService <<external>>

 User "1" --> "0..*" Assignment : <<has>>
 User "1" --> "0..*" Session : <<has>>

 UserOnboardingService ..> User : <<crea>>
 AuthorizationGuard ..> User : <<verify>>
 User ..> AuditService : <<emite eventos lifecycle>>

 note bottom of User
   UserOnboardingService orquesta
   provisioning completo
   (UC_USR_01). UserRepo y
   PasswordGenerator en :doc:`bounded-context`.
 end note

 @enduml

Lectura del diagrama
====================

- **Entidad central:** ``User`` con su ciclo de vida
  (state: ACTIVE, INACTIVE, BLOCKED, ELIMINATED — diagrama
  canonico en uc-usr-04).
- ``UserOnboardingService`` (renombrado en WP-E desde
  ``UserFactory``) orquesta la creacion completa: alta,
  password inicial, primera asignacion AGR.
- ``Assignment`` y ``Session`` viven en otros modulos pero
  son las entidades a las que el User esta acoplado por
  cardinalidad.
- Cada cambio de estado (create, modify, deactivate, block,
  unblock) emite ``AuditEvent``.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/user` — User
  entity (atributos, state).
- :doc:`/arquitectura-tecnica/domain-model/user-repo` —
  UserRepo (CRUD + bajas logicas BR-009).
- :doc:`/arquitectura-tecnica/domain-model/user-capability-resolver` —
  UserCapabilityResolver.
- :doc:`/arquitectura-tecnica/domain-model/password-generator` —
  PasswordGenerator.
- :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
  AuthorizationGuard (consumidor externo).
- :doc:`/arquitectura-tecnica/domain-model/audit-service` —
  AuditService (consumidor externo).

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Users

 bounded-context
 interaction-pattern
 user-lifecycle

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/users/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/access/index` —
   modulo que crea Assignment.
 - :doc:`/arquitectura-tecnica/design-view/auth/index` —
   modulo que gestiona Session.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.

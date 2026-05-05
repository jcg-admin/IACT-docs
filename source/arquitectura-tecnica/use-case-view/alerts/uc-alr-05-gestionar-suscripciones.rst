.. meta::
 :artefacto: AT_UC_ALR_05_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_alr_05_gestionar_suscripciones:

==============================
UC_ALR_05 — Gestionar Suscripciones
==============================

User suscribe/unsubscribe a reglas de alertas para recibir
notificaciones via mailbox. ``manage_own_subscriptions`` (self) +
``subscribe_to_alert`` (admin gestiona suscripciones de otros). Tres
tipos: (a) rule_id especifico, (b) severity_filter, (c) scope_filter.

.. uml::
 :caption: UC_ALR_05 — actores y casos asociados.

 @startuml

 left to right direction

 actor "manage_own_subscriptions" as manage_own_subscriptions
 actor "subscribe_to_alert" as subscribe_to_alert
 actor "User destino" as User_destino <<beneficiario>>
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "Subscription" as Subscription <<sistema>>
 actor "AlertRule" as AlertRule <<sistema>>
 actor "SegmentResolver" as SegmentResolver <<sistema>>
 actor "InternalMailbox" as InternalMailbox <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_05\nGestionar Suscripciones" as UC_ALR_05
   usecase "Verificar funcion\n(self vs admin)" as VERIFICAR_AGR
   usecase "Validar tipo\n(rule | severity | scope)" as VALIDAR_TIPO
   usecase "Validar scope ⊆\nsegmentos del User (CNST-008)" as VALIDAR_SCOPE
   usecase "Validar regla existe\n+ ACTIVE" as VALIDAR_RULE
   usecase "Persistir Subscription" as PERSISTIR
   usecase "Notificar invitacion\nvia InternalMailbox" as NOTIFICAR
 }

 manage_own_subscriptions --> UC_ALR_05
 subscribe_to_alert --> UC_ALR_05

 UC_ALR_05 ..> VERIFICAR_AGR : <<include>>
 UC_ALR_05 ..> VALIDAR_TIPO : <<include>>
 UC_ALR_05 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_05 ..> VALIDAR_RULE : <<include>>
 UC_ALR_05 ..> PERSISTIR : <<include>>
 UC_ALR_05 ..> NOTIFICAR : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 VALIDAR_SCOPE --> SegmentResolver
 VALIDAR_RULE --> AlertRule
 PERSISTIR --> Subscription
 NOTIFICAR --> InternalMailbox
 InternalMailbox --> User_destino

 note bottom of UC_ALR_05
   Self: manage_own_subscriptions
   (auto-subscribe).
   Admin: subscribe_to_alert
   (subscribe a otros — onboarding).
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/subscription` —
   entidad persistida.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla referenciada.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon destino.
 - :doc:`/arquitectura-tecnica/domain-model/internal-message` —
   item de invitacion.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   CNST-008.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/alerts/uc-alr-05/index` —
   spec textual.

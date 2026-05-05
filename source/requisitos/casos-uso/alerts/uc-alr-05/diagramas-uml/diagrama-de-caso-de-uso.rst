8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_ALR_05 — actores y casos asociados

 @startuml

 left to right direction

 actor "manage_own_subscriptions" as F_OWN
 actor "subscribe_to_alert" as F_ADMIN
 actor "User destino" as TARGET <<beneficiario>>
 actor "Subscription" as S <<sistema>>
 actor "InternalMailbox" as MB <<sistema>>

 rectangle "MOD_Alerts" {
   usecase "UC_ALR_05\nGestionar\nSuscripciones" as UC_ALR_05
   usecase "Validar tipo\n(rule | severity | scope)" as VALIDAR_TIPO
   usecase "Validar scope ⊆\nsegmentos del User" as VALIDAR_SCOPE
   usecase "Persistir\nSubscription" as PERSISTIR
   usecase "Notificar\n(invitacion mailbox)" as NOTIFICAR
 }

 F_OWN --> UC_ALR_05
 F_ADMIN --> UC_ALR_05

 UC_ALR_05 ..> VALIDAR_TIPO : <<include>>
 UC_ALR_05 ..> VALIDAR_SCOPE : <<include>>
 UC_ALR_05 ..> PERSISTIR : <<include>>
 UC_ALR_05 ..> NOTIFICAR : <<include>>

 PERSISTIR --> S
 NOTIFICAR --> MB
 MB --> TARGET

 note bottom of UC_ALR_05
   Tipos: (a) rule_id especifica,
   (b) severity_filter, (c) scope_filter.
   manage_own_subscriptions = self-service.
   subscribe_to_alert = admin/onboarding
   gestiona suscripciones de otros.
 end note

 note bottom of NOTIFICAR
   CNST-001 NO email externo.
   CNST-002 mailbox interno.
   CNST-008 isolation por scope.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/subscription` —
   entidad Subscription persistida.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
   regla referenciada en subscription_type=rule.
 - :doc:`/arquitectura-tecnica/domain-model/internal-mailbox` —
   buzon donde se envia invitacion al subscriber.
 - :doc:`/arquitectura-tecnica/domain-model/segment-resolver` —
   resuelve scope segun segmentos del User (CNST-008).

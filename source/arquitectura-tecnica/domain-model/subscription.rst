.. meta::
 :artefacto: AT_DM_CLASS_SUBSCRIPTION
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_subscription:

============
Subscription
============

Suscripcion de un usuario a una alerta con filtro de severidad. Por
D-03 las operaciones de suscripcion se separan en tres funciones
RBAC distintas (subscribe / unsubscribe / configure_severity) para
permitir separacion de deberes.

.. uml::
 :caption: Clase Subscription — suscripcion de usuario a alerta.

 @startuml

 class Subscription {
   + subscription_id : UUID
   + alert_id : UUID
   + subscriber_user_id : UUID
   + scope : SubscriptionScope
   + channel : NotificationChannel
   + severity_filter : Severity
   + state : SubscriptionState
   --
   + subscribe()              <<subscribe_to_alert>>
   + unsubscribe()            <<unsubscribe_from_alert>>
   + configure_severity()     <<configure_subscription_severity>>
 }

 enum SubscriptionState {
   ACTIVE
   INACTIVE
 }

 Subscription "*" -- "1" SubscriptionState : has

 note right of Subscription
   D-03: tres operaciones separadas para separacion de deberes a nivel RBAC.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/alert`

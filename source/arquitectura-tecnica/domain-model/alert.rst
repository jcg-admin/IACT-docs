.. meta::
 :artefacto: AT_DM_CLASS_ALERT
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Alerts
 :estado: Vigente
 :version: 1.1.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_alert:

=====
Alert
=====

Alerta disparada cuando una metrica supera un ``Threshold``. El ciclo
de vida incluye la transicion ACTIVE → ACKNOWLEDGED (D-02: closed-loop
alerts). La transicion queda auditada (CNST-025).

.. uml::
 :caption: Clase Alert — alerta con ciclo de vida closed-loop.

 @startuml

 class Alert {
   + alert_id : UUID
   + threshold_id : UUID
   + triggered_at : DateTime
   + value : Double
   + state : AlertState
   + acknowledged_by : UUID
   + acknowledged_at : DateTime
   --
   + configure()         <<view_alerts>>
   + acknowledge()       <<acknowledge_alert>>
   + disable()           <<disable_alerts>>
 }

 enum AlertState {
   ACTIVE
   ACKNOWLEDGED
   DISABLED
 }

 class Threshold {
   + threshold_id : UUID
   + metric_id : UUID
   + value : Double
   + severity : Severity
 }

 class Subscription {
   + subscription_id : UUID
   + alert_id : UUID
   + state : SubscriptionState
 }

 Alert -- AlertState
 Alert "*" -- "1" Threshold
 Alert "1" -- "0..*" Subscription

 note right of Alert
   D-02: closed-loop alerts.
   CNST-025: transicion ACTIVE -> ACKNOWLEDGED auditada.
 end note

 note right of Subscription
   D-03: tres operaciones separadas
   (subscribe / unsubscribe / configure_severity)
   para SoD a nivel RBAC.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/domain-model/threshold`
 :doc:`/arquitectura-tecnica/domain-model/subscription`

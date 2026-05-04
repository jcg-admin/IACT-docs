.. meta::
 :artefacto: AT_DOMINIO_06_ALERTS
 :tipo: Diagrama Arquitectonico — Modelo de Dominio
 :dominio: arquitectura_tecnica
 :subdominio: BoundedContexts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dominio_iact_alerts:

==========================================
Modelo de Dominio — Bounded Context Alerts
==========================================

4.6 Alerts
----------

Tres clases: ``Alert``, ``Threshold`` y ``Subscription``. La
maquina de estados de ``Alert`` incluye la transicion
ACTIVE → ACKNOWLEDGED introducida por D-02 (closed-loop alerts).
Por D-03 las operaciones de suscripcion se separan en tres
funciones RBAC distintas para permitir SoD.

.. uml::
 :caption: Bounded context Alerts — alertas, umbrales y
           suscripciones.

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
   + configure()         <<ALR-001>>
   + acknowledge()       <<ALR-007>>
   + disable()           <<ALR-005 disable_alerts>>
 }

 class Threshold {
   + threshold_id : UUID
   + metric_id : UUID
   + comparison_operator : CompOp
   + value : Double
   + severity : Severity
   --
   + configure()         <<ALR-002 configure_thresholds>>
 }

 class Subscription {
   + subscription_id : UUID
   + alert_id : UUID
   + subscriber_user_id : UUID
   + severity_filter : Severity
   + state : SubscriptionState
   --
   + subscribe()              <<ALR-008>>
   + unsubscribe()            <<ALR-009>>
   + configure_severity()     <<ALR-010>>
 }

 enum AlertState {
   ACTIVE
   ACKNOWLEDGED
   DISABLED
 }

 enum CompOp {
   GT
   GE
   LT
   LE
   EQ
   NE
 }
 enum SubscriptionState {
   ACTIVE
   INACTIVE
 }

 Alert "*" -- "1" Threshold
 Alert "1" -- "0..*" Subscription
 Alert -- AlertState

 note right of Alert
   D-02: closed-loop alerts.
   La transicion ACTIVE -> ACKNOWLEDGED
   queda auditada (CNST-025).
 end note

 note right of Subscription
   D-03: tres operaciones separadas
   (subscribe / unsubscribe / configure_severity)
   para SoD a nivel RBAC.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/rbac/modelo-rbac-iact/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

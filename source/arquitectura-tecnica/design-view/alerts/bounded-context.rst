.. meta::
 :artefacto: AT_DESIGN_CLASS_ALERTS
 :tipo: Diagrama Arquitectonico — Design View — Class
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_class_alerts:

============================================================
Design View — MOD_Alerts: Estructura de Clases
============================================================

Modulo de **alertas operativas**: definicion de reglas de
alerta sobre metricas, evaluacion en runtime, notificacion via
hooks, gestion de suscripciones y ciclo de vida del Alert.

.. uml::
 :caption: MOD_Alerts — clases canonicas y relaciones internas.

 @startuml

 class Alert
 class AlertRule
 class AlertHook
 class Threshold
 class Metric
 class AlertRepo <<sistema>>
 class EvaluatorReloader <<sistema>>
 class AuthorizationGuard <<sistema>>
 class AuditService <<sistema>>

 AlertRule "1" -- "1..n" Threshold : umbrales
 AlertRule --> Metric : monitorea
 Alert --> AlertRule : disparo de
 AlertRule "1" -- "0..n" AlertHook : notifica via

 AlertRepo ..> Alert
 AlertRepo ..> AlertRule
 EvaluatorReloader ..> AlertRule : recarga config en runtime

 AuthorizationGuard ..> AlertRepo : verify_function

 Alert ..> AuditService : on raise/ack/resolve
 AlertRule ..> AuditService : on create/update

 @enduml

----

UCs cubiertos
==============

UC_ALR_01..05 — definir regla de alerta, ver alertas activas,
acknowledgear, ver historial, gestionar suscripciones. Ver
:doc:`/arquitectura-tecnica/use-case-view/alerts/index`.

----

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert`
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook`
 - :doc:`/arquitectura-tecnica/domain-model/threshold`
 - :doc:`/arquitectura-tecnica/domain-model/metric`
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`
 - :doc:`/arquitectura-tecnica/use-case-view/alerts/index`
 - :doc:`/arquitectura-tecnica/design-view/alerts/interaction-pattern`
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-event-lifecycle`

.. meta::
 :artefacto: AT_DESIGN_MOD_ALERTS
 :tipo: Diagrama Arquitectonico — Design View — Module Box
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: alerts
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-08
 :ultimo_cambio: 2026-05-08
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_alerts:

============================================================
Design View — MOD_Alerts: Vista de Diseño
============================================================

Caja del modulo **MOD_Alerts** (definicion, evaluacion y
notificacion de alertas sobre metricas). Cubre la
configuracion de ``AlertRule`` con thresholds, la evaluacion
periodica de las reglas contra ``Metric``, la generacion de
``Alert`` cuando se dispara, y las suscripciones de usuarios
a notificaciones.

Materializa los UCs UC_ALR_01..05 documentados en
:doc:`/arquitectura-tecnica/use-case-view/alerts/index`.

Vista panoramica del modulo
============================

.. uml::
 :caption: MOD_Alerts — AlertRule + Alert + Subscription.
           Detalle de Threshold, Hook, repos en :doc:`bounded-context`.

 @startuml

 package "MOD_Alerts" {
   class AlertRule <<entity>>
   class Alert <<entity>>
   class Subscription <<entity>>
   class EvaluatorReloader <<service>>
 }

 class Metric <<external>>
 class InternalMailbox <<external>>
 class AuditService <<external>>

 AlertRule ..> Metric : <<monitorea>>
 Alert --> AlertRule : <<disparo de>>
 Subscription --> AlertRule : <<suscribe a>>
 EvaluatorReloader ..> AlertRule : <<recarga reglas>>

 Alert ..> InternalMailbox : <<notifica>>
 AlertRule ..> AuditService : <<emite cambios>>

 note bottom of AlertRule
   FSM Alert (raised → ack →
   resolved) en :doc:`alert-event-lifecycle`.
   Flujo de evaluacion en
   :doc:`alert-evaluation-flow`.
 end note

 @enduml

Lectura del diagrama
====================

- **Tres entidades centrales:** ``AlertRule`` (definicion
  + thresholds), ``Alert`` (instancia disparada),
  ``Subscription`` (que usuarios reciben notificaciones).
- **EvaluatorReloader** recarga las reglas activas tras
  cualquier cambio (CRUD, enable/disable) sin reiniciar el
  servicio.
- **Notificacion** via ``InternalMailbox`` (el modulo no
  enviera emails — solo mensajeria interna; CNST-001).
- Cada cambio en reglas o suscripciones emite
  ``AuditEvent``.

Clases canonicas que materializan el modulo
============================================

- :doc:`/arquitectura-tecnica/domain-model/alert` — Alert
  (instancia disparada).
- :doc:`/arquitectura-tecnica/domain-model/alert-rule` —
  AlertRule (definicion).
- :doc:`/arquitectura-tecnica/domain-model/alert-rule-repo` —
  AlertRuleRepo.
- :doc:`/arquitectura-tecnica/domain-model/alert-repo` —
  AlertRepo.
- :doc:`/arquitectura-tecnica/domain-model/alert-hook` —
  AlertHook (canal de notificacion).
- :doc:`/arquitectura-tecnica/domain-model/threshold` —
  Threshold.
- :doc:`/arquitectura-tecnica/domain-model/subscription` —
  Subscription.
- :doc:`/arquitectura-tecnica/domain-model/subscription-repo` —
  SubscriptionRepo.
- :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader` —
  EvaluatorReloader.
- :doc:`/arquitectura-tecnica/domain-model/alert-history-service`
  — AlertHistoryService.

Sub-vistas del modulo
======================

.. toctree::
 :maxdepth: 1
 :caption: Diagramas del modulo MOD_Alerts

 bounded-context
 interaction-pattern
 alert-event-lifecycle
 alert-evaluation-flow

----

.. seealso::

 - :doc:`/arquitectura-tecnica/use-case-view/alerts/index`.
 - :doc:`/arquitectura-tecnica/design-view/index`.
 - :doc:`/arquitectura-tecnica/design-view/pipeline/index` —
   modulo emisor de Metric.
 - :doc:`/arquitectura-tecnica/design-view/package-overview`.

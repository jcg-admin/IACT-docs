.. meta::
 :artefacto: AT_DESIGN_SEQ_ALERTS
 :tipo: Diagrama Arquitectonico — Design View — Sequence
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :modulo: alerts
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_seq_alerts:

============================================================
Design View — MOD_Alerts: Patron de Interaccion
============================================================

Secuencia canonica del modulo MOD_Alerts: evaluacion en runtime
de una ``AlertRule`` contra una metrica reciente. Si excede
threshold, crea ``Alert`` y notifica via ``AlertHook``.

.. uml::
 :caption: MOD_Alerts — evaluacion de rule y notificacion.

 @startuml

 actor evaluator <<sistema>>
 actor "EvaluatorReloader" as EvaluatorReloader <<sistema>>
 actor "AlertRule" as AlertRule <<sistema>>
 actor "Threshold" as Threshold <<sistema>>
 actor "Metric" as Metric <<sistema>>
 actor "Alert" as Alert <<sistema>>
 actor "AlertRepo" as AlertRepo <<sistema>>
 actor "AlertHook" as AlertHook <<sistema>>
 actor "AuditService" as AuditService <<sistema>>

 evaluator -> EvaluatorReloader : get_active_rules()
 activate EvaluatorReloader
 EvaluatorReloader --> evaluator : List<AlertRule>
 deactivate EvaluatorReloader

 loop por cada AlertRule
   evaluator -> Metric : current_value(rule.metric_id)
   Metric --> evaluator : value

   evaluator -> AlertRule : get_threshold()
   AlertRule -> Threshold : configure_check(value)
   Threshold --> AlertRule : exceeded? severity

   alt threshold exceeded
     evaluator -> Alert : raise(rule, value, severity)
     activate Alert
     Alert -> AlertRepo : persist
     Alert --> evaluator : Alert
     deactivate Alert

     evaluator -> AlertHook : notify(alert)
     activate AlertHook
     AlertHook --> evaluator : OK
     deactivate AlertHook

     evaluator -> AuditService : emit(AuditEvent\ntype=alert_raised)
   end
 end

 note right of Threshold
   CompOp: GT, GE, LT, LE, EQ, NE.
   Severity: info, warning, critical.
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/alerts/bounded-context`
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-event-lifecycle`
 - :doc:`/arquitectura-tecnica/design-view/alerts/alert-evaluation-flow`
 - :doc:`/arquitectura-tecnica/use-case-view/alerts/index`
 - :doc:`/arquitectura-tecnica/domain-model/alert`
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`
 - :doc:`/arquitectura-tecnica/domain-model/alert-hook`
 - :doc:`/arquitectura-tecnica/domain-model/threshold`
 - :doc:`/arquitectura-tecnica/domain-model/metric`
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`

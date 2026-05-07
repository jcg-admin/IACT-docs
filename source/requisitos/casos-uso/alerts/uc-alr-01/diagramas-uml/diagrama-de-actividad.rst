.. _uc-alr-01-parte-08-diagrama-actividad:

8.2 Diagrama de actividad — Crear regla de alerta
==================================================

.. uml::
 :caption: UC_ALR_01 — flujo de creacion de AlertRule.

 @startuml

 start
 :Invoker emite POST /api/v1/alerts/rules/;
 :Servicio de Aplicacion verifica capability
   manage_alert_rules;
 if (Capability presente?) then (no)
   :403 Forbidden;
   stop
 endif

 :Validar metric, scope, condition;
 if (Cross-segmento detectado?) then (si)
   :400 cross-segment no permitido;
   stop
 endif
 if (Action invalido?) then (si)
   :400 action invalida;
   stop
 endif

 :BEGIN TRANSACTION;
 :Persistir AlertRule (state=active)
   en AlertRuleRepo;
 :Audit ALERT_RULE_CREATED;
 :COMMIT;

 :Notificar EvaluatorReloader.reload(rule_id);
 :201 Created con AlertRule;
 stop

 @enduml

.. seealso::

 - :doc:`diagrama-de-caso-de-uso`.
 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator`.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`.

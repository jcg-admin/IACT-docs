8.4 Clases
==========

.. uml::

 @startuml
 class AlertRule {
   id, name, metric, scope,
   condition, window, severity,
   actions, cooldown, status
 }
 class RuleValidator {
   validate(rule, user_segments)
 }
 class EvaluatorReloader {
   reload(rule_id)
 }
 AlertRule -- RuleValidator
 AlertRule -- EvaluatorReloader
 @enduml

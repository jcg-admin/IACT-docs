.. _uc-alr-01-parte-08-diagrama-clases:

8.4 Diagrama de clases
=======================

.. uml::
 :caption: UC_ALR_01 — clases involucradas en gestion de AlertRule.

 @startuml

 class AlertRule {
   + rule_id : UUID
   + name : String
   + metric : String
   + scope : String
   + condition : Expression
   + window : Duration
   + severity : Severity
   + actions : List
   + cooldown : Duration
   + status : AlertRuleState
 }

 class RuleValidator {
   + validate(rule, user_segments) : ValidationResult
 }

 class EvaluatorReloader {
   + reload_rule(rule_id) : void
 }

 class AlertRuleRepo {
   + create(rule) : AlertRule
   + update(rule) : AlertRule
   + by_id(id) : AlertRule
 }

 AlertRule "1" -- "1" RuleValidator : validates
 AlertRule "1" -- "1" EvaluatorReloader : triggers reload
 AlertRuleRepo "1" --> "*" AlertRule : manages

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/alert-rule`.
 - :doc:`/arquitectura-tecnica/domain-model/alert-repo`.
 - :doc:`/arquitectura-tecnica/domain-model/rule-validator`.
 - :doc:`/arquitectura-tecnica/domain-model/evaluator-reloader`.

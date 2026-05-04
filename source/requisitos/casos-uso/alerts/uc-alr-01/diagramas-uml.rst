.. _uc-alr-01-parte-08:

==========================
Parte 8 — Diagramas UML
==========================

8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "configure_team_alerts" as configure_team_alerts
 actor "AlertEvaluator" as Alertevaluator
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales" as UC01
   usecase "Test rule\n(dry-run)" as TestRule
   usecase "Reload" as Reload
 }
 configure_team_alerts --> UC01
 configure_team_alerts --> TestRule
 UC01 ..> Reload : <<include>>
 Reload --> Alertevaluator
 @enduml

8.2 Actividad
=============

.. uml::

 @startuml
 start
 :POST rule;
 :JWT + RBAC;
 :Validar metric, scope, condition;
 if (Cross-segmento?) then (si)
   :400; stop
 endif
 if (Action invalido?) then (si)
   :400; stop
 endif
 :INSERT;
 :Audit ALERT_RULE_CREATED;
 :Notificar reload;
 :201;
 stop
 @enduml

8.3 Estado de la regla
======================

.. uml::

 @startuml
 [*] --> active : crear
 active --> paused : pause
 paused --> active : resume
 active --> [*] : delete
 paused --> [*] : delete
 @enduml

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

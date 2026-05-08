8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "configure_team_alerts" as configure_team_alerts
 actor "AlertEvaluator" as Alertevaluator
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_01\nConfigurar Umbrales" as UC_ALR_01
   usecase "Test rule\n(dry-run)" as TestRule
   usecase "Reload" as Reload
 }
 configure_team_alerts --> UC_ALR_01
 configure_team_alerts --> TestRule
 UC_ALR_01 ..> Reload : <<include>>
 Reload --> Alertevaluator
 @enduml


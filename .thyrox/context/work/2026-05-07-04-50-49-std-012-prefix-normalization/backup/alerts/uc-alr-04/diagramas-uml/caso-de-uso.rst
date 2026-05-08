8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_alert_history" as view_alert_history
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_04\nHistorial" as UC_ALR_04
 }
 view_alert_history --> UC_ALR_04
 @enduml


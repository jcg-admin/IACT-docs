8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_alerts" as view_alerts
 rectangle "MOD_Alerts" {
   usecase "UC_ALR_02\nAlertas Activas" as UC_ALR_02
   usecase "UC_ALR_03\nAck inline" as UC_ALR_03
   usecase "Auto-refresh" as AutoRefresh
 }
 view_alerts --> UC_ALR_02
 UC_ALR_02 ..> AutoRefresh : <<extend>>
 UC_ALR_02 ..> UC_ALR_03 : <<extend>>
 @enduml


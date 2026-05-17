8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_technical_metrics" as view_technical_metrics
 rectangle "MOD_Logs" {
   usecase "UC_LOG_07\nMetricas" as UC_LOG_07
 }
 view_technical_metrics --> UC_LOG_07
 @enduml


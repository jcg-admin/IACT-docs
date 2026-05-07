8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_pipeline_logs" as view_pipeline_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nLogs ETL" as UC_LOG_02
   usecase "Filtrar\npor trimestre" as FiltrarTrimestre
   usecase "Filtrar\npor estado" as FiltrarEstado
 }
 view_pipeline_logs --> UC_LOG_02
 UC_LOG_02 ..> FiltrarTrimestre : <<extend>>
 UC_LOG_02 ..> FiltrarEstado : <<extend>>
 @enduml


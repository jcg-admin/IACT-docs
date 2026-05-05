8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_etl_logs" as view_etl_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nLogs ETL" as UC_LOG_02
   usecase "Filtrar\npor trimestre" as FiltrarTrimestre
   usecase "Filtrar\npor estado" as FiltrarEstado
 }
 view_etl_logs --> UC_LOG_02
 UC_LOG_02 ..> FiltrarTrimestre : <<extend>>
 UC_LOG_02 ..> FiltrarEstado : <<extend>>
 @enduml


8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_etl_logs" as view_etl_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nLogs ETL" as UC02
   usecase "Filtrar\npor trimestre" as FiltrarTrimestre
   usecase "Filtrar\npor estado" as FiltrarEstado
 }
 view_etl_logs --> UC02
 UC02 ..> FiltrarTrimestre : <<extend>>
 UC02 ..> FiltrarEstado : <<extend>>
 @enduml


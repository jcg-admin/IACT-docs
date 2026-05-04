8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "request_pipeline_retry" as request_pipeline_retry
 actor "ETLScheduler" as Etlscheduler
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_04\nReintentar ETL" as UC04
 }
 request_pipeline_retry --> UC04
 UC04 --> Etlscheduler
 @enduml


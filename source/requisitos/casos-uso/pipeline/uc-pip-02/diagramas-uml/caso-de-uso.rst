8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_pipeline_errors" as view_pipeline_errors
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_02\nErrores ETL" as UC02
   usecase "Filtrar por trimestre" as FiltrarPorTrimestre
   usecase "Filtrar por period" as FiltrarPorPeriod
 }
 view_pipeline_errors --> UC02
 UC02 ..> FiltrarPorTrimestre : <<extend>>
 UC02 ..> FiltrarPorPeriod : <<extend>>
 @enduml


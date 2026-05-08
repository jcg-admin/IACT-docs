8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_pipeline_status" as view_pipeline_status
 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nSupervisar ETL" as UC_PIP_01
   usecase "Ver errores ETL" as VerErroresEtl
 }
 view_pipeline_status --> UC_PIP_01
 UC_PIP_01 ..> VerErroresEtl : <<extend>>
 @enduml


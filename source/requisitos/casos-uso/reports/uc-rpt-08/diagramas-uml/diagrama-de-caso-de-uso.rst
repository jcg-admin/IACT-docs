8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_08 — listar programados

 @startuml
 left to right direction
 actor "view_reports" as view_reports

 rectangle "MOD_Reports" {
   usecase "UC_RPT_08\nList scheduled" as UC_RPT_08
   usecase "Detalle" as VistaDetalle
   usecase "Historico runs" as TABLA_ETL_RUNS
 }

 view_reports --> UC_RPT_08
 UC_RPT_08 ..> DET : <<extend>>
 UC_RPT_08 ..> TABLA_ETL_RUNS : <<extend>>
 @enduml


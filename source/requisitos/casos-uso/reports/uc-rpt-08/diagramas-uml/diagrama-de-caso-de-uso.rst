8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_08 — listar programados

 @startuml
 left to right direction
 actor "view_reports" as view_reports

 rectangle "MOD_Reports" {
   usecase "UC_RPT_08\nList scheduled" as UC08
   usecase "Detalle" as VistaDetalle
   usecase "Historico runs" as RUNS
 }

 view_reports --> UC08
 UC08 ..> DET : <<extend>>
 UC08 ..> RUNS : <<extend>>
 @enduml


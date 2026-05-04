8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_RPT_14\nReporte Campanas" as UC14
   usecase "Detalle" as DET
 }
 view_reports --> UC14
 UC14 ..> DET : <<extend>>
 @enduml


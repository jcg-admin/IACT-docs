8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as IncludeUC
   usecase "UC_RPT_15\nReporte Transferencias" as UC15
   usecase "Ver por segmento" as SegmentoCodigo
 }
 view_reports --> UC15
 UC15 ..> INC : <<include>>
 UC15 ..> SEG : <<extend>>
 @enduml


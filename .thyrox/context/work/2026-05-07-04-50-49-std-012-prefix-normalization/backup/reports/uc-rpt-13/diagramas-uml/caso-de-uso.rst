8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as IncludeUC
   usecase "UC_RPT_13\nReporte Abandono" as UC13
 }
 view_reports --> UC13
 UC13 ..> INC : <<include>>
 @enduml


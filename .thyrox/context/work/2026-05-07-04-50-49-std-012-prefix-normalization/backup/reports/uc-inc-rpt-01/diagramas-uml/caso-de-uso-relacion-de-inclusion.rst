8.1 Caso de uso — relacion de inclusion
========================================

.. uml::

 @startuml
 left to right direction
 actor "view_reports" as view_reports
 rectangle "MOD_Reports" {
   usecase "UC_RPT_NN\n(cualquier reporte)" as UC_RPT_GENERICO
   usecase "UC_INC_RPT_01\nResolver Segmento" as INC01
 }
 view_reports --> UC_RPT_GENERICO
 UC_RPT_GENERICO ..> INC01 : <<include>>
 @enduml


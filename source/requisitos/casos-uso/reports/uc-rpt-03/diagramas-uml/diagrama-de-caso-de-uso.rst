8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_03 — historicos

 @startuml
 left to right direction
 actor "view_reports" as view_reports

 rectangle "MOD_Reports" {
   usecase "UC_RPT_03\nHistoricos" as UC_RPT_03
   usecase "Filtros + grupos" as FiltrosGrupos
   usecase "Comparative" as Comparative
   usecase "Cache" as Cache
 }

 view_reports --> UC_RPT_03
 UC_RPT_03 ..> FiltrosGrupos : <<include>>
 UC_RPT_03 ..> Comparative : <<extend>>
 UC_RPT_03 ..> Cache : <<include>>
 @enduml


8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_03 — historicos

 @startuml
 left to right direction
 actor "view_reports" as view_reports

 rectangle "MOD_Reports" {
   usecase "UC_RPT_03\nHistoricos" as UC03
   usecase "Filtros + grupos" as FiltrosGrupos
   usecase "Comparative" as Comparative
   usecase "Cache" as Cache
 }

 view_reports --> UC03
 UC03 ..> FiltrosGrupos : <<include>>
 UC03 ..> Comparative : <<extend>>
 UC03 ..> Cache : <<include>>
 @enduml


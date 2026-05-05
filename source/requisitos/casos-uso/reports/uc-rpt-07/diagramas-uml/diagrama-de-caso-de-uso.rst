8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_07 — programar

 @startuml
 left to right direction
 actor "schedule_report" as schedule_report
 actor "Scheduler" as Scheduler

 rectangle "MOD_Reports" {
   usecase "UC_RPT_07\nProgramar" as UC07
   usecase "Crear/Update" as OPERACION_CRUD
   usecase "Auto execute" as AutoExecute
   usecase "UC_RPT_04\nExport" as ExportarDatos
 }

 schedule_report --> UC07
 UC07 ..> OPERACION_CRUD : <<include>>
 Scheduler ..> AutoExecute : <<include>>
 AutoExecute ..> EXP : <<include>>
 @enduml


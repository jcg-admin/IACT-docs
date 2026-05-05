8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_01 — dashboard

 @startuml
 left to right direction

 actor "view_reports" as view_reports
 actor "Frontend" as Frontend

 rectangle "MOD_Reports" {
   usecase "UC_INC_RPT_01\nResolver Segmento" as IncludeUC
   usecase "UC_RPT_01\nVer Dashboard IVR" as UC_RPT_01
   usecase "Auto-refresh" as ReferenciaExterna
 }

 view_reports --> Frontend
 Frontend --> UC_RPT_01
 UC_RPT_01 ..> INC : <<include>>
 UC_RPT_01 ..> REF : <<extend>>

 note bottom of UC_RPT_01
   Read-only Analytics (CNST-007).
   Sin auditoria por invocacion.
 end note

 @enduml


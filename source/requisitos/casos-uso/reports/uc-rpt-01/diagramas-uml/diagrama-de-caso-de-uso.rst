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
   usecase "UC_RPT_01\nVer Dashboard IVR" as UC01
   usecase "Auto-refresh" as ReferenciaExterna
 }

 view_reports --> Frontend
 Frontend --> UC01
 UC01 ..> INC : <<include>>
 UC01 ..> REF : <<extend>>

 note bottom of UC01
   Read-only Analytics (CNST-007).
   Sin auditoria por invocacion.
 end note

 @enduml


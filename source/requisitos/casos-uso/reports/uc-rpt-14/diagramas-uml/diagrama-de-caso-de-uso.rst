8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_14 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "CampaignReportService" as SVC <<sistema>>
 actor "CampaignStatRepo" as REPO <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_14\nReporte de Campanas" as UC_RPT_14
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Calcular Contacts\n(attempted / reached)" as METRIC_CONTACTS
   usecase "Calcular Conversion\n(objective met / reached)" as METRIC_CONV
   usecase "Calcular Calls/hora\n+ TMO de campana" as METRIC_THROUGHPUT
   usecase "Calcular Disposition mix\n(success / no-answer / ...)" as METRIC_DISP
 }

 INVOKER --> UC_RPT_14
 UC_RPT_14 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_14 ..> METRIC_CONTACTS : <<include>>
 UC_RPT_14 ..> METRIC_CONV : <<include>>
 UC_RPT_14 ..> METRIC_THROUGHPUT : <<include>>
 UC_RPT_14 ..> METRIC_DISP : <<include>>

 METRIC_CONTACTS --> SVC
 SVC --> REPO

 note bottom of UC_RPT_14
   BReq-001 + BReq-003. Comparar
   campanas inbound/outbound,
   identificar mas eficiente.
   CNST-007 read-only Analytics.
 end note

 @enduml

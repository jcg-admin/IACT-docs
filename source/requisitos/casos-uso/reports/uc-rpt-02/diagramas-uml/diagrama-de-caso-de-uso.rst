8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_02 — realtime

 @startuml
 left to right direction

 actor "view_kpis" as view_kpis
 actor "AnalyticsStream" as Analyticsstream

 rectangle "MOD_Reports" {
   usecase "UC_RPT_02\nRealtime Metrics" as UC_RPT_02
   usecase "Suscribir stream" as Subscripcion
   usecase "Throttle" as Throttle
   usecase "Heartbeat" as Heartbeat
 }

 view_kpis --> UC_RPT_02
 UC_RPT_02 ..> SUB : <<include>>
 UC_RPT_02 ..> Throttle : <<include>>
 UC_RPT_02 ..> Heartbeat : <<include>>
 SUB --> Analyticsstream

 note bottom
   Stream push via SSE / WS / poll.
   Reconnect via Last-Event-ID.
 end note

 @enduml


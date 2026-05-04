8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_02 — realtime

 @startuml
 left to right direction

 actor "view_kpis" as view_kpis
 actor "AnalyticsStream" as Analyticsstream

 rectangle "MOD_Reports" {
   usecase "UC_RPT_02\nRealtime Metrics" as UC02
   usecase "Suscribir stream" as Subscripcion
   usecase "Throttle" as Throttle
   usecase "Heartbeat" as Heartbeat
 }

 view_kpis --> UC02
 UC02 ..> SUB : <<include>>
 UC02 ..> Throttle : <<include>>
 UC02 ..> Heartbeat : <<include>>
 SUB --> Analyticsstream

 note bottom
   Stream push via SSE / WS / poll.
   Reconnect via Last-Event-ID.
 end note

 @enduml


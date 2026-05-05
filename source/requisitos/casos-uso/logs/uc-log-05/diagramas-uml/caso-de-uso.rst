8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_infrastructure_logs" as view_infrastructure_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nLogs Infraestructura" as UC_LOG_05
   usecase "Filtrar por\nhosts" as FiltrarHosts
   usecase "Filtrar por\nnivel severity" as FiltrarSeverity
   usecase "Tail SSE\n(streaming)" as TailSse
 }
 view_infrastructure_logs --> UC_LOG_05
 UC_LOG_05 ..> FiltrarHosts : <<extend>>
 UC_LOG_05 ..> FiltrarSeverity : <<extend>>
 UC_LOG_05 ..> TailSse : <<extend>>
 @enduml


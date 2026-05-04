8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_infrastructure_logs" as view_infrastructure_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nLogs Infraestructura" as UC05
   usecase "Filtrar por\nhosts" as FiltrarHosts
   usecase "Filtrar por\nnivel severity" as FiltrarSeverity
   usecase "Tail SSE\n(streaming)" as TailSse
 }
 view_infrastructure_logs --> UC05
 UC05 ..> FiltrarHosts : <<extend>>
 UC05 ..> FiltrarSeverity : <<extend>>
 UC05 ..> TailSse : <<extend>>
 @enduml


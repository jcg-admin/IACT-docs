8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "view_application_logs" as view_application_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nLogs Sistema" as UC_LOG_01
   usecase "Tail SSE" as TailSse
 }
 view_application_logs --> UC_LOG_01
 UC_LOG_01 ..> TailSse : <<extend>>
 @enduml


8.1 Caso de uso
===============

.. uml::

 @startuml
 left to right direction
 actor "search_logs" as search_logs
 rectangle "MOD_Logs" {
   usecase "UC_LOG_03\nBuscar Logs" as UC_LOG_03
 }
 search_logs --> UC_LOG_03
 @enduml


8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_05 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_infrastructure_logs" as INVOKER
 actor "InfraLogStore" as STORE <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_05\nVer Logs de\nInfraestructura" as UC_LOG_05
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Filtrar por host" as FILTRAR_HOST
   usecase "Devolver entries" as DEVOLVER
 }

 INVOKER --> UC_LOG_05
 UC_LOG_05 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_05 ..> FILTRAR_HOST : <<include>>
 UC_LOG_05 ..> DEVOLVER : <<include>>

 FILTRAR_HOST --> STORE
 DEVOLVER --> STORE

 note bottom of UC_LOG_05
   Fuente: agregadores de infra
   logs (node-exporter, fluent-bit,
   etc.). CNST-009.
 end note

 @enduml

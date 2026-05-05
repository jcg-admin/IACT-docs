8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_02 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_pipeline_logs" as INVOKER
 actor "LogStore" as STORE <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_02\nConsultar Logs\ndel Pipeline" as UC_LOG_02
   usecase "Validar period\n(default last_1h)" as VALIDAR_PERIOD
   usecase "Forzar service ∈\n{etl-runner,\netl-validator, ...}" as FORZAR_SERVICE
   usecase "Filtrar por\npipeline_id" as FILTRAR_PIP
   usecase "Devolver entries" as DEVOLVER
 }

 INVOKER --> UC_LOG_02
 UC_LOG_02 ..> VALIDAR_PERIOD : <<include>>
 UC_LOG_02 ..> FORZAR_SERVICE : <<include>>
 UC_LOG_02 ..> FILTRAR_PIP : <<include>>
 UC_LOG_02 ..> DEVOLVER : <<include>>

 FORZAR_SERVICE --> STORE
 FILTRAR_PIP --> STORE
 DEVOLVER --> STORE

 note bottom of UC_LOG_02
   Variante de UC_LOG_01 con scope
   ETL forzado. Funcion separada
   para granular: data engineers
   ven Pipeline logs sin acceder
   al sistema general.
 end note

 @enduml

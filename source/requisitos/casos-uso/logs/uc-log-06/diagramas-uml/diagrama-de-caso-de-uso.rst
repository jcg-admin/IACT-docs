8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_LOG_06 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_system_health" as INVOKER
 actor "HealthAggregator" as AGG <<sistema>>
 actor "Servicios HTTP/DB/Queue" as SERVICIOS <<sistema>>
 actor "AlertEvaluator" as ALERTAS <<sistema>>
 actor "PipelineExecutionRepo" as PIPELINE_REPO <<sistema>>

 rectangle "MOD_Logs" {
   usecase "UC_LOG_06\nVer Estado del Sistema" as UC_LOG_06
   usecase "Aggregar status\nde Servicios" as STATUS_SVC
   usecase "Aggregar status de\nDependencies (BD/cache/queue)" as STATUS_DEP
   usecase "Resumen Pipeline\n(UC_PIP_01 summary)" as STATUS_ETL
   usecase "Count Alertas\nactivas (UC_ALR_02)" as STATUS_ALR
   usecase "Calcular overall\n(green | yellow | red)" as OVERALL
 }

 INVOKER --> UC_LOG_06
 UC_LOG_06 ..> STATUS_SVC : <<include>>
 UC_LOG_06 ..> STATUS_DEP : <<include>>
 UC_LOG_06 ..> STATUS_ETL : <<include>>
 UC_LOG_06 ..> STATUS_ALR : <<include>>
 UC_LOG_06 ..> OVERALL : <<include>>

 STATUS_SVC --> SERVICIOS
 STATUS_SVC --> AGG
 STATUS_ETL --> PIPELINE_REPO
 STATUS_ALR --> ALERTAS

 note bottom of UC_LOG_06
   BReq-006. Single-pane-of-glass:
   agrega estado de servicios HTTP,
   dependencias, pipeline y alertas
   en un overall green|yellow|red.
 end note

 @enduml

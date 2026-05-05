8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_13 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "QueueReportService" as SVC <<sistema>>
 actor "QueueDailyStatRepo" as REPO <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_13\nReporte de Colas" as UC_RPT_13
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Calcular Calls\noffered / answered / abandoned" as METRIC_VOL
   usecase "Calcular ASA\n(Average Speed of Answer)" as METRIC_ASA
   usecase "Calcular SL %\n(within threshold)" as METRIC_SL
   usecase "Calcular Abandon rate\n+ Max wait + Queue depth peak" as METRIC_QUEUE
 }

 INVOKER --> UC_RPT_13
 UC_RPT_13 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_13 ..> METRIC_VOL : <<include>>
 UC_RPT_13 ..> METRIC_ASA : <<include>>
 UC_RPT_13 ..> METRIC_SL : <<include>>
 UC_RPT_13 ..> METRIC_QUEUE : <<include>>

 METRIC_VOL --> SVC
 METRIC_ASA --> SVC
 SVC --> REPO

 note bottom of UC_RPT_13
   BReq-001 + BReq-006. Detectar
   colas saturadas o con SL bajo.
   CNST-007 read-only Analytics.
 end note

 @enduml

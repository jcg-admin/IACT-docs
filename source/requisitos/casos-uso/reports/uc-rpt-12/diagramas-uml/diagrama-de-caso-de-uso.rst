8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_RPT_12 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_reports" as INVOKER
 actor "AgentReportService" as SVC <<sistema>>
 actor "AgentDailyStatRepo" as REPO <<sistema>>

 rectangle "MOD_Reports" {
   usecase "UC_RPT_12\nReporte de Agentes" as UC_RPT_12
   usecase "UC_INC_RPT_01\nResolver Segmento\n(included)" as UC_INC_RPT_01
   usecase "Calcular Calls /\nTMO / AHT" as METRIC_HANDLE
   usecase "Calcular Ocupacion\n(busy/total_time)" as METRIC_OCUP
   usecase "Calcular Adherence\n(scheduled vs actual)" as METRIC_ADH
   usecase "Calcular Holds\n(count + avg time)" as METRIC_HOLD
 }

 INVOKER --> UC_RPT_12
 UC_RPT_12 ..> UC_INC_RPT_01 : <<include>>
 UC_RPT_12 ..> METRIC_HANDLE : <<include>>
 UC_RPT_12 ..> METRIC_OCUP : <<include>>
 UC_RPT_12 ..> METRIC_ADH : <<include>>
 UC_RPT_12 ..> METRIC_HOLD : <<include>>

 METRIC_HANDLE --> SVC
 METRIC_OCUP --> SVC
 SVC --> REPO

 note bottom of UC_RPT_12
   BReq-001 + BReq-003. CNST-007
   read-only Analytics. Casos:
   revision semanal de KPIs,
   identificar gaps de capacitacion,
   balanceo de cargas.
 end note

 @enduml

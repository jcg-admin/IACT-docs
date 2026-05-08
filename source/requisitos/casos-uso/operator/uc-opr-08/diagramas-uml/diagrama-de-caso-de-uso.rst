8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_OPR_08 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_own_metrics" as INVOKER
 actor "AgentDailyStatRepo" as REPO <<sistema>>
 actor "KpiCalculator" as KPI <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nVer Propio Dashboard" as UC_OPR_08
   usecase "Calcular Calls handled\n+ TMO" as METRIC_CALLS
   usecase "Calcular Service Level\npersonal" as METRIC_SL
   usecase "Calcular Adherence" as METRIC_ADH
   usecase "Calcular Breaks" as METRIC_BREAKS
   usecase "Comparativo team\n(opt-in)" as RANKING <<extend>>
 }

 INVOKER --> UC_OPR_08
 UC_OPR_08 ..> METRIC_CALLS : <<include>>
 UC_OPR_08 ..> METRIC_SL : <<include>>
 UC_OPR_08 ..> METRIC_ADH : <<include>>
 UC_OPR_08 ..> METRIC_BREAKS : <<include>>
 RANKING ..> UC_OPR_08 : <<extend>>

 METRIC_CALLS --> REPO
 METRIC_SL --> KPI
 METRIC_ADH --> KPI
 METRIC_BREAKS --> REPO

 note bottom of UC_OPR_08
   BReq-001. Vista PROPIA — sin
   RBAC adicional al rol agente.
   Diferencia con UC_RPT_12
   (vista supervisor sobre todos
   los agentes).
 end note

 note bottom of RANKING
   Posicion en ranking del team
   es opt-in: el agente decide
   si participar en comparativos.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo` —
   repositorio de stats agregadas (datos del propio User).
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   componente de calculo de KPIs personales.
 - :doc:`/arquitectura-tecnica/domain-model/comparative` —
   componente de ranking team (opt-in).

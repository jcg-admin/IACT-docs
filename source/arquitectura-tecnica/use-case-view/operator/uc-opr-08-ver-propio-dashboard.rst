.. meta::
 :artefacto: AT_UC_OPR_08_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: operator
 :estado: Reservado
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_opr_08_ver_propio_dashboard:

============================================================
UC_OPR_08 — Ver Propio Dashboard
============================================================

Vista PROPIA del agente con KPIs (Calls handled, TMO, SL personal,
Adherence, Breaks, ranking team opt-in). Sin RBAC adicional al rol User.
Diferencia con UC_RPT_12 (vista supervisor sobre todos los agentes).

.. uml::
 :caption: UC_OPR_08 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_own_metrics" as view_own_metrics
 actor "AgentDailyStatRepo" as AgentDailyStatRepo <<sistema>>
 actor "KpiCalculator" as KpiCalculator <<sistema>>
 actor "Comparative" as Comparative <<sistema>>
 actor "MetricsCache" as MetricsCache <<sistema>>

 rectangle "MOD_Operator" {
   usecase "UC_OPR_08\nVer Propio Dashboard\n.. extension points ..\nRankingTeam" as UC_OPR_08
   usecase "Calcular Calls handled\n+ TMO" as METRIC_CALLS
   usecase "Calcular Service Level\npersonal" as METRIC_SL
   usecase "Calcular Adherence" as METRIC_ADH
   usecase "Calcular Breaks" as METRIC_BREAKS
   usecase "Comparativo team\n(opt-in)" as RANKING
 }

 view_own_metrics --> UC_OPR_08

 UC_OPR_08 ..> METRIC_CALLS : <<include>>
 UC_OPR_08 ..> METRIC_SL : <<include>>
 UC_OPR_08 ..> METRIC_ADH : <<include>>
 UC_OPR_08 ..> METRIC_BREAKS : <<include>>
 RANKING ..> UC_OPR_08 : <<extend>> (RankingTeam)

 METRIC_CALLS --> AgentDailyStatRepo
 METRIC_SL --> KpiCalculator
 METRIC_ADH --> KpiCalculator
 METRIC_BREAKS --> AgentDailyStatRepo
 METRIC_CALLS --> MetricsCache
 RANKING --> Comparative

 note bottom of UC_OPR_08
   Vista PROPIA — sin RBAC adicional
   al rol User. Diferencia con
   UC_RPT_12 (vista supervisor).
 end note

 note bottom of RANKING
   Opt-in: el agente decide
   si participar en comparativos.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo` —
   stats agregadas del propio User.
 - :doc:`/arquitectura-tecnica/domain-model/kpi-calculator` —
   calculo de KPIs.
 - :doc:`/arquitectura-tecnica/domain-model/comparative` —
   ranking team (opt-in).
 - :doc:`/arquitectura-tecnica/domain-model/metrics-cache` —
   cache TTL adaptativo.
 - :doc:`/requisitos/casos-uso/operator/uc-opr-08/index` —
   spec textual.

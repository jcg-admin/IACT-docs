8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PIP_03 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_data_availability" as INVOKER
 actor "PipelineExecution" as PE <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_03\nConsultar Disponibilidad\nde Datos" as UC_PIP_03
   usecase "Calcular timestamp\nultimo refresh por dataset" as ULTIMO_REFRESH
   usecase "Listar datasets\n(CallSummary, AgentDailyStat,\nQueueDailyStat, ...)" as LIST_DATASETS
   usecase "Marcar staleness\nthreshold (verde/rojo)" as STALENESS
 }

 INVOKER --> UC_PIP_03
 UC_PIP_03 ..> LIST_DATASETS : <<include>>
 UC_PIP_03 ..> ULTIMO_REFRESH : <<include>>
 UC_PIP_03 ..> STALENESS : <<include>>

 ULTIMO_REFRESH --> PE
 LIST_DATASETS --> PE

 note bottom of UC_PIP_03
   CNST-007 read-only Analytics +
   pipeline metadata. Util para
   usuarios de reportes que verifican
   disponibilidad antes de query.
 end note

 note bottom of STALENESS
   Threshold por dataset: 24h por
   default. Configurable en
   futuro (out of scope).
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   PipelineExecution (ultimo run exitoso por dataset).
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo` —
   AgentDailyStat (consumido por UC_RPT_12).
 - :doc:`/arquitectura-tecnica/domain-model/system-health` —
   estado agregado consumido por UC_LOG_06.

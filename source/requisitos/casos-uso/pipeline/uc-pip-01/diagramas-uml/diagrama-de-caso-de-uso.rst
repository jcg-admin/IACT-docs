8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PIP_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_pipeline_status" as INVOKER
 actor "PipelineExecution" as PE <<sistema>>
 actor "TimingCalculator" as TC <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nSupervisar Pipeline" as UC_PIP_01
   usecase "Calcular jobs\nrunning/completed/failed" as METRICA_JOBS
   usecase "Calcular lag\npor source" as METRICA_LAG
   usecase "Calcular throughput\n(rows/min)" as METRICA_TP
   usecase "Calcular latency\npromedio" as METRICA_LAT
   usecase "Auto-refresh\ndashboard" as REFRESH <<extend>>
 }

 INVOKER --> UC_PIP_01
 UC_PIP_01 ..> METRICA_JOBS : <<include>>
 UC_PIP_01 ..> METRICA_LAG : <<include>>
 UC_PIP_01 ..> METRICA_TP : <<include>>
 UC_PIP_01 ..> METRICA_LAT : <<include>>
 REFRESH ..> UC_PIP_01 : <<extend>>

 METRICA_JOBS --> PE
 METRICA_LAG --> PE
 METRICA_TP --> PE
 METRICA_LAT --> TC
 METRICA_LAT --> PE

 note bottom of UC_PIP_01
   CNST-007 read-only Analytics +
   pipeline metadata. CNST-009
   fechas relativas. Sin auditoria
   por invocacion.
 end note

 note right of PE
   PipelineExecution: registro
   de ejecuciones del Servicio ETL.
   Datos calculados sobre estado real
   de la tabla pipeline_runs.
 end note

 @enduml

.. seealso::

 Modelo del dominio relevante para este UC:

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   entidad PipelineExecution (registro de ejecuciones).
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   log de eventos del pipeline (consumido en lag/throughput).
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   componente que calcula metricas de latencia.
 - :doc:`/arquitectura-tecnica/domain-model/system-health` —
   agregador de salud (consumido por UC_LOG_06).

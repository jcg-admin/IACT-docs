8.1 Diagrama de caso de uso
===========================

.. uml::
 :caption: UC_PIP_01 — actores y casos asociados

 @startuml

 left to right direction

 actor "view_pipeline_status" as INVOKER
 actor "PipelineExecutionRepo" as REPO <<sistema>>

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

 METRICA_JOBS --> REPO
 METRICA_LAG --> REPO
 METRICA_TP --> REPO
 METRICA_LAT --> REPO

 note bottom of UC_PIP_01
   CNST-007 read-only Analytics +
   ETL metadata. CNST-009 fechas
   relativas. Sin auditoria por
   invocacion.
 end note

 note right of REPO
   PipelineExecutionRepo: registro
   de ejecuciones del Servicio ETL.
   Datos calculados sobre estado real
   de la tabla pipeline_runs.
 end note

 @enduml

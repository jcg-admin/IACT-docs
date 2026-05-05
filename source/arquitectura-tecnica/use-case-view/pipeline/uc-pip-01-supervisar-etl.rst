.. meta::
 :artefacto: AT_UC_PIP_01_USECASE
 :tipo: Diagrama Arquitectonico — Use Case View — uml-07 standalone
 :dominio: arquitectura_tecnica
 :subdominio: UseCaseView
 :modulo: pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-05
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_uc_pip_01_supervisar_etl:

==============================
UC_PIP_01 — Supervisar Pipeline
==============================

Dashboard de salud del Pipeline (Servicio ETL): jobs running/completed/
failed, lag por source, throughput rows/min, latencia. CNST-007
read-only Analytics + pipeline metadata. ``view_pipeline_status``
(rename CNST-033 §8.2 desde view_etl_supervision).

.. uml::
 :caption: UC_PIP_01 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_pipeline_status" as view_pipeline_status
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PipelineExecution" as PipelineExecution <<sistema>>
 actor "PipelineExecutionRepo" as PipelineExecutionRepo <<sistema>>
 actor "TimingCalculator" as TimingCalculator <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_01\nSupervisar Pipeline" as UC_PIP_01
   usecase "Verificar\nview_pipeline_status" as VERIFICAR_AGR
   usecase "Calcular jobs\nrunning/completed/failed" as METRICA_JOBS
   usecase "Calcular lag\npor source" as METRICA_LAG
   usecase "Calcular throughput\n(rows/min)" as METRICA_TP
   usecase "Calcular latency\npromedio" as METRICA_LAT
   usecase "Auto-refresh dashboard" as REFRESH
 }

 view_pipeline_status --> UC_PIP_01

 UC_PIP_01 ..> VERIFICAR_AGR : <<include>>
 UC_PIP_01 ..> METRICA_JOBS : <<include>>
 UC_PIP_01 ..> METRICA_LAG : <<include>>
 UC_PIP_01 ..> METRICA_TP : <<include>>
 UC_PIP_01 ..> METRICA_LAT : <<include>>
 REFRESH ..> UC_PIP_01 : <<extend>>

 VERIFICAR_AGR --> AuthorizationGuard
 METRICA_JOBS --> PipelineExecutionRepo
 METRICA_LAG --> PipelineExecution
 METRICA_LAT --> TimingCalculator

 note bottom of UC_PIP_01
   CNST-007 read-only Analytics +
   pipeline metadata. CNST-009
   fechas relativas. Sin auditoria
   por invocacion.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   registro de ejecuciones.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo` —
   repositorio + queries.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-log` —
   logs operacionales.
 - :doc:`/arquitectura-tecnica/domain-model/timing-calculator` —
   metricas latencia.
 - :doc:`/arquitectura-tecnica/domain-model/system-health` —
   agregador (UC_LOG_06).
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index` —
   spec textual.

.. meta::
 :artefacto: AT_UC_PIP_03_USECASE
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

.. _at_uc_pip_03_consultar_disponibilidad_de_datos:

==================================================
UC_PIP_03 — Consultar Disponibilidad de Datos
==================================================

Muestra timestamp del ultimo refresh exitoso por dataset (CallSummary,
AgentDailyStat, QueueDailyStat, ...). Util para usuarios de reportes
que verifican disponibilidad antes de query. ``view_data_availability``.
Marca staleness verde/rojo (threshold default 24h).

.. uml::
 :caption: UC_PIP_03 — actores y casos asociados.

 @startuml

 left to right direction

 actor "view_data_availability" as view_data_availability
 actor "AuthorizationGuard" as AuthorizationGuard <<sistema>>
 actor "PipelineExecution" as PipelineExecution <<sistema>>
 actor "PipelineExecutionRepo" as PipelineExecutionRepo <<sistema>>

 rectangle "MOD_Pipeline" {
   usecase "UC_PIP_03\nConsultar Disponibilidad\nde Datos" as UC_PIP_03
   usecase "Verificar\nview_data_availability" as VERIFICAR_AGR
   usecase "Listar datasets\n(CallSummary, AgentDailyStat,\nQueueDailyStat, ...)" as LIST_DATASETS
   usecase "Calcular timestamp\nultimo refresh por dataset" as ULTIMO_REFRESH
   usecase "Marcar staleness\nthreshold (verde/rojo)" as STALENESS
 }

 view_data_availability --> UC_PIP_03

 UC_PIP_03 ..> VERIFICAR_AGR : <<include>>
 UC_PIP_03 ..> LIST_DATASETS : <<include>>
 UC_PIP_03 ..> ULTIMO_REFRESH : <<include>>
 UC_PIP_03 ..> STALENESS : <<include>>

 VERIFICAR_AGR --> AuthorizationGuard
 LIST_DATASETS --> PipelineExecutionRepo
 ULTIMO_REFRESH --> PipelineExecution

 note bottom of STALENESS
   Threshold default 24h.
   StaleDatasetSpec aplicada.
   Configurable por dataset en futuro.
 end note

 @enduml

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution` —
   ultimo run por dataset.
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo` —
   last_successful_by_dataset.
 - :doc:`/arquitectura-tecnica/domain-model/agent-daily-stat-repo` —
   AgentDailyStat (consumidor).
 - :doc:`/arquitectura-tecnica/domain-model/specification-pattern` —
   StaleDatasetSpec.
 - :doc:`/arquitectura-tecnica/domain-model/system-health` —
   estado agregado.
 - :doc:`/arquitectura-tecnica/domain-model/authorization-guard` —
   verifica.
 - :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/index` —
   spec textual.

.. meta::
 :artefacto: AT_DESIGN_STATE_PIPELINE_EXECUTION
 :tipo: Diagrama Arquitectonico — Design View — State Machine
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :entidad: PipelineExecution
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-06
 :ultimo_cambio: 2026-05-06
 :autor: NestorMonroy
 :clasificacion: Importante

.. _at_design_state_pipeline_execution:

============================================================
Design View — Ciclo de Vida: PipelineExecution
============================================================

Maquina de estados de la entidad ``PipelineExecution``. Cubre
el ciclo de un job ETL desde scheduled hasta completed/failed
incluyendo cancelacion manual.

.. uml::
 :caption: PipelineExecution FSM — running -> completed | failed | cancelled.

 @startuml

 [*] --> scheduled : Scheduler.create()
 scheduled --> running : Scheduler.dispatch()
 scheduled --> cancelled : User.cancel()

 state running {
   [*] --> extracting
   extracting --> transforming : extract_done
   transforming --> loading : transform_done
   loading --> [*] : load_done
 }

 running --> completed : ok
 running --> completed_with_errors : errors_count > 0\n&& errors_count < threshold
 running --> failed : fatal_error
 running --> cancelled : User.cancel()

 completed --> [*]
 completed_with_errors --> [*]
 failed --> [*]
 cancelled --> [*]

 note right of running
   Estados internos:
   extract -> transform -> load.
   Cada uno actualiza MetricsCache
   incrementalmente.
 end note

 note right of completed_with_errors
   Job termino pero algunos batches
   no pasaron validacion. Errores
   acumulados en errors[].
 end note

 @enduml

----

.. seealso::

 - :doc:`/arquitectura-tecnica/design-view/seq-pipeline`
 - :doc:`/arquitectura-tecnica/design-view/act-etl-pipeline-execution`
 - :doc:`/arquitectura-tecnica/design-view/class-pipeline`
 - :doc:`/arquitectura-tecnica/use-case-view/pipeline/index`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`

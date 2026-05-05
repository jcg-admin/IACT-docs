.. meta::
 :artefacto: AT_DESIGN_MOD_ETL_MONITORING
 :tipo: Diagrama Arquitectonico — Design View
 :dominio: arquitectura_tecnica
 :subdominio: DesignView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _at_design_mod_etl_monitoring:

=====================================================
Design View — MOD_Pipeline: Supervision ETL
=====================================================

Patron de interaccion del modulo de supervision ETL. Muestra la
consulta de ``PipelineExecution`` con evaluacion de estado mediante
``is_successful()`` / ``is_failed()``, y el reintento de una ejecucion
fallida con registro de ``AuditEvent(ETL_RETRY)``.

.. uml::
 :caption: Design View MOD_Pipeline — supervision y reintento de pipeline ETL.

 @startuml

 actor AGR_ADMIN

 participant InterfazPipeline        <<frontend>>
 participant ServicioETL             <<api>>
 participant RepositorioPipelineExecution <<repository>>
 database    AlmacenDatos            <<postgresql>>

 AGR_ADMIN -> InterfazPipeline : GET /pipeline/executions
 activate InterfazPipeline

 InterfazPipeline -> ServicioETL : listarEjecuciones()
 activate ServicioETL

 ServicioETL -> RepositorioPipelineExecution : findAll()
 activate RepositorioPipelineExecution
 RepositorioPipelineExecution -> AlmacenDatos : SELECT * FROM pipeline_runs\nORDER BY started_at DESC
 AlmacenDatos --> RepositorioPipelineExecution : List<PipelineExecution>
 RepositorioPipelineExecution --> ServicioETL : ejecuciones
 deactivate RepositorioPipelineExecution

 loop por cada PipelineExecution
   ServicioETL -> ServicioETL : ejecucion.is_successful()\n| ejecucion.is_failed()
 end

 ServicioETL --> InterfazPipeline : ejecuciones con estado evaluado
 deactivate ServicioETL
 InterfazPipeline --> AGR_ADMIN : tabla de ejecuciones
 deactivate InterfazPipeline

 AGR_ADMIN -> InterfazPipeline : POST /pipeline/executions/{id}/retry
 activate InterfazPipeline

 InterfazPipeline -> ServicioETL : reintentarEjecucion(id)
 activate ServicioETL

 ServicioETL -> RepositorioPipelineExecution : buscar(id)
 activate RepositorioPipelineExecution
 RepositorioPipelineExecution -> AlmacenDatos : SELECT pipeline_runs WHERE id=?
 AlmacenDatos --> RepositorioPipelineExecution : PipelineExecution{estado:fallido}
 RepositorioPipelineExecution --> ServicioETL : PipelineExecution
 deactivate RepositorioPipelineExecution

 ServicioETL -> AlmacenDatos : INSERT pipeline_runs{\n  source_table,\n  estado:IN_PROGRESS,\n  executed_by\n}
 AlmacenDatos --> ServicioETL : nueva PipelineExecution

 ServicioETL -> AlmacenDatos : INSERT audit_events\n{event_type:ETL_RETRY,\n details:{original_id}}
 AlmacenDatos --> ServicioETL : AuditEvent registrado

 ServicioETL --> InterfazPipeline : 202 Accepted {nuevo_id}
 deactivate ServicioETL
 InterfazPipeline --> AGR_ADMIN : reintento iniciado
 deactivate InterfazPipeline

 note right of AlmacenDatos
   CNST-007: tbl_historico_* solo lectura.
   CNST-008: ventana ETL 6-12 horas.
 end note

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`

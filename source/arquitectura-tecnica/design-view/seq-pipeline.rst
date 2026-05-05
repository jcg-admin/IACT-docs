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
consulta de ``ETLEjecucion`` con evaluacion de estado mediante
``es_exitosa()`` / ``es_fallida()``, y el reintento de una ejecucion
fallida con registro de ``AuditEvent(ETL_RETRY)``.

.. uml::
 :caption: Design View MOD_Pipeline — supervision y reintento de pipeline ETL.

 @startuml

 actor AGR_ADMIN

 participant InterfazPipeline        <<frontend>>
 participant ServicioETL             <<api>>
 participant RepositorioETLEjecucion <<repository>>
 database    AlmacenDatos            <<postgresql>>

 AGR_ADMIN -> InterfazPipeline : GET /pipeline/executions
 activate InterfazPipeline

 InterfazPipeline -> ServicioETL : listarEjecuciones()
 activate ServicioETL

 ServicioETL -> RepositorioETLEjecucion : findAll()
 activate RepositorioETLEjecucion
 RepositorioETLEjecucion -> AlmacenDatos : SELECT * FROM etl_runs\nORDER BY iniciado_en DESC
 AlmacenDatos --> RepositorioETLEjecucion : List<ETLEjecucion>
 RepositorioETLEjecucion --> ServicioETL : ejecuciones
 deactivate RepositorioETLEjecucion

 loop por cada ETLEjecucion
   ServicioETL -> ServicioETL : ejecucion.es_exitosa()\n| ejecucion.es_fallida()
 end

 ServicioETL --> InterfazPipeline : ejecuciones con estado evaluado
 deactivate ServicioETL
 InterfazPipeline --> AGR_ADMIN : tabla de ejecuciones
 deactivate InterfazPipeline

 AGR_ADMIN -> InterfazPipeline : POST /pipeline/executions/{id}/retry
 activate InterfazPipeline

 InterfazPipeline -> ServicioETL : reintentarEjecucion(id)
 activate ServicioETL

 ServicioETL -> RepositorioETLEjecucion : buscar(id)
 activate RepositorioETLEjecucion
 RepositorioETLEjecucion -> AlmacenDatos : SELECT etl_runs WHERE id=?
 AlmacenDatos --> RepositorioETLEjecucion : ETLEjecucion{estado:fallido}
 RepositorioETLEjecucion --> ServicioETL : ETLEjecucion
 deactivate RepositorioETLEjecucion

 ServicioETL -> AlmacenDatos : INSERT etl_runs{\n  tabla_origen,\n  estado:en_ejecucion,\n  ejecutado_por\n}
 AlmacenDatos --> ServicioETL : nueva ETLEjecucion

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
 :doc:`/arquitectura-tecnica/domain-model/etl-ejecucion`
 :doc:`/arquitectura-tecnica/domain-model/audit-event`

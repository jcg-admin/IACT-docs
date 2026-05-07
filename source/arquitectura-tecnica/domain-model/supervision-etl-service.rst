.. meta::
 :artefacto: AT_DM_CLASS_SUPERVISION_ETL_SERVICE
 :tipo: Diagrama Arquitectonico — Domain Model — Clase
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :bounded_context: Pipeline
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-07
 :ultimo_cambio: 2026-05-07
 :autor: NestorMonroy
 :clasificacion: Critico

.. _dm_class_supervision_etl_service:

======================
SupervisionETLService
======================

Servicio de aplicacion principal del pipeline ETL de
supervision. Coordina los componentes del bounded context
Pipeline para responder a dos casos de uso clave:

1. **Supervisar** (``uc-pip-01``) — devolver el
   ``ResumenSalud`` actual del pipeline.
2. **Reintento manual** (``uc-pip-04``) — invocar el
   ``DisparadorETL`` para reprocesar un rango.

Es el punto de entrada unico del bounded context Pipeline
para invocadores externos (UI, API). Internamente delega a
``ResumenSaludBuilder``, ``DisparadorETL``, y
``ErroresETLService``.

.. uml::
 :caption: SupervisionETLService — punto de entrada del
           BC Pipeline. Delega en builder, disparador y
           servicio de errores.

 @startuml

 class SupervisionETLService {
   - pipeline_repo : PipelineExecutionRepo
   - errores_service : ErroresETLService
   - builder : ResumenSaludBuilder
   - disparador : DisparadorETL
   --
   + supervisar(actor_user_id : UUID) : ResumenSalud
   + invocar_reproceso(actor_user_id : UUID, \
                        scope : ETLScope) : ETLRunId
   + estado_run(run_id : UUID) : RunStatus
 }

 class PipelineExecutionRepo
 class ErroresETLService
 class ResumenSaludBuilder
 class DisparadorETL
 class ResumenSalud
 class ETLScope
 class ETLRunId
 class RunStatus

 SupervisionETLService --> PipelineExecutionRepo : reads
 SupervisionETLService --> ErroresETLService : reads
 SupervisionETLService --> ResumenSaludBuilder : delegates
 SupervisionETLService --> DisparadorETL : invokes
 SupervisionETLService ..> ResumenSalud : returns

 @enduml

Operaciones principales
=======================

- ``supervisar(actor)`` — pipeline:

  1. Lee runs recientes via ``PipelineExecutionRepo``.
  2. Lee errores recientes via ``ErroresETLService``.
  3. Delega ensamble a ``ResumenSaludBuilder``.
  4. Devuelve ``ResumenSalud`` inmutable.

- ``invocar_reproceso(actor, scope)`` — pipeline:

  1. Verifica capability ``manage_pipeline`` del actor.
  2. Verifica que no haya run en ejecucion (``state=RUNNING``).
  3. Registra entry manual en ``PipelineExecutionRepo``.
  4. Invoca ``DisparadorETL.invocar_reproceso``.
  5. Audita ``ETL_REINTENTO_SOLICITADO``.
  6. Devuelve ``etl_run_id`` para tracking.

- ``estado_run(run_id)`` — devuelve el ``RunStatus`` actual.

Restricciones aplicables
========================

- **CNST-025** — operaciones de mutacion (``invocar_reproceso``)
  se auditan.
- **BR-pipeline-overlap** — no se permite reintento si ya
  hay un run activo.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index` —
  ``supervisar``.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  ``invocar_reproceso``.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/index` —
  consulta de errores via ``ErroresETLService``.

Relaciones
==========

- Punto de entrada unico del BC Pipeline.
- Lee de ``PipelineExecutionRepo`` y ``ErroresETLService``.
- Delega ensamble a ``ResumenSaludBuilder``.
- Invoca ``DisparadorETL`` para reprocesos.
- Emite via ``AuditService``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/resumen-salud`
 - :doc:`/arquitectura-tecnica/domain-model/resumen-salud-builder`
 - :doc:`/arquitectura-tecnica/domain-model/disparador-etl`
 - :doc:`/arquitectura-tecnica/domain-model/errores-etl-service`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution-repo`

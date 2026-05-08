.. meta::
 :artefacto: AT_DM_CLASS_ERRORES_ETL_SERVICE
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

.. _dm_class_errores_etl_service:

==================
ErroresETLService
==================

Servicio de aplicacion que captura, persiste y consulta
errores ocurridos durante runs ETL del pipeline de
supervision. Aplica vocabulario STD-010 — el termino
canonico es "Errores ETL" en lugar del tecnico
"ETL Errors".

Provee dos perfiles de uso:

1. **Captura** — invocado desde el ``Procesador Asincrono``
   (worker ETL) cuando un step falla; persiste el detalle
   del error con el ``run_id`` asociado.
2. **Consulta** — invocado desde ``uc-pip-02`` por usuarios
   con codename ``view_pipeline`` para investigar fallos.

.. uml::
 :caption: ErroresETLService — captura y consulta de
           errores ETL.

 @startuml

 class ErroresETLService {
   --
   + record(run_id : UUID, \
            step : String, \
            error : ErrorDetail) : void
   + query(filters : ETLErrorFilters, \
            period : DateRange) : List<ETLError>
   + summary(period : DateRange) : ETLErrorSummary
 }

 class ETLError {
   + id : UUID
   + run_id : UUID
   + step : String
   + level : ErrorLevel
   + message : String
   + traceback : String
   + occurred_at : DateTime
 }

 class ETLErrorSummary {
   + total : Integer
   + by_step : Map<String, Integer>
   + by_level : Map<ErrorLevel, Integer>
 }

 class ETLErrorFilters
 class ErrorLevel

 ErroresETLService ..> ETLError : produces
 ErroresETLService ..> ETLErrorSummary : produces
 ErroresETLService ..> ETLErrorFilters : queries with

 @enduml

Operaciones principales
=======================

- ``record(run_id, step, error)`` — persiste un error con
  contexto del run.
- ``query(filters, period)`` — devuelve errores filtrados.
- ``summary(period)`` — agregaciones para dashboard.

Restricciones aplicables
========================

- **CNST-025** — la consulta de errores ETL se audita.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-02/index` —
  consulta de errores ETL.
- :doc:`/requisitos/casos-uso/pipeline/uc-pip-04/index` —
  reintento ETL incluye consulta del ultimo error.

Relaciones
==========

- Es invocado por ``Procesador Asincrono`` (worker ETL)
  para capturar errores.
- Es leido por ``SupervisionETLService`` para componer el
  ``ResumenSalud`` del pipeline.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 - :doc:`/arquitectura-tecnica/domain-model/audit-service`

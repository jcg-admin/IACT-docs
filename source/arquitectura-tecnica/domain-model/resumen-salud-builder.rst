.. meta::
 :artefacto: AT_DM_CLASS_RESUMEN_SALUD_BUILDER
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

.. _dm_class_resumen_salud_builder:

====================
ResumenSaludBuilder
====================

Builder que ensambla un ``ResumenSalud`` consultando varias
fuentes (``PipelineExecutionRepo`` para runs,
``ErroresETLService`` para errores, runtime para lag) y
aplicando reglas configurables para derivar el
``EstadoSalud`` discreto.

Sigue el patron Builder (GoF) — la entidad ``ResumenSalud``
es inmutable; el builder centraliza la logica de calculo
para evitar dispersarla en consumidores.

.. uml::
 :caption: ResumenSaludBuilder — ensamble del DTO de salud
           con derivacion de estado_general por reglas.

 @startuml

 class ResumenSaludBuilder {
   - umbral_lag_amarillo : Integer
   - umbral_lag_rojo : Integer
   - umbral_errores_rojo : Integer
   --
   + build(executions : List<PipelineExecution>, \
            errores : List<ETLError>) : ResumenSalud
   - derive_estado(metrics : Metrics) : EstadoSalud
 }

 class ResumenSalud
 class PipelineExecution
 class ETLError

 ResumenSaludBuilder ..> ResumenSalud : produces
 ResumenSaludBuilder --> PipelineExecution : reads
 ResumenSaludBuilder --> ETLError : reads

 @enduml

Operaciones principales
=======================

- ``build(executions, errores)`` — pipeline de ensamble:

  1. Cuenta exitosas/fallidas en la ventana.
  2. Cuenta runs activos (state=RUNNING).
  3. Calcula ``lag_segundos`` = ahora — ultimo exito.
  4. Cuenta errores recientes en la ventana.
  5. Deriva ``estado_general`` aplicando umbrales:

     - VERDE si lag < umbral_amarillo y errores < umbral_rojo.
     - AMARILLO si lag entre umbrales.
     - ROJO si lag > umbral_rojo o errores > umbral_rojo.

  6. Empaqueta en ``ResumenSalud`` inmutable.

Restricciones aplicables
========================

- Los umbrales son configurables por entorno; no quedan
  hardcoded.

Trazabilidad a UCs
==================

- :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index` —
  builder invocado por SupervisionETLService.

Relaciones
==========

- Producido por inyeccion de dependencia con umbrales
  configurados.
- Lee ``PipelineExecution`` (raw) y ``ETLError`` (raw).
- Produce ``ResumenSalud`` (DTO inmutable).
- Es invocado por ``SupervisionETLService.supervisar``.

.. seealso::

 - :doc:`/arquitectura-tecnica/domain-model/resumen-salud`
 - :doc:`/arquitectura-tecnica/domain-model/pipeline-execution`
 - :doc:`/arquitectura-tecnica/domain-model/errores-etl-service`

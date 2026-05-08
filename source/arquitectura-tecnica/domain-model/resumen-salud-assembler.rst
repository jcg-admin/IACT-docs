.. meta::
 :artefacto: AT_DM_CLASS_RESUMEN_SALUD_ASSEMBLER
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

.. _dm_class_resumen_salud_assembler:

====================
ResumenSaludAssembler
====================

Assembler que construye un ``ResumenSalud`` consultando
varias fuentes (``PipelineExecutionRepo`` para runs,
``ErroresETLService`` para errores, runtime para lag) y
aplicando reglas configurables para derivar el
``EstadoSalud`` discreto.

Patron Assembler (no Builder GoF) — la clase expone una
sola operacion ``build`` que recibe todas las entradas y
devuelve el ``ResumenSalud`` inmutable. No hay interfaz
fluent encadenable. Centraliza la logica de calculo para
evitar dispersarla en consumidores.

.. note::

   El sufijo ``Builder`` esta prohibido por
   CLEAN_CODE_NAMING_PRINCIPLES §1.2 cuando no hay
   interfaz fluent real. Esta clase fue renombrada de
   ``ResumenSaludBuilder`` a ``ResumenSaludAssembler``
   en WP ``naming-rules-resolution`` (D3 del audit
   ``clean-code-naming``).

.. uml::
 :caption: ResumenSaludAssembler — ensamble del DTO de salud
           con derivacion de estado_general por reglas.

 @startuml

 class ResumenSaludAssembler {
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

 ResumenSaludAssembler ..> ResumenSalud : produces
 ResumenSaludAssembler --> PipelineExecution : reads
 ResumenSaludAssembler --> ETLError : reads

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

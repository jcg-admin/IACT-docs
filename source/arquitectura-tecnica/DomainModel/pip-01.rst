.. meta::
 :artefacto: AT_UC_PIP_01_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_01_domain:

=================================================
UC_PIP_01 — Supervisar ETL: Domain Model
=================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index`.

.. uml::
 :caption: UC_PIP_01 — Domain Model

 @startuml

 left to right direction

 class ETLEjecucion
 class etl_runs
 class ETLEjecucion

 ETLEjecucion --> etl_runs
 etl_runs --> ETLEjecucion

 @enduml


.. uml::
 :caption: UC_PIP_01 — Supervisar ETL — Estado de ETLRun

 @startuml
 hide empty description

 [*] --> Programado : agendar ejecucion
 Programado --> Ejecutando : sp_etl_maestro inicia
 Ejecutando --> Completado : todas las etapas OK
 Ejecutando --> Fallido : error en etapa
 Completado --> [*] : registrar en etl_runs
 Fallido --> Reintento : politica de reintento
 Reintento --> Ejecutando : reintentar
 Reintento --> [*] : agotar reintentos

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index`

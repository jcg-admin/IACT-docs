.. meta::
 :artefacto: AT_UC_PIP_03_DOMAIN
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-03
 :ultimo_cambio: 2026-05-03
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_03_domain:

====================================================================
UC_PIP_03 — Consultar Disponibilidad de Datos: Domain Model
====================================================================

Entidades del dominio y sus relaciones. Vista logica del modelo
conceptual para :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/index`.

.. uml::
 :caption: UC_PIP_03 — Domain Model

 @startuml

 left to right direction

 class ETLEjecucion
 class BaseAnaliticaIVR
 class ETLEjecucion

 ETLEjecucion --> BaseAnaliticaIVR
 BaseAnaliticaIVR --> ETLEjecucion

 @enduml


.. uml::
 :caption: UC_PIP_03 — Consultar Disponibilidad de Datos — Estado de ETLRun

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
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-03/index`

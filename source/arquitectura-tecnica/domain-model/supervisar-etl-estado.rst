.. meta::
 :artefacto: AT_UC_PIP_01_DOMAIN_ESTADO
 :tipo: Diagrama Arquitectonico — Domain Model
 :dominio: arquitectura_tecnica
 :subdominio: DomainModel
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_pip_01_domain_estado:

=============================================
UC_PIP_01 — Supervisar ETL — Estado de ETLRun
=============================================

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

.. seealso::

 :doc:`/arquitectura-tecnica/modelo-dominio-iact`
 :doc:`/requisitos/casos-uso/pipeline/uc-pip-01/index`

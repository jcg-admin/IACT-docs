.. meta::
 :artefacto: AT_UC_MOD_LOGS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 2.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-05
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_logs:

==========================================
MOD_Logs — Consulta de Logs: UC por Modulo
==========================================

Acceso a los logs operativos del sistema: logs de
aplicación, pipeline, infraestructura, estado del sistema
y métricas técnicas. Distintos roles controlan qué tipo
de log puede ver cada usuario.

.. uml::
 :caption: MOD_Logs — SystemAdmin opera todo el espectro;
           Auditor lee aplicación y pipeline; PipelineAdmin
           especializado en pipeline.

 @startuml
 left to right direction

 actor SystemAdmin
 actor Auditor
 actor PipelineAdmin

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nVer Logs\ndel Sistema" as VER_LOGS_SISTEMA
   usecase "UC_LOG_02\nVer Logs Pipeline" as VER_LOGS_PIPELINE
   usecase "UC_LOG_03\nBuscar Logs" as BUSCAR_LOGS
   usecase "UC_LOG_04\nExportar Logs" as EXPORTAR_LOGS
   usecase "UC_LOG_05\nVer Logs de\nInfraestructura" as VER_LOGS_INFRAESTRUCTURA
   usecase "UC_LOG_06\nVer Estado\ndel Sistema" as VER_ESTADO_SISTEMA
   usecase "UC_LOG_07\nVer Metricas\nTecnicas" as VER_METRICAS_TECNICAS
 }

 SystemAdmin --> VER_LOGS_SISTEMA
 SystemAdmin --> VER_LOGS_INFRAESTRUCTURA
 SystemAdmin --> VER_ESTADO_SISTEMA
 SystemAdmin --> VER_METRICAS_TECNICAS
 SystemAdmin --> EXPORTAR_LOGS

 Auditor --> VER_LOGS_SISTEMA
 Auditor --> VER_LOGS_PIPELINE

 PipelineAdmin --> VER_LOGS_PIPELINE

 VER_LOGS_SISTEMA ..> BUSCAR_LOGS : <<extend>>
 VER_LOGS_PIPELINE ..> BUSCAR_LOGS : <<extend>>
 BUSCAR_LOGS ..> EXPORTAR_LOGS : <<extend>>

 note right of MOD_Logs
   Codenames RBAC:
     SystemAdmin (AGR-010) →
       view_application_logs,
       view_infrastructure_logs,
       view_system_health,
       view_technical_metrics,
       export_logs
     Auditor (AGR-008) →
       view_application_logs, view_pipeline_logs
     PipelineAdmin (AGR-009) →
       view_pipeline_logs
   search_logs es capacidad transversal
   sobre cualquier vista de log.
 end note

 @enduml

Lectura del diagrama
====================

- ``SystemAdmin`` opera el espectro completo: logs de
  aplicación, infraestructura, estado del sistema y
  métricas técnicas; única autoridad para exportar.
- ``Auditor`` consume logs de aplicación y pipeline
  para trazabilidad de compliance.
- ``PipelineAdmin`` foco operativo en logs del pipeline
  para diagnosticar fallos del ``UC_PIP_04``.
- ``UC_LOG_03 Buscar Logs`` ``<<extend>>`` cualquier
  vista — es capacidad transversal disparada por filtros
  del usuario.

Implementación en domain-model
==============================

Las clases canónicas que materializan estos UCs viven en
``source/arquitectura-tecnica/domain-model/``:

- :doc:`/arquitectura-tecnica/domain-model/application-log` — ApplicationLog (UC_LOG_01).
- :doc:`/arquitectura-tecnica/domain-model/pipeline-log` — PipelineLog (UC_LOG_02).
- :doc:`/arquitectura-tecnica/domain-model/infrastructure-log` — InfrastructureLog (UC_LOG_05).
- :doc:`/arquitectura-tecnica/domain-model/system-health` — SystemHealth (UC_LOG_06).
- :doc:`/arquitectura-tecnica/domain-model/technical-metric` — TechnicalMetric (UC_LOG_07).


.. toctree::
 :maxdepth: 1
 :caption: Casos de uso del módulo

 uc-log-01/index
 uc-log-02/index
 uc-log-03/index
 uc-log-04/index
 uc-log-05/index
 uc-log-06/index
 uc-log-07/index

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

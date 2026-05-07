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

 rectangle "MOD_Logs" as MOD_Logs {
   usecase "UC_LOG_01\nVer Logs\ndel Sistema\n.. extension points ..\nBuscar" as VER_LOGS_SISTEMA
   usecase "UC_LOG_02\nVer Logs Pipeline\n.. extension points ..\nBuscar" as VER_LOGS_PIPELINE
   usecase "UC_LOG_03\nBuscar Logs\n.. extension points ..\nExportar" as BUSCAR_LOGS
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

 BUSCAR_LOGS ..> VER_LOGS_SISTEMA : <<extend>>
 BUSCAR_LOGS ..> VER_LOGS_PIPELINE : <<extend>>
 EXPORTAR_LOGS ..> BUSCAR_LOGS : <<extend>>

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

Casos de uso del módulo
=========================

Cada UC tiene su especificación textual completa y su diagrama
individual (con `<<include>>` y `<<extend>>` per uml-07) en
``source/requisitos/casos-uso/``:

.. list-table::
 :header-rows: 1
 :widths: 20 50 30

 * - UC
   - Nombre
   - Diagrama
 * - :doc:`UC_LOG_01 </requisitos/casos-uso/logs/uc-log-01/index>`
   - Consultar Logs del Sistema
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-01/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_LOG_02 </requisitos/casos-uso/logs/uc-log-02/index>`
   - Consultar Logs del ETL
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-02/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_LOG_03 </requisitos/casos-uso/logs/uc-log-03/index>`
   - Buscar Logs
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-03/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_LOG_04 </requisitos/casos-uso/logs/uc-log-04/index>`
   - Exportar Logs
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-04/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_LOG_05 </requisitos/casos-uso/logs/uc-log-05/index>`
   - Ver Logs de Infraestructura
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-05/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_LOG_06 </requisitos/casos-uso/logs/uc-log-06/index>`
   - Ver Estado del Sistema
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-06/diagramas-uml/diagrama-de-caso-de-uso>`
 * - :doc:`UC_LOG_07 </requisitos/casos-uso/logs/uc-log-07/index>`
   - Ver Metricas Tecnicas
   - :doc:`Diagrama </requisitos/casos-uso/logs/uc-log-07/diagramas-uml/diagrama-de-caso-de-uso>`

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

UC standalone uml-07
====================

Diagramas standalone uml-07 por UC (auto-explicativos):

.. toctree::
 :maxdepth: 1

 uc-log-01-consultar-logs-del-sistema
 uc-log-02-consultar-logs-del-etl
 uc-log-03-buscar-logs
 uc-log-04-exportar-logs
 uc-log-05-ver-logs-de-infraestructura
 uc-log-06-ver-estado-del-sistema
 uc-log-07-ver-metricas-tecnicas

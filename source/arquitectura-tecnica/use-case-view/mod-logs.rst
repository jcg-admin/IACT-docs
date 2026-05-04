.. meta::
 :artefacto: AT_UC_MOD_LOGS
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uc_mod_logs:

==========================================
MOD_Logs — Consulta de Logs: UC por Modulo
==========================================

MOD_Logs — Consulta de Logs
==============================

Acceso a los logs operativos del sistema: logs de aplicacion, ETL,
infraestructura, estado del sistema y metricas tecnicas. Distintas
funciones RBAC controlan que tipo de log puede ver cada usuario.

.. uml::
 :caption: Figura 24 — MOD_Logs: casos de uso

 @startuml
 left to right direction

 actor "view_application_logs" as view_application_logs
 actor "view_etl_logs" as view_etl_logs
 actor "search_logs" as search_logs
 actor "export_logs" as export_logs
 actor "view_infrastructure_logs" as view_infrastructure_logs
 actor "view_system_health" as view_system_health
 actor "view_technical_metrics" as view_technical_metrics

 rectangle "MOD_Logs" {
   usecase "UC_LOG_01\nVer Logs\ndel Sistema" as VER_LOGS_SISTEMA
   usecase "UC_LOG_02\nVer Logs ETL\n(etl_runs)" as VER_LOGS_ETL
   usecase "UC_LOG_03\nBuscar Logs" as BUSCAR_LOGS
   usecase "UC_LOG_04\nExportar Logs" as EXPORTAR_LOGS
   usecase "UC_LOG_05\nVer Logs de\nInfraestructura" as VER_LOGS_INFRAESTRUCTURA
   usecase "UC_LOG_06\nVer Estado\ndel Sistema" as VER_ESTADO_SISTEMA
   usecase "UC_LOG_07\nVer Metricas\nTecnicas" as VER_METRICAS_TECNICAS
 }

 view_application_logs --> VER_LOGS_SISTEMA
 view_etl_logs --> VER_LOGS_ETL
 search_logs --> BUSCAR_LOGS
 export_logs --> EXPORTAR_LOGS
 view_infrastructure_logs --> VER_LOGS_INFRAESTRUCTURA
 view_system_health --> VER_ESTADO_SISTEMA
 view_technical_metrics --> VER_METRICAS_TECNICAS

 VER_LOGS_SISTEMA ..> BUSCAR_LOGS : <<extend>>
 VER_LOGS_ETL ..> BUSCAR_LOGS : <<extend>>
 BUSCAR_LOGS ..> EXPORTAR_LOGS : <<extend>>

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

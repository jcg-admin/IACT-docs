.. meta::
 :artefacto: ARQ_MOD_008_DIAG_COMPONENTES
 :tipo: Diagrama Arquitectonico — Comportamiento de Modulo
 :dominio: arquitectura_tecnica
 :subdominio: modulos/sys-logs/diagramas
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arq_mod_008_componentes_mod_logs:

==================================
Diagrama de componentes — MOD_Logs
==================================

Diagrama de componentes — MOD_Logs
=====================================

.. uml::
 :caption: Componentes de MOD_Logs y pipeline de recoleccion de logs.

 @startuml

 component "Aplicaciones del sistema\n(stdout/stderr)" as AppsDjango
 component "fluent-bit\n(shipper)" as FluentBit
 database "LogStore\n(PostgreSQL)" as Logstore
 database "etl_runs" as ETL_LOG

 component "view_application_logs" as view_application_logs
 component "view_etl_logs" as view_etl_logs
 component "search_logs" as search_logs
 component "export_logs" as export_logs
 component "InternalMailbox" as Internalmailbox

 AppsDjango --> FluentBit : stdout logs estructurados
 FluentBit --> Logstore : registrar logs

 view_application_logs --> Logstore : consultar sistema
 view_etl_logs --> ETL_LOG : consultar etl_runs
 search_logs --> Logstore : consultar con filtros
 export_logs --> Logstore : consultar rango + generar CSV
 export_logs --> Internalmailbox : notificar via buzon

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/modulos/sys-logs/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

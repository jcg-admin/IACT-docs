.. meta::
 :artefacto: AT_ARQ_SISTEMA_03_DFD_NIVEL_1
 :tipo: Diagrama Arquitectonico — Arquitectura del Sistema
 :dominio: arquitectura_tecnica
 :subdominio: ArquitecturaSistema
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arquitectura_dfd_nivel_1:

======================================
DFD Nivel 1 — Sub-procesos del Sistema
======================================

4. DFD Nivel 1 — Sub-procesos del Sistema
==========================================

El DFD Nivel 1 descompone el sistema IACT en sus sub-procesos
numerados con los flujos de datos entre ellos y los almacenes de
datos (``etl_runs``, ``base_ivr_*``, ``audit_log``,
``auth_session``).

.. uml::
 :caption: Figura 3 — DFD Nivel 1: descomposicion de sub-procesos

 @startuml
 skinparam rectangle {
   RoundCorner 10
   BackgroundColor white
   BorderColor #333333
   FontSize 10
 }
 skinparam database {
   BackgroundColor #f5f5f5
   BorderColor #555555
 }
 skinparam arrowColor #333333

 rectangle "Sistema IVR" as SistemaIVR
 rectangle "view_pipeline_status" as SupervisorSistema
 rectangle "view_reports" as AnalistaReportes
 rectangle "APScheduler" as DisparadorScheduler

 rectangle "1\nAutenticacion JWT" as PASO_AUTENTICACION
 rectangle "2\nDashboard IVR" as DASHBOARD_IVR
 rectangle "3\nCierre de Sesion" as CIERRE_SESION
 rectangle "4\nGestion\nPipeline ETL" as GESTION_PIPELINE_ETL
 rectangle "5\nConsulta\nde Logs" as CONSULTA_LOGS
 rectangle "6\nMOD Reports" as MODULO_REPORTES
 rectangle "7\nServicio de\nReportes\nsp_rpt_*" as BASE_ANALITICA_IVR
 rectangle "8\nAlertas" as ALERTAS_NOTIFICACIONES
 rectangle "9\nResolver Segmento\nUC_INC_RPT_01" as RESOLVER_SEGMENTO
 rectangle "10\nAuditoria" as AUDITORIA_ACCESO

 database "etl_runs" as DS1
 database "base_ivr_*" as DS2
 database "audit_log" as DS3
 database "auth_session" as DS4

 IVR --> BASE_ANALITICA_IVR : datos IVR raw
 SUP --> PASO_AUTENTICACION : credenciales
 ANA --> PASO_AUTENTICACION : credenciales
 SCH --> GESTION_PIPELINE_ETL : disparo automatico

 PASO_AUTENTICACION --> DS4 : crear sesion
 PASO_AUTENTICACION --> DASHBOARD_IVR : JWT valido

 DASHBOARD_IVR --> GESTION_PIPELINE_ETL
 DASHBOARD_IVR --> CONSULTA_LOGS
 DASHBOARD_IVR --> MODULO_REPORTES
 DASHBOARD_IVR --> ALERTAS_NOTIFICACIONES

 GESTION_PIPELINE_ETL --> DS1 : registrar ejecucion
 GESTION_PIPELINE_ETL --> RESOLVER_SEGMENTO

 BASE_ANALITICA_IVR --> DS2 : leer datos analiticos
 DS2 --> BASE_ANALITICA_IVR

 MODULO_REPORTES --> RESOLVER_SEGMENTO
 RESOLVER_SEGMENTO --> MODULO_REPORTES : segmentos del usuario

 DS1 --> GESTION_PIPELINE_ETL : historial ETL
 CONSULTA_LOGS --> DS3 : consultar logs

 ALERTAS_NOTIFICACIONES --> AUDITORIA_ACCESO
 CONSULTA_LOGS --> AUDITORIA_ACCESO
 AUDITORIA_ACCESO --> DS3 : registrar auditoria
 RESOLVER_SEGMENTO --> CIERRE_SESION
 AUDITORIA_ACCESO --> CIERRE_SESION

 @enduml

.. note::

 Los almacenes de datos ``etl_runs`` y ``base_ivr_*`` residen en
 **Almacen de Datos**. Los almacenes ``audit_log`` y ``auth_session``
 residen en **PostgreSQL** (tablas operacionales del sistema). Los
 stored procedures ``sp_rpt_*`` y ``sp_etl_*`` son parte del
 motor Almacen de Datos y no del codigo Python.

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`

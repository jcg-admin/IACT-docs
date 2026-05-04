.. meta::
 :artefacto: AT_ARQ_SISTEMA_01_GENERAL
 :tipo: Diagrama Arquitectonico — Arquitectura del Sistema
 :dominio: arquitectura_tecnica
 :subdominio: ArquitecturaSistema
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _arquitectura_sistema_general:

===========================================
Arquitectura del Sistema — Diagrama General
===========================================

2. Arquitectura del Sistema — Diagrama General
================================================

El diagrama siguiente muestra todas las funcionalidades del sistema
en orden de acceso. Representa el flujo completo desde la
autenticacion hasta el cierre de sesion, incluyendo las rutas hacia
los modulos funcionales y sus interdependencias.

Los actores externos son el **Sistema IVR** (fuente de datos de
llamadas) y los **Usuarios IACT** (Supervisores de Operaciones y
Analistas de Datos). El sistema no tiene registro publico: las
cuentas son creadas por el Administrador IACT.

.. uml::
 :caption: Figura 1 — Arquitectura general del Sistema IACT

 @startuml
 skinparam rectangle {
   RoundCorner 10
   BackgroundColor white
   BorderColor #333333
   FontSize 11
 }
 skinparam arrowColor #333333

 rectangle "Sistema IVR\n(Fuente de datos)" as SistemaIVR
 rectangle "view_pipeline_status\n/ view_alerts" as SupervisorSistema
 rectangle "view_reports\n/ view_dashboard" as AnalistaReportes

 rectangle "1\nAutenticacion\nJWT" as PASO_AUTENTICACION
 rectangle "2\nDashboard IVR" as DASHBOARD_IVR
 rectangle "3\nCierre de\nSesion" as CIERRE_SESION
 rectangle "4\nGestion\nPipeline ETL" as GESTION_PIPELINE_ETL
 rectangle "5\nConsulta\nde Logs" as CONSULTA_LOGS
 rectangle "6\nMOD Reports\n(Reportes IVR)" as MODULO_REPORTES
 rectangle "7\nBase Analitica\nIVR" as BASE_ANALITICA_IVR
 rectangle "8\nAlertas y\nNotificaciones" as ALERTAS_NOTIFICACIONES
 rectangle "9\nResolver\nSegmento\nUC_INC_RPT_01" as RESOLVER_SEGMENTO
 rectangle "10\nAuditoria\nde Acceso" as AUDITORIA_ACCESO

 SupervisorSistema --> PASO_AUTENTICACION
 AnalistaReportes --> PASO_AUTENTICACION
 SistemaIVR --> BASE_ANALITICA_IVR

 PASO_AUTENTICACION --> DASHBOARD_IVR
 DASHBOARD_IVR --> GESTION_PIPELINE_ETL
 DASHBOARD_IVR --> CONSULTA_LOGS
 DASHBOARD_IVR --> MODULO_REPORTES
 DASHBOARD_IVR --> ALERTAS_NOTIFICACIONES
 MODULO_REPORTES --> BASE_ANALITICA_IVR
 GESTION_PIPELINE_ETL --> RESOLVER_SEGMENTO
 BASE_ANALITICA_IVR --> RESOLVER_SEGMENTO
 CONSULTA_LOGS --> AUDITORIA_ACCESO
 ALERTAS_NOTIFICACIONES --> AUDITORIA_ACCESO
 RESOLVER_SEGMENTO --> CIERRE_SESION
 AUDITORIA_ACCESO --> CIERRE_SESION

 @enduml

.. note::

 El flujo de datos empieza en la autenticacion JWT (1) a traves de
 la cual el usuario accede a todos los servicios disponibles hasta
 el cierre de sesion (3). Los modulos MOD_Reports (6) y Gestion
 Pipeline ETL (4) dependen de Resolver Segmento (9) para filtrar
 datos por segmento del usuario. La Base Analitica IVR (7) es
 alimentada por el ETL y consumida exclusivamente via
 ``sp_rpt_*``.

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`

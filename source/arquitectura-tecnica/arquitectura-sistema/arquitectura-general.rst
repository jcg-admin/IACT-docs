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

 rectangle "1\nAutenticacion\nJWT" as P1
 rectangle "2\nDashboard IVR" as P2
 rectangle "3\nCierre de\nSesion" as P3
 rectangle "4\nGestion\nPipeline ETL" as P4
 rectangle "5\nConsulta\nde Logs" as P5
 rectangle "6\nMOD Reports\n(Reportes IVR)" as P6
 rectangle "7\nBase Analitica\nIVR" as P7
 rectangle "8\nAlertas y\nNotificaciones" as P8
 rectangle "9\nResolver\nSegmento\nUC_INC_RPT_01" as P9
 rectangle "10\nAuditoria\nde Acceso" as P10

 SUP --> P1
 ANA --> P1
 IVR --> P7

 P1 --> P2
 P2 --> P4
 P2 --> P5
 P2 --> P6
 P2 --> P8
 P6 --> P7
 P4 --> P9
 P7 --> P9
 P5 --> P10
 P8 --> P10
 P9 --> P3
 P10 --> P3

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

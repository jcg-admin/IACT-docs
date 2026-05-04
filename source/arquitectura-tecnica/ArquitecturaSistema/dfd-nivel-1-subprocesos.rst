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

 rectangle "Sistema IVR" as IVR
 rectangle "view_pipeline_status" as SUP
 rectangle "view_reports" as ANA
 rectangle "APScheduler" as SCH

 rectangle "1\nAutenticacion JWT" as P1
 rectangle "2\nDashboard IVR" as P2
 rectangle "3\nCierre de Sesion" as P3
 rectangle "4\nGestion\nPipeline ETL" as P4
 rectangle "5\nConsulta\nde Logs" as P5
 rectangle "6\nMOD Reports" as P6
 rectangle "7\nServicio de\nReportes\nsp_rpt_*" as P7
 rectangle "8\nAlertas" as P8
 rectangle "9\nResolver Segmento\nUC_INC_RPT_01" as P9
 rectangle "10\nAuditoria" as P10

 database "etl_runs" as DS1
 database "base_ivr_*" as DS2
 database "audit_log" as DS3
 database "auth_session" as DS4

 IVR --> P7 : datos IVR raw
 SUP --> P1 : credenciales
 ANA --> P1 : credenciales
 SCH --> P4 : disparo automatico

 P1 --> DS4 : crear sesion
 P1 --> P2 : JWT valido

 P2 --> P4
 P2 --> P5
 P2 --> P6
 P2 --> P8

 P4 --> DS1 : registrar ejecucion
 P4 --> P9

 P7 --> DS2 : leer datos analiticos
 DS2 --> P7

 P6 --> P9
 P9 --> P6 : segmentos del usuario

 DS1 --> P4 : historial ETL
 P5 --> DS3 : consultar logs

 P8 --> P10
 P5 --> P10
 P10 --> DS3 : registrar auditoria
 P9 --> P3
 P10 --> P3

 @enduml

.. note::

 Los almacenes de datos ``etl_runs`` y ``base_ivr_*`` residen en
 **MariaDB**. Los almacenes ``audit_log`` y ``auth_session``
 residen en **PostgreSQL** (tablas operacionales Django). Los
 stored procedures ``sp_rpt_*`` y ``sp_etl_*`` son parte del
 motor MariaDB y no del codigo Python.

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`

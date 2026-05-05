.. meta::
 :artefacto: AT_UML_SISTEMA_10_COMPONENTES
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_componentes:

======================================
Sistema IACT — Diagrama de Componentes
======================================

10. Diagrama de Componentes
=============================

El componente ``view_reports`` accede a los modulos de
reportes y dashboard. El componente ``Backend IACT``
gestiona autenticacion, reportes y ETL. ``Almacen de Datos`` contiene
los 7 stored procedures de reporte (``sp_rpt_*``) y los 4 de
ETL (``sp_etl_*``). ``PostgreSQL`` gestiona usuarios y auditoria.

.. uml::
 :caption: Figura 11 — Diagrama de componentes del Sistema IACT

 @startuml

 component "<<System>>\nview_reports\n(view_reports / view_dashboard)" as SISTEMA_VER_REPORTES {
   artifact "<<artifact>>\nReport Request Buffer\n(JWT + trimestre)" as ARTEFACTO_REPORT_REQUEST
 }

 component "<<System>>\nBackend IACT" as SISTEMA_BACKEND_IACT {
   component "Suggestion\nServicio de Reportes" as SERVICIO_REPORTES_EXTERNO {
     artifact "<<artifact>>\nsp_rpt_llamadas_abandonadas" as ARTEFACTO_SP_RPT_LLAMADAS_ABANDONADAS
     artifact "<<artifact>>\nsp_rpt_centros_transferencia" as ARTEFACTO_SP_RPT_TRANSFERENCIAS
     artifact "<<artifact>>\nsp_rpt_menu_redirigidos" as ARTEFACTO_SP_RPT_MENUS_REDIRIGIDOS
     artifact "<<artifact>>\nsp_rpt_clientes" as ARTEFACTO_SP_RPT_CLIENTES
     artifact "<<artifact>>\nsp_rpt_centros_xsegmento" as ARTEFACTO_SP_RPT_CENTROS_XSEGMENTO
     artifact "<<artifact>>\nsp_rpt_menu_centro" as ARTEFACTO_SP_RPT_MENU_CENTRO
     artifact "<<artifact>>\nsp_rpt_cMENU_ERROR" as ARTEFACTO_SP_RPT_MENU_ERROR
   }
   component "<<process>>\nAuthService\n(JWT + RBAC)" as SERVICIO_AUTH_PROCESO
   component "<<process>>\nSegmentResolver\n(DID_MAP)" as SERVICIO_SEGMENT_RESOLVER
   component "<<process>>\nDisparadorETL\n(management command)" as SERVICIO_ETL_DISPARADOR
 }

 database "<<subsystem>>\nMariaDB 10.1.48" as BASE_DATOS_MARIADB {
   artifact "tbl_historico_*\n(Repositorio IVR)" as ARTEFACTO_HISTORICO_IVR
   artifact "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as ARTEFACTO_BASE_ANALITICA
   artifact "etl_runs\n(Registro ETL)" as ARTEFACTO_ETL_RUNS
 }

 database "<<subsystem>>\nPostgreSQL" as BASE_DATOS_POSTGRESQL {
   artifact "auth_user\n(AccessGroup / AccessFunction)" as ARTEFACTO_AUTH_USER
   artifact "audit_log" as ARTEFACTO_AUDIT_LOG
 }

 SISTEMA_VER_REPORTES --> SISTEMA_BACKEND_IACT : +Request\n1..* a 1\nHTTPS
 SISTEMA_BACKEND_IACT --> BASE_DATOS_MARIADB : communicates\nSQL/TCP :3306
 SISTEMA_BACKEND_IACT --> BASE_DATOS_POSTGRESQL : communicates\nSQL/TCP :5432

 SERVICIO_ETL_DISPARADOR --> ARTEFACTO_HISTORICO_IVR : lee (fuente IVR)
 SERVICIO_ETL_DISPARADOR --> ARTEFACTO_BASE_ANALITICA : escribe via sp_etl_*
 SERVICIO_ETL_DISPARADOR --> ARTEFACTO_ETL_RUNS : registra ejecucion
 SERVICIO_REPORTES_EXTERNO --> ARTEFACTO_BASE_ANALITICA : lee via sp_rpt_*
 SERVICIO_SEGMENT_RESOLVER --> ARTEFACTO_AUTH_USER : lee DIDs RBAC
 SERVICIO_AUTH_PROCESO --> ARTEFACTO_AUTH_USER : valida usuario
 SERVICIO_AUTH_PROCESO --> ARTEFACTO_AUDIT_LOG : registra acciones

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`

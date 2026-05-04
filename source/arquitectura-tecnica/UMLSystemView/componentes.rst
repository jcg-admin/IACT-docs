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
reportes y dashboard. El componente ``Backend IACT`` (Django)
gestiona autenticacion, reportes y ETL. ``MariaDB`` contiene
los 7 stored procedures de reporte (``sp_rpt_*``) y los 4 de
ETL (``sp_etl_*``). ``PostgreSQL`` gestiona usuarios y auditoria.

.. uml::
 :caption: Figura 11 — Diagrama de componentes del Sistema IACT

 @startuml

 component "<<System>>\nview_reports\n(view_reports / view_dashboard)" as COMP_RVG {
   artifact "<<artifact>>\nReport Request Buffer\n(JWT + trimestre)" as ART_REQ
 }

 component "<<System>>\nBackend IACT (Django)" as COMP_BACK {
   component "Suggestion\nServicio de Reportes" as SVC_OUTER {
     artifact "<<artifact>>\nsp_rpt_llamadas_abandonadas" as ART_R1
     artifact "<<artifact>>\nsp_rpt_centros_transferencia" as ART_R2
     artifact "<<artifact>>\nsp_rpt_menu_redirigidos" as ART_R3
     artifact "<<artifact>>\nsp_rpt_clientes" as ART_R4
     artifact "<<artifact>>\nsp_rpt_centros_xsegmento" as ART_R5
     artifact "<<artifact>>\nsp_rpt_menu_centro" as ART_R6
     artifact "<<artifact>>\nsp_rpt_cMENU_ERROR" as ART_R7
   }
   component "<<process>>\nAuthService\n(JWT + RBAC)" as SVC_AUTH
   component "<<process>>\nSegmentResolver\n(DID_MAP)" as SVC_SEG
   component "<<process>>\nDisparadorETL\n(management command)" as SVC_ETL
 }

 database "<<subsystem>>\nMariaDB 10.1.48" as DB_MARIA {
   artifact "tbl_historico_*\n(Repositorio IVR)" as ART_HIST
   artifact "base_ivr_detalle\nbase_ivr_clientes\n(Base Analitica)" as ART_BASE
   artifact "etl_runs\n(Registro ETL)" as ART_ETLRUNS
 }

 database "<<subsystem>>\nPostgreSQL" as DB_PG {
   artifact "auth_user\n(AccessGroup / AccessFunction)" as ART_USERS
   artifact "audit_log" as ART_AUDIT
 }

 COMP_RVG --> COMP_BACK : +Request\n1..* a 1\nHTTPS
 COMP_BACK --> DB_MARIA : communicates\nSQL/TCP :3306
 COMP_BACK --> DB_PG : communicates\nSQL/TCP :5432

 SVC_ETL --> ART_HIST : lee (fuente IVR)
 SVC_ETL --> ART_BASE : escribe via sp_etl_*
 SVC_ETL --> ART_ETLRUNS : registra ejecucion
 SVC_OUTER --> ART_BASE : lee via sp_rpt_*
 SVC_SEG --> ART_USERS : lee DIDs RBAC
 SVC_AUTH --> ART_USERS : valida usuario
 SVC_AUTH --> ART_AUDIT : registra acciones

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`

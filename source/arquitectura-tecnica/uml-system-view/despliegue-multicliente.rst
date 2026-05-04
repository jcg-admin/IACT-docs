.. meta::
 :artefacto: AT_UML_SISTEMA_14_DESPLIEGUE_MULTICLIENTE
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_despliegue_multicliente:

==========================================================
Sistema IACT — Diagrama de Despliegue: Vista Multi-cliente
==========================================================

14. Diagrama de Despliegue — Vista Multi-cliente
=================================================

Vista extendida del despliegue mostrando los distintos tipos de
cliente (grupos RBAC) conectados al servidor de aplicacion.
Cada grupo accede al servidor con su propio JWT y conjunto de
funciones. El servidor organiza sus modulos por area funcional
con los artefactos correspondientes.

.. uml::
 :caption: Figura 15 — Diagrama de despliegue (vista multi-cliente)

 @startuml

 node "view_reports\nos WINDOWS / MacOS" as CLI_RVG {
   node "<<app>>\nNavegador (Chrome / Firefox)" as BR_RVG {
     artifact "<<artifact>>\nUser_View\n(JWT + view_reports)" as ART_RVG
   }
 }

 node "request_pipeline_retry\nos WINDOWS / Linux" as CLI_PAG {
   node "<<app>>\nNavegador (Chrome / Firefox)" as BR_PAG {
     artifact "<<artifact>>\nUser_View\n(JWT + view_pipeline_status)" as ART_PAG
   }
 }

 node "assign_functions\nos WINDOWS" as CLI_UAG {
   node "<<app>>\nNavegador (Chrome / Firefox)" as BR_UAG {
     artifact "<<artifact>>\nUser_View\n(JWT + assign_functions)" as ART_UAG
   }
 }

 node "<<server>>\nServidor IACT" as NODE_SRV {

   node "MOD_Reports\n(view_reports / view_dashboard)" as MOD_RPT {
     artifact "<<artifact>>\nsp_rpt_centros_xsegmento" as ART_S1
     artifact "<<artifact>>\nsp_rpt_llamadas_abandonadas" as ART_S2
   }

   node "MOD_Pipeline ETL\n(view_pipeline_status / request_pipeline_retry)" as MOD_ETL {
     artifact "<<artifact>>\nsp_etl_maestro" as ART_E1
     artifact "<<artifact>>\netl_runs" as ART_E2
   }

   node "MOD_Logs\n(view_audit_log)" as MOD_LOG {
     artifact "<<artifact>>\naudit_log" as ART_L1
   }

   node "MOD_Admin\n(assign_functions / create_users)" as MOD_ADM {
     artifact "<<artifact>>\nAccessGroup" as ART_A1
     artifact "<<artifact>>\nAccessFunction" as ART_A2
   }

 }

 node "Database" as NODE_DB {
   artifact "<<artifact>>\nbase_ivr_detalle\nbase_ivr_clientes" as DB_IVR
   artifact "<<artifact>>\nauth_user\naudit_log" as DB_AUTH
   artifact "<<artifact>>\ntbl_historico_*" as DB_HIST
 }

 CLI_RVG --> NODE_SRV : +receive Fetch\n1..* 1 +send
 CLI_PAG --> NODE_SRV : +receive Fetch\n1..* 1 +send
 CLI_UAG --> NODE_SRV : +receive Fetch\n1..* 1 +send
 NODE_SRV --> NODE_DB : +receive/send\nFetch 1 1 +receive/send

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`

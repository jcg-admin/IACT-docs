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

 node "view_reports\nos WINDOWS / MacOS" as CLIENTE_REPORTES {
   node "<<app>>\nNavegador (Chrome / Firefox)" as NAVEGADOR_REPORTES {
     artifact "<<artifact>>\nUser_View\n(JWT + view_reports)" as ARTEFACTO_VISTA_REPORTES
   }
 }

 node "request_pipeline_retry\nos WINDOWS / Linux" as CLIENTE_PIPELINE {
   node "<<app>>\nNavegador (Chrome / Firefox)" as NAVEGADOR_PIPELINE {
     artifact "<<artifact>>\nUser_View\n(JWT + view_pipeline_status)" as ARTEFACTO_VISTA_PIPELINE_ADMIN
   }
 }

 node "assign_functions\nos WINDOWS" as CLIENTE_ASIGNACION {
   node "<<app>>\nNavegador (Chrome / Firefox)" as NAVEGADOR_ASIGNACION {
     artifact "<<artifact>>\nUser_View\n(JWT + assign_functions)" as ARTEFACTO_VISTA_ASIGNACION
   }
 }

 node "<<server>>\nServidor IACT" as NODO_SERVIDOR_IACT {

   node "MOD_Reports\n(view_reports / view_dashboard)" as MODULO_REPORTES {
     artifact "<<artifact>>\nsp_rpt_centros_xsegmento" as ARTEFACTO_SP_RPT_CENTROS_XSEGMENTO
     artifact "<<artifact>>\nsp_rpt_llamadas_abandonadas" as ARTEFACTO_SP_RPT_LLAMADAS_ABANDONADAS
   }

   node "MOD_Pipeline ETL\n(view_pipeline_status / request_pipeline_retry)" as MODULO_ETL {
     artifact "<<artifact>>\nsp_etl_maestro" as ARTEFACTO_SP_ETL_MAESTRO
     artifact "<<artifact>>\netl_runs" as ARTEFACTO_ETL_RUNS
   }

   node "MOD_Logs\n(view_audit_log)" as MODULO_LOGS {
     artifact "<<artifact>>\naudit_log" as ARTEFACTO_AUDIT_LOG
   }

   node "MOD_Admin\n(assign_functions / create_users)" as MODULO_ADMIN {
     artifact "<<artifact>>\nAccessGroup" as ARTEFACTO_ACCESS_GROUP
     artifact "<<artifact>>\nAccessFunction" as ARTEFACTO_ACCESS_FUNCTION
   }

 }

 node "Database" as NODO_BASE_DATOS {
   artifact "<<artifact>>\nbase_ivr_detalle\nbase_ivr_clientes" as BASE_DATOS_IVR
   artifact "<<artifact>>\nauth_user\naudit_log" as BASE_DATOS_AUTH
   artifact "<<artifact>>\ntbl_historico_*" as BASE_DATOS_HISTORICO
 }

 CLIENTE_REPORTES --> NODO_SERVIDOR_IACT : +receive Fetch\n1..* 1 +send
 CLIENTE_PIPELINE --> NODO_SERVIDOR_IACT : +receive Fetch\n1..* 1 +send
 CLIENTE_ASIGNACION --> NODO_SERVIDOR_IACT : +receive Fetch\n1..* 1 +send
 NODO_SERVIDOR_IACT --> NODO_BASE_DATOS : +receive/send\nFetch 1 1 +receive/send

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`

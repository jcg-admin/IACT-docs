.. meta::
 :artefacto: AT_UML_SISTEMA_03_CASOS_USO
 :tipo: Diagrama Arquitectonico — UML Sistema
 :dominio: arquitectura_tecnica
 :subdominio: UMLSystemView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _uml_sistema_casos_uso:

=======================================
Sistema IACT — Diagrama de Casos de Uso
=======================================

3. Diagrama de Casos de Uso
=============================

.. uml::
 :caption: Figura 4 — Diagrama de casos de uso del Sistema IACT

 @startuml
 left to right direction

 actor "view_reports\n(view_dashboard)" as view_reports
 actor "view_pipeline_status\n(view_alerts)" as view_pipeline_status
 actor "request_pipeline_retry" as request_pipeline_retry
 actor "assign_functions\n(create_users)" as assign_functions
 actor "view_audit_log" as view_audit_log
 actor "APScheduler\n/ Cron" as APScheduler
 actor "Sistema IVR\n(fuente datos)" as SistemaIVR

 rectangle "Sistema IACT" {
   usecase "Autenticar JWT" as CLUSTER_AUTH
   usecase "Acceder a\nModulos" as CLUSTER_ACCESO
   usecase "Ver Dashboard IVR" as VER_DASHBOARD_IVR
   usecase "Ver Reportes IVR" as CLUSTER_REPORTES
   usecase "Resolver Segmento\nUC_INC_RPT_01" as RESOLVER_SEGMENTO
   usecase "Ver Llamadas\nAbandonadas\n(sp_rpt_llamadas_abandonadas)" as VER_LLAMADAS_ABANDONADAS
   usecase "Ver\nTransferencias\n(sp_rpt_centros_transferencia)" as VER_TRANSFERENCIAS
   usecase "Ver Menus IVR\n(sp_rpt_menu_redirigidos)" as VER_MENUS_IVR
   usecase "Ver Clientes\nUnicos\n(sp_rpt_clientes)" as VER_CLIENTES_UNICOS
   usecase "Gestionar\nPipeline ETL" as CLUSTER_ETL
   usecase "Ver Disponibilidad\nde Datos" as VER_DISPONIBILIDAD_DATOS
   usecase "Consultar Logs\n(view_audit_log)" as CLUSTER_LOGS
   usecase "Gestionar\nFunciones RBAC" as CLUSTER_RBAC
   usecase "Cerrar Sesion" as CERRAR_SESION
 }

 view_reports --> CLUSTER_AUTH
 view_pipeline_status --> CLUSTER_AUTH
 request_pipeline_retry --> CLUSTER_AUTH
 assign_functions --> CLUSTER_AUTH
 view_audit_log --> CLUSTER_AUTH
 APScheduler --> CLUSTER_ETL
 IVR --> CLUSTER_ETL

 CLUSTER_AUTH ..> CLUSTER_ACCESO : <<include>>
 CLUSTER_ACCESO ..> VER_DASHBOARD_IVR : <<extend>>
 CLUSTER_ACCESO ..> CLUSTER_REPORTES : <<extend>>
 CLUSTER_ACCESO ..> CLUSTER_ETL : <<extend>>
 CLUSTER_ACCESO ..> CLUSTER_LOGS : <<extend>>
 CLUSTER_ACCESO ..> CERRAR_SESION : <<extend>>
 assign_functions --> CLUSTER_RBAC
 CLUSTER_RBAC ..> CLUSTER_AUTH : <<include>>

 CLUSTER_REPORTES ..> RESOLVER_SEGMENTO : <<include>>
 VER_DASHBOARD_IVR ..> RESOLVER_SEGMENTO : <<include>>

 CLUSTER_REPORTES ..> VER_LLAMADAS_ABANDONADAS : <<extend>>
 CLUSTER_REPORTES ..> VER_TRANSFERENCIAS : <<extend>>
 CLUSTER_REPORTES ..> VER_MENUS_IVR : <<extend>>
 CLUSTER_REPORTES ..> VER_CLIENTES_UNICOS : <<extend>>

 CLUSTER_ETL ..> VER_DISPONIBILIDAD_DATOS : <<extend>>

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`

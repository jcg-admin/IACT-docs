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
 actor "Sistema IVR\n(fuente datos)" as IVR

 rectangle "Sistema IACT" {
   usecase "Autenticar JWT" as UC_AUTH
   usecase "Acceder a\nModulos" as UC_ACC
   usecase "Ver Dashboard IVR" as UC_DASH
   usecase "Ver Reportes IVR" as UC_RPT
   usecase "Resolver Segmento\nUC_INC_RPT_01" as UC_INC
   usecase "Ver Llamadas\nAbandonadas\n(sp_rpt_llamadas_abandonadas)" as UC_R13
   usecase "Ver\nTransferencias\n(sp_rpt_centros_transferencia)" as UC_R15
   usecase "Ver Menus IVR\n(sp_rpt_menu_redirigidos)" as UC_R16
   usecase "Ver Clientes\nUnicos\n(sp_rpt_clientes)" as UC_R17
   usecase "Gestionar\nPipeline ETL" as UC_PIP
   usecase "Ver Disponibilidad\nde Datos" as UC_DISP
   usecase "Consultar Logs\n(view_audit_log)" as UC_LOG
   usecase "Gestionar\nFunciones RBAC" as UC_RBAC
   usecase "Cerrar Sesion" as UC_LOGOUT
 }

 view_reports --> UC_AUTH
 view_pipeline_status --> UC_AUTH
 request_pipeline_retry --> UC_AUTH
 assign_functions --> UC_AUTH
 view_audit_log --> UC_AUTH
 APScheduler --> UC_PIP
 IVR --> UC_PIP

 UC_AUTH ..> UC_ACC : <<include>>
 UC_ACC ..> UC_DASH : <<extend>>
 UC_ACC ..> UC_RPT : <<extend>>
 UC_ACC ..> UC_PIP : <<extend>>
 UC_ACC ..> UC_LOG : <<extend>>
 UC_ACC ..> UC_LOGOUT : <<extend>>
 assign_functions --> UC_RBAC
 UC_RBAC ..> UC_AUTH : <<include>>

 UC_RPT ..> UC_INC : <<include>>
 UC_DASH ..> UC_INC : <<include>>

 UC_RPT ..> UC_R13 : <<extend>>
 UC_RPT ..> UC_R15 : <<extend>>
 UC_RPT ..> UC_R16 : <<extend>>
 UC_RPT ..> UC_R17 : <<extend>>

 UC_PIP ..> UC_DISP : <<extend>>

 @enduml

.. seealso::

 :doc:`/arquitectura-tecnica/vistas-kruchten`
 :doc:`/requisitos/casos-uso/index`

.. meta::
 :artefacto: AT_RBAC_FUNCIONES_POR_MODULO
 :tipo: Diagrama Arquitectonico — UC por Modulo
 :dominio: arquitectura_tecnica
 :subdominio: UCModuleView
 :estado: Vigente
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :ultimo_cambio: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _rbac_funciones_por_modulo:

=============================================
Vista Consolidada — Funciones RBAC por Modulo
=============================================

Vista Consolidada — Todas las Funciones RBAC por Modulo
=========================================================

Mapa de funciones RBAC del sistema IACT y los modulos que
las requieren. Referencia cruzada entre UC y funcion RBAC.

.. uml::
 :caption: Figura 28 — Mapa de funciones RBAC por modulo

 @startuml

 package "MOD_Auth" {
   artifact "view_all_active_sessions" as F_SESS
 }

 package "MOD_Users" {
   artifact "create_users" as F_CU
   artifact "list_users" as F_LU
   artifact "update_users" as F_UU
   artifact "deactivate_users" as F_DU
 }

 package "MOD_Access / MOD_Permissions" {
   artifact "assign_functions" as F_AF
   artifact "revoke_functions" as F_RF
   artifact "view_assignments" as F_VA
   artifact "assign_function_groups" as F_AFG
   artifact "revoke_function_group" as F_RFG
   artifact "create_function_group" as F_MAG
   artifact "assign_functions_to_group" as F_MAGC
   artifact "view_separation_rules" as F_VSR
   artifact "view_audit_log" as F_VAA
   artifact "view_own_navigation" as F_VON
 }

 package "MOD_Reports" {
   artifact "view_dashboard" as F_VD
   artifact "view_reports" as F_VR
   artifact "view_kpis" as F_VK
   artifact "view_charts" as F_VCH
   artifact "filter_reports" as F_FR
   artifact "export_csv" as F_ECSV
   artifact "export_excel" as F_EXL
   artifact "export_pdf" as F_EPDF
   artifact "schedule_report" as F_SCH
   artifact "save_view" as F_SV
   artifact "share_report" as F_SHR
 }

 package "MOD_Pipeline" {
   artifact "view_pipeline_status" as F_VEE
   artifact "view_pipeline_errors" as F_VEER
   artifact "view_data_availability" as F_VDD
   artifact "request_pipeline_retry" as F_RE
 }

 package "MOD_Alerts" {
   artifact "configure_team_alerts" as F_MAT
   artifact "view_alerts" as F_VAA2
   artifact "acknowledge_alert" as F_ACA
   artifact "view_alert_history" as F_VAH
 }

 package "MOD_Audit / MOD_Logs" {
   artifact "view_audit_log" as F_VGA
   artifact "search_audit_log" as F_SA
   artifact "export_audit_log" as F_EA
   artifact "generate_compliance_report" as F_GCR
   artifact "view_application_logs" as F_VSL
   artifact "view_etl_logs" as F_VEL
   artifact "search_logs" as F_SL
   artifact "export_logs" as F_EL
   artifact "view_infrastructure_logs" as F_VIL
   artifact "view_system_health" as F_VSS
   artifact "view_technical_metrics" as F_VTM
 }

 package "MOD_Supervision" {
   artifact "monitor_live_calls" as F_MLC
   artifact "barge_in_calls" as F_BIC
   artifact "broadcast_team_messages" as F_BTM
 }

 package "MOD_Operator" {
   artifact "manage_own_agent_state" as F_MOAS
   artifact "answer_inbound_calls" as F_AIC
   artifact "make_outbound_calls" as F_MOC
   artifact "hold_calls" as F_HC
   artifact "transfer_calls" as F_TC
   artifact "enter_call_disposition" as F_ECD
   artifact "request_break" as F_RBK
   artifact "view_own_performance_dashboard" as F_VOPD
   artifact "view_own_call_history" as F_VOCH
   artifact "read_own_mailbox" as F_ROM
 }

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

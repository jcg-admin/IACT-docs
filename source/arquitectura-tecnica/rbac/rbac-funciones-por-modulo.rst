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
   artifact "view_all_active_sessions" as FUNCION_VER_SESIONES_ACTIVAS
 }

 package "MOD_Users" {
   artifact "create_users" as FUNCION_CREAR_USUARIOS
   artifact "list_users" as FUNCION_LISTAR_USUARIOS
   artifact "update_users" as FUNCION_ACTUALIZAR_USUARIOS
   artifact "deactivate_users" as FUNCION_DESACTIVAR_USUARIOS
 }

 package "MOD_Access / MOD_Permissions" {
   artifact "assign_functions" as FUNCION_ASIGNAR_FUNCIONES
   artifact "revoke_functions" as FUNCION_REVOCAR_FUNCIONES
   artifact "view_assignments" as FUNCION_VER_ASIGNACIONES
   artifact "assign_function_groups" as FUNCION_ASIGNAR_GRUPOS_FUNCION
   artifact "revoke_function_group" as FUNCION_REVOCAR_GRUPO_FUNCION
   artifact "create_function_group" as FUNCION_CREAR_GRUPO_FUNCION
   artifact "assign_functions_to_group" as FUNCION_ASIGNAR_FUNCIONES_A_GRUPO
   artifact "view_separation_rules" as FUNCION_VER_REGLAS_SOD
   artifact "view_audit_log" as FUNCION_VER_AUDITORIA
   artifact "view_own_navigation" as FUNCION_VER_NAVEGACION_PROPIA
 }

 package "MOD_Reports" {
   artifact "view_dashboard" as FUNCION_VER_DASHBOARD
   artifact "view_reports" as FUNCION_VER_REPORTES
   artifact "view_kpis" as FUNCION_VER_KPIS
   artifact "view_charts" as FUNCION_VER_GRAFICOS
   artifact "filter_reports" as FUNCION_FILTRAR_REPORTES
   artifact "export_csv" as FUNCION_EXPORTAR_CSV
   artifact "export_excel" as FUNCION_EXPORTAR_EXCEL
   artifact "export_pdf" as FUNCION_EXPORTAR_PDF
   artifact "schedule_report" as FUNCION_PROGRAMAR_REPORTE
   artifact "save_view" as FUNCION_GUARDAR_VISTA
   artifact "share_report" as FUNCION_COMPARTIR_REPORTE
 }

 package "MOD_Pipeline" {
   artifact "view_pipeline_status" as FUNCION_VER_ESTADO_ETL
   artifact "view_pipeline_errors" as FUNCION_VER_ERRORES_ETL
   artifact "view_data_availability" as FUNCION_VER_DISPONIBILIDAD_DATOS
   artifact "request_pipeline_retry" as FUNCION_REINTENTAR_ETL
 }

 package "MOD_Alerts" {
   artifact "configure_team_alerts" as FUNCION_CONFIGURAR_ALERTAS_EQUIPO
   artifact "view_alerts" as F_VAA2
   artifact "acknowledge_alert" as FUNCION_RECONOCER_ALERTA
   artifact "view_alert_history" as FUNCION_VER_HISTORIAL_ALERTAS
 }

 package "MOD_Audit / MOD_Logs" {
   artifact "view_audit_log" as FUNCION_VER_AUDITORIA
   artifact "search_audit_log" as FUNCION_BUSCAR_AUDITORIA
   artifact "export_audit_log" as FUNCION_EXPORTAR_AUDITORIA
   artifact "generate_compliance_report" as FUNCION_GENERAR_REPORTE_COMPLIANCE
   artifact "view_application_logs" as FUNCION_VER_LOGS_APLICACION
   artifact "view_etl_logs" as FUNCION_VER_LOGS_ETL
   artifact "search_logs" as FUNCION_BUSCAR_LOGS
   artifact "export_logs" as FUNCION_EXPORTAR_LOGS
   artifact "view_infrastructure_logs" as FUNCION_VER_LOGS_INFRAESTRUCTURA
   artifact "view_system_health" as FUNCION_VER_ESTADO_SISTEMA
   artifact "view_technical_metrics" as FUNCION_VER_METRICAS_TECNICAS
 }

 package "MOD_Supervision" {
   artifact "monitor_live_calls" as FUNCION_MONITOREAR_LLAMADAS_VIVO
   artifact "barge_in_calls" as FUNCION_INTERVENIR_LLAMADA
   artifact "broadcast_team_messages" as FUNCION_ENVIAR_MENSAJE_EQUIPO
 }

 package "MOD_Operator" {
   artifact "manage_own_agent_state" as FUNCION_GESTIONAR_ESTADO_AGENTE
   artifact "answer_inbound_calls" as FUNCION_ATENDER_LLAMADA
   artifact "make_outbound_calls" as FUNCION_LLAMADA_OUTBOUND
   artifact "hold_calls" as FUNCION_HOLD_LLAMADA
   artifact "transfer_calls" as FUNCION_TRANSFERIR_LLAMADA
   artifact "enter_call_disposition" as FUNCION_DISPOSICION_LLAMADA
   artifact "request_break" as FUNCION_SOLICITAR_BREAK
   artifact "view_own_performance_dashboard" as FUNCION_VER_DASHBOARD_DESEMPENO
   artifact "view_own_call_history" as FUNCION_VER_HISTORIAL_LLAMADAS_PROPIAS
   artifact "read_own_mailbox" as FUNCION_LEER_BUZON_PROPIO
 }

 @enduml

.. seealso::

 :doc:`/requisitos/casos-uso/index`
 :doc:`/arquitectura-tecnica/vistas-kruchten`

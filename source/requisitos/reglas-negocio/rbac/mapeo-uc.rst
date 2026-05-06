.. _modelo-rbac-iact-mapeo-uc:

=======================================
Modelo RBAC IACT — Mapeo Funciones UC
=======================================

10. MAPEO FUNCIONES → CASOS DE USO
==================================

.. note:: Scope del mapeo (v5.6.0)

 La tabla incluye las **64 funciones in-scope** de los 9 modulos
 activos. Las **13 funciones reservadas** de MOD_Operator y
 MOD_Supervision (extension points open-closed) se documentan
 en sus respectivos catalogos pero quedan fuera del mapeo
 operativo de esta release. Ver
 :doc:`/requisitos/reglas-negocio/rbac/catalogo-funciones` §3.9
 y §3.10.

10.1 Tabla Completa
-------------------



.. list-table::
 :widths: 33 33 33
 :header-rows: 1

 * - Función
   - Casos de Uso
   - Módulo
 * - view_own_sessions
   - UC-005
   - Auth
 * - close_user_session
   - UC-005
   - Auth
 * - reset_password
   - UC-003
   - Auth
 * - view_all_active_sessions
   - UC-005
   - Auth
 * - create_users
   - UC-006
   - Users
 * - update_users
   - UC-007
   - Users
 * - deactivate_users
   - UC-008
   - Users
 * - list_users
   - UC-009
   - Users
 * - search_users
   - UC-009
   - Users
 * - block_users
   - UC-007
   - Users
 * - unblock_users
   - UC-007
   - Users
 * - reactivate_users
   - UC-007
   - Users
 * - view_users
   - UC-009
   - Users
 * - assign_functions
   - UC-010, UC-042
   - Access
 * - revoke_functions
   - UC-010
   - Access
 * - view_assignments
   - UC-011, UC_ACC_03
   - Access
 * - assign_function_groups
   - UC-010
   - Access
 * - view_separation_rules
   - UC_ADM_01
   - Admin
 * - update_separation_rule
   - UC_ADM_01
   - Admin
 * - disable_separation_rule
   - UC_ADM_01
   - Admin
 * - view_pipeline_status
   - UC-050
   - Pipeline
 * - view_pipeline_errors
   - UC-051
   - Pipeline
 * - view_data_availability
   - UC-052
   - Pipeline
 * - request_pipeline_retry
   - UC-053
   - Pipeline
 * - view_reports
   - UC-017, UC-018, UC-019
   - Reports
 * - view_dashboard
   - UC-025
   - Reports
 * - filter_reports
   - UC-020, UC-021
   - Reports
 * - export_csv
   - UC-022
   - Reports
 * - export_excel
   - UC-023
   - Reports
 * - export_pdf
   - UC-024
   - Reports
 * - view_kpis
   - UC-025
   - Reports
 * - view_charts
   - UC-027, UC-028, UC-029
   - Reports
 * - view_alerts
   - UC-039
   - Alerts
 * - configure_alerts
   - UC-036
   - Alerts
 * - configure_team_alerts
   - UC-040
   - Alerts
 * - pause_alerts
   - UC-038
   - Alerts
 * - disable_alerts
   - UC-038
   - Alerts
 * - view_alert_history
   - UC-039
   - Alerts
 * - acknowledge_alert
   - uc-alr-03
   - Alerts
 * - subscribe_to_alert
   - uc-alr-05
   - Alerts
 * - unsubscribe_from_alert
   - uc-alr-05
   - Alerts
 * - configure_subscription_severity
   - uc-alr-05
   - Alerts
 * - view_audit_log
   - UC-061
   - Audit
 * - search_audit_log
   - UC-061
   - Audit
 * - export_audit_log
   - UC-063
   - Audit
 * - generate_compliance_report
   - UC-062
   - Audit
 * - view_application_logs
   - uc-log-01
   - Logs
 * - export_logs
   - uc-log-04
   - Logs
 * - search_logs
   - uc-log-03
   - Logs
 * - view_pipeline_logs
   - uc-log-02
   - Logs
 * - view_infrastructure_logs
   - uc-log-05
   - Logs
 * - view_system_health
   - uc-log-06
   - Logs
 * - view_technical_metrics
   - uc-log-07
   - Logs
 * - read_own_mailbox
   - UC_OPR_10
   - Operator


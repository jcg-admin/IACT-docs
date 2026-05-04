.. _raci-rbac-iact-modulo:

=================================
RACI RBAC IACT — RACI por Modulo
=================================

3. RACI por modulo (vista resumida)
===================================

3.1 MOD_Auth (4 funciones — autenticacion y sesiones)
-----------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``view_own_sessions``
   - I
   - C
   - R
   - A
   - I
   - I
 * - ``close_user_session``
   - C
   - R
   - R
   - A
   - I
   - —
 * - ``reset_password``
   - R
   - R
   - —
   - A
   - I
   - I
 * - ``view_all_active_sessions``
   - I
   - C
   - —
   - A
   - R
   - I

3.2 MOD_Users (9 funciones — gestion de identidades)
----------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``create_users``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``update_users``
   - R
   - C
   - —
   - A
   - I
   - —
 * - ``deactivate_users``
   - C
   - R
   - —
   - A
   - I
   - I
 * - ``list_users``
   - R
   - I
   - —
   - A
   - R
   - —
 * - ``search_users``
   - R
   - —
   - —
   - A
   - R
   - —
 * - ``block_users``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``unblock_users``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``reactivate_users``
   - R
   - C
   - —
   - A
   - I
   - —
 * - ``view_users``
   - R
   - —
   - —
   - A
   - R
   - —

3.3 MOD_Access (12 funciones — RBAC vista funcional + admin)
------------------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``assign_functions``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``revoke_functions``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``view_assignments``
   - R
   - I
   - —
   - A
   - R
   - —
 * - ``assign_function_groups``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``view_separation_rules``
   - C
   - R
   - —
   - A
   - C
   - I
 * - ``create_function_group`` (NUEVA v5.3.0)
   - I
   - R
   - —
   - A
   - C
   - I
 * - ``assign_functions_to_group`` (NUEVA v5.3.0)
   - I
   - R
   - —
   - A
   - C
   - I
 * - ``grant_exceptional_permission`` (NUEVA v5.3.0)
   - C
   - R
   - —
   - A
   - C
   - I
 * - ``revoke_exceptional_permission`` (NUEVA v5.3.0)
   - C
   - R
   - —
   - A
   - C
   - I
 * - ``revoke_function_group`` (NUEVA v5.3.0)
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``update_separation_rule`` (NUEVA v5.4.0)
   - I
   - R
   - —
   - A
   - C
   - I
 * - ``disable_separation_rule`` (NUEVA v5.4.0)
   - I
   - R
   - —
   - A
   - C
   - I

3.4 MOD_Pipeline (4 funciones — supervision ETL)
------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``view_pipeline_status``
   - I
   - I
   - R
   - A
   - I
   - —
 * - ``view_pipeline_errors``
   - —
   - I
   - R
   - A
   - I
   - —
 * - ``view_data_availability``
   - —
   - I
   - R
   - A
   - I
   - —
 * - ``request_pipeline_retry``
   - —
   - C
   - R
   - A
   - I
   - —

3.5 MOD_Reports (11 funciones — visualizacion y reportes)
---------------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``view_reports``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``view_dashboard``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``filter_reports``
   - R
   - —
   - R
   - A
   - I
   - —
 * - ``export_csv``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``export_excel``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``export_pdf``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``view_kpis``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``view_charts``
   - R
   - —
   - R
   - A
   - I
   - I
 * - ``schedule_report`` (NUEVA v5.3.0 — restaura ``programa_reportes`` v5.0_1/v5.1)
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``save_view`` (NUEVA v5.3.0)
   - R
   - —
   - R
   - A
   - I
   - —
 * - ``share_report`` (NUEVA v5.3.0 — restaura ``comparte_reportes`` v5.0_1/v5.1)
   - R
   - C
   - R
   - A
   - I
   - I

3.6 MOD_Alerts (10 funciones — alertas y notificaciones)
--------------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``view_alerts``
   - R
   - —
   - R
   - A
   - I
   - —
 * - ``configure_alerts``
   - R
   - C
   - C
   - A
   - I
   - I
 * - ``configure_team_alerts``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``pause_alerts``
   - R
   - I
   - —
   - A
   - I
   - —
 * - ``disable_alerts``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ``view_alert_history``
   - R
   - —
   - R
   - A
   - R
   - —
 * - ``acknowledge_alert`` (NUEVA v5.4.0)
   - R
   - C
   - R
   - A
   - I
   - I
 * - ``subscribe_to_alert`` (NUEVA v5.4.0)
   - R
   - C
   - R
   - A
   - I
   - —
 * - ``unsubscribe_from_alert`` (NUEVA v5.4.0)
   - R
   - C
   - R
   - A
   - I
   - —
 * - ``configure_subscription_severity`` (NUEVA v5.4.0)
   - R
   - C
   - —
   - A
   - I
   - —

3.7 MOD_Audit (4 funciones — auditoria funcional)
-------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``view_audit_log``
   - I
   - I
   - —
   - A
   - R
   - C
 * - ``search_audit_log``
   - I
   - I
   - —
   - A
   - R
   - C
 * - ``export_audit_log``
   - I
   - C
   - —
   - A
   - R
   - C
 * - ``generate_compliance_report``
   - I
   - I
   - —
   - A
   - R
   - C

3.8 MOD_Logs (7 funciones — bitacoras tecnicas + health + métricas)
-------------------------------------------------------------------

.. list-table::
 :header-rows: 1
 :widths: 8 12 10 10 10 10 10

 * - ID
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ``view_application_logs``
   - —
   - R
   - —
   - A
   - C
   - —
 * - ``export_logs``
   - —
   - R
   - —
   - A
   - C
   - I
 * - ``search_logs`` (NUEVA v5.3.0)
   - —
   - R
   - —
   - A
   - C
   - —
 * - ``view_etl_logs`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - C
   - —
 * - ``view_infrastructure_logs`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - C
   - —
 * - ``view_system_health`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - I
   - —
 * - ``view_technical_metrics`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - I
   - —


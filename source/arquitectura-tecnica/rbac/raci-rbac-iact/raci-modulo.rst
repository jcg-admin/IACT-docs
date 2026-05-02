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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - AUTH-001
   - ``view_own_sessions``
   - I
   - C
   - R
   - A
   - I
   - I
 * - AUTH-002
   - ``close_user_session``
   - C
   - R
   - R
   - A
   - I
   - —
 * - AUTH-003
   - ``reset_password``
   - R
   - R
   - —
   - A
   - I
   - I
 * - AUTH-004
   - ``view_all_active_sessions``
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - USR-001
   - ``create_users``
   - R
   - C
   - —
   - A
   - I
   - I
 * - USR-002
   - ``update_users``
   - R
   - C
   - —
   - A
   - I
   - —
 * - USR-003
   - ``deactivate_users``
   - C
   - R
   - —
   - A
   - I
   - I
 * - USR-004
   - ``list_users``
   - R
   - I
   - —
   - A
   - R
   - —
 * - USR-005
   - ``search_users``
   - R
   - —
   - —
   - A
   - R
   - —
 * - USR-006
   - ``block_users``
   - R
   - C
   - —
   - A
   - I
   - I
 * - USR-007
   - ``unblock_users``
   - R
   - C
   - —
   - A
   - I
   - I
 * - USR-008
   - ``reactivate_users``
   - R
   - C
   - —
   - A
   - I
   - —
 * - USR-009
   - ``view_users``
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ACC-001
   - ``assign_functions``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ACC-002
   - ``revoke_functions``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ACC-003
   - ``view_assignments``
   - R
   - I
   - —
   - A
   - R
   - —
 * - ACC-004
   - ``assign_function_groups``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ACC-005
   - ``view_separation_rules``
   - C
   - R
   - —
   - A
   - C
   - I
 * - ACC-006
   - ``create_function_group`` (NUEVA v5.3.0)
   - I
   - R
   - —
   - A
   - C
   - I
 * - ACC-007
   - ``assign_functions_to_group`` (NUEVA v5.3.0)
   - I
   - R
   - —
   - A
   - C
   - I
 * - ACC-008
   - ``grant_exceptional_permission`` (NUEVA v5.3.0)
   - C
   - R
   - —
   - A
   - C
   - I
 * - ACC-009
   - ``revoke_exceptional_permission`` (NUEVA v5.3.0)
   - C
   - R
   - —
   - A
   - C
   - I
 * - ACC-010
   - ``revoke_function_group`` (NUEVA v5.3.0)
   - R
   - C
   - —
   - A
   - I
   - I
 * - ACC-011
   - ``update_separation_rule`` (NUEVA v5.4.0)
   - I
   - R
   - —
   - A
   - C
   - I
 * - ACC-012
   - ``disable_separation_rule`` (NUEVA v5.4.0)
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - PIP-001
   - ``view_pipeline_status``
   - I
   - I
   - R
   - A
   - I
   - —
 * - PIP-002
   - ``view_pipeline_errors``
   - —
   - I
   - R
   - A
   - I
   - —
 * - PIP-003
   - ``view_data_availability``
   - —
   - I
   - R
   - A
   - I
   - —
 * - PIP-004
   - ``request_pipeline_retry``
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - RPT-001
   - ``view_reports``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-002
   - ``view_dashboard``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-003
   - ``filter_reports``
   - R
   - —
   - R
   - A
   - I
   - —
 * - RPT-004
   - ``export_csv``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-005
   - ``export_excel``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-006
   - ``export_pdf``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-007
   - ``view_kpis``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-008
   - ``view_charts``
   - R
   - —
   - R
   - A
   - I
   - I
 * - RPT-009
   - ``schedule_report`` (NUEVA v5.3.0 — restaura ``programa_reportes`` v5.0_1/v5.1)
   - R
   - C
   - —
   - A
   - I
   - I
 * - RPT-010
   - ``save_view`` (NUEVA v5.3.0)
   - R
   - —
   - R
   - A
   - I
   - —
 * - RPT-011
   - ``share_report`` (NUEVA v5.3.0 — restaura ``comparte_reportes`` v5.0_1/v5.1)
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - ALR-001
   - ``view_alerts``
   - R
   - —
   - R
   - A
   - I
   - —
 * - ALR-002
   - ``configure_alerts``
   - R
   - C
   - C
   - A
   - I
   - I
 * - ALR-003
   - ``configure_team_alerts``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ALR-004
   - ``pause_alerts``
   - R
   - I
   - —
   - A
   - I
   - —
 * - ALR-005
   - ``disable_alerts``
   - R
   - C
   - —
   - A
   - I
   - I
 * - ALR-006
   - ``view_alert_history``
   - R
   - —
   - R
   - A
   - R
   - —
 * - ALR-007
   - ``acknowledge_alert`` (NUEVA v5.4.0)
   - R
   - C
   - R
   - A
   - I
   - I
 * - ALR-008
   - ``subscribe_to_alert`` (NUEVA v5.4.0)
   - R
   - C
   - R
   - A
   - I
   - —
 * - ALR-009
   - ``unsubscribe_from_alert`` (NUEVA v5.4.0)
   - R
   - C
   - R
   - A
   - I
   - —
 * - ALR-010
   - ``configure_subscription_severity`` (NUEVA v5.4.0)
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - AUD-001
   - ``view_audit_log``
   - I
   - I
   - —
   - A
   - R
   - C
 * - AUD-002
   - ``search_audit_log``
   - I
   - I
   - —
   - A
   - R
   - C
 * - AUD-003
   - ``export_audit_log``
   - I
   - C
   - —
   - A
   - R
   - C
 * - AUD-004
   - ``generate_compliance_report``
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
 :widths: 8 30 12 10 10 10 10 10

 * - ID
   - Funcion
   - AdmNT
   - AdmT
   - Op
   - TLB
   - Aud
   - Comp
 * - LOG-001
   - ``view_application_logs``
   - —
   - R
   - —
   - A
   - C
   - —
 * - LOG-002
   - ``export_logs``
   - —
   - R
   - —
   - A
   - C
   - I
 * - LOG-003
   - ``search_logs`` (NUEVA v5.3.0)
   - —
   - R
   - —
   - A
   - C
   - —
 * - LOG-004
   - ``view_etl_logs`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - C
   - —
 * - LOG-005
   - ``view_infrastructure_logs`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - C
   - —
 * - LOG-006
   - ``view_system_health`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - I
   - —
 * - LOG-007
   - ``view_technical_metrics`` (NUEVA v5.4.0)
   - —
   - R
   - —
   - A
   - I
   - —


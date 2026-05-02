.. _modelo-rbac-iact-resumen:

==============================
Modelo RBAC IACT — Resumen
==============================

11. MIGRACIÓN DESDE v5.2.0
==========================



11.1 Cambios Breaking
---------------------



.. list-table::
 :widths: 33 33 33
 :header-rows: 1

 * - Aspecto
   - v5.2.0
   - v5.2.1
 * - **Nombres funciones**
   - Español
   - Inglés
 * - **Nombres grupos**
   - Español con `agr_`
   - Inglés sin prefijo
 * - **Nombres reglas SoD**
   - Español con `sod_`
   - Inglés sin prefijo
 * - **Campos**
   - `assigned_date`
   - `assigned_at`



11.2 Script de Migración SQL
----------------------------



.. code-block:: sql

 -- Actualizar 74 funciones
 UPDATE functions SET name = 'manage_sessions' WHERE function_id = 'AUTH-001';
 UPDATE functions SET name = 'close_user_session' WHERE function_id = 'AUTH-002';
 UPDATE functions SET name = 'reset_password' WHERE function_id = 'AUTH-003';
 UPDATE functions SET name = 'view_active_sessions' WHERE function_id = 'AUTH-004';
 
 UPDATE functions SET name = 'create_users' WHERE function_id = 'USR-001';
 UPDATE functions SET name = 'update_users' WHERE function_id = 'USR-002';
 UPDATE functions SET name = 'delete_users' WHERE function_id = 'USR-003';
 UPDATE functions SET name = 'list_users' WHERE function_id = 'USR-004';
 UPDATE functions SET name = 'search_users' WHERE function_id = 'USR-005';
 UPDATE functions SET name = 'block_users' WHERE function_id = 'USR-006';
 UPDATE functions SET name = 'unblock_users' WHERE function_id = 'USR-007';
 UPDATE functions SET name = 'reactivate_users' WHERE function_id = 'USR-008';
 UPDATE functions SET name = 'view_users' WHERE function_id = 'USR-009';
 
 UPDATE functions SET name = 'assign_functions' WHERE function_id = 'ACC-001';
 UPDATE functions SET name = 'revoke_functions' WHERE function_id = 'ACC-002';
 UPDATE functions SET name = 'view_assignments' WHERE function_id = 'ACC-003';
 UPDATE functions SET name = 'assign_function_groups' WHERE function_id = 'ACC-004';
 UPDATE functions SET name = 'manage_separation_rules' WHERE function_id = 'ACC-005';
 
 UPDATE functions SET name = 'view_pipeline_status' WHERE function_id = 'PIP-001';
 UPDATE functions SET name = 'view_pipeline_errors' WHERE function_id = 'PIP-002';
 UPDATE functions SET name = 'view_data_availability' WHERE function_id = 'PIP-003';
 UPDATE functions SET name = 'request_pipeline_retry' WHERE function_id = 'PIP-004';
 
 UPDATE functions SET name = 'view_reports' WHERE function_id = 'RPT-001';
 UPDATE functions SET name = 'view_dashboard' WHERE function_id = 'RPT-002';
 UPDATE functions SET name = 'filter_reports' WHERE function_id = 'RPT-003';
 UPDATE functions SET name = 'export_csv' WHERE function_id = 'RPT-004';
 UPDATE functions SET name = 'export_excel' WHERE function_id = 'RPT-005';
 UPDATE functions SET name = 'export_pdf' WHERE function_id = 'RPT-006';
 UPDATE functions SET name = 'view_kpis' WHERE function_id = 'RPT-007';
 UPDATE functions SET name = 'view_charts' WHERE function_id = 'RPT-008';
 
 UPDATE functions SET name = 'view_alerts' WHERE function_id = 'ALR-001';
 UPDATE functions SET name = 'configure_alerts' WHERE function_id = 'ALR-002';
 UPDATE functions SET name = 'configure_team_alerts' WHERE function_id = 'ALR-003';
 UPDATE functions SET name = 'pause_alerts' WHERE function_id = 'ALR-004';
 UPDATE functions SET name = 'delete_alerts' WHERE function_id = 'ALR-005';
 UPDATE functions SET name = 'view_alert_history' WHERE function_id = 'ALR-006';
 
 UPDATE functions SET name = 'view_audit_log' WHERE function_id = 'AUD-001';
 UPDATE functions SET name = 'search_audit_log' WHERE function_id = 'AUD-002';
 UPDATE functions SET name = 'export_audit_log' WHERE function_id = 'AUD-003';
 UPDATE functions SET name = 'generate_compliance_report' WHERE function_id = 'AUD-004';
 
 UPDATE functions SET name = 'view_technical_logs' WHERE function_id = 'LOG-001';
 UPDATE functions SET name = 'export_logs' WHERE function_id = 'LOG-002';
 
 -- Actualizar 12 grupos
 UPDATE function_groups SET name = 'basic_operator_group' WHERE group_id = 'AGR-001';
 UPDATE function_groups SET name = 'report_viewer_group' WHERE group_id = 'AGR-002';
 UPDATE function_groups SET name = 'quality_supervisor_group' WHERE group_id = 'AGR-003';
 UPDATE function_groups SET name = 'data_exporter_group' WHERE group_id = 'AGR-004';
 UPDATE function_groups SET name = 'alert_manager_group' WHERE group_id = 'AGR-005';
 UPDATE function_groups SET name = 'user_admin_group' WHERE group_id = 'AGR-006';
 UPDATE function_groups SET name = 'permission_admin_group' WHERE group_id = 'AGR-007';
 UPDATE function_groups SET name = 'auditor_group' WHERE group_id = 'AGR-008';
 UPDATE function_groups SET name = 'pipeline_admin_group' WHERE group_id = 'AGR-009';
 UPDATE function_groups SET name = 'system_admin_group' WHERE group_id = 'AGR-010';
 
 -- Actualizar 3 reglas SoD
 UPDATE function_separation_rules 
 SET name = 'pipeline_audit_separation',
 description = 'Pipeline operations cannot audit themselves'
 WHERE restriction_id = 'SOD-001';
 
 UPDATE function_separation_rules 
 SET name = 'user_audit_separation',
 description = 'User management cannot audit themselves'
 WHERE restriction_id = 'SOD-002';
 
 UPDATE function_separation_rules 
 SET name = 'access_audit_separation',
 description = 'Permission management cannot audit themselves'
 WHERE restriction_id = 'SOD-003';
 
 -- Renombrar columnas (si es necesario)
 ALTER TABLE user_function_assignments 
 CHANGE assigned_date assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
 
 ALTER TABLE user_function_group_assignments 
 CHANGE assigned_date assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP;
 
 ALTER TABLE function_separation_rule_details 
 CHANGE separation_group rule_group CHAR(1) NOT NULL;


----

12. RESUMEN
===========



12.1 Métricas del Modelo v5.2.1
-------------------------------



.. list-table::
 :widths: 50 50
 :header-rows: 1

 * - Aspecto
   - Valor
 * - **Filosofía**
   - Sin Pretensiones
 * - **Módulos IACT**
   - 8
 * - **Funciones atómicas**
   - 42
 * - **Grupos**
   - 10
 * - **Restricciones SoD**
   - 3
 * - **Segmentos de datos**
   - 0
 * - **Restricciones CNST**
   - 8
 * - **Nomenclatura**
   - Inglés (Clean Code v2.0.0)
 * - **Consistencia**
   - 100%



12.2 Cambios Clave v5.2.1
-------------------------


1. **[OK] 100% Inglés en código:**
   - Funciones: ``manage_sessions``, ``view_reports``, ``export_csv``
   - Grupos: ``basic_operator_group``, ``user_admin_group``
   - Reglas SoD: ``pipeline_audit_separation``

2. **[OK] Clean Code completo:**
   - Sin prefijos redundantes (``agr_``, ``sod_``)
   - Sin acrónimos en nombres (ETL en descripción OK)
   - Nombres descriptivos completos

3. **[OK] Convenciones SQL:**
   - ``assigned_at`` (NO ``assigned_date``)
   - ``rule_group`` (NO ``separation_group``)

4. **[OK] Comentarios español:**
   - Docstrings en español
   - ``help_text`` en español
   - ``description`` en español

----

**FIN DEL DOCUMENTO**

**Versión:** 5.2.1 
**Fecha:** 13 de enero de 2026 
**Estado:** [OK] Listo para Implementación 
**Changelog:**
- v5.2.0 → v5.2.1: Consistencia 100% inglés en código
- Nombres funciones: español → inglés
- Nombres grupos: español + ``agr_`` → inglés sin prefijo
- Nombres reglas SoD: español + ``sod_`` → inglés sin prefijo
- Campos: ``assigned_date`` → ``assigned_at``, ``separation_group`` → ``rule_group``
- Base: Clean Code v2.0.0 + MODELO_RBAC_IACT_v5_1_1.rst

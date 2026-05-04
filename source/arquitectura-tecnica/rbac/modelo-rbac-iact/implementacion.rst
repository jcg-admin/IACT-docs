.. _modelo-rbac-iact-implementacion:

====================================
Modelo RBAC IACT — Implementacion
====================================

8. IMPLEMENTACIÓN SQL
=====================



8.1 Tabla functions
-------------------



.. code-block:: sql

 CREATE TABLE functions (
 function_id VARCHAR(20) PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 description TEXT NOT NULL,
 category VARCHAR(50) NOT NULL,
 
 CONSTRAINT uk_function_name UNIQUE (name),
 CONSTRAINT chk_category CHECK (category IN (
 'auth', 'users', 'access', 'pipeline',
 'reports', 'alerts', 'audit', 'logs',
 'operator', 'supervisor'
 ))
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
 CREATE INDEX idx_function_category ON functions(category);



8.2 Tabla function_groups
-------------------------



.. code-block:: sql

 CREATE TABLE function_groups (
 group_id VARCHAR(20) PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 description TEXT NOT NULL,
 
 CONSTRAINT uk_group_name UNIQUE (name)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



8.3 Tabla function_group_membership
-----------------------------------



.. code-block:: sql

 CREATE TABLE function_group_membership (
 id INT AUTO_INCREMENT PRIMARY KEY,
 group_id VARCHAR(20) NOT NULL,
 function_id VARCHAR(20) NOT NULL,
 
 CONSTRAINT fk_fgm_group FOREIGN KEY (group_id)
 REFERENCES function_groups(group_id),
 CONSTRAINT fk_fgm_function FOREIGN KEY (function_id)
 REFERENCES functions(function_id),
 CONSTRAINT uk_group_function UNIQUE (group_id, function_id)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



8.4 Tabla user_function_assignments
-----------------------------------



.. code-block:: sql

 CREATE TABLE user_function_assignments (
 id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT NOT NULL,
 function_id VARCHAR(20) NOT NULL,
 assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 assigned_by INT NULL,
 justification TEXT,
 expiration_date DATE NULL,
 
 CONSTRAINT fk_ufa_user FOREIGN KEY (user_id)
 REFERENCES auth_user(id),
 CONSTRAINT fk_ufa_function FOREIGN KEY (function_id)
 REFERENCES functions(function_id),
 CONSTRAINT fk_ufa_assigned_by FOREIGN KEY (assigned_by)
 REFERENCES auth_user(id),
 CONSTRAINT uk_user_function UNIQUE (user_id, function_id),
 CONSTRAINT chk_justification_length 
 CHECK (justification IS NULL OR LENGTH(justification) >= 20),
 CONSTRAINT chk_expiration_date
 CHECK (expiration_date IS NULL OR 
 expiration_date <= DATE_ADD(assigned_at, INTERVAL 6 MONTH))
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
 CREATE INDEX idx_ufa_user ON user_function_assignments(user_id);
 CREATE INDEX idx_ufa_expiration ON user_function_assignments(expiration_date);


**CAMBIO v5.2.1:** ``assigned_at`` (NO ``assigned_date``, convención ``*_at`` para datetime)


8.5 Tabla user_function_group_assignments
-----------------------------------------



.. code-block:: sql

 CREATE TABLE user_function_group_assignments (
 id INT AUTO_INCREMENT PRIMARY KEY,
 user_id INT NOT NULL,
 group_id VARCHAR(20) NOT NULL,
 assigned_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
 assigned_by INT NULL,
 
 CONSTRAINT fk_ufga_user FOREIGN KEY (user_id)
 REFERENCES auth_user(id),
 CONSTRAINT fk_ufga_group FOREIGN KEY (group_id)
 REFERENCES function_groups(group_id),
 CONSTRAINT fk_ufga_assigned_by FOREIGN KEY (assigned_by)
 REFERENCES auth_user(id),
 CONSTRAINT uk_user_group UNIQUE (user_id, group_id)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
 
 CREATE INDEX idx_ufga_user ON user_function_group_assignments(user_id);


**CAMBIO v5.2.1:** ``assigned_at`` (convención datetime)


8.6 Tabla function_separation_rules
-----------------------------------



.. code-block:: sql

 CREATE TABLE function_separation_rules (
 restriction_id VARCHAR(20) PRIMARY KEY,
 name VARCHAR(100) NOT NULL,
 description TEXT NOT NULL,
 reason TEXT NOT NULL,
 cnst_reference VARCHAR(20) NOT NULL,
 active BOOLEAN NOT NULL DEFAULT TRUE,
 
 CONSTRAINT uk_sod_name UNIQUE (name)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;



8.7 Tabla function_separation_rule_details
------------------------------------------



.. code-block:: sql

 CREATE TABLE function_separation_rule_details (
 id INT AUTO_INCREMENT PRIMARY KEY,
 restriction_id VARCHAR(20) NOT NULL,
 function_id VARCHAR(20) NOT NULL,
 rule_group CHAR(1) NOT NULL,
 
 CONSTRAINT fk_fsrd_restriction FOREIGN KEY (restriction_id)
 REFERENCES function_separation_rules(restriction_id),
 CONSTRAINT fk_fsrd_function FOREIGN KEY (function_id)
 REFERENCES functions(function_id),
 CONSTRAINT chk_group CHECK (rule_group IN ('A', 'B')),
 CONSTRAINT uk_restriction_function UNIQUE (restriction_id, function_id)
 ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;


**CAMBIO v5.2.1:** ``rule_group`` (NO ``separation_group``, más conciso)


8.8 Datos Iniciales - 74 Funciones (v5.5.0)
-------------------------------------------



.. code-block:: sql

 -- MOD_Auth (4 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('AUTH-001', 'view_own_sessions', 'Ve sesiones activas propias del usuario', 'auth'),
 ('AUTH-002', 'close_user_session', 'Cierra sesión de otro usuario', 'auth'),
 ('AUTH-003', 'reset_password', 'Genera contraseña temporal', 'auth'),
 ('AUTH-004', 'view_all_active_sessions', 'Ve TODAS las sesiones activas del sistema (admin)', 'auth');

 -- MOD_Users (9 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('USR-001', 'create_users', 'Crea nuevos usuarios', 'users'),
 ('USR-002', 'update_users', 'Modifica datos de usuarios', 'users'),
 ('USR-003', 'deactivate_users', 'Baja lógica de usuarios (BR-009)', 'users'),
 ('USR-004', 'list_users', 'Lista usuarios con filtros', 'users'),
 ('USR-005', 'search_users', 'Busca usuarios por criterios', 'users'),
 ('USR-006', 'block_users', 'Bloquea acceso de usuario', 'users'),
 ('USR-007', 'unblock_users', 'Desbloquea usuario', 'users'),
 ('USR-008', 'reactivate_users', 'Reactiva usuario inactivo', 'users'),
 ('USR-009', 'view_users', 'Consulta información de usuarios', 'users');

 -- MOD_Access (12 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('ACC-001', 'assign_functions', 'Asigna funciones a usuarios', 'access'),
 ('ACC-002', 'revoke_functions', 'Revoca funciones de usuarios', 'access'),
 ('ACC-003', 'view_assignments', 'Ve asignaciones de funciones', 'access'),
 ('ACC-004', 'assign_function_groups', 'Asigna grupos de funciones', 'access'),
 ('ACC-005', 'view_separation_rules', 'Ve reglas SoD configuradas', 'access'),
 ('ACC-006', 'create_function_group', 'Crea grupo de funciones custom', 'access'),
 ('ACC-007', 'assign_functions_to_group', 'Asigna funciones a un grupo', 'access'),
 ('ACC-008', 'grant_exceptional_permission', 'Otorga permiso temporal excepcional (CNST-031)', 'access'),
 ('ACC-009', 'revoke_exceptional_permission', 'Revoca permiso excepcional', 'access'),
 ('ACC-010', 'revoke_function_group', 'Revoca grupo asignado', 'access'),
 ('ACC-011', 'update_separation_rule', 'Actualiza parámetros de regla SoD', 'access'),
 ('ACC-012', 'disable_separation_rule', 'Desactiva regla SoD (toggle on/off; BR-009)', 'access');

 -- MOD_Pipeline (4 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('PIP-001', 'view_pipeline_status', 'Ve estado actual del ETL', 'pipeline'),
 ('PIP-002', 'view_pipeline_errors', 'Consulta errores del ETL', 'pipeline'),
 ('PIP-003', 'view_data_availability', 'Ve disponibilidad de datos', 'pipeline'),
 ('PIP-004', 'request_pipeline_retry', 'Solicita reintento de ETL', 'pipeline');

 -- MOD_Reports (11 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('RPT-001', 'view_reports', 'Ve reportes tabulares', 'reports'),
 ('RPT-002', 'view_dashboard', 'Ve dashboard principal', 'reports'),
 ('RPT-003', 'filter_reports', 'Aplica filtros a reportes', 'reports'),
 ('RPT-004', 'export_csv', 'Exporta a CSV', 'reports'),
 ('RPT-005', 'export_excel', 'Exporta a Excel', 'reports'),
 ('RPT-006', 'export_pdf', 'Exporta a PDF', 'reports'),
 ('RPT-007', 'view_kpis', 'Ve KPIs estáticos', 'reports'),
 ('RPT-008', 'view_charts', 'Ve gráficos predefinidos', 'reports'),
 ('RPT-009', 'schedule_report', 'Programa generación automática de reportes', 'reports'),
 ('RPT-010', 'save_view', 'Persiste configuración de filtros como vista', 'reports'),
 ('RPT-011', 'share_report', 'Comparte reporte vía URL/buzón interno', 'reports');

 -- MOD_Alerts (10 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('ALR-001', 'view_alerts', 'Ve alertas propias', 'alerts'),
 ('ALR-002', 'configure_alerts', 'Configura alertas personales', 'alerts'),
 ('ALR-003', 'configure_team_alerts', 'Configura alertas de equipo', 'alerts'),
 ('ALR-004', 'pause_alerts', 'Pausa alertas temporalmente', 'alerts'),
 ('ALR-005', 'disable_alerts', 'Desactiva alerta (toggle on/off; BR-009)', 'alerts'),
 ('ALR-006', 'view_alert_history', 'Ve historial de alertas', 'alerts'),
 ('ALR-007', 'acknowledge_alert', 'Reconoce alerta (state transition)', 'alerts'),
 ('ALR-008', 'subscribe_to_alert', 'Suscribe usuario a tipo de alerta', 'alerts'),
 ('ALR-009', 'unsubscribe_from_alert', 'Desuscribe usuario de tipo de alerta', 'alerts'),
 ('ALR-010', 'configure_subscription_severity', 'Configura severidad mínima', 'alerts');

 -- MOD_Audit (4 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('AUD-001', 'view_audit_log', 'Ve registros de auditoría', 'audit'),
 ('AUD-002', 'search_audit_log', 'Busca en auditoría', 'audit'),
 ('AUD-003', 'export_audit_log', 'Exporta registros de auditoría', 'audit'),
 ('AUD-004', 'generate_compliance_report', 'Genera reporte de cumplimiento', 'audit');

 -- MOD_Logs (7 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('LOG-001', 'view_application_logs', 'Ve logs de aplicación (errores 500, INFO/WARN/ERROR)', 'logs'),
 ('LOG-002', 'export_logs', 'Exporta paquete de logs', 'logs'),
 ('LOG-003', 'search_logs', 'Busca logs por criterios', 'logs'),
 ('LOG-004', 'view_etl_logs', 'Ve logs del proceso ETL (sync IVR→Analytics)', 'logs'),
 ('LOG-005', 'view_infrastructure_logs', 'Ve logs de infraestructura (timeouts, up/down)', 'logs'),
 ('LOG-006', 'view_system_health', 'Ve estado de salud del sistema y servicios', 'logs'),
 ('LOG-007', 'view_technical_metrics', 'Ve métricas técnicas agregadas (CPU, memoria)', 'logs');

 -- MOD_Operator (10 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('OPR-001', 'manage_own_agent_state', 'Cambia propio estado de disponibilidad (available/busy/break/offline)', 'operator'),
 ('OPR-002', 'answer_inbound_calls', 'Atiende llamada entrante asignada por el enrutador', 'operator'),
 ('OPR-003', 'make_outbound_calls', 'Realiza llamada saliente autorizada', 'operator'),
 ('OPR-004', 'hold_calls', 'Pone en espera o retoma llamada activa', 'operator'),
 ('OPR-005', 'transfer_calls', 'Transfiere llamada a otro agente o cola', 'operator'),
 ('OPR-006', 'enter_call_disposition', 'Registra resultado de la llamada (disposition code)', 'operator'),
 ('OPR-007', 'request_break', 'Solicita pausa autorizada (break/lunch/training)', 'operator'),
 ('OPR-008', 'view_own_performance_dashboard', 'Consulta propio dashboard de métricas de desempeño', 'operator'),
 ('OPR-009', 'view_own_call_history', 'Consulta historial personal de llamadas atendidas/realizadas', 'operator'),
 ('OPR-010', 'read_own_mailbox', 'Consulta el buzón de mensajes internos del agente (InternalMailbox)', 'operator');

 -- MOD_Supervision (3 funciones)
 INSERT INTO functions (function_id, name, description, category) VALUES
 ('SUP-001', 'monitor_live_calls', 'Escucha llamada activa en modo silent o whisper', 'supervisor'),
 ('SUP-002', 'barge_in_calls', 'Interviene en llamada activa habilitando canal tripartito', 'supervisor'),
 ('SUP-003', 'broadcast_team_messages', 'Envía mensaje de texto a todos los agentes del equipo', 'supervisor');



8.9 Datos Iniciales - 12 Grupos
-------------------------------



.. code-block:: sql

 INSERT INTO function_groups (group_id, name, description) VALUES
 ('AGR-001', 'basic_operator_group', 'Visualización básica de reportes y dashboard'),
 ('AGR-002', 'report_viewer_group', 'Análisis de reportes con filtros'),
 ('AGR-003', 'quality_supervisor_group', 'Supervisión con alertas'),
 ('AGR-004', 'data_exporter_group', 'Exportación autorizada de datos'),
 ('AGR-005', 'alert_manager_group', 'Gestión completa de alertas'),
 ('AGR-006', 'user_admin_group', 'Administración de usuarios'),
 ('AGR-007', 'permission_admin_group', 'Administración de permisos RBAC'),
 ('AGR-008', 'auditor_group', 'Auditoría y compliance'),
 ('AGR-009', 'pipeline_admin_group', 'Administración del ETL'),
 ('AGR-010', 'system_admin_group', 'Administración técnica del sistema'),
 ('AGR-011', 'call_center_operator_group', 'Operador de call center — funciones OPR-001..010'),
 ('AGR-012', 'call_center_supervisor_group', 'Supervisor de call center — SUP-001..003 + quality_supervisor_group');



8.10 Datos Iniciales - 3 Reglas SoD
-----------------------------------



.. code-block:: sql

 -- Insertar restricciones SoD
 INSERT INTO function_separation_rules 
 (restriction_id, name, description, reason, cnst_reference) VALUES
 ('SOD-001', 'pipeline_audit_separation', 
 'Pipeline operations cannot audit themselves', 
 'Evitar que quien opera el ETL audite sus propias acciones', 
 'CNST-005'),
 ('SOD-002', 'user_audit_separation', 
 'User management cannot audit themselves', 
 'Evitar que quien administra usuarios vea auditoría de sus acciones', 
 'CNST-005'),
 ('SOD-003', 'access_audit_separation', 
 'Permission management cannot audit themselves', 
 'Separación de poderes entre asignación y auditoría', 
 'CNST-005');
 
 -- SOD-001 detalles
 INSERT INTO function_separation_rule_details 
 (restriction_id, function_id, rule_group) VALUES
 ('SOD-001', 'PIP-001', 'A'),
 ('SOD-001', 'PIP-002', 'A'),
 ('SOD-001', 'PIP-003', 'A'),
 ('SOD-001', 'PIP-004', 'A'),
 ('SOD-001', 'AUD-001', 'B'),
 ('SOD-001', 'AUD-002', 'B'),
 ('SOD-001', 'AUD-003', 'B'),
 ('SOD-001', 'AUD-004', 'B');
 
 -- SOD-002 detalles
 INSERT INTO function_separation_rule_details 
 (restriction_id, function_id, rule_group) VALUES
 ('SOD-002', 'USR-001', 'A'),
 ('SOD-002', 'USR-003', 'A'),
 ('SOD-002', 'USR-004', 'A'),
 ('SOD-002', 'USR-007', 'A'),
 ('SOD-002', 'AUD-001', 'B'),
 ('SOD-002', 'AUD-002', 'B'),
 ('SOD-002', 'AUD-003', 'B');
 
 -- SOD-003 detalles
 INSERT INTO function_separation_rule_details 
 (restriction_id, function_id, rule_group) VALUES
 ('SOD-003', 'ACC-001', 'A'),
 ('SOD-003', 'ACC-002', 'A'),
 ('SOD-003', 'ACC-005', 'A'),
 ('SOD-003', 'AUD-001', 'B'),
 ('SOD-003', 'AUD-002', 'B');


----


9. IMPLEMENTACIÓN DJANGO
========================



9.1 Models (appsaccessmodels.py)
--------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
9.2 Service (appsaccessservices.py)
-----------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
9.3 Decorator (appsaccessdecorators.py)
---------------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
9.4 Middleware (appsaccessmiddleware.py)
----------------------------------------



.. note::

 Los detalles de implementacion de este componente estan en el
 repositorio de codigo fuente. Esta especificacion describe el
 comportamiento esperado, no la implementacion concreta.
9.5 Management Command
----------------------



.. code-block:: bash

 # Inicializar RBAC v5.2.1
 python manage.py initialize_permissions
 
 # O paso a paso:
 python manage.py initialize_functions # 74 funciones
 python manage.py initialize_function_groups # 12 grupos
 python manage.py initialize_separation_rules # 3 reglas SoD


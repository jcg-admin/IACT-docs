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
 'reports', 'alerts', 'audit', 'logs'
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


8.8 Datos Iniciales - 61 Funciones (v5.4.0)
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



8.9 Datos Iniciales - 10 Grupos
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
 ('AGR-010', 'system_admin_group', 'Administración técnica del sistema');



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



.. code-block:: python

 """
 Modelos de control de acceso RBAC v5.2.1
 Sistema IACT - 42 funciones atómicas
 """
 from django.db import models
 from django.contrib.auth import get_user_model
 
 User = get_user_model
 
 
 class Function(models.Model):
 """
 Función atómica del sistema (42 funciones).
 
 Una función representa una capacidad específica que puede 
 realizar un usuario. Ejemplos:
 - view_reports
 - export_csv
 - create_users
 """
   function_id = models.CharField(
   max_length=20,
   unique=True,
   help_text="Identificador único (AUTH-001, USR-001, etc.)"
   )
   name = models.CharField(
   max_length=100,
   help_text="Nombre descriptivo (view_reports, export_csv, create_users)"
   )
   description = models.TextField(
   help_text="Descripción de qué hace la función"
   )
   category = models.CharField(
   max_length=50,
   choices=[
   ('auth', 'Autenticación'),
   ('users', 'Usuarios'),
   ('access', 'Acceso'),
   ('pipeline', 'Pipeline'),
   ('reports', 'Reportes'),
   ('alerts', 'Alertas'),
   ('audit', 'Auditoría'),
   ('logs', 'Logs'),
   ],
   help_text="Módulo al que pertenece"
   )
 
 class Meta:
 db_table = 'functions'
 verbose_name = 'Función'
 verbose_name_plural = 'Funciones'
 ordering = ['function_id']
 
 def __str__(self):
 return f"{self.function_id}: {self.name}"
 
 
 class FunctionGroup(models.Model):
 """
 Grupo de funciones que se asignan juntas (10 grupos).
 
 Un grupo agrupa múltiples funciones relacionadas. Ejemplos:
 - basic_operator_group (view_reports + view_dashboard)
 - user_admin_group (create + update + delete users)
 """
   group_id = models.CharField(
   max_length=20,
   unique=True,
   help_text="Identificador único (AGR-001 a AGR-010)"
   )
   name = models.CharField(
   max_length=100,
   help_text="Nombre del grupo (basic_operator_group, user_admin_group)"
   )
   description = models.TextField(
   help_text="Descripción del grupo"
   )
   functions = models.ManyToManyField(
   Function,
   through='FunctionGroupMembership',
   related_name='groups',
   help_text="Funciones incluidas en este grupo"
   )
 
 class Meta:
 db_table = 'function_groups'
 verbose_name = 'Grupo de Funciones'
 verbose_name_plural = 'Grupos de Funciones'
 ordering = ['group_id']
 
 def __str__(self):
 return f"{self.group_id}: {self.name}"
 
 
 class FunctionGroupMembership(models.Model):
 """Pertenencia de una función a un grupo (tabla intermedia M2M)."""
 group = models.ForeignKey(
 FunctionGroup,
 on_delete=models.CASCADE,
 help_text="Grupo de funciones"
 )
 function = models.ForeignKey(
 Function,
 on_delete=models.CASCADE,
 help_text="Función que pertenece al grupo"
 )
 
 class Meta:
 db_table = 'function_group_membership'
 unique_together = [['group', 'function']]
 verbose_name = 'Pertenencia a Grupo'
 verbose_name_plural = 'Pertenencias a Grupos'
 
 
 class UserFunctionAssignment(models.Model):
 """
 Asignación directa de una función a un usuario.
 
 Tiene MAYOR precedencia que los grupos.
 Puede ser permanente o temporal (con vencimiento máx 6 meses).
 """
 user = models.ForeignKey(
 User,
 on_delete=models.CASCADE,
 related_name='function_assignments',
 help_text="Usuario al que se asigna la función"
 )
 function = models.ForeignKey(
 Function,
 on_delete=models.CASCADE,
 help_text="Función asignada"
 )
 assigned_at = models.DateTimeField(
 auto_now_add=True,
 help_text="Fecha y hora de asignación"
 )
 assigned_by = models.ForeignKey(
 User,
 on_delete=models.SET_NULL,
 null=True,
 related_name='functions_assigned_by_me',
 help_text="Usuario que realizó la asignación"
 )
 justification = models.TextField(
 blank=True,
 help_text="Justificación obligatoria si es temporal (mín 20 caracteres)"
 )
 expiration_date = models.DateField(
 null=True,
 blank=True,
 help_text="Fecha de vencimiento (máx 6 meses desde asignación)"
 )
 
 class Meta:
 db_table = 'user_function_assignments'
 unique_together = [['user', 'function']]
 verbose_name = 'Asignación de Función'
 verbose_name_plural = 'Asignaciones de Funciones'
 ordering = ['-assigned_at']
 
 def __str__(self):
 return f"{self.user.username} → {self.function.function_id}"
 
 
 class UserFunctionGroupAssignment(models.Model):
 """
 Asignación de un grupo de funciones a un usuario.
 
 El usuario obtiene automáticamente TODAS las funciones del grupo.
 Tiene MENOR precedencia que las asignaciones directas.
 """
 user = models.ForeignKey(
 User,
 on_delete=models.CASCADE,
 related_name='group_assignments',
 help_text="Usuario al que se asigna el grupo"
 )
 group = models.ForeignKey(
 FunctionGroup,
 on_delete=models.CASCADE,
 help_text="Grupo de funciones asignado"
 )
 assigned_at = models.DateTimeField(
 auto_now_add=True,
 help_text="Fecha y hora de asignación"
 )
 assigned_by = models.ForeignKey(
 User,
 on_delete=models.SET_NULL,
 null=True,
 related_name='groups_assigned_by_me',
 help_text="Usuario que realizó la asignación"
 )
 
 class Meta:
 db_table = 'user_function_group_assignments'
 unique_together = [['user', 'group']]
 verbose_name = 'Asignación de Grupo'
 verbose_name_plural = 'Asignaciones de Grupos'
 ordering = ['-assigned_at']
 
 def __str__(self):
 return f"{self.user.username} → {self.group.group_id}"
 
 
 class FunctionSeparationRule(models.Model):
 """
 Regla que define funciones que NO pueden coexistir (3 reglas).
 
 Un usuario NO puede tener simultáneamente funciones de 
 ambos grupos (A y B) de la misma regla.
 
 Ejemplo: pipeline_audit_separation
 - Grupo A: Funciones de pipeline (PIP-001 a PIP-004)
 - Grupo B: Funciones de auditoría (AUD-001 a AUD-004)
 """
   restriction_id = models.CharField(
   max_length=20,
   unique=True,
   help_text="Identificador único (SOD-001, SOD-002, SOD-003)"
   )
   name = models.CharField(
   max_length=100,
   help_text="Nombre de la regla (pipeline_audit_separation)"
   )
   description = models.TextField(
   help_text="Descripción de la restricción"
   )
   reason = models.TextField(
   help_text="Razón de negocio para la separación"
   )
   cnst_reference = models.CharField(
   max_length=20,
   help_text="Restricción CNST relacionada (CNST-005)"
   )
   active = models.BooleanField(
   default=True,
   help_text="Si la regla está activa"
   )
 
 class Meta:
 db_table = 'function_separation_rules'
 verbose_name = 'Regla de Separación de Funciones'
 verbose_name_plural = 'Reglas de Separación de Funciones'
 ordering = ['restriction_id']
 
 def __str__(self):
 return f"{self.restriction_id}: {self.name}"
 
 
 class FunctionSeparationRuleDetail(models.Model):
 """
 Detalle de una regla de separación.
 
 Define qué función pertenece a qué grupo (A o B) 
 dentro de una regla de separación.
 """
 rule = models.ForeignKey(
 FunctionSeparationRule,
 on_delete=models.CASCADE,
 related_name='details',
 help_text="Regla a la que pertenece"
 )
 function = models.ForeignKey(
 Function,
 on_delete=models.CASCADE,
 help_text="Función incluida en la regla"
 )
 rule_group = models.CharField(
 max_length=1,
 choices=[
 ('A', 'Grupo A'),
 ('B', 'Grupo B')
 ],
 help_text="Grupo al que pertenece la función en esta regla"
 )
 
 class Meta:
 db_table = 'function_separation_rule_details'
 unique_together = [['rule', 'function']]
 verbose_name = 'Detalle de Regla de Separación'
 verbose_name_plural = 'Detalles de Reglas de Separación'
 
 def __str__(self):
 return f"{self.rule.restriction_id} - {self.function.function_id} (Grupo {self.rule_group})"



9.2 Service (appsaccessservices.py)
-----------------------------------



.. code-block:: python

 """
 Servicio de permisos RBAC v5.2.1
 """
 from typing import Set, Tuple
 from django.contrib.auth import get_user_model
 from django.core.exceptions import ValidationError
 from django.utils import timezone
 from .models import (
 Function,
 FunctionGroup,
 UserFunctionAssignment,
 UserFunctionGroupAssignment,
 FunctionSeparationRule,
 FunctionSeparationRuleDetail,
 )
 
 User = get_user_model
 
 
 class PermissionService:
 """
 Servicio para gestión de permisos (RBAC v5.2.1).
 
 Clean Code v2.0.0:
 - Nombre descriptivo (NO "RBACService")
 - Métodos en inglés
 - Comentarios en español
 """
 
 def __init__(self, request_user: User = None):
 """
 Inicializa el servicio.
 
 Args:
 request_user: Usuario que realiza la operación
 """
 self.request_user = request_user
 
 def calculate_effective_functions(self, user: User) -> Set[str]:
 """
 Calcula funciones efectivas de un usuario.
 
 Precedencia:
 1. Funciones directas (UserFunctionAssignment)
 2. Funciones de grupos (UserFunctionGroupAssignment)
 
 Args:
 user: Usuario para calcular funciones
 
 Returns:
 Set of function_id: {'RPT-001', 'RPT-002', ...}
 """
 functions = set
 
 # 1. Funciones directas (mayor precedencia)
 direct_assignments = UserFunctionAssignment.objects.filter(
 user=user,
 ).select_related('function')
 
 for assignment in direct_assignments:
 # Validar vencimiento
 if assignment.expiration_date:
 if assignment.expiration_date >= timezone.now.date:
 functions.add(assignment.function.function_id)
 else:
 functions.add(assignment.function.function_id)
 
 # 2. Funciones de grupos (menor precedencia)
 group_assignments = UserFunctionGroupAssignment.objects.filter(
 user=user
 ).prefetch_related('group__functions')
 
 for assignment in group_assignments:
 functions.update(
 f.function_id 
 for f in assignment.group.functions.all
 )
 
 return functions
 
 def validate_separation_rules(
 self,
 user: User,
 new_function_id: str
 ) -> Tuple[bool, str]:
 """
 Valida reglas SoD antes de asignar función.
 
 Args:
 user: Usuario
 new_function_id: ID de función a asignar (ej: 'RPT-001')
 
 Returns:
 (valid, error_message)
 """
 current_functions = self.calculate_effective_functions(user)
 
 # Obtener reglas SoD activas
 active_rules = FunctionSeparationRule.objects.filter(
 active=True
 )
 
 for rule in active_rules:
 # Obtener funciones de grupos A y B
 details = FunctionSeparationRuleDetail.objects.filter(
 rule=rule
 ).select_related('function')
 
 group_a = set(
 d.function.function_id 
 for d in details 
 if d.rule_group == 'A'
 )
 group_b = set(
 d.function.function_id 
 for d in details 
 if d.rule_group == 'B'
 )
 
 # Validar conflicto
 if new_function_id in group_a:
 if current_functions & group_b:
 return False, (
 f"Violación SoD: {rule.name}. "
 f"Razón: {rule.reason}"
 )
 
 if new_function_id in group_b:
 if current_functions & group_a:
 return False, (
 f"Violación SoD: {rule.name}. "
 f"Razón: {rule.reason}"
 )
 
 return True, ""
 
 def assign_function_group(
 self,
 user: User,
 group_id: str,
 assigned_by: User
 ) -> UserFunctionGroupAssignment:
 """
 Asigna grupo de funciones a usuario validando SoD.
 
 Args:
 user: Usuario destino
 group_id: ID del grupo (ej: 'AGR-001')
 assigned_by: Usuario que asigna
 
 Returns:
 Asignación creada
 
 Raises:
 ValidationError: Si viola SoD
 """
 group = FunctionGroup.objects.get(group_id=group_id)
 
 # Validar SoD para cada función del grupo
 for function in group.functions.all:
 valid, message = self.validate_separation_rules(
 user,
 function.function_id
 )
 if not valid:
 raise ValidationError(message)
 
 # Asignar grupo
 assignment = UserFunctionGroupAssignment.objects.create(
 user=user,
 group=group,
 assigned_by=assigned_by
 )
 
 # Auditar (CNST-009)
 from apps.audit.services import AuditService
 AuditService.record_action(
 user=assigned_by,
 action='ASSIGN_FUNCTION_GROUP',
 resource_type='User',
 resource_id=str(user.id),
 details={
 'group_id': group_id,
 'group_name': group.name
 }
 )
 
 return assignment



9.3 Decorator (appsaccessdecorators.py)
---------------------------------------



.. code-block:: python

 """
 Decoradores para control de acceso RBAC v5.2.1
 """
 from functools import wraps
 from django.core.exceptions import PermissionDenied
 
 
 def require_function(*required_function_ids):
 """
 Decorator que valida función RBAC.
 
 El usuario debe tener AL MENOS UNA de las funciones requeridas.
 
 Args:
 *required_function_ids: IDs de funciones requeridas
 
 Uso:
 @require_function('RPT-001') # view_reports
 def list_reports(request):
 ...
 
 CNST-009: Audita intentos de acceso denegado.
 """
 def decorator(view_func):
 @wraps(view_func)
 def wrapper(request, *args, **kwargs):
 # Validar autenticación
 if not request.user.is_authenticated:
 raise PermissionDenied("Usuario no autenticado")
 
 # Obtener funciones del usuario
 user_functions = getattr(request, 'user_functions', set)
 
 # Validar si tiene alguna función requerida
 has_permission = any(
 fid in user_functions 
 for fid in required_function_ids
 )
 
 if not has_permission:
 # Auditar acceso denegado
 from apps.audit.services import AuditService
 AuditService.record_action(
 user=request.user,
 action='ACCESS_DENIED',
 resource_type='Endpoint',
 resource_id=request.path,
 result='FAIL',
 details={
 'required_functions': list(required_function_ids),
 'user_functions': list(user_functions)
 }
 )
 
 raise PermissionDenied(
 f"Requiere una de: {', '.join(required_function_ids)}"
 )
 
 return view_func(request, *args, **kwargs)
 
 return wrapper
 return decorator



9.4 Middleware (appsaccessmiddleware.py)
----------------------------------------



.. code-block:: python

 """
 Middleware de permisos RBAC v5.2.1
 """
 from django.utils.deprecation import MiddlewareMixin
 from .services import PermissionService
 
 
 class PermissionMiddleware(MiddlewareMixin):
 """
 Middleware que inyecta funciones efectivas en cada request.
 
 Inyecta `request.user_functions` con las funciones del usuario.
 
 CNST-002: Valida sesión única por usuario.
 """
 
 def __init__(self, get_response):
 """Inicializa el middleware."""
 self.get_response = get_response
 self.permission_service = PermissionService
 
 def __call__(self, request):
 """
 Procesa el request.
 
 Args:
 request: HttpRequest
 
 Returns:
 HttpResponse
 """
 if request.user.is_authenticated:
 # Calcular funciones efectivas
 request.user_functions = (
 self.permission_service.calculate_effective_functions(
 request.user
 )
 )
 
 # CNST-002: Validar sesión única
 self._validate_single_session(request)
 else:
 request.user_functions = set
 
 response = self.get_response(request)
 return response
 
 def _validate_single_session(self, request):
 """
 CNST-002: Solo una sesión activa por usuario.
 
 Si detecta sesión duplicada, invalida la anterior.
 """
 from django.contrib.sessions.models import Session
 from django.utils import timezone
 
 current_session_key = request.session.session_key
 
 # Buscar otras sesiones del mismo usuario
 active_sessions = Session.objects.filter(
 expire_date__gte=timezone.now
 )
 
 for session in active_sessions:
 data = session.get_decoded
 session_user_id = data.get('_auth_user_id')
 
 if session_user_id == str(request.user.id):
 if session.session_key != current_session_key:
 # Invalidar sesión anterior
 session.delete



9.5 Management Command
----------------------



.. code-block:: bash

 # Inicializar RBAC v5.2.1
 python manage.py initialize_permissions
 
 # O paso a paso:
 python manage.py initialize_functions # 42 funciones
 python manage.py initialize_function_groups # 10 grupos
 python manage.py initialize_separation_rules # 3 reglas SoD


----

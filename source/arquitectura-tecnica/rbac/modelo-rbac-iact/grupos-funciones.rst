.. _modelo-rbac-iact-grupos:

=======================================
Modelo RBAC IACT — Grupos de Funciones
=======================================

4. LOS 10 GRUPOS DE FUNCIONES
=============================



4.1 Catálogo de Grupos
----------------------



.. list-table::
 :widths: 20 20 20 20 20
 :header-rows: 1

 * - ID
   - Nombre
   - Funciones
   - Actor Típico
   - Descripción
 * - **AGR-001**
   - `basic_operator_group`
   - 6
   - Operador
   - Visualización básica
 * - **AGR-002**
   - `report_viewer_group`
   - 8
   - Analista
   - Análisis sin exportación
 * - **AGR-003**
   - `quality_supervisor_group`
   - 11
   - Supervisor
   - Análisis + filtros avanzados
 * - **AGR-004**
   - `data_exporter_group`
   - 14
   - Data Analyst
   - Exportación autorizada
 * - **AGR-005**
   - `alert_manager_group`
   - 6
   - Gestor Alertas
   - Gestión completa alertas
 * - **AGR-006**
   - `user_admin_group`
   - 9
   - Admin Usuarios
   - Gestión de identidades
 * - **AGR-007**
   - `permission_admin_group`
   - 5
   - Admin Permisos
   - Gestión RBAC
 * - **AGR-008**
   - `auditor_group`
   - 4
   - Auditor
   - Solo auditoría (SoD)
 * - **AGR-009**
   - `pipeline_admin_group`
   - 4
   - Admin Pipeline
   - Supervisión ETL
 * - **AGR-010**
   - `system_admin_group`
   - 6
   - Sysadmin
   - Administración completa


**CAMBIO v5.2.1:**
- Todos los nombres en inglés
- Sin prefijo redundante ``agr_``
- Sufijo ``_group`` explícito


4.2 Detalle de Grupos
---------------------



AGR-001 basic_operator_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (6):**

.. code-block:: text

 AUTH-001: manage_sessions (propias)
 AUTH-004: view_active_sessions (propias)
 RPT-001: view_reports
 RPT-002: view_dashboard
 RPT-007: view_kpis
 RPT-008: view_charts


**Propósito:** Usuario básico que solo visualiza información.

----

AGR-002 report_viewer_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (8):**

.. code-block:: text

 Todas de AGR-001 +
 RPT-003: filter_reports
 USR-009: view_users


**Propósito:** Analista que puede aplicar filtros pero no exportar.

----

AGR-003 quality_supervisor_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (11):**

.. code-block:: text

 Todas de AGR-002 +
 ALR-001: view_alerts
 ALR-002: configure_alerts
 ALR-006: view_alert_history


**Propósito:** Supervisor con capacidad de configurar alertas propias.

----

AGR-004 data_exporter_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (14):**

.. code-block:: text

 Todas de AGR-003 +
 RPT-004: export_csv
 RPT-005: export_excel
 RPT-006: export_pdf


**Propósito:** Analista autorizado para exportar con límites CNST-007.

----

AGR-005 alert_manager_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (6):**

.. code-block:: text

 ALR-001: view_alerts
 ALR-002: configure_alerts
 ALR-003: configure_team_alerts
 ALR-004: pause_alerts
 ALR-005: delete_alerts
 ALR-006: view_alert_history


**Propósito:** Gestor de alertas de equipo/departamento.

----

AGR-006 user_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (9):**

.. code-block:: text

 USR-001: create_users
 USR-002: update_users
 USR-003: delete_users
 USR-004: list_users
 USR-005: search_users
 USR-006: block_users
 USR-007: unblock_users
 USR-008: reactivate_users
 USR-009: view_users


**Propósito:** Administración completa de identidades.

**SoD:** NO puede tener funciones de AGR-008 (auditoría).

----

AGR-007 permission_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (5):**

.. code-block:: text

 ACC-001: assign_functions
 ACC-002: revoke_functions
 ACC-003: view_assignments
 ACC-004: assign_function_groups
 ACC-005: manage_separation_rules


**Propósito:** Administración de RBAC.

**SoD:** NO puede tener funciones de AGR-008 (auditoría).

----

AGR-008 auditor_group
^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (4):**

.. code-block:: text

 AUD-001: view_audit_log
 AUD-002: search_audit_log
 AUD-003: export_audit_log
 AUD-004: generate_compliance_report


**Propósito:** Auditoría y compliance.

**SoD CRÍTICA:** NO puede combinarse con:
- AGR-006 (user_admin_group)
- AGR-007 (permission_admin_group)
- AGR-009 (pipeline_admin_group)

----

AGR-009 pipeline_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (4):**

.. code-block:: text

 PIP-001: view_pipeline_status
 PIP-002: view_pipeline_errors
 PIP-003: view_data_availability
 PIP-004: request_pipeline_retry


**Propósito:** Administración de ETL.

**SoD:** NO puede tener funciones de AGR-008 (auditoría).

----

AGR-010 system_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (6):**

.. code-block:: text

 AUTH-001: manage_sessions (de todos)
 AUTH-002: close_user_session
 AUTH-003: reset_password
 AUTH-004: view_active_sessions
 LOG-001: view_technical_logs
 LOG-002: export_logs


**Propósito:** Administración técnica del sistema.


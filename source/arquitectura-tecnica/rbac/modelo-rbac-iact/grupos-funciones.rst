.. _modelo-rbac-iact-grupos:

=======================================
Modelo RBAC IACT — Grupos de Funciones
=======================================

4. LOS 12 GRUPOS DE FUNCIONES
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
 * - **AGR-011**
   - `call_center_operator_group`
   - 9
   - Agente
   - Acciones operativas del agente de call center
 * - **AGR-012**
   - `call_center_supervisor_group`
   - 12
   - Supervisor
   - Supervision en tiempo real + todas las de AGR-003


**CAMBIO v5.2.1:**
- Todos los nombres en inglés
- Sin prefijo redundante ``agr_``
- Sufijo ``_group`` explícito

**CAMBIO v5.5.0:**
- AGR-011 ``call_center_operator_group`` (10 funciones OPR-001..010)
- AGR-012 ``call_center_supervisor_group`` (SUP-001..003 + AGR-003)


4.2 Detalle de Grupos
---------------------



AGR-001 basic_operator_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (6):**

.. code-block:: text

 view_own_sessions
 view_all_active_sessions
 view_reports
 view_dashboard
 view_kpis
 view_charts


**Propósito:** Usuario básico que solo visualiza información.

----

AGR-002 report_viewer_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (8):**

.. code-block:: text

 Todas de AGR-001 +
 filter_reports
 view_users


**Propósito:** Analista que puede aplicar filtros pero no exportar.

----

AGR-003 quality_supervisor_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (11):**

.. code-block:: text

 Todas de AGR-002 +
 view_alerts
 configure_alerts
 view_alert_history


**Propósito:** Supervisor con capacidad de configurar alertas propias.

----

AGR-004 data_exporter_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (14):**

.. code-block:: text

 Todas de AGR-003 +
 export_csv
 export_excel
 export_pdf


**Propósito:** Analista autorizado para exportar con límites CNST-007.

----

AGR-005 alert_manager_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (6):**

.. code-block:: text

 view_alerts
 configure_alerts
 configure_team_alerts
 pause_alerts
 disable_alerts
 view_alert_history


**Propósito:** Gestor de alertas de equipo/departamento.

----

AGR-006 user_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (9):**

.. code-block:: text

 create_users
 update_users
 deactivate_users
 list_users
 search_users
 block_users
 unblock_users
 reactivate_users
 view_users


**Propósito:** Administración completa de identidades.

**SoD:** NO puede tener funciones de AGR-008 (auditoría).

----

AGR-007 permission_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (5):**

.. code-block:: text

 assign_functions
 revoke_functions
 view_assignments
 assign_function_groups
 view_separation_rules


**Propósito:** Administración de RBAC.

**SoD:** NO puede tener funciones de AGR-008 (auditoría).

----

AGR-008 auditor_group
^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (4):**

.. code-block:: text

 view_audit_log
 search_audit_log
 export_audit_log
 generate_compliance_report


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

 view_pipeline_status
 view_pipeline_errors
 view_data_availability
 request_pipeline_retry


**Propósito:** Administración de ETL.

**SoD:** NO puede tener funciones de AGR-008 (auditoría).

----

AGR-010 system_admin_group
^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (6):**

.. code-block:: text

 view_own_sessions
 close_user_session
 reset_password
 view_all_active_sessions
 view_application_logs
 export_logs


**Propósito:** Administración técnica del sistema.

----

AGR-011 call_center_operator_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (10):**

.. code-block:: text

 manage_own_agent_state
 answer_inbound_calls
 make_outbound_calls
 hold_calls
 transfer_calls
 enter_call_disposition
 request_break
 view_own_performance_dashboard
 view_own_call_history
 read_own_mailbox


**Propósito:** Conjunto base de acciones para agentes del call center.
Auto-asignado al activar perfil de operador.

----

AGR-012 call_center_supervisor_group
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Funciones incluidas (12):**

.. code-block:: text

 monitor_live_calls
 barge_in_calls
 broadcast_team_messages
 Todas las funciones de AGR-003 (quality_supervisor_group)


**Propósito:** Supervisores con capacidad de intervención en tiempo real.

**SoD:** Los supervisores NO deben tener funciones de AGR-008 (auditoría)
simultáneamente — aplica SOD-002 si también tienen funciones de gestión
de usuarios.


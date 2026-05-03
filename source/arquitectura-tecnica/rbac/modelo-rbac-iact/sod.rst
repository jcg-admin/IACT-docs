.. _modelo-rbac-iact-sod:

=============================================
Modelo RBAC IACT — Separacion de Funciones
=============================================

5. SEPARACIÓN DE FUNCIONES (SoD)
================================



5.1 Las 3 Restricciones SoD
---------------------------



SOD-001 pipeline_audit_separation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Restricción:** Un usuario NO puede tener funciones de Pipeline Y de Auditoría.

**Grupo A (Pipeline):**

.. code-block:: text

 PIP-001: view_pipeline_status
 PIP-002: view_pipeline_errors
 PIP-003: view_data_availability
 PIP-004: request_pipeline_retry


**Grupo B (Auditoría):**

.. code-block:: text

 AUD-001: view_audit_log
 AUD-002: search_audit_log
 AUD-003: export_audit_log
 AUD-004: generate_compliance_report


**Razón:** Evitar que quien opera el ETL audite sus propias acciones.

**CNST:** CNST-005

----

SOD-002 user_audit_separation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Restricción:** Un usuario NO puede tener funciones de gestión de Usuarios Y de Auditoría.

**Grupo A (Usuarios - críticas):**

.. code-block:: text

 USR-001: create_users
 USR-003: deactivate_users
 USR-004: list_users
 USR-007: unblock_users


**Grupo B (Auditoría):**

.. code-block:: text

 AUD-001: view_audit_log
 AUD-002: search_audit_log
 AUD-003: export_audit_log


**Razón:** Evitar que quien gestiona usuarios vea auditoría de sus acciones.

**CNST:** CNST-005

----

SOD-003 access_audit_separation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^


**Restricción:** Un usuario NO puede tener funciones de gestión de Acceso Y de Auditoría.

**Grupo A (Acceso):**

.. code-block:: text

 ACC-001: assign_functions
 ACC-002: revoke_functions
 ACC-005: view_separation_rules


**Grupo B (Auditoría):**

.. code-block:: text

 AUD-001: view_audit_log
 AUD-002: search_audit_log


**Razón:** Separación de poderes entre quien asigna permisos y quien audita.

**CNST:** CNST-005


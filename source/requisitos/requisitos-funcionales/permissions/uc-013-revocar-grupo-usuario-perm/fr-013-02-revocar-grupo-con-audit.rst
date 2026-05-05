.. meta::
 :artefacto: FR-013.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-013-02:

===============================================================
FR-013.02: Revocar grupo con validación y registro de auditoría
===============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-013.02
 * - **Nombre**
   - Revocar grupo con validación y registro de auditoría
 * - **UC Origen**
   - UC_PERM_02: Revocar Grupo a Usuario (vista PERM)
 * - **Paso UC**
   - Pasos 6-15 del flujo principal
 * - **Módulo**
   - MOD_Permissions
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE revocar el grupo de permisos del usuario CUANDO el administrador confirma la revocación, emitiendo el evento AGR_REVOKED y invalidando el caché.

**Descripción:**

 El backend valida JWT, la función revoke_function_group, la existencia del Assignment activo y el revoke_reason. Persiste UPDATE Assignment → REVOKED, emite AuditEvent AGR_REVOKED e invalida el caché post-commit. Flujo backend idéntico a UC_ACC_02.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador confirma revocar AGR-006 de ana.gomez.0001
 CUANDO DELETE /api/users/{id}/access-groups/{agr_id}/
 ENTONCES 200 OK y AGR revocado
 
 Escenario 1: Revocación exitosa
 DADO Assignment activo
 ENTONCES state=REVOKED + AuditEvent AGR_REVOKED
 
 Escenario 2: Sin permiso
 DADO invoker sin revoke_function_group
 ENTONCES 403 + AuditEvent UNAUTHORIZED

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-005, CNST-009, CNST-013, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_02: Revocar Grupo a Usuario (vista PERM)
 * - **Depende de**
   - FR-013.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-013-02 (pendiente)

----

6. Historial
------------

.. list-table::
 :widths: 15 15 70
 :header-rows: 1

 * - Versión
   - Fecha
   - Cambio
 * - 1.0.0
   - 2026-05-04
   - Versión inicial derivada de UC_PERM_02

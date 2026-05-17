.. meta::
 :artefacto: FR-015.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-015-02:

===================================================================
FR-015.02: Revocar permiso excepcional con notificación y auditoría
===================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-015.02
 * - **Nombre**
   - Revocar permiso excepcional con notificación y auditoría
 * - **UC Origen**
   - UC_PERM_04: Revocar Permiso Excepcional
 * - **Paso UC**
   - Pasos 11-16 del flujo principal
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

 El sistema DEBE marcar el permiso excepcional como REVOKED, enviar notificación InternalMessage OBLIGATORIA y emitir AuditEvent CUANDO la revocación es válida.

**Descripción:**

 El UPDATE state → REVOKED incluye metadata de revocación (revoke_reason, revoked_by, revoked_at). La notificación InternalMessage es mandatoria en la misma transacción. Se invalida el caché post-commit. AuditEvent EXCEPTIONAL_PERMISSION_REVOKED emitido.

----

3. Criterio de Aceptación
-------------------------

::

 DADO validación exitosa de revocación
 CUANDO se procesa
 ENTONCES 200 OK + state=REVOKED + InternalMessage + AuditEvent
 
 Escenario 1: Revocación exitosa
 DADO permiso ACTIVE y revoke_reason proporcionado
 ENTONCES state=REVOKED + notificación enviada
 
 Escenario 2: Sin permiso
 DADO invoker sin revoke_exceptional_permission
 ENTONCES 403

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-005, CNST-009, CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_04: Revocar Permiso Excepcional
 * - **Depende de**
   - FR-015.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-015-02 (pendiente)

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
   - Versión inicial derivada de UC_PERM_04

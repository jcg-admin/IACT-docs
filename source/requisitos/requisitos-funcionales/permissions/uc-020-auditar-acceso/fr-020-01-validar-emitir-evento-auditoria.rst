.. meta::
 :artefacto: FR-020.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-020-01:

===============================================================
FR-020.01: Validar y emitir evento de auditoría con escaneo PII
===============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-020.01
 * - **Nombre**
   - Validar y emitir evento de auditoría con escaneo PII
 * - **UC Origen**
   - UC_PERM_09: Auditar Acceso (write side)
 * - **Paso UC**
   - Pasos 2-5 del flujo principal
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

 El sistema DEBE validar la estructura del evento, escanear el payload en busca de PII y sanitizarlo ANTES de persistir cualquier registro de auditoría.

**Descripción:**

 La validación verifica: event_type en enum conocido, payload JSON serializable, tamaño ≤ 16 KB, module en MOD_*. El escaneo PII detecta emails, números de identidad, passwords/tokens, teléfonos — si detecta, lanza AuditPIIDetected bloqueando la emisión. El sanitizador convierte nombres/emails a hashes antes de persistir.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un UC invocante emite AuditEvent con payload
 CUANDO el servicio procesa el evento
 ENTONCES se valida estructura y se escanea PII antes de persistir
 
 Escenario 1: Payload limpio
 DADO sin PII en payload
 ENTONCES INSERT AuditEvent normalizado
 
 Escenario 2: PII detectado
 DADO payload contiene email explícito
 ENTONCES AuditPIIDetected → ROLLBACK en el caller
 
 Escenario 3: Payload > 16 KB
 DADO payload de 20 KB
 ENTONCES AuditValidationError → ROLLBACK

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-025, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_09: Auditar Acceso (write side)
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-020.02
 * - **TEST**
   - TST-fr-020-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_09

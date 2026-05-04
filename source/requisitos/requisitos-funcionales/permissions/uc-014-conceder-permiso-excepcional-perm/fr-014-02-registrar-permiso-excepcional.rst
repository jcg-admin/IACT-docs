.. meta::
 :artefacto: FR-014.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-014-02:

=====================================================================
FR-014.02: Registrar permiso excepcional con notificación obligatoria
=====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-014.02
 * - **Nombre**
   - Registrar permiso excepcional con notificación obligatoria
 * - **UC Origen**
   - UC_PERM_03: Conceder Permiso Excepcional (vista PERM)
 * - **Paso UC**
   - Pasos 12-16 del flujo principal
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

 El sistema DEBE persistir el permiso excepcional, enviar notificación interna OBLIGATORIA y emitir AuditEvent de alta prioridad CUANDO las validaciones son exitosas.

**Descripción:**

 La notificación InternalMessage al supervisor del User es mandatoria (no opcional). El AuditEvent EXCEPTIONAL_PERMISSION_GRANTED se clasifica como high-priority. La respuesta incluye resumen del permiso concedido y warnings SoD si aplica.

----

3. Criterio de Aceptación
-------------------------

::

 DADO validaciones exitosas para un permiso excepcional
 CUANDO se completa la operación
 ENTONCES 201 Created + InternalMessage enviado + AuditEvent high-priority
 
 Escenario 1: Notificación enviada
 DADO concesión exitosa
 ENTONCES InternalMessage registrado en misma transacción
 
 Escenario 2: Falla de notificación
 DADO error en InternalMessage
 ENTONCES ROLLBACK de toda la operación

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
   - UC_PERM_03: Conceder Permiso Excepcional (vista PERM)
 * - **Depende de**
   - FR-014.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-014-02 (pendiente)

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
   - Versión inicial derivada de UC_PERM_03

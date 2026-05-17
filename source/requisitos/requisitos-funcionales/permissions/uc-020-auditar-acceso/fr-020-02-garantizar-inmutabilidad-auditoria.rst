.. meta::
 :artefacto: FR-020.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-020-02:

===========================================================================
FR-020.02: Garantizar append-only e inmutabilidad de registros de auditoría
===========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-020.02
 * - **Nombre**
   - Garantizar append-only e inmutabilidad de registros de auditoría
 * - **UC Origen**
   - UC_PERM_09: Auditar Acceso (write side)
 * - **Paso UC**
   - Paso 4-5 del flujo principal (post-sanitize)
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

 El sistema DEBE persistir los registros de auditoría de forma append-only CUANDO el evento es válido y sanitizado, sin permitir modificación ni eliminación posterior.

**Descripción:**

 La tabla de AuditEvents es append-only: no hay UPDATE ni DELETE permitidos por el servicio de auditoría. Los registros son inmutables una vez escritos. Esta restricción es un requisito de cumplimiento normativo (CNST-025).

----

3. Criterio de Aceptación
-------------------------

::

 DADO un AuditEvent sanitizado listo para persistir
 CUANDO se escribe
 ENTONCES INSERT inmutable sin posibilidad de UPDATE posterior
 
 Escenario 1: Escritura exitosa
 DADO evento válido
 ENTONCES INSERT único y definitivo
 
 Escenario 2: Intento de modificación
 DADO cualquier intento de UPDATE sobre AuditEvent
 ENTONCES operación rechazada a nivel de servicio

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
   - FR-020.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-020-02 (pendiente)

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

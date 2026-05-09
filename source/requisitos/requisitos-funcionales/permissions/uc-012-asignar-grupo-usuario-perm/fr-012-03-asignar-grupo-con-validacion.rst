.. meta::
 :artefacto: FR-012.03
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-012-03:

================================================================================
FR-012.03: Asignar grupo a usuario con validación RBAC y separacion de deberes
================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-012.03
 * - **Nombre**
   - Asignar grupo a usuario con validación RBAC y separacion de deberes
 * - **UC Origen**
   - UC_PERM_01: Asignar Grupo a Usuario (vista PERM)
 * - **Paso UC**
   - Pasos 7-15 del flujo principal
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

 El sistema DEBE asignar el grupo de permisos al usuario destino CUANDO el administrador confirma la asignación, validando JWT, idempotencia y restricciones de separacion antes de persistir.

**Descripción:**

 La asignación sigue el mismo flujo backend que UC_ACC_04: validar JWT, verificar función assign_function_groups, expandir AGR, validar separacion, INSERT Assignment, emitir AuditEvent AGR_ASSIGNED, invalidar caché. La operación es atómica ACID.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador confirma asignar AGR-006 a ana.gomez.0001
 CUANDO se envía POST /api/users/{id}/access-groups/
 ENTONCES status 201 y el AGR queda asignado
 
 Escenario 1: Asignación exitosa
 DADO User activo y AGR activo sin conflicto de separacion
 ENTONCES 201 Created
 
 Escenario 2: Ya asignado (idempotencia)
 DADO el AGR ya asignado al User
 ENTONCES 200 OK (no duplicado)
 
 Escenario 3: Conflicto de separacion
 DADO el AGR genera conflicto de separacion
 ENTONCES 422 con detalle del conflicto

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
   - UC_PERM_01: Asignar Grupo a Usuario (vista PERM)
 * - **Depende de**
   - FR-012.02
 * - **Requerido por**
   - FR-012.04
 * - **TEST**
   - TST-fr-012-03 (pendiente)

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
   - Versión inicial derivada de UC_PERM_01

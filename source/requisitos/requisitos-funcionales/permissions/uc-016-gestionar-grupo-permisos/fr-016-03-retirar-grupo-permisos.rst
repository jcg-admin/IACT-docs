.. meta::
 :artefacto: FR-016.03
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-016-03:

=========================================================================
FR-016.03: Retirar grupo de permisos con verificación de usuarios activos
=========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-016.03
 * - **Nombre**
   - Retirar grupo de permisos con verificación de usuarios activos
 * - **UC Origen**
   - UC_PERM_05: Crear/Modificar/Retirar Grupo de Permisos
 * - **Paso UC**
   - Sub-flujo 3.C del flujo principal
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

 El sistema DEBE rechazar el retiro de un grupo que tiene usuarios asignados activos CUANDO se intenta eliminarlo, protegiendo la integridad del modelo RBAC.

**Descripción:**

 Antes del DELETE, el sistema verifica que el AGR no tenga Assignments activos. Si los tiene, retorna 409 con count de usuarios afectados. Solo si users_count=0 procede con la eliminación lógica + AuditEvent ACCESS_GROUP_RETIRED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO DELETE /api/access-groups/{id}/
 CUANDO el AGR tiene usuarios asignados
 ENTONCES 409 Conflict con users_count
 
 Escenario 1: AGR sin usuarios
 DADO users_count=0
 ENTONCES eliminación lógica + AuditEvent
 
 Escenario 2: AGR con usuarios activos
 DADO users_count=3
 ENTONCES 409 con mensaje de 3 usuarios afectados

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_05: Crear/Modificar/Retirar Grupo de Permisos
 * - **Depende de**
   - FR-016.02
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-016-03 (pendiente)

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
   - Versión inicial derivada de UC_PERM_05

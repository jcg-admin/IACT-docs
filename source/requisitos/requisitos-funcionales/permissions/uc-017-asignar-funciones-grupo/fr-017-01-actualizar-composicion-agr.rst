.. meta::
 :artefacto: FR-017.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-017-01:

=========================================================================
FR-017.01: Actualizar composición del grupo con validación SoD en cascada
=========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-017.01
 * - **Nombre**
   - Actualizar composición del grupo con validación SoD en cascada
 * - **UC Origen**
   - UC_PERM_06: Asignar Funciones a Grupo (composición AGR)
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

 El sistema DEBE actualizar las funciones de un grupo de permisos personalizado CUANDO se proporciona la lista de funciones a agregar y retirar, validando que el cambio no genere conflictos SoD para ningún usuario que tenga el grupo asignado.

**Descripción:**

 El backend valida assign_functions_to_group, que el AGR sea custom y ACTIVE, que las funciones existan y estén activas, aplica idempotencia, calcula el cascade_affected_user_count, valida SoD post-cambio para cada usuario afectado (defensa cascade), persiste INSERT/DELETE AccessGroupFunction y emite AuditEvent ACCESS_GROUP_COMPOSITION_CHANGED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO POST /api/access-groups/{id}/functions/ con add_ids y remove_ids
 CUANDO se procesa el cambio de composición
 ENTONCES 200 OK con resumen y cascade_count
 
 Escenario 1: Sin conflicto SoD
 DADO cambio no genera SoD para ningún usuario
 ENTONCES composición actualizada
 
 Escenario 2: Conflicto SoD cascade
 DADO el cambio genera SoD para 2 usuarios
 ENTONCES 422 con detalle de usuarios en conflicto
 
 Escenario 3: Idempotencia
 DADO función ya presente en add_ids
 ENTONCES operación ignorada silenciosamente

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-005, CNST-009, CNST-013, CNST-025

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-004
 * - **UC**
   - UC_PERM_06: Asignar Funciones a Grupo (composición AGR)
 * - **Depende de**
   - Ninguno
 * - **Requerido por**
   - FR-017.02
 * - **TEST**
   - TST-fr-017-01 (pendiente)

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
   - Versión inicial derivada de UC_PERM_06

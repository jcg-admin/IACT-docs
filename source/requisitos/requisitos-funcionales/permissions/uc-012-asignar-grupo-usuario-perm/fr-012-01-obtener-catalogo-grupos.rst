.. meta::
 :artefacto: FR-012.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-012-01:

=================================================
FR-012.01: Obtener catálogo de grupos de permisos
=================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-012.01
 * - **Nombre**
   - Obtener catálogo de grupos de permisos
 * - **UC Origen**
   - UC_PERM_01: Asignar Grupo a Usuario (vista PERM)
 * - **Paso UC**
   - Paso 1-2 del flujo principal
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

 El sistema DEBE retornar la lista de grupos de permisos (AGRs) activos con su composición de funciones y conteo de usuarios asignados CUANDO un administrador de seguridad consulta el catálogo de permisos.

**Descripción:**

 La respuesta incluye para cada AGR: código, nombre, descripción, cantidad de funciones y cantidad de usuarios actuales. El listado soporta filtros por categoría y severity.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador con permiso de lectura RBAC
 CUANDO solicita GET /api/access-groups/
 ENTONCES recibe lista de AGRs con function_count y users_count
 
 Escenario 1: Catálogo con AGRs activos
 DADO 5 AGRs activos
 CUANDO se consulta el catálogo
 ENTONCES respuesta status 200 con los 5 AGRs y sus metadatos
 
 Escenario 2: Sin permisos
 DADO un usuario sin assign_function_groups
 CUANDO consulta el catálogo
 ENTONCES respuesta 403

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009 (autenticación), CNST-014 (paginación)

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
   - Ninguno
 * - **Requerido por**
   - FR-012.02
 * - **TEST**
   - TST-fr-012-01 (pendiente)

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

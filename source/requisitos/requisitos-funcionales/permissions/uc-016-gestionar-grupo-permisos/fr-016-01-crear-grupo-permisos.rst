.. meta::
 :artefacto: FR-016.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-016-01:

===================================================
FR-016.01: Crear grupo de permisos con código único
===================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-016.01
 * - **Nombre**
   - Crear grupo de permisos con código único
 * - **UC Origen**
   - UC_PERM_05: Crear/Modificar/Retirar Grupo de Permisos
 * - **Paso UC**
   - Sub-flujo 3.A del flujo principal
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

 El sistema DEBE crear un nuevo grupo de permisos personalizado CUANDO se proporciona un código único y formato válido, validando que no colisione con AGRs predefinidos.

**Descripción:**

 El backend valida la función create_function_group, el formato del código (único, no colisión con predefinidos), persiste INSERT AccessGroup y emite AuditEvent ACCESS_GROUP_CREATED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador envía POST /api/access-groups/ con código único
 CUANDO se procesa
 ENTONCES 201 Created con el nuevo AGR
 
 Escenario 1: Código único
 DADO code='custom_ops_group' no existente
 ENTONCES INSERT AccessGroup y 201
 
 Escenario 2: Código duplicado
 DADO code ya existente
 ENTONCES 409 Conflict

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013

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
   - Ninguno
 * - **Requerido por**
   - FR-016.02
 * - **TEST**
   - TST-fr-016-01 (pendiente)

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

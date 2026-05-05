.. meta::
 :artefacto: FR-012.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-012-02:

=========================================================
FR-012.02: Mostrar composición del grupo antes de asignar
=========================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-012.02
 * - **Nombre**
   - Mostrar composición del grupo antes de asignar
 * - **UC Origen**
   - UC_PERM_01: Asignar Grupo a Usuario (vista PERM)
 * - **Paso UC**
   - Paso 5 del flujo principal
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

 El sistema DEBE mostrar la composición completa de funciones del grupo seleccionado CUANDO el administrador inicia la asignación, antes de confirmarla.

**Descripción:**

 El modal de confirmación lista las funciones del AGR usando display_names (no IDs internos). Esta visualización es obligatoria como defensa contra asignaciones ciegas por nombre de AGR.

----

3. Criterio de Aceptación
-------------------------

::

 DADO un administrador que selecciona el AGR 'user_admin_group'
 CUANDO clickea Asignar
 ENTONCES el modal muestra las 8 funciones del AGR con nombres descriptivos
 
 Escenario 1: AGR con funciones
 DADO AGR con 8 funciones activas
 CUANDO se muestra el modal
 ENTONCES se listan los display_names de las 8 funciones
 
 Escenario 2: AGR sin funciones
 DADO AGR recién creado sin funciones
 CUANDO se muestra el modal
 ENTONCES mensaje de advertencia de AGR vacío

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009

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
   - FR-012.01
 * - **Requerido por**
   - FR-012.03
 * - **TEST**
   - TST-fr-012-02 (pendiente)

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

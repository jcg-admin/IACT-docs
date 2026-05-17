.. meta::
 :artefacto: FR-017.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-017-02:

==============================================================
FR-017.02: Invalidar caché post-cambio de composición de grupo
==============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-017.02
 * - **Nombre**
   - Invalidar caché post-cambio de composición de grupo
 * - **UC Origen**
   - UC_PERM_06: Asignar Funciones a Grupo (composición AGR)
 * - **Paso UC**
   - Paso 14 del flujo principal
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

 El sistema DEBE invalidar el caché de permisos para todos los usuarios que tienen el grupo modificado CUANDO la composición del grupo cambia exitosamente.

**Descripción:**

 La invalidación de caché ocurre post-commit para garantizar consistencia. Todos los usuarios con el AGR modificado tienen su caché de permisos y menú invalidados para que la próxima verificación resuelva el conjunto efectivo actualizado.

----

3. Criterio de Aceptación
-------------------------

::

 DADO cambio de composición de AGR con 10 usuarios asignados
 CUANDO el commit se completa
 ENTONCES caché invalidado para los 10 usuarios
 
 Escenario 1: Invalidación masiva
 DADO 100 usuarios con el AGR
 ENTONCES todos sus cachés invalidados post-commit

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
   - UC_PERM_06: Asignar Funciones a Grupo (composición AGR)
 * - **Depende de**
   - FR-017.01
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-017-02 (pendiente)

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

.. meta::
 :artefacto: FR-012.04
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-012-04:

=============================================================
FR-012.04: Actualizar contadores del catálogo post-asignación
=============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-012.04
 * - **Nombre**
   - Actualizar contadores del catálogo post-asignación
 * - **UC Origen**
   - UC_PERM_01: Asignar Grupo a Usuario (vista PERM)
 * - **Paso UC**
   - Paso 16 del flujo principal
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

 El sistema DEBE reflejar la asignación en los contadores del catálogo de permisos CUANDO la asignación se completa exitosamente.

**Descripción:**

 Después de una asignación exitosa, el users_count del AGR debe incrementarse en 1 en la respuesta del catálogo. La invalidación de caché garantiza que la próxima consulta refleje el estado actual.

----

3. Criterio de Aceptación
-------------------------

::

 DADO asignación exitosa de AGR a User
 CUANDO el frontend consulta el catálogo
 ENTONCES users_count del AGR incrementado en 1
 
 Escenario 1: Conteo actualizado
 DADO AGR con users_count=5 antes de asignación
 CUANDO se consulta el catálogo después
 ENTONCES users_count=6

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
   - FR-012.03
 * - **Requerido por**
   - Ninguno
 * - **TEST**
   - TST-fr-012-04 (pendiente)

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

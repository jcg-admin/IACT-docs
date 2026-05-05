.. meta::
 :artefacto: FR-016.02
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/permissions
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-016-02:

====================================================
FR-016.02: Modificar grupo de permisos personalizado
====================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-016.02
 * - **Nombre**
   - Modificar grupo de permisos personalizado
 * - **UC Origen**
   - UC_PERM_05: Crear/Modificar/Retirar Grupo de Permisos
 * - **Paso UC**
   - Sub-flujo 3.B del flujo principal
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

 El sistema DEBE permitir modificar atributos de un grupo personalizado CUANDO el grupo existe, está activo y es de tipo custom (no predefinido).

**Descripción:**

 Solo grupos custom (is_predefined=false) son modificables. El código (code) es inmutable post-creación. Los campos modificables son nombre, descripción y categoría. UPDATE AccessGroup + AuditEvent ACCESS_GROUP_MODIFIED.

----

3. Criterio de Aceptación
-------------------------

::

 DADO PATCH /api/access-groups/{id}/ con nombre actualizado
 CUANDO el AGR es custom y ACTIVE
 ENTONCES 200 OK con cambios aplicados
 
 Escenario 1: Modificación exitosa
 DADO AGR custom ACTIVE
 ENTONCES UPDATE + AuditEvent
 
 Escenario 2: Intento de modificar predefinido
 DADO is_predefined=true
 ENTONCES 403 Forbidden
 
 Escenario 3: Intento de cambiar code
 DADO payload con code diferente
 ENTONCES 422 (código inmutable)

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
   - FR-016.01
 * - **Requerido por**
   - FR-016.03
 * - **TEST**
   - TST-fr-016-02 (pendiente)

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

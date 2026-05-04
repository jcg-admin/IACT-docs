.. meta::
 :artefacto: FR-038.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-038-01:

=============================================================================
FR-038.01: Crear, listar, actualizar y eliminar filtros guardados del usuario
=============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-038.01
 * - **Nombre**
   - Crear, listar, actualizar y eliminar filtros guardados del usuario
 * - **UC Origen**
   - UC_RPT_09: Gestionar Filtros Guardados
 * - **Paso UC**
   - Pasos 1-6 del flujo principal (crear) y operaciones CRUD
 * - **Módulo**
   - MOD_Reports
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE permitir al usuario guardar combinaciones de filtros de reporte CUANDO los crea con nombre único, validando que los filtros no violen el segmento del usuario y que no supere el límite de 50 filtros.

**Descripción:**

 Crear: valida nombre no vacío ≤ 100 chars, único por usuario, filtros estructuralmente válidos, filtros NO violan segmento, usuario ≤ 50 filtros. INSERT SavedFilter. CRUD completo (list, get, update, delete) con ownership check.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario crea filtro 'Semana pasada - nacional_A'
 CUANDO POST con nombre y filtros
 ENTONCES 201 con filter_id
 
 Escenario 1: Nombre duplicado
 DADO mismo nombre ya existe para el usuario
 ENTONCES 409
 
 Escenario 2: Filtro viola segmento
 DADO filtro incluye DID fuera del segmento
 ENTONCES 422

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
   - BReq-001
 * - **UC**
   - UC_RPT_09: Gestionar Filtros Guardados
 * - **TEST**
   - TST-fr-038-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_09

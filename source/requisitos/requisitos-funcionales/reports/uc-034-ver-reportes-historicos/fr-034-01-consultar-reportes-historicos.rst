.. meta::
 :artefacto: FR-034.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-034-01:

==============================================================================
FR-034.01: Consultar reportes históricos con filtros y paginación por segmento
==============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-034.01
 * - **Nombre**
   - Consultar reportes históricos con filtros y paginación por segmento
 * - **UC Origen**
   - UC_RPT_03: Ver Reportes Históricos
 * - **Paso UC**
   - Pasos 1-9 del flujo principal
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

 El sistema DEBE retornar datos históricos CUANDO un usuario con view_reports los solicita, validando que el rango temporal no exceda 2 años y que el agrupamiento sea compatible con el período.

**Descripción:**

 Se valida JWT + view_reports + segmento. Validaciones: período en enum o date range válido (≤ 2 años), group_by compatible con período, page_size ≤ 200. Query sobre réplica analítica filtrada por segmento. Paginación cursor-based.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita históricos del último trimestre
 CUANDO GET con period=Q1 y filtros
 ENTONCES 200 con resultados paginados del segmento
 
 Escenario 1: Rango válido
 DADO date range < 2 años
 ENTONCES resultados con cursor
 
 Escenario 2: Rango excedido
 DADO date range > 2 años
 ENTONCES 422

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_03: Ver Reportes Históricos
 * - **TEST**
   - TST-fr-034-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_03

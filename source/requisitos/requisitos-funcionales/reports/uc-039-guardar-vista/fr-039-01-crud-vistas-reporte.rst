.. meta::
 :artefacto: FR-039.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-039-01:

=============================================================
FR-039.01: Crear y gestionar vistas de reporte personalizadas
=============================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-039.01
 * - **Nombre**
   - Crear y gestionar vistas de reporte personalizadas
 * - **UC Origen**
   - UC_RPT_10: Guardar Vista de Reporte
 * - **Paso UC**
   - Pasos 1-7 del flujo principal
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

 El sistema DEBE permitir al usuario guardar vistas personalizadas de reportes CUANDO las crea con nombre único, validando columnas, filtros y configuración de gráficos, con límite de 30 vistas.

**Descripción:**

 Validaciones: nombre único por usuario, columns ⊆ catálogo del report_type, filtros válidos contra segmento, chart_config consistente, usuario ≤ 30 vistas. INSERT SavedView + AuditEvent VIEW_CREATED. CRUD completo.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario crea vista 'Agentes top TMO'
 CUANDO POST con columns y chart_config
 ENTONCES 201 con view_id
 
 Escenario 1: Columna inválida
 DADO column no en catálogo del report_type
 ENTONCES 422

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
   - BReq-001
 * - **UC**
   - UC_RPT_10: Guardar Vista de Reporte
 * - **TEST**
   - TST-fr-039-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_10

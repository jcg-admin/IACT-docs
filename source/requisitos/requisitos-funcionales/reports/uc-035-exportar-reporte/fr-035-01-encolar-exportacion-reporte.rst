.. meta::
 :artefacto: FR-035.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-035-01:

=============================================================================
FR-035.01: Encolar exportación de reporte con validación de límites y formato
=============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-035.01
 * - **Nombre**
   - Encolar exportación de reporte con validación de límites y formato
 * - **UC Origen**
   - UC_RPT_04: Exportar Reporte
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
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

 El sistema DEBE encolar una exportación de reporte CUANDO un usuario con export_csv lo solicita, validando el tipo de reporte, formato de salida, volumen estimado y que no supere el límite de jobs simultáneos.

**Descripción:**

 Validaciones: report_type en enum, format en {csv, xlsx, json, pdf}, filtros válidos para el tipo, estimación de filas ≤ 1M, user no excede 5 jobs simultáneos. INSERT ExportJob + AuditEvent EXPORT_REQUESTED. Job ejecutado asíncronamente; respuesta inmediata 202 con job_id.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita exportación de reporte de agentes a CSV
 CUANDO POST con report_type y filters
 ENTONCES 202 Accepted con job_id
 
 Escenario 1: Export encolado
 DADO params válidos y < 5 jobs activos
 ENTONCES 202 + ExportJob en cola
 
 Escenario 2: Límite de jobs
 DADO usuario ya tiene 5 jobs activos
 ENTONCES 429 límite excedido
 
 Escenario 3: Volumen excedido
 DADO estimación > 1M filas
 ENTONCES 422

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-013

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_04: Exportar Reporte
 * - **TEST**
   - TST-fr-035-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_04

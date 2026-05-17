.. meta::
 :artefacto: FR-036.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-036-01:

====================================================================
FR-036.01: Crear y ejecutar reporte programado con cron configurable
====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-036.01
 * - **Nombre**
   - Crear y ejecutar reporte programado con cron configurable
 * - **UC Origen**
   - UC_RPT_07: Programar Reporte
 * - **Paso UC**
   - Pasos 1-9 del flujo principal (creación) y ejecución automática
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

 El sistema DEBE crear un reporte programado CUANDO un usuario con schedule_report y export_csv lo configura, validando la expresión cron y calculando la próxima ejecución; y ejecutarlo automáticamente en cada disparo.

**Descripción:**

 Validaciones: cron parseable, period_relative válido para frequency, usuario no excede 10 schedules activos. INSERT ScheduledReport + next_run_at calculado + AuditEvent SCHEDULED_REPORT_CREATED. Ejecución automática por el scheduler en next_run_at; genera ExportJob y notifica por buzón interno.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario crea schedule con cron='0 8 * * 1' (lunes 8am)
 CUANDO POST con payload
 ENTONCES 201 con schedule_id y next_run_at calculado
 
 Escenario 1: Creación exitosa
 DADO cron válido y < 10 schedules
 ENTONCES 201
 
 Escenario 2: Cron inválido
 DADO cron='99 8 * * 1'
 ENTONCES 422
 
 Escenario 3: Límite de schedules
 DADO usuario ya tiene 10
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
   - UC_RPT_07: Programar Reporte
 * - **TEST**
   - TST-fr-036-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_07

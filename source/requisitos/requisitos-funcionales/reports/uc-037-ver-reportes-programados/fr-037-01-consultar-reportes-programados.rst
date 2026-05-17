.. meta::
 :artefacto: FR-037.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-037-01:

=================================================================
FR-037.01: Consultar y gestionar reportes programados del usuario
=================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-037.01
 * - **Nombre**
   - Consultar y gestionar reportes programados del usuario
 * - **UC Origen**
   - UC_RPT_08: Ver Reportes Programados
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

 El sistema DEBE retornar la lista de reportes programados del usuario autenticado CUANDO los solicita, con filtros por estado y frecuencia.

**Descripción:**

 Valida JWT + RBAC view_reports. Query ScheduledReportRepo filtrado por actor_id (caller) con filtros opcionales. Detalle incluye última ejecución. Paginación estándar.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita GET /api/scheduled-reports/
 CUANDO se procesa
 ENTONCES lista paginada de sus schedules
 
 Escenario 1: Filtro por status
 DADO filter=active
 ENTONCES solo schedules activos del usuario

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-014

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_08: Ver Reportes Programados
 * - **TEST**
   - TST-fr-037-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_08

.. meta::
 :artefacto: FR-042.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-042-01:

========================================================================
FR-042.01: Generar reporte de métricas de colas con KPIs ASA/SL/abandono
========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-042.01
 * - **Nombre**
   - Generar reporte de métricas de colas con KPIs ASA/SL/abandono
 * - **UC Origen**
   - UC_RPT_13: Reporte de Colas
 * - **Paso UC**
   - Pasos 1-11 del flujo principal
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

 El sistema DEBE retornar métricas agregadas de colas CUANDO un usuario con view_reports las solicita, calculando KPIs (ASA, Service Level, tasa de abandono) y tendencias por hora.

**Descripción:**

 Estructura idéntica a UC_RPT_12. Query QueueDailyStat con KPIs específicos de cola: ASA (Average Speed of Answer), SL (Service Level ≥ X% en ≤ Y seg), abandono. Detalle incluye trends por hora.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita reporte de colas
 CUANDO GET con period y filtros
 ENTONCES 200 con KPIs por cola del segmento
 
 Escenario 1: SL calculado
 DADO datos de cola disponibles
 ENTONCES SL = calls_answered_in_threshold / total * 100

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-014, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_13: Reporte de Colas
 * - **TEST**
   - TST-fr-042-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_13

.. meta::
 :artefacto: FR-043.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-043-01:

==============================================================================
FR-043.01: Generar reporte de métricas de campañas con conversión y tendencias
==============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-043.01
 * - **Nombre**
   - Generar reporte de métricas de campañas con conversión y tendencias
 * - **UC Origen**
   - UC_RPT_14: Reporte de Campañas
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

 El sistema DEBE retornar métricas de campañas CUANDO un usuario con view_reports las solicita, calculando tasas de conversión por hora y breakdown de disposiciones.

**Descripción:**

 Estructura idéntica a UC_RPT_12/13. Query CampaignDailyStat. KPIs: conversión (resolved/total), llamadas por hora, breakdown por disposition. Detalle incluye trends por día.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita reporte de campaña 'Campaña Q1'
 CUANDO GET con campaign_id y period
 ENTONCES 200 con conversión y tendencias
 
 Escenario 1: Tasa de conversión
 DADO 100 llamadas, 45 resolved
 ENTONCES conversion_rate=45%

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
   - UC_RPT_14: Reporte de Campañas
 * - **TEST**
   - TST-fr-043-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_14

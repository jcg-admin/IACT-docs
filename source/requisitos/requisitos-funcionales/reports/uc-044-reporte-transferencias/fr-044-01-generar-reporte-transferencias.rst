.. meta::
 :artefacto: FR-044.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-044-01:

==============================================================================
FR-044.01: Generar reporte de transferencias con totales, breakdowns y heatmap
==============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-044.01
 * - **Nombre**
   - Generar reporte de transferencias con totales, breakdowns y heatmap
 * - **UC Origen**
   - UC_RPT_15: Reporte de Transferencias
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

 El sistema DEBE retornar análisis de transferencias CUANDO un usuario con view_reports lo solicita, con totales, breakdowns por tipo (warm/cold) y heatmap de flujos de transferencia.

**Descripción:**

 Query TransferEvent agregado. Calcula totals, breakdowns por tipo de transferencia y agente origen/destino. Construye heatmap de flujos de transferencia entre agentes/colas. Caché adaptativo.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita reporte de transferencias
 CUANDO GET con period
 ENTONCES 200 con totales, breakdowns y heatmap
 
 Escenario 1: Heatmap generado
 DADO datos de TransferEvent
 ENTONCES matriz agente_origen × agente_destino con conteos

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
   - UC_RPT_15: Reporte de Transferencias
 * - **TEST**
   - TST-fr-044-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_15

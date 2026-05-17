.. meta::
 :artefacto: FR-045.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-045-01:

=====================================================================
FR-045.01: Generar reporte de navegación de menús IVR con path mining
=====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-045.01
 * - **Nombre**
   - Generar reporte de navegación de menús IVR con path mining
 * - **UC Origen**
   - UC_RPT_16: Reporte de Menús IVR
 * - **Paso UC**
   - Pasos 1-10 del flujo principal
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

 El sistema DEBE retornar análisis de uso de menús IVR CUANDO un usuario con view_reports lo solicita, incluyendo entry/drop/completion por opción y los paths más frecuentes.

**Descripción:**

 Query IVRSessionEvent agregado: conteos de entrada, abandono y completación por opción, distribución de drop-off por nodo. Path mining para top N paths frecuentes.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita reporte IVR de la semana
 CUANDO GET con period
 ENTONCES 200 con métricas por opción y top paths
 
 Escenario 1: Drop-off por nodo
 DADO 30% abandono en opción '2' del menú principal
 ENTONCES nodo marcado con tasa de abandono

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
   - UC_RPT_16: Reporte de Menús IVR
 * - **TEST**
   - TST-fr-045-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_16

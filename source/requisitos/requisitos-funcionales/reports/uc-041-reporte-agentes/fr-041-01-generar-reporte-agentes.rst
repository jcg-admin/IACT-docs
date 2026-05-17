.. meta::
 :artefacto: FR-041.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-041-01:

============================================================================
FR-041.01: Generar reporte de métricas de agentes con KPIs derivados y caché
============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-041.01
 * - **Nombre**
   - Generar reporte de métricas de agentes con KPIs derivados y caché
 * - **UC Origen**
   - UC_RPT_12: Reporte de Agentes
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

 El sistema DEBE retornar métricas agregadas de agentes CUANDO un supervisor con view_reports las solicita, calculando KPIs derivados (TMO, AHT, occupancy, adherence) y filtrando por segmento.

**Descripción:**

 Valida JWT + view_reports + segmento. Cache lookup con TTL adaptativo. En miss: query AgentDailyStat agregado por agente en período filtrado por segmento. Calcula KPIs derivados y summary del equipo. Cache write.

----

3. Criterio de Aceptación
-------------------------

::

 DADO supervisor solicita reporte de agentes del último mes
 CUANDO GET con period
 ENTONCES 200 con métricas por agente del segmento
 
 Escenario 1: Cache hit
 DADO reporte cacheado
 ENTONCES respuesta inmediata
 
 Escenario 2: Segmento restringido
 DADO supervisor con segmento nacional_A
 ENTONCES solo agentes de nacional_A

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
   - UC_RPT_12: Reporte de Agentes
 * - **TEST**
   - TST-fr-041-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_12

.. meta::
 :artefacto: FR-065.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-065-01:

===================================================================
FR-065.01: Consultar métricas de rendimiento del sistema desde TSDB
===================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-065.01
 * - **Nombre**
   - Consultar métricas de rendimiento del sistema desde TSDB
 * - **UC Origen**
   - UC_LOG_07: Ver Métricas de Rendimiento
 * - **Paso UC**
   - Pasos 1-8 del flujo principal
 * - **Módulo**
   - MOD_Logs
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar métricas de rendimiento (latencia, throughput) CUANDO un usuario las solicita, consultando la TSDB con agregaciones y calculando percentiles P50/P95/P99.

**Descripción:**

 Valida JWT + RBAC. Valida parámetros. Cache lookup (TTL 30s). Query TSDB con time range y agregación. Calcula P50/P95/P99 desde histogramas. Cache write.

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin solicita latencia de API del último día
 CUANDO GET con metric y range
 ENTONCES 200 con P50/P95/P99
 
 Escenario 1: Cache hit
 DADO métricas cacheadas
 ENTONCES respuesta < 50ms

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-017

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-006
 * - **UC**
   - UC_LOG_07: Ver Métricas de Rendimiento
 * - **TEST**
   - TST-fr-065-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_07

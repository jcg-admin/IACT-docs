.. meta::
 :artefacto: FR-053.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/alerts
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-053-01:

============================================================================
FR-053.01: Consultar historial de alertas resueltas con métricas time-to-ack
============================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-053.01
 * - **Nombre**
   - Consultar historial de alertas resueltas con métricas time-to-ack
 * - **UC Origen**
   - UC_ALR_04: Ver Historial de Alertas
 * - **Paso UC**
   - Pasos 1-11 del flujo principal
 * - **Módulo**
   - MOD_Alerts
 * - **Prioridad**
   - Alta
 * - **Tipo**
   - Funcional

----

2. Especificación
-----------------

**Declaración:**

 El sistema DEBE retornar alertas en estado resolved/closed CUANDO un usuario con view_alert_history las consulta, calculando time-to-ack y time-to-resolve por alerta, con caché.

**Descripción:**

 Valida JWT + view_alert_history + segmento. Validación: range ≤ 1 año. Cache lookup. Query Alert WHERE state ∈ {resolved, closed} + filtros. Calcula time-to-ack y time-to-resolve. Build summary.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita historial del último mes
 CUANDO GET con period
 ENTONCES lista de alertas resueltas con métricas
 
 Escenario 1: Rango válido
 DADO period < 1 año
 ENTONCES resultados con time-to-ack calculado

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
   - BReq-006
 * - **UC**
   - UC_ALR_04: Ver Historial de Alertas
 * - **TEST**
   - TST-fr-053-01 (pendiente)

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
   - Versión inicial derivada de UC_ALR_04

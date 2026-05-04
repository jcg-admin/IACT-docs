.. meta::
 :artefacto: FR-059.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-059-01:

====================================================================
FR-059.01: Consultar logs de aplicación con rango máximo de 24 horas
====================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-059.01
 * - **Nombre**
   - Consultar logs de aplicación con rango máximo de 24 horas
 * - **UC Origen**
   - UC_LOG_01: Ver Logs de Aplicación
 * - **Paso UC**
   - Pasos 1-6 del flujo principal
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

 El sistema DEBE retornar logs de aplicación CUANDO un usuario con view_application_logs los consulta, con rango máximo de 24 horas y sanitización de PII.

**Descripción:**

 Valida JWT + view_application_logs. Valida range ≤ 24h (ad-hoc). Query LogStore con filtros. Sanitiza removiendo PII por safety. Retorna 200.

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin consulta logs del último día
 CUANDO GET con filtros y range
 ENTONCES 200 con logs sanitizados
 
 Escenario 1: Rango excedido
 DADO range > 24h
 ENTONCES 422

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-013, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005, BReq-006
 * - **UC**
   - UC_LOG_01: Ver Logs de Aplicación
 * - **TEST**
   - TST-fr-059-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_01

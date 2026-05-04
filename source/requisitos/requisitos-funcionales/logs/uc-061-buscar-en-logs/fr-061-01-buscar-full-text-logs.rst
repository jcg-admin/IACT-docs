.. meta::
 :artefacto: FR-061.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/logs
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-061-01:

====================================================================================
FR-061.01: Búsqueda full-text en logs con rango máximo de 7 días y cap de resultados
====================================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-061.01
 * - **Nombre**
   - Búsqueda full-text en logs con rango máximo de 7 días y cap de resultados
 * - **UC Origen**
   - UC_LOG_03: Buscar en Logs
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

 El sistema DEBE permitir búsqueda full-text en el LogStore CUANDO un usuario autorizado lo solicita, con rango ≤ 7 días, throttling y cap de 1000 resultados.

**Descripción:**

 Valida JWT + RBAC. Valida query + range ≤ 7d. Aplica throttle. Search FTS en LogStore. Sanitiza resultados. Cap a 1000 hits máximo.

----

3. Criterio de Aceptación
-------------------------

::

 DADO admin busca 'ConnectionError' en logs
 CUANDO POST query con date range
 ENTONCES resultados sanitizados (máx 1000)
 
 Escenario 1: Más de 1000 resultados
 DADO 5000 matches
 ENTONCES primeros 1000 con indicador de truncado

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-013, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-005, BReq-006
 * - **UC**
   - UC_LOG_03: Buscar en Logs
 * - **TEST**
   - TST-fr-061-01 (pendiente)

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
   - Versión inicial derivada de UC_LOG_03

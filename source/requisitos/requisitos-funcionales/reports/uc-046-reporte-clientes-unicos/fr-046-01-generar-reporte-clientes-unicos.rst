.. meta::
 :artefacto: FR-046.01
 :tipo: Requisito Funcional
 :dominio: requisitos
 :subdominio: funcionales/reports
 :estado: Aprobado
 :version: 1.0.0
 :fecha_creacion: 2026-05-04
 :autor: NestorMonroy
 :clasificacion: Interno

.. _fr-046-01:

==========================================================================
FR-046.01: Generar reporte de clientes únicos con recurrencia y privacidad
==========================================================================


1. Identificación
-----------------

.. list-table::
 :widths: 25 75

 * - **ID**
   - FR-046.01
 * - **Nombre**
   - Generar reporte de clientes únicos con recurrencia y privacidad
 * - **UC Origen**
   - UC_RPT_17: Reporte de Clientes Únicos
 * - **Paso UC**
   - Pasos 1-12 del flujo principal
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

 El sistema DEBE retornar el conteo de clientes únicos y distribución de recurrencia CUANDO un usuario con view_reports lo solicita, usando hashes para garantizar privacidad y HyperLogLog para alto volumen.

**Descripción:**

 Valida JWT + view_reports + segmento. Query COUNT(DISTINCT client_hash) o HLL si volumen alto. Calcula distribución de recurrencia (calls_per_client). Calcula new vs returning comparando con período anterior. Top N anonimizado (prefijo de hash, no hash completo). CNST-026 garantiza privacidad.

----

3. Criterio de Aceptación
-------------------------

::

 DADO usuario solicita clientes únicos del mes
 CUANDO GET con period
 ENTONCES 200 con count, recurrencia y new_vs_returning
 
 Escenario 1: Alto volumen
 DADO > 1M eventos
 ENTONCES HLL usado para estimación eficiente
 
 Escenario 2: Top N anonimizado
 DADO top 10 clientes frecuentes
 ENTONCES prefijo de hash, no identificador completo

----

4. Reglas y Restricciones
-------------------------

- **CNST aplicables:** CNST-009, CNST-011, CNST-014, CNST-017, CNST-026

----

5. Trazabilidad
---------------

.. list-table::
 :widths: 20 80

 * - **BReq**
   - BReq-001
 * - **UC**
   - UC_RPT_17: Reporte de Clientes Únicos
 * - **TEST**
   - TST-fr-046-01 (pendiente)

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
   - Versión inicial derivada de UC_RPT_17

.. _arq-mod-004-restricciones:

================================================
ARQ_MOD_004 — Restricciones Aplicables
================================================

.. list-table::
 :widths: 15 85
 :header-rows: 1

 * - CNST
   - Descripcion y Aplicacion
 * - CNST_003
   - **BD Dual Inmutable**: Solo lectura de IVR via vw_llamadas.
     Analytics es la unica BD escribible.
 * - CNST_004
   - **Actualizacion Datos ETL**: ETL nocturno, no manual.
     Sin TRUNCATE, solo INSERT/UPDATE controlado.

.. _arq-mod-005-restricciones:

================================================
ARQ_MOD_005 — Restricciones Aplicables
================================================

.. list-table::
 :widths: 15 85
 :header-rows: 1

 * - CNST
   - Descripcion y Aplicacion
 * - CNST_003
   - **BD Dual Inmutable**: Solo consume datos de Analytics.
     NO consulta IVR directamente. NO real-time.
 * - CNST_007
   - **Limites Performance SLA**: Max 10,000 registros por consulta.
     Max 5 exportaciones/dia por usuario. Timeout 30s.

.. _uc-log-02-parte-09:

=================================
Parte 9 — Criterios de aceptacion
=================================

CA-01: Solo logs etl retornados.
CA-02: Filter pipeline_run_id correlaciona.
CA-03: Sanitize.
CA-04: Tail SSE.
CA-05: Sin permiso 403.
CA-06: LogStore timeout 503.

.. list-table::
 :widths: 12 50 38

 * - ID
   - Concepto
   - Tipo
 * - CA-01..02
   - Scope ETL + correlation
   - Funcional
 * - CA-03..04
   - Sanitize / tail
   - varios
 * - CA-05..06
   - Auth/errores
   - varios

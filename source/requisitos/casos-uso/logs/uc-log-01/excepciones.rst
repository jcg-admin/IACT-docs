.. _uc-log-01-parte-05:

==========================
Parte 5 — Excepciones
==========================

EX-01: JWT — 401.
EX-02: Sin permiso — 403.
EX-03: Range > 24h — 400.
EX-04: LogStore timeout — 503.

.. list-table::
 :widths: 12 40 18 30
 :header-rows: 1

 * - ID
   - Condicion
   - Status
   - Audit
 * - EX-01..04
   - varios
   - 401/403/400/503
   - middleware

.. _uc-log-01-parte-04:

==========================
Parte 4 — Flujos alternos
==========================

FA-01: Filter level.
FA-02: Filter service.
FA-03: Tail mode (SSE) — stream live.
FA-04: > 24h → buscar via UC_LOG_03 o
exportar UC_LOG_04.

.. list-table::
 :widths: 12 38 30 20

 * - FA
   - Disparador
   - Comportamiento
   - Notas
 * - FA-01..02
   - Filtros
   - subset
   -
 * - FA-03
   - Tail
   - SSE
   - reuso P-61
 * - FA-04
   - > 24h
   - 400
   - search/export

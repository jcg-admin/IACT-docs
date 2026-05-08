.. _uc-log-01-parte-09:

=================================
Parte 9 — Criterios de aceptacion
=================================

CA-01: List basico.
CA-02: Filter level.
CA-03: Filter service.
CA-04: Range > 24h rechazado.
CA-05: Sanitize PII.
CA-06: Tail mode SSE.
CA-07: LogStore timeout 503.
CA-08: Sin permiso 403.

.. list-table::
 :widths: 12 50 38

 * - ID
   - Concepto
   - Tipo
 * - CA-01..03
   - List + filtros
   - Funcional
 * - CA-04..05
   - Limites + sanitize
   - Robustez/Cumplimiento
 * - CA-06
   - Tail
   - UX
 * - CA-07..08
   - Auth/errores
   - varios

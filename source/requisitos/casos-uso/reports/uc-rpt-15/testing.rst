.. _uc-rpt-15-parte-12:

==================
Parte 12 — Testing
==================

UT-01: HeatmapAssembler construye matriz
desde las filas de
``sp_rpt_centros_xsegmento``.
UT-02: Top reasons ordenado desde las
filas del SP.
UT-03: Top agents desde las filas de
``sp_rpt_centros_transferencia``.

IT-01: Totales correctos.
IT-02: Filtro direction.
IT-03: Cross-segmento → 403.
IT-04: callproc BD_IVR timeout (cualquiera
de los 2 SPs) → 503.

E2E-01: Supervisor identifica loop.

SEC-01: Cross-segmento bloqueado.

Mapeo CA → Tests:

.. list-table::
 :widths: 12 35 53

 * - CA
   - Concepto
   - Tests
 * - CA-01..05
   - Datos
   - IT-01, UT-01..03
 * - CA-06, 10
   - Auth
   - IT-03, SEC-01
 * - CA-07..09
   - Robustez
   - integration

Cobertura: 3 unit, 4 integration, 1 E2E,
1 security. 100% de los 10 CAs.

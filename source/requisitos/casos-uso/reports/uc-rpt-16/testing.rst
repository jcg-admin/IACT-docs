.. _uc-rpt-16-parte-12:

==================
Parte 12 — Testing
==================

UT-01: parser de filas de
``sp_rpt_menu_redirigidos`` mapea
correctamente cada opcion / nodo.
UT-02: parser de filas de
``sp_rpt_menu_centro`` arma la
distribucion menu x centro.
UT-03: parser de filas de
``sp_rpt_cMENU_ERROR`` arma drop-off /
errores por nodo (sin recalculo).

IT-01: Totales correctos.
IT-02: Filtro ivr_id.
IT-03: Cross-segmento → 403.
IT-04: callproc BD_IVR timeout (cualquiera
de los 3 SPs) → 503.

E2E-01: Optimizar IVR via reporte.

SEC-01: Cross-segmento bloqueado.

Mapeo CA → Tests:

.. list-table::
 :widths: 12 35 53

 * - CA
   - Concepto
   - Tests
 * - CA-01..04
   - Datos
   - IT-01, UT-01..03
 * - CA-05, 09
   - Auth
   - IT-03, SEC-01
 * - CA-06..08
   - Robustez
   - integration
 * - CA-10
   - Filtros
   - IT-02

Cobertura: 3 unit, 4 integration, 1 E2E,
1 security. 100% de los 10 CAs.

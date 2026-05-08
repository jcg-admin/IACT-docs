.. _uc-rpt-17-parte-12:

==================
Parte 12 — Testing
==================

UT-01: parser mapea
``rows.distinct_clients_count``
(entregado por el SP, exact o HLL segun
volumen).
UT-02: parser mapea HLL count cuando el
SP indica ``count_method = 'hll'``
(within 1%).
UT-03: parser mapea
``rows.recurrence_distribution``
(buckets 1, 2, 3+).
UT-04: parser mapea
``rows.new_vs_returning`` calculado por
el SP contra periodo prior.
UT-05: parser construye Top N exponiendo
solo prefix del hash.

IT-01: get basico (volumen bajo, exact).
IT-02: get volumen alto (HLL).
IT-03: Cross-segmento → 403.
IT-04: callproc BD_IVR timeout → 503.
IT-05: Cache hit.

E2E-01: Reporte para mes en curso.

SEC-01: Response NO contiene client_id raw.
SEC-02: client_hash sigue siendo
calculable solo con tenant_salt.
SEC-03: Cross-segmento bloqueado.

Mapeo CA → Tests:

.. list-table::
 :widths: 12 35 53

 * - CA
   - Concepto
   - Tests
 * - CA-01..02
   - Distinct
   - UT-01, UT-02, IT-01, IT-02
 * - CA-03..04
   - Recurrence/comparative
   - UT-03, UT-04
 * - CA-05
   - Top N anonimizado
   - UT-05
 * - CA-06
   - Sin PII
   - SEC-01, SEC-02
 * - CA-07, 11
   - Auth
   - IT-03, SEC-03
 * - CA-08..10
   - Robustez
   - integration

Cobertura: 5 unit, 5 integration, 1 E2E,
3 security. 100% de los 11 CAs.

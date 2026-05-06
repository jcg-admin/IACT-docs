.. _uc-adm-02-parte-12:

==================
Parte 12 — Testing
==================

UT-01: Validator codename snake_case valido.
UT-02: Validator codename caracteres invalidos.
UT-03: Validator codename duplicado.
UT-04: Validator module invalido.

IT-01: Crear funcion + audit + reload catalog.
IT-02: Update description → funcion actualizada.
IT-03: Deactivate → is_active=False.
IT-04: Asignacion historica preservada tras deactivate.
IT-05: Listado por module y state.

E2E-01: Admin crea funcion, la asigna a grupo,
desactiva; verifica que nueva asignacion
de la funcion queda bloqueada.

SEC-01: Sin AGR-010 → 403.
SEC-02: Audit inmutable verificado post-cambio.

Mapeo CA → Tests:

.. list-table::
 :widths: 12 35 53

 * - CA
   - Concepto
   - Tests
 * - CA-01..04
   - CRUD + validation
   - IT-01, UT-01..04
 * - CA-05
   - Update parcial
   - IT-02
 * - CA-06..07
   - Deactivate
   - IT-03, IT-04
 * - CA-08
   - Audit
   - IT-01, SEC-02
 * - CA-09
   - Auth
   - SEC-01
 * - CA-10
   - Reload
   - IT-01
 * - CA-11
   - Listado
   - IT-05

Cobertura: 4 unit, 5 integration, 1 E2E,
2 security. 100% de los 11 CAs.

.. _uc-adm-03-parte-12:

==================
Parte 12 — Testing
==================

UT-01: SoDPreCheckValidator — sin conflicto OK.
UT-02: SoDPreCheckValidator — conflicto detectado.
UT-03: SystemGroupGuard — is_system=True OK.
UT-04: SystemGroupGuard — is_system=False → 403.

IT-01: Agregar funcion → composicion actualizada + audit.
IT-02: Remover funcion → composicion actualizada + audit.
IT-03: Agregar funcion ya existente → 409.
IT-04: Agregar funcion con conflicto SoD → 400.
IT-05: GET /impact/ retorna usuarios afectados.
IT-06: PermissionsEngine recalcula tras cambio.

E2E-01: Admin agrega funcion a AGR-009; verifica
que usuario con AGR-009 adquiere nueva funcion en
su effective_set.

SEC-01: Sin AGR-009 → 403.
SEC-02: AGR custom (is_system=False) → 403.
SEC-03: Audit inmutable verificado post-cambio.

Mapeo CA → Tests:

.. list-table::
 :widths: 12 35 53

 * - CA
   - Concepto
   - Tests
 * - CA-01..05
   - CRUD + validation
   - IT-01..04, UT-01..04
 * - CA-06
   - Recalculo
   - IT-06, E2E-01
 * - CA-07
   - Impact preview
   - IT-05
 * - CA-08
   - Audit
   - IT-01, SEC-03
 * - CA-09
   - Auth
   - SEC-01
 * - CA-10
   - Engine reload
   - IT-06

Cobertura: 4 unit, 6 integration, 1 E2E,
3 security. 100% de los 10 CAs.

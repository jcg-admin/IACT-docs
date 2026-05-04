.. _uc-adm-01-parte-12:

==================
Parte 12 — Testing
==================

UT-01: DisjointSetValidator — conjuntos disjuntos OK.
UT-02: DisjointSetValidator — interseccion detectada.
UT-03: FunctionValidator — funcion inexistente.
UT-04: FunctionValidator — todas validas.

IT-01: Crear SoDRule + audit + enforcement reload.
IT-02: Update incrementa version.
IT-03: Disable → INACTIVE; enforcement recarga.
IT-04: Reactivar → ACTIVE; enforcement recarga.
IT-05: Lista con filtro state=ACTIVE.

E2E-01: Admin crea, actualiza y desactiva regla;
verifica que nueva asignacion es bloqueada/liberada.

SEC-01: Sin AGR-009 → 403.
SEC-02: Audit inmutable verificado post-cambio.

Mapeo CA → Tests:

.. list-table::
 :widths: 12 35 53

 * - CA
   - Concepto
   - Tests
 * - CA-01..04
   - CRUD + validation
   - IT-01..02, UT-01..04
 * - CA-05
   - Update version
   - IT-02
 * - CA-06..07
   - State lifecycle
   - IT-03, IT-04
 * - CA-08
   - Audit
   - IT-01, SEC-02
 * - CA-09
   - Auth
   - SEC-01
 * - CA-10
   - Enforcement reload
   - IT-01, IT-03

Cobertura: 4 unit, 5 integration, 1 E2E,
2 security. 100% de los 10 CAs.
